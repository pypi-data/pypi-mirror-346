from useFileHook import greet, saveLocalData, loadLocalData, clear_cache, getFileUTime
import time
def test():
    saveLocalData({"name": "Alice"}, "test.json")
    data = loadLocalData("test.json")
    print(data)
    
    print(getFileUTime("test.json"))
    # clear_cache("test.json")
    # data = loadLocalData("test.json")
    time.sleep(10)
    clear_cache("test.json")


test()