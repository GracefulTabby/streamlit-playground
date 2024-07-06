import pandas as pd
import streamlit as st
import requests
import chardet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

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

    # Seleniumの設定
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    # 対象のレースID
    race_id = "202410030401"

    # オッズページのURL
    url = f"https://race.netkeiba.com/odds/index.html?type=b0&race_id={race_id}"

    # ページにアクセス
    driver.get(url)
    # sleep(1)  # ページ読み込み待ち
    
    elem_table = driver.find_element_by_css_selector("table.full-name-type")
    html = elem_table.get_attribute('outerHTML')
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
    driver.quit()    
    
    
 
if __name__ == "__main__":
    main2()