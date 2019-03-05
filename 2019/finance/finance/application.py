import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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

    userId = session.get('user_id')
    # get information from shares sheet
    shares = db.execute("SELECT symbol, shares FROM shares WHERE userId=:userId ORDER BY symbol", userId=userId)
    # get information on user
    user = db.execute("SELECT * FROM users WHERE id=:id", id=userId)

    # display current price for each stock
    indPrice = list()
    totalPrice = list()
    for share in shares:
        sPrice = lookup(share['symbol'])['price']
        indPrice.append(sPrice)
        totalPrice.append(sPrice * int(share['shares']))
    sv = 0
    for price in totalPrice:
        sv += price
    cash = round(user[0]['cash'], 2)
    grand = sv + cash
    return render_template("index.html", userId=userId, shares=shares, user=user, indPrice=indPrice, totalPrice=totalPrice, cash=cash, sv=sv, grand=grand)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'POST':
        # ensure stock symbol is submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        #ensure number of shares submitted, and more than 0
        elif not request.form.get("shares") or int(request.form.get("shares")) <= 0:
            return apology("must provide positive amount of shares")

        quote = lookup(request.form.get("symbol"))
        row = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        # Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price.
        cash = row[0]['cash']
        total = quote['price'] * int(request.form.get("shares"))

        if cash < total:
            return apology("you're not rich enough", 403)

        db.execute("UPDATE users SET cash = :total WHERE id = :id", total=cash - total, id=session.get('user_id'))
        db.execute("INSERT INTO transactions (userId, stock, price, total, shares, type) VALUES (:userId, :stock, :price, :total, :shares, 1)", userId=session.get('user_id'), stock=quote['symbol'], price=quote['price'], total=total, shares=int(request.form.get("shares")))
        sharesRow = db.execute("SELECT * FROM shares WHERE userId=:userId AND symbol=:symbol", userId=session.get('user_id'), symbol=request.form.get("symbol"))
        if not sharesRow:
            db.execute("INSERT INTO shares (userId, symbol, shares) VALUES (:userId, :symbol, :shares)", userId=session.get('user_id'), symbol=quote['symbol'], shares=request.form.get("shares"))
        else:
            db.execute("UPDATE shares SET shares=:shares WHERE userId=:userId AND symbol=:symbol", shares=sharesRow[0]['shares'] + int(request.form.get("shares")), userId=session.get('user_id'), symbol=request.form.get("symbol"))
    return render_template("buy.html")



@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # The route should accept, via GET, an HTTP parameter called username.
    username = request.args.get("username")
    taken = db.execute("SELECT username FROM users WHERE username=:username", username=username)
    if (len(username) > 0) and (not taken):
        return jsonify(True)
    else:
        return jsonify(False)
    # If the value of username is of length at least 1 and does not already belong to a user in the database, the route should return, in JSON format, true, signifying that the username is (as of that moment) available. Else it should return, in JSON format, false. Recall that jsonify in Flask can return a value in JSON format.

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get all transactions from the table (overriding the codes with the proper names)
    history = db.execute("SELECT time, stock, price, total, shares, name FROM transactions JOIN tra_enum ON transactions.type=tra_enum.type ORDER BY time DESC")
    print(history)
    # append an additional tag 'b' for buy and 's' for sell

    return render_template("history.html", history=history)


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
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Please enter valid symbol", 400)
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password matches with confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password do not match with confirmation")

        #INSERT the new user into users, storing a hash of the user’s password, not the password itself. Hash the user’s password with generate_password_hash.
        # http://werkzeug.pocoo.org/docs/0.14/utils/#werkzeug.security.generate_password_hash
        if(db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))):
            return render_template('login.html'), 200
        else:
            return render_template('register.html'), 400
    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == 'POST':
        # ensure stock symbol is submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        #ensure number of shares submitted, and more than 0
        elif not request.form.get("shares") or int(request.form.get("shares")) <= 0:
            return apology("must provide positive amount of shares")

        quote = lookup(request.form.get("symbol"))
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        sharesRow = db.execute("SELECT * FROM shares WHERE userId=:userId AND symbol=:symbol", userId=session.get('user_id'), symbol=request.form.get("symbol"))

        # Render an apology, without completing a sales, if the user does not have enough share to sell

        salesQty = int(request.form.get("shares"))
        owned = int(sharesRow[0]['shares'])
        if salesQty > owned:
            return apology("you don't have enough shares to sell (lol)", 403)

        total = quote['price'] * int(request.form.get("shares"))
        db.execute("UPDATE users SET cash = :total WHERE id = :id", total=total + row[0]['cash'], id=session.get('user_id'))
        db.execute("INSERT INTO transactions (userId, stock, price, total, shares, type) VALUES (:userId, :stock, :price, :total, :shares, 2)", userId=session.get('user_id'), stock=quote['symbol'], price=quote['price'], total=total, shares=int(request.form.get("shares")))
        db.execute("UPDATE shares SET shares=:shares WHERE userId=:userId AND symbol=:symbol", shares=sharesRow[0]['shares'] - salesQty, userId=session.get('user_id'), symbol=request.form.get("symbol"))
    return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
