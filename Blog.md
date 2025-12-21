# KHI APRIORI "GỤC NGÃ" VÀ SỰ TRỖI DẬY CỦA FP-GROWTH

**Tác giả:** Tô Vi Đức  
**Chủ đề:** Trải nghiệm thực nghiệm Lab 2 - Market Basket Analysis

---

## Lời nguyền mang tên MemoryError
Trong Lab 1, Apriori là "ông vua". Nhưng khi bước sang Lab 2, khi chúng tôi hạ $min\_support$ xuống 0.015, "ông vua" đã gục ngã. Hệ thống báo lỗi: `MemoryError: Unable to allocate 5.58 GiB` (Xem `image_5269ed.png`). 

Tại sao? Vì Apriori sinh ra quá nhiều tập ứng viên (Candidate Generation), khiến RAM máy tính cá nhân bị quá tải.

## FP-Growth: Người hùng cứu cánh
Chúng tôi chuyển sang **FP-Growth**. Thay vì tạo ra hàng triệu ứng viên, nó nén dữ liệu vào một cây **FP-Tree**.
* **Kết quả:** Trong khi Apriori thất bại, FP-Growth hoàn thành mức 0.01 chỉ trong **35.8 giây**! (Xem minh chứng tại `image_5269ed.png`).


## Sức mạnh của trực quan hóa (Weighted Network Graph)
Điểm "ăn tiền" nhất của Lab 2 là đồ thị mạng lưới có trọng số (Xem `image_bef411.png`). 
* **Độ dày của đường nối:** Đại diện cho chỉ số **Lift**.
* **Kích thước nút:** Đại diện cho **Support**.

Nhìn vào đồ thị `images/lab2/weighted_network_graph.png`, bạn sẽ thấy ngay các cụm sản phẩm liên kết chặt chẽ như Herb Markers. Những đường nối dày đặc chứng minh rằng khách hàng luôn mua chúng theo nhóm.


## Kết luận
Đừng cố dùng một cái búa cũ cho một tảng đá lớn. FP-Growth không chỉ là một thuật toán, nó là lời giải cho bài toán dữ liệu lớn mà nhóm chúng tôi đã chinh phục thành công trong Lab 2 này.

---
*Xem chi tiết báo cáo kỹ thuật tại REPORT_TECHNICAL.md*