import pandas as pd
import plotly.express as px
import streamlit as st

# Atur halaman menjadi lebar penuh
st.set_page_config(layout="wide")

# CSS untuk mengatur margin, padding, dan kotak
st.markdown(
    """
    <style>
    .main {
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 10px;
    }
    .block-container {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .center-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load dataset
file_path = 'Penyebab Kematian di Indonesia yang Dilaporkan - Clean.csv'
data = pd.read_csv(file_path)

# Title
st.markdown('<h1 class="center-title">Penyebab Kematian di Indonesia</h1>', unsafe_allow_html=True)

# Filter section
st.subheader("Filter Data")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    year = st.selectbox("Tahun", sorted(data['Year'].unique()), index=len(data['Year'].unique())-1)

with col2:
    filtered_data_by_year = data[data['Year'] == year]
    type_filter = st.selectbox(
        "Kategori Penyebab Kematian",
        options=sorted(filtered_data_by_year['Type'].unique()),
        index=0
    )

with col3:
    filtered_data_by_type = filtered_data_by_year[filtered_data_by_year['Type'] == type_filter]
    cause = st.multiselect(
        "Penyebab Kematian",
        options=sorted(filtered_data_by_type['Cause'].unique()),
        default=sorted(filtered_data_by_type['Cause'].unique())
    )

filtered_data = filtered_data_by_type[filtered_data_by_type['Cause'].isin(cause)]

# Separator
st.markdown('<hr>', unsafe_allow_html=True)

# Trends in Causes of Death 
st.markdown('<div class="box">', unsafe_allow_html=True)
st.header(f"Tren Kematian di Indonesia Berdasarkan Kategori Penyebab Hingga Tahun {year}")
allyears = sorted(data['Year'].unique())
alltypes = sorted(data['Type'].unique())
index = pd.MultiIndex.from_product([allyears, alltypes], names=['Year', 'Type'])
dataGroupby = data.groupby(['Year', 'Type'])['Total Deaths'].sum().reindex(index, fill_value=0).reset_index()
line_chart = px.line(
    dataGroupby[dataGroupby['Year'] <= year],
    x='Year',
    y='Total Deaths',
    color='Type',
    labels={'Year': 'Tahun', 'Total Deaths': 'Total Kematian', 'Type': 'Kategori Penyebab'},
)
st.plotly_chart(line_chart, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
with st.expander("Deskripsi"):
        st.write("""
        Grafik ini menunjukkan perubahan jumlah kematian berdasarkan kategori penyebab kematian di Indonesia. Tren ini membantu
        mengidentifikasi pola jumlah kematian di Indonesia berdasarkan kategori penyebab dari tahun ke tahun.
        """)

# Rows for percentage and total deaths by Category of cause
row2_col1, row2_col2 = st.columns(2)

# Percentage total deaths by category
with row2_col1:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader(f"Persentase Total Kematian Berdasarkan Kategori Penyebab di Tahun {year}")
    percentDeath = filtered_data_by_year.groupby('Type')['Total Deaths'].sum().reset_index()
    pie_chart = px.pie(
        percentDeath,
        names='Type',
        values='Total Deaths',
        labels={'Type': 'Kategori Penyebab', 'Total Deaths': 'Total Kematian'}
    )
    st.plotly_chart(pie_chart)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("Deskripsi"):
        st.write("""
        Grafik ini menunjukkan persentase distribusi kematian berdasarkan 
        tiga kategori utama yaitu, Bencana Alam, Bencana Non-Alam dan Penyakit, dan Bencana Sosial.
        Persentase ini memberi informasi terkait kategori penyebab kematian terbanyak di Indonesia di tahun tertentu.
        """)

# Total deaths
with row2_col2:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader(f"Total Kematian Berdasarkan Penyebab untuk {type_filter} di Tahun {year}")
    if not filtered_data.empty:
        causeChart = px.bar(
            filtered_data,
            x='Cause',
            y='Total Deaths',
            labels={'Cause': 'Penyebab', 'Total Deaths': 'Total Kematian'},
            text='Total Deaths',
            color='Total Deaths',
            color_continuous_scale='Viridis'
        )
        causeChart.update_layout(coloraxis_showscale=False)
        st.plotly_chart(causeChart)
    else:
        st.write("Tidak ada data untuk penyebab kematian yang dipilih.")
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("Deskripsi"):
        st.write("""
        Grafik ini memberikan rincian jumlah kematian berdasarkan penyebab spesifik dalam kategori tertentu. 
        Grafik ini membantu mengindentifikasi akar masalah pada jumlah kematian di Indonesia dalam kategori tertentu.
        """)

# Separator
st.markdown('<hr>', unsafe_allow_html=True)

# Leading Cause of Death
st.markdown('<div class="box">', unsafe_allow_html=True)
st.header("Penyebab Kematian Terbanyak di Indonesia")
causeTotals = data.groupby('Cause')['Total Deaths'].sum().reset_index()
causeTotals = causeTotals.sort_values(by='Total Deaths', ascending=False).head(10)
causeTotalchart = px.bar(
    causeTotals,
    x='Cause',
    y='Total Deaths',
    labels={'Cause': 'Penyebab', 'Total Deaths': 'Total Kematian'},
    text='Total Deaths',
    color='Total Deaths',
    color_continuous_scale='Blues'
)
causeTotalchart.update_layout(showlegend=False, coloraxis_showscale=False)
st.plotly_chart(causeTotalchart, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
