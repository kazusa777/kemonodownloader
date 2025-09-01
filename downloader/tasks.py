from dataclasses import dataclass


@dataclass
class FileTask:
    url: str  # 下载地址
    save_path: str  # 本地保存路径
    post_id: str  # 所属帖子 ID（用于状态）
    user_id: str  # 所属用户（用于状态存储）
    file_type: str = "file"  # 可为 "image" / "file" / "external"
