import os
import re
import json
import aiohttp
import aiofiles
from asyncio import Semaphore, create_task
from downloader.tasks import FileTask
from utils import sanitize_filename, rename_list, save_post_content_to_txt
from utils.meta_dir import load_status

# ========= 全域常數 =========
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
BASE = "https://kemono.cr"
DATA_BASE = f"{BASE}/data"

# 所有 API 請求都統一代 Accept:text/css；詳情頁/列表頁面都按 JSON 解析，但忽略 MIME 檢查
DEFAULT_HEADERS = {
    "Accept": "text/css",
    "User-Agent": USER_AGENT,
    "Referer": BASE,
}

# ========= 公用工具 =========
async def refresh_cookie(session: aiohttp.ClientSession, user: str | None = None):
    """
    訪問主畫面以刷新 DDG 短效 cookie。
    user 傳入類似 'fanbox/user/6668233'；如果是空的就訪問根站
    """
    home_url = f"{BASE}/{user}" if user else BASE
    try:
        async with session.get(home_url, headers=DEFAULT_HEADERS) as resp:
            print(f"[Cookie] 刷新 cookie: {resp.status} {home_url}")
    except Exception as e:
        print(f"[Cookie] 刷新 cookie 出錯: {e}")

async def get_json(session: aiohttp.ClientSession, url: str, user_for_refresh: str | None, *, retry_once: bool = True):
    """
    統一請求 JSON：
    - 先請求一次；
    - 非 200 或 JSON 解析失敗時，刷新 cookie 然後再試一次（可配）。
    - 返回 (status, data or None)
    """
    async def _one_try():
        async with session.get(url, headers=DEFAULT_HEADERS) as resp:
            status = resp.status
            if status != 200:
                return status, None
            try:
                data = await resp.json(content_type=None)  # 忽略 MIME 類型檢查
                return 200, data
            except Exception as e:
                # 印出前 200 字方便排查
                body = await resp.text()
                # print(f"[JSON] 解析失敗：{e}\n[JSON] Body preview: {body[:200]}")
                return 200, None

    status, data = await _one_try()
    if (status != 200 or data is None) and retry_once:
        print(f"[Retry] {url} 首次失敗(status={status}, data={type(data).__name__}), 嘗試刷新 cookie 後重試…")
        await refresh_cookie(session, user_for_refresh)
        status, data = await _one_try()
    return status, data

def extract_external_links(html: str) -> list[str]:
    if not html:
        return []
    # 支援 mega/drive/dropbox/puu.sh；注意反斜槓轉義
    return re.findall(r'https?://(?:mega|drive|dropbox|puu\.sh)[^\s"<>]+', html or "")

# ========= 1) 拉取貼文列表（含翻頁 & 失敗刷新） =========
async def GetPosts(user: str, session: aiohttp.ClientSession) -> list[dict]:
    """
    user 形如: 'fanbox/user/6668233/posts' 或 'fanbox/user/6668233'
    這裡統一拼成 /api/v1/{user}/posts
    """
    user_norm = user.rstrip("/")
    if not user_norm.endswith("/posts"):
        user_norm = f"{user_norm}/posts"

    posts = []
    offset = 0

    while True:
        url = f"{BASE}/api/v1/{user_norm}?o={offset}"
        print(f"[List] GET {url}")
        status, batch = await get_json(session, url, user_for_refresh=user, retry_once=True)
        if status != 200:
            print(f"[List] HTTP {status}，結束。")
            break
        if not batch:
            print("[List] 空頁，結束。")
            break
        posts.extend(batch)
        offset += 50

    print(f"[List] 共獲取 {len(posts)} 條")
    return posts

# ========= 2) 產生選擇列表 =========
async def get_post_choices(user_url: str, day_mode: int = 1):
    user = user_url.split('https://kemono.cr/')[-1]
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        posts = await GetPosts(user, session)
        choices = []
        for post in posts:
            published = post.get("published") or ""
            day = published.split("T")[0] if "T" in published else published or "unknown"
            title = sanitize_filename(post.get("title", "untitled"))
            if day_mode == 1:
                display = f"{day}_{title}"
            elif day_mode == 2:
                display = f"{title}_{day}"
            else:
                display = title
            choices.append({"id": post["id"], "display": display})
        return choices

