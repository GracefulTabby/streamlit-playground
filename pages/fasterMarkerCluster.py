import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx, add_script_run_ctx
from streamlit.runtime.state.session_state import SessionState
import folium
from folium.plugins import MarkerCluster, FastMarkerCluster, FeatureGroupSubGroup
import pandas as pd
from streamlit.components.v1 import html as st_html
from geojson import Feature, Point, FeatureCollection
from collections import OrderedDict
import pandas as pd
import numpy as np
import streamlit as st
import time
import string
import random
import time
from pyinstrument import Profiler

st.set_page_config(layout="wide")


def randstr(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


@st.cache_resource
def get_df() -> pd.DataFrame:
    # https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv
    df = pd.read_csv(
        "https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv",
        encoding="cp932",
    ).fillna("")
    df = df.query('データ区分 != "国・都道府県機関"')

    # データフレームの行を10倍に増やす
    df_expanded = pd.concat([df] * 5, ignore_index=True)
    df_expanded["a"] = [randstr(20) for _ in range(len(df_expanded))]
    df_expanded["b"] = [randstr(18) for _ in range(len(df_expanded))]
    df_expanded["c"] = [randstr(17) for _ in range(len(df_expanded))]
    return df_expanded


def main():
    df = get_df()

    st.write(df)

    # geojsonを作成する
    # features = []
    # for _, row in df.head(100).iterrows():
    #     point = Point((row["経度"], row["緯度"]))
    #     properties = {
    #         "施設名": row["施設名"],
    #         "市町村名": row["市町村名"],
    #         "住所_出典元": row["住所_出典元"],
    #         "検索用住所": row["検索用住所"],
    #         "ビル等": row["ビル等"] if not pd.isna(row["ビル等"]) else "",
    #         "データ区分": row["データ区分"],
    #         "出典": row["出典"],
    #         "原典資料名": row["原典資料名"],
    #     }
    #     features.append(Feature(geometry=point, properties=properties))
    # # GeoJSONのFeatureCollectionを作成する
    # feature_collection = FeatureCollection(features)

    lon, lat = df["緯度"].mean(), df["経度"].mean()
    m = folium.Map((lon, lat))
    # marker_cluster = MarkerCluster(name="Developments")
    # gj = folium.GeoJson(
    #     feature_collection,
    #     embed=False,
    #     tooltip=folium.GeoJsonTooltip(
    #         fields=[
    #             "施設名",
    #             "市町村名",
    #             "住所_出典元",
    #             "検索用住所",
    #             "ビル等",
    #             "データ区分",
    #             "出典",
    #             "原典資料名",
    #         ]
    #     ),
    # )
    # m.add_child(gj)
    # m.add_child(marker_cluster)

    # fasterMarkerCluster
    callback = (
        "function (row) {"
        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
        "var icon = L.AwesomeMarkers.icon({"
        "icon: 'info-sign',"
        "iconColor: 'white',"
        "markerColor: 'green',"
        "prefix: 'glyphicon',"
        "extraClasses: 'fa-rotate-0'"
        "});"
        "marker.setIcon(icon);"
        "var popup = L.popup({maxWidth: '300'});"
        "const display_text = {text: row[2]};"
        "var mytext = L.DomUtil.create('div', 'display_text');"
        "mytext.textContent = display_text.text;"
        "popup.setContent(mytext);"
        "marker.bindPopup(popup);"
        "return marker};"
    )
    # コールバック関数を定義
    callback = (
        "function (row) {"
        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
        "var icon = L.AwesomeMarkers.icon({"
        "icon: 'info-sign',"
        "iconColor: 'white',"
        "markerColor: 'green',"
        "prefix: 'glyphicon',"
        "extraClasses: 'fa-rotate-0'"
        "});"
        "marker.setIcon(icon);"
        "var tooltipContent = '';"
        "var properties = row[2];"
        "var keys = ['施設名', '市町村名', '住所_出典元', '検索用住所', 'ビル等', 'データ区分', '出典', '原典資料名'];"
        "keys.forEach(function(key) {"
        "tooltipContent += key + ': ' + properties[key] + '<br>';"
        "});"
        "marker.bindTooltip(tooltipContent);"
        "return marker};"
    )
    callback = (
        "function (row) {"
        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
        "var icon = L.AwesomeMarkers.icon({"
        "icon: 'info-sign',"
        "iconColor: 'white',"
        "markerColor: 'green',"
        "prefix: 'glyphicon',"
        "extraClasses: 'fa-rotate-0'"
        "});"
        "marker.setIcon(icon);"
        "var tooltipContent = '';"
        "var properties = row[2];"
        "var keys = ['施設名', '市町村名', '住所_出典元', '検索用住所', 'ビル等', 'データ区分', '出典', '原典資料名'];"
        "keys.forEach(function(key) {"
        "tooltipContent += '<div style=\"font-weight: bold; text-align: left;\">' + key + ':</div>';"
        "tooltipContent += '<div style=\"text-align: right;\">' + properties[key] + '</div><br>';"
        "});"
        "marker.bindTooltip(tooltipContent);"
        "return marker};"
    )
    # コールバック関数を定義
    callback = (
        "function (row) {"
        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
        "var icon = L.AwesomeMarkers.icon({"
        "icon: 'info-sign',"
        "iconColor: 'white',"
        "markerColor: 'green',"
        "prefix: 'glyphicon',"
        "extraClasses: 'fa-rotate-0'"
        "});"
        "marker.setIcon(icon);"
        "var tooltipContent = '<div style=\"max-width: 300px;\">';"
        "var properties = row[2];"
        "tooltipContent += '<table>';"
        "var keys = ['施設名', '市町村名', '住所_出典元', '検索用住所', 'ビル等', 'データ区分', '出典', '原典資料名'];"
        "keys.forEach(function(key) {"
        "tooltipContent += '<tr>' +"
        "'<td style=\"font-weight: bold; text-align: left; padding-right: 5px;\">' + key + ':</td>' +"
        "'<td style=\"text-align: left;\">' + properties[key] + '</td>' +"
        "'</tr>';"
        "});"
        "tooltipContent += '</table>';"
        "tooltipContent += '</div>';"
        'marker.bindTooltip(tooltipContent, { direction: "top", offset: L.point(0, -10) });'
        "return marker};"
    )
    # 必要な列を抽出し、辞書形式のリストを作成
    data = df.apply(
        lambda row: [
            row["緯度"],
            row["経度"],
            OrderedDict(
                [
                    ("施設名", row["施設名"]),
                    ("市町村名", row["市町村名"]),
                    ("住所_出典元", row["住所_出典元"]),
                    ("検索用住所", row["検索用住所"]),
                    ("ビル等", row["ビル等"]),
                    ("データ区分", row["データ区分"]),
                    ("出典", row["出典"]),
                    ("原典資料名", row["原典資料名"]),
                ]
            ),
        ],
        axis=1,
    ).tolist()
    # FastMarkerClusterを作成
    fast_marker_cluster = FastMarkerCluster(data, callback=callback)
    m.add_child(fast_marker_cluster)
    html = m.get_root().render()
    st_html(html, height=600)


if __name__ == "__main__":
    profiler = Profiler()
    with profiler:
        main()

    # output Streamlit
    html_str = profiler.output_html()
    st_html(html=html_str, height=500)
