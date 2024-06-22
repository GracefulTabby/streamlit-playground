import pandas as pd
import numpy as np
import streamlit as st
import folium
from folium.plugins import FastMarkerCluster
import pandas as pd
from streamlit.components.v1 import html as st_html
from collections import OrderedDict
from pyinstrument import Profiler
import branca.colormap as cm
import json
from jinja2 import Template
from folium.map import Layer
from folium.elements import JSCSSMixin
from folium.utilities import (
    if_pandas_df_convert_to_numpy,
    validate_location,
    parse_options,
)

import json

st.set_page_config(layout="wide")


class FastCircleMarker(JSCSSMixin, Layer):
    """
    Add CircleMarkers to a map using in-browser rendering.
    Using FastCircleMarker it is possible to render thousands of
    points far quicker than the usual Folium methods.

    Parameters
    ----------
    data: list of list with values
        List of list of shape [[lat, lon, value], [lat, lon, value], etc.]
    callback: string, optional
        A string representation of a valid Javascript function
        that will be passed each row in data.
    name : string, optional
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    **kwargs
        Additional arguments are passed to Leaflet options.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = (function(){
                {{ this.callback }}

                var data = {{ this.data|tojson }};
                var layer = L.featureGroup()
                
                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var marker = callback(row);
                    marker.addTo(layer);
                }

                layer.addTo({{ this._parent.get_name() }});
                return layer;
            })();
        {% endmacro %}
        """
    )

    def __init__(
        self,
        data,
        callback=None,
        name=None,
        overlay=True,
        control=True,
        show=True,
        **kwargs,
    ):
        super().__init__(
            name=name,
            overlay=overlay,
            control=control,
            show=show,
            **kwargs,
        )
        self._name = "FastCircleMarker"
        data = if_pandas_df_convert_to_numpy(data)
        self.data = [[*validate_location(row[:2]), *row[2:]] for row in data]

        if callback is None:
            self.callback = """
                var callback = function (row) {
                    var marker = L.circleMarker(new L.LatLng(row[0], row[1]), {
                        radius: 8,
                        fillColor: 'blue',
                        color: "#000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                    return marker;
                };"""
        else:
            self.callback = f"var callback = {callback};"


def generate_random_japan_data(num_samples):
    # 日本国内の緯度と経度の範囲
    lat_min, lat_max = 24.396308, 45.551483
    lon_min, lon_max = 122.93457, 153.986672

    # ランダムな緯度と経度の生成
    latitudes = np.random.uniform(lat_min, lat_max, num_samples)
    longitudes = np.random.uniform(lon_min, lon_max, num_samples)

    # 3種類のランダムな数値の生成
    random_value1 = np.random.rand(num_samples)
    random_value2 = np.random.randint(0, 100, num_samples)
    random_value3 = np.random.normal(50, 15, num_samples)

    # データフレームの作成
    data = {
        "Latitude": latitudes,
        "Longitude": longitudes,
        "RandomValue1": random_value1,
        "RandomValue2": random_value2,
        "RandomValue3": random_value3,
    }
    df = pd.DataFrame(data)

    return df


def main():
    # サンプルデータ（緯度, 経度, 値）
    df = pd.DataFrame(
        [
            [35.6895, 139.6917, 10],  # 東京
            [34.6937, 135.5023, 20],  # 大阪
            [43.0621, 141.3544, 30],  # 札幌
        ],
        columns=["lat", "lng", "value"],
    )
    # カラーマップの作成
    colormap = cm.LinearColormap(
        colors=["blue", "green", "yellow", "red"], vmin=0, vmax=30
    )
    # 色の情報を追加
    df["color"] = df["value"].apply(colormap)
    # 地図に渡すデータを生成する
    # lat,lng,value,color
    data = df[["lat", "lng", "value", "color"]].values.tolist()
    # JavaScriptコールバック関数
    callback = f"""
    function (row) {{
        var point = new L.LatLng(row[0], row[1]);
        var color = row[3];
        var marker = L.circleMarker(point, {{
            radius: 8,
            fillColor: color,
            color: color,
            weight: 1,
            // opacity: 0.5,
            fillOpacity: 0.4,
        }});
        return marker;
    }};
    """

    # 地図の中心とズームレベルを設定
    m = folium.Map(location=[35.6895, 139.6917], zoom_start=5)

    # FastCircleMarkerを追加
    fast_marker = FastCircleMarker(data, callback=callback)
    fast_marker.add_to(m)

    # カラーマップを地図に追加
    colormap.add_to(m)

    # レイヤーコントロールを追加
    folium.LayerControl().add_to(m)

    # 地図を保存または表示
    m_html = m.get_root().render()
    st_html(m_html, height=600)


if __name__ == "__main__":
    main()
