import socket

def scan_port(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                print(f"端口 {port} 开放")
            # else:
            #     print(f"端口 {port} 关闭或过滤")
    except socket.error:
        print(f"扫描端口 {port} 时出错：{e}")


def main():
    target = input("请输入IP或域名：").strip()

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("无法解析该IP或域名")
        return

    try:
        begin_port = int(input("开始端口："))
        end_port = int(input("结束端口："))
    except ValueError:
        print("端口必须是整数")
        return

    if begin_port < 1 or end_port > 65535 or begin_port > end_port:
        print("端口范围无效，应为 1-65535，且开始端口 <= 结束端口")
        return

    print(f"开始扫描 {target} 的端口，从 {begin_port} 到 {end_port}")

    for port in range(begin_port, end_port + 1):
        scan_port(target_ip, port)


if __name__ == "__main__":
    main()
