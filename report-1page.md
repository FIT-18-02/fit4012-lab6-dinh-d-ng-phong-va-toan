# Report 1 page - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Đinh Dương Phong
- Thành viên 2: Trần Đinh Đức Toàn

## Mục tiêu

Mục tiêu chính của bài Lab này là xây dựng hệ thống truyền nhận dữ liệu an toàn thông qua TCP Socket sử dụng thuật toán mã hóa AES-CBC. Sinh viên cần làm quen với việc tách biệt luồng dữ liệu thành hai kênh: kênh khóa (Key channel) để trao đổi AES Key/IV và kênh dữ liệu (Data channel) để truyền bản mã. Ngoài ra, bài tập yêu cầu triển khai cơ chế PKCS#7 padding, thiết kế cấu trúc gói tin với Header độ dài và thực hiện kiểm thử tự động để đánh giá tính đúng đắn của hệ thống. Cuối cùng, thông qua việc phân tích mô hình đe dọa (Threat Model), sinh viên nhận diện được các điểm yếu bảo mật của hệ thống khi truyền khóa ở dạng văn bản rõ (plaintext).

## Phân công thực hiện

Đinh Dương Phong: Phụ trách chính phần triển khai Sender, thiết kế cấu trúc kênh khóa, thực hiện ghi log gửi và soạn thảo nội dung báo cáo.

Trần Đình Đức Toàn: Phụ trách chính phần triển khai Receiver, xử lý kênh dữ liệu, thực hiện giải mã AES và xây dựng bộ công cụ kiểm thử (tests).

Phần làm chung: Cả hai thành viên cùng tham gia thảo luận về mô hình đe dọa (Threat Model), phân tích các khía cạnh đạo đức (Ethics) và thực hiện chạy demo hệ thống để đối chiếu kết quả.

## Cách làm
AES-CBC & Padding: Sử dụng thư viện pycryptodome để mã hóa AES chế độ CBC. Triển khai hàm pad và unpad theo tiêu chuẩn PKCS#7 để đảm bảo dữ liệu đầu vào luôn là bội số của 16 bytes.

Cấu trúc gói tin: Thiết kế Header độ dài 4 bytes (network-order) đính kèm trước dữ liệu để Receiver biết chính xác số lượng bytes cần nhận, tránh hiện tượng nghẽn hoặc mất dữ liệu trên dòng stream của Socket.

Kênh truyền:
Key Channel: Sender tạo Key/IV ngẫu nhiên bằng os.urandom, đóng gói theo cấu trúc [key_len][key][iv] và gửi qua KEY_PORT.

Data Channel: Bản mã sau khi mã hóa được gửi qua DATA_PORT kèm theo Header độ dài.

## Kết quả
Chạy Demo: Hệ thống hoạt động ổn định, Receiver nhận và giải mã chính xác các bản tin từ Sender, bao gồm cả tin nhắn trực tiếp và dữ liệu từ file sample_input.txt.

Log minh chứng: Các file log trong thư mục logs/ ghi nhận chi tiết quá trình khởi tạo Key, IV, độ dài bản rõ/bản mã và nội dung giải mã cuối cùng.

Kiểm thử: Toàn bộ các test cases trong thư mục tests/ đều vượt qua (passed), bao gồm các tình huống quan trọng như: kiểm tra padding đúng/sai, truyền nhận gói tin qua socket, và xử lý khi bị thay đổi dữ liệu (tamper).
## Kết luận

