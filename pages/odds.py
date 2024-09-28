import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def main():
    if not st.toggle("Run!"):
        st.stop()
    # 対象のレースID
    race_id_base = "2024100304"
    race_num = st.selectbox("レース番号", [i for i in range(1, 13)], format_func=lambda x: f"{x}R")
    race_id = f"{race_id_base}{race_num:02}"
    st.write(race_id)

    # オッズページのURL
    b1_url = f"https://race.netkeiba.com/odds/index.html?type=b1&race_id={race_id}"
    b1_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202410030401&rf=shutuba_submenu"
    st.write(b1_url)

    # https://ohenziblog.com/streamlit_cloud_for_selenium/
    # Seleniumの設定
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # 画面描画の待ち時間
        wait = WebDriverWait(driver=driver, timeout=30)
        driver.implicitly_wait(30)

        # ページにアクセス
        driver.get(b1_url)
        # 要素が全て検出できるまで待機する
        wait.until(EC.presence_of_all_elements_located)

        el = driver.find_element(
            By.CLASS_NAME, "Shutuba_Table RaceTable01 ShutubaTable tablesorter tablesorter-default"
        )  # IDでテーブルを指定
        html = el.get_attribute("outerHTML")  # table要素を含むhtmlを取得

        dfs = pd.read_html(html)
        with st.expander("DFS raw", True):
            st.write(dfs)
            st.write(dfs[0])
        st.code(dfs[0].to_markdown(index=False))

    except Exception as e:
        print(e)
    finally:
        # 最後にドライバーを終了する
        # ブラウザを閉じる
        driver.close()
        driver.quit()


if __name__ == "__main__":
    from streamlit_playground.page_routing import routing

    routing()

if __name__ == "__page__":
    try:
        st.set_page_config(layout="wide")
    except:  # noqa
        pass
    main()
