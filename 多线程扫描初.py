import socket
from concurrent.futures import ThreadPoolExecutor

def probe(host, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#保障自动调用s.close
        s.settimeout(timeout)#设置时限
        if s.connect_ex((host, port)) == 0:#connect_ex不返回错误码可添加try/except优化
            return port
    return None


def scan(host, ports, timeout=1.0, workers=100):
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as pool:#创线程池
        results = pool.map(lambda p: probe(host, p, timeout), ports)#提交到线程池
        for port in results:#获取结果
            if port is not None:
                open_ports.append(port)
    return open_ports


if __name__ == "__main__":#只有直接运行这个脚本时才执行如果被其他模块 import，不会自动扫描
    result = scan("127.0.0.1", range(1, 1025), workers=100)#"127.0.0.1" range(1, 1025)可修改
    print(result)
