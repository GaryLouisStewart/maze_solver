import time
from maze import Maze
import matplotlib.pyplot as plt

test_sizes = [5, 10, 50, 100, 200, 500]
execution_times = []

def main():
    for size in test_sizes:
        start_time = time.time()
        m = Maze(0, 0, size, size, 10, 10, seed=0)
        execution_time = time.time() - start_time
        execution_times.append(execution_time)
        print(f"Maze of size {size}x{size} generate in {execution_time:.6f} seconds")

    plt.plot(test_sizes, execution_times)
    plt.xlabel('Maze Size (NxN)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('maze Generation Performance')
    plt.show()

if __name__ == '__main__':
    main()
