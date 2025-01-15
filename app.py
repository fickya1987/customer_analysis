import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Define additional stop words
custom_stopwords = set([
    "yang", "dan", "oleh", "untuk", "dalam", "dengan", "pada", "tidak", "ini", "itu", "akan", "adalah", "saya", "kami", "dari", "di", "ke",
    "karena", "sering", "ada", "pastikan", "selalu", "agar", "atau", "seperti", "jika", "juga"
])

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
    st.subheader("Interactive Chart: Keluhan dan Saran Berdasarkan Cabang")
    chart_type = st.radio("Pilih Jenis Chart", ("Bar Chart", "Area Chart"))
    selected_branch = st.selectbox("Pilih Cabang", options=df["Cabang"].unique())

    # Filter data for the selected branch
    branch_data = df[df["Cabang"] == selected_branch]
    if not branch_data.empty:
        complaints_count = branch_data["Keluhan"].count()
        suggestions_count = branch_data["Saran"].count()

        st.write(f"**Jumlah Keluhan**: {complaints_count}")
        st.write(f"**Jumlah Saran**: {suggestions_count}")

        if chart_type == "Bar Chart":
            fig_bar = px.bar(
                x=["Keluhan", "Saran"],
                y=[complaints_count, suggestions_count],
                labels={"x": "Jenis", "y": "Jumlah"},
                title=f"Keluhan dan Saran untuk Cabang: {selected_branch}"
            )
            st.plotly_chart(fig_bar)

        elif chart_type == "Area Chart":
            data_area = pd.DataFrame({
                "Jenis": ["Keluhan", "Saran"],
                "Jumlah": [complaints_count, suggestions_count]
            })
            fig_area = px.area(
                data_area,
                x="Jenis",
                y="Jumlah",
                title=f"Keluhan dan Saran untuk Cabang: {selected_branch}"
            )
            st.plotly_chart(fig_area)

        # Display detailed narratives
        st.write("### Narasi Keluhan")
        for row in branch_data["Keluhan"].dropna().to_list():
            st.write(f"- {row}")

        st.write("### Narasi Saran")
        for row in branch_data["Saran"].dropna().to_list():
            st.write(f"- {row}")

    else:
        st.write("Tidak ada data untuk cabang yang dipilih.")

    # Word Cloud Visualizations
    st.subheader("Word Cloud Keluhan")
    keluhan_text = " ".join(branch_data["Keluhan"].dropna().tolist())
    wordcloud_keluhan = WordCloud(width=800, height=400, background_color='white',
                                  stopwords=custom_stopwords).generate(keluhan_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud_keluhan, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    st.subheader("Word Cloud Saran")
    saran_text = " ".join(branch_data["Saran"].dropna().tolist())
    wordcloud_saran = WordCloud(width=800, height=400, background_color='white',
                                stopwords=custom_stopwords).generate(saran_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud_saran, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

if __name__ == "__main__":
    main()








