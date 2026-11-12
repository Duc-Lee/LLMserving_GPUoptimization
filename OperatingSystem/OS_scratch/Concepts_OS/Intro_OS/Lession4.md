# Bài 4: Cách thức hoạt động phối hợp của các thiết bị đầu vào, đầu ra

## 1. Phân vùng bộ nhớ RAM: Kernel Space và User Space

- Khi bật máy tính, hệ điều hành (chính là một tập hợp các mã lệnh) sẽ được nạp ngay từ ổ cứng vào RAM.

```mermaid
flowchart LR
    subgraph PC ["Máy tính (Computer)"]
        SCREEN["Màn hình"]
        CASE["Thùng máy (Case)"]
    end

    subgraph RAM ["Thanh RAM"]
        direction TB
        OS["Hệ điều hành<br/>(OS program)"]
        EMPTY["(Vùng nhớ trống)"]
    end

    PC -- "Bật máy (Start)" --> RAM
```

- **Đặc tính của hệ điều hành (OS) trong RAM:** Mã hệ điều hành sẽ nằm thường trực trong RAM suốt quá trình máy tính hoạt động (chỉ mất khi tắt máy).
- **RAM được chia thành 2 vùng:**
  + **Kernel Space (Không gian hệ điều hành):** Nơi chứa toàn bộ mã nguồn, cấu trúc dữ liệu và các module quản lí của OS.
  + **User Space (Không gian người dùng):** Vùng nhớ còn lại dùng để nạp các chương trình ứng dụng do con người cài đặt và sử dụng như MS Word, Photoshop, Calculator,... Các tiến trình $P_1, P_2, P_3,...$ sẽ được cấp phát không gian tại đây.

```mermaid
flowchart LR
    USER["Người dùng (User)"]

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        subgraph KS ["Kernel Space"]
            OS_CODE["Mã nguồn & Module quản lý OS"]
        end
        subgraph US ["User Space"]
            direction TB
            P1["Tiến trình P1"]
            P2["Tiến trình P2"]
            Pdots["..."]
        end
    end

    USER -. "Không thể truy cập trực tiếp<br/>(Can't Access)" .-> KS
    USER --> |"Được phép truy cập<br/>(Can Access)"| US
```

---

## 2. Luồng thực thi của chương trình và cơ chế giao tiếp I/O qua Buffer

- Mã nguồn được biên dịch thành mã máy (`.exe`) nằm trên đĩa cứng. Khi cần chạy, nó được nạp vào User Space trên RAM. CPU sẽ tìm nạp (fetch) và thực thi (execute) từng lệnh. Khi tiến trình kết thúc, toàn bộ dữ liệu và không gian của nó trong RAM sẽ bị thu hồi hoàn toàn để nhường chỗ cho tiến trình khác.

```mermaid
flowchart LR
    subgraph BUILD ["Quy trình xây dựng"]
        direction TB
        SRC["main.c<br/>(Mã nguồn)"] --> COMP["Compiler<br/>(Trình biên dịch)"]
        COMP --> BIN["010110..."]
        BIN --> EXE["main.exe"]
    end

    subgraph DISK ["Ổ cứng (Hard Disk)"]
        STORAGE["Lưu trữ main.exe"]
    end

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        KS["Kernel Space"]
        subgraph US ["User Space"]
            APP["main.exe"]
        end
    end

    subgraph CPU ["CPU"]
        CORE["Lõi xử lý (Core)"]
    end

    EXE -- "Lưu trữ" --> STORAGE
    RAM -- "Gọi main.exe" --> STORAGE
    STORAGE -- "Copy main.exe" --> US
    US -- "Fetch (Tìm nạp lệnh)" --> CORE
    CORE -- "Execute (Thực thi)" --> US
```

- Khi tiến trình chạy xong và cho ra kết quả, CPU thực hiện thu hồi không gian bộ nhớ:

```mermaid
flowchart LR
    RESULT["Kết quả (Result)<br/>(Kết thúc)"]

    subgraph CPU ["CPU"]
        CORE["Lõi xử lý"]
    end

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        KS["Kernel Space"]
        subgraph US ["User Space"]
            FREE["Thu hồi main.exe<br/>(Giải phóng vùng nhớ)"]
        end
    end

    CORE --> |"Thực thi xong"| RESULT
    CORE --> |"Thu hồi main.exe"| US
```

