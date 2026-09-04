import streamlit as st
import httpx

import pandas as pd

import os

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def main():
    st.markdown("# eClipseBoard")

    stats = httpx.get(f"{BASE_URL}/solar/stats", timeout=30).json()

    type_counts = httpx.get(f"{BASE_URL}/solar/type-counts", timeout=30).json()

    counts_df = pd.DataFrame.from_dict(type_counts, orient="index", columns=["Counts"])

    st.dataframe(stats)

    st.markdown("## Number of eclipses per type")

    st.bar_chart(counts_df)

    st.markdown("https://www.kaggle.com/datasets/nasa/solar-eclipses?select=solar.csv ")


if __name__ == "__main__":
    main()
