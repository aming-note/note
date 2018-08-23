#coding:utf8
import psutil,platform

class physical_info():
    os_type = platform.system()
    os_info = platform.version()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_version = platform.processor()
    if os_type == 'Windows':
        mem_total = "%.2f" % (psutil.virtual_memory().total /1024 /1024 /1024)
        mem_used = "%.2f" % (psutil.virtual_memory().used /1024 /1024 /1024)
        mem_free = "%.2f" % (psutil.virtual_memory().free /1024 /1024 /1024)
        swap_total = "%.2f" % (psutil.swap_memory().total /1024 /1024 /1024)
        swap_used = "%.2f" % (psutil.swap_memory().used /1024 /1024 /1024)
        swap_free = "%.2f" % (psutil.swap_memory().free /1024 /1024 /1024)
    elif os_type == 'Linux':
        mem_total = psutil.virtual_memory().total / 1024 / 1024
        mem_used = psutil.virtual_memory().used / 1024 / 1024
        mem_free = psutil.virtual_memory().free / 1024 / 1024
        swap_total = psutil.swap_memory().total / 1024 / 1024
        swap_used = psutil.swap_memory().used / 1024 / 1024
        swap_free = psutil.swap_memory().free / 1024 / 1024