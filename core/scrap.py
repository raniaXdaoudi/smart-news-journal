from bs4 import BeautifulSoup
import html
import requests
from urllib.parse import urljoin, urlparse

HEADERS = {
	"User-Agent": (
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) "
		"Chrome/115.0 Safari/537.36"
	)
}

def _get_soup(url: str) -> BeautifulSoup | None:
	url = (url or "").strip()
	if not (url.startswith("http://") or url.startswith("https://")):
		print("L'URL doit commencer par http:// ou https://")
		return None
	try:
		r = requests.get(url, headers=HEADERS, timeout=15)
		r.raise_for_status()
		return BeautifulSoup(r.content, "html.parser")
	except requests.RequestException as e:
		print(f"[HTTP] {url} -> {e}")
		return None


def _dedup_and_filter(paragraphs: list[str], min_len: int = 80) -> list[str]:
	seen = set()
	clean = []
	for p in paragraphs:
		if not p:
			continue
		t = html.unescape(" ".join(p.split()))
		if len(t) < min_len:
			continue
		if t in seen:
			continue
		if any(x in t.lower() for x in ["©", "crédit photo", "lire aussi", "suivez-nous", "newsletter"]):
			continue
		seen.add(t)
		clean.append(t)
	return clean

def trouver_liens_articles_actuia(listing_url: str, limit: int = 6) -> list[str]:
	soup = _get_soup(listing_url)
	if not soup:
		return []

	parsed = urlparse(listing_url)
	base = f"{parsed.scheme}://{parsed.netloc}"

	liens, vus = [], set()
	for a in soup.select("h2 a[href], h3 a[href], article a[href], a[href]"):
		href = a.get("href")
		if not href:
			continue
		href_abs = urljoin(base, href)

		if "/actualite/" not in href_abs:
			continue
		if "#" in href_abs or href_abs.rstrip("/").endswith("/actualite"):
			continue
		if href_abs in vus:
			continue

		vus.add(href_abs)
		liens.append(href_abs)
		if len(liens) >= limit:
			break
	return liens


def extraire_texte_article(url_article: str) -> tuple[str, str]:
	soup = _get_soup(url_article)
	if not soup:
		return "", ""

	title_tag = soup.find("h1")
	if title_tag and title_tag.get_text(strip=True):
		title = html.unescape(title_tag.get_text(strip=True))
	else:
		og = soup.find("meta", attrs={"property": "og:title"}) or soup.find("meta", attrs={"name": "title"})
		title = html.unescape(og["content"].strip()) if og and og.has_attr("content") else url_article

	candidates = []
	for selector in [
		"article",
		"main",
		"div.entry-content",
		"section[class*='content']",
		"div[class*='content']",
		"div.post-content",
		"div[itemprop='articleBody']"
	]:
		found = soup.select_one(selector)
		if found:
			candidates.append(found)

	paragraphs = []
	for bloc in candidates or [soup]:
		for tag in bloc.find_all(["p", "li"]):
			txt = tag.get_text(separator=" ", strip=True)
			if txt:
				paragraphs.append(txt)

	clean = _dedup_and_filter(paragraphs, min_len=80)
	full_text = "\n".join(clean)
	return title, full_text


def scrape_listing_actuia_et_articles(listing_url: str, max_articles: int = 6) -> list[dict]:
	articles = []
	for url in trouver_liens_articles_actuia(listing_url, limit=max_articles):
		title, text = extraire_texte_article(url)
		if not text:
			continue
		articles.append({"title": title, "url": url, "text": text})
	return articles
