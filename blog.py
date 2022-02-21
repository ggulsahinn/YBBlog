import re
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from flask_session import Session
from functools import wraps
from flask_ckeditor import CKEditor

cred = credentials.Certificate(
    "ybblog-506ca-firebase-adminsdk-rr5mm-4c893a30b7.json")
pb = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = "ybblog" # flash mesajları gözükmesi için
# app.config['SECRET_KEY'] = 'kmakmakma'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

#Kullanıcı Giriş Decorator'ı

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapınız.", "danger")
            return redirect(url_for("login"))
    return decorated_function

@app.route("/")
def index():
    users = db.collection("users")
    all_users = [doc.to_dict() for doc in users.stream()]
    print(len(all_users))
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
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
            "name": name,
            "username": username,
            "email": email,
            "password": password,
            "key": kayityolu.id,
            "date": datetime.now()
        })
        flash("Başarıyla kayıt oldunuz...", "success")
        # gitmek istediğin sayfanın fonksiyon adını ver
        return redirect(url_for("login"))
    kayit = db.collection("users")
    gelenveri = [doc.to_dict() for doc in kayit.stream()]
    return render_template("register.html", gelenveri=gelenveri)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        #form a girilen veriler alındı.
        username = request.form["username"]
        password = request.form["password"]
        
        #veri tabanından bütün kullanıcılar çekildi
        users = db.collection("users")
        all_users = [doc.to_dict() for doc in users.stream()]
        
        #veri tabanından gelen kullanıcılar kadar for döngüsü döndürülüp her kullanıcı x değerine atandı
        for x in all_users:
            #veritabanından gelen kullanıcılar arasında forma girilen kullanıcı adına sahip biri varmı kontrol edildi
            if username == x['username']:
                #kullanıcı adı mevcut ise parolası dbpassword değişkenine atandı
                dbpassword = x['password']
                
                #formdan gelen password ile kullanıcının veri tabanından gelen passwordu karşılaştırıldı
                if password == dbpassword:
                    #giriş başarılı ise session a username atandı
                    session["logged_in"] = True
                    session["username"] = username
                    flash("Başarıyla giriş yaptınız...", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Şifreniz yanlış...", "danger")
                    return redirect(url_for("login"))
            else:
                flash("Böyle bir kullanıcı bulunamadı...", "danger")
                return redirect(url_for("login"))

    return render_template('login.html', error=error)

@app.route("/addarticle", methods=["GET", "POST"])
def addarticle():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]
        kayityolu = db.collection("articles").document()
        kayityolu.set({
            "id": id,
            "title": title,
            "author": author,
            "content": content,
            "key": kayityolu.id,
            "date": datetime.now()
        })
        return redirect(url_for(addarticle))
    kayit = db.collection("articles")
    gelenveri = [doc.to_dict() for doc in kayit.stream()]
    return render_template("addarticle.html", gelenveri=gelenveri)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/_formhelpers", methods=["GET", "POST"])
def formhelpers():
    return render_template("_formhelpers.html")

if __name__ == "__main__":
    app.run(debug=True)
