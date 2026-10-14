import urllib.request
import json
import xml.etree.ElementTree as ET
import os
import re
import sys
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


WORKSPACE = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(WORKSPACE, "articles_registry.json")
ARTICLES_DIR = os.path.join(WORKSPACE, "articles")
os.makedirs(ARTICLES_DIR, exist_ok=True)

# Load registry
if os.path.exists(REGISTRY_PATH):
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception:
        registry = {}
else:
    registry = {}

def clean_html(raw_html):
    if not raw_html:
        return ""
    # Strip unnecessary substack tracking pixels or scripts
    cleaned = re.sub(r'<script.*?</script>', '', raw_html, flags=re.DOTALL)
    cleaned = re.sub(r'<iframe.*?>.*?</iframe>', '', cleaned, flags=re.DOTALL)
    return cleaned

def generate_article_page(item):
    slug = item["slug"]
    title = item["title"]
    description = item.get("description", "")
    author = item.get("author", "Frédéric Murria — Ostéopathe D.O")
    date_str = item.get("date", datetime.now().strftime("%Y-%m-%d"))
    cover_image = item.get("cover_image", "https://rdv.osteomagazine.com/osteo.png")
    content_html = item.get("body_html", "")
    source_name = item.get("source_name", "Osteomagazine")
    canonical_url = item.get("canonical_url", f"https://rdv.osteomagazine.com/articles/{slug}.html")

    html = f"""<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Revue Santé Frédéric Murria</title>
  <meta name="description" content="{description[:160]}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description[:200]}">
  <meta property="og:image" content="{cover_image}">
  <meta property="og:url" content="https://rdv.osteomagazine.com/articles/{slug}.html">
  <meta property="og:type" content="article">

  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&family=Playfair+Display:ital,wght@0,600;0,800;1,600&display=swap" rel="stylesheet">

  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .serif {{ font-family: 'Playfair Display', serif; }}
    .article-body p {{ margin-bottom: 1.5rem; line-height: 1.85; font-size: 1.125rem; color: #334155; }}
    .article-body h2 {{ font-size: 1.75rem; font-weight: 800; margin-top: 2.5rem; margin-bottom: 1rem; color: #0f172a; line-height: 1.3; }}
    .article-body h3 {{ font-size: 1.35rem; font-weight: 700; margin-top: 2rem; margin-bottom: 0.75rem; color: #0f172a; }}
    .article-body img {{ border-radius: 1rem; margin: 2rem auto; max-width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.08); }}
    .article-body ul, .article-body ol {{ margin-bottom: 1.5rem; padding-left: 1.5rem; }}
    .article-body li {{ margin-bottom: 0.5rem; line-height: 1.75; }}
    .article-body blockquote {{ border-left: 4px solid #0d9488; padding-left: 1.25rem; font-style: italic; color: #0f766e; margin: 1.5rem 0; background: #f0fdfa; padding: 1rem 1.25rem; border-radius: 0.75rem; }}
  </style>

  <!-- Schema.org Article -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "headline": "{title}",
    "description": "{description[:200]}",
    "image": "{cover_image}",
    "datePublished": "{date_str}",
    "author": {{
      "@type": "Person",
      "name": "Frédéric Murria",
      "jobTitle": "Ostéopathe D.O",
      "url": "https://rdv.osteomagazine.com"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Cabinet d'Ostéopathie Frédéric Murria",
      "url": "https://rdv.osteomagazine.com"
    }}
  }}
  </script>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col justify-between">

  <!-- Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-40 border-b border-teal-500/30 backdrop-blur-md bg-slate-900/95">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center max-w-5xl">
      <div class="flex items-center gap-3">
        <a href="../index.html" class="flex items-center gap-3 group">
          <img src="../logo.png" alt="Logo Frédéric Murria" class="w-10 h-10 object-contain">
          <div>
            <span class="text-lg font-bold leading-tight block group-hover:text-teal-300 transition">Frédéric Murria</span>
            <span class="text-[10px] font-bold text-teal-400 uppercase tracking-widest block">Ostéopathe D.O | Cabinet Pinet</span>
          </div>
        </a>
      </div>
      <div class="flex items-center gap-4">
        <a href="../revue-sante.html" class="hidden sm:inline-block text-xs font-bold uppercase tracking-wider hover:text-teal-300 transition text-slate-300">
          <i class="fas fa-arrow-left mr-1"></i> Tous les articles
        </a>
        <a href="https://rdv.terapiz.com/osteopathe/pinet/frederic-murria" target="_blank" class="bg-teal-600 hover:bg-teal-500 text-white font-black text-xs uppercase px-4 py-2.5 rounded-full shadow-lg transition">
          Prendre RDV
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Article -->
  <main class="py-12 md:py-16">
    <article class="container mx-auto px-4 max-w-3xl">
      
      <!-- Breadcrumb -->
      <nav class="text-xs text-slate-500 mb-6 flex items-center gap-2 font-medium">
        <a href="../index.html" class="hover:text-teal-600">Accueil</a>
        <span>/</span>
        <a href="../revue-sante.html" class="hover:text-teal-600">Revue Santé</a>
        <span>/</span>
        <span class="text-slate-700 truncate max-w-xs">{title}</span>
      </nav>

      <!-- Badge source -->
      <div class="flex items-center gap-3 mb-4">
        <span class="bg-teal-100 text-teal-800 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          <i class="fas fa-book-medical mr-1.5"></i> {source_name}
        </span>
        <span class="text-xs text-slate-400 font-semibold">{date_str[:10]}</span>
      </div>

      <!-- Titre principal -->
      <h1 class="serif text-3xl md:text-5xl font-black text-slate-900 mb-6 leading-tight tracking-tight">
        {title}
      </h1>

      <!-- Auteur et signature -->
      <div class="flex items-center gap-4 p-4 bg-white rounded-2xl border border-slate-200 shadow-sm mb-10">
        <img src="../manipulateur.png" alt="Frédéric Murria" class="w-14 h-14 rounded-full object-cover border-2 border-teal-500 shadow">
        <div>
          <p class="font-bold text-slate-900 text-sm">{author}</p>
          <p class="text-xs text-slate-500 font-medium">23 ans d'expertise hospitalière en imagerie (scanner/IRM) • Cabinet à Pinet (34850)</p>
        </div>
      </div>

      <!-- Image de couverture si présente -->
      {f'<div class="mb-10 rounded-3xl overflow-hidden shadow-xl border-4 border-white"><img src="{cover_image}" alt="{title}" class="w-full h-auto object-cover max-h-[450px]"></div>' if cover_image and 'osteo.png' not in cover_image else ''}

      <!-- Encart Consultation Rapide -->
      <div class="bg-gradient-to-r from-teal-900 to-slate-900 text-white p-6 md:p-8 rounded-3xl shadow-xl mb-12 flex flex-col md:flex-row items-center justify-between gap-6 border-2 border-teal-400/40">
        <div>
          <span class="text-teal-400 font-black text-xs uppercase tracking-widest block mb-1">Vous souffrez de douleurs articulaires ou de dos ?</span>
          <p class="text-lg font-bold">Consultez au cabinet de Pinet ou à domicile</p>
          <p class="text-xs text-teal-100 mt-1">Secteur Pinet, Marseillan (7 min), Agde (12 min), Pézenas & Mèze • N° ADELI 340008544</p>
        </div>
        <div class="flex gap-3 shrink-0">
          <a href="tel:+33670605984" class="bg-white text-slate-900 font-black px-5 py-3 rounded-xl text-xs uppercase tracking-wider hover:bg-teal-50 transition shadow">
            <i class="fas fa-phone-alt text-teal-600 mr-1.5"></i> 06 70 60 59 84
          </a>
          <a href="https://rdv.terapiz.com/osteopathe/pinet/frederic-murria" target="_blank" class="bg-teal-500 hover:bg-teal-400 text-slate-900 font-black px-5 py-3 rounded-xl text-xs uppercase tracking-wider transition shadow">
            RDV Terapiz
          </a>
        </div>
      </div>

      <!-- Corps de l'article -->
      <div class="article-body bg-white p-8 md:p-12 rounded-3xl shadow-sm border border-slate-200">
        {clean_html(content_html)}
      </div>

      <!-- Bas d'article & CTA -->
      <div class="mt-12 bg-white p-8 rounded-3xl border-2 border-teal-500 text-center shadow-lg">
        <h3 class="text-2xl font-black text-slate-900 mb-3">Une question sur vos radios, scanner ou douleurs ?</h3>
        <p class="text-slate-600 text-base mb-6 max-w-xl mx-auto leading-relaxed">
          Frédéric Murria vous accueille au cabinet au 21 avenue de Pomerols à Pinet avec <strong>parking gratuit dans la cour</strong>, ou se déplace directement à votre domicile.
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <a href="https://rdv.terapiz.com/osteopathe/pinet/frederic-murria" target="_blank" class="bg-slate-900 text-teal-400 font-black py-4 px-8 rounded-xl shadow-xl hover:bg-slate-800 transition text-sm uppercase tracking-wider">
            Prendre Rendez-vous en Ligne
          </a>
          <a href="../revue-sante.html" class="bg-slate-100 text-slate-800 font-bold py-4 px-8 rounded-xl hover:bg-slate-200 transition text-sm">
            Voir les autres articles
          </a>
        </div>
      </div>

    </article>
  </main>

  <!-- Footer -->
  <footer class="bg-slate-950 text-white py-12 mt-16 border-t border-slate-800">
    <div class="container mx-auto px-4 text-center max-w-4xl">
      <p class="font-black text-xl mb-1 text-teal-400 uppercase tracking-wider">Frédéric Murria — Ostéopathe D.O</p>
      <p class="text-slate-500 text-xs font-bold mb-6 tracking-widest">N° ADELI : 340008544 • Cabinet à Pinet (34850)</p>
      <div class="flex flex-wrap justify-center gap-4 text-xs font-semibold text-slate-400">
        <a href="../index.html" class="hover:text-teal-400">Accueil</a> •
        <a href="../osteopathe-marseillan.html" class="hover:text-teal-400">Marseillan</a> •
        <a href="../osteopathe-agde.html" class="hover:text-teal-400">Agde</a> •
        <a href="../osteopathe-pezenas.html" class="hover:text-teal-400">Pézenas</a> •
        <a href="../osteopathe-meze.html" class="hover:text-teal-400">Mèze</a> •
        <a href="../revue-sante.html" class="hover:text-teal-400">Revue Santé</a> •
        <a href="https://osteomagazine.com" target="_blank" class="hover:text-teal-400">Osteomagazine.com</a>
      </div>
    </div>
  </footer>

</body>
</html>
"""
    filepath = os.path.join(ARTICLES_DIR, f"{slug}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return filepath

def generate_hub_page(registry_items):
    # Sort items by date desc
    sorted_items = sorted(registry_items.values(), key=lambda x: x.get("date", ""), reverse=True)

    cards_html = []
    for item in sorted_items:
        title = item["title"]
        slug = item["slug"]
        desc = item.get("description", "")[:140] + "..."
        date_str = item.get("date", "")[:10]
        cover = item.get("cover_image", "./osteo.png")
        source = item.get("source_name", "Dossier Médical")

        cards_html.append(f"""
        <article class="bg-white rounded-3xl overflow-hidden shadow-lg border border-slate-200 hover:border-teal-400 hover:shadow-2xl transition duration-300 flex flex-col justify-between group">
          <div>
            <div class="h-48 overflow-hidden bg-slate-900 relative">
              <img src="{cover}" alt="{title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy" onerror="this.src='./osteo.png'">
              <span class="absolute top-4 left-4 bg-slate-950/80 backdrop-blur-md text-teal-300 text-[10px] font-black uppercase px-3 py-1 rounded-full tracking-wider border border-teal-500/30">
                {source}
              </span>
            </div>
            <div class="p-6 md:p-8">
              <span class="text-xs text-slate-400 font-semibold block mb-2">{date_str}</span>
              <h3 class="text-xl font-black text-slate-900 mb-3 group-hover:text-teal-600 transition leading-snug">
                <a href="./articles/{slug}.html">{title}</a>
              </h3>
              <p class="text-slate-600 text-sm leading-relaxed mb-6 font-medium">
                {desc}
              </p>
            </div>
          </div>
          <div class="px-6 md:px-8 pb-6 pt-0 border-t border-slate-100 flex justify-between items-center mt-auto">
            <span class="text-xs text-teal-700 font-bold uppercase tracking-wider">Par Frédéric Murria</span>
            <a href="./articles/{slug}.html" class="inline-flex items-center text-xs font-black uppercase text-teal-600 hover:text-teal-800 transition tracking-wider">
              Lire l'article <i class="fas fa-chevron-right ml-1.5 text-[10px]"></i>
            </a>
          </div>
        </article>
        """)

    cards_joined = "\n".join(cards_html)

    hub_html = f"""<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Revue Santé & Guides Cliniques d'Ostéopathie | Frédéric Murria Pinet</title>
  <meta name="description" content="Découvrez tous les articles, conseils cliniques et analyses biomécaniques rédigés par Frédéric Murria, ostéopathe D.O à Pinet (34850).">
  <link rel="canonical" href="https://rdv.osteomagazine.com/revue-sante.html">
  <meta name="robots" content="index, follow">

  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&family=Playfair+Display:ital,wght@0,600;0,800;1,600&display=swap" rel="stylesheet">

  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .serif {{ font-family: 'Playfair Display', serif; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col justify-between">

  <!-- Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-40 border-b border-teal-500/30 backdrop-blur-md bg-slate-900/95">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center max-w-6xl">
      <div class="flex items-center gap-3">
        <a href="./index.html" class="flex items-center gap-3 group">
          <img src="./logo.png" alt="Logo Frédéric Murria" class="w-10 h-10 object-contain">
          <div>
            <span class="text-xl font-bold leading-tight block group-hover:text-teal-300 transition">Frédéric Murria</span>
            <span class="text-xs font-bold text-teal-400 uppercase tracking-widest block">Ostéopathe D.O | Cabinet Pinet</span>
          </div>
        </a>
      </div>
      <div class="flex items-center gap-6">
        <nav class="hidden md:flex space-x-6 font-bold text-xs uppercase tracking-wider">
          <a href="./index.html" class="hover:text-teal-300 transition">Accueil Cabinet</a>
          <a href="./osteopathe-marseillan.html" class="hover:text-teal-300 transition">Marseillan</a>
          <a href="./osteopathe-agde.html" class="hover:text-teal-300 transition">Agde</a>
          <a href="./osteopathe-pezenas.html" class="hover:text-teal-300 transition">Pézenas</a>
          <a href="./osteopathe-meze.html" class="hover:text-teal-300 transition">Mèze</a>
        </nav>
        <a href="https://rdv.terapiz.com/osteopathe/pinet/frederic-murria" target="_blank" class="bg-teal-600 hover:bg-teal-500 text-white font-black text-xs uppercase px-5 py-3 rounded-full shadow-lg transition">
          Prendre RDV
        </a>
      </div>
    </div>
  </header>

  <!-- Hero -->
  <section class="bg-gradient-to-b from-slate-900 to-slate-800 text-white py-16 md:py-24 border-b border-teal-900">
    <div class="container mx-auto px-4 max-w-4xl text-center">
      <span class="text-xs font-black text-teal-400 uppercase tracking-widest mb-3 block">Publication & Vulgarisation Clinique</span>
      <h1 class="serif text-4xl md:text-6xl font-black mb-6 tracking-tight">Revue Santé & Guides d'Ostéopathie</h1>
      <p class="text-lg md:text-xl text-teal-100 max-w-2xl mx-auto leading-relaxed italic">
        Comprendre vos douleurs, le dos, les articulations et l'imagerie médicale. Rédigé par Frédéric Murria, ostéopathe D.O avec 23 ans d'expertise hospitalière en scanner et IRM.
      </p>
    </div>
  </section>

  <!-- Grille d'articles -->
  <main class="py-16 md:py-24">
    <div class="container mx-auto px-4 max-w-6xl">
      <div class="flex justify-between items-center mb-12 border-b border-slate-200 pb-4">
        <div>
          <h2 class="text-2xl font-black text-slate-900">Dossiers & Analyses Récents</h2>
          <p class="text-sm text-slate-500 font-medium">Mis à jour automatiquement avec les publications régulières</p>
        </div>
        <span class="text-xs font-black uppercase text-teal-600 bg-teal-50 px-4 py-2 rounded-full border border-teal-200">
          {len(sorted_items)} articles disponibles
        </span>
      </div>

      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {cards_joined}
      </div>
    </div>
  </main>

  <!-- Banner Cabinet -->
  <section class="bg-teal-900 text-white py-16 border-y border-teal-800">
    <div class="container mx-auto px-4 max-w-4xl text-center">
      <h2 class="text-3xl font-black mb-4">Besoin d'une consultation ou d'un soulagement rapide ?</h2>
      <p class="text-teal-100 text-lg mb-8 max-w-2xl mx-auto">
        Le cabinet de Frédéric Murria vous reçoit à Pinet avec parking privé gratuit, ou se déplace à votre domicile (Marseillan, Agde, Pézenas, Mèze).
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <a href="https://rdv.terapiz.com/osteopathe/pinet/frederic-murria" target="_blank" class="bg-white text-slate-900 font-black px-8 py-4 rounded-xl shadow-xl hover:bg-teal-50 transition text-sm uppercase tracking-wider">
          Prendre RDV en Ligne
        </a>
        <a href="tel:+33670605984" class="bg-teal-600 text-white font-black px-8 py-4 rounded-xl shadow-xl hover:bg-teal-500 transition text-sm uppercase tracking-wider border border-teal-400">
          <i class="fas fa-phone-alt mr-2"></i> 06 70 60 59 84
        </a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-slate-950 text-white py-12">
    <div class="container mx-auto px-4 text-center max-w-4xl">
      <p class="font-black text-xl mb-1 text-teal-400 uppercase tracking-wider">Frédéric Murria — Ostéopathe D.O</p>
      <p class="text-slate-500 text-xs font-bold mb-6 tracking-widest">N° ADELI : 340008544 • Cabinet au 21 avenue de Pomerols, 34850 Pinet</p>
      <div class="flex flex-wrap justify-center gap-4 text-xs font-semibold text-slate-400">
        <a href="./index.html" class="hover:text-teal-400">Accueil</a> •
        <a href="./osteopathe-marseillan.html" class="hover:text-teal-400">Marseillan</a> •
        <a href="./osteopathe-agde.html" class="hover:text-teal-400">Agde</a> •
        <a href="./osteopathe-pezenas.html" class="hover:text-teal-400">Pézenas</a> •
        <a href="./osteopathe-meze.html" class="hover:text-teal-400">Mèze</a> •
        <a href="https://osteomagazine.com" target="_blank" class="hover:text-teal-400">Osteomagazine.com</a>
      </div>
    </div>
  </footer>

</body>
</html>
"""
    hub_path = os.path.join(WORKSPACE, "revue-sante.html")
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(hub_html)
    print("Page hub revue-sante.html mise à jour avec succès !")

def update_sitemap(registry_items):
    sitemap_path = os.path.join(WORKSPACE, "sitemap.xml")
    base_urls = [
        "https://rdv.osteomagazine.com/",
        "https://rdv.osteomagazine.com/osteopathe-marseillan.html",
        "https://rdv.osteomagazine.com/osteopathe-agde.html",
        "https://rdv.osteomagazine.com/osteopathe-pezenas.html",
        "https://rdv.osteomagazine.com/osteopathe-meze.html",
        "https://rdv.osteomagazine.com/revue-sante.html"
    ]
    today = datetime.now().strftime("%Y-%m-%d")

    url_blocks = []
    for u in base_urls:
        pri = "1.0" if u == "https://rdv.osteomagazine.com/" else "0.9"
        url_blocks.append(f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{pri}</priority>
  </url>""")

    for slug, item in registry_items.items():
        article_url = f"https://rdv.osteomagazine.com/articles/{slug}.html"
        item_date = item.get("date", today)[:10]
        url_blocks.append(f"""  <url>
    <loc>{article_url}</loc>
    <lastmod>{item_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_blocks)}
</urlset>
"""
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("sitemap.xml mis à jour avec les nouveaux articles !")

def fetch_substack_posts(limit=25):
    url = f"https://osteomagazine.com/api/v1/posts?limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = urllib.request.urlopen(req, timeout=10).read()
        return json.loads(data)
    except Exception as e:
        print(f"Erreur API Substack: {e}")
        return []

def sync():
    new_articles_count = 0
    print("Synchronisation des articles...")

    # 1. Fetch from Osteomagazine Substack
    substack_posts = fetch_substack_posts(limit=25)
    for p in substack_posts:
        slug = p.get("slug")
        if not slug:
            continue
        if slug in registry:
            continue

        title = p.get("title", "")
        desc = p.get("description", "") or p.get("subtitle", "")
        body = p.get("body_html", "")
        if not body or len(body) < 100:
            continue

        item = {
            "slug": slug,
            "title": title,
            "description": desc,
            "author": "Frédéric Murria — Ostéopathe D.O",
            "date": p.get("post_date", datetime.now().isoformat()),
            "cover_image": p.get("cover_image", "https://rdv.osteomagazine.com/osteo.png"),
            "source_name": "Osteomagazine",
            "canonical_url": p.get("canonical_url", f"https://rdv.osteomagazine.com/articles/{slug}.html"),
            "body_html": body
        }

        generate_article_page(item)
        registry[slug] = {
            "slug": slug,
            "title": title,
            "description": desc,
            "date": item["date"],
            "cover_image": item["cover_image"],
            "source_name": item["source_name"]
        }
        new_articles_count += 1
        print(f" -> Nouvel article généré : {title}")

    # Save registry
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    # Generate Hub & Sitemap
    generate_hub_page(registry)
    update_sitemap(registry)

    print(f"Terminé ! {new_articles_count} nouveaux articles synchronisés.")
    return new_articles_count

if __name__ == "__main__":
    sync()
