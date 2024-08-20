import psutil
import time

def monitor_all_processes(interval=2):
    seen_pids = set()

    i = 60
    while i:
        print("Monitoring all processes...")

        for proc in psutil.process_iter(['pid']):
            try:
                pid = proc.info['pid']

                if pid in seen_pids:
                    continue

                seen_pids.add(pid)

                with proc.oneshot():
                    cpu_usage = proc.cpu_percent(interval=0.1)
                    mem_info = proc.memory_info()
                    mem_usage = mem_info.rss / (1024 * 1024)  # Convert bytes to MB
                    print(f"PID: {pid:<5} | CPU: {cpu_usage:>5.2f}% | Memory: {mem_usage:>8.2f} MB | Name: {proc.name()}")

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        seen_pids = set()
        i -= 1
        print("=" * 40)
        time.sleep(interval)

if __name__ == "__main__":
    monitor_all_processes()
