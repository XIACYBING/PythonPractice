import ctypes
import http.server
import platform
import ssl
import os
import subprocess

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
import sys

# https://grok.com/share/bGVnYWN5_6ce47d37-f453-47b6-9c17-e457de2d770e


def generate_self_signed_cert(cert_path='server.cert', key_path='server.key'):
    """生成自签名证书和私钥"""
    # 生成私钥
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 生成证书
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'local.hkdev.cn')
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName('local.hkdev.cn')]),
            critical=False
        )
        .sign(key, hashes.SHA256())
    )
    with open(cert_path, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(key_path, 'wb') as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print(f"Generated certificate: {cert_path}")
    print(f"Generated private key: {key_path}")


def delete_cert_files(cert_path='server.cert', key_path='server.key'):
    """删除证书和私钥文件"""
    for path in [cert_path, key_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted: {path}")


def get_hosts_file_path():
    """获取系统 hosts 文件路径"""
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"


def is_admin() -> bool:
    """检查当前是否以管理员/root权限运行"""
    try:
        if platform.system() == "Windows":
            # Windows: 使用 ctypes 检查是否为管理员
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Linux/Mac: 检查有效用户 ID 是否为 0 (root)
            return os.geteuid() == 0
    except AttributeError:
        # 如果 os.geteuid 不存在（Windows 上），假设非管理员
        return False
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False


def add_hosts_entry(ip, domain):
    """将 IP 和域名映射添加到 hosts 文件"""

    # 非管理员不操作
    if not is_admin():
        print("Warn: not administrator, do not operate hosts")
        return

    hosts_file = get_hosts_file_path()
    new_entry = f"{ip} {domain}"

    try:
        # 读取现有 hosts 文件内容
        with open(hosts_file, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # 检查是否已存在相同的映射
        for line in content:
            if new_entry in line.strip():
                print(f"Hosts entry '{new_entry}' already exists.")
                return

        # 追加新映射
        with open(hosts_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{new_entry}\n")
        print(f"Added to hosts: {new_entry}")

        # Windows 需要刷新 DNS 缓存
        if platform.system() == "Windows":
            subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True, text=True, encoding='gbk')
            print("Flushed DNS cache on Windows.")

    except PermissionError:
        print(f"Error: Permission denied when accessing {hosts_file}.")
        print("Please run this script as administrator (Windows) or with sudo (Linux/Mac).")
        sys.exit(1)
    except Exception as e:
        print(f"Error adding hosts entry: {e}")
        sys.exit(1)


def remove_hosts_entry(ip, domain):
    """从 hosts 文件中删除指定的 IP 和域名映射"""

    # 非管理员不操作
    if not is_admin():
        return

    hosts_file = get_hosts_file_path()
    new_entry = f"{ip} {domain}"

    try:
        # 读取 hosts 文件
        with open(hosts_file, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # 过滤掉目标映射
        new_content = [line for line in content if new_entry not in line.strip()]

        # 写回 hosts 文件
        with open(hosts_file, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        print(f"Removed from hosts: {new_entry}")

        # Windows 需要刷新 DNS 缓存
        if platform.system() == "Windows":
            subprocess.run(["ipconfig", "/flushdns"], check=True)
            print("Flushed DNS cache on Windows.")

    except PermissionError:
        print(f"Error: Permission denied when accessing {hosts_file}.")
        print("Please run this script as administrator (Windows) or with sudo (Linux/Mac).")
    except Exception as e:
        print(f"Error removing hosts entry: {e}")


def start_https_server(directory, host='0.0.0.0', port=8000, ip='127.0.0.1', domain='local.hkdev.cn'):
    """启动 HTTPS 服务器并管理 hosts 文件"""
    # 切换到指定目录，支持绝对路径和相对路径，以resource文件夹为例，directory = '../resource'
    os.chdir(directory)
    print(f"Serving files from directory: {os.getcwd()}")

    # 检查证书和私钥是否存在，不存在则生成
    cert_path = os.path.join(directory, 'server.cert')
    key_path = os.path.join(directory, 'server.key')
    generate_self_signed_cert(cert_path, key_path)

    # 添加 hosts 映射
    add_hosts_entry(ip, domain)

    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    print(f"Starting HTTPS server on https://{host}:{port}")
    print(f"Access your page at https://{domain}:{port}/protocol-sign-page.html"
          f"?targetUserType=staff&targetUserId=20193629")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        # 清理：删除证书和 hosts 映射
        delete_cert_files(cert_path, key_path)
        remove_hosts_entry(ip, domain)


if __name__ == '__main__':
    # 默认目录为当前脚本所在目录，你可以修改为其他路径
    target_directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' does not exist.")
        sys.exit(1)

    # 启动服务器
    start_https_server(directory=target_directory, host='0.0.0.0', port=8000)
