FROM python:3.9-slim

WORKDIR /app

# Python 패키지 설치
RUN pip install psutil docker python-dotenv

# 스크립트 복사
COPY src/cpu_monitor.py /app/src/
COPY src/memory_monitor.py /app/src/
COPY main.py /app/

# 환경 변수 파일 복사
COPY .env /app/

CMD ["python", "-u", "main.py"]
