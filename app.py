from flask import Flask, render_template, request, redirect, url_for, flash
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'alma123'

# ngarko variablat nga .env
load_dotenv()

def send_email(name, email, message):
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Mesazh nga formulari i kontaktit'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg.set_content(f'Emri: {name}\nEmail: {email}\nMesazhi:\n{message}')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print(f"[GABIM GJATË DËRGIMIT]: {e}")
        return False


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Bitte füllen Sie alle Felder aus.', 'error')
        else:
            if send_email(name, email, message):
                flash('Nachricht wurde erfolgreich gesendet!', 'success')
            else:
                flash('Senden fehlgeschlagen. Bitte versuchen Sie es erneut..', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
