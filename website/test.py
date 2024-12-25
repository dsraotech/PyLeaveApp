import time

# Example usage
for i in range(10):
    print(f"Progress: {i+1}/10", end='\r', flush=True)
    time.sleep(1)