# ========= 3) 擷取附件（可選按標題過濾） =========
async def extract_attachments_urls(
    user_url: str,
    selected_titles: list = None,  # None=全部, 否則只下載這些title
    day_mode: int = 0
):
    user = user_url.split('https://kemono.cr/')[-1]
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        posts = await GetPosts(user, session)

        def post_key(post):
            published = post.get("published") or ""
            day = published.split("T")[0] if "T" in published else published or "unknown"
            title = sanitize_filename(post.get("title", "untitled"))
            if day_mode == 1:
                return f"{day}_{title}"
            elif day_mode == 2:
                return f"{title}_{day}"
            else:
                return title

        if selected_titles is not None:
            posts = [p for p in posts if post_key(p) in selected_titles]

        for post in posts:
            post_id = post["id"]
            published = post.get("published") or ""
            day = published.split("T")[0] if "T" in published else published or "unknown"
            title = sanitize_filename(post.get("title", "untitled"))
            user_id = post["user"]
            service = post["service"]

            folder_title = post_key(post)
            post_url_api = f'{BASE}/api/v1/{service}/user/{user_id}/post/{post_id}'
            url_out = f'{BASE}/{service}/user/{user_id}/post/{post_id}'

            status, data = await get_json(session, post_url_api, user_for_refresh=f"{service}/user/{user_id}", retry_once=True)
            if status != 200 or not data:
                print(f"[Detail] 拉取失敗: {status} {post_url_api}")
                continue

            html_content = (data.get("post") or {}).get("content", "")
            file = (data.get("post") or {}).get("file")
            attachments = [file] + (data.get("post") or {}).get("attachments", []) if file else (data.get("post") or {}).get("attachments", [])

            image_raw, other_files = [], []
            for att in attachments:
                if not att:
                    continue
                name = att.get("name", "")
                path = att.get("path", "")
                if not name or not path:
                    continue
                ext = name.lower().split('.')[-1]
                url = DATA_BASE + path
                (image_raw if ext in ("jpg", "jpeg", "png", "gif", "webp") else other_files).append({"url": url, "name": name})

            images = rename_list(image_raw)
            external_links = extract_external_links(html_content)

            yield {
                "title": folder_title,
                "url": url_out,
                "id": post_id,
                "day": day,
                "images": images,
                "files": other_files,
                "external_links": external_links
            }

# ========= 4) 舊介面（按 ID 過濾） =========
async def extract_attachments_urls_by_id(
    user_url: str,
    selected_ids: list = None,  # None=全部，指定id只下載部分
    day_mode: int = 0
):
    user = user_url.split('https://kemono.cr/')[-1]
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        posts = await GetPosts(user, session)
        if selected_ids is not None:
            posts = [post for post in posts if post["id"] in selected_ids]

        for post in posts:
            post_id = post["id"]
            published = post.get("published") or ""
            day = published.split("T")[0] if "T" in published else published or "unknown"
            title = sanitize_filename(post.get("title", "untitled"))
            user_id = post["user"]
            service = post["service"]

            folder_title = title if day_mode == 0 else (f"{day}_{title}" if day_mode == 1 else f"{title}_{day}")
            post_url_api = f'{BASE}/api/v1/{service}/user/{user_id}/post/{post_id}'
            url_out = f'{BASE}/{service}/user/{user_id}/post/{post_id}'

            status, data = await get_json(session, post_url_api, user_for_refresh=f"{service}/user/{user_id}", retry_once=True)
            if status != 200 or not data:
                print(f"[Detail] 拉取失敗: {status} {post_url_api}")
                continue

            html_content = (data.get("post") or {}).get("content", "")
            file = (data.get("post") or {}).get("file")
            attachments = [file] + (data.get("post") or {}).get("attachments", []) if file else (data.get("post") or {}).get("attachments", [])

            image_raw, other_files = [], []
            for att in attachments:
                if not att:
                    continue
                name = att.get("name", "")
                path = att.get("path", "")
                if not name or not path:
                    continue
                ext = name.lower().split('.')[-1]
                url = DATA_BASE + path
                (image_raw if ext in ("jpg", "jpeg", "png", "gif", "webp") else other_files).append({"url": url, "name": name})

            images = rename_list(image_raw)
            external_links = extract_external_links(html_content)

            yield {
                "id": post_id,
                "title": folder_title,
                "service": service,
                "published": published,
                "url": url_out,
                "day": day,
                "images": images,
                "files": other_files,
                "external_links": external_links,
                "content": html_content,
                "user": user_id
            }

# ========= 5) 流式迭代 & 並發拉取詳情（保留但對齊 headers/重試） =========
async def iter_posts(user: str, session: aiohttp.ClientSession):
    """
    非同步分頁獲取指定使用者的貼文列表（產生器）。
    user 形如 'fanbox/user/6668233'
    """
    offset = 0
    base_url = f"{BASE}/api/v1/{user}"
    while True:
        url = f"{base_url}?o={offset}"
        status, batch = await get_json(session, url, user_for_refresh=user, retry_once=True)
        if status != 200:
            print(f"[Iter] HTTP {status} 終止。")
            break
        if not batch:
            break
        for post in batch:
            yield post
        offset += 50

