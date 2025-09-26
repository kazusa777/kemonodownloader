import logging
log = logging.getLogger(__name__)

import re
from bs4 import BeautifulSoup
import aiofiles
import unicodedata
import platform
import os

def sanitize_filename(title: str, max_length=150) -> str:
    """將任意字串轉換為安全的 Windows 檔名"""
    title = re.sub(r'[\\/:*?"<>|]', '_', title)
    title = ''.join(c for c in title if unicodedata.category(c)[0] != "C")  # 控制符
    title = ''.join(c for c in title if unicodedata.category(c) != "So")  # emoji
    title = title.rstrip(' .')
    return title[:max_length].rstrip(' .')


def rename_list(previews):
    total_files = len(previews)
    digits = 1 if total_files < 10 else (2 if total_files < 100 else 3)

    for i, preview in enumerate(previews):
        file_extension = preview["name"].split(".")[-1]
        new_name = f"{(i + 1):0{digits}d}.{file_extension}"
        preview["name"] = new_name

    return previews

def set_hidden_windows(path):
    if platform.system() == "Windows":
        import ctypes
        FILE_ATTRIBUTE_HIDDEN = 0x02
        try:
            ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            # print(f"設定隱藏屬性失敗: {e}")
            log.info(f"設定隱藏屬性失敗: {e}")

async def save_post_content_to_txt(folder_path, post):
    """
    保存貼文內容為 content.txt
    """
    file_path = os.path.join(folder_path, "content.txt")
    lines = []
    lines.append(f"標題: {post.get('title','')}")
    lines.append(f"發布時間: {post.get('day','')}")
    lines.append(f"貼文連結: {post.get('url','')}\n")
    lines.append("="*30 + "\n")

    content_html = post.get("content", "")
    if content_html:
        # 提取純文字
        soup = BeautifulSoup(content_html, "html.parser")
        text_content = soup.get_text(separator='\n', strip=True)
        lines.append("文字：\n")
        lines.append(text_content)
        lines.append("\n")
        # 額外提取所有圖片和連結
        images = [img.get("src") for img in soup.find_all("img") if img.get("src")]
        if images:
            lines.append("貼文內圖片連結：")
            lines += [f"- {url}" for url in images]
        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        if links:
            lines.append("貼文內連結：")
            lines += [f"- {url}" for url in links]
    else:
        lines.append("貼文是空的。\n")

    lines.append("\n附件：")
    for f in post.get("files", []):
        lines.append(f"- {f.get('name','文件')} : {f.get('url','')}")
    lines.append("\n外部連結：")
    for link in post.get("external_links", []):
        lines.append(f"- {link}")

    content_str = "\n".join(lines)
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(content_str)


def format_title_with_date(title: str, published: str, day_mode: int) -> str:
    """
    根據日期格式化標題（用於創建資料夾名稱）：
        0 - 無前輟/後輟
        1 - 日期前輟：2025-06-17_標題
        2 - 日期後輟：標題_2025-06-17
    """
    try:
        day = published.split("T")[0]
    except Exception:
        day = "unknown"

    if day_mode == 1:
        return f"{day}_{title}"
    elif day_mode == 2:
        return f"{title}_{day}"
    return title
