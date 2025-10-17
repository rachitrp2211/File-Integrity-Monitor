import os
import time
import random

# Folder to test — make sure it matches your config.yaml
FOLDER = "C:/Users/patel/OneDrive/Desktop/fim_test"

# Ensure the folder exists
os.makedirs(FOLDER, exist_ok=True)

file_counter = 1

try:
    while True:
        action = random.choice(["create", "modify", "delete"])
        file_name = f"stress_file_{random.randint(1, 5)}.txt"
        file_path = os.path.join(FOLDER, file_name)

        if action == "create":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Created {file_name}\n")
            print(f"Created: {file_path}")

        elif action == "modify" and os.path.exists(file_path):
            with open(file_path, "a", encoding="utf-8") as f:
                f.write("Appending some random content...\n")
            print(f"Modified: {file_path}")

        elif action == "delete" and os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        time.sleep(random.randint(1, 3))  # wait 1-3 seconds before next action

except KeyboardInterrupt:
    print("\nStress test stopped.")
