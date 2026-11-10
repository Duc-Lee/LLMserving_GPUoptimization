# Cách các thiết bị hoạt động cùng nhau

- Khi người dùng viết phần mềm bằng ngôn ngữ lập trình bậc cao (C, C++, Java, Python,...) mục đích cuối cùng để CPU thực thi. Tuy nhiên CPU là một mạch số thuần túy - nó không thể hiểu được cú pháp tiếng Anh hay các biến số trừu tượng. CPU chỉ hiểu mã máy (Machine code), tức là các chuỗi nhị phân của các số 0 và 1 (các lệnh mã hóa tập lệnh ISA như x86, ARM)

```mermaid
flowchart TD
    SRC["main.c"] --> COMP["Compiler"]
    COMP --> MC["Machine code<br/><i>Biên dịch thành file .exe để máy tính có thể hiểu và thực thi</i>"]
    MC --> EXE["main.exe<br/>001001<br/>111..."]
```

```text
           main.c
             |
             v
       +------------+
       |  Compiler  | <--- Trình biên dịch
       +------------+
             |
             v
     +--------------+
     | Machine code |
     +--------------+
   Biên dịch thành file .exe để máy
   tính có thể hiểu và thực thi
             |
             v
        +--------+
        | 001001 |   main.exe
        | 111... |
        +--------+
```

+ Trình biên dịch (Compiler) : Đóng vai trò làm thông dịch viên chuyển toàn bộ mã nguồn cấp cao thành tệp thực thi chứa mã máy ví dụ như .exe trên Windows hay định dạng ELF trên Linux
+ Nơi lưu trữ ban đầu : Sau khi biên dịch hoặc cài đặt, tệp thực thi này sẽ được ghi vào ổ cứng (Secondary Storage) dưới dạng một chương trình tĩnh (Passive Entity)

- Tại sao CPU không nạp toàn bộ mọi thứ vào RAM để chạy, hoặc không đọc trực tiếp từ ổ cứng?

+ Ta quay lại bảng so sánh ổ cứng (HDD/SSD) và RAM

| | Ổ cứng (HDD / SSD) | RAM (Bộ nhớ chính) |
| :--- | :--- | :--- |
| **Giá thành và dung lượng** | - Giá thành trên mỗi gigabyte rất rẻ -> Dung lượng rất lớn (500 GB - vài TB) | - Giá thành đắt đỏ -> Dung lượng bị giới hạn (8GB - 64GB) |
| **Tốc độ truy xuất** | Cực kì chậm (mili giây trên HDD, micro giây trên SSD) | Cực kì nhanh (tính bằng nano giây) |
| **Khả năng chứa dữ liệu** | Dư sức chứa hàng trăm phần mềm và dữ liệu lớn | Không thể chứa cùng lúc tất cả dữ liệu trên ổ cứng |

=> Vì sự chênh lệch dung lượng quá lớn, RAM chỉ có thể là không gian lưu trữ tạm thời cho những gì thực sự đang cần dùng

- Về mặt kiến trúc máy tính, CPU không bao giờ nạp từng lệnh thực thi trực tiếp từ các sector của đĩa cứng vì độ trễ I/O quá lớn sẽ làm CPU rơi vào trạng thái nhàn rỗi (idle) liên tục. CPU chỉ giao tiếp trực tiếp với bộ nhớ RAM

- Khi người dùng lệnh chạy một tiến trình

```mermaid
flowchart TD
    CPU["CPU"] -- "truy xuất bus tốc độ cao" --> RAM["RAM (DRAM)"]
    RAM <--> |"Sao chép qua I/O controller khi thiếu trang"| DISK["Ổ cứng (Disk)"]
```

```text
        +---------------+
        |      CPU      |
        +---------------+
                |
                | truy xuất bus tốc độ cao
                v
        +---------------+
        |  RAM (DRAM)   |
        +---------------+
                ^
                | Sao chép qua I/O controller khi thiếu trang
                v
        +---------------+
        | Ổ cứng (Disk) |
        +---------------+
```

