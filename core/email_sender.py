import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

def envoyer_email(fichier_pdf: str, destinataire: str = None):
	smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
	smtp_port = int(os.getenv("SMTP_PORT", "587"))
	email_expediteur = os.getenv("EMAIL_FROM")
	email_password = os.getenv("EMAIL_PASSWORD")
	email_destinataire = destinataire or os.getenv("EMAIL_TO")

	if not all([email_expediteur, email_password, email_destinataire]):
		print("Configuration email manquante dans .env")
		print("Requis: EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO")
		return False

	if not os.path.exists(fichier_pdf):
		print(f"Fichier PDF introuvable : {fichier_pdf}")
		return False

	msg = MIMEMultipart()
	msg['From'] = email_expediteur
	msg['To'] = email_destinataire
	msg['Subject'] = f"Journal IA - {date.today().strftime('%d/%m/%Y')}"

	corps = f"""
Bonjour,

Voici votre journal IA quotidien du {date.today().strftime('%d/%m/%Y')}.

Le PDF est joint à cet email.

Bonne lecture !

---
Généré automatiquement par LBMS
"""

	msg.attach(MIMEText(corps, 'plain'))

	try:
		with open(fichier_pdf, "rb") as attachment:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(attachment.read())

		encoders.encode_base64(part)
		part.add_header(
			'Content-Disposition',
			f'attachment; filename= {os.path.basename(fichier_pdf)}'
		)
		msg.attach(part)

		with smtplib.SMTP(smtp_server, smtp_port) as server:
			server.starttls()
			server.login(email_expediteur, email_password)
			server.send_message(msg)

		print(f"Email envoyé avec succès à {email_destinataire}")
		return True

	except smtplib.SMTPAuthenticationError as e:
		print(f"Erreur d'authentification email: {e}")
		print(f"Serveur: {smtp_server}:{smtp_port}")
		print(f"Email utilisé: {email_expediteur}")
		print("Vérifiez EMAIL_FROM et EMAIL_PASSWORD dans .env")
		return False
	except smtplib.SMTPException as e:
		print(f"Erreur SMTP : {e}")
		return False
	except Exception as e:
		print(f"Erreur lors de l'envoi de l'email : {e}")
		import traceback
		traceback.print_exc()
		return False

