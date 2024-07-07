import pandas as pd
import streamlit as st
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

st.set_page_config(layout="wide")


def main():

    # 対象のレースID
    race_id_base = "2024100304"
    race_num = st.selectbox("レース番号",[i for i in range(1,13)],format_func=lambda x: f"{x}R")
    race_id = f"{race_id_base}{race_num:02}"
    st.write(race_id)

    # オッズページのURL
    b1_url = f"https://race.netkeiba.com/odds/index.html?type=b1&race_id={race_id}"
    st.write(b1_url)

    # https://ohenziblog.com/streamlit_cloud_for_selenium/
    # Seleniumの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                options=options)    
    # 画面描画の待ち時間
    wait=WebDriverWait(driver,20)
    driver.implicitly_wait(30)

    # ページにアクセス
    driver.get(b1_url)
    time.sleep(3)
    
    el= driver.find_element(By.CLASS_NAME, 'RaceOdds_HorseList_Table') #IDでテーブルを指定
    html=el.get_attribute("outerHTML") #table要素を含むhtmlを取得
    
    dfs = pd.read_html(html)    
    st.write(dfs)

    # HTMLを取得してBeautiful Soupでパース
    # html = driver.page_source
    # soup = BeautifulSoup(html, "html.parser")

    # # オッズテーブルを取得
    # odds_table = soup.find("table", class_="RaceOdds_HorseList_Table")

    # # 馬番とオッズを取得
    # for row in odds_table.find_all("tr", class_="Txt_R")[1:]:
    #     cells = row.find_all("td")
    #     umaban = cells[1].text
    #     odds = cells[2].text
    #     st.write(f"馬番: {umaban}, オッズ: {odds}")

    # ブラウザを閉じる  
    driver.close()    
    
    
 
if __name__ == "__main__":
    main()