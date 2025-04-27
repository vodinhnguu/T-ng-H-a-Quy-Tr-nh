import os
import shutil
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

DATABASE_FOLDER = 'database'   
BACKUP_FOLDER = 'backups'        
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
load_dotenv()
EMAIL_SENDER = os.getenv('EMAIL_SENDER')  
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') 
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')  

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Bật bảo mật
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email thông báo: {subject}")

    except Exception as e:
        print("Gửi email thất bại:", e)

def backup_database():
    try:
        # Đường dẫn tới file database gốc
        src_file = "database/SQLBai3.sql"
        # Thư mục lưu file backup
        backup_dir = "backups"
        # Tạo thư mục backup nếu chưa có
        os.makedirs(backup_dir, exist_ok=True)

        # Tạo tên file backup theo ngày giờ
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"SQLBai3_backup_{timestamp}.sql")

        # Copy file
        if os.path.exists(src_file):
            shutil.copy(src_file, backup_file)
            send_email("Backup Database Thành Công", f"Đã sao lưu database thành công tới file {backup_file}")
        else:
            send_email("Backup Database Thất Bại", "Không tìm thấy file database để sao lưu.")

    except Exception as e:
        send_email("Backup Database Thất Bại", f"Lỗi: {str(e)}")
# Lên lịch chạy mỗi ngày lúc 00:00
schedule.every().day.at("23:53").do(backup_database)
print("Đang chạy tiến trình backup database mỗi ngày lúc 00:00...")

while True:
    schedule.run_pending()  # Kiểm tra công việc lên lịch
    time.sleep(60)  # Chờ một phút để kiểm tra lại