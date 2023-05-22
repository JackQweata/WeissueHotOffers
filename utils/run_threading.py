import threading as mp


def start_threading(date):
    thread = mp.Thread(target=date["target"], args=date.get("args"), name=date['name'])
    thread.start()
    return thread
