import numpy as np
import pandas as pd

# doc file csv trong pandas
df = pd.read_csv('sales_data.csv')

# xem 10 dong dau tien cua DataFrame
print(df.head(10))

# xem 10 dong cuoi cung cua DataFrame
print(df.tail(10))

