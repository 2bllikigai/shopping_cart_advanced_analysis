# BÁO CÁO KỸ THUẬT  
## TỐI ƯU HÓA & TRỰC QUAN HÓA NETWORK GRAPH  

**Dự án:** Market Basket Analysis – Lab 2  
**Leader phụ trách:** Trường *(Technical Optimization)*  

---

## 1. Phân tích cấu trúc thuật toán *(Question 1)*  

Trong khuôn khổ **Lab 2**, nhóm đã thực hiện nâng cấp pipeline xử lý từ thuật toán **Apriori** sang **FP-Growth** nhằm tối ưu hóa quá trình khai phá tri thức trên bộ dữ liệu bán lẻ quy mô lớn.

### 1.1. Cơ chế cải tiến  
- **Apriori:** Dựa trên cơ chế sinh tập ứng viên *(Candidate Generation)*, gây bùng nổ số lượng tập khi ngưỡng hỗ trợ thấp.  
- **FP-Growth:** Sử dụng cấu trúc **FP-Tree** để nén dữ liệu giao dịch, loại bỏ hoàn toàn bước sinh tập ứng viên.

### 1.2. Tối ưu hóa số lần quét dữ liệu  
- Thuật toán chỉ cần **02 lần quét CSDL**:
  1. Xác định các mục phổ biến (Frequent Items).
  2. Xây dựng cấu trúc **FP-Tree**.  
→ Giảm đáng kể chi phí **I/O** và sử dụng **bộ nhớ**.

### 1.3. Tính nhất quán và độ chính xác  
- Thực nghiệm đối chứng tại ngưỡng `min_support = 0.03` cho thấy:
  - **145 tập phổ biến**
  - **22 luật kết hợp**  
- Kết quả của **FP-Growth** hoàn toàn trùng khớp với **Apriori**, khẳng định **tính chính xác tuyệt đối** của mô hình mới.

---

## 2. So sánh hiệu năng & Độ nhạy tham số *(Question 2)*  

Nhóm tiến hành **Stress Test** bằng cách giảm dần ngưỡng hỗ trợ từ `0.05` xuống `0.01` để đánh giá phản ứng của hệ thống.

### 2.1. Giới hạn vật lý của Apriori *(MemoryError)*  
- Khi `min_support = 0.015` và `0.01`, thuật toán **Apriori hoàn toàn thất bại**.
- **Hiện tượng:**  
*(Minh chứng: image_5269ed.png)*

- **Nguyên nhân:**  
- Ngưỡng support thấp → số lượng tập ứng viên tăng theo **cấp số nhân**  
- Dẫn đến **Candidate Explosion**, vượt quá dung lượng RAM của máy tính cá nhân.

### 2.2. Khả năng mở rộng vượt trội của FP-Growth  
- Trong khi Apriori dừng hoạt động, **FP-Growth vẫn hoàn thành** khai phá tại `min_support = 0.01` chỉ trong **~35.8 giây**.

| Ngưỡng Support | Thời gian Apriori (s) | Thời gian FP-Growth (s) | Trạng thái |
|----------------|----------------------|-------------------------|------------|
| 0.05 | ~0.2 | ~2.5 | Hiệu năng tương đương |
| 0.03 | ~0.4 | ~3.1 | Mốc đối chứng thành công |
| 0.015 | FAILED | ~4.1 | Apriori lỗi MemoryError |
| 0.01 | FAILED | ~5.2 | Chỉ FP-Growth khả thi |

**Kết luận:**  
Biểu đồ thực nghiệm chứng minh **FP-Growth có khả năng mở rộng (Scalability) vượt trội**, cho phép khai phá các **mẫu hiếm (Rare Patterns)** ở ngưỡng hỗ trợ thấp.

---

## 3. Chủ đề 5: Phân tích bằng Network Graph có trọng số  

Nhóm đã nâng cấp trực quan hóa từ đồ thị đơn giản sang **Weighted Network Graph** nhằm làm nổi bật các mối quan hệ kinh doanh quan trọng.

### 3.1. Thiết lập trọng số kỹ thuật *(Weighted Logic)*  
- **Độ dày cạnh (Edge Thickness):**  
- Gán theo chỉ số **Lift**  
- Cạnh càng dày → mức độ mua kèm càng mạnh (không phải ngẫu nhiên)

- **Kích thước nút (Node Size):**  
- Đại diện cho chỉ số **Support**  
- Sản phẩm xuất hiện càng nhiều → nút càng lớn

- **Xử lý hiển thị:**  
- Tinh chỉnh tham số giãn cách nút `k = 3.0`  
- Khắc phục hiện tượng chồng chéo nhãn, nâng cao tính trực quan và chuyên nghiệp.

### 3.2. Insight từ đồ thị có trọng số  
- Phát hiện **mối liên kết cực mạnh** trong nhóm sản phẩm **"HERB MARKER"**.  
- Trọng số cạnh lớn cho thấy khách hàng có xu hướng:
- Mua **trọn bộ** (Rosemary, Basil, Thyme, …)  
- Thay vì mua lẻ từng sản phẩm

→ **Cơ hội kinh doanh:**  
Triển khai chiến lược **Bundling sản phẩm**, gia tăng giá trị đơn hàng và doanh thu.

---

## 4. Tổng kết kỹ thuật  

- Việc triển khai **FP-Growth**:
- Vượt qua giới hạn vật lý của RAM
- Khai phá hiệu quả các **mẫu đuôi dài (Long-tail Patterns)**

- Sự kết hợp giữa:
- Thuật toán dựa trên **cấu trúc cây**
- **Network Graph có trọng số**

→ Cung cấp cái nhìn sâu sắc về **cấu trúc liên kết sản phẩm**, những insight mà thuật toán **Apriori truyền thống không thể tiếp cận**.
