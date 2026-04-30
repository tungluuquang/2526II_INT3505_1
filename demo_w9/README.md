Chiến lược nâng cấp API Thanh toán từ v1 lên v2
1. Giới thiệu

Tài liệu này trình bày kế hoạch chi tiết về việc chuyển đổi hệ thống Payment API từ phiên bản v1 (Legacy) sang phiên bản v2 (Standardized). Mục tiêu của việc nâng cấp là cải thiện tính toàn vẹn dữ liệu, tuân thủ các tiêu chuẩn thanh toán quốc tế và tối ưu hóa khả năng mở rộng của hệ thống.
2. Phân tích sự khác biệt giữa v1 và v2
2.1. API v1 (Lỗi thời)

    Endpoint: /v1/payments

    Vấn đề kỹ thuật:

        Trường amount được định nghĩa kiểu dữ liệu String, gây khó khăn cho việc kiểm thử (validation) và tính toán số học tại backend.

        Dữ liệu bị nhập nhằng: Giá trị số và đơn vị tiền tệ bị gộp chung (ví dụ: "100000VND"), vi phạm nguyên tắc tách biệt dữ liệu.

        Thiếu tính chuẩn hóa: Không tuân theo các chuẩn quốc tế về tài chính.

    Hệ quả:

        Tăng độ phức tạp của logic xử lý chuỗi (parsing) tại backend.

        Rủi ro sai sót dữ liệu cao khi có các định dạng tiền tệ khác nhau.

        Khó khăn khi tích hợp với các cổng thanh toán quốc tế hoặc đối tác bên thứ ba.

2.2. API v2 (Cải tiến)

    Endpoint: /v2/payments

    Cải tiến kỹ thuật:

        amount: Chuyển sang kiểu dữ liệu Integer (đơn vị nhỏ nhất của tiền tệ) để tránh lỗi làm tròn số thập phân.

        currency: Tách riêng thành một trường độc lập, tuân thủ tiêu chuẩn ISO 4217.

        schema: Định nghĩa rõ ràng các trường bắt buộc (required fields) bằng JSON Schema.

    Cấu trúc dữ liệu mẫu:
    JSON

    {
      "transactionId": "TXN-12345",
      "amount": 100000,
      "currency": "VND",
      "userId": "USR-001"
    }

    Lợi ích:

        Tự động hóa việc validate dữ liệu tại tầng API Gateway hoặc Controller.

        Tương thích hoàn toàn với các hệ thống tài chính lớn như Stripe, PayPal.

        Hỗ trợ đa tiền tệ một cách linh hoạt.

3. Chiến lược quản lý phiên bản (Versioning Strategy)
3.1. URI Versioning

Sử dụng tiền tố phiên bản trực tiếp trong URL để phân tách logic xử lý.

    v1: /v1/payments

    v2: /v2/payments

Phương pháp này đảm bảo tính tường minh, không gây gián đoạn cho các client cũ và cho phép duy trì song song hai nền tảng trong giai đoạn chuyển đổi.
3.2. Lộ trình triển khai song song

Hệ thống sẽ duy trì v1 cho đến khi toàn bộ các client quan trọng hoàn tất việc di chuyển dữ liệu.
Giai đoạn	Mô tả hoạt động
Giai đoạn 1	Phát hành v2 chính thức và duy trì hoạt động của v1.
Giai đoạn 2	Đánh dấu v1 là Deprecated trong tài liệu kỹ thuật và phản hồi API.
Giai đoạn 3	Ngừng hỗ trợ hoàn toàn v1 (Dự kiến: 31/12/2026).
3.3. Kỹ thuật đánh dấu lỗi thời (Deprecation Strategy)

    Trong OpenAPI/Swagger: Cấu hình thuộc tính deprecated: true cho tất cả các endpoint thuộc v1.

    Cảnh báo trong tài liệu: Đưa ra thông báo chính thức về thời hạn ngừng hoạt động của v1.

4. Thông báo cho đội ngũ phát triển (Developers)
4.1. Nội dung thông báo chính thức

Tiêu đề: Thông báo ngừng hỗ trợ Payment API v1

Chúng tôi chính thức thông báo rằng endpoint /v1/payments đã được đánh dấu là lỗi thời (deprecated) và sẽ ngừng hoạt động vào ngày 31/12/2026.

Lý do nâng cấp:

    Chuẩn hóa định dạng dữ liệu theo tiêu chuẩn tài chính ISO 4217.

    Tách biệt tường minh giá trị giao dịch và đơn vị tiền tệ.

    Nâng cao khả năng kiểm soát dữ liệu đầu vào và tính bảo mật.

Yêu cầu hành động:

    Thực hiện chuyển đổi các lời gọi API sang endpoint mới: /v2/payments.

    Cập nhật cấu trúc payload theo định dạng v2.

    Hoàn tất việc migration trước ngày 01/12/2026 để đảm bảo ổn định dịch vụ.

Mọi yêu cầu hỗ trợ kỹ thuật vui lòng liên hệ qua kênh hỗ trợ của team Backend.
4.2. Các kênh truyền thông

    Cập nhật trực tiếp trên trang tài liệu Swagger/OpenAPI.

    Gửi email thông báo tới danh sách các tài khoản Developer đang sử dụng API.

    Ghi chú trong danh mục Release Notes của hệ thống.

    Bổ sung HTTP Header vào phản hồi của v1 (Tùy chọn):

        Deprecation: true

        Sunset: 2026-12-31

5. Chiến lược chuyển đổi dữ liệu (Migration Strategy)
5.1. Quy tắc ánh xạ dữ liệu

Dữ liệu từ v1 sẽ được chuẩn hóa sang v2 theo quy tắc sau:

    v1: "100000VND" (String)

    v2: amount: 100000 (Integer) và currency: "VND" (String ISO)

5.2. Các bước thực hiện

    Rà soát toàn bộ các module mã nguồn đang gọi tới v1.

    Tái cấu trúc lại logic tạo payload tại phía client.

    Thay đổi endpoint sang v2.

    Thực hiện kiểm thử tích hợp (End-to-End) trên môi trường Staging.

    Triển khai thực tế và giám sát lưu lượng qua v2.

5.3. Khả năng tương thích ngược (Tùy chọn)

Để hỗ trợ các client chưa thể nâng cấp ngay lập tức, có thể triển khai một lớp Adapter trung gian tại backend:
JavaScript

/**
 * Chuyển đổi dữ liệu từ định dạng v1 sang v2
 * @param {Object} data - Payload định dạng v1
 * @returns {Object} - Payload định dạng v2
 */
function convertV1ToV2(data) {
  const match = data.amount.match(/(\d+)([A-Z]+)/);
  if (!match) throw new Error("Invalid v1 amount format");
  
  return {
    transactionId: data.transactionId,
    amount: parseInt(match[1], 10),
    currency: match[2],
    userId: data.userId
  };
}