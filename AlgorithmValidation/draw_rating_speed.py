import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv('rating_minimize_testcase.csv')
# df = pd.read_csv('rating_create_testcase.csv')

# Sắp xếp dữ liệu theo số state tăng dần
df_sorted = df.sort_values('Number of states')

# Tính thời gian trung bình cho số state chạy được trong một đơn vị thời gian (ví dụ: giây)
df_sorted['Average states'] = df_sorted['Number of states'] / df_sorted['Execution time']
average_states = df_sorted['Average states'].mean()

# Vẽ biểu đồ đường
plt.plot(df_sorted['Number of states'], df_sorted['Execution time'], marker='o', linestyle='-',color="#ff7f0e")
plt.xlabel('Number of states (states)', fontsize=12)
plt.ylabel('Execution time (s)', fontsize=12)
plt.title('Speed of Minimize state table Algorithm', fontsize=14)

# Hiển thị thời gian trung bình trên biểu đồ
plt.text(0.5, 0.95, f'Speed Algorithm: {average_states:.2f} states/s', transform=plt.gca().transAxes,
         color='#2ca02c', fontsize=14, va="top", ha="center")

# Tăng kích thước các chữ trong biểu đồ
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.show()
