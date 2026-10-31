# Pandas in Python : Series & DataFrame

- Tiếp tục chuỗi bài học Python thuộc mô đun Phân tích dữ liệu (Data Analysis), sau khi tìm hiểu về thư viện Numpy, tiếp theo sẽ đi sâu vào một thư viện quan trọng tiếp theo là Pandas.
- Pandas cung cấp khả năng xử lí, dọn dẹp và chuẩn bị dữ liệu mạnh mẽ. Trọng tâm bài học này sẽ giải quyết 2 cấu trúc dữ liệu cốt lõi: Series (chuỗi dữ liệu) và DataFrame (khung dữ liệu).

### 1. Giới thiệu tổng quan và cài đặt Pandas

- Pandas là thư viện xử lí và phân tích dữ liệu dạng bảng (tabular data), hỗ trợ linh hoạt thao tác làm sạch dữ liệu.
- **Series**: Là cấu trúc mảng một chiều (1D array-like), có trục nhãn (index). Series tương đương với một cột duy nhất trong bảng tính. Bạn có thể chuyển đổi trực tiếp một mảng 1 chiều từ Numpy thành một Series.
- **DataFrame**: Là cấu trúc dữ liệu dạng bảng 2 chiều (2D), có thể thay đổi kích thước (size-mutable) và chứa các kiểu dữ liệu không đồng nhất (heterogeneous). DataFrame tương đương với một bảng tính trong Excel hoặc một bảng trong cơ sở dữ liệu quan hệ (gồm nhiều hàng và nhiều cột). Tương tự mảng 2 chiều Numpy có thể chuyển thành DataFrame.
- Trước khi bắt đầu, môi trường ảo (virtual environment) cần được kích hoạt. Có 2 cách cài đặt:
  - **Cách 1: Cài đặt qua file requirements.txt**
    - Thêm pandas vào file rồi mở terminal gõ lệnh:
```bash
pip install -r requirements.txt
```
  - **Cách 2: Cài đặt trực tiếp trên terminal**
```bash
pip install pandas
```
- Quy ước khi làm việc với Pandas là import kèm bí danh (alias) là `pd`:
```python
import pandas as pd
```

### 2. Pandas Series

- Series là cấu trúc dữ liệu một chiều có nhãn, có lưu trữ bất kì kiểu dữ liệu nào (số nguyên, số thực, chuỗi, vv...).

#### a. Tạo Series từ List

```python
import pandas as pd

data = [1, 2, 3, 4, 5]

# khoi tao Series
series = pd.Series(data)
print(series)
```

- Kết quả:
```text
0    1
1    2
2    3
3    4
4    5
dtype: int64
```

- Lưu ý: Các số 0, 1, 2, 3, 4 ở cột bên trái là index mặc định do Pandas tự động sinh ra.
- Kiểm tra kiểu dữ liệu của biến:

```python
# Kiem tra kieu du lieu cua bien
print(type(series))
# Output:
# <class 'pandas.core.series.Series'>
```

#### b. Tạo Series từ Dictionary

- Khi truyền một Dictionary vào `pd.Series()`, các key (khóa) của từ điển sẽ tự động được sử dụng làm index, còn các value sẽ đóng vai trò là dữ liệu.

```python
import pandas as pd

data_dict = {
    'a': 1,
    'b': 2,
    'c': 3
}

# chuyen dict sang series
series_dict = pd.Series(data_dict)
print(series_dict)
```

- Kết quả:
```text
a    1
b    2
c    3
dtype: int64
```

#### c. Tạo Series kèm index tùy chỉnh (Custom index)

- Bạn có thể tùy biến hoàn toàn nhãn index bằng cách truyền tham số `index`.

```python
import pandas as pd

data = [10, 20, 30]
custom_index = ['a', 'b', 'c']

# tuy chinh index
series = pd.Series(data, index=custom_index)
print(series)
```

