from flask import Flask, render_template
from flask import jsonify
import random
import os
import linecache
import socket

# file definition
FILE = "mydata.txt"
rf = open(FILE, "w")
n = 1024

# write number inside the file
for i in range(n):
    line = str(random.uniform(-4096, 4096))  + "\n"
    rf.write(line)
rf.close()

# func to do the math operation
def math_operation(optype, x, y):
    try:
        if optype == "sum":
            return x + y
        elif optype == "rest":
            return x - y
        elif optype == "multiply":
            return x * y
        elif optype == "division":
            if y >= x:
                #raise ValueError('Error: Please, '+ str(y) + ' must be greater than ' + str(x) + ' in order to execute the math operation')
                return x / y
    except ZeroDivisionError:
        return 'Cannot divide by 0'

# func to find the numbers inside the file with the numbers of the lines from the url
def find_numbers(line1, line2):
    if os.path.exists(FILE):
        # read expecific lines
        line_numbers = [line1, line2]
        #print(line_numbers)
        lines = []
        for i in line_numbers:
            x = linecache.getline(FILE, i).strip()
            lines.append(float(x))
        return lines

#FLASK app definition
myapp = Flask(__name__)

# home
@myapp.route("/")
@myapp.route("/home")
def home():
    return render_template('index.html', mess=socket.gethostname())

# math operations page
@myapp.route("/operation", defaults={'optype': 'sum', 'line1': 1,'line2':1})
@myapp.route('/operation/<string:optype>/<int:line1>/<int:line2>/', methods = ['GET'])
def operation(optype, line1, line2):
    #read numbers from file with the lines
    lines = find_numbers(line1, line2)
    x = lines[0]
    y = lines[1] 

    # prepare the data to json
    data = {'linea1' : line1, 'linea2' : line2, 'valorLinea1' : x, 'valorLinea2' : y, 'result' : math_operation(optype, x, y)}
    response = jsonify(data) #Convert to json
    response.status_code = 200 #Set status code to 200=ok
    response.headers['Link'] = 'http://localhost'
    return response #return json response
    #verify the math operation
    print(math_operation(optype, x, y))


if __name__ == '__main__':
    myapp.run(debug=True, host='0.0.0.0')