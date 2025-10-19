import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODELS = [
	"csebuetnlp/mT5_multilingual_XLSum",
]

def clean_input_text(text: str) -> str:
	text = re.sub(r'https?://\S+', '', text)
	text = re.sub(r'(Lire aussi|Suivez-nous|Newsletter|Crédits?|©).*', '', text, flags=re.IGNORECASE)
	text = re.sub(r'\s+', ' ', text)
	sentences = re.split(r'[.!?]+', text)
	sentences = [s.strip() for s in sentences if len(s.split()) >= 10]
	text = '. '.join(sentences) + '.'
	return text.strip()

def clean_output_summary(summary: str) -> str:
	summary = re.sub(r'\([^)]{1,3}\s[^)]{1,3}\)', '', summary)
	summary = re.sub(r'\s[a-z]\s', ' ', summary)
	summary = re.sub(r'\b(BBC|Afrique|com)\b', '', summary, flags=re.IGNORECASE)
	summary = re.sub(r'\s+', ' ', summary)
	summary = re.sub(r'\s([.,;!?])', r'\1', summary)
	return summary.strip()

def is_valid_summary(summary: str, min_words: int = 20) -> bool:
	if not summary or len(summary) < 50:
		return False
	word_count = len(summary.split())
	if word_count < min_words:
		return False
	special_chars = len(re.findall(r'[^a-zA-ZÀ-ÿ0-9\s.,;!?\'-]', summary))
	if special_chars > word_count * 0.1:
		return False
	return True

def summarize(text: str, sentences_count: int = 4) -> str:
	if not HF_API_TOKEN:
		raise RuntimeError("Aucun token Hugging Face détecté. Vérifie ton fichier .env")

	headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
	text = clean_input_text(text)

	if not text or len(text) < 100:
		return "(texte trop court)"

	target_length = sentences_count * 100
	min_length = max(80, target_length - 60)
	max_length = min(512, target_length + 150)

	for i, MODEL in enumerate(MODELS):
		if "bart" in MODEL.lower():
			payload = {
				"inputs": text[:3000],
				"parameters": {
					"max_length": max_length,
					"min_length": min_length,
					"do_sample": False,
					"early_stopping": True,
				}
			}
		elif "mt5" in MODEL.lower() or "multilingual" in MODEL.lower():
			payload = {
				"inputs": text[:4000],
				"parameters": {
					"max_length": max_length,
					"min_length": min_length,
					"do_sample": False,
					"num_beams": 4,
					"early_stopping": True,
				}
			}
		else:
			payload = {
				"inputs": text[:3500],
				"parameters": {
					"max_length": max_length,
					"min_length": min_length,
					"do_sample": False,
				}
			}

		try:
			print(f"Tentative {i+1}/{len(MODELS)} : {MODEL.split('/')[-1]}...")
			response = requests.post(
				f"https://api-inference.huggingface.co/models/{MODEL}",
				headers=headers,
				json=payload,
				timeout=90
			)
			response.raise_for_status()
			data = response.json()

			if isinstance(data, list) and len(data) > 0:
				result = data[0].get("summary_text") or data[0].get("generated_text", "")
				if result:
					result = clean_output_summary(result)
					if is_valid_summary(result):
						print(f"Résumé généré par {MODEL.split('/')[-1]}")
						return f"Résumé : {result}"
					else:
						print(f"Résumé de mauvaise qualité, essai du modèle suivant...")
						continue
			else:
				print(f"Réponse inattendue : {data}")
				if isinstance(data, dict) and "estimated_time" in data:
					import time
					wait_time = min(data["estimated_time"], 30)
					print(f"Modèle en chargement, attente de {wait_time}s...")
					time.sleep(wait_time)
					continue

		except requests.exceptions.HTTPError as e:
			print(f"Erreur HTTP avec {MODEL}: {e}")
		except requests.exceptions.RequestException as e:
			print(f"Erreur réseau : {e}")

	print("Tous les modèles API ont échoué, fallback vers mode LOCAL recommandé")
	return "(Impossible de générer un résumé via API. Utilisez MODE=local pour de meilleurs résultats)"
