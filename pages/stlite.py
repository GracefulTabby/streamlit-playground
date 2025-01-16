from pathlib import Path

import streamlit as st
from jinja2 import Template
from streamlit.components import v1 as components

html_template = Template(Path("./stlite.html.j2").read_text())
html_str = html_template.render()

st.write("test")

components.html(html_str, height=500)


def run():
    nav = st.navigation(
        [
            st.Page("pages/demo_app.py", title="デモアプリ", default=True),
            st.Page("pages/srcdoc.py", url_path="srcdoc"),
        ],
        position="hidden",
    )
    nav.run()
