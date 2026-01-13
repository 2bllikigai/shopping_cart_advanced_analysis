import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from ast import literal_eval 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Cấu hình trang
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

## 1. TIÊU ĐỀ VÀ SIDEBAR
st.title("📊 Hệ Thống Phân Khúc Khách Hàng Chuyên Sâu")
st.markdown(
    "Dashboard kết hợp phân tích **RFM** và **Luật kết hợp (Association Rules)** để thấu hiểu hành vi khách hàng."
)

with st.sidebar:
    st.header("Cấu hình mô hình")
    k_clusters = st.slider("Số lượng cụm (K)", 2, 8, 4)
    top_n_rules = st.number_input("Số lượng luật hiển thị mỗi cụm", 1, 10, 3)
    st.info("Dữ liệu được tải từ thư mục data/processed")


## 2. HÀM XỬ LÝ DỮ LIỆU
# Hàm làm sạch chuỗi luật (Biến "frozenset({'Item A'})" thành "Item A")
def clean_rule_text(rule_str):
    try:
        if isinstance(rule_str, str):
            # Dùng literal_eval để biến chuỗi thành set thật
            rule_set = literal_eval(rule_str)
            # Chuyển thành chuỗi ngăn cách bởi dấu phẩy
            return ", ".join(list(rule_set))
        return str(rule_str)
    except:
        return str(rule_str)

@st.cache_data
def load_data():
    base_path = "data/processed/"

    if not os.path.exists(base_path):
        st.error(
            f"Không tìm thấy thư mục '{base_path}'. Vui lòng kiểm tra xem bạn đã chạy Notebook để xuất file CSV chưa."
        )
        return None, None, None, None

    # Load dữ liệu
    try:
        df_trans = pd.read_csv(f"{base_path}cleaned_uk_data.csv")
        df_rules = pd.read_csv(f"{base_path}rules_fpgrowth_filtered.csv")
        df_results = pd.read_csv(f"{base_path}customer_segments.csv")
        
        # Load file summary (Index cột 0 là Cluster ID)
        df_summary = pd.read_csv(f"{base_path}cluster_profile_summary.csv", index_col=0)

        # Xử lý cột CustomerID nếu bị lỗi tên
        if "CustomerID" not in df_results.columns:
            if "Unnamed: 0" in df_results.columns:
                df_results.rename(columns={"Unnamed: 0": "CustomerID"}, inplace=True)
            else:
                df_results["CustomerID"] = df_results.index

        return df_trans, df_rules, df_results, df_summary
    except Exception as e:
        st.error(f"Lỗi khi đọc file CSV: {e}")
        return None, None, None, None


