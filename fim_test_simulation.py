import os
import time

# Folder to test — make sure it matches your config.yaml
FOLDER = "C:/Users/patel/OneDrive/Desktop/fim_test"

# Ensure the folder exists
os.makedirs(FOLDER, exist_ok=True)

# 1️⃣ Create files
for i in range(1, 4):
    file_path = os.path.join(FOLDER, f"test_file_{i}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"This is test file {i}\n")
    print(f"Created: {file_path}")
    time.sleep(1)

# 2️⃣ Modify files
for i in range(1, 4):
    file_path = os.path.join(FOLDER, f"test_file_{i}.txt")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("Appending some new content...\n")
    print(f"Modified: {file_path}")
    time.sleep(1)

# 3️⃣ Delete files
for i in range(1, 4):
    file_path = os.path.join(FOLDER, f"test_file_{i}.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    time.sleep(1)

print("Simulation complete! Check your FIM logs and email alerts.")
