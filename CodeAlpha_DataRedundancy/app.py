import pandas as pd

# Step 1: Read data from CSV
data = pd.read_csv("data.csv")

print("📂 Original Data:")
print(data)

# Step 2: Remove duplicates based on Email
cleaned_data = data.drop_duplicates(subset=["Email"])

print("\n✅ Cleaned Data (Duplicates removed based on Email):")
print(cleaned_data)

# Step 3: Save cleaned data to new file
cleaned_data.to_csv("cleaned_data.csv", index=False)

print("\n🎉 Done! Clean data saved in cleaned_data.csv")