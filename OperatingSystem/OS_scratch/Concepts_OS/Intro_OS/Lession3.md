# Bài 3: Nhu cầu xây dựng hệ điều hành từ đầu

- Hệ điều hành (Operating System - OS) thực chất là một hệ thống phần mềm lớn đóng vai trò cốt lõi là **Bộ quản trị và phân bổ tài nguyên** (Resource Allocator / Resource Manager)
- Bản chất của máy tính là sự cạnh tranh giữa các chương trình để sử dụng các tài nguyên phần cứng giới hạn (RAM, CPU, ổ cứng, thiết bị I/O). Để giải quyết bài toán này, hệ điều hành chia nhỏ nhiệm vụ cho các module chức năng chuyên trách, tiêu biểu là 2 bộ lập lịch dưới đây:

---

## 1. Bài toán phân bổ RAM: Bộ lập lịch dài hạn (Long-term scheduler)

### Bối cảnh:
- **Ổ cứng (Hard Disk):** Lưu trữ khối lượng lớn (Ví dụ: 500 chương trình), nhưng CPU không thể truy xuất trực tiếp dữ liệu / lệnh từ ổ cứng để thực thi.
- **RAM:** Có tốc độ cao và CPU truy xuất trực tiếp được, nhưng dung lượng có hạn (Ví dụ: chỉ chứa tối đa 50 chương trình cùng lúc).

```mermaid
flowchart LR
    subgraph DISK ["Ổ cứng - Hard Disk (500 chương trình)"]
        PLATTER["Đĩa từ (Platter) / Flash"]
    end

    subgraph CPU ["CPU (Bộ vi xử lý)"]
        CORE["Lõi xử lý (Core)"]
    end

    subgraph RAM ["Thanh RAM (50 chương trình)"]
        direction TB
        R1["Slot 1"]
        R2["Slot 2"]
        Rdots["..."]
        R50["Slot 50"]
    end

    DISK -.- |"Không thể truy xuất trực tiếp (X)"| CPU
    CPU <--> |"Truy xuất trực tiếp tốc độ cao"| RAM
```

---

### Vấn đề đặt ra:
- Trong số 500 chương trình trên đĩa cứng, 50 chương trình nào sẽ được nạp vào RAM trước?

```mermaid
flowchart LR
    subgraph CPU ["CPU"]
        CORE["Lõi xử lý"]
    end

    subgraph RAM ["Thanh RAM (Chứa tối đa 50 CT)"]
        direction TB
        R1["Ô nhớ 1: ?"]
        R2["Ô nhớ 2: ?"]
        Rdots["..."]
        R50["Ô nhớ 50: ?"]
    end

    subgraph DISK ["Ổ cứng - Hard Disk"]
        direction TB
        PLATTER["500 chương trình<br/>(Prog 1 ... Prog 500)"]
    end

    CPU <--> |"Truy xuất trực tiếp"| RAM
    DISK -.-> |"Nạp 50 chương trình nào trước?"| RAM
```

- **Mục tiêu tối ưu:** Lý tưởng nhất là giữ sẵn trong RAM những chương trình mà CPU có xác suất cần dùng cao nhất trong tương lai gần. Nếu CPU tìm thấy chương trình ngay trong RAM, thời gian đáp ứng cực nhanh; ngược lại, nếu phải sinh truy xuất từ đĩa cứng, hệ thống sẽ trễ rất lớn.
- **Giải pháp kĩ thuật:** Hệ điều hành không thể biết chính xác 100% tương lai, do đó nó sử dụng các thuật toán dự đoán và chính sách nạp.
- **Module đảm trách:** **Bộ lập lịch dài hạn (Long-Term Scheduler)** hay còn gọi là **Job Scheduler**. Chức năng này quyết định mức độ đa chương (**Degree of multiprogramming**) bằng cách chọn lọc các tác vụ từ hàng đợi trên đĩa cứng (**Job Pool**) nạp vào bộ nhớ RAM.

