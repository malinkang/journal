def generate_reading_plan(book_name, total_pages, pages_per_day):
    """
    生成阅读计划，将书籍按每天阅读页数拆分成多个任务
    
    参数:
    book_name (str): 书名
    total_pages (int): 书籍总页数
    pages_per_day (int): 每天阅读页数
    
    返回:
    list: 包含每个阅读任务的字符串列表
    """
    reading_plan = []
    current_start_page = 1
    
    while current_start_page <= total_pages:
        end_page = min(current_start_page + pages_per_day - 1, total_pages)
        
        # 创建任务字符串
        task = f"读《{book_name}》 P{current_start_page}-P{end_page}"
        reading_plan.append(task)
        
        # 更新下一个任务的起始页
        current_start_page = end_page + 1
    
    return reading_plan

# 示例使用
def main():
    # 获取用户输入
    book_name = input("请输入书名: ")
    total_pages = int(input("请输入书籍总页数: "))
    pages_per_day = int(input("请输入每天阅读的页数: "))
    
    # 生成阅读计划
    reading_tasks = generate_reading_plan(book_name, total_pages, pages_per_day)
    
    # 打印阅读计划
    for task in reading_tasks:
        print(task)

if __name__ == "__main__":
    main()