import psutil
import docker

def check_cpu_usage(threshold, send_email):
    # Docker 컨테이너 모니터링
    client = docker.from_env()
    for container in client.containers.list():
        try:
            stats = container.stats(stream=False)
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
            cpu_usage_percent = (cpu_delta / system_delta) * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100

            if cpu_usage_percent > threshold:
                subject = f"[Docker Alert] High CPU Usage: {container.name}"
                body = f"Container '{container.name}' is using {cpu_usage_percent:.2f}% of CPU."
                send_email(subject, body)
        except Exception as e:
            print(f"Error monitoring container {container.name}: {e}")

    # 호스트 프로세스 모니터링
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent(interval=None)  # CPU 사용률 계산 초기화
            if proc.info['cpu_percent'] > threshold:
                subject = f"[Host Alert] High CPU Usage: {proc.info['name']}"
                body = (f"Process '{proc.info['name']}' (PID: {proc.info['pid']}) "
                        f"is using {proc.info['cpu_percent']:.2f}% of CPU.")
                send_email(subject, body)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
