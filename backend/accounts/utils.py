from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from accounts.models import User
b=1
class Util:
    @staticmethod
    def send_email(data):
        html_part = MIMEMultipart(_subtype='related')
        user=User.objects.get(email=data["to_email"])
        a='''<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  </head>
  <body >
    <h2>Invitation from the management of Vanquishers!</h2>
    <p>Respected Sir/Mam,</p>
    <p>We extend our warm greetings from the management of Vanquishers. It is with great pleasure that we write to extend an invitation for you to join as a faculty.</p>
    <p>At Vanquishers , we have a long-standing tradition of producing highly skilled and well-prepared graduates. We are confident that you will teach and motivate our students for their better future.</p>
    <p>Thankyou for joining us.</p>
    <h3>Your Details:</h3>
    Name : '''+user.full_name+'''
    <br><span>Email : </span>'''+user.email+'''
    <br>Contact Number : '''+user.mobile_number+'''<br>
    <a href="https://akgec-timetable.vercel.app/login">Click here</a> to Login and reset your Password.
    <hr>
    <p>Login Credentials:</p><p><span>Email : </span>'''+data['to_email']+'''</p><p>Password : '''+data['passwd']+'''</p>
    Regards,<br>
    <strong>Team Vanquishers</strong><br>
    Computer Society of India,AKGEC
  </body>
</html>'''
        body = MIMEText(a, _subtype='html')
        html_part.attach(body)
        msg = EmailMessage(subject=data['email_subject'],to=(data['to_email'],))
        msg.attach(html_part)
        msg.send()
