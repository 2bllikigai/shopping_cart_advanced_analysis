import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys

# Cấu hình trang
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

## 1. TIÊU ĐỀ VÀ SIDEBAR
st.title("📊 Hệ Thống Phân Khúc Khách Hàng Chuyên Sâu")
st.markdown("Dashboard kết hợp phân tích **RFM** và **Luật kết hợp (Association Rules)** để thấu hiểu hành vi khách hàng.")

with st.sidebar:
    st.header("Cấu hình mô hình")
    k_clusters = st.slider("Số lượng cụm (K)", 2, 8, 4)
    top_n_rules = st.number_input("Số lượng luật hiển thị mỗi cụm", 1, 10, 3)
    st.info("Dữ liệu được tải từ các file processed trong dự án.")

## 2. LOAD DỮ LIỆU (Caching để tăng tốc)
@st.cache_data
def load_data():
    # Giả định các file đã được lưu từ code trước đó của bạn
    df_trans = pd.read_csv('../data/processed/cleaned_uk_data.csv')
    df_rules = pd.read_csv('../data/processed/rules_fpgrowth_filtered.csv')
    df_results = pd.read_csv('../data/processed/customer_segments.csv')
    df_summary = pd.read_csv('../data/processed/cluster_profile_summary.csv', index_index=0)
    return df_trans, df_rules, df_results, df_summary

try:
    df_trans, df_rules, df_results, df_summary = load_data()
    
    ## 3. TỔNG QUAN CHỈ SỐ (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng khách hàng", f"{df_results.shape[0]:,}")
    col2.metric("Số lượng giao dịch", f"{df_trans.shape[0]:,}")
    col3.metric("Số lượng luật tìm thấy", len(df_rules))
    col4.metric("Số cụm phân tích", k_clusters)

    st.divider()

    ## 4. PHÂN TÍCH RFM TRỰC QUAN
    st.header("🎯 Phân Tích Chỉ Số RFM Theo Cụm")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Biểu đồ Boxplot so sánh RFM
        metrics = ['Recency', 'Frequency', 'Monetary']
        selected_metric = st.selectbox("Chọn chỉ số để so sánh:", metrics)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x='Cluster', y=selected_metric, data=df_results, palette='viridis', ax=ax)
        plt.title(f"Phân phối {selected_metric} giữa các cụm")
        st.pyplot(fig)

    with col_right:
        st.write("**Bảng thống kê trung bình:**")
        st.dataframe(df_summary[['Recency', 'Frequency', 'Monetary']].style.highlight_max(axis=0, color='#d4edda'))

    st.divider()

    ## 5. ĐẶC TRƯNG HÀNH VI (RULES)
    st.header("🛍️ Hành Vi Mua Sắm Theo Luật Kết Hợp")
    
    # Tạo các tabs cho mỗi cụm
    tabs = st.tabs([f"Cụm {i}" for i in range(k_clusters)])
    
    for i in range(k_clusters):
        with tabs[i]:
            st.subheader(f"Top {top_n_rules} Quy luật mua sắm của Cụm {i}")
            
            # Logic lấy rule giống hàm get_top_rules_for_cluster của bạn
            cluster_data = df_summary.loc[i]
            rule_cols = [c for c in cluster_data.index if c.startswith('Rule_')]
            top_rules_idx = cluster_data[rule_cols].sort_values(ascending=False).head(top_n_rules)
            
            for r_col, score in top_rules_idx.items():
                if score > 0.01:
                    idx = int(r_col.split('_')[1])
                    rule_info = df_rules.iloc[idx]
                    
                    with st.expander(f"{r_col} - Mức độ phổ biến: {score*100:.1f}%"):
                        st.write(f"**Khi khách mua:** `{rule_info['antecedents']}`")
                        st.write(f"**Họ thường mua thêm:** `{rule_info['consequents']}`")
                        st.write(f"👉 *Chỉ số Lift:* **{rule_info['lift']:.2f}**")
                else:
                    st.write("*(Không có luật nào đạt ngưỡng phổ biến trong cụm này)*")

    ## 6. PHÂN TÍCH KHÔNG GIAN (2D Visualization)
    st.header("🔍 Bản Đồ Phân Cụm 2D")
    # Sử dụng Plotly để biểu đồ có thể tương tác (zoom, hover)
    fig_2d = px.scatter(df_results, x='Recency', y='Monetary', color='Cluster',
                        size='Frequency', hover_data=['CustomerID'],
                        title="Trực quan hóa khách hàng trên không gian RFM",
                        color_continuous_scale='Portland')
    st.plotly_chart(fig_2d, use_container_width=True)

except FileNotFoundError:
    st.error("Không tìm thấy các file dữ liệu trong thư mục `../data/processed/`. Vui lòng chạy code phân tích trước để xuất file CSV.")