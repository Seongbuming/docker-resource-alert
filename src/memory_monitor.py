import psutil
import docker

def check_memory_usage(threshold, send_email):
    # Docker 컨테이너 모니터링
    client = docker.from_env()
    for container in client.containers.list():
        try:
            # Docker 컨테이너 메모리 사용량 가져오기
            stats = container.stats(stream=False)
            memory_usage = stats["memory_stats"]["usage"]
            memory_limit = stats["memory_stats"]["limit"]

            # 무제한 메모리 설정 예외 처리
            if memory_limit == 0 or memory_limit == float('inf'):
                memory_limit = psutil.virtual_memory().total # 호스트 전체 메모리로 설정

            # 메모리 사용 비율 계산
            memory_usage_percent = (memory_usage / memory_limit) * 100

            # 임계값 초과 여부 확인
            if memory_usage_percent > threshold:
                subject = f"[Docker Alert] High Memory Usage: {container.name}"
                body = (f"Container '{container.name}' is using {memory_usage_percent:.2f}% of its allocated memory.\n"
                        f"Usage: {memory_usage / (1024**2):.2f} MB / {memory_limit / (1024**2):.2f} MB.")
                send_email(subject, body)
        except Exception as e:
            print(f"Error monitoring container {container.name}: {e}")

    # 호스트 프로세스 모니터링
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            memory_percent = proc.info['memory_percent']
            if memory_percent > threshold:
                subject = f"[Host Alert] High Memory Usage: {proc.info['name']}"
                body = (f"Process '{proc.info['name']}' (PID: {proc.info['pid']}) "
                        f"is using {memory_percent:.2f}% of the total memory.")
                send_email(subject, body)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
