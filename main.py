# imports
from flask import Flask, render_template, request, session, redirect, url_for, flash, copy_current_request_context
from DB_administration import *
from Notification import *
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import functools
import operator
import threading
import math

# server config
app = Flask(__name__)
app.secret_key = "secret"
csrf = CSRFProtect(app)


# manejo de errores
@app.errorhandler(404)
def pageNotFound(e):
    return redirect(url_for('ForWeb', id=1))


# ruta principal
@app.route("/")
def home():
    return render_template("login.html")


# cerrar sesion
@app.route("/Logout")
def Logout():
    session.pop('username')
    passed = "You logout successfully!"
    flash(passed)
    return render_template("login.html")


# sub ruta inicio sesion
@app.route("/inicio")
def inicio():
    return render_template("login.html")


# sub ruta registro
@app.route("/register")
def register():
    return render_template("register.html")


# iniciar sesion
@app.route("/inicioSesion", methods=["POST"])
def trySession():
    password = request.form['password']
    user = request.form['User']
    if initSession(user, password):
        session['username'] = user
        userOnline = session['username']
        return redirect(url_for('ForWeb', id=1))
    else:
        error = "User or password was invalid!"
        flash(error)
        return render_template("login.html")


# registro de usuarios
@app.route("/oRegister", methods=["POST"])
def newUser():
    user = request.form['User']
    email = request.form['email']
    password = request.form['password']
    if addValuesUser(user, email, password):
        passed = "User was created successfully!"
        flash(passed)

        # envio del mail
        @copy_current_request_context
        def notiNewUser():
            EmailNewUser(user, email)
            return print("Notificacion enviada")

        sender = threading.Thread(name='enviar_mail', target=notiNewUser)
        sender.start()

        return render_template("login.html")
    else:
        error = "Try with another Username or Email"
        flash(error)
        return render_template("register.html")


# subruta modificar password
@app.route("/modUser")
def modUser():
    return render_template("change-password.html")


# modifica password
@app.route("/changePassword", methods=["POST"])
def changePassword():
    try:
        userOnline = session['username']
        oldPassword = request.form['oldPassword']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2 and initSession(userOnline, oldPassword):
            passed = "the password change successfully!"
            flash(passed)
            changPassword(userOnline, password1)
            return render_template("user-config.html", olus=userOnline, email=getEmail(userOnline),
                                   nDiscussions=len(getAllUserDiscussion(userOnline)),
                                   since=functools.reduce(operator.add, getDateCreate(userOnline)))
        else:
            passed = "the passwords does not match"
            flash(passed)
            return render_template("change-password.html")
    except:
        return render_template("login.html")


# sub ruta foro inicial
@app.route("/ForWeb/<int:id>", methods=['GET', 'POST'])
def ForWeb(id):
    n = math.ceil(len(getDiscussion()) / 5)
    userOnline = session['username']
    discussion = []
    if id == 1:
        discussion.append(getDiscussion()[0:5])
    elif id in range(1, n+1) and id != 1:
        discussion.append(getDiscussion()[5*(id-1):5*id])

    return render_template("index-foro.html", nDiscussions=getNDiscussions(),
                           discussion=discussion[0], totalDisussions=len(getDiscussion()), users=getAllUsers(),
                           n=n, icon=getIcon(userOnline))


# sub ruta inicio sesion
@app.route("/userConfig")
def userConfig():
    try:
        userOnline = session['username']
        return render_template("user-config.html", olus=userOnline, email=getEmail(userOnline),
                               nDiscussions=len(getAllUserDiscussion(userOnline)), icon=getIcon(userOnline),
                               since=functools.reduce(operator.add, getDateCreate(userOnline)))
    except:
        return render_template("login.html")


# vista de foros
@app.route("/viewTopics/<int:id>", methods=['GET', 'POST'])
def viewTopics(id):
    try:
        userOnline = session['username']
        return render_template("topic.html", discussion=getAllDiscussion(id),
                               topic=functools.reduce(operator.add, (getTopic(id))), id=id, olus=userOnline, v=False)
    except:
        return redirect(url_for('inicio'))


# agregar comentario en foros
@app.route("/replyPost", methods=["POST"])
def replyPost():
    try:
        # manejo de los datos y envio del mensaje
        userOnline = session['username']
        id = request.form['id']
        topic = request.form['topic']
        comment = request.form['comment']
        time = datetime.now().date()
        addComents(id, topic, userOnline, comment, time)

        # envio del mail
        @copy_current_request_context
        def noti(a, t, c, u, i):
            enviarEmailNotificacion(a, t, c, u, i)
            return print("Notificacion enviada")

        sender = threading.Thread(name='enviar_mail', target=noti,
                                  args=(getEmailDiscussion(id), topic, comment, userOnline, id))
        sender.start()

        return render_template("topic.html", discussion=getAllDiscussion(id),
                               topic=functools.reduce(operator.add, (getTopic(id))), id=id, olus=userOnline, v=True)
    except:
        return redirect(url_for('inicio'))


# Borrar comentarios
@app.route("/Delet/<int:n>/<string:c>", methods=['GET'])
def Delet(n, c):
    deletComent(n, c)
    delet = "The comment was deleted"
    flash(delet)
    try:
        userOnline = session['username']
        return render_template("topic.html", discussion=getAllDiscussion(n),
                               topic=functools.reduce(operator.add, (getTopic(n))), id=n, olus=userOnline, v=False)
    except:
        return redirect(url_for('ForWeb', id=1))


# sub ruta crear nuevo topico
@app.route("/newTopic")
def newTopic():
    return render_template("new-topic.html")


# agregar nuevas discusiones
@app.route("/addNewTopic", methods=["POST"])
def addNewTopic():
    try:
        userOnline = session['username']
        a = getDiscussion()
        id = a[0][0] + 1
        topic = request.form['title']
        comment = request.form['comment']
        time = datetime.now().date()
        addComents(id, topic, userOnline, comment, time)
        return render_template("topic.html", discussion=getAllDiscussion(id),
                               topic=functools.reduce(operator.add, (getTopic(id))), id=id)
    except:
        return redirect(url_for('inicio'))


if __name__ == "__main__":
    app.run(debug=True)
