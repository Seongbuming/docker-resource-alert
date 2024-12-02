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
            cpu_quota = stats["cpu_stats"]["online_cpus"]
            cpu_usage_percent = (cpu_delta / system_delta) * cpu_quota * 100

            if cpu_usage_percent > threshold:
                subject = f"[Docker Alert] High CPU Usage: {container.name}"
                body = f"Container '{container.name}' is using {cpu_usage_percent:.2f}% of allocated CPU resources."
                send_email(subject, body)
        except Exception as e:
            print(f"Error monitoring container {container.name}: {e}")

    # 호스트 프로세스 모니터링
    total_cores = psutil.cpu_count()  # 전체 논리 코어 수
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            # CPU 사용률 계산 초기화
            cpu_percent = proc.cpu_percent(interval=0.1)

            # 전체 코어 기준 CPU 사용률 계산
            adjusted_cpu_percent = cpu_percent / total_cores

            if adjusted_cpu_percent > threshold:
                subject = f"[Host Alert] High CPU Usage: {proc.info['name']}"
                body = (f"Process '{proc.info['name']}' (PID: {proc.info['pid']}) "
                        f"is using {adjusted_cpu_percent:.2f}% of total CPU capacity.")
                send_email(subject, body)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