```mermaid
flowchart LR
    subgraph DISK ["Ổ cứng (Hard Disk)"]
        direction TB
        JP["Job Pool<br/>- Prog 1<br/>- Prog 2<br/>- Prog 3<br/>...<br/>- Prog 500"]
    end

    LTS["Long-Term Scheduler<br/>(Bộ lập lịch dài hạn)<br/>- Phân tích dự đoán<br/>- Áp dụng thuật toán chọn<br/>- Kiểm soát mức đa chương"]

    subgraph RAM ["Thanh RAM (Đầy 50 spots)"]
        direction TB
        subgraph RQ ["Ready Queue"]
            direction TB
            P1["P1"]
            P2["P2"]
            Pdots["..."]
            P50["P50"]
        end
    end

    subgraph CPU ["CPU"]
        CORE["Lõi xử lý"]
    end

    JP -->|"500 chương trình đang chờ"| LTS
    LTS -->|"Chọn 50 chương trình"| RQ
    RQ -->|"Các tiến trình tranh CPU<br/>(Short-Term Scheduler)"| CORE
```

=> **Như vậy:** Bộ lập lịch dài hạn (Long-term scheduler) kiểm soát số lượng tiến trình trong RAM, cân bằng giữa tác vụ I/O và tác vụ CPU.

---

## 2. Bài toán phân bổ CPU: Bộ lập lịch ngắn hạn (Short-Term scheduler)

### Bối cảnh:
- Khi các chương trình được nạp thành công vào RAM (lúc này được gọi là các tiến trình - **Processes**), chúng đều ở trạng thái sẵn sàng (**Ready**) để chạy.

```mermaid
flowchart LR
    subgraph RAM ["Thanh RAM"]
        direction TB
        subgraph RQ ["Ready Queue (Hàng đợi sẵn sàng)"]
            direction TB
            P1["Tiến trình P1"]
            P2["Tiến trình P2"]
            Pdots["..."]
            P50["Tiến trình P50"]
        end
    end

    subgraph CPU ["CPU (1 lõi đơn)"]
        CORE["Lõi xử lý duy nhất<br/>(Chỉ chạy 1 tiến trình tại 1 thời điểm)"]
    end

    RQ <--> |"Cấp phát CPU cho ai trước?<br/>(P1 hay P2?)"| CORE
```

### Vấn đề đặt ra:
- CPU tại 1 thời điểm với 1 lõi đơn chỉ có thể xử lí một tiến trình. Vậy tiến trình nào? ($P_1$ hay $P_2$) sẽ được cấp phát CPU trước?

### Giải pháp:
- Hệ điều hành áp dụng các thuật toán định thời CPU cụ thể, ví dụ:
  + Tiến trình nào vào RAM trước thì chạy trước (**FCFS** - First-Come, First-Served)
  + Tiến trình có thời gian thực thi ngắn nhất được ưu tiên (**SJF** - Shortest Job First)
  + Phân chia theo độ ưu tiên hoặc kích thước / loại tác vụ

### Module đảm trách:
- **Bộ lập lịch ngắn hạn (Short-Term Scheduler)** hay còn gọi là **CPU scheduler**.
- Chức năng này chạy với tần suất rất cao (thường ở mức mili giây) để liên tục chọn tiến trình sẵn sàng tiếp theo và giao quyền kiểm soát CPU (thông qua Dispatcher). Tại đây, CPU chính là tài nguyên đang được phân bổ.

```mermaid
flowchart LR
    subgraph RAM ["Thanh RAM"]
        direction TB
        subgraph RQ ["Ready Queue"]
            direction TB
            P1_Q["[ P1 ]"]
            P2_Q["[ P2 ]"]
            P3_Q["[ P3 ]"]
            Pdots_Q["..."]
            P50_Q["[ P50 ]"]
        end
    end

    STS["Short-Term Scheduler<br/>(CPU Scheduler)<br/>Tần suất: mili giây"]
    PROC["Tiến trình P1<br/>(Được chọn)"]

    subgraph CPU ["CPU"]
        CORE["Lõi xử lý<br/>[ P1 đang chạy ]"]
    end

    STS -.-> |"1. Kiểm tra hàng đợi"| RQ
    RQ -->|"2. Lấy P1 ra"| PROC
    PROC -->|"3. Giao quyền kiểm soát"| STS
    STS -->|"4. Dispatcher nạp vào core"| CORE
```

=> **Short-Term Scheduler** chính là bộ phân bổ tài nguyên CPU theo thời gian thực. Nhiệm vụ cốt lõi của nó là điều phối dòng tiến trình từ Ready Queue lên CPU một cách nhanh và chính xác nhất, đảm bảo CPU không bao giờ rơi vào trạng thái rảnh rỗi vô ích.
