import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "french"

def clean_text(text: str) -> str:
	text = re.sub(r"http\S+", "", text)
	text = re.sub(r"Lire aussi.*?\. ?", "", text, flags=re.I)
	text = re.sub(r"\s+", " ", text).strip()
	phrases = list(dict.fromkeys(re.split(r'(?<=[.!?]) +', text)))
	return " ".join(phrases)


def summarize_ensemble(text: str, sentences_count: int = 4) -> str:
	if not text or len(text) < 200:
		return text.strip()

	parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)

	summarizers = [
		LsaSummarizer(stemmer),
		LuhnSummarizer(stemmer),
		LexRankSummarizer(stemmer)
	]

	for s in summarizers:
		s.stop_words = get_stop_words(LANGUAGE)

	all_sentences = []
	for summarizer in summarizers:
		summary = summarizer(parser.document, sentences_count)
		all_sentences += [str(sentence).strip() for sentence in summary if len(str(sentence).strip()) > 30]

	seen = set()
	unique = [s for s in all_sentences if not (s in seen or seen.add(s))]

	result = " ".join(unique[:sentences_count])
	return result.strip()


def format_resume(resume: str) -> str:
	resume = resume.replace(" .", ".").replace(" ,", ",")
	resume = re.sub(r"\s+", " ", resume).strip()
	if not resume.endswith("."):
		resume += "."
	return f"Résumé : {resume}"


def summarize(text: str, sentences_count: int = 4) -> str:
	cleaned = clean_text(text)
	resume = summarize_ensemble(cleaned, sentences_count)
	return format_resume(resume)
