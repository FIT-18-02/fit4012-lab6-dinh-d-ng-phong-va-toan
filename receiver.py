import socket
import os
import sys
from Crypto.Cipher import AES
# ... các import khác

def main():
    # Lấy thông tin từ environment variables hoặc arguments
    host = os.environ.get('RECEIVER_HOST', '127.0.0.1')
    data_port = int(os.environ.get('DATA_PORT', 5000))
    key_port = int(os.environ.get('KEY_PORT', 5001))
    
    # Tạo socket cho key channel
    key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    key_socket.bind((host, key_port))
    key_socket.listen(1)
    print(f"kênh khóa đã sẵn sàng trên {host}:{key_port}", flush=True)
    
    # Tạo socket cho data channel
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data_socket.bind((host, data_port))  # Dòng 113 - cần biến 'host' đã được định nghĩa
    data_socket.listen(1)
    print(f"data channel đã sẵn sàng trên {host}:{data_port}", flush=True)
    
    print("đã sẵn sàng nhận kết nối", flush=True)
    
    # ... phần còn lại của code

if __name__ == "__main__":
    main()