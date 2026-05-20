import os

from flask import Flask, render_template
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import text



load_dotenv()
app = Flask(__name__)
app.secret_key = "qawsedrftgyhujikolp"

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)



############################################################################
### 関数
############################################################################

# SQL実行関数
def execute_query(sql, params=None):
    with engine.connect() as conn:

        result = conn.execute(
            text(sql),
            params or {}
        )

        return result
    

############################################################################
### パス
############################################################################

@app.route('/')
def index():

    result = execute_query("""
        SELECT *
        FROM accounts
    """)

    users = result.fetchall()
    print(users)

    return render_template(
        "index.html",
        users=users
    )


############################################################################
### 実行制御
############################################################################
if __name__ == "__main__":
    app.run(debug=True)
