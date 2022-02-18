from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate(
    "ybblog-506ca-firebase-adminsdk-rr5mm-4c893a30b7.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = "ybblog"  # flash mesajları gözükmesi için
#app.config['SECRET_KEY'] = 'kmakmakma'

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
    return render_template("index.html")

    # articles = [
    #     {"id":1 , "title":"Deneme1", "content":"Deneme1 içerik"},
    #     {"id":2 , "title":"Deneme2", "content":"Deneme2 içerik"},
    #     {"id":3 , "title":"Deneme3", "content":"Deneme3 içerik"}]
    # return render_template("index.html",articles=articles)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/article/<string:id>")  # Dinamik URL
def detail(id):
    return "Article Id: "+id



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        kayityolu = db.collection("users").document()
        kayityolu.set({
            "name":name,
            "username":username,
            "email":email,
            "password":password,
            "key":kayityolu.id,
            "date":datetime.now()
        })
        flash("Başarıyla kayıt oldunuz...", "success")    
        return redirect(url_for("login")) #gitmek istediğin sayfanın fonksiyon adını ver
    kayityolu = db.collection("users")
    gelenveri = [doc.to_dict() for doc in kayityolu.stream()]
    return render_template("register.html", gelenveri=gelenveri)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        kayityolu = db.collection("login").document()
        kayityolu.set({
            "username":username,
            "password":password,
            "key":kayityolu.id,
            "date":datetime.now()
        })
        result=len(kayityolu["username"])
        if result>0:
            data = kayityolu.fetchone()
            if data["password"]==kayityolu["password"]:
                flash("Giriş Yapıldı", "success")
                
                session["logged_in"] = True
                session["username"] = username
                                
                return redirect(url_for("index"))
            else:
                flash("Parola hatalı", "danger")
                return redirect(url_for("login"))
            
        else:
            flash("Böyle bir kullanıcı bulunmuyor!", "danger")
            return redirect(url_for("login"))
    kayityolu = db.collection("login")
    gelenveri = [doc.to_dict() for doc in kayityolu.stream()]
    return render_template("login.html", gelenveri=gelenveri)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))







if __name__ == "__main__":
    app.run(debug=True)