- Trong quá trình chạy, chương trình cần tương tác bên ngoài thông qua các thiết bị vào/ra (I/O Devices).
- **Nguyên tắc cơ bản:** Mọi thiết bị I/O đều đi kèm một vùng nhớ đệm (Buffer / thanh ghi dữ liệu). Dữ liệu không đi thẳng từ phần cứng I/O vào lõi tính toán của CPU mà luôn trung chuyển qua **Buffer $\leftrightarrow$ RAM**.

```mermaid
flowchart LR
    subgraph INPUT_DEV ["Thiết bị Input"]
        KB["Bàn phím"]
    end

    KB_BUF["Keyboard Buffer<br/>(Bộ đệm bàn phím)"]

    subgraph STORAGE_DEV ["Ổ cứng (Vừa In vừa Out)"]
        DISK["Disk"]
    end

    DISK_BUF["Disk Controller Track / Sector Buffer<br/>(Bộ đệm ổ cứng)"]

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        subgraph US ["User Space"]
            DATA["Dữ liệu tiến trình đang thực thi"]
        end
        KS["Kernel Space"]
    end

    subgraph CPU ["CPU"]
        direction TB
        REG["Thanh ghi (Register)"]
        ALU["ALU (Khối tính toán số học)"]
    end

    KB -- "Gõ phím" --> KB_BUF
    KB_BUF --> US

    DISK <--> |"Đọc / Ghi"| DISK_BUF
    DISK_BUF <--> US

    US --> |"Load lệnh / dữ liệu"| REG
    ALU --> |"Store kết quả về RAM"| US
```

### Minh họa qua 2 trường hợp cụ thể:

#### Trường hợp 1: Ứng dụng Calculator ($2 + 3 = 5$)
- Khi người dùng bấm phím $2$ và $3$: Kí tự chuyển thành mã nhị phân (`010` và `011`) đi vào Keyboard buffer, sau đó chuyển tiếp vào RAM.
- CPU nạp các toán hạng này từ RAM vào thanh ghi nội bộ (Register).

```mermaid
flowchart LR
    subgraph INPUT ["Đầu vào (Input)"]
        CALC["Calculator<br/>[ 2 + 3 ]"]
    end

    KB_BUF["Keyboard Buffer<br/>[ 011 | + | 010 ]"]

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        KS["Kernel Space"]
        subgraph US ["User Space"]
            CALC_RAM["Calculator<br/>010 | Add | 011"]
        end
    end

    subgraph CPU ["CPU"]
        direction TB
        REG["Register<br/>010 | Add | 011"]
        ALU["ALU"]
        REG --> ALU
    end

    CALC --> KB_BUF
    KB_BUF --> CALC_RAM
    CALC_RAM --> REG
```

- Khối tính toán số học và logic (ALU - Arithmetic and Logic Unit) của CPU kích hoạt mạch cộng tạo ra kết quả $5$ ($101_2$) và ghi vào một thanh ghi.
- Kết quả được đẩy lại RAM rồi chuyển tới Display Buffer (Bộ đệm màn hình để hiển thị ra pixel cho người dùng thấy).

```mermaid
flowchart LR
    subgraph CPU ["CPU"]
        direction TB
        ALU["ALU"]
        REG["Register<br/>[ 101 ]"]
        ALU --> REG
    end

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        KS["Kernel Space"]
        subgraph US ["User Space"]
            CALC_RAM["Calculator<br/>[ 101 ]"]
        end
    end

    DISP_BUF["Display Buffer<br/>[ 101 ]"]

    subgraph OUTPUT ["Đầu ra (Output)"]
        DISP["Display (Màn hình)<br/>[ 2 + 3 = 5 ]"]
    end

    REG --> CALC_RAM
    CALC_RAM --> DISP_BUF
    DISP_BUF --> DISP
```

---

#### Trường hợp 2: Chỉnh sửa tài liệu MS Word
- File tài liệu lưu trên ổ cứng được nạp lên RAM để CPU xử lí.
- Người dùng gõ bàn phím $\Rightarrow$ dữ liệu qua Buffer vào RAM để chắp nối vào văn bản.
- Khi bấm Save (Lưu vĩnh viễn): toàn bộ dữ liệu từ RAM được ghi xuống ổ cứng.

