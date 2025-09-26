import logging

log = logging.getLogger(__name__)
from pathlib import Path
import os, aiohttp, aiofiles, asyncio
from scraper.kemono import fetch_and_yield_post, extract_attachments_urls_by_id


# --- 下载图片 ---
async def download_image(session, url, save_path, sem, pause_event=None, stop_event=None, logger=None, error_signal=None):
    from pathlib import Path
    temp_path = save_path + ".temp"
    async with sem:
        for attempt in range(1, 4):
            if stop_event and stop_event.is_set():
                if logger: logger("⛔ 偵測到終止，退出圖片下載")
                return
            while pause_event and not pause_event.is_set():
                await asyncio.sleep(0.2)
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(temp_path, "wb") as f:
                            await f.write(await resp.read())
                        os.replace(temp_path, save_path)
                        msg = f"✅ 圖片下載完成: {Path(save_path).as_posix()}"
                        if logger: logger(msg)
                        return
                    else:
                        raise Exception(f"{resp.status}")
            except Exception as e:
                if attempt < 3:
                    if logger: logger(f"⚠️ 圖片下載失敗（第 {attempt} 次），重試中: {url}")
                    await asyncio.sleep(1)
                else:
                    msg = f"❌ 圖片下載失敗（已重試 3 次）: {url} - {e}"
                    if logger: logger(msg)
                    await record_error(save_path, error_signal=error_signal, url=url)


# --- 下载大文件 ---
async def download_with_resume(session, url, save_path, sem, chunk_size=1024 * 1024, pause_event=None, stop_event=None,
                               logger=None, error_signal=None):
    from pathlib import Path
    temp_path = save_path + ".temp"
    async with sem:
        for attempt in range(1, 4):
            if stop_event and stop_event.is_set():
                if logger: logger("⛔ 偵測到終止，退出大文件下載")
                return
            while pause_event and not pause_event.is_set():
                await asyncio.sleep(0.2)
            try:
                file_size = os.path.getsize(temp_path) if os.path.exists(temp_path) else 0
                headers = {"Range": f"bytes={file_size}-"} if file_size else {}
                async with session.get(url, headers=headers) as resp:
                    if resp.status not in (200, 206):
                        raise Exception(f"{resp.status}")
                    mode = "ab" if file_size else "wb"
                    async with aiofiles.open(temp_path, mode) as f:
                        async for chunk in resp.content.iter_chunked(chunk_size):
                            if stop_event and stop_event.is_set():
                                if logger: logger("⛔ 偵測到終止（大文件區塊）")
                                return
                            while pause_event and not pause_event.is_set():
                                await asyncio.sleep(0.2)
                            await f.write(chunk)
                    total = int(resp.headers.get("Content-Range", "").split("/")[-1]
                                or resp.headers.get("Content-Length", 0) or 0)
                    final_size = os.path.getsize(temp_path)
                    if total and final_size >= total:
                        os.replace(temp_path, save_path)
                        if logger: logger(f"✅ 大文件下载完成: {Path(save_path).as_posix()}")
                    else:
                        if logger: logger(f"⚠️ 文件部分保存: {Path(temp_path).as_posix()}")
                    return
            except Exception as e:
                if attempt < 3:
                    if logger: logger(f"⚠️ 大文件下載失敗（第 {attempt} 次），重試中: {url}")
                    await asyncio.sleep(1)
                else:
                    if logger: logger(f"❌ 大文件下載失敗（已重試 3 次）: {url} - {e}")
                    await record_error(save_path, error_signal=error_signal, url=url)


