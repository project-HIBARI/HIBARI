from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector



app = Flask(__name__)
app.secret_key = "qawsedrftgyhujikolp"



############################################################################
### 関数の定義
############################################################################

# db接続用関数
def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        db="dbname",
        charset="utf8"
    )
    return conn


############################################################################
### パスの定義
############################################################################

# TOP
@app.route('/')
def index():
    return render_template("index.html")



############################################################################
### 実行制御
############################################################################
if __name__ == "__main__":
    app.run(debug=True)