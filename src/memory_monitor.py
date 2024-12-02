import psutil
import docker

def check_memory_usage(threshold, send_email):
    # Docker 컨테이너 모니터링
    client = docker.from_env()
    for container in client.containers.list():
        try:
            stats = container.stats(stream=False)
            memory_usage = stats["memory_stats"]["usage"]
            memory_limit = stats["memory_stats"]["limit"]
            memory_usage_percent = (memory_usage / memory_limit) * 100

            if memory_usage_percent > threshold:
                subject = f"[Docker Alert] High Memory Usage: {container.name}"
                body = f"Container '{container.name}' is using {memory_usage_percent:.2f}% of its allocated memory."
                send_email(subject, body)
        except Exception as e:
            print(f"Error monitoring container {container.name}: {e}")

    # 호스트 프로세스 모니터링
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            if proc.info['memory_percent'] > threshold:
                subject = f"[Host Alert] High Memory Usage: {proc.info['name']}"
                body = (f"Process '{proc.info['name']}' (PID: {proc.info['pid']}) "
                        f"is using {proc.info['memory_percent']:.2f}% of the total memory.")
                send_email(subject, body)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
