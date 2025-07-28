import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# 请替换为您自己的 api_id, api_hash 和 session 文件名
api_id = 1234567  # 替换为您的 api_id
api_hash = 'YOUR_API_HASH'  # 替换为您的 api_hash
session_file = 'my_telegram_session'

# 您想要获取帖子的 channel 的用户名或链接
# 例如 'test_channel_username' 或 'https://t.me/test_channel_username'
target_channel = 'https://t.me/malinkanglife' # 替换为目标 channel 的用户名

# 要获取的帖子数量
post_limit = 10

def format_size(size_bytes):
    """将文件大小从字节转换为更易读的格式 (KB, MB, GB)"""
    if size_bytes is None:
        return "N/A"
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024*1024*1024):.2f} GB"
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024*1024):.2f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes} bytes"

async def main():
    """
    主函数，用于连接 Telegram 并获取 channel 帖子及其媒体文件。
    """
    async with TelegramClient(session_file, api_id, api_hash) as client:
        print("成功连接到 Telegram！")

        try:
            # 获取 channel 实体
            channel_entity = await client.get_entity(target_channel)
            print(f"成功找到 Channel: {channel_entity.title}")

            # 获取历史消息
            history = await client(GetHistoryRequest(
                peer=channel_entity,
                limit=post_limit,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))

            if not history.messages:
                print("该 Channel 中没有找到任何帖子。")
                return

            print(f"\n以下是最新的 {len(history.messages)} 条帖子：\n")
            # 遍历并打印每条消息
            for message in history.messages:
                print(f"帖子 ID: {message.id}")
                print(f"发布时间: {message.date.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 打印帖子文本内容
                if message.message:
                    print(f"内容:\n{message.message}")
                
                # ==================== 新增部分：检查和列出媒体文件 ====================
                if message.media:
                    print("媒体文件:")
                    
                    # 情况一：媒体是图片
                    if isinstance(message.media, MessageMediaPhoto):
                        print("  - 类型: 图片 (Photo)")

                    # 情况二：媒体是文件、视频、音频等
                    elif isinstance(message.media, MessageMediaDocument):
                        doc = message.media.document
                        
                        file_name = "N/A"
                        # 从属性中提取文件名
                        for attr in doc.attributes:
                            if hasattr(attr, 'file_name'):
                                file_name = attr.file_name
                                break
                        
                        print(f"  - 类型: 文件 (Document)")
                        print(f"  - 文件名: {file_name}")
                        print(f"  - 文件大小: {format_size(doc.size)}")
                        print(f"  - MIME 类型: {doc.mime_type}")
                    
                    else:
                        print(f"  - 类型: 未知 ({type(message.media).__name__})")
                # =====================================================================

                print("-" * 20)

        except Exception as e:
            print(f"发生错误: {e}")
            print("请确保您输入的 channel 用户名正确，并且您有权访问该 channel。")

if __name__ == '__main__':
    asyncio.run(main())