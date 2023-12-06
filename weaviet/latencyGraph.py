import os
import numpy as np
import matplotlib.pyplot as plt

def read_and_plot_numpy_files(directory):

    size_latency = []
    # Read each file in the directory
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            # Parse the filename
            search_space = int(file[12:-4])


            # # Read numpy data from txt file
            data = np.loadtxt(os.path.join(directory, file))

            # # Calculate the average and append to list
            total = np.sum(data)
            size_latency.append([search_space, total])
    size_latency.sort()

    print(size_latency)
    x = [size for size,_ in size_latency]
    y = [time for _,time in size_latency]
    print(x)
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title('Weviet Performance (HNSW Index)', fontsize=30)
    plt.xlabel('DB Size (Search Space)', fontsize=15)
    plt.ylabel('10000 Queries Latency (s)', fontsize=15)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example usage
read_and_plot_numpy_files('runtime_old')
