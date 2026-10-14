import re
import html
import json

def clean_body_text_and_lists(body_text):
    """
    Nettoie et normalise les espacements et fusionne les tirets isolés
    avant la génération HTML.
    """
    # 1. Fusionner les tirets ou puces orphelins isolés
    body_text = re.sub(r'^\s*[-–—•*◆]\s*\n+\s*([^\n]+)', r'- \1', body_text, flags=re.MULTILINE)
    # 2. Fusionner les numéros orphelins (ex: "1.\n\nRedressez-vous")
    body_text = re.sub(r'^\s*(\d+[\.\)])\s*\n+\s*([^\n]+)', r'\1 \2', body_text, flags=re.MULTILINE)
    # 3. Supprimer les points isolés
    body_text = re.sub(r'^\s*\.\s*$', '', body_text, flags=re.MULTILINE)
    # 4. Supprimer les hashtags Markdown isolés
    body_text = re.sub(r'^\s*#{1,6}\s*$', '', body_text, flags=re.MULTILINE)
    # 5. Supprimer tirets restants isolés
    body_text = re.sub(r'^\s*[-–—•*]\s*$', '', body_text, flags=re.MULTILINE)
    # 6. Éviter les lignes vides excessives
    body_text = re.sub(r'\n{3,}', '\n\n', body_text)
    return body_text.strip()

