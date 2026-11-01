# Nhu cầu xây dựng hệ điều hành

- Qua các phần trước, chúng ta đã biết mã máy nằm trên ổ cứng và CPU chỉ có thể nạp lệnh trực tiếp từ RAM. Bây giờ hãy đi sâu vào bản chất: Hệ điều hành (Operating System) thật sự làm gì trong cỗ máy này?
=> Hệ điều hành bản chất là một bộ quản lí và phân bổ tài nguyên (Resource Allocator / Resource Manager)

- Mọi thành phần trong máy tính mà các tiến trình tranh giành để sử dụng đều là tài nguyên (Resource): CPU, RAM, ổ cứng, thiết bị I/O (chuột, bàn phím, card mạng, máy in,...). Vì tài nguyên luôn có hạn nhưng nhu cầu sử dụng tài nguyên thì vô hạn. Hệ điều hành sinh ra để giải quyết bài toán phân bổ công bằng và tối ưu nhất
