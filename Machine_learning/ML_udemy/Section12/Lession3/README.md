# Data Manipulation with Pandas and Numpy

- Bài học này tập trung vào các kĩ thuật xử lí dữ liệu thực tế, kỹ thuật đặc trưng (Feature Engineering) và phân tích dữ liệu khám phá (Data Analysis - EDA) bằng thư viện Pandas. Chúng ta sẽ sử dụng một tập dữ liệu mẫu `data.csv` chứa nhiều giá trị bị khuyết để thực hành trực tiếp các thao tác: kiểm tra tổng quan, xử lí dữ liệu thiếu, biến đổi dữ liệu / đổi tên cột, gom nhóm tổng hợp (Groupby) và kết hợp dữ liệu (Merge / Join).

### 1. Kiểm tra tổng quan tập dữ liệu

- Trước hết, import thư viện pandas với bí danh `pd` để đọc dữ liệu `data.csv`:

```python
import pandas as pd

# đọc file dữ liệu csv
df = pd.read_csv('data.csv')
```

#### a. Xem đoạn đầu và cuối của bảng dữ liệu

- Tập dữ liệu bao gồm các trường thông tin: Date, Category, Product, Values, Sales, Region.

```python
# xem 5 hàng đầu tiên
print(df.head(5))

# xem 5 hàng cuối
print(df.tail(5))

# 5 là tham số có thể điều chỉnh tham số khác
```

#### b. Thống kê với df.describe()

```python
# in các thông kê
print(df.describe())
```

- Phương thức này tính toán trên các cột định lượng (numerical columns) là Value và Sales (các cột còn lại là Category, Product, Region là dạng phân loại nên bỏ qua). Bảng thống kê hiển thị count, mean, std, min, 25%, 50%, 75%, max.
- Kết quả:
```text

```

#### c. Kiểm tra hiển thị dữ liệu của các cột (.dtypes)

```python
print(df.dtypes)
```

- Kết quả:
  + Date: object (chuỗi văn bản - sau này trong các dự án nâng cao có thể chuyển sang kiểu datetime)
  + Category: object
  + Product: object
  + Value: float64
  + Sales: float64
  + Region: object

---

### 2. Xử lí dữ liệu bị thiếu (Missing Values)

- Trong thực tế, dữ liệu khuyết thiếu thường được biểu diễn dưới dạng NaN (Not a Number).

#### a. Phát hiện dữ liệu thiếu

- Kiểm tra từng ô với `.isnull()`:

```python
# trả về ma trận true false, True là ô bị thiếu
print(df.isnull())
```

- Kiểm tra sự tồn tại của giá trị thiếu:

```python
# Kiểm tra theo từng hàng axis = 1
# Hàng nào có ít nhất 1 ô bị thiếu sẽ trả về True
print(df.isnull().any(axis=1))

# Kiểm tra theo từng cột axis = 0 - mặc định
print(df.isnull().any(axis=0))
```

- Lưu ý: Tham số axis
  + Axis = 1 : Duyệt theo chiều ngang
  + Axis = 0 : Duyệt theo chiều dọc

- Đếm chính xác giá trị bị thiếu trên mỗi cột: `.sum()`

```python
print(df.isnull().sum())
```

#### b. Điền dữ liệu thiếu (Imputation)

**Cách 1: Điền bằng 1 hằng số**
- Ví dụ điền số 0:

```python
# điền số 0 vào tất cả ô thiếu
# thao tác này có thể gán sang DataFrame mới hoặc bản sao
df_filled_zero = df.fillna(0)
```

- Lưu ý: Với dữ liệu số, việc điền số 0 vào toàn bộ các trường thường không tối ưu vì làm sai lệch phân phối dữ liệu.

**Cách 2: Điền bằng giá trị trung bình (mean imputation)**
- Thay thế các vị trí NaN trong một cột giá trị trung bình (.mean()) của chính cột đó:

```python
# Tạo một cột mới 'Sales_fillna' được điền giá trị trung bình vào các ô trống của cột 'Sales'
df['Sales_fillna'] = df['Sales'].fillna(df['Sales'].mean())
# print(df.head(5))
```

- Tại các hàng ban đầu chứa NaN, giá trị bây giờ được lấp đầy bằng giá trị trung bình của cột Sales.

---

### 3. Thao tác biến đổi cột và kiểu dữ liệu

#### a. Đổi tên cột (.rename())

- Khi đổi tên cột, bắt buộc phải truyền vào một dictionary ánh xạ {tên cũ: tên mới} thông qua tham số columns:

```python
# đổi tên cột 'Date' thành 'Sales_date'
df = df.rename(columns={'Date': 'Sales_date'})
print(df.head())
```

- Kết quả:
```text

```

#### b. Ép kiểu dữ liệu (.astype())

- Giả sử ta muốn chuyển đổi cột giá trị từ kiểu số thực (float64) sang số nguyên (int):
- Lưu ý then chốt: Pandas không thể ép kiểu một cột chứa giá trị NaN sang kiểu int trực tiếp. Cần phải điền hết các giá trị thiếu trước khi gọi `.astype(int)`:

```python
# Tạo cột 'value_new' điền các ô thiếu trong 'Value' bằng mean
# Sau đó ép sang kiểu int
df['value_new'] = df['Value'].fillna(df['Value'].mean()).astype(int)

print(df.head())
```

- Kết quả:
```text

```

#### c. Áp dụng hàm lên cột với .apply() và biểu thức lambda

