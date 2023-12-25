import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv('all_data.csv')

all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

def create_products_df(df):
    total_products_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "product_id": "nunique"
    })

    total_products_df = total_products_df.reset_index()
    total_products_df.rename(columns={
        "product_id": "product_count"
    }, inplace=True)

    return total_products_df

def create_purchase_category_df(df):
    purchase_category_df = df.groupby(by="product_category_name_english")["product_id"].count().reset_index() # Menentukan jumlah pembelian
    purchase_category_df = purchase_category_df.rename(columns={"product_category_name_english": "category",
                                                            "product_id": "orders"})
    
    return purchase_category_df

def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%m-%Y')

    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    
    return monthly_orders_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id", as_index=False).agg(
    max_order_date = ("order_purchase_timestamp", "max"), # mengambil tanggal order terakhir
    frequency = ("order_id", "nunique"), # menghitung jumlah order
    monetary = ("total_order_value", "sum") # menghitung total jumlah uang untuk pemesanan
    )

    rfm_df['max_order_date'] = rfm_df['max_order_date'].dt.date #mengubah menjadi format tanggal
    recent_order_date = all_df['order_purchase_timestamp'].dt.date.max() #memilih hari terakhir dalam kolom order_purchase_timestamp
    rfm_df.insert(1,'recency', rfm_df['max_order_date'].apply(lambda x: (recent_order_date - x).days)) #mencari selisih kapan terakhir pelanggan bertransaksi
    rfm_df.drop('max_order_date', axis=1, inplace=True) #menghapus kolom yang tidak dibutuhkan
    rfm_df.head(10)
    
    return rfm_df

#Membuat komponen Filter
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://dnn65p9ixwrwn.cloudfront.net/uploads/2022/06/logo-olist-site.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

products_df = create_products_df(main_df)
purchase_category_df = create_purchase_category_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header('E-Commerce Dashboard 🛍️')

# Kategori produk dengan pembelian terbanyak dan paling sedikit
st.subheader("Most and Least Purchased Products by Category")
col1, col2 = st.columns(2)

with col1:
    total_product = products_df.product_count.sum()
    st.metric("Total Items", value=total_product)
 
with col2:
    total_average = round(products_df.product_count.mean(), 2)
    st.metric("Average Items", value=total_average)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="orders", y="category", data=purchase_category_df.sort_values(by="orders", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Pembelian Terbanyak", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="orders", y="category", data=purchase_category_df.sort_values(by="orders", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Pembelian Paling Sedikit", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# tren penjualan bulanan selama periode tertentu
st.subheader("Monthly Sales Trend Over a Specific Period")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["order_count"], marker='o', linewidth=2, color="#72BCD4")
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10, rotation=45) 
st.pyplot(fig)

#Pelanggan terbaik berdasarkan pesanan terakhirnya, frekuensi order, dan total nilai ordernya
st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "BRL", locale="pt_BR") 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))
colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

sns.barplot(x="customer_unique_id", y="recency", data= rfm_df.sort_values(by='recency', ascending=True).head(10), palette=colors, ax=ax[0])
ax[0].set_ylabel('Hari', fontsize=25)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency(Days)", loc="center", fontsize=30)
ax[0].tick_params(axis ='y', labelsize=20)
ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=20)

sns.barplot(x="customer_unique_id", y="frequency", data= rfm_df.sort_values(by='frequency', ascending=False).head(10), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=20)

sns.barplot(x="customer_unique_id", y="monetary", data= rfm_df.sort_values(by='monetary', ascending=False).head(10), palette=colors, ax=ax[2])
ax[2].set_ylabel('R$', fontsize=25)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=30)
ax[2].tick_params(axis ='y', labelsize=20)
ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=20)
st.pyplot(fig)




