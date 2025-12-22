# BÁO CÁO PHÂN TÍCH INSIGHT KINH DOANH: CHIẾN LƯỢC TỐI ƯU HÓA BÁN LẺ
**Dự án:** Market Basket Analysis - Lab 2
**Người thực hiện:** Võ Minh Quân (Business Analyst)

---

## 1. Tổng quan kết quả khai thác
Dựa trên thuật toán FP-Growth, chúng tôi đã trích xuất thành công 22 luật kết hợp tại mức $min\_support = 0.03$. 
* **Chất lượng luật:** Đạt chỉ số Lift cực cao (lên đến 15.86), cho thấy các sản phẩm không được mua ngẫu nhiên mà theo nhu cầu hệ thống.

---

## 2. Phân tích cụm sản phẩm trọng tâm (Insights)

### 2.1. Cụm bộ sưu tập "Regency Teacup"
Dựa trên bảng dữ liệu trích xuất (Xem `images/lab2/top_5_lift_sup_03.png`):
* **Luật mạnh nhất:** Pink Regency Teacup -> Green Regency Teacup.
* **Chỉ số:** Confidence **82.05%**, Lift **15.86**.
* **Ý nghĩa:** Đây là nhóm khách hàng có gu thẩm mỹ cao, mua sắm theo bộ sưu tập màu sắc. Việc sở hữu một mẫu teacup dẫn đến nhu cầu hoàn thiện bộ sưu tập rất lớn.

### 2.2. Insight từ Đồ thị mạng lưới có trọng số (Weighted Graph)
Phân tích đồ thị `images/lab2/weighted_network_graph.png` (Xem `image_bef411.png`):
* **Cụm "Herb Marker":** Các nút như Rosemary, Basil, Thyme liên kết với nhau bằng các đường kẻ rất dày (Weight = Lift cao).
* **Hành vi:** Khách hàng làm vườn có xu hướng mua **trọn bộ** các nhãn đánh dấu loại cây cùng một lúc thay vì mua lẻ từng cái.

---

## 3. Đề xuất chiến lược (Action Plans)

1. **Chiến lược Bundling (Combo):** Đóng gói bộ "Herb Garden Starter" gồm 4-5 loại nhãn đánh dấu cây hoặc bộ "Trio Teacup" với giá ưu đãi hơn 12% so với mua lẻ.
2. **Sắp xếp kệ hàng:** Đặt các mẫu Herb Marker cạnh nhau theo nhóm thay vì chia theo thứ tự bảng chữ cái.
3. **Marketing:** Gửi thông báo "Hoàn thiện bộ sưu tập" cho khách đã mua 1 trong các mẫu Regency Teacup nhưng chưa mua đủ 3 màu.