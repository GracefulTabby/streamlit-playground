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
            st.Page("pages/tmna_marketlink_simulator.py", title="MarketLinkSimulator"),
        ],
    }
    nav = st.navigation(pages)
    nav.run()
    return
