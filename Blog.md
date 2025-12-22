# [BLOG] BÍ MẬT TRONG GIỎ HÀNG: CÁCH CHÚNG TÔI DÙNG PYTHON ĐỂ "BẮT BÀI" TÂM LÝ NGƯỜI MUA SẮM

**Tác giả:** Nhóm Data Mining - [Tên lớp/Khóa học]
**Team:** Kiều Quang Trường (Leader), Võ Minh Quân, Tô Vi Đức

---

### 1. Mở đầu: Không chỉ là chuyện "Bia và Tã lót"

Bạn đã bao giờ tự hỏi: Tại sao trong siêu thị, kẹo cao su lại đặt cạnh quầy thu ngân? Tại sao trên Shopee, khi bạn mua một chiếc váy, hệ thống lại gợi ý một đôi giày "hợp rơ" đến lạ lùng?

Đó không phải là ngẫu nhiên. Đó là quyền năng của **Market Basket Analysis (Phân tích giỏ hàng)**.

Trong dự án kết thúc môn học lần này, nhóm chúng tôi đã thử sức "đào sâu" vào bộ dữ liệu **Online Retail** (với hơn 500.000 giao dịch thực tế tại Anh Quốc) để tìm ra câu trả lời cho câu hỏi: *"Khách hàng thực sự muốn mua những gì cùng nhau?"*

### 2. Thử thách kỹ thuật: Khi dữ liệu lớn làm "tràn bộ nhớ"

Hành trình nào cũng có chông gai. Ngay khi bắt tay vào chạy thuật toán **Apriori** (một thuật toán kinh điển để tìm luật kết hợp), team chúng tôi đã va phải một bức tường lớn: **MemoryError**.

Với lượng dữ liệu khổng lồ, việc tạo ra ma trận tính toán đã ngốn sạch 11GB RAM và khiến máy tính "đình công".

Tuy nhiên, dưới sự dẫn dắt kỹ thuật của **Leader Kiều Quang Trường**, nhóm đã tìm ra giải pháp tối ưu:
* Can thiệp trực tiếp vào mã nguồn thư viện để kích hoạt chế độ **`low_memory`**.
* Tinh chỉnh lại các kiểu dữ liệu để tiết kiệm tài nguyên.
* **Kết quả:** Thuật toán chạy mượt mà, cho phép chúng tôi thử nghiệm ở các mức *Support* thấp (0.02 - 0.03) để không bỏ sót các "viên ngọc quý" (hidden gems) trong dữ liệu.

### 3. Bức tranh toàn cảnh: Mạng lưới mua sắm

Sau khi thuật toán chạy xong, điều thú vị nhất đã hiện ra. Thay vì những con số khô khan, chúng tôi đã mô hình hóa các luật kết hợp thành một **Mạng lưới (Network Graph)**.

![Network Graph](/images/lab1/sup_03_network.png)
*(Hình 1: Mạng lưới liên kết giữa các sản phẩm tại mức Support 0.03)*

Nhìn vào biểu đồ trên, bạn có thể thấy rõ các **"Cụm sản phẩm" (Product Clusters)** tách biệt nhau:
1.  **Cụm "Tiệc trà Anh Quốc" (The Tea Party):** Nơi hội tụ của các bộ tách trà *Regency Teacup* đủ màu sắc.
2.  **Cụm "Túi cơm văn phòng" (Lunch Bags):** Các loại túi đựng cơm với họa tiết khác nhau nhưng luôn đi cùng nhau.
3.  **Cụm "Túi Jumbo":** Những chiếc túi khổng lồ đựng đồ gia đình.

### 4. Insight đắt giá: "Sự cám dỗ" mang tên Lift và Confidence
Dựa vào số liệu, bạn **Võ Minh Quân (Analyst)** đã tìm ra 2 loại quy luật mua sắm thú vị:

#### a. Hiệu ứng "Bộ sưu tập" (Dựa trên chỉ số Lift cao kỷ lục)

![Top Lift Rules](/images/lab1/top_5_lifts_rules.png)
*(Hình 2: Các luật có chỉ số Lift cao nhất)*

Chúng tôi phát hiện ra cặp sản phẩm: **Pink Regency Teacup** (Tách hồng) và **Green Regency Teacup** (Tách xanh).
* **Lift = 15.8:** Nghĩa là việc khách mua Tách Hồng sẽ "kích thích" khả năng mua Tách Xanh tăng gấp **15.8 lần** so với bình thường.
* **Giải mã:** Khách hàng mua dòng sản phẩm này không phải chỉ để dùng, mà là để **sưu tầm**. Họ muốn bàn tiệc của mình rực rỡ và đồng bộ (Mix & Match).

#### b. Hiệu ứng "Dự báo chắc chắn" (Dựa trên Confidence > 80%)

![Top Confidence Rules](/images/lab1/top_5_confidence_rules.png)
*(Hình 3: Các luật có độ tin cậy cao nhất)*

Dữ liệu chỉ ra rằng: Nếu khách đã bỏ *Pink Teacup* vào giỏ, thì **82%** chắc chắn họ sẽ tìm mua *Green Teacup*. Đây là một con số biết nói để bộ phận kho vận chuẩn bị hàng hóa, tránh tình trạng "lệch pha" (thừa màu này thiếu màu kia).

### 5. Từ Dữ liệu đến Chiến lược kinh doanh

Không để dữ liệu nằm trên giấy, nhóm đề xuất 3 chiến lược hành động ngay lập tức (Actionable Insights):

1.  **Chiến lược "Royal Bundle" (Bán Combo):**
    * Thay vì bán lẻ từng chiếc tách, hãy đóng gói bộ 3 màu (Hồng - Xanh - Hoa hồng) thành một set quà tặng.
    * **Lợi ích:** Tăng giá trị đơn hàng (AOV) và xả được hàng tồn của các màu ít phổ biến.

2.  **Chiến lược "Smart Layout" (Trưng bày thông minh):**
    * Tại cửa hàng: Tuyệt đối không xếp tách Hồng và tách Xanh ở hai kệ xa nhau. Hãy xếp xen kẽ để kích thích thị giác.
    * Trên Website: Cài đặt thuật toán *Recommendation*: "Khách mua cái này thường mua thêm..." ngay tại trang thanh toán.

3.  **Chiến lược "Cặp đôi hoàn hảo" cho Túi Lunch Bag:**
    * Với các sản phẩm túi đựng cơm, khách hàng thường mua mẫu *Red Retrospot* cùng với *Pink Polkadot*. Đây là gợi ý tuyệt vời cho các chương trình "Mua 1 tặng 1" hoặc "Giảm 20% cho chiếc thứ 2".

### 6. Kết luận

Dự án này đã chứng minh rằng: Dữ liệu không biết nói dối. Đằng sau hàng triệu dòng giao dịch lộn xộn là những quy luật tâm lý mua sắm cực kỳ chặt chẽ.

Việc ứng dụng Data Mining không chỉ giúp chúng ta hiểu khách hàng hơn, mà còn là chìa khóa để tối ưu hóa doanh thu và vận hành một cách thông minh nhất.

---
**Thành viên thực hiện:**
* 👨‍💻 **Kiều Quang Trường:** Kỹ thuật, Tối ưu thuật toán & Xử lý dữ liệu lớn.
* 📊 **Võ Minh Quân:** Phân tích dữ liệu, Insight & Chiến lược kinh doanh.
* ✍️ **Tô Vi Đức:** Trực quan hóa & Xây dựng nội dung Blog.

*Source code dự án: [[Link GitHub của nhóm](https://github.com/2bllikigai/shopping_cart_analysis)]*
