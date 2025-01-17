import branca.colormap as cm
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import streamlit as st
from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.utilities import (
    if_pandas_df_convert_to_numpy,
    parse_options,
    validate_location,
)
from jinja2 import Template
from pyinstrument import Profiler
from shapely.geometry import Point
from streamlit.components.v1 import html as st_html


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
                var layer = L.featureGroup({{ this.options|tojson }});

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
        self.options = parse_options(**kwargs)


@st.cache_resource
def generate_random_japan_data(num_samples: int = 1000) -> pd.DataFrame:
    # 日本の地理データをダウンロード
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    japan = world[world.name == "Japan"]

    # 日本の境界を取得
    japan_boundary = japan.geometry.iloc[0]

    # 日本の境界ボックスを取得
    minx, miny, maxx, maxy = japan_boundary.bounds

    # データポイントを生成
    points = []
    while len(points) < num_samples:
        # ランダムなポイントを生成
        point = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))

        # ポイントが日本の陸地内にあるかチェック
        if japan_boundary.contains(point):
            points.append(point)

    # ジオデータフレームの作成
    gdf = gpd.GeoDataFrame(geometry=points)

    # 緯度経度を抽出
    gdf["lat"] = gdf.geometry.y
    gdf["lng"] = gdf.geometry.x

    # 3種類のランダムな数値の生成
    gdf["RandomValue1"] = np.random.rand(num_samples)
    gdf["RandomValue2"] = np.random.randint(0, 100, num_samples)
    gdf["RandomValue3"] = np.random.normal(50, 15, num_samples)

    # 通常のDataFrameに変換
    df = pd.DataFrame(gdf.drop(columns="geometry"))

    return df


def main():
    # サンプルデータ（緯度, 経度, 値）
    df = generate_random_japan_data(10000)
    # カラーマップの作成
    colormap = cm.LinearColormap(colors=["blue", "green", "yellow", "red"], vmin=0, vmax=100)
    # 色の末尾2桁を落とす(alpha)
    colormap_func = lambda x: colormap(x)[:-2]
    # 色の情報を追加
    df["color2"] = df["RandomValue2"].apply(colormap_func)
    # sliderで値による絞り込みができるように
    min_value = df["RandomValue2"].min()
    max_value = df["RandomValue2"].max()
    selected_range = st.slider(
        "RandomValue2 RangeSelect",
        min_value=min_value,
        max_value=max_value,
        value=(min_value, max_value),
    )
    # 地図に渡すデータを生成する
    # lat,lng,value,color
    filtered_df = df[(df["RandomValue2"] >= selected_range[0]) & (df["RandomValue2"] <= selected_range[1])]
    data = filtered_df[["lat", "lng", "RandomValue2", "color2"]].values.tolist()
    # JavaScriptコールバック関数
    # https://leafletjs.com/reference.html#circlemarker
    callback = """
    function (row) {
        var point = new L.LatLng(row[0], row[1]);
        var color = row[3];
        var marker = L.circleMarker(point, {
            radius: 6,
            fillColor: color,
            color: color,
            weight: 1,
            // opacity: 0.5,
            fillOpacity: 0.4,
        });
        var tooltip = L.tooltip({maxWidth: '300'});
        tooltip.setContent('value : ' + row[2]);
        marker.bindTooltip(tooltip);
        return marker;
    };
    """

    # 地図の中心とズームレベルを設定
    m = folium.Map(location=[35.6895, 139.6917], zoom_start=5)

    # FastCircleMarkerを追加
    fast_marker = FastCircleMarker(data, name="randomCircleMarker", callback=callback)
    fast_marker.add_to(m)

    # カラーマップを地図に追加
    colormap.add_to(m)

    # レイヤーコントロールを追加
    folium.LayerControl(collapsed=False).add_to(m)

    # 地図を保存または表示
    m_html = m.get_root().render()
    st_html(m_html, height=600)


if __name__ == "__main__":
    from streamlit_playground.page_routing import routing

    routing()

if __name__ == "__page__":
    try:
        st.set_page_config(layout="wide")
    except:  # noqa
        pass

    profiler = Profiler()
    with profiler:
        main()

    # output Streamlit
    html_str = profiler.output_html()
    st_html(html=html_str, height=500)
