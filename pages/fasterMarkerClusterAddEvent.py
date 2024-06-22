import streamlit as st
import folium
from folium.plugins import FastMarkerCluster
import pandas as pd
from streamlit.components.v1 import html as st_html
from collections import OrderedDict
from pyinstrument import Profiler


@st.cache_resource
def get_df() -> pd.DataFrame:
    # https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv
    df = pd.read_csv(
        "https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv",
        encoding="cp932",
    ).fillna("")
    df = df.query('データ区分 != "国・都道府県機関"')
    return df


def main():
    df = get_df()
    # マップを作成
    lon, lat = df["緯度"].mean(), df["経度"].mean()
    m = folium.Map((lon, lat))
    # fasterMarkerClusterにイベントを追加するコールバック関数を定義
    callback = """
    function (row) {
        var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});
        var icon = L.AwesomeMarkers.icon({
        icon: 'info-sign',
        iconColor: 'white',
        markerColor: 'green',
        prefix: 'glyphicon',
        extraClasses: 'fa-rotate-0'
        });
        marker.setIcon(icon);
        var tooltipContent = '<div style="max-width: 300px;">';
        var properties = row[2];
        tooltipContent += '<table>';
        var keys = ['施設名', '市町村名', '住所_出典元', '検索用住所', 'ビル等', 'データ区分', '出典', '原典資料名'];
        keys.forEach(function(key) {
        tooltipContent += '<tr>' +
        '<td style="font-weight: bold; text-align: left; padding-right: 5px;">' + key + ':</td>' +
        '<td style="text-align: left;">' + properties[key] + '</td>' +
        '</tr>';
        });
        tooltipContent += '</table>';
        tooltipContent += '</div>';
        marker.bindTooltip(tooltipContent, { direction: "top", offset: L.point(0, -10) });
        
        var lat = row[0];
        var lng = row[1];
        var delta = 0.005;  // 矩形の大きさを調整するための値（度単位）
        
        var bounds = [
            [lat - delta, lng - delta],
            [lat - delta, lng + delta],
            [lat + delta, lng + delta],
            [lat + delta, lng - delta]
        ];

        var polygon = L.polygon(bounds);
        // 内側からleafletマップオブジェクトにアクセス
        marker.on('mouseover', function(e) {
            polygon.addTo(e.target._map);
        });
        marker.on('mouseout', function(e) {
            e.target._map.removeLayer(polygon);
        });
        return marker
        };
    """
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
    fast_marker_cluster = FastMarkerCluster(
        data,
        callback=callback,
        options={"maxClusterRadius": 120, "disableClusteringAtZoom": 16},
    )
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
