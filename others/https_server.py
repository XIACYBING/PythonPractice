import http.server
import ssl
import os

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
import sys


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


def start_https_server(directory, host='0.0.0.0', port=8000):
    """启动 HTTPS 服务器"""
    # 切换到指定目录
    os.chdir(directory)
    print(f"Serving files from directory: {os.getcwd()}")

    # 检查证书和私钥是否存在，不存在则生成
    cert_path = os.path.join(directory, 'server.cert')
    key_path = os.path.join(directory, 'server.key')
    generate_self_signed_cert(cert_path, key_path)

    # 创建 HTTP 服务器
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

    # 配置 SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print(f"Starting HTTPS server on https://{host}:{port}")
    print(f"Access your page at https://local.hkdev.cn:{port}/protocol-sign-page.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
    finally:
        delete_cert_files(cert_path, key_path)


if __name__ == '__main__':
    # 默认目录为当前脚本所在目录，你可以修改为其他路径
    target_directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' does not exist.")
        sys.exit(1)

    # 启动服务器
    start_https_server(directory=target_directory, host='0.0.0.0', port=8000)
