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

# Helper function to summarize narratives
def summarize_text(text, word_limit=10):
    words = text.split()
    return " ".join(words[:word_limit]) + ("..." if len(words) > word_limit else "")

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
        suggestions_count = branch_data["Saran"].count()

        st.write(f"**Jumlah Saran**: {suggestions_count}")

        data_chart = pd.DataFrame({
            "Jenis": ["Saran"],
            "Jumlah": [suggestions_count],
            "Narasi": [
                summarize_text(" ".join(branch_data["Saran"].dropna().to_list()))
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

    st.subheader("Word Cloud Saran")
    saran_text = " ".join(branch_data["Saran"].dropna().tolist())
    wordcloud_saran = WordCloud(width=800, height=400, background_color='white',
                                stopwords=custom_stopwords).generate(saran_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud_saran, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # Feature: Combined Chart for Keluhan and Saran
    st.subheader("Combined Chart for Keluhan dan Saran")
    combined_chart_data = branch_data.melt(id_vars="Cabang", value_vars=["Saran"], var_name="Jenis", value_name="Narasi")
    combined_chart_data = combined_chart_data.dropna()
    combined_chart_data["Count"] = 1
    combined_summary = combined_chart_data.groupby(["Jenis", "Narasi"]).sum().reset_index()
    combined_summary["Narasi"] = combined_summary["Narasi"].apply(lambda x: summarize_text(x))

    combined_chart = px.bar(
        combined_summary, x="Narasi", y="Count", color="Jenis",
        title=f"Combined View of Keluhan dan Saran for Cabang: {selected_branch}",
        labels={"Narasi": "Narasi", "Count": "Jumlah"},
        color_discrete_map={"Saran": "#33FF57"},
        hover_data={"Narasi": True}
    )
    combined_chart.update_xaxes(tickangle=45, title_text="Narasi", title_font=dict(size=12))
    combined_chart.update_yaxes(title_text="Jumlah", title_font=dict(size=12))
    st.plotly_chart(combined_chart)

    # Feature: Total Accumulated Complaints and Suggestions
    st.subheader("Total Keluhan dan Saran")
    total_summary = df.melt(id_vars="Cabang", value_vars=["Saran"], var_name="Jenis", value_name="Narasi")
    total_summary = total_summary.dropna()
    total_summary["Count"] = 1
    total_counts = total_summary.groupby("Jenis").sum().reset_index()

    total_chart = px.bar(
        total_counts, x="Jenis", y="Count",
        title="Total Akumulasi Keluhan dan Saran",
        labels={"Jenis": "Jenis", "Count": "Jumlah"},
        color="Jenis",
        color_discrete_map={"Saran": "#33FF57"}
    )
    total_chart.update_traces(textposition="outside")
    st.plotly_chart(total_chart)

if __name__ == "__main__":
    main()














