from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

def generer_pdf(contenu: str, titre: str = "Mon Journal", fichier: str | None = None):
	if not fichier:
		fichier = f"{titre.replace(' ', '_').lower()}_{date.today().isoformat()}.pdf"
	data_dir = "data"
	if not os.path.exists(data_dir):
		os.makedirs(data_dir)
	fichier_complet = os.path.join(data_dir, fichier)
	styles = getSampleStyleSheet()
	doc = SimpleDocTemplate(fichier_complet, pagesize=A4)
	story = []
	story.append(Paragraph(titre, styles["Title"]))
	story.append(Spacer(1, 12))
	for para in (contenu or "").split("\n"):
		p = para.strip()
		if not p:
			continue
		story.append(Paragraph(p, styles["BodyText"]))
		story.append(Spacer(1, 8))
	doc.build(story)
	print(f"PDF généré : {fichier_complet}")