async def stream_post_details(user_url, day_mode=0, selected_ids=None, logger=print):
    user = user_url.split('https://kemono.cr/')[-1]
    sem = Semaphore(5)
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        async for post in iter_posts(user, session):
            if selected_ids and post["id"] not in selected_ids:
                continue
            create_task(fetch_and_yield_post(post, session, sem, day_mode, logger))

async def fetch_and_yield_post(
    post, session, sem, day_mode, logger,
    task_queue=None, save_base_path=None,
    on_new_file=None, post_file_counter=None, post_file_done_callback=None, signal_host=None
):
    post_id = post["id"]
    user_id = post["user"]
    service = post["service"]

    # meta_dir 跳過
    try:
        status_meta = load_status(user_id)
        if status_meta.get(str(post_id)) == "finished":
            logger(f"已完成（meta_dir），跳過：{post.get('title')}")
            return
    except Exception:
        pass

    folder_title = sanitize_filename(post.get("title", "untitled"))
    if save_base_path:
        # 處理重複目錄 / .post_id
        original_folder_path = os.path.join(save_base_path, folder_title)
        folder_path = original_folder_path
        suffix = 1
        while os.path.exists(folder_path):
            post_id_path = os.path.join(folder_path, ".post_id")
            if os.path.exists(post_id_path):
                try:
                    async with aiofiles.open(post_id_path, "r", encoding="utf-8") as f:
                        existing_id = (await f.read()).strip()
                        if existing_id == post_id:
                            break
                except Exception:
                    pass
            folder_path = f"{original_folder_path}_{suffix}"
            suffix += 1
        os.makedirs(folder_path, exist_ok=True)
        path = os.path.join(folder_path, ".post_id")
        try:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(post_id))
        except Exception as e:
            logger(f"寫入 .post_id 失敗: {e}")
    else:
        folder_path = None  # 不落地時允許為空

    async with sem:
        try:
            post_url_api = f"{BASE}/api/v1/{service}/user/{user_id}/post/{post_id}"
            status, data = await get_json(session, post_url_api, user_for_refresh=f"{service}/user/{user_id}", retry_once=True)
            if status != 200 or not data:
                logger(f"貼文詳情拉取失敗: HTTP {status} {post_url_api}")
                return

            content = (data.get("post") or {}).get("content", "")
            file = (data.get("post") or {}).get("file")
            attachments = [file] + (data.get("post") or {}).get("attachments", []) if file else (data.get("post") or {}).get("attachments", [])

            image_raw, other_files = [], []
            for att in attachments:
                if not att:
                    continue
                name = att.get("name", "")
                path = att.get("path", "")
                if not name or not path:
                    continue
                ext = name.lower().split('.')[-1]
                url = DATA_BASE + path
                (image_raw if ext in ("jpg", "jpeg", "png", "gif", "webp") else other_files).append({"url": url, "name": name})

            images = rename_list(image_raw)
            external_links = extract_external_links(content)

            tasks = []
            if task_queue and folder_path:
                for img in images:
                    tasks.append(FileTask(
                        url=img["url"],
                        save_path=os.path.join(folder_path, img["name"]),
                        post_id=post_id,
                        user_id=user_id,
                        file_type="image"
                    ))
                for f in other_files:
                    tasks.append(FileTask(
                        url=f["url"],
                        save_path=os.path.join(folder_path, f["name"]),
                        post_id=post_id,
                        user_id=user_id,
                        file_type="file"
                    ))
                if post_file_counter is not None:
                    post_file_counter[(user_id, post_id)] = len(tasks)
                for task in tasks:
                    await task_queue.put(task)
                if signal_host and hasattr(signal_host, "file_max_signal"):
                    signal_host.file_max_signal.emit(len(tasks))

                # 外部連結與 content.txt
                if external_links:
                    links_path = os.path.join(folder_path, "external_links.txt")
                    try:
                        async with aiofiles.open(links_path, "w", encoding="utf-8") as f:
                            await f.write("\n".join(external_links))
                    except Exception as e:
                        logger(f"儲存失敗: {e}")
                try:
                    await save_post_content_to_txt(folder_path, post)
                except Exception as e:
                    logger(f"儲存 content.txt 失敗: {e}")

        except Exception as e:
            logger(f"貼文詳情拉取異常: {e}")
