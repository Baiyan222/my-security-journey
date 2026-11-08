import socket
import argparse#加入argparse函数实现高效自动化
import sys
from concurrent.futures import ThreadPoolExecutor

def parse_ports(port_str):
    """解析端口参数，支持 '80,443' 或 '1-1024' 混合写法"""
    ports = set()
    for part in port_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            except ValueError:
                raise argparse.ArgumentTypeError(f"端口范围格式错误: {part}")
        elif part:
            try:
                ports.add(int(part))
            except ValueError:
                raise argparse.ArgumentTypeError(f"端口格式错误: {part}")
    
    # 过滤非法端口并排序
    valid_ports = sorted([p for p in ports if 0 < p <= 65535])
    if not valid_ports:
        raise argparse.ArgumentTypeError("没有提供有效的端口")
    return valid_ports

def scan_port(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    try:
        # connect_ex 返回 0 代表端口开放
        result = s.connect_ex((ip, port))
        if result == 0:
            return port  # 开放则返回端口号
    except Exception:
        pass
    finally:
        s.close()  # 无论成功失败，必定关闭 socket
        
    return None

def main():
    #定义 argparse 参数
    parser = argparse.ArgumentParser(description="Python 自动化端口扫描器")
    parser.add_argument("target", help="目标 IP 或域名 (例如: 127.0.0.1 或 baidu.com)")
    parser.add_argument("-p", "--ports", default="1-1024", help="端口范围，支持 '80,443' 或 '1-1000' (默认: 1-1024)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="超时时间/秒 (默认: 1.0)")
    parser.add_argument("-w", "--workers", type=int, default=100, help="并发线程数 (默认: 100)")
    
    #解析参数
    args = parser.parse_args()
    
    # 解析目标 IP（如果是域名，先转成 IP）
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[-] 无法解析目标域名: {args.target}")
        sys.exit(1)
        
    ports = parse_ports(args.ports)
    
    print(f"[*] 开始扫描目标: {args.target} ({target_ip})")
    print(f"[*] 扫描端口数: {len(ports)} | 超时时间: {args.timeout}s | 并发数: {args.workers}")
    print("-" * 50)

    # 3. 多线程执行扫描（自动化利器）
    open_ports = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # 提交所有任务
        futures = [executor.submit(scan_port, target_ip, port, args.timeout) for port in ports]
        
        # 实时获取结果
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)
                print(f"[+] 端口 {result} 开放")

    print("-" * 50)
    print(f"[*] 扫描完成。共发现 {len(open_ports)} 个开放端口。")

if __name__ == "__main__":
    main()
