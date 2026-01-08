import mysql.connector

# Thay thế các thông tin kết nối tại đây
host = "127.0.0.1"  # Địa chỉ IP của Raspberry Pi
user = "root"
password = "654321"
database = "dht_data"

try:
    # Kết nối tới cơ sở dữ liệu MySQL
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Tạo con trỏ để thực hiện truy vấn
    cursor = db.cursor()

    # Ví dụ truy vấn: Hiển thị dữ liệu từ bảng light_status
    cursor.execute("SELECT * FROM dht_data")
    result = cursor.fetchall()

    for row in result:
        print(f"ID: {row[0]}, Humidity: {row[1]}, Temperature: {row[2]}, Timestamp: {row[3]}")

except mysql.connector.Error as err:
    print(f"Lỗi: {err}")

finally:
    # Đóng kết nối với cơ sở dữ liệu
    if 'db' in locals():
        db.close()
