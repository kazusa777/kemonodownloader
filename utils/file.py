import logging
log = logging.getLogger(__name__)

import re
from bs4 import BeautifulSoup
import aiofiles
import unicodedata
import platform
import os

def sanitize_filename(title: str, max_length=150) -> str:
    """将任意字符串转换为安全的 Windows 文件名"""
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
            # print(f"设置隐藏属性失败: {e}")
            log.info(f"设置隐藏属性失败: {e}")

async def save_post_content_to_txt(folder_path, post):
    """
    保存帖子内容为 content.txt
    """
    file_path = os.path.join(folder_path, "content.txt")
    lines = []
    lines.append(f"标题: {post.get('title','')}")
    lines.append(f"发布时间: {post.get('day','')}")
    lines.append(f"原帖链接: {post.get('url','')}\n")
    lines.append("="*30 + "\n")

    content_html = post.get("content", "")
    if content_html:
        # 提取纯文本
        soup = BeautifulSoup(content_html, "html.parser")
        text_content = soup.get_text(separator='\n', strip=True)
        lines.append("正文：\n")
        lines.append(text_content)
        lines.append("\n")
        # 额外提取所有图片和超链接
        images = [img.get("src") for img in soup.find_all("img") if img.get("src")]
        if images:
            lines.append("正文内图片链接：")
            lines += [f"- {url}" for url in images]
        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        if links:
            lines.append("正文内超链接：")
            lines += [f"- {url}" for url in links]
    else:
        lines.append("正文为空。\n")

    lines.append("\n附件：")
    for f in post.get("files", []):
        lines.append(f"- {f.get('name','文件')} : {f.get('url','')}")
    lines.append("\n外链：")
    for link in post.get("external_links", []):
        lines.append(f"- {link}")

    content_str = "\n".join(lines)
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(content_str)


def format_title_with_date(title: str, published: str, day_mode: int) -> str:
    """
    根据日期模式格式化标题（用于创建文件夹名）：
        0 - 无前缀/后缀
        1 - 日期前缀：2025-06-13_标题
        2 - 日期后缀：标题_2025-06-13
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