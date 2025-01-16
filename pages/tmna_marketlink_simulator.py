import chardet
import pandas as pd
import streamlit as st

ENCODINGS = ["SHIFT_JIS", "UTF-8", "EUC-JP", "ISO-2022-JP"]


def main():
    # タイトルとサブタイトルの表示
    st.title("マーケットリンク シミュレーション")
    st.subheader("外国株式型の運用シミュレーション")

    # ユーザー入力の受け取り
    monthly_payment = st.number_input("毎月の支払額（円）", min_value=0, value=10000, step=1000)
    start_date = st.date_input("積み立て開始日")

    # CSVファイルのアップロード
    uploaded_file = st.file_uploader("ユニットプライスのCSVファイルをアップロードしてください", type="csv")
    st.write(uploaded_file)

    if uploaded_file is not None:
        # csv_data = StringIO(uploaded_file.getvalue().decode("cp932"))
        result = chardet.detect(uploaded_file.getvalue())
        detect_encoding = result["encoding"]
        encodings_list = [*ENCODINGS, detect_encoding]
        encodings_list = list(set(encodings_list))
        encoding = st.selectbox("エンコーディングを選択", encodings_list, index=encodings_list.index(detect_encoding))
        df_prices = pd.read_csv(uploaded_file, skiprows=1, encoding=encoding)
        st.expander("読み込んだプライスリスト").write(df_prices)
        # 加工していく
        df_prices["年月日"] = pd.to_datetime(df_prices["年月日"]).dt.date

        # 積み立て開始日以降のデータに絞り込む
        df_prices = df_prices[df_prices["年月日"] >= start_date]

        if not df_prices.empty:
            # 手数料率の設定
            contract_fee_rate = 0.002  # 保険料の0.2%
            trust_fee_rate = 0.00176  # 信託報酬 年率0.176%
            risk_fee_rate = 0.00375  # 最低保証費用 年率0.375%

            # シミュレーション計算
            months = len(df_prices)
            total_payment = monthly_payment * months
            contract_fee = total_payment * contract_fee_rate

            monthly_trust_fee = trust_fee_rate / 12
            monthly_risk_fee = risk_fee_rate / 12

            data = []
            accumulated_amount = 0
            units = 0

            for _, row in df_prices.iterrows():
                price = row["外国株式型"]
                if pd.notnull(price):
                    accumulated_amount += monthly_payment * (1 - contract_fee_rate)
                    units += accumulated_amount / price
                    accumulated_amount = units * price
                    accumulated_amount *= 1 - monthly_trust_fee
                    accumulated_amount *= 1 - monthly_risk_fee
                    data.append(accumulated_amount)
                else:
                    data.append(None)

            df_result = pd.DataFrame({"年月日": df_prices["年月日"], "積立金額": data})

            # 結果の表示
            st.subheader("シミュレーション結果")
            st.write(f'積み立て終了時の積立金額: {df_result.iloc[-1]["積立金額"]:,.0f}円')

            st.line_chart(df_result.set_index("年月日"))
        else:
            st.warning("選択された期間のデータがありません。")
    else:
        st.info("ユニットプライスのCSVファイルをアップロードしてください。")
    return


if __name__ == "__main__":
    from streamlit_playground.page_routing import routing

    routing()

if __name__ == "__page__":
    try:
        st.set_page_config(layout="wide")
    except:  # noqa
        pass

    main()
