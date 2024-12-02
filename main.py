import time
import os
from dotenv import load_dotenv
from src.cpu_monitor import check_cpu_usage
from src.memory_monitor import check_memory_usage
from email.mime.text import MIMEText
import smtplib

load_dotenv()

# 환경 변수 설정
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
RECIPIENT = os.getenv("RECIPIENT")
MEMORY_THRESHOLD_PERCENT = int(os.getenv("MEMORY_THRESHOLD", 80))  # 메모리 임계값 (%)
CPU_THRESHOLD_PERCENT = int(os.getenv("CPU_THRESHOLD", 90))  # CPU 임계값 (%)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  # 초 단위

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, RECIPIENT, msg.as_string())
        print(f"Email sent successfully to {RECIPIENT}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    print("[INFO] Resource monitoring started.")
    print(f"[INFO] Monitoring with the following thresholds:")
    print(f"       - Memory Threshold: {MEMORY_THRESHOLD_PERCENT}%")
    print(f"       - CPU Threshold: {CPU_THRESHOLD_PERCENT}%")
    print(f"       - Check Interval: {CHECK_INTERVAL} seconds")

    while True:
        # CPU 및 메모리 모니터링
        check_cpu_usage(CPU_THRESHOLD_PERCENT, send_email)
        check_memory_usage(MEMORY_THRESHOLD_PERCENT, send_email)

        # 대기 시간 설정
        time.sleep(CHECK_INTERVAL)
