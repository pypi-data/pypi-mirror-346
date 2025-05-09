from useFileHook import greet, saveLocalData, loadLocalData, clear_cache, getFileUTime
import time
from timeHook import timeStart
def test():
    saveLocalData({"name": "Alice"}, "test.json")
    data = loadLocalData("test.json")
    print(data)
    
    print(getFileUTime("test.json"))
    # clear_cache("test.json")
    # data = loadLocalData("test.json")
    time.sleep(10)
    clear_cache("test.json")


# test()
def test_timeStart():
    def cb(*args, **kwargs):
        print("1")
    timeStart(cb,"9:40:00-11:40:00",h=1)
test_timeStart()