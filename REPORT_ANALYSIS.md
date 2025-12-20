# BÁO CÁO PHÂN TÍCH & CHIẾN LƯỢC KINH DOANH
**Người thực hiện:** Võ Minh Quân (được hỗ trợ số liệu bởi Leader)
**Dữ liệu:** Kết quả thuật toán Apriori (Min Support 0.03)

---

## 1. Bằng chứng số liệu (Data Evidence)

Chúng tôi đã thực hiện khai phá dữ liệu giao dịch và trích xuất các luật kết hợp (Association Rules). Dưới đây là hình ảnh thực tế từ hệ thống phân tích:

### a. Top các luật có sức hút mạnh nhất (Theo Lift)
*Những cặp sản phẩm này kích thích nhau mua sắm mãnh liệt nhất (Khách mua A thì khao khát mua B).*

![Top 5 Lift Rules](../images/top5_lifts_rules.png)

### b. Top các luật có độ tin cậy cao nhất (Theo Confidence)
*Nếu khách đã bỏ món A vào giỏ, thì bao nhiêu % chắc chắn họ sẽ lấy tiếp món B?*

![Top 5 Confidence Rules](../images/top5_confidence_rules.png)

---

## 2. Phân tích chuyên sâu (Deep Dive Insights)

Từ bảng số liệu trên, chúng ta nhận thấy những hành vi mua sắm thú vị của khách hàng Anh Quốc:

### a. Hiệu ứng "Bộ sưu tập" (The Collector Effect)
* **Dữ liệu:** Cặp sản phẩm *Pink Regency Teacup* và *Green Regency Teacup* có chỉ số **Lift lên tới 15.8**.
* **Ý nghĩa:** Đây là con số cực kỳ cao, cho thấy hai sản phẩm này gần như không bao giờ được mua tách rời. Khách hàng không mua tách trà chỉ để uống, họ mua để **trưng bày và sưu tập**.
* **Hành vi:** Khách hàng có xu hướng mua trọn bộ các màu (Hồng, Xanh, Hoa hồng) để tạo sự đồng bộ cho bàn tiệc trà (Tea Party).

### b. Dự báo nhu cầu chắc chắn (High Confidence)
* **Dữ liệu:** Luật *Pink Regency Teacup -> Green Regency Teacup* có độ tin cậy (**Confidence**) là **82%**.
* **Ý nghĩa:** Cứ 10 khách hàng cầm chiếc tách màu Hồng lên, thì hệ thống dự báo chính xác 8 người sẽ tìm mua chiếc tách màu Xanh.
* **Cảnh báo:** Nếu cửa hàng chỉ còn tách Hồng mà hết tách Xanh, chúng ta đang đứng trước nguy cơ mất 82% doanh thu tiềm năng của lượt khách đó.

---

## 3. Đề xuất chiến lược kinh doanh (Action Plan)

Dựa trên các Insight trên, nhóm đề xuất kế hoạch hành động cụ thể:

### Chiến lược 1: Đóng gói Combo (Smart Bundling) - Tăng giá trị đơn hàng
Thay vì bán lẻ từng chiếc, hãy tạo ra các gói sản phẩm định sẵn để kích thích mua sắm trọn gói.

* **Tên gói:** *"Royal Tea Party Collection"* (Bộ sưu tập Trà chiều Hoàng gia).
* **Thành phần:** 1 Tách Hồng + 1 Tách Xanh + 1 Tách Họa tiết Hoa Hồng.
* **Giá bán:** Giảm **10%** so với mua lẻ từng chiếc.
* **Mục tiêu:** Tận dụng chỉ số Lift cao để bán chéo các màu ít phổ biến hơn (nếu có), giúp xả hàng tồn kho nhanh chóng.

### Chiến lược 2: Tối ưu hóa trưng bày (Store & Web Layout)
Tuyệt đối không để các sản phẩm có mối liên kết mạnh ở xa nhau.

* **Trên Website:**
    * Cài đặt thuật toán Cross-sell: Khi khách xem *Pink Teacup*, hiển thị ngay thông báo: *"82% khách hàng đã mua thêm Green Teacup cùng sản phẩm này"*.
    * Thêm nút **"Add Bundle to Cart"** (Thêm cả bộ vào giỏ) ngay dưới nút mua hàng.

* **Tại kho hàng & Cửa hàng:**
    * **Sắp xếp kệ:** Đặt xen kẽ Tách Hồng và Tách Xanh cạnh nhau. Hiệu ứng thị giác mạnh sẽ kích thích khách hàng cầm cả hai.
    * **Quản lý tồn kho:** Dựa vào Confidence 82%, bộ phận kho vận cần nhập hàng theo tỷ lệ tương ứng (1:1 hoặc 1:0.8) để tránh tình trạng "lệch pha" hàng hóa (thừa màu này nhưng thiếu màu kia).

---

## 4. Kết luận
Dữ liệu từ thuật toán Apriori đã chứng minh rằng khách hàng của chúng ta có tư duy mua sắm theo **"Hệ sinh thái"** (mua theo bộ/combo). Việc chuyển đổi từ tư duy bán lẻ từng món (Product-centric) sang tư duy bán theo cụm nhu cầu (Customer-centric) sẽ là chìa khóa để tăng trưởng doanh thu bền vững.