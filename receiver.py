#!/usr/bin/env python3
import os
import sys
import socket
import struct
from Crypto.Cipher import AES

# Đọc environment variables NGAY TỪ ĐẦU
RECEIVER_HOST = os.environ.get('RECEIVER_HOST', '127.0.0.1')
DATA_PORT = int(os.environ.get('DATA_PORT', 5000))
KEY_PORT = int(os.environ.get('KEY_PORT', 5001))
SOCKET_TIMEOUT = int(os.environ.get('SOCKET_TIMEOUT', 5))

# Gán cho các biến ngắn gọn
host = RECEIVER_HOST
data_port = DATA_PORT
key_port = KEY_PORT

def main():
    try:
        # Tạo key channel
        print(f"Đang khởi tạo key channel trên {host}:{key_port}", flush=True)
        key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        key_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        key_socket.bind((host, key_port))
        key_socket.listen(1)
        print(f"kênh khóa đã sẵn sàng", flush=True)
        
        # Tạo data channel
        print(f"Đang khởi tạo data channel trên {host}:{data_port}", flush=True)
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        data_socket.bind((host, data_port))
        data_socket.listen(1)
        print(f"data channel đã sẵn sàng", flush=True)
        
        print("đã sẵn sàng nhận kết nối", flush=True)
        
        # Chấp nhận kết nối từ sender
        print("Đang chờ kết nối từ sender...", flush=True)
        key_conn, key_addr = key_socket.accept()
        print(f"Đã chấp nhận kết nối key từ {key_addr}", flush=True)
        
        data_conn, data_addr = data_socket.accept()
        print(f"Đã chấp nhận kết nối data từ {data_addr}", flush=True)
        
        # Nhận key
        key_data = key_conn.recv(1024)
        print(f"Đã nhận key, độ dài: {len(key_data)}", flush=True)
        
        # TODO: Xử lý giải mã ở đây
        
        key_conn.close()
        data_conn.close()
        key_socket.close()
        data_socket.close()
        
    except Exception as e:
        print(f"Lỗi: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()