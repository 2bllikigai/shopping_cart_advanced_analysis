# BÁO CÁO KỸ THUẬT: MARKET BASKET ANALYSIS
**Chủ đề:** Khai phá luật kết hợp trên dữ liệu Online Retail
**Vai trò:** Leader (Phụ trách Kỹ thuật & Tối ưu thuật toán)

---

## 1. Tối ưu hóa thuật toán (Technical Optimization)
Trong quá trình triển khai thuật toán Apriori trên bộ dữ liệu lớn (~500.000 dòng giao dịch), nhóm đã gặp thách thức về tài nguyên phần cứng.

* **Vấn đề:** Gặp lỗi `MemoryError: Unable to allocate 11.2 GiB` khi chạy ở mức Support thấp (< 0.03).
* **Nguyên nhân:** Thư viện `mlxtend` mặc định tạo ma trận tính toán khổng lồ, vượt quá dung lượng RAM của máy tính cá nhân.
* **Giải pháp (Critical Fix):**
    * Can thiệp vào mã nguồn thư viện `src/apriori_library.py`.
    * Kích hoạt tham số `low_memory=True` trong hàm `apriori()`.
    * **Kết quả:** Giảm tải bộ nhớ, giúp thuật toán chạy mượt mà ngay cả ở mức Support 0.02 mà không cần nâng cấp phần cứng.

---

## 2. Thử nghiệm tham số (Experimentation)
Chúng tôi đã tiến hành so sánh kết quả giữa hai mức `min_support` là **0.02** và **0.03** để tìm ra cấu hình tối ưu nhất cho báo cáo kinh doanh.

### Kịch bản 1: Min Support = 0.02
* **Mô tả:** Chấp nhận các sản phẩm xuất hiện trong ít nhất 2% số giao dịch.
* **Kết quả:** Sinh ra số lượng luật rất lớn.
* **Hình ảnh mạng lưới (Network Graph):** Các đường liên kết dày đặc, khá rối rắm, khó nhìn ra các cụm chính ngay lập tức.
* **Đánh giá:** Phù hợp để khai thác sâu (Deep Mining) nhưng khó để trình bày tổng quan cho bộ phận kinh doanh.

### Kịch bản 2: Min Support = 0.03 (ĐƯỢC CHỌN)
* **Mô tả:** Nâng ngưỡng lọc lên 3%.
* **Kết quả:** Số lượng luật giảm đi nhưng chất lượng tăng lên (High Confidence & High Lift).
* **Hình ảnh mạng lưới (Network Graph):** (Xem file `images/sup0.03_network.png`)
    * Biểu đồ thoáng, hiện rõ các **Cụm sản phẩm (Product Clusters)** riêng biệt.
    * Phát hiện rõ cụm "Túi Lunch Bag", cụm "Tách trà" và cụm "Túi Jumbo".
* **Đánh giá:** Đây là mức cân bằng (Trade-off) tốt nhất giữa độ phủ và độ rõ ràng của thông tin.

---

## 3. Cấu hình chốt (Final Configuration)
Dựa trên thử nghiệm trên, nhóm thống nhất sử dụng bộ tham số sau cho toàn bộ báo cáo phân tích:

| Tham số | Giá trị | Giải thích |
| :--- | :--- | :--- |
| **Min Support** | **0.03** | Ngưỡng tối ưu đã chọn. |
| **Metric** | **Lift** | Đánh giá sức mạnh liên kết thực sự. |
| **Min Threshold** | **1.0** | Chỉ lấy các luật có tương quan dương (>1). |
| **Top Rules** | **20** | Lấy 20 luật mạnh nhất để trực quan hóa. |

---

## 4. Hướng dẫn cho thành viên (Next Steps)
* **@Thành viên Phân tích:** Dựa vào file `notebooks/apriori_modelling.ipynb` (đã chạy mức 0.03) để lấy danh sách các cặp sản phẩm có Lift cao nhất.
* **@Thành viên Viết bài:** Sử dụng hình ảnh Network Graph mức 0.03 để minh họa cho bài Blog, tập trung vào câu chuyện "Tại sao khách mua túi màu hồng lại mua thêm túi màu đỏ?".