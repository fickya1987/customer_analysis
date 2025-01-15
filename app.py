import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Define additional stop words
custom_stopwords = set(["yang", "dan", "oleh", "untuk", "dalam", "dengan", "pada", "tidak", "ini", "itu", "akan", "adalah", "saya", "kami", "dari", "di", "ke"])

# Load data
file_path = "Keluhan_dan_Saran_Pelanggan_stakeholder_pelindo.xlsx"
df = pd.read_excel(file_path)

# Streamlit app
def main():
    st.title("Keluhan dan Saran Pelanggan")

    # Show the dataframe
    st.subheader("Data Keluhan dan Saran")
    st.dataframe(df)

    # Visualization: Area chart for complaints and suggestions by branch
    st.subheader("Area Chart: Keluhan dan Saran Berdasarkan Cabang")
    area_data = df.groupby("Cabang").size().reset_index(name="Jumlah")
    fig_area = px.area(area_data, x="Cabang", y="Jumlah", title="Keluhan dan Saran Berdasarkan Cabang",
                       labels={"Cabang": "Cabang", "Jumlah": "Jumlah"})
    st.plotly_chart(fig_area)

    # Visualization: Spider chart (Radar chart) for Keluhan and Saran comparison
    st.subheader("Radar Chart: Perbandingan Keluhan dan Saran")
    branches = df["Cabang"].unique()
    radar_data = []
    for branch in branches:
        complaints = df[df["Cabang"] == branch]["Keluhan"].count()
        suggestions = df[df["Cabang"] == branch]["Saran"].count()
        radar_data.append({"Cabang": branch, "Keluhan": complaints, "Saran": suggestions})
    radar_df = pd.DataFrame(radar_data)

    categories = list(radar_df["Cabang"])
    complaints = radar_df["Keluhan"].tolist()
    suggestions = radar_df["Saran"].tolist()

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=complaints, theta=categories, fill='toself', name='Keluhan'))
    fig_radar.add_trace(go.Scatterpolar(r=suggestions, theta=categories, fill='toself', name='Saran'))

    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)),
                            title="Radar Chart: Keluhan dan Saran",
                            showlegend=True)
    st.plotly_chart(fig_radar)

    # Visualization: Word Cloud for complaints
    st.subheader("Word Cloud Keluhan")
    keluhan_text = " ".join(df["Keluhan"].dropna().tolist())
    wordcloud_keluhan = WordCloud(width=800, height=400, background_color='white',
                                  stopwords=custom_stopwords).generate(keluhan_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud_keluhan, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # Visualization: Word Cloud for suggestions
    st.subheader("Word Cloud Saran")
    saran_text = " ".join(df["Saran"].dropna().tolist())
    wordcloud_saran = WordCloud(width=800, height=400, background_color='white',
                                stopwords=custom_stopwords).generate(saran_text)

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






