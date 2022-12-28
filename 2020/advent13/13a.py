import sys

start = int(sys.stdin.readline())
buses = [int(c) for c in sys.stdin.readline().split(",") if c != "x"]

def wait_time(b):
    return b - (start % b)

bus = min(buses, key=wait_time)
print(bus * wait_time(bus))