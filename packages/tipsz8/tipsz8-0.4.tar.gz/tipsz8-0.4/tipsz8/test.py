from useFileHook import greet, saveLocalData, loadLocalData, clear_cache, getFileUTime
import time
from timeHook import timeStart,timeDay
def test():
    saveLocalData({"name": "Alice"}, "test.json")
    data = loadLocalData("test.json")
    print(data)
    
    print(getFileUTime("test.json"))
    # clear_cache("test.json")
    # data = loadLocalData("test.json")
    time.sleep(10)
    clear_cache("test.json")

def cb(*args, **kwargs):
    print("1")
# test()
def test_timeStart(): 
    timeDay(cb,"10:54:00","10:55:00","10:56:00")
   
test_timeStart()
