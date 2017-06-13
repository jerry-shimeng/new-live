import smtplib
from email.mime.text import MIMEText

_user = "system@iyuhou.com"
_pwd = "QAQQWEasd123"
_to = "2306395363@qq.com"

msg = MIMEText("Test")
msg["Subject"] = "don't panic"
msg["From"] = _user
msg["To"] = _to

if __name__ == '__main__':

	try:
		s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
		s.login(_user, _pwd)
		s.sendmail(_user, _to, msg.as_string())
		s.quit()
		print("Success!")
	except smtplib.SMTPException as e:
		print("Falied,%s" % e)
