import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Load data
file_path = "Keluhan_dan_Saran_Pelanggan_stakeholder_pelindo.xlsx"
df = pd.read_excel(file_path)

# Streamlit app
def main():
    st.title("Keluhan dan Saran Pelanggan")

    # Show the dataframe
    st.subheader("Data Keluhan dan Saran")
    st.dataframe(df)

    # Visualization: Bar chart of complaints by branch
    st.subheader("Visualisasi Keluhan Berdasarkan Cabang")
    keluhan_count = df["Cabang"].value_counts().reset_index()
    keluhan_count.columns = ["Cabang", "Jumlah Keluhan"]

    fig_bar = px.bar(keluhan_count, x="Cabang", y="Jumlah Keluhan", color="Jumlah Keluhan",
                     title="Jumlah Keluhan per Cabang",
                     labels={"Cabang": "Cabang", "Jumlah Keluhan": "Jumlah Keluhan"})
    st.plotly_chart(fig_bar)

    # Visualization: Interactive bar chart for suggestions
    st.subheader("Visualisasi Saran Berdasarkan Cabang")
    saran_count = df["Cabang"].value_counts().reset_index()
    saran_count.columns = ["Cabang", "Jumlah Saran"]

    fig_saran = px.bar(saran_count, x="Cabang", y="Jumlah Saran", color="Jumlah Saran",
                       title="Jumlah Saran per Cabang",
                       labels={"Cabang": "Cabang", "Jumlah Saran": "Jumlah Saran"})
    st.plotly_chart(fig_saran)

    # Visualization: Word Cloud for complaints
    st.subheader("Word Cloud Keluhan")
    keluhan_text = " ".join(df["Keluhan"].dropna().tolist())
    wordcloud_keluhan = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(keluhan_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud_keluhan, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # Visualization: Word Cloud for suggestions
    st.subheader("Word Cloud Saran")
    saran_text = " ".join(df["Saran"].dropna().tolist())
    wordcloud_saran = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(saran_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud_saran, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # Visualization: Pie chart of service types
    st.subheader("Distribusi Jenis Pelayanan")
    pelayanan_count = df["Jenis Pelayanan"].value_counts().reset_index()
    pelayanan_count.columns = ["Jenis Pelayanan", "Jumlah"]

    fig_pie = px.pie(pelayanan_count, values="Jumlah", names="Jenis Pelayanan",
                     title="Distribusi Jenis Pelayanan",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie)

    # Filter by branch
    st.subheader("Filter Keluhan dan Saran Berdasarkan Cabang")
    selected_cabang = st.selectbox("Pilih Cabang", options=df["Cabang"].unique())
    filtered_data = df[df["Cabang"] == selected_cabang]

    st.write(f"Menampilkan data untuk cabang: {selected_cabang}")
    st.dataframe(filtered_data)

if __name__ == "__main__":
    main()





