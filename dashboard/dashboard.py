import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
# Perbaikan Data
# =====================================
if df["season"].dtype != "object":
    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }
    df["season"] = df["season"].map(season_map)

df["day_type"] = df["workingday"].map({
    0: "Weekend / Holiday",
    1: "Working Day"
})

# Mapping tahun
df["year"] = df["yr"].map({
    0: 2011,
    1: 2012
})

# =====================================
# Sidebar Filter
# =====================================
st.sidebar.header("🔍 Filter Data")

# Filter Tahun
selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    options=["Semua", 2011, 2012]
)

# Filter Musim
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df["season"].unique(),
    default=df["season"].unique()
)

# Filter Jenis Hari
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
# Judul Dashboard
# =====================================
st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard interaktif analisis penggunaan sepeda tahun 2011 - 2012")

# =====================================
# KPI Section
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Peminjaman", f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():.0f}")
col3.metric("Jumlah Data", f"{filtered_df.shape[0]} Hari")

# =====================================
# Preview Data
# =====================================
with st.expander("📄 Lihat Data"):
    st.dataframe(filtered_df)

# =====================================
# Visualisasi 1
# =====================================
col4, col5 = st.columns(2)

with col4:
    st.subheader("Peminjaman Berdasarkan Musim")

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(
        data=filtered_df,
        x="season",
        y="cnt",
        estimator="mean",
        order=["Spring", "Summer", "Fall", "Winter"],
        ax=ax
    )

    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)

# =====================================
# Visualisasi 2
# =====================================
with col5:
    st.subheader("Hari Kerja vs Libur")

    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(
        data=filtered_df,
        x="day_type",
        y="cnt",
        estimator="mean",
        ax=ax2
    )

    ax2.set_xlabel("Jenis Hari")
    ax2.set_ylabel("Rata-rata")
    st.pyplot(fig2)

# =====================================
# Visualisasi 3
# =====================================
st.subheader("Trend Jumlah Peminjaman")

fig3, ax3 = plt.subplots(figsize=(12,5))
filtered_df["cnt"].plot(ax=ax3)

ax3.set_xlabel("Index Hari")
ax3.set_ylabel("Jumlah Peminjaman")

st.pyplot(fig3)

# =====================================
# Insight
# =====================================
st.subheader("📌 Insight")

st.write("""
- Jumlah peminjaman sepeda cenderung lebih tinggi pada musim **Fall** dan **Summer**.  
- Hari kerja menunjukkan penggunaan lebih tinggi dibandingkan akhir pekan/libur.  
- Dashboard ini dapat difilter berdasarkan tahun, musim, dan jenis hari untuk melihat pola penggunaan secara spesifik.
""")