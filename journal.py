import os
from datetime import date
from core.pdf_generator import generer_pdf
from core.scrap import scrape_listing_actuia_et_articles
from core.email_sender import envoyer_email
from dotenv import load_dotenv

load_dotenv()
MODE = os.getenv("MODE", "local")
SOURCES = os.getenv("SOURCES", "https://www.actuia.com/actualite/")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "4"))
SENTENCES_COUNT = int(os.getenv("SENTENCES_COUNT", "5"))
SEND_EMAIL = os.getenv("SEND_EMAIL", "false").lower() == "true"

if MODE == "local":
	from core.summarizer_local import summarize
	print("Mode résumé : LOCAL (Sumy)")
else:
	from core.summarizer_api_hf import summarize
	print("Mode résumé : API (Hugging Face)")

def generer_journal():
	sources = [s.strip() for s in SOURCES.split(",") if s.strip()]
	print(f"Scraping {len(sources)} source(s)...")

	all_blocs = []

	for source in sources:
		print(f"\nTraitement : {source}")
		articles = scrape_listing_actuia_et_articles(source, max_articles=MAX_ARTICLES)

		if not articles:
			print(f"Aucun article trouvé pour {source}")
			continue

		for art in articles:
			titre = art["title"]
			url = art["url"]
			texte = art["text"]

			resume = summarize(texte, sentences_count=SENTENCES_COUNT)
			if not resume:
				continue

			bloc = f"{titre}\n{url}\n{resume}\n"
			all_blocs.append(bloc)

	if not all_blocs:
		return ""

	header = f"Journal IA — {date.today().isoformat()}\n"
	header += f"{len(sources)} source(s) | {len(all_blocs)} article(s)\n\n"
	return header + "\n\n".join(all_blocs)

if __name__ == "__main__":
	contenu = generer_journal()
	if contenu.strip():
		nom_pdf = f"mon_journal_{date.today().isoformat()}.pdf"
		fichier_pdf = generer_pdf(contenu, titre="Mon Journal", fichier=nom_pdf)

		if SEND_EMAIL:
			envoyer_email(f"data/{nom_pdf}")
	else:
		print("Aucun article résumable aujourd'hui.")
