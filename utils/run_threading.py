import threading as mp


def start_threading(active_processes):
    for processes in active_processes:
        date = mp.Thread(target=processes["target"], args=processes["args"])
        date.start()
