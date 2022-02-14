from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import From,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config["MYSQL_HOST"] =  "localhost"
app.config["MYSQL_USER"] =  "root"
app.config["MYSQL_PASSWORD"] =  ""
app.config["MYSQL_DB"] =  "ybblog"
app.config["MYSQL_CURSORCLASS"] =  "DictCursor"

mysql = MySQL(app)

""" 
@app.route("/")
def index():
    
    sayi=10
    sayi2=20
    return render_template("index.html",number=sayi,number2=sayi2)
    
    article = dict()
    article["title"] = "Deneme"
    article["body"] = "Deneme 123"
    article["author"] = "Gülşah"
    return render_template("index.html",article=article)
"""

@app.route("/")
def index():
    articles = [
        {"id":1 , "title":"Deneme1", "content":"Deneme1 içerik"},
        {"id":2 , "title":"Deneme2", "content":"Deneme2 içerik"},
        {"id":3 , "title":"Deneme3", "content":"Deneme3 içerik"}
    ]
    
    return render_template("index.html",articles=articles)

@app.route("/about")
def about():
    return render_template("about.html") #Dinamik URL

@app.route("/article/<string:id>")
def detail(id):
    return "Article Id: "+id



if __name__ == "__main__":
    app.run(debug=True)