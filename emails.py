# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_mail(pass_temp, username, name, link):

    # create message object instance
    msg = MIMEMultipart()

    message = """
    <html>
    <body>
        <div style="margin:0;padding-top:0;background-color:#c7cda7;color:#000000">
            <div class="adM"></div>
            <table width="100%" cellpadding="0" cellspacing="0" style="padding:10px;border-bottom:#121635">
                <tbody>
                    <tr>
                        <td height="35"></td>
                    </tr>
                    <tr>
                        <td height="80" style="text-align:center;color:#ffffff">
                            <img height="80" alt="CAM" src="http://cobrareumatologia.com.br/wp-content/uploads/2019/10/logo-cobra.png" style="vertical-align:middle" data-image-whitelisted="" class="CToWUd">
                        </td>
                    </tr>
                </tbody>
            </table>
            <center>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="34"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0" style="background-color:#f3f2f0;border-radius:3rem">
                    <tbody>
                        <tr>
                            <td style="padding:24px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tbody>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Olá """ + name + """, seu usuário foi registrado, estes são os seus dados de login<br><br>
                                                email: <a href="mailto:"""+username+""" target="_blank">"""+username+"""</a><br>
                                                senha: """ + pass_temp + """
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Descarregue seu App no celular accesando este link:
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                <a href=" """+link+""" " target="_blank" data-saferedirecturl=" """+link+""" "> """+link+""" </a>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Caso tenha problemas com o link entre em contato com a equipe de suporte através do email <a href="mailto:suporte@ievo4action.com.br" target="_blank">suporte@ievo4action.com.br</a>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="padding:24px 0 24px 0;text-align:center">
                                                <center>
                                                    <table cellpadding="0" cellspacing="0" style="background-image:linear-gradient(to bottom right,#213615,#6e773e);border-color:#213615;border-radius:1rem">
                                                        <tbody><tr>
                                                            <td style="padding:8px 16px 8px 16px">
                                                                <a href="http://localhost:4200" style="text-decoration:none;font-size:16px;line-height:24px;font-family:'Open Sans',sans-serif;color:#ffffff" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://localhost:4200&amp;source=gmail&amp;ust=1637826436805000&amp;usg=AOvVaw03pnTf4on_0VIT5Z4I3-YU">Conecte-se</a>
                                                            </td>
                                                        </tr>
                                                    </tbody></table>
                                                </center>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>

    
                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td><img width="100%"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="24"></td>
                        </tr>
                    </tbody>
                </table>
                
                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#ffffff;padding:8px 16px 16px 16px;text-align:center">
                                Footer cobra
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#474747;padding:0 16px 0 16px;text-align:center">
                                ©2020 cobra
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="32"></td>
                        </tr>
                    </tbody>
                </table>
            </center>
            <div class="yj6qo"></div>
            <div class="adL"></div>
        </div>
    </body>
</html>
   
    """

    # setup the parameters of the message
    password = "suporte@ievo4action"
    msg['From'] = "suporte@ievo4action.com.br"
    msg['To'] = username
    msg['Subject'] = "Usuario Cadastrado"

    # add in the message body
    part_1 = MIMEText(message, 'html')
    msg.attach(part_1)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print
    "successfully sent email to %s:" % (msg['To'])