+ Kịch bản 1: Chương trình P1 đã nạp sẵn ở trong RAM (tối ưu)
++) Quy trình : CPU phát tín hiệu yêu cầu chỉ thị từ P1. Vì mã lệnh đã nằm trong không gian địa chỉ của RAM, CPU chỉ việc tìm nạp (fetch) và thực thi (execute) trên bus hệ thống

```mermaid
flowchart LR
    CPU["CPU"] <--> |"Tìm nạp và thực thi<br/>(chỉ là nano giây)"| RAM
    
    subgraph RAM ["RAM"]
        direction TB
        R1["Chương trình P1 đã<br/>được sao chép từ ổ cứng<br/>sang RAM"]
        R2[" "]
        R3[" "]
    end
```

```text
                         Tìm nạp                      +-------------------+
    +---------+        và thực thi                    | +---------------+ | <-- chương trình P1 đã
---|   CPU   |--- <------------------->               | |      P1       | |     được sao chép từ
    +---------+      (chỉ là nano giây)               | +---------------+ |     ổ cứng sang RAM
                                                      | +---------------+ |
                                                      | |               | |
                                                      | +---------------+ |
                                                      | +---------------+ |
                                                      | |               | |
                                                      | +---------------+ |
                                                      +-------------------+
                                                               RAM
```

++ Thời gian xử lí : Cực ngắn (vài nano giây). Toàn bộ hệ thống chạy ở vận tốc tối đa của phần cứng

- Kịch bản 2: Chương trình P1 chưa có trong RAM => Xảy ra tắc nghẽn I/O
+ Quy trình : 
    ++ Hệ thống phát hiện chương trình P1 không nằm trong RAM
    ++ Hệ điều hành phải điều khiển bộ điều khiển đĩa (Disk Controller) định vị và đọc dữ liệu của P1 từ các khối trên ổ cứng
    ++ Dữ liệu mã máy được sao chép từ ổ cứng sang các khung trang trống trong RAM
    ++ Sau khi nạp xong vào RAM, CPU mới bắt đầu đọc lệnh từ RAM để thực thi

```mermaid
flowchart LR
    CPU["CPU"] <-- "CPU đọc và thực thi" --- P1_RAM
    
    subgraph RAM ["RAM"]
        direction TB
        M1[" "]
        M2[" "]
        P1_RAM["P1<br/>(Bản sao)"]
    end
    
    subgraph DISK ["Ổ cứng (HDD/SSD)"]
        direction TB
        PLATTER["( Đĩa từ )"]
        P1_DISK["P1"]
    end
    
    P1_DISK -. "Sao chép P1 vào RAM" .-> P1_RAM
```

```text
                       RAM                                   Ổ cứng (HDD/SSD)
                +-------------------+                     +--------------------+
    +-----+     | +---------------+ |                     |       ( O )        |
---| CPU |<-----| |               | |                     |      (đĩa từ)      |
    +-----+     | +---------------+ |                     |                    |
 CPU đọc và     | +---------------+ |                     | +----------------+ |
  thực thi      | |               | |                     | |       P1       | |
                | +---------------+ |                     | +----------------+ |
                | +---------------+ |  Sao chép P1 vào RAM +---------+----------+
                | |      P1       | | < - - - - - - - - - - - - - - -+
                | +---------------+ |
                +---------+---------+
                          |
                       Bản sao
```

+ Thời gian xử lí : Rất dài. Toàn bộ thời gian truy xuất ổ cứng (Seek time, Rotational latency hay SSD NAND read latency) cộng thêm thời gian truyền tải số khối thô từ ổ cứng làm cho CPU luôn có độ trễ nhàn rỗi

=> Như vậy, cốt lõi của một chương trình là sử dụng RAM như một bộ đệm tốc độ cao cho ổ cứng. Khi một chương trình bắt đầu chạy trong RAM, nó không còn đơn thuần là một tệp mã máy tĩnh nữa, nó trở thành một tiến trình (Process)