- Để thực hiện các phép biến đổi tùy biến hoặc áp dụng các logic kỹ thuật đặc trưng lên từng phần tử của cột, ta dùng `.apply()`:

```python
# Tạo cột 'Value_doubled' bằng cách nhân đôi giá trị của cột số Value bằng hàm lambda
df['Value_doubled'] = df['Value'].apply(lambda x: x * 2)

print(df.head())
```

- Tất cả các giá trị ban đầu (như 28) đã được nhân đôi thành 56, 78 thành 156,.... Ngoài lambda, bạn có thể dùng định nghĩa bất kì hàm tùy chỉnh (Custom function) nào rồi truyền tên hàm vào `.apply()`.

---

### 4. Gom nhóm và tổng hợp dữ liệu (Aggregation & Group By)

- Tương tự như lệnh Group By trong SQL, Pandas cung cấp phương thức `groupby()` để gom nhóm dữ liệu theo các biến phân loại.

#### a. Gom nhóm theo một biến phân loại

```python
# gom nhóm theo 'Product' và tính giá trị trung bình của cột 'Value'
grouped_mean = df.groupby('Product')['Value'].mean()
print(grouped_mean)

# output tương ứng giá trị trung bình của từng Product:
```

- Kết quả:
```text

```

#### b. Gom nhóm theo nhiều biến phân loại (Multi-column GroupBy)

- Truyền danh sách các cột cần gom nhóm vào `.groupby()`
- Tính tổng theo sản phẩm và khu vực:

```python
# gom nhóm theo ['Product', 'Region'] và tính tổng cột 'Value'
grouped_sum = df.groupby(['Product', 'Region'])['Value'].sum()

print(grouped_sum)
# Tổng value của từng khu vực East, North, South, West thuộc từng Product
```

- Kết quả:
```text

```

- Tính trung bình theo sản phẩm và khu vực:

```python
grouped_mean_multi = df.groupby(['Product', 'Region'])['Value'].mean()

print(grouped_mean_multi)
```

- Kết quả:
```text

```

#### c. Áp dụng đồng thời nhiều hàm tổng hợp (.agg())

- Muốn tính toán nhiều chỉ số thống kê (như mean, sum, count) cùng một lúc trên một nhóm, ta dùng phương thức `.agg()` và truyền vào danh sách các tên hàm:

```python
# gom nhóm theo 'Region'
# Lấy cột 'Value' với tính đồng thời mean, sum, count
grouped_agg = df.groupby('Region')['Value'].agg(['mean', 'sum', 'count'])

print(grouped_agg)
```

- Kết quả:
```text

```

---

### 5. Hợp nhất và nối các DataFrame (Merge & Join)

- Để kết hợp dữ liệu từ hai DataFrame dựa trên một hoặc nhiều cột khóa (Key), ta dùng hàm `pd.merge()`.
- Cú pháp:
```python
pd.merge(df1, df2, on='Key', how='kiểu_kết_nối')
```

- Khởi tạo 2 DataFrame mẫu:

```python
import pandas as pd

df1 = pd.DataFrame({
    'Key': ['A', 'B', 'C'],
    'Value1': [1, 2, 3]
})

df2 = pd.DataFrame({
    'Key': ['A', 'B', 'D'],
    'Value2': [4, 5, 6]
})

print(df1)
print(df2)
```

- Kết quả:
```text

```

#### a. Dùng phép nối trong (Inner Join): how = 'inner'

- Chỉ giữ lại các bản ghi có khóa xuất hiện đồng thời ở cả 2 DataFrame (Giao của 2 tập hợp).

```python
merged_inner = pd.merge(df1, df2, on='Key', how='inner')

print(merged_inner)
```

- Kết quả:
```text
  Key  Value1  Value2
0   A       1       4
1   B       2       5
```

#### b. Phép nối ngoài toàn phần (Outer Join): how = 'outer'

- Lấy toàn bộ các khóa từ cả 2 DataFrame (Hợp của 2 tập hợp). Vị trí nào bên kia không có dữ liệu thì tự động điền NaN.

```python
merged_outer = pd.merge(df1, df2, on='Key', how='outer')

print(merged_outer)
```

- Kết quả:
```text
  Key  Value1  Value2
0   A     1.0     4.0
1   B     2.0     5.0
2   C     3.0     NaN
3   D     NaN     6.0
```

- Khóa 'C' không có ở df2 nên Value2 mang giá trị NaN, khóa 'D' cũng không có ở df1 nên Value1 mang giá trị NaN.

#### c. Phép nối ngoài bên trái (Left Join): how = 'left'

- Ưu tiên giữ lại toàn bộ các khóa của DataFrame bên trái (df1). Nếu df2 không có khóa tương ứng thì điền NaN.

```python
merged_left = pd.merge(df1, df2, on='Key', how='left')

print(merged_left)
```

- Kết quả:
```text
  Key  Value1  Value2
0   A       1     4.0
1   B       2     5.0
2   C       3     NaN
```

#### d. Phép nối ngoài bên phải (Right Join): how = 'right'

- Ưu tiên giữ lại toàn bộ các khóa của DataFrame bên phải df2. Nếu df1 không có khóa tương ứng thì điền NaN.

```python
merged_right = pd.merge(df1, df2, on='Key', how='right')

print(merged_right)
```

- Kết quả:
```text
  Key  Value1  Value2
0   A     1.0       4
1   B     2.0       5
2   D     NaN       6
```