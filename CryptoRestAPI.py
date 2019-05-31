import random
# For REST API
from flask import Flask
from flask import request
import threading
from sortedcontainers import SortedList

# sl = Global Container variable to store accumulated int array from multiple clients
sl = SortedList()

# To protect global variable sl from data racing
sl_lock = threading.Lock()

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Provide the End point you want [clean_array, get_array, add_value]!"


@app.route('/clean_array', methods=['GET', 'DELETE'])
def clean_current_array():
    if request.method == 'DELETE':
        print('DEBUG: clean_array() called with DELETE')
    else:
        print("DEBUG: clean_array() GET method was called")

    # lock acquired by web client
    sl_lock.acquire()
    sl.clear()
    print(f"REST API Server [EndPoint = clean_array] : Cleansed int array, New Size: {len(sl)}, New Array: {sl}")
    # Release lock
    sl_lock.release()

    return f"REST API Server [EndPoint = clean_array] : Cleansed int array, New Size: {len(sl)}, New Array: {sl}"


@app.route('/get_array', methods=['GET'])
def get_current_array():
    print('REST API Server[EndPoint = get_array] : Return sorted array in Server, Size:', len(sl), 'Array:', sl)
    return f"REST API Server[EndPoint = get_array] response : Array Size: {len(sl)}, Array: {sl}"


@app.route('/add_value', methods=['GET', 'POST'])
def add_value():
    if request.method == 'POST':
        print('DEBUG: add_value() called with POST')
    else:
        print("DEBUG: add_value() GET method was called")

    random_int = random.randint(1000, 10000)

    # lock acquired by web client
    sl_lock.acquire()

    print('REST API Server[EndPoint = add_value] : Adding random integer:', random_int, 'in array, Old Size:', len(sl), 'Old Array:', sl)
    sl.add(random_int)

    print(f"REST API Server[EndPoint = add_value] : Added random integer: {random_int} in array, New Size: {len(sl)}, New Array: {sl}")
    tmpStr = f"REST API Server[EndPoint = add_value] response : Added random integer: {random_int}, New Size: {len(sl)}, New Array: {sl}"

    # Release lock
    sl_lock.release()

    return tmpStr