try:
    df_trans, df_rules, df_results, df_summary = load_data()

    if df_trans is not None:
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
            metrics = ["Recency", "Frequency", "Monetary"]
            selected_metric = st.selectbox("Chọn chỉ số để so sánh:", metrics)

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.boxplot(
                x="Cluster",
                y=selected_metric,
                data=df_results,
                palette="viridis",
                ax=ax,
            )
            plt.title(f"Phân phối {selected_metric} giữa các cụm")
            st.pyplot(fig)

        with col_right:
            st.write("**Bảng thống kê trung bình:**")
            st.dataframe(
                df_summary[["Recency", "Frequency", "Monetary"]].style.highlight_max(
                    axis=0, color="#d4edda"
                )
            )

        st.divider()

        ## 5. CHIẾN LƯỢC & LUẬT KẾT HỢP
        st.header("🛍️ Phân Tích Chi Tiết & Chiến Lược Hành Động")

        # Định nghĩa chiến lược (Bạn có thể sửa text ở đây cho phù hợp với biểu đồ RFM thực tế)
        cluster_strategies = {
            0: {
                "name": "Nhóm Vàng (Loyal)",
                "desc": "Khách mua thường xuyên và chi tiêu cao.",
                "action": "Chăm sóc đặc biệt, upsell sản phẩm cao cấp."
            },
            1: {
                "name": "Nhóm Rời bỏ (Churn)",
                "desc": "Mua nhiều trong quá khứ nhưng lâu không quay lại.",
                "action": "Gửi email 'We miss you' kèm mã giảm giá."
            },
            2: {
                "name": "Nhóm Tiết kiệm (Low Value)",
                "desc": "Mua ít và giá trị đơn hàng thấp.",
                "action": "Gợi ý combo giá rẻ để tăng giá trị giỏ hàng."
            },
            3: {
                "name": "Nhóm Mới/Tiềm năng",
                "desc": "Mới mua gần đây, tần suất trung bình.",
                "action": "Cross-sell sản phẩm liên quan để giữ chân."
            }
        }
        default_strategy = {"name": "Nhóm Khách hàng", "desc": "Đang phân tích...", "action": "Tiếp tục theo dõi."}

        tabs = st.tabs([f"Cụm {i}" for i in range(k_clusters)])
        
        for i in range(k_clusters):
            with tabs[i]:
                # 5.1 HIỂN THỊ PERSONA & STRATEGY
                strategy = cluster_strategies.get(i, default_strategy)
                st.info(f"💡 **Persona:** {strategy['name']} - {strategy['desc']}")
                st.success(f"🚀 **Chiến lược:** {strategy['action']}")
                
                st.divider()
                
                # 5.2 HIỂN THỊ LUẬT KẾT HỢP (Đã nâng cấp hiển thị)
                st.subheader(f"Top {top_n_rules} Quy luật nổi bật của Cụm {i}")
                
                if i in df_summary.index:
                    cluster_data = df_summary.loc[i]
                    rule_cols = [c for c in cluster_data.index if c.startswith('Rule_')]
                    
                    if rule_cols:
                        top_rules_idx = cluster_data[rule_cols].sort_values(ascending=False).head(top_n_rules)
                        
                        has_rule = False
                        for r_col, score in top_rules_idx.items():
                            if score > 0.0: # Chỉ hiện luật có xuất hiện trong cụm
                                has_rule = True
                                idx = int(r_col.split('_')[1])
                                
                                if idx < len(df_rules):
                                    rule_info = df_rules.iloc[idx]
                                    
                                    # --- SỬA Ở ĐÂY: Dùng hàm clean_rule_text ---
                                    ant = clean_rule_text(rule_info['antecedents'])
                                    con = clean_rule_text(rule_info['consequents'])
                                    
                                    with st.expander(f"Quy luật {idx} - Độ phổ biến: {score*100:.1f}%"):
                                        st.markdown(f"🛒 **Khách mua:** `{ant}`")
                                        st.markdown(f"🎁 **Thường mua thêm:** `{con}`")
                                        col_a, col_b = st.columns(2)
                                        col_a.caption(f"Lift: {rule_info['lift']:.2f}")
                                        col_b.caption(f"Confidence: {rule_info.get('confidence', 0):.2f}")
                        
                        if not has_rule:
                                st.warning("Các luật trong cụm này có tần suất xuất hiện rất thấp.")
                    else:
                        st.warning("Không tìm thấy dữ liệu luật trong bảng tổng hợp.")
                else:
                    st.warning(f"Không có dữ liệu cho cụm {i}")

        ## 6. PHÂN TÍCH KHÔNG GIAN (PCA)
        st.header("🔍 Trực Quan Hóa Phân Cụm (PCA)")
        st.markdown("Biểu đồ giảm chiều dữ liệu (RFM + Rules) xuống 2D giúp quan sát độ tách biệt giữa các cụm.")

        feature_cols = [c for c in df_results.columns if c not in ['CustomerID', 'Cluster', 'dbscan_labels']]
        
        if len(feature_cols) > 1:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df_results[feature_cols].fillna(0))
            
            pca = PCA(n_components=2)
            components = pca.fit_transform(X_scaled)
            
            df_pca = df_results.copy()
            df_pca['PC1'] = components[:, 0]
            df_pca['PC2'] = components[:, 1]
            
            fig_pca = px.scatter(
                df_pca, 
                x='PC1', 
                y='PC2', 
                color='Cluster',
                title=f"Biểu đồ PCA (Giải thích {sum(pca.explained_variance_ratio_)*100:.1f}% phương sai)",
                hover_data=['CustomerID', 'Recency', 'Monetary'],
                color_continuous_scale='Turbo'
            )
            st.plotly_chart(fig_pca, use_container_width=True)
        else:
            st.error("Không đủ dữ liệu để chạy PCA.")

except Exception as e:
    st.error(f"Đã xảy ra lỗi hệ thống: {e}")