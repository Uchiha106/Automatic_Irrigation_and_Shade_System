Hệ thống tưới nước và đóng mở rèm che tự động cho cây cảnh.
Phần cứng gồm: Raspberry Pi 3b+, cảm biến DHT11, còi, cảm biến độ ẩm đất, led 3.3v.
Hệ thống được điều khiển qua giao diện với địa chỉ host. Máy bơm có thể để ở trạng thái tự động hoặc thủ công. 
Nếu để ở chế độ tự động máy bơm sẽ tự bật khi cảm biến độ ẩm đất trả về giá trị tương ứng với độ ẩm dưới 60% ( sau khi đã chuẩn hóa) và tự tắt khi độ ẩm >60%
Ở chế độ thủ công thì máy bơm sẽ được bật tắt theo người thao tác.
Khi trời quá nắng khiến nhiệt độ và độ ẩm của không khi quá mức cho phép rèm sẽ được đóng lại và còi kêu cảnh báo.
Các thông số nhiệt độ, độ ẩm của không khí đọc được từ cảm biến DHT11 và độ ẩm đất tuwf cảm biến độ ẩm đất sẽ được lưu vào MySQL
