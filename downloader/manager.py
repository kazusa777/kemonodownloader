import os
import aiohttp
import aiofiles
import asyncio


async def download_file(session, url, save_path, sem):
    async with sem:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(save_path, "wb") as f:
                        await f.write(await resp.read())
                    print(f"✅ 下載完成: {save_path}")
                else:
                    print(f"❌ 下載失敗: {url} ({resp.status})")
        except Exception as e:
            print(f"❌ 下載異常: {url} - {e}")

async def save_post_concurrent(post, base_path, session, sem):
    folder_name = post["title"]
    post_path = os.path.join(base_path, folder_name)
    os.makedirs(post_path, exist_ok=True)

    # 下載圖片（高並發任務佇列）
    download_tasks = []
    for img in post["images"]:
        save_path = os.path.join(post_path, img["name"])
        download_tasks.append(download_file(session, img["url"], save_path, sem))
    if download_tasks:
        await asyncio.gather(*download_tasks)

    # 下載其他檔案（按需）
    for f in post.get("files", []):
        save_path = os.path.join(post_path, f["name"])
        await download_file(session, f["url"], save_path, sem)

    # 保存外部連結
    if post.get("external_links"):
        links_path = os.path.join(post_path, "external_links.txt")
        async with aiofiles.open(links_path, "w", encoding="utf-8") as f:
            await f.write("\n".join(post["external_links"]))
        print(f"📝 已儲存：{links_path}")


async def download_streamed_posts(post_stream, base_path, concurrency=10):
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        async for post in post_stream:
            # 對每一個新獲取到的貼文立刻啟動並發下載
            await save_post_concurrent(post, base_path, session, sem)
