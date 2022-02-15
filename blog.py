from sqlite3 import Cursor
from sre_constants import SUCCESS
from click import confirm
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#Kulllanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("Ad Soyad", validators=[validators.Length(min=4,max=25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5,max=35)])
    email = StringField("Email Adresi", validators=[validators.Email(message="Lütfen geçerli bir email giriniz.")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola giriniz."),
        validators.EqualTo(fieldname="confirm", message="Parolanız uyuşmuyor!")
    ])
    confirm = PasswordField("Parola Doğrula")

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
    return render_template("about.html") 

@app.route("/article/<string:id>") #Dinamik URL
def detail(id):
    return "Article Id: "+id

#Kayıt olma
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method=="POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        confirm = form.confirm.data
        
        cursor = mysql.connection.cursor()        
        sorgu = "Insert into users(name,username,email,password) VALUES(%s, %s, %s, %s)"
        cursor.execute(sorgu,(name,username,email,password))
        mysql.connection.commit()
        cursor.close()
        
        flash("Başarıyla kayıt oldunuz...", SUCCESS)
        
        return redirect(url_for("index")) #gitmek istediğin sayfanın fonksiyon adını ver
    else :
        return render_template("register.html", form=form)





if __name__ == "__main__":
    app.run(debug=True)