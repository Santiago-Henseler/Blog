# imports
from email.message import EmailMessage
import smtplib
import ssl
import time

# conifg
em = EmailMessage()
email = 'forweb.notification@gmail.com'
contrasena = 'iprqkjftdxdwknns'
context = ssl.create_default_context()


def enviarEmailNotificacion(l, t, c, u, id):
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=None) as smtp:
        # config
        smtp.starttls(context=context)
        smtp.login(email, contrasena)

        for i in l:
            # adjuntos
            asunto = f'New comment in the discussion: "{t}"'

            em.set_content(f"""
                <html>
                <body>
                    <font color="black" size="5">
                        <p><b>{u}</b> comment: "{c}"</p>
                        
                             <center><button><a style="text-decoration:none" href="https://callgore.pythonanywhere.com/viewTopics/{id}">Reply this comment</a></button></center>
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


def EmailNewUser(u, e):
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=None) as smtp:
        # adjuntos
        asunto = f'Hi {u}, welcome'

        em.set_content(f"""
                        <html>
                        <body>
                            <font color="black" size="5">
                                <p>Thank you for creating an account on ForWeb.
                                we hope you enjoy using it and make new friends!!!</p>

                                <center><button><a style="text-decoration:none" href="https://callgore.pythonanywhere.com/ForWeb">Start using ForWeb</a></button></center>
                            </font>
                            <hr>           
                    """, subtype='html')
        em['Subject'] = asunto
        em['from'] = email
        em['TO'] = e

        # config
        smtp.starttls(context=context)
        smtp.login(email, contrasena)
        smtp.send_message(em)
        time.sleep(5)
        del em['To']
        del em['Subject']
        del em['from']
