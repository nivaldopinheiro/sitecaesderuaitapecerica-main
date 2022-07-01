from flask import Flask, render_template, redirect, request
import requests
from Services import database as db
app = Flask(__name__)

@app.route('/')
def index():
    db.criar_table()
    return render_template('index.html', alerta = None)


@app.route('/send_mail/', methods=['POST'])
def send_mail():
    alerta = None
    user_nome = request.form['name']
    user_email = request.form['email']
    user_phone = request.form['phone']
    user_message = request.form['message']
      
    db.insert_message(user_nome, user_email, user_phone, user_message)
    
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
    
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # Quem envia
    senderSmtp = sib_api_v3_sdk.SendSmtpEmailSender(name=user_nome, email=user_email)
    
    # Definir o e-mail 
    # sendTo = sib_api_v3_sdk.SendSmtpEmailTo(email='anjo_li35@hotmail.com', name='Projeto integrador - ')
    
    # Quem recebe
    sendTo = sib_api_v3_sdk.SendSmtpEmailTo(email="alvarogp2010@gmail.com", name=f'Contato - {user_nome} - {user_phone}')
    arrTo = [sendTo] #Adding `to` in a list
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(sender=senderSmtp, to=arrTo, html_content=user_message,subject=f'Contato - {user_nome} - {user_phone}') # SendSmtpEmail | Values to send a transactional email
    try:
    # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"EMAIL ENVIADO COM SUCESS O.\n{api_response}")
        alerta = 'success'
    except ApiException as e:
        alerta = 'error'
        print("Exception when calling AccountApi->get_account: %s\n" % e)
    
    return render_template('index.html', alerta = alerta)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port='8000')
