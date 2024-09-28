import streamlit as st


def routing():
    pages = {
        "🛝 Play Ground": [
            st.Page("pages/fasterCircleMarker.py", title="fasterCircleMarker"),
            st.Page("pages/fasterMarkerCluster.py", title="fasterMarkerCluster"),
            st.Page("pages/fasterMarkerClusterAddEvent.py", title="fasterMarkerClusterAddEvent"),
            st.Page("pages/multiThread.py", title="multiThread"),
            st.Page("pages/odds.py", title="odds"),
        ],
        "🧰 MyTools": [
            st.Page("pages/fasterCircleMarker.py", title="fasterCircleMarker", url_path="faster-circle-marker-2"),
        ],
    }
    nav = st.navigation(pages)
    nav.run()
    return
