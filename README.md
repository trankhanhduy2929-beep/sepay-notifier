# **SePay Notifier cho Home Assistant**

Tích hợp thông báo giao dịch ngân hàng từ SePay.vn vào Home Assistant. Tự động cập nhật số dư, số tiền giao dịch và thông báo qua loa (TTS) một cách chuyên nghiệp.

## **1\. Giới thiệu**

Component này giúp bạn nhận dữ liệu biến động số dư từ SePay. Dữ liệu được tách bạch thành các thực thể (entities) riêng lẻ để bạn dễ dàng quản lý và hiển thị trên Dashboard.

## **2\. Tính năng nổi bật**

* **7 thực thể riêng biệt:** Số tiền, Nội dung, STK, Thời gian, Loại giao dịch, Ngân hàng, Số dư.  
* **Thông báo TTS (Edge TTS):** Tự động đọc số tiền nhận được qua loa (bảo mật: không đọc nội dung).  
* **Giao diện cấu hình UI:** Thiết lập và thay đổi tùy chọn (Configure) trực tiếp trên giao diện HA mà không cần khởi động lại hoặc cài lại.  
* **Tương thích cao:** Hỗ trợ mọi ngân hàng mà SePay cung cấp.

## **3\. Hướng dẫn cài đặt**

### **Bước 1: Cài qua Hacs

Điền link vào kho lưu trữ tùy chỉnh https://github.com/trankhanhduy2929-beep/sepay-notifier 

### **Bước 2: Khởi động lại Home Assistant**

Vào **Settings** \-\> **System** \-\> **YAML** \-\> **Check Configuration**. Nếu không có lỗi, hãy nhấn **Restart**.

### **Bước 3: Thêm Integration vào UI**

1. Vào **Settings** \-\> **Devices & Services**.  
2. Nhấn **Add Integration**.  
3. Tìm kiếm **SePay Notifier**.  
4. Nhập các thông tin:  
   * **Webhook ID:** Đặt một cái tên duy nhất (ví dụ: chuyen\_tien\_nha\_toi).  
   * **TTS Entity:** Chọn thực thể TTS bạn đang dùng (mặc định tts.edge\_tts\_2).  
   * **Media Player:** Chọn loa muốn phát thông báo.  
   * **Voice/Rate/Volume:** Tùy chỉnh giọng nói theo ý muốn.

## **5\. Cấu hình trên Dashboard SePay.vn**

1. Đăng nhập vào [SePay.vn](https://sepay.vn).  
2. Vào mục **Cấu hình Webhook** (hoặc Tích hợp hệ thống).  
3. Tạo Webhook mới với URL có cấu dạng:  
   https://\<DOMAIN\_CỦA\_BẠN\>/api/webhook/\<WEBHOOK\_ID\_BẠN\_ĐÃ\_ĐẶT\>  
   Ví dụ: https://myhome.duckdns.org/api/webhook/chuyen\_tien\_nha\_toi  
4. Chọn phương thức: POST và Content-Type: application/json.

## **6\. Danh sách các thực thể (Entities)**

Sau khi cài đặt thành công, Integration sẽ tạo ra 1 Thiết bị (Device) chứa 7 thực thể:

* sensor.sepay\_amount: Số tiền của giao dịch gần nhất.  
* sensor.sepay\_content: Nội dung chuyển khoản.  
* sensor.sepay\_account: Số tài khoản nhận tiền.  
* sensor.sepay\_time: Thời gian giao dịch (giờ ngân hàng).  
* sensor.sepay\_type: Tiền vào / Tiền ra.  
* sensor.sepay\_bank: Tên ngân hàng nhận.  
* sensor.sepay\_balance: Số dư tài khoản sau giao dịch.

## **7\. Cách thay đổi cấu hình (Configure)**

Bạn không cần xóa cài lại nếu muốn đổi loa hay đổi giọng nói:

1. Vào **Settings** \-\> **Devices & Services**.  
2. Tìm thẻ **SePay Notifier**.  
3. Nhấn vào nút **CONFIGURE** (Cấu hình).  
4. Thay đổi thông số và nhấn **Submit**. Các thay đổi sẽ có hiệu lực ngay lập tức cho lần giao dịch tới.

## **8\. Xử lý sự cố (Troubleshooting)**

* **Không thấy thực thể:** Kiểm tra lại file sensor.py đã có trong thư mục chưa và đã Restart HA chưa.  
* **Loa không báo:** Đảm bảo thực thể loa (media\_player) đang ở trạng thái idle hoặc playing và âm lượng không bị tắt. Kiểm tra Log trong HA để xem có lỗi dịch vụ tts.speak không.  
* **Webhook không hoạt động:** Kiểm tra URL Webhook xem đã chính xác chưa, và Home Assistant của bạn có đang mở port ra internet (hoặc dùng Nabu Casa/DuckDNS) để SePay có thể gửi dữ liệu về không.

*Tài liệu hướng dẫn được tạo dựa trên phiên bản v1.6.0 của SePay Custom Component.*
