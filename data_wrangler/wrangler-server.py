from flask import Flask, jsonify, request
import sqlite3
import json
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome. Data wrangler is running"

@app.route('/save_data',methods=['POST'])
def save_data():
    if request.method == 'POST':
        data=request.json['data']
        f2=open("/docker-flask/data/data.txt","a")
        f2.write("\n")
        f2.write(str(time.ctime(time.time())))
        f2.write("\n")
        f2.write(str(data))
        f2.write("\n")
        f2.write("\n")
        f2.close() 
        return "Data saved successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)