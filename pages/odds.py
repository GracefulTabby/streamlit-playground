import pandas as pd
import streamlit as st
import requests
import chardet
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

st.set_page_config(layout="wide")


def detect_encoding(url):
    response = requests.get(url)
    result = chardet.detect(response.content)
    return result['encoding']


def main():
    race_id = "202410030401"
    base_url = "https://race.netkeiba.com/odds/index.html?type=b0&race_id=202410030401&rf=shutuba_submenu"
    base_url = f"https://nar.netkeiba.com/odds/index.html?type=b1&race_id={race_id}"


    encoding = detect_encoding(base_url)
    st.write(encoding)
    dfs = pd.read_html(base_url,encoding=encoding)
    st.write(dfs)
    

def main2():
    # https://ohenziblog.com/streamlit_cloud_for_selenium/
    # Seleniumの設定
    
    # Using on Local
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                options=options)    
    # 画面描画の待ち時間
    wait=WebDriverWait(driver,20)
    driver.implicitly_wait(30)
    
    # 対象のレースID
    race_id = "202410030401"

    # オッズページのURL
    url = f"https://race.netkeiba.com/odds/index.html?type=b0&race_id={race_id}"

    # ページにアクセス
    driver.get(url)
    
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
    main2()