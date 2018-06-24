from flask import Flask,render_template,redirect,request,session,flash
import re
import pymysql
import datetime


app=Flask(__name__)

@app.route('/',methods=['GET'])
def index():
	return render_template("/hom2.html")



@app.route('/login', methods=['GET'])
def login():
	return render_template("login2.html")



if __name__ == "__main__":
    app.run(port=5000, debug=True)