def generate_prestigious_book():
    with open('livre_osteomagazine/recueil_osteomagazine_complet.md', 'r', encoding='utf-8') as f:
        raw_md = f.read()

    parts_raw = raw_md.split('# PARTIE : ')
    intro_raw = parts_raw[0]

    parts_data = []
    
    for p_block in parts_raw[1:]:
        lines = p_block.strip().split('\n')
        part_title = lines[0].strip()
        part_content = '\n'.join(lines[1:])
        
        chapters_raw = part_content.split('\n## ')
        chapters_data = []
        
        for c_block in chapters_raw:
            c_lines = c_block.strip().split('\n')
            if not c_lines or not c_lines[0].strip():
                continue
            
            c_title = c_lines[0].replace('## ', '').strip()
            if c_title.startswith('='):
                continue

            c_text = '\n'.join(c_lines[1:]).strip()
            
            c_subtitle = ""
            if c_text.startswith('*') and '\n' in c_text:
                first_line, rest = c_text.split('\n', 1)
                c_subtitle = first_line.strip('*').strip()
                c_text = rest.strip()

            c_cover = ""
            cover_match = re.search(r'!\[Illustration principale\]\((.*?)\)', c_text)
            if cover_match:
                c_cover = cover_match.group(1)
                c_text = c_text.replace(cover_match.group(0), '').strip()

            c_text = clean_body_text_and_lists(c_text)

            chapters_data.append({
                'title': c_title,
                'subtitle': c_subtitle,
                'cover': c_cover,
                'body': c_text
            })

        if chapters_data:
            parts_data.append({
                'title': part_title,
                'chapters': chapters_data
            })

    html_out = []
    html_out.append("""<!DOCTYPE html>
<html lang="fr" data-theme="sepia">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Le Grand Guide du Corps & du Mouvement — Frédéric Murria</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>

  <style>
    :root {
      --bg-body: #f7f4ee;
      --bg-page: #fdfbf7;
      --bg-card: #f4efe6;
      --text-main: #242220;
      --text-muted: #6e685f;
      --accent-teal: #0f766e;
      --accent-gold: #c59b27;
      --accent-gold-dark: #977416;
      --border-color: #e5ded0;
      --shadow-paper: 0 15px 45px rgba(30, 25, 15, 0.08), 0 1px 3px rgba(30, 25, 15, 0.05);
      --font-title: 'Cinzel', serif;
      --font-body: 'Cormorant Garamond', Georgia, serif;
      --font-ui: 'Outfit', sans-serif;
      --font-scale: 1.16rem;
    }

    [data-theme="dark"] {
      --bg-body: #0b0f19;
      --bg-page: #111827;
      --bg-card: #1f2937;
      --text-main: #e2e8f0;
      --text-muted: #94a3b8;
      --accent-teal: #2dd4bf;
      --accent-gold: #fbbf24;
      --accent-gold-dark: #d97706;
      --border-color: #374151;
      --shadow-paper: 0 20px 50px rgba(0, 0, 0, 0.5);
    }

    [data-theme="white"] {
      --bg-body: #f8fafc;
      --bg-page: #ffffff;
      --bg-card: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #475569;
      --accent-teal: #0d9488;
      --accent-gold: #b45309;
      --border-color: #e2e8f0;
      --shadow-paper: 0 15px 40px rgba(0, 0, 0, 0.06);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }

    body {
      background-color: var(--bg-body);
      color: var(--text-main);
      font-family: var(--font-body);
      font-size: var(--font-scale);
      line-height: 1.85;
      margin: 0;
      padding: 0;
      transition: background-color 0.3s, color 0.3s;
    }

    .top-reader-bar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--bg-page);
      border-bottom: 1px solid var(--border-color);
      box-shadow: 0 4px 20px rgba(0,0,0,0.05);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-ui);
    }
    .top-reader-bar .title-badge {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      font-size: 0.95rem;
      color: var(--accent-teal);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .reader-controls {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    .btn-ctrl {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: 8px;
      font-family: var(--font-ui);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-ctrl:hover {
      border-color: var(--accent-gold);
      color: var(--accent-gold-dark);
      transform: translateY(-1px);
    }

    .book-wrapper {
      max-width: 940px;
      margin: 40px auto 100px;
      background: var(--bg-page);
      box-shadow: var(--shadow-paper);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border-color);
    }

    .book-cover {
      background: linear-gradient(145deg, #07191d 0%, #0d2e35 50%, #061518 100%);
      color: #fdfbf7;
      padding: 120px 60px 100px;
      text-align: center;
      position: relative;
      border-bottom: 6px solid #c59b27;
      box-shadow: inset 0 0 100px rgba(0,0,0,0.6);
    }
    .cover-frame {
      border: 2px solid rgba(197, 155, 39, 0.4);
      padding: 50px 30px;
      position: relative;
    }
    .cover-frame::before {
      content: '';
      position: absolute;
      top: 6px; left: 6px; right: 6px; bottom: 6px;
      border: 1px solid rgba(197, 155, 39, 0.2);
      pointer-events: none;
    }
    .cover-tagline {
      font-family: var(--font-ui);
      text-transform: uppercase;
      letter-spacing: 0.35em;
      font-size: 0.85rem;
      color: #c59b27;
      margin-bottom: 24px;
      font-weight: 600;
    }
    .cover-title {
      font-family: var(--font-title);
      font-size: 3.2rem;
      font-weight: 900;
      line-height: 1.2;
      letter-spacing: 0.04em;
      margin: 0 0 20px;
      color: #ffffff;
      text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .cover-subtitle {
      font-family: var(--font-body);
      font-size: 1.55rem;
      font-style: italic;
      color: #b2d8d8;
      max-width: 680px;
      margin: 0 auto 40px;
      line-height: 1.5;
    }
    .cover-divider {
      width: 80px;
      height: 2px;
      background: #c59b27;
      margin: 30px auto;
    }
    .cover-author {
      font-family: var(--font-title);
      font-size: 1.6rem;
      letter-spacing: 0.15em;
      color: #ffffff;
      margin-bottom: 8px;
    }
    .cover-role {
      font-family: var(--font-ui);
      font-size: 0.9rem;
      letter-spacing: 0.1em;
      color: #c59b27;
      text-transform: uppercase;
      font-weight: 500;
    }

    .preface-card {
      padding: 80px 90px 40px;
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-color);
    }
    .preface-inner {
      display: flex;
      gap: 40px;
      align-items: center;
    }
    .preface-photo {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      object-fit: cover;
      box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      border: 4px solid var(--accent-gold);
      flex-shrink: 0;
    }
    .preface-quote {
      font-style: italic;
      font-size: 1.35rem;
      line-height: 1.6;
      color: var(--accent-teal);
      border-left: 3px solid var(--accent-gold);
      padding-left: 24px;
      margin: 0;
    }

    .toc-section {
      padding: 80px 90px;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-page);
    }
    .toc-header {
      text-align: center;
      margin-bottom: 50px;
    }
    .toc-header h2 {
      font-family: var(--font-title);
      font-size: 2.2rem;
      letter-spacing: 0.08em;
      color: var(--text-main);
      margin: 0 0 10px;
    }
    .toc-grid {
      display: grid;
      gap: 30px;
    }
    .toc-part-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 24px 30px;
      transition: all 0.2s;
    }
    .toc-part-title {
      font-family: var(--font-title);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--accent-teal);
      letter-spacing: 0.05em;
      margin: 0 0 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .toc-part-card ul {
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 8px;
    }
    .toc-part-card li a {
      color: var(--text-main);
      text-decoration: none;
      font-size: 1.05rem;
      display: flex;
      align-items: baseline;
      gap: 10px;
      transition: color 0.2s;
    }
    .toc-part-card li a:hover {
      color: var(--accent-gold-dark);
    }
    .toc-part-card li a::before {
      content: '◆';
      font-size: 0.65rem;
      color: var(--accent-gold);
    }

    .part-banner {
      background: linear-gradient(135deg, rgba(15,118,110,0.08) 0%, rgba(197,155,39,0.08) 100%);
      padding: 90px 60px;
      text-align: center;
      border-top: 1px solid var(--border-color);
      border-bottom: 1px solid var(--border-color);
      margin: 60px 0;
      position: relative;
    }
    .part-banner-tag {
      font-family: var(--font-ui);
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.3em;
      text-transform: uppercase;
      color: var(--accent-gold-dark);
      margin-bottom: 16px;
    }
    .part-banner-title {
      font-family: var(--font-title);
      font-size: 2.3rem;
      font-weight: 900;
      color: var(--accent-teal);
      margin: 0;
      letter-spacing: 0.04em;
    }

    .chapter-article {
      padding: 50px 90px;
      border-bottom: 1px solid var(--border-color);
      position: relative;
    }
    .chapter-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-ui);
      font-size: 0.82rem;
      font-weight: 600;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--accent-gold-dark);
      margin-bottom: 12px;
    }
    .chapter-title {
      font-family: var(--font-title);
      font-size: 2.2rem;
      font-weight: 700;
      line-height: 1.25;
      color: var(--text-main);
      margin: 0 0 16px;
      letter-spacing: 0.02em;
    }
    .chapter-subtitle {
      font-family: var(--font-body);
      font-size: 1.35rem;
      font-style: italic;
      color: var(--accent-teal);
      margin-bottom: 35px;
      line-height: 1.5;
    }
    
    .chapter-body > p:first-of-type::first-letter {
      font-family: var(--font-title);
      font-size: 3.6rem;
      float: left;
      line-height: 0.8;
      padding-top: 4px;
      padding-right: 12px;
      padding-bottom: 4px;
      color: var(--accent-teal);
      font-weight: 700;
    }

    /* ESPACEMENTS DE TEXTE HARMONIEUX (STYLE LIVRE) */
    .chapter-body p {
      margin-top: 0;
      margin-bottom: 1.35em;
      text-align: justify;
      hyphens: auto;
    }
    .chapter-body h3 {
      font-family: var(--font-ui);
      font-size: 1.3rem;
      font-weight: 700;
      color: var(--accent-teal);
      margin-top: 36px;
      margin-bottom: 14px;
      letter-spacing: -0.01em;
      border-left: 3px solid var(--accent-gold);
      padding-left: 14px;
    }

    /* LISTES COMPACTES ET ÉLÉGANTES (PAS DE VIDES ANORMAUX) */
    .chapter-body ul.book-list {
      margin: 16px 0 24px;
      padding: 0;
      list-style: none;
    }
    .chapter-body ul.book-list li {
      margin-bottom: 8px;
      position: relative;
      padding-left: 24px;
      line-height: 1.65;
    }
    .chapter-body ul.book-list li::before {
      content: '◆';
      position: absolute;
      left: 2px;
      top: 0;
      color: var(--accent-gold);
      font-size: 0.75rem;
    }

    .book-figure {
      margin: 36px 0;
      text-align: center;
      background: var(--bg-card);
      padding: 14px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    }
    .book-figure img {
      max-width: 100%;
      max-height: 520px;
      height: auto;
      border-radius: 8px;
      display: inline-block;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .book-figure figcaption {
      font-family: var(--font-ui);
      font-size: 0.85rem;
      font-weight: 500;
      color: var(--text-muted);
      margin-top: 10px;
      font-style: italic;
    }

    .floating-toc-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 1001;
      background: var(--accent-teal);
      color: white;
      border: none;
      width: 54px;
      height: 54px;
      border-radius: 50%;
      box-shadow: 0 8px 25px rgba(15,118,110,0.35);
      cursor: pointer;
      font-size: 1.3rem;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s;
    }
    .floating-toc-btn:hover {
      transform: scale(1.1);
    }
    .toc-modal {
      position: fixed;
      top: 0; right: -420px;
      width: 400px;
      height: 100vh;
      background: var(--bg-page);
      border-left: 2px solid var(--border-color);
      box-shadow: -10px 0 30px rgba(0,0,0,0.15);
      z-index: 1002;
      transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
      padding: 30px;
      font-family: var(--font-ui);
    }
    .toc-modal.open {
      right: 0;
    }
    .toc-modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 15px;
      margin-bottom: 20px;
    }

    .book-colophon {
      padding: 80px 40px;
      text-align: center;
      background: var(--bg-card);
      font-family: var(--font-ui);
      font-size: 0.9rem;
      color: var(--text-muted);
    }

    @media print {
      .top-reader-bar, .floating-toc-btn, .toc-modal { display: none !important; }
      body { background: white !important; color: black !important; font-size: 11pt; }
      .book-wrapper { box-shadow: none; border: none; margin: 0; max-width: 100%; border-radius: 0; }
      .book-cover { page-break-after: always; padding: 180px 40px; }
      .part-banner { page-break-before: always; page-break-after: always; padding: 200px 40px; }
      .chapter-article { page-break-before: always; padding: 40px 0; border: none; }
      .book-figure { page-break-inside: avoid; border: none; background: none; box-shadow: none; }
      .book-figure img { max-height: 400px; box-shadow: none; }
      p, li { orphans: 3; widows: 3; }
    }

    @media (max-width: 768px) {
      .book-wrapper { margin: 0; border-radius: 0; border: none; }
      .book-cover { padding: 60px 24px; }
      .cover-title { font-size: 2.2rem; }
      .preface-card, .toc-section, .chapter-article { padding: 40px 24px; }
      .preface-inner { flex-direction: column; text-align: center; }
    }
  </style>
</head>
<body>

  <div class="top-reader-bar">
    <div class="title-badge">
      <i class="fas fa-book-medical"></i>
      <span>Le Guide Global du Corps & du Mouvement</span>
    </div>
    <div class="reader-controls">
      <button class="btn-ctrl" onclick="changeTheme('sepia')"><i class="fas fa-scroll"></i> Livre</button>
      <button class="btn-ctrl" onclick="changeTheme('white')"><i class="fas fa-sun"></i> Clair</button>
      <button class="btn-ctrl" onclick="changeTheme('dark')"><i class="fas fa-moon"></i> Sombre</button>
      <button class="btn-ctrl" onclick="adjustFont(-1)">A-</button>
      <button class="btn-ctrl" onclick="adjustFont(1)">A+</button>
      <button class="btn-ctrl" onclick="window.print()" style="background: var(--accent-teal); color: white; border: none;">
        <i class="fas fa-print"></i> Exporter PDF
      </button>
    </div>
  </div>

  <div class="book-wrapper">

    <div class="book-cover">
      <div class="cover-frame">
        <div class="cover-tagline">Édition Intégrale de Référence • 78 Chapitres</div>
        <h1 class="cover-title">LE GUIDE DU CORPS & DU MOUVEMENT</h1>
        <div class="cover-subtitle">Comprendre, soulager et optimiser sa santé mécanique à la lumière de 23 ans d'imagerie médicale et d'ostéopathie</div>
        <div class="cover-divider"></div>
        <div class="cover-author">FRÉDÉRIC MURRIA</div>
        <div class="cover-role">Ostéopathe D.O — Ancien Manipulateur Radio Scanner & IRM</div>
      </div>
    </div>

    <div class="preface-card">
      <div class="preface-inner">
        <img src="../manipulateur.png" alt="Frédéric Murria" class="preface-photo">
        <div>
          <blockquote class="preface-quote">
            « L'imagerie médicale nous montre avec une précision chirurgicale l'état de nos disques et de nos articulations. L'ostéopathie nous apprend à leur redonner vie et liberté de mouvement. Ce livre est la synthèse de ces deux mondes. »
          </blockquote>
          <p style="margin-top: 16px; font-family: var(--font-ui); font-size: 0.95rem; font-weight: 600; color: var(--accent-gold-dark);">
            — Frédéric Murria, Cabinet d'Ostéopathie de Pinet
          </p>
        </div>
      </div>
    </div>

    <div class="toc-section" id="table-des-matieres">
      <div class="toc-header">
        <h2>SOMMAIRE GÉNÉRAL</h2>
        <div style="font-family: var(--font-ui); font-size: 0.95rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.2em;">
          6 Grandes Parties • 78 Chapitres Cliniques
        </div>
      </div>
      <div class="toc-grid">
""")

    for p_idx, part in enumerate(parts_data):
        html_out.append(f"""
        <div class="toc-part-card">
          <div class="toc-part-title">
            <span>PARTIE {p_idx+1} : {html.escape(part['title'])}</span>
            <span style="font-size: 0.8rem; font-family: var(--font-ui); opacity: 0.8;">{len(part['chapters'])} chapitres</span>
          </div>
          <ul>
        """)
        for c_idx, chap in enumerate(part['chapters']):
            c_slug = f"part-{p_idx+1}-chap-{c_idx+1}"
            html_out.append(f'<li><a href="#{c_slug}">{html.escape(chap["title"])}</a></li>')
        html_out.append("""
          </ul>
        </div>
        """)

    html_out.append("""
      </div>
    </div>
""")

    global_chap_counter = 0

    for p_idx, part in enumerate(parts_data):
        html_out.append(f"""
        <div class="part-banner" id="partie-{p_idx+1}">
          <div class="part-banner-tag">Partie {p_idx+1}</div>
          <h2 class="part-banner-title">{html.escape(part['title'])}</h2>
        </div>
        """)

        for c_idx, chap in enumerate(part['chapters']):
            global_chap_counter += 1
            c_slug = f"part-{p_idx+1}-chap-{c_idx+1}"
            
            body_lines = chap['body'].split('\n')
            formatted_body = []
            in_list = False
            
            for line in body_lines:
                line_s = line.strip()
                if not line_s:
                    if in_list:
                        formatted_body.append("</ul>")
                        in_list = False
                    continue

                # Traitement des images
                img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', line_s)
                if img_match:
                    if in_list:
                        formatted_body.append("</ul>")
                        in_list = False
                    alt_t = img_match.group(1).strip()
                    src_u = img_match.group(2).strip()
                    caption_h = f"<figcaption>{html.escape(alt_t)}</figcaption>" if alt_t else ""
                    formatted_body.append(f"""
                    <figure class="book-figure">
                      <img src="{html.escape(src_u)}" alt="{html.escape(alt_t)}" loading="lazy">
                      {caption_h}
                    </figure>
                    """)
                    continue

                if line_s.startswith('### '):
                    if in_list:
                        formatted_body.append("</ul>")
                        in_list = False
                    h_text = line_s[4:].strip()
                    formatted_body.append(f"<h3>{html.escape(h_text)}</h3>")
                elif line_s.startswith('- ') or line_s.startswith('◆ ') or line_s.startswith('✓ ') or line_s.startswith('✗ '):
                    if not in_list:
                        formatted_body.append('<ul class="book-list">')
                        in_list = True
                    item_t = re.sub(r'^[-\s◆✓✗]+', '', line_s).strip()
                    item_t = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(item_t))
                    formatted_body.append(f"<li>{item_t}</li>")
                elif re.match(r'^\d+[\.\)]\s+', line_s):
                    # Élément de liste numérotée (ex: "1. Redressez-vous !")
                    if in_list:
                        formatted_body.append("</ul>")
                        in_list = False
                    num_match = re.match(r'^(\d+[\.\)])\s+(.*)', line_s)
                    num_prefix = num_match.group(1)
                    num_content = num_match.group(2)
                    num_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(num_content))
                    formatted_body.append(f'<p style="font-weight: 700; color: var(--accent-teal); margin-top: 24px; margin-bottom: 8px;"><span style="color: var(--accent-gold-dark); margin-right: 6px;">{num_prefix}</span> {num_content}</p>')
                elif line_s == "---" or line_s.startswith("====="):
                    if in_list:
                        formatted_body.append("</ul>")
                        in_list = False
                    formatted_body.append("<hr>")
                else:
                    if in_list:
                        formatted_body.append("</ul>")
                        in_list = False
                    p_t = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(line_s))
                    p_t = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_t)
                    formatted_body.append(f"<p>{p_t}</p>")

            if in_list:
                formatted_body.append("</ul>")

            cover_figure = ""
            if chap['cover']:
                cover_figure = f"""
                <figure class="book-figure" style="margin-top: 10px;">
                  <img src="{html.escape(chap['cover'])}" alt="{html.escape(chap['title'])}" loading="lazy">
                </figure>
                """

            subtitle_html = f"<div class=\"chapter-subtitle\">{html.escape(chap['subtitle'])}</div>" if chap['subtitle'] else ""

            html_out.append(f"""
            <article class="chapter-article" id="{c_slug}">
              <div class="chapter-meta">
                <span>Chapitre {global_chap_counter:02d}</span>
                <span>•</span>
                <span>Partie {p_idx+1}</span>
              </div>
              <h2 class="chapter-title">{html.escape(chap['title'])}</h2>
              {subtitle_html}
              {cover_figure}
              <div class="chapter-body">
                {' '.join(formatted_body)}
              </div>
            </article>
            """)

    html_out.append("""
      <div class="book-colophon">
        <p style="font-family: var(--font-title); font-size: 1.2rem; color: var(--accent-teal); margin-bottom: 8px;">
          LE GUIDE DU CORPS & DU MOUVEMENT
        </p>
        <p>Achevé de rédiger et compilé par Frédéric Murria, Ostéopathe D.O.</p>
        <p style="font-size: 0.8rem; opacity: 0.7;">© 2026 Frédéric Murria • Tous droits réservés • Pinet, France</p>
      </div>

  </div> <!-- Fin .book-wrapper -->

  <button class="floating-toc-btn" onclick="toggleTocModal()" title="Ouvrir le Sommaire">
    <i class="fas fa-list-ul"></i>
  </button>

  <div class="toc-modal" id="tocModal">
    <div class="toc-modal-header">
      <h3 style="margin: 0; font-family: var(--font-title); color: var(--accent-teal); font-size: 1.1rem;">Sommaire</h3>
      <button onclick="toggleTocModal()" style="background: none; border: none; font-size: 1.4rem; cursor: pointer; color: var(--text-muted);">&times;</button>
    </div>
    <div id="modalLinks" style="display: grid; gap: 8px;">
      <a href="#table-des-matieres" onclick="toggleTocModal()" style="font-weight: 700; color: var(--accent-gold-dark); text-decoration: none; margin-bottom: 12px; display: block;">
        ↑ Haut du livre & Sommaire complet
      </a>
    </div>
  </div>

  <script>
    function changeTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
    }

    let currentScale = 1.16;
    function adjustFont(delta) {
      currentScale += (delta * 0.08);
      if (currentScale < 0.9) currentScale = 0.9;
      if (currentScale > 1.6) currentScale = 1.6;
      document.documentElement.style.setProperty('--font-scale', currentScale + 'rem');
    }

    function toggleTocModal() {
      const modal = document.getElementById('tocModal');
      modal.classList.toggle('open');
    }

    document.addEventListener('DOMContentLoaded', () => {
      const modalLinks = document.getElementById('modalLinks');
      const articles = document.querySelectorAll('.chapter-article');
      articles.forEach((art, idx) => {
        const title = art.querySelector('.chapter-title').innerText;
        const link = document.createElement('a');
        link.href = '#' + art.id;
        link.innerText = (idx + 1) + '. ' + title;
        link.style.fontSize = '0.85rem';
        link.style.textDecoration = 'none';
        link.style.color = 'var(--text-main)';
        link.style.padding = '4px 0';
        link.style.borderBottom = '1px solid var(--border-color)';
        link.onclick = toggleTocModal;
        modalLinks.appendChild(link);
      });
    });
  </script>
</body>
</html>
""")

    out_file = "livre_osteomagazine/livre_complet.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write('\n'.join(html_out))

    print(f"Livre d'Édition Prestige réactualisé sans espacements anormaux dans : {out_file}")

if __name__ == '__main__':
    generate_prestigious_book()
