import smtplib


def send_email(mailto, sub, msag):
    try:
        gmailaddress = "ai.bot.for.healthcare@gmail.com"
        gmailpassword = "xofbmzojngqftyev"
        msg = 'Subject: {}\n\n{}'.format(sub, msag)
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.starttls()
        mailServer.login(gmailaddress, gmailpassword)
        mailServer.sendmail(gmailaddress, mailto, msg)
        mailServer.quit()
        return
    except Exception as e:
        print(e)
        return "UNABLE TO SEND EMAIL! PLEASE VERIFY"
