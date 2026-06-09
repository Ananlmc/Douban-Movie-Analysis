# 获取豆瓣top250的电影信息
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import trange


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
}
moves = []
for start_num in trange(0, 250, 25, desc="🔄 总进度"):
    content = requests.get(f"https://movie.douban.com/top250?start={start_num}", headers=headers).text
    time.sleep(5)
    soup = BeautifulSoup(content, "html.parser")
    time.sleep(2)
    for item in soup.find_all("div", class_="item"):
        title = item.find("span", class_ = "title")
        rating = item.find("span",class_ = "rating_num")
        bd = item.find("div", class_="bd")
        p = bd.find('p')
        genre = p.get_text(strip=True).split('/')[-1].replace("\xa0", "").replace(" ", ",")
        moves.append([title.text,rating.text,genre])
columns = ["电影名","评分","类型"]
df = pd.DataFrame(moves,columns=columns)
print("准备写入电影信息")
df.to_csv("douban_top250.csv",index= False)
print("已完成")
