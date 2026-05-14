#!/usr/bin/env python3
import os
import sys
import socket
import struct
from Crypto.Cipher import AES

# Đọc environment variables
RECEIVER_HOST = os.environ.get('RECEIVER_HOST', '127.0.0.1')
DATA_PORT = int(os.environ.get('DATA_PORT', 5000))
KEY_PORT = int(os.environ.get('KEY_PORT', 5001))
SOCKET_TIMEOUT = int(os.environ.get('SOCKET_TIMEOUT', 5))

host = RECEIVER_HOST
data_port = DATA_PORT
key_port = KEY_PORT

def decrypt_aes_cbc(key, iv, ciphertext):
    """Giải mã AES-CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    # Xóa padding PKCS7
    pad_len = plaintext_padded[-1]
    return plaintext_padded[:-pad_len]

def recv_exact(sock, num_bytes):
    """Nhận chính xác num_bytes từ socket"""
    data = b''
    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

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
        
        # Nhận key packet (key + IV)
        # Giả sử sender gửi: [4-byte key length][key][4-byte IV length][IV]
        key_len_data = recv_exact(key_conn, 4)
        key_len = struct.unpack('!I', key_len_data)[0]
        
        key = recv_exact(key_conn, key_len)
        
        iv_len_data = recv_exact(key_conn, 4)
        iv_len = struct.unpack('!I', iv_len_data)[0]
        
        iv = recv_exact(key_conn, iv_len)
        
        print(f"Đã nhận key (length: {len(key)}) và IV (length: {len(iv)})", flush=True)
        
        # Nhận ciphertext từ data channel
        # Giả sử format: [4-byte ciphertext length][ciphertext]
        ct_len_data = recv_exact(data_conn, 4)
        ct_len = struct.unpack('!I', ct_len_data)[0]
        
        ciphertext = recv_exact(data_conn, ct_len)
        print(f"Đã nhận ciphertext, độ dài: {len(ciphertext)}", flush=True)
        
        # Giải mã
        plaintext = decrypt_aes_cbc(key, iv, ciphertext)
        plaintext_str = plaintext.decode('utf-8')
        
        # In kết quả
        print(f"[+] Bản tin gốc: {plaintext_str}", flush=True)
        
        # Đóng kết nối
        key_conn.close()
        data_conn.close()
        key_socket.close()
        data_socket.close()
        
    except Exception as e:
        print(f"Lỗi: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()