def send_mail_ios(username, name, link):
    # create message object instance
    msg = MIMEMultipart()

    message = """
    <html>
    <body>
        <div style="margin:0;padding-top:0;background-color:#c7cda7;color:#000000">
            <div class="adM"></div>
            <table width="100%" cellpadding="0" cellspacing="0" style="padding:10px;border-bottom:#121635">
                <tbody>
                    <tr>
                        <td height="35"></td>
                    </tr>
                    <tr>
                        <td height="80" style="text-align:center;color:#ffffff">
                            <img height="80" alt="CAM" src="http://cobrareumatologia.com.br/wp-content/uploads/2019/10/logo-cobra.png" style="vertical-align:middle" data-image-whitelisted="" class="CToWUd">
                        </td>
                    </tr>
                </tbody>
            </table>
            <center>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="34"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0" style="background-color:#f3f2f0;border-radius:3rem">
                    <tbody>
                        <tr>
                            <td style="padding:24px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tbody>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                <center> Olá """ + name + """<br> </center> 
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Descarregue seu App no celular accesando este link:
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                <a href=" """ + link + """ " target="_blank" data-saferedirecturl=" """ + link + """ "> """ + link + """ </a>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Caso tenha problemas com o link entre em contato com a equipe de suporte através do email <a href="mailto:suporte@ievo4action.com.br" target="_blank">suporte@ievo4action.com.br</a>
                                            </td>
                                        </tr>

                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>


                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td><img width="100%"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="24"></td>
                        </tr>
                    </tbody>
                </table>

                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#ffffff;padding:8px 16px 16px 16px;text-align:center">
                                Footer cobra
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#474747;padding:0 16px 0 16px;text-align:center">
                                ©2020 cobra
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="32"></td>
                        </tr>
                    </tbody>
                </table>
            </center>
            <div class="yj6qo"></div>
            <div class="adL"></div>
        </div>
    </body>
</html>

    """

    # setup the parameters of the message
    password = "suporte@ievo4action"
    msg['From'] = "suporte@ievo4action.com.br"
    msg['To'] = username
    msg['Subject'] = "Novo Link -  APP IOS"

    # add in the message body
    part_1 = MIMEText(message, 'html')
    msg.attach(part_1)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print
    "successfully sent email to %s:" % (msg['To'])


def send_mail_recovery(pass_temp, username, name):
    # create message object instance
    msg = MIMEMultipart()

    message = """
    <html>
    <body>
        <div style="margin:0;padding-top:0;background-color:#c7cda7;color:#000000">
            <div class="adM"></div>
            <table width="100%" cellpadding="0" cellspacing="0" style="padding:10px;border-bottom:#121635">
                <tbody>
                    <tr>
                        <td height="35"></td>
                    </tr>
                    <tr>
                        <td height="80" style="text-align:center;color:#ffffff">
                            <img height="80" alt="CAM" src="http://cobrareumatologia.com.br/wp-content/uploads/2019/10/logo-cobra.png" style="vertical-align:middle" data-image-whitelisted="" class="CToWUd">
                        </td>
                    </tr>
                </tbody>
            </table>
            <center>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="34"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0" style="background-color:#f3f2f0;border-radius:3rem">
                    <tbody>
                        <tr>
                            <td style="padding:24px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tbody>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Olá """ + name + """, estes são os seus dados de login<br><br>
                                                email: <a href="mailto:""" + username + """ target="_blank">""" + username + """</a><br>
                                                senha: """ + pass_temp + """
                                            </td>
                                        </tr>
                                     

                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Caso tenha problemas com o link entre em contato com a equipe de suporte através do email <a href="mailto:suporte@ievo4action.com.br" target="_blank">suporte@ievo4action.com.br</a>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="padding:24px 0 24px 0;text-align:center">
                                                <center>
                                                    <table cellpadding="0" cellspacing="0" style="background-image:linear-gradient(to bottom right,#213615,#6e773e);border-color:#213615;border-radius:1rem">
                                                        <tbody><tr>
                                                            <td style="padding:8px 16px 8px 16px">
                                                                <a href="http://localhost:4200" style="text-decoration:none;font-size:16px;line-height:24px;font-family:'Open Sans',sans-serif;color:#ffffff" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://localhost:4200&amp;source=gmail&amp;ust=1637826436805000&amp;usg=AOvVaw03pnTf4on_0VIT5Z4I3-YU">Conecte-se</a>
                                                            </td>
                                                        </tr>
                                                    </tbody></table>
                                                </center>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>


                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td><img width="100%"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="24"></td>
                        </tr>
                    </tbody>
                </table>

                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#ffffff;padding:8px 16px 16px 16px;text-align:center">
                                Footer cobra
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#474747;padding:0 16px 0 16px;text-align:center">
                                ©2020 cobra
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="32"></td>
                        </tr>
                    </tbody>
                </table>
            </center>
            <div class="yj6qo"></div>
            <div class="adL"></div>
        </div>
    </body>
</html>

    """

    # setup the parameters of the message
    password = "suporte@ievo4action"
    msg['From'] = "suporte@ievo4action.com.br"
    msg['To'] = username
    msg['Subject'] = "Recovery Senha"

    # add in the message body
    part_1 = MIMEText(message, 'html')
    msg.attach(part_1)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print
    "successfully sent email to %s:" % (msg['To'])