import logging
log = logging.getLogger(__name__)


from utils.meta_dir import load_status, save_status

async def update_status(user_id, post_id, finished=False):
    status = load_status(user_id)
    status[str(post_id)] = "finished" if finished else "pending"
    save_status(user_id, status)
    # print(f"[META] 状态已保存: {user_id} -> {post_id} = {'finished' if finished else 'pending'}")
