from flask import Flask
from flask import redirect, render_template, session, url_for
from forms import LoginForm, RegisterUserForm
from api_request import access, create_user, get_current_user
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        auth = access(**form.data)
        auth.store_in_session()
        user = get_current_user()
        user.store_in_session()
        return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = create_user(**form.data)
        user.store_in_session()
        auth = access(**form.data)
        auth.store_in_session()
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run()