async def download_worker(
        task_queue, sem, session,
        pause_event, stop_event, update_status, logger,
        file_progress_signal=None,
        post_file_counter=None,
        post_file_done=None,
        cancelled_posts=None,
        error_signal=None
):
    """
    單一檔案下載 worker，不斷從任務佇列中拉取 FileTask 進行處理。
    支援暫停、終止控制。

    參數：
        task_queue (asyncio.Queue): 下載任務佇列
        sem (asyncio.Semaphore): 並發下載控制信號量
        session (aiohttp.ClientSession): aiohttp 會話
        pause_event / stop_event: 控制標誌
        update_status (Callable): 狀態更新回呼
        logger (Callable): 日誌函式
    """
    file_done = 0
    while True:
        try:
            task = await task_queue.get()

            if stop_event and stop_event.is_set():
                if logger: logger("⛔ 終止指令下達，worker 停止")
                break

            while pause_event and not pause_event.is_set():
                await asyncio.sleep(0.3)

            if os.path.exists(task.save_path):
                if logger: logger(f"⏭️ 已存在，跳過: {task.save_path}")
                if file_progress_signal:
                    file_progress_signal.emit(1)
                task_queue.task_done()
                continue

            async with sem:
                # 选择下载方式
                if task.file_type == "image":
                    await download_image(session, task.url, task.save_path, sem, pause_event, stop_event, logger,error_signal)
                else:
                    await download_with_resume(session, task.url, task.save_path, sem,
                                               pause_event=pause_event,
                                               stop_event=stop_event,
                                               logger=logger,
                                               error_signal=error_signal)

                if update_status:
                    await update_status(task.user_id, task.post_id, finished=False)  # 可设置为 per-file 状态

            file_done += 1
            if file_progress_signal:
                file_progress_signal.emit(1)
                # print("完成数+1")
            task_queue.task_done()

            key = (task.user_id, task.post_id)
            post_file_done[key] = post_file_done.get(key, 0) + 1

            if post_file_done[key] == post_file_counter.get(key, 0):
                if cancelled_posts and key in cancelled_posts:
                    if logger:
                        logger(f"⛔ 已取消任務，不標記為完成：{key}")
                elif stop_event and stop_event.is_set():
                    if logger:
                        logger(f"⛔ 偵測到終止標誌，跳過標記完成：{key}")
                else:
                    if update_status:
                        await update_status(task.user_id, task.post_id, finished=True)
        except Exception as e:
            if logger:
                logger(f"❌ 下載任務異常: {e}")
            # record_error(task.save_path, error_signal=error_signal, url=task.url)
            task_queue.task_done()


# --- 下載主循環 ---
async def download_streamed_posts(
        url=None,
        post_stream=None,
        base_path=None,
        concurrency=10,
        update_status=None,
        pause_event=None,
        stop_event=None,
        logger=None,
        day_mode=0,
        selected_ids=None,
        signal_host=None,
        error_signal=None
):
    """
    以檔案為單位進行下載，使用任務佇列驅動並行 worker。
    貼文進度與檔案進度皆即時訊號傳遞。
    """
    cancelled_posts = set()

    post_total = 0
    post_done = 0
    file_total = 0
    file_done = 0
    task_queue = asyncio.Queue()
    sem = asyncio.Semaphore(concurrency)
    post_file_counter = {}
    post_file_done = {}

    file_max_signal = getattr(signal_host, "file_max_signal", None)
    file_progress_signal = getattr(signal_host, "file_progress_signal", None)
    post_max_signal = getattr(signal_host, "post_max_signal", None)
    post_progress_signal = getattr(signal_host, "post_progress_signal", None)

    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(
                download_worker(
                    task_queue, sem, session,
                    pause_event, stop_event, update_status, logger,
                    file_progress_signal=file_progress_signal,
                    post_file_counter=post_file_counter,
                    post_file_done=post_file_done,
                    cancelled_posts=cancelled_posts,
                    error_signal=error_signal
                )
            )
            for _ in range(concurrency)
        ]

        fetch_sem = asyncio.Semaphore(5)

        if post_stream is None and selected_ids is not None:
            post_stream = extract_attachments_urls_by_id(url, selected_ids=selected_ids, day_mode=day_mode)

        if post_stream is not None:
            if isinstance(post_stream, list):
                async def wrap_list():
                    for item in post_stream:
                        yield item

                post_stream = wrap_list()
            if logger: logger("📦 使用 post_stream 下載")

            async for post in post_stream:
                if stop_event and stop_event.is_set():
                    key = (post["user"], post["id"])
                    cancelled_posts.add(key)
                    if logger: logger(f"⛔ 檢測到終止，中斷貼文：{post.get('title')}（{key}）")
                    break

                while pause_event and not pause_event.is_set():
                    await asyncio.sleep(0.2)

                post_total += 1
                if post_max_signal:
                    post_max_signal.emit(post_total)

                def count_file(n):
                    nonlocal file_total
                    file_total += n
                    if file_max_signal:
                        file_max_signal.emit(n)

                await fetch_and_yield_post(
                    post, session, fetch_sem, day_mode, logger,
                    task_queue, base_path, on_new_file=count_file,
                    post_file_counter=post_file_counter,
                    signal_host=signal_host
                )

                post_done += 1
                if post_progress_signal:
                    post_progress_signal.emit(post_done)
        else:
            if logger: logger("❌ 無下載源（post_stream 和 selected_ids 均為空）")

        await task_queue.join()
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

        if logger:
            logger("✅ 全部文件下載完成")


def record_error(path, error_signal=None, url=None):
    try:
        posix_path = Path(path).as_posix()

        log_path = os.path.join(os.path.dirname(path), "error.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{posix_path} | {url or 'N/A'}\n")
        if error_signal:
            error_signal.emit([f"{posix_path} | {url or 'N/A'}"])
    except Exception as e:
        print(f"❌ 寫入 error.txt 失敗: {e}")