```mermaid
flowchart LR
    FOLDER1["Thư mục (Folder)"]

    subgraph DISK1 ["Ổ cứng (Hard Disk)"]
        PLATTER1["Đĩa từ (Platter)"]
    end

    subgraph RAM1 ["Bộ nhớ RAM"]
        direction TB
        KS1["Kernel Space"]
        subgraph US1 ["User Space"]
            WORD1["MS Word"]
        end
    end

    subgraph CPU1 ["CPU"]
        CORE1["Lõi xử lý"]
    end

    FOLDER1 -- "Lưu trữ" --> PLATTER1
    PLATTER1 -- "Đọc" --> US1
    US1 <--> CORE1
```

```mermaid
flowchart LR
    KB["Bàn phím<br/>(Thiết bị đầu vào - Input)"]
    KB_BUF["Buffer Keyboard"]

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        KS["Kernel Space"]
        subgraph US ["User Space"]
            WORD["MS Word"]
        end
    end

    KB --> KB_BUF
    KB_BUF -- "Ghi dữ liệu" --> US
```

```mermaid
flowchart LR
    subgraph CPU ["CPU"]
        CORE["Lõi xử lý"]
    end

    subgraph RAM ["Bộ nhớ RAM"]
        direction TB
        KS["Kernel Space"]
        subgraph US ["User Space"]
            WORD["MS Word"]
        end
    end

    subgraph DISK ["Ổ cứng (Hard Disk)"]
        PLATTER["Đĩa từ (Platter)"]
    end

    FOLDER["Thư mục (Folder)"]

    CORE -- "Lệnh Save" --> US
    US -- "Thực thi" --> CORE
    US -- "Ghi dữ liệu" --> PLATTER
    PLATTER -- "Lưu trữ" --> FOLDER
```

=> **Kết luận:** Ổ cứng vừa có thể đọc dữ liệu lên RAM, vừa có thể ghi dữ liệu từ RAM xuống nên ổ cứng đóng cả 2 vai trò: **Thiết bị Input lẫn Output**.

---

## 3. Vòng đời tiến trình và khái niệm cốt lõi Turnaround Time

- Bất kì chương trình nào được nạp vào RAM cũng sẽ luân chuyển qua 3 trạng thái hoạt động chính:
  + **Running (Burst Time / Execution Time):** CPU đang trực tiếp xử lí các lệnh tính toán của chương trình.
  + **Waiting for I/O (I/O Time):** Chương trình tạm dừng chạy để chờ nhận dữ liệu từ bàn phím, chờ đọc/ghi ổ cứng, hoặc chờ xuất màn hình.
  + **Waiting (Waiting Time):** Chương trình nằm sẵn trong RAM nhưng phải chờ đến lượt được CPU cấp phát thời gian chạy (chờ scheduler điều phối).

- Thứ tự đan xen giữa tính toán (CPU burst) $\rightarrow$ Chờ I/O (I/O burst) $\rightarrow$ Chờ CPU (Waiting) sẽ tùy thuộc vào bản chất của từng chương trình cụ thể, không cố định.

---

### Công thức thời gian quay vòng (Turnaround Time):

- Khoảng thời gian tính từ khi một chương trình bắt đầu được nạp vào RAM cho đến khi kết thúc hoàn toàn và giải phóng khỏi RAM được gọi là **Turnaround Time (Thời gian quay vòng)**.

$$\text{Turnaround Time} = \text{Waiting Time} + \text{Burst Time (Execution Time)} + \text{I/O Time}$$

- **Ví dụ:** Một tiến trình $P_1$ được nạp vào RAM lúc 1:00 am và hoàn tất toàn bộ, giải phóng RAM lúc 3:00 am:
  $$\text{Turnaround Time} = 3\text{h} - 1\text{h} = 2\text{h}$$

=> **Ý nghĩa:** Trong suốt quá trình 2 tiếng này, thời gian của $P_1$ thực chất là tổng của:
- Thời gian CPU bận xử lí nó (**Burst Time**)
- Thời gian thao tác nó đọc/ghi thiết bị (**I/O Time**)
- Thời gian nó phải nằm trong hàng đợi để nhường CPU cho tiến trình khác (**Waiting Time**)

---

### Như vậy:
- Việc hiểu rõ một tiến trình luôn tiêu tốn thời gian cho **Tính toán (Burst)**, **Vào/ra dữ liệu (I/O)** và **Chờ đợi (Waiting)** chính là tiền đề quan trọng nhất để bước vào phần: **Các thuật toán lập lịch CPU (CPU scheduler Algorithms)**, nơi Hệ điều hành tìm cách tối ưu hóa Turnaround Time và Waiting Time của toàn bộ hệ thống.

