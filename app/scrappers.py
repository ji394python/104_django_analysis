from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from datetime import datetime



# KLOOK客路網站
class Klook():
    
    def __init__(self,city_name):
        self.city_name = city_name
        
    def scrape(self):

        result = []  # 回傳結果

        if self.city_name:  # 如果城市名稱非空值

            # 取得傳入城市的所有一日遊&導賞團票券
            response = requests.get(
                f"https://www.ptt.cc/bbs/Stock/index.html")
            soup = BeautifulSoup(response.text, "lxml")

            # 取得十個票券卡片(Card)元素
            activities = soup.select('.r-ent')

            for activity in activities:

                # 票券名稱
                try:
                    title = activity.select('.title > a')[0].text
                except:
                    title= "測試"

                # 票券詳細內容連結
                try:
                    link = "https://www.ptt.cc/" + \
                        activity.select('.title > a')[0]['href']
                except:
                    link= "測試"

                # 票券價格
                try:
                    price = activity.select('.nrec')[0].text
                except:
                    price= "測試"

                # 最早可使用日期
                try:
                    booking_date = activity.select('.meta > .date')[0].text
                except:
                    booking_date= "測試"

                # 評價
                try:
                    star = activity.select('.meta > .author')[0].text
                except:
                    star= "測試"

                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="https://cdn.klook.com/s/dist_web/assert/desktop/imgs/favicon-098cf2db20.png"))

        return result