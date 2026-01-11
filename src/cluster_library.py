import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

class RuleBasedCustomerClusterer:
    def __init__(self):
        self.rules = None
        self.customer_features = None
        self.model = None
        self.labels = None
        self.kmeans_kwargs = {
            "init": "random",
            "n_init": 10,
            "max_iter": 300,
            "random_state": 42,
        }

    def load_top_rules(self, rules_df, top_k=30, metric='lift'):
        """
        Lọc top-K luật mạnh nhất để làm feature.
        """
        # Sắp xếp và lấy top K
        self.rules = rules_df.sort_values(by=metric, ascending=False).head(top_k).reset_index(drop=True)
        
        # Xử lý chuỗi antecedents thành set (vì lưu trong CSV nó là chuỗi ký tự)
        # Ví dụ: "{'A', 'B'}" -> set(['A', 'B'])
        if isinstance(self.rules['antecedents'].iloc[0], str):
             self.rules['antecedents'] = self.rules['antecedents'].apply(lambda x: eval(x))
             
        print(f"✅ Đã load {len(self.rules)} luật dựa trên {metric} cao nhất.")
        return self.rules

    def build_customer_feature_matrix(self, transactions_df, customer_col='CustomerID', item_col='StockCode'):
        """
        Tạo ma trận Customer x Rules (Biến thể 1: Binary - Thỏa luật hay không)
        """
        print("⏳ Đang tạo đặc trưng từ luật cho từng khách hàng (bước này tốn chút thời gian)...")
        
        # 1. Gom giỏ hàng của từng khách: {Khách A: {'Món 1', 'Món 2'...}}
        # Đảm bảo item_col là string để khớp với antecedents trong rules
        transactions_df[item_col] = transactions_df[item_col].astype(str)
        customer_baskets = transactions_df.groupby(customer_col)[item_col].apply(set)
        customer_ids = customer_baskets.index.tolist()
        
        # 2. Tạo ma trận
        # Hàng = Khách hàng, Cột = Rule_0, Rule_1...
        # Giá trị = 1 nếu khách mua đủ bộ antecedents của luật đó, 0 nếu không.
        
        matrix_data = []
        
        for cid in customer_ids:
            basket = customer_baskets[cid]
            row_features = {}
            
            for idx, rule in self.rules.iterrows():
                antecedents = rule['antecedents'] 
                
                # Kiểm tra xem khách có mua trọn vẹn vế trái của luật không
                if antecedents.issubset(basket):
                    row_features[f'Rule_{idx}'] = 1 
                else:
                    row_features[f'Rule_{idx}'] = 0
            
            matrix_data.append(row_features)
            
        self.customer_features = pd.DataFrame(matrix_data, index=customer_ids)
        print(f"✅ Đã tạo xong vector đặc trưng. Shape: {self.customer_features.shape}")
        return self.customer_features

    def add_rfm_features(self, rfm_df, weight=1.0):
        """
        Biến thể 2 (Nâng cao): Ghép thêm RFM vào
        rfm_df phải có index là CustomerID
        """
        print("⏳ Đang ghép dữ liệu RFM...")
        # Scale RFM về 0-1 để tương đồng với Rule features (vốn là 0-1)
        scaler = MinMaxScaler()
        rfm_scaled = pd.DataFrame(
            scaler.fit_transform(rfm_df), 
            index=rfm_df.index, 
            columns=rfm_df.columns
        )
        
        # Nhân trọng số (nếu muốn RFM ảnh hưởng nhiều hơn Rules)
        rfm_scaled = rfm_scaled * weight
        
        # Join với bảng feature hiện tại (Inner join để khớp ID)
        self.customer_features = self.customer_features.join(rfm_scaled, how='inner').fillna(0)
        print(f"✅ Đã ghép thêm RFM. Shape mới: {self.customer_features.shape}")

    def choose_k_elbow_silhouette(self, k_range=range(2, 10)):
        """
        Tìm K tối ưu và vẽ biểu đồ Elbow + Silhouette
        """
        silhouette_coefficients = []
        sse = [] # Sum of squared errors (Elbow)

        print(f"⏳ Đang chạy thử nghiệm K từ {k_range.start} đến {k_range.stop - 1}...")

        for k in k_range:
            kmeans = KMeans(n_clusters=k, **self.kmeans_kwargs)
            kmeans.fit(self.customer_features)
            sse.append(kmeans.inertia_)
            score = silhouette_score(self.customer_features, kmeans.labels_)
            silhouette_coefficients.append(score)
            print(f"   K={k} -> Silhouette={score:.4f}")

        # Vẽ 2 biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Elbow
        ax1.plot(k_range, sse, 'bx-')
        ax1.set_xlabel('k')
        ax1.set_ylabel('Inertia (SSE)')
        ax1.set_title('Phương pháp Elbow (Tìm điểm gập)')
        
        # Silhouette
        ax2.plot(k_range, silhouette_coefficients, 'ro-')
        ax2.set_xlabel('k')
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Phương pháp Silhouette (Càng cao càng tốt)')
        
        plt.show()

    def run_clustering(self, k):
        """
        Chạy model với K đã chốt
        """
        self.model = KMeans(n_clusters=k, **self.kmeans_kwargs)
        self.labels = self.model.fit_predict(self.customer_features)
        
        # Lưu kết quả
        self.results = self.customer_features.copy()
        self.results['Cluster'] = self.labels
        return self.results

    def visualize_2d(self):
        """
        Giảm chiều PCA để vẽ biểu đồ phân tán 2D
        """
        pca = PCA(n_components=2)
        # Lấy features (trừ cột Cluster vừa tạo)
        features_only = self.results.drop(columns=['Cluster'])
        components = pca.fit_transform(features_only)
        
        plt.figure(figsize=(10, 7))
        sns.scatterplot(
            x=components[:,0], y=components[:,1], 
            hue=self.results['Cluster'], 
            palette="viridis", s=80, alpha=0.8
        )
        plt.title("Phân cụm khách hàng (PCA Projection)")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend(title='Cluster')
        plt.show()
        
    def profile_clusters(self):
        """
        Hàm báo cáo thống kê trung bình của từng cụm
        """
        return self.results.groupby('Cluster').mean()