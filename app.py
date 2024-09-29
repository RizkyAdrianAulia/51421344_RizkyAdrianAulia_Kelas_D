# Mengimport Library yang dibutuhkan
import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
from matplotlib.ticker import FuncFormatter

sns.set(style='dark')

#Membaca Dataset
df  = pd.read_csv("data_tanaman_padi_sumatra.csv")
df_outlier = df.select_dtypes(exclude=['object'])

def produksi_pada_provinsi(df):
    produksi_provinsi = df.groupby('Provinsi')['Produksi'].count().sort_index()
    
    return produksi_provinsi

def tahun_jumlah_produksi(df):
    tahun_produksi = df.groupby('Tahun')['Produksi'].count().sort_index()

    return tahun_produksi

def keuntungan_per_provinsi(df):
    untung_produksi = df.groupby('Provinsi')['Produksi'].sum().sort_index()

    return untung_produksi

def cek_outlier(df):
    q1 = df.select_dtypes(exclude=['object']).quantile (0.25)
    q3 = df.select_dtypes(exclude=['object']).quantile (0.75)
    iqr = q3-q1

    batas_bawah = q1 - (1.5 * iqr)
    batas_atas = q3 + (1.5 * iqr)
    outlier_data = (df.select_dtypes(exclude=['object']) < batas_bawah) | (df.select_dtypes(exclude=['object']) > batas_atas)


#Mengassign Dataset ke Function Yang Sudah Dibuat
produksi_pada_provinsi = produksi_pada_provinsi(df)
tahun_jumlah_produksi = tahun_jumlah_produksi(df)
keuntungan_per_provinsi = keuntungan_per_provinsi(df)
cek_outlier = cek_outlier(df)


tab1, tab2, tab3 = st.tabs(['Mengecek Outlier', 'Handling Outlier Kelembapan', 'Handling Outlier Suhu Rata-Rata'])
tab4, tab5, tab6 = st.tabs(['Produksi Tiap Provinsi', 'Jumlah Produksi Tahunan', 'Total Keuntungan per Provinsi'])


with tab1:
    q1 = df.select_dtypes(exclude=['object']).quantile (0.25)
    q3 = df.select_dtypes(exclude=['object']).quantile (0.75)
    iqr = q3-q1

    batas_atas = q3 + 1.5 * iqr
    batas_bawah = q1 - 1.5 * iqr

    outlier_data = (df.select_dtypes(exclude=['object']) < batas_bawah) | (df.select_dtypes(exclude=['object']) > batas_atas)

    df_outlier = df.select_dtypes(exclude=['object'])

    fig = plt.figure(figsize=(20,2))
    sns.boxplot(data=df_outlier, x=df_outlier['Kelembapan'])

    fig1 = plt.figure(figsize=(20,2))
    sns.boxplot(data=df_outlier, x=df_outlier['Suhu rata-rata'])

    st.pyplot(fig)
    st.pyplot(fig1)

with tab2:
    q1 = df.select_dtypes(exclude=['object']).quantile (0.25)
    q3 = df.select_dtypes(exclude=['object']).quantile (0.75)
    iqr = q3-q1

    df_outlier_data = df[~((df.select_dtypes(exclude="object") < q1 - 1.5 * iqr) | (df.select_dtypes(exclude="object") > q3 + 1.5 * iqr)).any(axis=1)]

    q1 = df_outlier_data['Kelembapan'].quantile(0.25)
    q3 = df_outlier_data['Kelembapan'].quantile(0.75)
    iqr = q3-q1

    print("Outlier data kelembapan sebelum dibersihkan")
    fig = plt.figure(figsize=(20,2))
    sns.boxplot(data=df_outlier_data, x=df_outlier_data['Kelembapan'])

    batas_atas = q3 + 1.5 * iqr
    batas_bawah = q1 - 1.5 * iqr
    total_outliers = (df_outlier_data['Kelembapan'] > batas_atas).sum()

    df = df_outlier_data[(df_outlier_data['Kelembapan'] >= batas_bawah) & (df_outlier_data['Kelembapan'] <= batas_atas)]

    print("Outlier data kelembapan setelah dibersihkan")
    fig1 = plt.figure(figsize=(20,2))
    sns.boxplot(data=df, x=df['Kelembapan'])

    st.pyplot(fig)
    st.pyplot(fig1)

with tab3:
    q1 = df.select_dtypes(exclude=['object']).quantile (0.25)
    q3 = df.select_dtypes(exclude=['object']).quantile (0.75)
    iqr = q3-q1

    df_outlier_data = df[~((df.select_dtypes(exclude="object") < q1 - 1.5 * iqr) | (df.select_dtypes(exclude="object") > q3 + 1.5 * iqr)).any(axis=1)]

    q1 = df_outlier_data['Suhu rata-rata'].quantile(0.25)
    q3 = df_outlier_data['Suhu rata-rata'].quantile(0.75)
    iqr = q3-q1

    print("Outlier data suhu sebelum dibersihkan")
    fig = plt.figure(figsize=(20,2))
    sns.boxplot(data=df_outlier_data, x=df_outlier_data['Suhu rata-rata'])

    batas_atas = q3 + 1.5 * iqr
    batas_bawah = q1 - 1.5 * iqr
    total_outliers = (df_outlier_data['Suhu rata-rata'] > batas_atas).sum()

    df = df_outlier_data[(df_outlier_data['Suhu rata-rata'] >= batas_bawah) & (df_outlier_data['Suhu rata-rata'] <= batas_atas)]

    print("Outlier data suhu setelah dibersihkan")
    fig1 = plt.figure(figsize=(20,2))
    sns.boxplot(data=df, x=df['Suhu rata-rata'])

    st.pyplot(fig)
    st.pyplot(fig1)

with tab4:
    fig = plt.figure(figsize=(12,8))
    myColors = sns.color_palette('viridis')[0:5]
    produksi_pada_provinsi.plot(kind='bar',color=myColors)
    plt.ylabel('Jumlah Produksi')
    plt.title('Provinsi')
    plt.show()

    st.pyplot(fig)

with tab5:
    fig = plt.figure(figsize=(12,8))

    myColors = sns.color_palette('crest')[0:5]
    tahun_jumlah_produksi.plot(kind='bar',color=myColors)

    plt.ylabel('Jumlah Produksi')
    plt.title('Tahun Produksi')
    plt.show()

    st.pyplot(fig)

with tab6:
    fig = plt.figure(figsize=(12,8))
    myColors = sns.color_palette('crest')[0:5]
    ax = keuntungan_per_provinsi.plot(kind='bar', color=myColors)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.2f}'))

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 5), 
                    textcoords='offset points')

    plt.ylabel('Keuntungan Produksi (Rp.)')
    plt.title('Provinsi Produksi')
    plt.show()
    st.pyplot(fig)


with st.sidebar:
    st.write('ASSOCIATE DATA SCIENCE :chart:')
    st.image('padi.png')
    st.write('Data Produksi Padi Pulau Sumatra')

