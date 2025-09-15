import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard title and description
st.title("📊 Dashboard Analisis Data E-Commerce")
st.write("""
Dashboard ini menampilkan hasil analisis data E-Commerce, menjawab lima pertanyaan bisnis utama:
1. Bagaimana Pola Pembelian Pelanggan?
2. Bagaimana Pola Pembelian Berdasarkan Kategori Produk?
3. Seberapa Besar Pengaruh Biaya Pengiriman terhadap Jumlah Transaksi?
4. Bagaimana Distribusi Metode Pembayaran yang Paling Sering Digunakan?
5. Bagaimana Pola Loyalitas Pelanggan Berdasarkan RFM Analysis?
""")

# Function to load data with error handling
@st.cache_data
def load_data():
    try:
        # Pastikan path data relatif terhadap lokasi dashboard.py
        data_path = "../data/"
        df_orders = pd.read_csv(f"{data_path}orders_dataset.csv")
        df_items = pd.read_csv(f"{data_path}order_items_dataset.csv")
        df_pay = pd.read_csv(f"{data_path}order_payments_dataset.csv")
        df_product = pd.read_csv(f"{data_path}products_dataset.csv")
        df_cust = pd.read_csv(f"{data_path}customers_dataset.csv")
        st.success("Data berhasil dimuat dari file lokal!")
    except FileNotFoundError:
        # Jika file tidak ditemukan, berikan opsi upload
        st.warning("File CSV tidak ditemukan. Silakan upload file Anda.")
        
        # Create file uploaders
        uploaded_files = {}
        file_names = ["orders_dataset.csv", "order_items_dataset.csv", 
                      "order_payments_dataset.csv", "products_dataset.csv", 
                      "customers_dataset.csv"]
        
        for file in file_names:
            uploaded_files[file] = st.file_uploader(f"Upload {file}", type="csv")
        
        # Check if all files are uploaded
        if all(uploaded_files.values()):
            df_orders = pd.read_csv(uploaded_files["orders_dataset.csv"])
            df_items = pd.read_csv(uploaded_files["order_items_dataset.csv"])
            df_pay = pd.read_csv(uploaded_files["order_payments_dataset.csv"])
            df_product = pd.read_csv(uploaded_files["products_dataset.csv"])
            df_cust = pd.read_csv(uploaded_files["customers_dataset.csv"])
            st.success("Semua file berhasil diupload!")
        else:
            st.error("Silakan upload semua file yang diperlukan")
            # Gunakan placeholder empty DataFrames jika data tidak tersedia
            df_orders = pd.DataFrame()
            df_items = pd.DataFrame()
            df_pay = pd.DataFrame()
            df_product = pd.DataFrame() 
            df_cust = pd.DataFrame()
            return df_orders, df_items, df_pay, df_product, df_cust
    
    # Preprocessing - konversi timestamp dan tambah kolom waktu
    if not df_orders.empty:
        df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
        df_orders['year'] = df_orders['order_purchase_timestamp'].dt.year
        df_orders['month'] = df_orders['order_purchase_timestamp'].dt.month
        df_orders['order_yearmonth'] = df_orders['order_purchase_timestamp'].dt.to_period('M')
    
    return df_orders, df_items, df_pay, df_product, df_cust

# Load data
df_orders, df_items, df_pay, df_product, df_cust = load_data()

