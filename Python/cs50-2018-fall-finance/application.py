import os
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    total = 0
    account_info = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session.get("user_id"))
    purchase_info = db.execute("SELECT * FROM purchaseHistory WHERE username = :user_name",
                          user_name=account_info[0]['username'])
    for item in purchase_info:
        db.execute(f"UPDATE purchaseHistory SET price ='{lookup(item['symbol'])['price']}' WHERE id = :purchase_id",
                          purchase_id=item['id'])
        total += db.execute("SELECT price FROM purchaseHistory WHERE id = :purchase_id", purchase_id=item['id'])[0]['price'] * item['amount']
    purchase_info = db.execute("SELECT * FROM purchaseHistory WHERE username = :user_name",
                          user_name=account_info[0]['username'])

    return render_template("index.html", table=purchase_info, info=account_info[0], total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        sym = request.form.get("symbol")
        info = lookup(sym)
        shares = int(request.form.get("shares"))
        curentDT = datetime.now()


        if not sym or not info['symbol']:
            return apology("please, enter right stocks` symbol")
        if shares < 0:
            return apology("please, enter positive number to buy")

        cash = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session.get("user_id"))

        if cash[0]['cash'] < shares * info['price']:
            return apology("sorry, you don't have enough money")
        purchase_id = db.execute("SELECT id FROM purchaseHistory WHERE username = :user_name AND symbol = :symb",
                        user_name=cash[0]['username'], symb=sym)

        if purchase_id:
            db.execute(f"UPDATE purchaseHistory SET amount = amount + {shares}, price = '{info['price']}' WHERE id = :id",
                          id=purchase_id[0]['id'])
        else:
            db.execute(f"INSERT INTO purchaseHistory ('id','username','symbol','amount','price') VALUES (NULL,'{cash[0]['username']}','{sym}','{shares}','{info['price']}')")

        db.execute(f"INSERT INTO history ('id','username','symbol','amount','price','action','time','date') VALUES (NULL,'{cash[0]['username']}','{sym}','{shares}','{info['price']}','BUY','{3 + curentDT.hour}:{curentDT.minute}:{curentDT.second}','{curentDT.day}.{curentDT.month}.{curentDT.year}')")
        db.execute(f"UPDATE users SET cash ='{cash[0]['cash'] - shares * info['price']}' WHERE id = :user_id",
                          user_id=session.get("user_id"))
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format
    user = request.form.get("username")
    if len(username) < 2 or db.execute("SELECT username FROM users WHERE username = :user", user = user)
        return jsonify(false)
    else
        return jsonify(true)"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_name = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session.get("user_id"))[0]['username']
    table = db.execute("SELECT * FROM history WHERE username = :user_id",
                          user_id=user_name)
    return render_template("history.html", table=table)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        if not info:
            return apology("please, enter right stocks` symbol")
        return render_template("quoted.html", info = info)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        """Register user"""
        if not name:
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        if db.execute("SELECT * FROM users WHERE username = :username", username = name):
            return apology("username already exists", 403)
        if password != request.form.get("repeat"):
            return apology("Sorry, passwords do not match", 403)

        db.execute(f"INSERT INTO users(id, username, hash) VALUES(NULL,'{name}', '{hash}')")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/", 302)
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        sym = request.form.get("symbol")
        info = lookup(sym)
        shares = int(request.form.get("shares"))
        curentDT = datetime.now()

        user = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session.get("user_id"))[0]

        sell = db.execute("SELECT * FROM purchaseHistory WHERE username = :user_name AND symbol = :symb",
                            user_name=user['username'], symb=sym)[0]

        if shares < 0 or shares > sell['amount']:
            return apology("please, enter relevant number for selling")

        db.execute(f"UPDATE purchaseHistory SET amount = amount-{shares} WHERE username = :user_name AND symbol = :symb",
                            user_name=user['username'], symb=sym)
        db.execute(f"UPDATE users SET cash = cash + ({shares} * {info['price']}) WHERE id = :user_id",
                          user_id=session.get("user_id"))
        db.execute(f"INSERT INTO history ('id','username','symbol','amount','price','action','time','date') VALUES (NULL,'{user['username']}','{sym}','{shares}','{info['price']}','SELL','{3 + curentDT.hour}:{curentDT.minute}:{curentDT.second}','{curentDT.day}.{curentDT.month}.{curentDT.year}')")
        return redirect("/")
    else:
        user_name = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session.get("user_id"))[0]['username']
        table = db.execute("SELECT symbol FROM purchaseHistory WHERE username = :username", username=user_name)
        return render_template("sell.html", table=table)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
