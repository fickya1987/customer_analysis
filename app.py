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
file_path = "Keluhan_dan_Saran_Pelanggan.xlsx"
df = pd.read_excel(file_path)

# Streamlit app
def main():
    st.title("Keluhan dan Saran Pelanggan")

    # Show the dataframe
    st.subheader("Data Keluhan dan Saran")
    st.dataframe(df)

    # Visualization: Multiple chart types for complaints and suggestions by branch
    st.subheader("Interactive Chart: Keluhan dan Saran Berdasarkan Cabang")
    chart_type = st.selectbox("Pilih Jenis Chart", (
        "Bar Chart", "Area Chart", "Pie Chart", "Scatter Plot", "Line Chart", "Bubble Chart", "Treemap", "Sunburst", "Funnel Chart", "Radar Chart"
    ))
    selected_branch = st.selectbox("Pilih Cabang", options=df["Cabang"].unique())

    # Filter data for the selected branch
    branch_data = df[df["Cabang"] == selected_branch]
    if not branch_data.empty:
        complaints_count = branch_data["Keluhan"].count()
        suggestions_count = branch_data["Saran"].count()

        st.write(f"**Jumlah Keluhan**: {complaints_count}")
        st.write(f"**Jumlah Saran**: {suggestions_count}")

        data_chart = pd.DataFrame({
            "Jenis": ["Keluhan", "Saran"],
            "Jumlah": [complaints_count, suggestions_count],
            "Narasi": [
                "\n".join(branch_data["Keluhan"].dropna().to_list()),
                "\n".join(branch_data["Saran"].dropna().to_list())
            ]
        })

        if chart_type == "Bar Chart":
            fig = px.bar(
                data_chart, x="Jenis", y="Jumlah", color="Jenis",
                hover_data={"Narasi": True},
                title=f"Keluhan dan Saran untuk Cabang: {selected_branch}",
                labels={"Jenis": "Jenis", "Jumlah": "Jumlah"},
                color_discrete_sequence=px.colors.sequential.Viridis
            )

        elif chart_type == "Area Chart":
            fig = px.area(
                data_chart, x="Jenis", y="Jumlah",
                hover_data={"Narasi": True},
                title=f"Keluhan dan Saran untuk Cabang: {selected_branch}",
                color_discrete_sequence=px.colors.sequential.Plasma
            )

        elif chart_type == "Pie Chart":
            fig = px.pie(
                data_chart, values="Jumlah", names="Jenis",
                hover_data={"Narasi": True},
                title=f"Distribusi Keluhan dan Saran untuk Cabang: {selected_branch}",
                color_discrete_sequence=px.colors.sequential.RdBu
            )

        elif chart_type == "Scatter Plot":
            fig = px.scatter(
                data_chart, x="Jenis", y="Jumlah", size="Jumlah", color="Jenis",
                hover_data={"Narasi": True},
                title=f"Keluhan dan Saran untuk Cabang: {selected_branch}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

        elif chart_type == "Line Chart":
            fig = px.line(
                data_chart, x="Jenis", y="Jumlah", markers=True,
                hover_data={"Narasi": True},
                title=f"Keluhan dan Saran untuk Cabang: {selected_branch}",
                color_discrete_sequence=["#636EFA"]
            )

        elif chart_type == "Bubble Chart":
            fig = px.scatter(
                data_chart, x="Jenis", y="Jumlah", size="Jumlah", color="Jenis",
                hover_data={"Narasi": True},
                title=f"Bubble Chart Keluhan dan Saran: {selected_branch}",
                color_discrete_sequence=px.colors.qualitative.Set1
            )

        elif chart_type == "Treemap":
            fig = px.treemap(
                data_chart, path=["Jenis"], values="Jumlah",
                hover_data={"Narasi": True},
                title=f"Treemap Keluhan dan Saran untuk Cabang: {selected_branch}",
                color="Jumlah", color_continuous_scale="Blues"
            )

        elif chart_type == "Sunburst":
            fig = px.sunburst(
                data_chart, path=["Jenis"], values="Jumlah",
                hover_data={"Narasi": True},
                title=f"Sunburst Chart Keluhan dan Saran: {selected_branch}",
                color="Jumlah", color_continuous_scale="Magma"
            )

        elif chart_type == "Funnel Chart":
            fig = px.funnel(
                data_chart, x="Jenis", y="Jumlah",
                hover_data={"Narasi": True},
                title=f"Funnel Chart Keluhan dan Saran: {selected_branch}"
            )

        elif chart_type == "Radar Chart":
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=data_chart["Jumlah"],
                theta=data_chart["Jenis"],
                text=data_chart["Narasi"],
                hoverinfo="text+r+theta",
                fill="toself",
                name="Keluhan dan Saran"
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title=f"Radar Chart Keluhan dan Saran: {selected_branch}",
                showlegend=True
            )

        st.plotly_chart(fig)

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