- Kết quả:
```text
a    10
b    20
c    30
dtype: int64
```

### 3. Pandas DataFrame

- DataFrame là cấu trúc dữ liệu 2 chiều có nhãn ở cả hàng (index) và cột (columns).

#### a. Tạo DataFrame từ Dictionary chứa các List

- Mỗi khóa key sẽ đại diện cho một cột và danh sách (List) tương ứng đại diện cho các giá trị trên từng hàng của cột đó. Độ dài của các List phải bằng nhau.

```python
import pandas as pd

data = {
    'name': ['Krish', 'John', 'Jack'],
    'age': [25, 30, 45],
    'city': ['Bangalore', 'New York', 'Florida']
}

df = pd.DataFrame(data)
print(df)
```

- Kết quả:
```text
    name  age       city
0  Krish   25  Bangalore
1   John   30   New York
2   Jack   45    Florida
```

- **Chuyển đổi DataFrame sang mảng Numpy**: Khi cần đưa dữ liệu về dạng mảng tính toán mà không giữ lại nhãn hàng hay tên cột.

```python
import numpy as np

# Chuyen DataFrame sang mang Numpy
arr = np.array(df)
print(arr)
```

- Kết quả:
```text
[['Krish' 25 'Bangalore']
 ['John' 30 'New York']
 ['Jack' 45 'Florida']]
```

#### b. Tạo DataFrame từ List các Dictionary

- Mỗi dictionary trong danh sách (List) tương ứng với một hàng dữ liệu.

```python
import pandas as pd

data_list = [
    {'name': 'Krish', 'age': 32, 'city': 'Bangalore'},
    {'name': 'John', 'age': 34, 'city': 'New York'},
    {'name': 'Jack', 'age': 32, 'city': 'Berkeley'}
]

# chuyen sang data frame
df_from_list = pd.DataFrame(data_list)
print(df_from_list)
```

- Kết quả:
```text
    name  age       city
0  Krish   32  Bangalore
1   John   34   New York
2   Jack   32   Berkeley
```

#### c. Đọc dữ liệu từ file ngoài (Đọc file CSV)

- Trong thực tế, dữ liệu thường được lưu trữ dưới dạng tệp như CSV hoặc excel, Pandas cung cấp hàm chuyên dụng `pd.read_csv()`.

```python
import pandas as pd

# doc file du lieu file csv
df = pd.read_csv('sales_data.csv')

# xem 5 dong dau tien cua DataFrame
print(df.head())

# xem 5 dong cuoi cung cua DataFrame
print(df.tail())
```

### 4. Truy cập và trích xuất dữ liệu từ DataFrame

- Sử dụng DataFrame mẫu:

```python
import pandas as pd

data = {
    'name': ['Krish', 'John', 'Jack'],
    'age': [25, 30, 45],
    'city': ['Bangalore', 'New York', 'Florida']
}

df = pd.DataFrame(data)
```

#### a. Truy cập theo cột

- Để lấy một cột cụ thể, ta truyền tên cột vào cặp dấu ngoặc vuông. Dữ liệu một cột trả về chính là một Series.

```python
print(df['name'])
print(type(df['name']))
```

- Kết quả:
```text
0    Krish
1     John
2     Jack
Name: name, dtype: object
<class 'pandas.core.series.Series'>
```

#### b. Truy cập theo hàng và vị trí (.loc và .iloc)

- `.loc` (label-based indexing): Dùng để truy cập theo nhãn của index.

```python
# lay hang co nhan index la 0
print(df.loc[0])
```

- Kết quả:
```text
name        Krish
age            25
city    Bangalore
Name: 0, dtype: object
```

- `.iloc` (Integer-location based indexing): Dùng để truy cập theo vị trí nguyên (tính từ 0):

```python
# Lay hang o vi tri 0
print(df.iloc[0])

# Lay phan tu tai hang vi tri 0, cot 1
print(df.iloc[0, 1])

# Lay phan tu hang 2, cot 2
print(df.iloc[2, 2])
```

