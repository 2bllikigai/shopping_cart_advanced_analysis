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
def clean_rule_text(raw_text):
    text = str(raw_text)
    # Danh sách các ký tự rác cần xóa bỏ khỏi chuỗi
    garbage_list = ["frozenset({", "})", "frozenset", "{", "}", "'", '"']
    
    for garbage in garbage_list:
        text = text.replace(garbage, "")
    
    return text.strip()

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
            "name": "Nhóm Vàng (Champions)",
            "desc": "Chi tiêu mạnh tay (M cao), mua thường xuyên (F cao) và mới mua gần đây (R thấp).",
            "action": "Ưu tiên số 1: Giới thiệu sản phẩm mới nhất, đắt nhất."
        },
        1: {
            "name": "Nhóm Trung Thành (Loyal)",
            "desc": "Mua hàng đều đặn (F cao), là nguồn thu ổn định.",
            "action": "Tặng điểm thưởng, gợi ý sản phẩm mua kèm (Cross-sell)."
        },
        2: {
            "name": "Nhóm Tiềm Năng (Promising)",
            "desc": "Mới mua gần đây, giá trị đơn hàng trung bình.",
            "action": "Gửi voucher giảm giá để kích thích mua đơn tiếp theo."
        },
        3: {
            "name": "Khách Mới (New Customers)",
            "desc": "Vừa thực hiện giao dịch đầu tiên (R rất thấp, F thấp).",
            "action": "Gửi email cảm ơn, hướng dẫn sử dụng, xây dựng mối quan hệ."
        },
        4: {
            "name": "Cần Chăm Sóc (Need Attention)",
            "desc": "Có sức mua khá nhưng tần suất đang giảm dần.",
            "action": "Gợi ý các combo (Bundle) giá tốt để kéo họ quay lại."
        },
        5: {
            "name": "Nguy Cơ Rời Bỏ (At Risk)",
            "desc": "Đã từng mua nhiều nhưng rất lâu không quay lại (R cao).",
            "action": "CHIẾN DỊCH KHẨN CẤP: Giảm giá sâu, quà tặng miễn phí để kéo lại."
        },
        6: {
            "name": "Ngủ Đông (Lost/Hibernating)",
            "desc": "Lâu không mua, giá trị thấp, ít tương tác.",
            "action": "Giảm thiểu chi phí marketing, chỉ gửi tin tin khuyến mãi lớn dịp lễ."
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
                
                # 5.2 HIỂN THỊ LUẬT KẾT HỢP
                st.subheader(f"Top {top_n_rules} Quy luật nổi bật của Cụm {i}")
                
                if i in df_summary.index:
                    cluster_data = df_summary.loc[i]
                    rule_cols = [c for c in cluster_data.index if c.startswith('Rule_')]
                    
                    if rule_cols:
                        top_rules_idx = cluster_data[rule_cols].sort_values(ascending=False).head(top_n_rules)
                        
                        has_rule = False
                        for r_col, score in top_rules_idx.items():
                            if score > 0.0:
                                has_rule = True
                                idx = int(r_col.split('_')[1])
                                
                                if idx < len(df_rules):
                                    rule_info = df_rules.iloc[idx]
                                    
                                    # 1. Làm sạch tên sản phẩm
                                    ant = clean_rule_text(rule_info['antecedents'])
                                    con = clean_rule_text(rule_info['consequents'])
                                    
                                    # 2. Tính toán chỉ số để diễn giải
                                    conf_percent = rule_info.get('confidence', 0) * 100
                                    lift_val = rule_info['lift']
                                    
                                    # 3. Tạo câu "Thần chú Marketing" dựa trên số liệu
                                    marketing_text = ""
                                    if lift_val >= 3:
                                        marketing_text = "🔥 **Combo Siêu Kết Dính:** Hai món này gần như luôn được mua cùng nhau. Hãy đóng gói chung (Bundle) để bán ngay!"
                                    elif lift_val >= 1.5:
                                        marketing_text = "✅ **Cơ hội Cross-sell:** Khách mua món trước rất dễ bị thuyết phục mua món sau. Hãy gợi ý ngay tại quầy thu ngân."
                                    else:
                                        marketing_text = "💡 **Gợi ý phổ biến:** Đây là thói quen mua sắm thường thấy."

                                    # 4. HIỂN THỊ GIAO DIỆN (Đã cải tiến cho người dùng dễ hiểu)
                                    with st.expander(f"📌 Gợi ý #{idx} (Độ phổ biến: {score*100:.1f}%)"):
                                        
                                        # Hiện câu thần chú marketing
                                        st.info(marketing_text)
                                        
                                        # Hiện luồng hành vi dạng mũi tên trực quan
                                        c1, c2, c3 = st.columns([4, 1, 4])
                                        with c1:
                                            st.markdown("**Khi khách chọn mua:**")
                                            st.markdown(f"<div style='background-color:#e8f5e9; padding:10px; border-radius:5px; color:#1b5e20'>🛒 {ant}</div>", unsafe_allow_html=True)
                                        with c2:
                                            st.markdown("<h2 style='text-align:center; color:#999'>➡</h2>", unsafe_allow_html=True)
                                        with c3:
                                            st.markdown("**Hãy mời chào họ thêm:**")
                                            st.markdown(f"<div style='background-color:#ffebee; padding:10px; border-radius:5px; color:#b71c1c'>🎁 {con}</div>", unsafe_allow_html=True)
                                        
                                        st.divider()
                                        
                                        # Giải thích các con số kỹ thuật bằng ngôn ngữ người thường
                                        st.markdown(f"""
                                        **Tại sao nên tin luật này?**
                                        - 🎯 **Khả năng thành công ({conf_percent:.1f}%):** Cứ 100 người mua món đầu tiên, thì có khoảng **{int(conf_percent)} người** sẽ đồng ý mua món thứ hai.
                                        - 🔗 **Sức mạnh liên kết (Lift {lift_val:.2f}):** Việc mua kèm này mạnh gấp **{lift_val:.1f} lần** so với mua ngẫu nhiên.
                                        """)
                        
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