# Only proceed if data is loaded successfully
if not any(df.empty for df in [df_orders, df_items, df_pay, df_product, df_cust]):
    # Sidebar filters
    st.sidebar.header("Filter Data")
    
    # Year filter
    years = sorted(df_orders["year"].unique())
    selected_year = st.sidebar.selectbox("Pilih Tahun", years)
    
    # Merge orders with customers to get state info
    merged_orders_cust = pd.merge(df_orders, df_cust, on='customer_id', how='left')
    
    # State filter
    states = sorted(merged_orders_cust["customer_state"].unique())
    selected_state = st.sidebar.selectbox("Pilih State", ["All"] + list(states))
    
    # Apply filters
    if selected_state == "All":
        df_filtered = df_orders[df_orders["year"] == selected_year]
    else:
        df_year_filtered = df_orders[df_orders["year"] == selected_year]
        merged_df = pd.merge(df_year_filtered, df_cust, on='customer_id', how='inner')
        df_filtered = merged_df[merged_df["customer_state"] == selected_state]
    
    # Show active filters info
    st.sidebar.info(f"""
    **Filter Aktif:**
    - Tahun: {selected_year}
    - State: {selected_state if selected_state != 'All' else 'Semua State'}
    - Total Data: {len(df_filtered)} pesanan
    """)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pesanan", f"{len(df_filtered):,}")
    with col2:
        merged_items = df_items.merge(df_filtered[['order_id']], on='order_id', how='inner')
        avg_price = merged_items['price'].mean() if not merged_items.empty else 0
        st.metric("Rata-rata Harga", f"${avg_price:.2f}")
    with col3:
        avg_freight = merged_items['freight_value'].mean() if not merged_items.empty else 0
        st.metric("Rata-rata Ongkir", f"${avg_freight:.2f}")
    with col4:
        status_counts = df_filtered['order_status'].value_counts()
        delivered_pct = status_counts.get('delivered', 0) / len(df_filtered) * 100 if len(df_filtered) > 0 else 0
        st.metric("% Pesanan Terkirim", f"{delivered_pct:.1f}%")
    
    # Create tabs for each business question
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ Pola Pembelian", 
        "2️⃣ Kategori Produk", 
        "3️⃣ Biaya Pengiriman", 
        "4️⃣ Metode Pembayaran",
        "5️⃣ RFM Analysis"
    ])
    
    # Tab 1: Purchase Patterns
    with tab1:
        st.header("Bagaimana Pola Pembelian Pelanggan?")
    
        # Menggunakan hasil analisis dari notebook.ipynb
        df_filtered['order_month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M')
        monthly_sales = df_filtered.groupby('order_month').size()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_sales.plot(kind='line', marker='o', ax=ax)
        ax.set_title(f'Tren Penjualan Bulanan ({selected_year})')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Jumlah Pesanan')
        ax.grid(True)
        st.pyplot(fig)
        
        # Add tab-specific insights and recommendations
        st.subheader("Kesimpulan & Rekomendasi")
        st.markdown("""
        #### **Pola Pembelian Pelanggan**
        - Mayoritas pelanggan hanya melakukan **satu kali transaksi**.
        - Pengeluaran pelanggan cenderung kecil dan tidak merata.
        - **Rekomendasi:** Gunakan **loyalty rewards** & **email marketing** untuk meningkatkan repeat orders.
        """)
    
    # Tab 2: Product Categories
    with tab2:
        st.header("Bagaimana Pola Pembelian Berdasarkan Kategori Produk?")
    
        # Menggunakan hasil analisis dari notebook.ipynb
        df_merged = df_items.merge(df_filtered[['order_id']], on='order_id', how='inner')
        df_merged = df_merged.merge(df_product[['product_id', 'product_category_name']], on='product_id', how='left')
        
        # Top product categories
        df_category_sales = df_merged['product_category_name'].value_counts().reset_index()
        df_category_sales.columns = ['Kategori Produk', 'Total Penjualan']
        
        # Show top categories as bar chart
        top_n = min(10, len(df_category_sales))
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=df_category_sales.head(top_n), 
                y='Kategori Produk', x='Total Penjualan', 
                palette='viridis', ax=ax)
        ax.set_title(f'Top {top_n} Kategori Produk Terlaris')
        ax.set_xlabel('Jumlah Penjualan')
        ax.set_ylabel('Kategori Produk')
        st.pyplot(fig)
        
        # Add tab-specific insights and recommendations
        st.subheader("Kesimpulan & Rekomendasi")
        st.markdown("""
        #### **Pola Pembelian Berdasarkan Kategori Produk**
        - Kategori dengan harga rendah lebih sering dibeli.
        - Produk mahal memiliki transaksi lebih sedikit tetapi nilai pembelian lebih besar.
        - **Rekomendasi:** Fokus promosi pada kategori populer dan gunakan **bundling/upselling**.
        """)
    
    # Tab 3: Shipping Cost Analysis
    with tab3:
        st.header("Seberapa Besar Pengaruh Biaya Pengiriman terhadap Jumlah Transaksi?")
    
        # Menggunakan hasil analisis dari notebook.ipynb
        df_shipping = df_items.merge(df_filtered[['order_id']], on='order_id', how='inner')
        
        # Correlation calculation
        correlation = df_shipping[['price', 'freight_value']].corr().iloc[0, 1]
        st.write(f"Korelasi antara harga produk dan biaya pengiriman: **{correlation:.4f}**")
        
        # Price vs shipping cost scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_shipping, x='price', y='freight_value', alpha=0.5, ax=ax)
        ax.set_title('Hubungan antara Harga Produk dan Biaya Pengiriman')
        ax.set_xlabel('Harga Produk')
        ax.set_ylabel('Biaya Pengiriman')
        st.pyplot(fig)
        
        # Add tab-specific insights and recommendations
        st.subheader("Kesimpulan & Rekomendasi")
        st.markdown("""
        #### **Pengaruh Biaya Pengiriman terhadap Transaksi**
        - Transaksi lebih banyak terjadi pada ongkir rendah.
        - Ongkir tinggi mengurangi jumlah pembelian.
        - **Rekomendasi:** Terapkan **gratis ongkir dengan minimum belanja** untuk meningkatkan nilai transaksi.
        """)
    
    # Tab 4: Payment Methods
    with tab4:
        st.header("Bagaimana Distribusi Metode Pembayaran yang Paling Sering Digunakan?")
    
        # Menggunakan hasil analisis dari notebook.ipynb
        df_payment = df_pay.merge(df_filtered[['order_id']], on='order_id', how='inner')
        
        # Payment method distribution
        payment_distribution = df_payment['payment_type'].value_counts().reset_index()
        payment_distribution.columns = ['Metode Pembayaran', 'Jumlah Transaksi']
        
        # Payment method pie chart
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(payment_distribution['Jumlah Transaksi'], 
            labels=payment_distribution['Metode Pembayaran'], 
            autopct='%1.1f%%', 
            colors=sns.color_palette('pastel'),
            startangle=90)
        ax.set_title('Distribusi Metode Pembayaran')
        st.pyplot(fig)
        
        # Add tab-specific insights and recommendations
        st.subheader("Kesimpulan & Rekomendasi")
        st.markdown("""
        #### **Distribusi Metode Pembayaran**
        - Kartu kredit paling dominan.
        - Metode alternatif seperti **boleto dan voucher** masih rendah.
        - **Rekomendasi:** Perluas opsi pembayaran dan berikan **promo khusus untuk metode alternatif**.
        """)
    
    # Tab 5: RFM Analysis
    with tab5:
        st.header("Bagaimana Pola Loyalitas Pelanggan Berdasarkan RFM Analysis?")
    
        # Menggunakan hasil analisis dari notebook.ipynb
        reference_date = df_orders['order_purchase_timestamp'].max()
        
        # Choose base dataset for RFM based on filters
        if selected_state == "All":
            df_rfm_base = df_orders[df_orders["year"] == selected_year]
        else:
            df_rfm_base = df_filtered
        
        # Calculate RFM components
        rfm = df_rfm_base.groupby('customer_id').agg(
            recency=('order_purchase_timestamp', lambda x: (reference_date - x.max()).days),
            frequency=('order_id', 'count')
        ).reset_index()
        
        # Add monetary component
        df_pay_agg = df_pay.groupby('order_id')['payment_value'].sum().reset_index()
        df_orders_pay = df_rfm_base.merge(df_pay_agg, on='order_id', how='left')
        monetary_data = df_orders_pay.groupby('customer_id')['payment_value'].sum().reset_index()
        
        rfm = rfm.merge(monetary_data, on='customer_id', how='left')
        rfm.rename(columns={'payment_value': 'monetary'}, inplace=True)
        
        # RFM distributions in one figure
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # Recency distribution
        sns.histplot(rfm['recency'], bins=30, kde=True, ax=axes[0], color='blue')
        axes[0].set_title('Distribusi Recency')
        axes[0].set_xlabel('Hari sejak transaksi terakhir')
        
        # Frequency distribution
        sns.histplot(rfm['frequency'], bins=30, kde=True, ax=axes[1], color='green')
        axes[1].set_title('Distribusi Frequency')
        axes[1].set_xlabel('Jumlah Transaksi')
        
        # Monetary distribution
        sns.histplot(rfm['monetary'], bins=30, kde=True, ax=axes[2], color='red')
        axes[2].set_title('Distribusi Monetary')
        axes[2].set_xlabel('Total Pengeluaran')
        
        st.pyplot(fig)
        
        # Add tab-specific insights and recommendations
        st.subheader("Kesimpulan & Rekomendasi")
        st.markdown("""
        #### **Loyalitas Pelanggan Berdasarkan RFM**
        - Sebagian besar pelanggan jarang bertransaksi.
        - **Rekomendasi:** Gunakan **segmentasi pelanggan** dan berikan **promo khusus untuk pelanggan potensial**.
        """)
    
else:
    st.error("Data tidak berhasil dimuat. Silakan periksa file atau upload data Anda.")