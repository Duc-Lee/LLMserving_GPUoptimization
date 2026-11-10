# Giới thiệu hệ thống máy tính

- Hệ thống máy tính là sự kết hợp của phần cứng, phần mềm và dữ liệu được sử dụng để giải quyết vấn đề của con người
  + Phần cứng (Hardware) : Các linh kiện vật lí (CPU, RAM, ổ cứng,...)
  + Phần mềm (Software) : Tập hợp các lệnh chỉ dẫn máy tính cần làm gì (thực chất là các chương trình như Chrome,...)
  + Dữ liệu (Data) : Thông tin thô cần xử lí (văn bản, hình ảnh, video). Không có dữ liệu, phần mềm trở nên vô nghĩa

- Mô hình chương trình lưu trữ
  + Máy tính hiện đại vận hành dựa trên nguyên lí then chốt : Muốn chạy được, chương trình phải được nạp vào bộ nhớ

```mermaid
flowchart LR
    classDef ioStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#bf360c;
    classDef cpuStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1;
    classDef subCpu fill:#bbdefb,stroke:#1976d2,stroke-width:1.5px,color:#0d47a1;

    IN["Input Unit<br/>(Bàn phím, Chuột...)"]:::ioStyle

    subgraph CPU_CHIP ["CPU (Bộ vi xử lý trung tâm)"]
        direction TB
        MU["Memory Unit<br/>(Đơn vị bộ nhớ trong)"]:::subCpu
        CU["Control Unit<br/>(Đơn vị điều khiển)"]:::subCpu
        ALU["Arithmetic & Logic Unit<br/>(Đơn vị số học & logic)"]:::subCpu
        
        MU <--> CU
        CU <--> ALU
    end

    OUT["Output Unit<br/>(Màn hình, Máy in...)"]:::ioStyle

    IN --> CU
    CU --> OUT
```

++) Khi bạn muốn chỉnh sửa hình ảnh, phần mềm (chương trình) và bức ảnh (dữ liệu) sẽ được đưa vào bộ nhớ  
++) CPU đóng vai trò như bộ não : liên tục tìm nạp dữ liệu (fetch), giải mã (decode) và thực thi (execute) từng chỉ thị từ bộ nhớ với tốc độ cực cao

---

• Tại sao máy tính cần phân cấp bộ nhớ (Memory hierarchy)
- Tại sao không lưu tất cả vào một nơi duy nhất mà phải chia ra ổ cứng, RAM rồi đến Cache và Register?
=> Câu trả lời nằm ở bài toán đánh đổi giữa tốc độ truy xuất và tính bền vững của dữ liệu

| | Ổ cứng (HDD / SSD) | RAM (Bộ nhớ chính) |
| :--- | :--- | :--- |
| **Bảo toàn dữ liệu** | - Không mất dữ liệu : Tắt máy hay mất điện, dữ liệu vẫn còn nguyên | - Mất dữ liệu khi mất điện : Dữ liệu biến mất ngay lập tức khi ngắt nguồn |
| **Tốc độ truy xuất** | Rất chậm (tính bằng mili giây hoặc micro giây) | - Cực kì nhanh (tính bằng nano giây), nhanh hơn cả ổ cứng trăm đến hàng chục nghìn lần |
| **Giá và Dung lượng** | Rẻ trên mỗi GB, dung lượng lưu trữ lớn (hàng trăm GB đến TB) | Đắt hơn nhiều, dung lượng giới hạn 8GB - 64GB |

- Chúng ta muốn cả 2 : Dữ liệu vừa phải được lưu vĩnh viễn, vừa phải được CPU xử lí với tốc độ tối đa
=> Vì vậy hệ thống hoạt động theo nguyên lí "Copy - Paste" chứ không phải "Cut - Paste"
  + Lưu trữ tĩnh : mọi phần mềm và tệp tin luôn nằm an toàn trên ổ đĩa
  + Nạp khi thực thi : Khi bạn mở một ứng dụng ví dụ Word, hệ thống sẽ tạo một bản sao của chương trình cùng dữ liệu liên quan từ ổ cứng sang RAM
  + CPU làm việc trực tiếp với RAM : nhờ tốc độ của RAM, CPU không bị nghẽn cổ chai và có thể chạy hết công suất
  + An toàn dữ liệu : Nếu mất điện đột ngột, bản gốc trên đĩa cứng vẫn nguyên vẹn

- Các tầng bộ nhớ sâu hơn như Cache hay Register nằm trực tiếp trên CPU để phục vụ tối ưu kiến trúc phần cứng, còn đối với hệ điều hành, mối quan hệ giữa RAM và ổ cứng là nền tảng cốt lõi cần nắm vững trước tiên

```mermaid
flowchart LR
    classDef noteStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1.5px,color:#4a148c;
    classDef cpuStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:1.5px,color:#0d47a1;
    classDef ramSlot fill:#e8f5e9,stroke:#2e7d32,stroke-width:1.5px,color:#1b5e20;

    subgraph Ghi_chu_CPU ["Chú thích CPU"]
        direction TB
        C1["CU: Khối điều khiển (Giải mã lệnh)"]:::noteStyle
        C2["ALU: Khối tính toán (Số học & logic)"]:::noteStyle
        C3["Register: Thanh ghi tạm thời siêu tốc"]:::noteStyle
        C4["Cache: Bộ nhớ đệm tốc độ cao"]:::noteStyle
    end

    subgraph CPU ["CPU"]
        direction TB
        CU["CU"]:::cpuStyle
        ALU["ALU"]:::cpuStyle
        REG["Register"]:::cpuStyle
        CACHE["Cache"]:::cpuStyle
    end

    C1 -.-> CU
    C2 -.-> ALU
    C3 -.-> REG
    C4 -.-> CACHE

    subgraph RAM_STICK ["Thanh RAM (Bộ nhớ truy cập ngẫu nhiên)"]
        direction TB
        R1["[ Ô nhớ 0x01 ]"]:::ramSlot
        R2["[ Ô nhớ 0x02 ]"]:::ramSlot
        R3["[ Ô nhớ 0x03 ]"]:::ramSlot
        R4["[ Ô nhớ 0x04 ]"]:::ramSlot
        R5["[ Ô nhớ 0x05 ]"]:::ramSlot
    end

    CU -- "1. CPU gửi yêu cầu dữ liệu" --> RAM_STICK
    RAM_STICK -- "2. RAM phản hồi dữ liệu" --> CU
    RAM_STICK -- "Đọc lệnh / dữ liệu" --> ALU
    RAM_STICK -- "Nạp vào thanh ghi" --> REG
    RAM_STICK -- "Đệm dữ liệu" --> CACHE

    CPU ==>|"3. Tính toán xong, ghi kết quả về RAM"| RAM_STICK
```

- Khi đã hiểu CPU tương tác với RAM và ổ cứng, câu hỏi tiếp theo là: "Ai là người chịu trách nhiệm tải chương trình từ đĩa vào RAM, quản lí không gian RAM để các phần mềm không ghi đè lên nhau, và điều phối CPU chạy luân phiên giữa các ứng dụng?"
=> Đó là nhiệm vụ của HĐH
