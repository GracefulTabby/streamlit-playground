import streamlit as st

from streamlit_playground.page_routing import routing


def main():
    routing()
    return


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
