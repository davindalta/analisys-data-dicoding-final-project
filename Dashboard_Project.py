import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

all_df = pd.read_csv('all_df.csv')

all_df.rename(columns={ # rename kolom product_category_name_english dan order_id
    'product_category_name_english':'products_name',
    'order_id':'order_count'
}, inplace=True)
# mengelompokkan berdasarkan products_name
sum_orders_df = all_df.groupby(by='products_name').agg({
    'order_count':'nunique'
}).reset_index().sort_values(by='order_count', ascending=False)


# -------------------------------
# mengelompokkan berdasarkan customer_state
all_df.groupby(by='customer_state').customer_id.nunique().sort_values(ascending=False)


# -------------------------------
# RFM Analysis
rfm_df = all_df.groupby(by='customer_id', as_index=False).agg({
    'order_purchase_timestamp':'max',
    'order_count':'nunique',
    'payment_value':'sum'
})

rfm_df.columns = ['customer_id', 'max_order_timestamp', 'frequency', 'monetary']

# menghitung kapan terakhir kali pelanggan melakukan transaksi (hari)
rfm_df['max_order_timestamp'] = pd.to_datetime(rfm_df['max_order_timestamp'])

recent_date = pd.to_datetime(all_df['order_purchase_timestamp']).max()

rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)

rfm_df.drop('max_order_timestamp', axis=1, inplace=True)


# =======================================================================

st.header("Dasboard Project :sparkles:")

st.subheader("Best and Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 20))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='order_count', y='products_name', data=sum_orders_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Number of Sales', fontsize=30)
ax[0].set_title('Best Performing Product', loc='center', fontsize=50)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].tick_params(axis='y', labelsize=30)

sns.barplot(x='order_count', y='products_name', data=sum_orders_df.sort_values(by='order_count', ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('Number of Sales', fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].tick_params(axis='y', labelsize=30)

st.pyplot(fig)


# -----------------------------------------------------
# mengidentifikasi demografi pelanggan berdasarkan state
st.subheader("Number of Customer by States")
bystate_df = all_df.groupby(by='customer_state').customer_id.nunique().reset_index()
bystate_df.rename(columns={
    'customer_id':'customer_count'
}, inplace=True)

fig, ax = plt.subplots(figsize=(20, 10))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x = 'customer_count',
    y = 'customer_state',
    data = bystate_df.sort_values(by='customer_count', ascending=False).head(10),
    palette=colors_,
    ax=ax
)

plt.title('Number of Customer by States', loc='center', fontsize=30)
plt.xlabel('Number of Customers', fontsize=20)
plt.ylabel(None)
plt.tick_params(axis='x', labelsize=25)
plt.tick_params(axis='y', labelsize=25)
st.pyplot(fig)


# ------------------------------------------
# RFM Analysis
st.subheader("RFM Analysis")

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "EUR", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 12))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=25)
ax[0].tick_params(axis ='x', labelsize=20)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=25)
ax[1].tick_params(axis='x', labelsize=20)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=25)
ax[2].tick_params(axis='x', labelsize=20)

st.pyplot(fig)