- Kết quả:
```text
name        Krish
age            25
city    Bangalore
Name: 0, dtype: object

25

Florida
```

#### c. Truy cập giá trị đơn lẻ với hiệu năng cao (.at và .iat)

- Hai phương thức này được tối ưu để truy xuất giá trị của một ô đơn lẻ cực nhanh.

- `.at`: Dựa theo nhãn hàng và tên cột:

```python
# Lay gia tri cot 'age' tai hang 1
print(df.at[1, 'age'])

# Lay gia tri cot 'name' tai hang 2
print(df.at[2, 'name'])

# Output:
# 30
# 'Jack'
```

- `.iat`: Dựa trên tọa độ số nguyên của hàng và cột:

```python
# Lay vi tri tai hang 2, cot 2
print(df.iat[2, 2])

# Output:
# 'Florida'
```

### 5. Thao tác dữ liệu (Data Manipulation) với DataFrame

#### a. Thêm cột mới

- Gán một List giá trị tương đương với số lượng hàng hiện có.

```python
# Them cot luong 'salary'
df['salary'] = [50000, 60000, 70000]
print(df)
```

- Kết quả:
```text
    name  age       city  salary
0  Krish   25  Bangalore   50000
1   John   30   New York   60000
2   Jack   45    Florida   70000
```

#### b. Biến đổi dữ liệu trên cột

- Áp dụng phép tính số học trực tiếp lên toàn bộ cột.

```python
# Tang so tuoi cua tat ca cac ban ghi len 1
df['age'] = df['age'] + 1
print(df)
```

- Kết quả:
```text
    name  age       city  salary
0  Krish   26  Bangalore   50000
1   John   31   New York   60000
2   Jack   46    Florida   70000
```

#### c. Xóa cột hoặc hàng (.drop)

- Phương thức `.drop()` sử dụng tham số `axis` để định hướng trục thao tác:
  - `axis = 0` (mặc định): Thao tác trên hàng.
  - `axis = 1`: Thao tác trên cột.
- **Lưu ý về inplace**: Mặc định, `.drop()` chỉ trả về một bản sao mới mà không làm thay đổi DataFrame gốc. Muốn áp dụng thay đổi vĩnh viễn lên DataFrame hiện tại, bắt buộc phải truyền `inplace = True`.

- **Xóa một cột**:

```python
# Xoa cot 'salary' vinh vien
df.drop('salary', axis=1, inplace=True)
print(df)
```

- Kết quả:
```text
    name  age       city
0  Krish   26  Bangalore
1   John   31   New York
2   Jack   46    Florida
```

- **Xóa một hàng**:

```python
# Xoa hang co index 0 vinh vien
df.drop(0, axis=0, inplace=True)
print(df)
```

- Kết quả:
```text
   name  age      city
1  John   31  New York
2  Jack   46   Florida
```

### 6. Xem tóm tắt thống kê với .describe()

- Phương thức `.describe()` cung cấp bản tóm tắt phân tích thống kê mô tả nhanh chóng các cột chứa dữ liệu số.

```python
print(df.describe())
```

- Kết quả : 
```text
       age        salary
count   3.000000      3.000000
mean   34.000000  60000.000000
std    11.055416  10000.000000
min    25.000000  50000.000000
25%    27.500000  55000.000000
50%    30.000000  60000.000000
75%    37.500000  65000.000000
max    45.000000  70000.000000
```

- Bảng tóm tắt bao gồm:
  - `count`: Số lượng giá trị không rỗng (non-null).
  - `mean`: Giá trị trung bình.
  - `std`: Độ lệch chuẩn (standard deviation).
  - `min`: Giá trị nhỏ nhất.
  - `25%`, `50%` (trung vị - median), `75%`: Các phân vị.
  - `max`: Giá trị lớn nhất.
