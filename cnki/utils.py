import json
import os

# 定义保存进度的文件名
PROGRESS_FILE = "search_progress.json"


# 加载进度
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)
    return {}


# 保存进度
def save_progress(progress):
    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress, file, indent=4)


# 更新进度
def update_progress(keyword, page):
    progress = load_progress()
    progress[keyword] = page
    save_progress(progress)


# 模拟搜索和进度保存
def search(keyword, max_pages=5):
    current_page = load_progress().get(keyword, 1)

    for page in range(current_page, max_pages + 1):
        print(f"正在搜索关键词 '{keyword}' 的第 {page} 页...")

        # 在这里可以放你的爬虫逻辑，获取搜索结果
        # 假设搜索成功后，更新进度
        update_progress(keyword, page + 1)


async def jump_to_start_page(page, start_page) -> None:
    # 跳转到 start_page
    cur_page = 1
    while start_page - cur_page > 5:
        cur_page += 5
        await page.get_by_role("link", name=f"{cur_page}", exact=True).click()
        print(f"jump to page {cur_page}")
    if cur_page != start_page:
        await page.get_by_role("link", name=f"{start_page}", exact=True).click()
