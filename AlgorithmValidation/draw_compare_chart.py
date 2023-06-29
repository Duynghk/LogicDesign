import pandas as pd
import matplotlib.pyplot as plt

# File path to the CSV file
file_path = "Compare.csv"

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Get data
minimized_column = data["Number of minimized states"]
to_minimize_column = data["Number of states to minimize"]

# Calculate the similarity based on the percentage
similarity = (minimized_column == to_minimize_column).mean() * 100

# Plot the chart
plt.plot(minimized_column, label="Minimized states", color="lime")
plt.plot(to_minimize_column, label="States to minimize", color="#ff7f0e")
plt.xlabel("File", fontsize=14)
plt.ylabel("Number of States", fontsize=14)
plt.title("Comparison of the result of two Algorithm", fontsize=16)
plt.legend()

# Print the similarity on the chart
plt.text(0.5, 0.92, f"Similarity: {similarity:.2f}%", ha='center', va='center', transform=plt.gca().transAxes, color="#2ca02c", fontsize=14)
plt.show()
