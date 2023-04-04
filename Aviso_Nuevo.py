# imports
from email.message import EmailMessage
import smtplib
import ssl
import time
import sqlite3
import functools
import operator

# conifg
connection = sqlite3.connect("C:\\users\\Santy\\source python\\Blog\\database\\data", check_same_thread=False)
cursor = connection.cursor()
em = EmailMessage()
email = 'forweb.notification@gmail.com'
contrasena = 'iprqkjftdxdwknns'
context = ssl.create_default_context()

lMails = cursor.execute("SELECT email FROM account;").fetchall()


def enviarEmailAviso():
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=None) as smtp:
        # config
        smtp.starttls(context=context)
        smtp.login(email, contrasena)

        for i in functools.reduce(operator.add, lMails):
            # adjuntos
            asunto = f'Hola, hay disponibles nuevas funcionalidades en nuestro foro!!'

            em.set_content(f"""
                <html>
                <body>
                    <font color="black" size="5">
                        <ul>
                            <li>Configuraciones del usuario</li>
                            <li>Panel del usuario con informacion relevante</li>
                            <li>Division de discuciones en varias paginas</li>
                        </ul>
                        <br/>
                        <center><button><a style="text-decoration:none" href="https://callgore.pythonanywhere.com/ForWeb/1">Entrar al foro</a></button></center>
                    </font>
                    <hr>           
            """, subtype='html')
            em['Subject'] = asunto
            em['from'] = email
            em['TO'] = i

            smtp.send_message(em)
            time.sleep(5)
            del em['To']
            del em['Subject']
            del em['from']


enviarEmailAviso()
