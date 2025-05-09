import os
import json
import time
import requests
def greet(name):
    return f"Hello, {name}!"

def saveLocalData(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    except requests.exceptions.RequestException as e:
        print(f"save{filename}失败: {e}")
        return False

def loadLocalData(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                cached_data = json.load(f)
                if cached_data:  # 如果缓存数据存在，直接返回
                    return cached_data
            except json.JSONDecodeError:
                # pass  # 如果缓存文件损坏，忽略并重新获取数据 
                return False
    else:
        return False

def clear_cache(filename):
    if os.path.exists(filename):
        os.remove(filename)
    print(f"{filename}缓存已清理")
    # else:
    #     print(f"{filename} cache不存在")

def getFileUTime(filename):
    if os.path.exists(filename):
        file_mod_time = time.localtime(os.path.getmtime(filename))
        today = time.localtime()
        if file_mod_time.tm_year == today.tm_year and file_mod_time.tm_yday == today.tm_yday:
            print(f"{filename} is up to date")
            return True
            
        else:
            clear_cache(filename)
            print(f"{filename} is outdated")
            return False
    else:
        print(f"{filename}文件不存在")
        return False
