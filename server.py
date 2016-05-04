from flask import Flask, render_template, redirect, request, session, flash
from flask import redirect


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/handle-login", methods=['POST'])
def handle_login():
    """Action for login form; log a user in."""

    email = request.form['email']
    password = request.form['password']

    if password == 'let-me-in':   # FIXME
        session['current_user'] = username
        flash("Logged in as %s" % username)
        return redirect("/")

    else:
        flash("Wrong password!")
        return redirect("/login")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()