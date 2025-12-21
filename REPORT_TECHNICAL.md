# BÁO CÁO KỸ THUẬT: SO SÁNH HIỆU NĂNG APRIORI VS FP-GROWTH
**Dự án:** Market Basket Analysis - Lab 2
**Leader phụ trách:** Trường (Technical & Optimization)

---

## 1. Phân tích cấu trúc thuật toán (Question 1)
Trong giai đoạn này, nhóm đã thực hiện chuyển đổi và so sánh giữa thuật toán Apriori (Lab 1) và **FP-Growth** (Lab 2).

* **Cơ chế cải tiến:** Khác với Apriori phải sinh các tập ứng viên (Candidate Generation), FP-Growth sử dụng cấu trúc dữ liệu nén gọi là **FP-Tree**. 
* **Tối ưu hóa:** Cấu trúc cây này giúp thuật toán chỉ cần quét cơ sở dữ liệu đúng **02 lần**, giảm thiểu đáng kể chi phí I/O.
* **Tính nhất quán:** Qua thực nghiệm (Xem file `image_5247aa.png`), tại cùng mức tham số, cả hai thuật toán đều cho ra **145 tập phổ biến** và **22 luật kết hợp** giống hệt nhau.



---

## 2. So sánh hiệu năng và Độ nhạy tham số (Question 2)
Nhóm đã tiến hành một bài kiểm tra áp lực (Stress Test) bằng cách giảm dần ngưỡng $min\_support$ từ 0.05 xuống 0.01.

### 2.1. Giới hạn vật lý của Apriori (MemoryError)
* **Hiện tượng:** Khi hạ $min\_support$ xuống mức **0.015** và **0.01**, thuật toán Apriori hoàn toàn thất bại (Xem file `image_5269ed.png`).
* **Chi tiết lỗi:** `MemoryError: Unable to allocate 5.58 GiB`.
* **Nguyên nhân:** Ở ngưỡng support thấp, Apriori gặp hiện tượng **"Bùng nổ tổ hợp"** (Candidate Explosion), sinh ra hơn 332,000 tập ứng viên khiến bộ nhớ RAM bị quá tải.

### 2.2. Ưu thế của FP-Growth (Scalability)
Trong khi Apriori dừng hoạt động, **FP-Growth** vẫn hoàn thành khai phá ở mức 0.01 chỉ trong vài giây (Xem file `image_5269ed.png`). 

| Ngưỡng Support | Apriori (s) | FP-Growth (s) | Kết quả |
| :--- | :--- | :--- | :--- |
| **0.05** | ~0.2 | ~2.5 | Hiệu năng tương đương. |
| **0.02** | ~0.56 | ~3.24 | Apriori bắt đầu chậm hơn (Xem `image_51f632.png`). |
| **0.015** | **FAILED** | ~4.1 | Apriori lỗi MemoryError. |
| **0.01** | **FAILED** | ~5.2 | Chỉ FP-Growth khả thi. |

**=> Kết luận:** Biểu đồ đường trong file `sensitivity_analysis_line.png` cho thấy đường thời gian của Apriori dốc đứng (nhạy cảm cao), trong khi FP-Growth đi ngang ổn định (độ nhạy thấp).



---

## 3. Kết quả khai phá tiêu biểu (Insights)
Dựa trên kết quả chạy thành công ở mức **Support = 0.03**, nhóm đã trích xuất được các luật có giá trị kinh doanh cao.

* **Chỉ số Lift:** Các luật mạnh nhất tập trung vào dòng sản phẩm "Regency Teacup" với chỉ số Lift vượt mốc 15.0 (Xem file `image_52cf32.jpg`).
* **Trực quan hóa:** File `network_graph_sup_03.png` hiển thị rõ các cụm sản phẩm liên kết chặt chẽ, hỗ trợ việc thiết kế combo bán hàng.

---

## 4. Tổng kết & Phân công
* **Leader (Trường):** Đã hoàn thành pipeline so sánh và xử lý lỗi bộ nhớ bằng cách điều phối sang FP-Growth.
* **Analyst (Quân):** Cần lấy danh sách 22 luật từ mức 0.03 để giải thích ý nghĩa kinh doanh.
* **Blogger (Đức):** Sử dụng ảnh `sensitivity_analysis_line.png` và thông báo lỗi `MemoryError` để viết bài blog về sự vượt trội của giải pháp Tree-based.

---