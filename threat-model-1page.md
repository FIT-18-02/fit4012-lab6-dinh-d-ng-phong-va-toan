# Threat Model - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Đinh Dương Phong
- Thành viên 2: Trần Đình Đức Toàn

## Assets

Các tài sản cần được bảo vệ trong hệ thống gồm:

Plaintext: dữ liệu gốc trước khi mã hóa.
AES key: khóa bí mật dùng để mã hóa và giải mã dữ liệu.
IV (Initialization Vector): giá trị khởi tạo dùng trong AES mode như CBC/GCM.
Ciphertext: dữ liệu sau khi mã hóa.
File đầu vào: file chứa dữ liệu gốc của người dùng.
File đầu ra: file chứa dữ liệu đã mã hóa hoặc giải mã.
Log hệ thống: thông tin ghi nhận hoạt động gửi/nhận dữ liệu và lỗi hệ thống.
Packet mạng: dữ liệu truyền giữa Sender và Receiver qua socket.

## Attacker model

Đối tượng tấn công có thể:

Nghe lén mạng LAN để bắt các gói tin truyền giữa Sender và Receiver.
Sử dụng công cụ sniffing để đọc ciphertext, key hoặc IV nếu chúng bị gửi plaintext.
Chỉnh sửa ciphertext trước khi đến Receiver.
Thực hiện replay attack bằng cách gửi lại packet cũ.
Đọc file log nếu có quyền truy cập hệ thống.
Giả mạo Sender để gửi dữ liệu giả đến Receiver.

## Threats

Một số mối đe dọa đối với hệ thống:

Key disclosure
AES key hoặc IV có thể bị lộ nếu được gửi dưới dạng plaintext qua mạng hoặc ghi vào log.
Tampering attack
Attacker có thể sửa ciphertext trong quá trình truyền làm dữ liệu giải mã sai hoặc gây lỗi hệ thống.
Replay attack
Packet cũ có thể bị gửi lại nhiều lần khiến Receiver xử lý dữ liệu lặp.
Log leakage
Nếu log chứa key, IV hoặc plaintext thì attacker có thể đọc được thông tin nhạy cảm.
No authentication
Receiver không xác thực Sender nên attacker có thể giả mạo client gửi dữ liệu độc hại.

## Mitigations

Không gửi key plaintext
Trong hệ thống thực tế, AES key không nên truyền trực tiếp qua mạng.
Sử dụng TLS hoặc trao đổi khóa an toàn
Dùng TLS, RSA hoặc Diffie-Hellman để bảo vệ key khi truyền.
Dùng AES-GCM
AES-GCM cung cấp cả mã hóa và xác thực dữ liệu để phát hiện chỉnh sửa ciphertext.
Không ghi key vào log
Chỉ log thông tin cần thiết, không lưu AES key hoặc plaintext thật.
Thêm nonce hoặc timestamp
Giúp phát hiện và ngăn replay attack.
Xác thực Sender
Sử dụng token, certificate hoặc chữ ký số để xác minh client hợp lệ.

## Residual risks

Một số rủi ro vẫn còn tồn tại:

Hệ thống hiện tại chỉ mô phỏng kênh trao đổi khóa và chưa sử dụng TLS thực sự.
Chưa có cơ chế xác thực mạnh giữa Sender và Receiver.
Replay attack vẫn có thể xảy ra nếu nonce/timestamp chưa được kiểm tra đầy đủ.
Nếu attacker chiếm được máy chủ hoặc máy client thì dữ liệu và key vẫn có thể bị lộ.
