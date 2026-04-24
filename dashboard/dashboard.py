import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# =====================================
# Konfigurasi Halaman
# =====================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# =====================================
# Load Data
# =====================================
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "main_data.csv")

df = pd.read_csv(file_path)

# =====================================
# Data Cleaning / Mapping (AMAN UNTUK CLOUD)
# =====================================

season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

df["season"] = df["season"].replace(season_map)

df["day_type"] = df["workingday"].map({
    0: "Weekend / Holiday",
    1: "Working Day"
})

df["year"] = df["yr"].map({
    0: 2011,
    1: 2012
})

# =====================================
# Sidebar Filter
# =====================================
st.sidebar.header("🔍 Filter Data")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    options=["Semua", 2011, 2012]
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df["season"].unique(),
    default=df["season"].unique()
)

selected_day = st.sidebar.multiselect(
    "Pilih Jenis Hari",
    options=df["day_type"].unique(),
    default=df["day_type"].unique()
)

# =====================================
# Filtering Data
# =====================================
filtered_df = df.copy()

if selected_year != "Semua":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

filtered_df = filtered_df[
    filtered_df["season"].isin(selected_season)
]

filtered_df = filtered_df[
    filtered_df["day_type"].isin(selected_day)
]

# =====================================
# Title
# =====================================
st.title("🚲 Bike Sharing Dashboard")
st.write("Analisis penggunaan sepeda 2011 - 2012")

# =====================================
# KPI
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Peminjaman", f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():.0f}")
col3.metric("Jumlah Hari", f"{filtered_df.shape[0]}")

st.write("Data setelah filter:", filtered_df.shape)

# =====================================
# Data Preview
# =====================================
with st.expander("📄 Lihat Data"):
    st.dataframe(filtered_df)

# =====================================
# VISUALISASI 1 - MUSIM
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Peminjaman Berdasarkan Musim")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.barplot(
        data=filtered_df,
        x="season",
        y="cnt",
        estimator=np.mean,
        order=["Spring", "Summer", "Fall", "Winter"],
        ax=ax
    )

    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Peminjaman")

    st.pyplot(fig)

# =====================================
# VISUALISASI 2 - WORKING DAY
# =====================================
with col2:
    st.subheader("Hari Kerja vs Libur")

    fig2, ax2 = plt.subplots(figsize=(8,5))

    sns.barplot(
        data=filtered_df,
        x="day_type",
        y="cnt",
        estimator=np.mean,
        ax=ax2
    )

    ax2.set_xlabel("Jenis Hari")
    ax2.set_ylabel("Rata-rata Peminjaman")

    st.pyplot(fig2)

# =====================================
# VISUALISASI 3 - TREND
# =====================================
st.subheader("Trend Peminjaman Sepeda")

fig3, ax3 = plt.subplots(figsize=(12,5))

ax3.plot(filtered_df.index, filtered_df["cnt"])

ax3.set_xlabel("Index Hari")
ax3.set_ylabel("Jumlah Peminjaman")

st.pyplot(fig3)

# =====================================
# INSIGHT
# =====================================
st.subheader("📌 Insight")

st.write("""
- Terdapat perbedaan rata-rata peminjaman sepeda berdasarkan musim.  
- Terdapat perbedaan rata-rata peminjaman antara hari kerja dan hari libur.  
- Pola penggunaan sepeda menunjukkan variasi berdasarkan kondisi data yang difilter.  
- Dashboard ini mendukung analisis interaktif berdasarkan tahun, musim, dan jenis hari.
""")