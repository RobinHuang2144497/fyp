import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 设置目标 URL（东方财富网股吧广场）
url = "https://guba.eastmoney.com/"

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# 定义一个函数爬取广场页面内容
def scrape_guba_page(page_url):
    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # 找到所有的发言块
    posts = soup.find_all("div", class_="articleh")  # 根据实际页面结构调整 class 名称

    data = []
    for post in posts:
        try:
            # 用户名
            user = post.find("span", class_="l3").get_text(strip=True)
            # 发言内容
            content = post.find("span", class_="l2").get_text(strip=True)
            # 时间
            time_text = post.find("span", class_="l5").get_text(strip=True)

            data.append({"用户": user, "发言内容": content, "时间": time_text})
        except AttributeError:
            continue  # 如果某个字段缺失，跳过

    return data

# 爬取多页
all_data = []
for page in range(1, 3):  # 修改范围以爬取更多页
    print(f"正在爬取第 {page} 页...")
    page_url = f"https://guba.eastmoney.com/list,gz,hot_{page}.html"  # 根据实际情况调整 URL
    page_data = scrape_guba_page(page_url)
    if page_data:
        all_data.extend(page_data)
    time.sleep(2)  # 添加延迟，避免过于频繁的请求

# 保存数据到 Excel
df = pd.DataFrame(all_data)
df.to_excel("东方财富网股吧广场发言.xlsx", index=False)

print("爬取完成，数据已保存到 Excel 文件。")
