import urllib.request
import json
import re
import os
import html
from html.parser import HTMLParser

def get_image_id(url):
    """Extrait un identifiant unique pour éviter les doublons d'images."""
    if not url:
        return ""
    match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', url, re.I)
    if match:
        return match.group(1).lower()
    clean = url.split('?')[0].split('$')[0].rstrip('/')
    return clean.split('/')[-1].lower()

def is_any_gif(url, alt=""):
    """Détecte TOUT type de GIF (animé, mème, ou boucle vidéo)."""
    url_l = url.lower()
    alt_l = alt.lower()
    if '.gif' in url_l or 'fl_lossy' in url_l or 'giphy' in url_l or 'tenor' in url_l or 'gifer' in url_l:
        return True
    if 'gif' in alt_l:
        return True
    return False

def clean_emojis_and_tone(text):
    """Supprime les emojis de réseaux sociaux / IA et remplace par une typographie sobre."""
    text = re.sub(r'^[ \t]*[👉👉👇👆💡🔹🔸▶️►][ \t]*', '◆ ', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[✅✔][ \t]*', '✓ ', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[❌✖][ \t]*', '✗ ', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*[⚠️🚨❗][ \t]*', 'Attention : ', text, flags=re.MULTILINE)

    replacements = {
        '✅': '✓ ',
        '❌': '✗ ',
        '⚠️': ' (Attention) ',
        '👉': ' ',
        '👈': ' ',
        '👇': ' ',
        '👆': ' ',
        '🚀': '',
        '🔥': '',
        '💡': '',
        '🎯': '',
        '⚡': '',
        '💪': '',
        '💥': '',
        '✨': '',
        '🎉': '',
        '🥳': '',
        '👀': '',
        '🤔': '',
        '🤷': '',
        '🤦': '',
        '🤫': '',
        '😱': '',
        '🔔': '',
        '📢': '',
        '📣': '',
        '📌': '',
        '📍': '',
        '🔑': '',
        '🛑': '',
        '🏆': '',
        '🧠': 'cerveau',
        '🦴': 'os',
        '❤️': '',
        '🩺': '',
        '🏥': '',
        '☕': '',
    }
    for emo, rep in replacements.items():
        text = text.replace(emo, rep)

    emoji_regex = re.compile(
        r'[\U0001F300-\U0001F5FF'
        r'\U0001F600-\U0001F64F'
        r'\U0001F680-\U0001F6FF'
        r'\U0001F700-\U0001F77F'
        r'\U0001F780-\U0001F7FF'
        r'\U0001F800-\U0001F8FF'
        r'\U0001F900-\U0001F9FF'
        r'\U0001FA00-\U0001FA6F'
        r'\U0001FA70-\U0001FAFF'
        r'\U00002702-\U000027B0'
        r'\U000024C2-\U0001F251]'
    )
    text = emoji_regex.sub('', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text

def normalize_spacing_and_lists(text):
    """
    Nettoie drastiquement les espacements anormaux, les tirets isolés
    et reconstitue de vraies listes à puces continues.
    """
    # 1. Fusionner les tirets orphelins isolés avec la ligne de texte suivante (évite les grands vides avec un tiret seul)
    text = re.sub(r'^\s*[-–—•*◆]\s*\n+\s*([^\n]+)', r'- \1', text, flags=re.MULTILINE)
    
    # 2. Fusionner les numéros orphelins (ex: "1.\n\nRedressez-vous" -> "1. Redressez-vous")
    text = re.sub(r'^\s*(\d+[\.\)])\s*\n+\s*([^\n]+)', r'\1 \2', text, flags=re.MULTILINE)
    
    # 3. Supprimer les points isolés utilisés comme espacements web
    text = re.sub(r'^\s*\.\s*$', '', text, flags=re.MULTILINE)
    
    # 4. Supprimer les hashtags Markdown isolés non suivis de texte
    text = re.sub(r'^\s*#{1,6}\s*$', '', text, flags=re.MULTILINE)
    
    # 5. Supprimer les tirets restants isolés sans texte
    text = re.sub(r'^\s*[-–—•*]\s*$', '', text, flags=re.MULTILINE)
    
    # 6. Remplacer les triples (ou plus) sauts de ligne par un double saut propre
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

class StrictCleanHTMLToMarkdownParser(HTMLParser):
    def __init__(self, seen_images):
        super().__init__()
        self.output = []
        self.seen_images = seen_images

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        if 'button' in cls or 'subscribe' in cls or 'share' in cls or 'comments' in cls:
            return

        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.output.append('\n\n### ')
        elif tag == 'p':
            self.output.append('\n\n')
        elif tag in ['ul', 'ol']:
            self.output.append('\n')
        elif tag == 'li':
            self.output.append('\n- ')
        elif tag in ['strong', 'b']:
            self.output.append('**')
        elif tag in ['em', 'i']:
            self.output.append('*')
        elif tag == 'br':
            self.output.append('\n')
        elif tag == 'img':
            src = attrs_dict.get('src', '').strip()
            alt = attrs_dict.get('alt', '').strip()
            if not src:
                return

            if is_any_gif(src, alt):
                return

            if any(skip in src.lower() for skip in ['avatar', 'icon', 'tracker', 'metricool', 'google', 'logo']):
                return

            img_id = get_image_id(src)
            if img_id in self.seen_images:
                return
            self.seen_images.add(img_id)

            self.output.append(f'\n\n![{alt}]({src})\n\n')

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.output.append('\n\n')
        elif tag in ['strong', 'b']:
            self.output.append('**')
        elif tag in ['em', 'i']:
            self.output.append('*')

    def handle_data(self, data):
        self.output.append(data)

    def get_markdown(self):
        text = ''.join(self.output)
        patterns_to_remove = [
            r'Abonnez-vous pour lire la suite.*',
            r'Partagez cet article.*',
            r'Cet article est réservé aux abonnés.*',
            r'Laissez un commentaire.*',
            r'Restack.*',
            r'Share.*',
            r'Subscribe.*'
        ]
        for pat in patterns_to_remove:
            text = re.sub(pat, '', text, flags=re.IGNORECASE)
        
        text = clean_emojis_and_tone(text)
        text = normalize_spacing_and_lists(text)
        return text

def fetch_all_posts():
    all_posts = []
    offset = 0
    print("Récupération des articles depuis osteomagazine.com...")
    while True:
        url = f"https://osteomagazine.com/api/v1/posts?limit=50&offset={offset}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if not data:
                    break
                all_posts.extend(data)
                offset += len(data)
                if len(data) < 50:
                    break
        except Exception as e:
            print(f"Erreur à l'offset {offset}: {e}")
            break
    return all_posts

def main():
    posts = fetch_all_posts()
    print(f"Total d'articles téléchargés : {len(posts)}")

    categories = {
        "Dos, Rachis & Imagerie Médicale (Lumbago, Hernies, Cervicales)": [],
        "Hanches, Bassin & Membres (Épaule, Genou, Sciatique)": [],
        "Biomécanique, Posture & Chaînes Musculaires": [],
        "Sport, Cyclisme & Préparation Physique": [],
        "Santé Globale, Micronutrition & Système Digestif": [],
        "Réflexions & Pratique Ostéopathique": []
    }

    total_images = 0

    for p in posts:
        title = clean_emojis_and_tone((p.get('title') or '').strip())
        subtitle = clean_emojis_and_tone((p.get('subtitle') or '').strip())
        cover_image = (p.get('cover_image') or '').strip()
        body_html = p.get('body_html') or ''
        date = (p.get('post_date') or '')[:10]

        if is_any_gif(cover_image):
            cover_image = ''

        seen_images = set()
        cover_id = get_image_id(cover_image)
        if cover_id:
            seen_images.add(cover_id)

        parser = StrictCleanHTMLToMarkdownParser(seen_images)
        try:
            parser.feed(body_html)
            content_md = parser.get_markdown()
        except Exception:
            content_md = normalize_spacing_and_lists(clean_emojis_and_tone(body_html))

        chapter_images = len(seen_images)
        total_images += chapter_images

        title_lower = (title + " " + subtitle + " " + content_md[:500]).lower()
        cat = "Réflexions & Pratique Ostéopathique"
        if any(w in title_lower for w in ['dos', 'lombaire', 'lumbago', 'rachis', 'cervical', 'disque', 'hernie', 'colonne']):
            cat = "Dos, Rachis & Imagerie Médicale (Lumbago, Hernies, Cervicales)"
        elif any(w in title_lower for w in ['hanche', 'épaule', 'genou', 'sciatique', 'bras', 'jambe', 'bassin', 'articulation']):
            cat = "Hanches, Bassin & Membres (Épaule, Genou, Sciatique)"
        elif any(w in title_lower for w in ['muscle', 'posture', 'tuyauterie', 'fascia', 'raide', 'étirement', 'mobilité']):
            cat = "Biomécanique, Posture & Chaînes Musculaires"
        elif any(w in title_lower for w in ['cyclis', 'vélo', 'course', 'running', 'sport', 'musculation', 'échauffement']):
            cat = "Sport, Cyclisme & Préparation Physique"
        elif any(w in title_lower for w in ['bactérie', 'flore', 'intestin', 'digest', 'nutrition', 'foie', 'inflammation', 'alimentation']):
            cat = "Santé Globale, Micronutrition & Système Digestif"

        categories[cat].append({
            'title': title,
            'subtitle': subtitle,
            'cover_image': cover_image,
            'date': date,
            'content': content_md
        })

    book_lines = [
        "# LE GUIDE GLOBAL DU CORPS & DU MOUVEMENT",
        "## Comprendre, soulager et optimiser sa santé mécanique à la lumière de l'imagerie médicale et de l'ostéopathie",
        "\n**Par Frédéric Murria**  ",
        "*Ostéopathe D.O — 23 ans d'expertise en imagerie médicale (Scanner, IRM)*\n",
        "---\n",
        "## Table des Matières\n"
    ]

    for cat_name, items in categories.items():
        if items:
            book_lines.append(f"### {cat_name} ({len(items)} chapitres)\n")
            for item in items:
                book_lines.append(f"◆ {item['title']}")
            book_lines.append("")

    book_lines.append("\n---\n")

    for cat_name, items in categories.items():
        if not items:
            continue
        book_lines.append(f"\n\n# PARTIE : {cat_name.upper()}\n")
        book_lines.append("=" * 60 + "\n\n")

        for item in items:
            book_lines.append(f"## {item['title']}\n")
            if item['subtitle']:
                book_lines.append(f"*{item['subtitle']}*\n\n")
            if item['cover_image']:
                book_lines.append(f"![Illustration principale]({item['cover_image']})\n\n")
            book_lines.append(item['content'])
            book_lines.append("\n\n---\n\n")

    full_book_content = "\n".join(book_lines)

    output_path = "livre_osteomagazine/recueil_osteomagazine_complet.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_book_content)

    print(f"\nRecueil Markdown mis à jour avec espacements et listes parfaites !")
    print(f"Total d'illustrations fixes et nettes conservées : {total_images}")

if __name__ == '__main__':
    main()
