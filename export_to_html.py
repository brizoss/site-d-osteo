import re
import html

def md_to_html():
    with open('livre_osteomagazine/recueil_osteomagazine_complet.md', 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    html_lines = []
    
    html_lines.append("""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Le Guide Global du Corps & du Mouvement - Frédéric Murria</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
    
    body {
      font-family: 'Merriweather', Georgia, serif;
      line-height: 1.85;
      color: #1e293b;
      background: #f1f5f9;
      margin: 0;
      padding: 0;
    }
    .book-container {
      max-width: 860px;
      margin: 40px auto;
      background: #ffffff;
      padding: 70px 90px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.06);
      border-radius: 16px;
    }
    h1, h2, h3, h4 {
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #0f172a;
      line-height: 1.35;
      letter-spacing: -0.01em;
    }
    h1 {
      font-size: 2.1rem;
      font-weight: 800;
      margin-top: 50px;
      margin-bottom: 24px;
      color: #0f766e;
      border-bottom: 2px solid #0f766e;
      padding-bottom: 12px;
    }
    h2 {
      font-size: 1.6rem;
      font-weight: 700;
      margin-top: 45px;
      margin-bottom: 16px;
      color: #0f172a;
    }
    h3 {
      font-size: 1.2rem;
      font-weight: 600;
      margin-top: 28px;
      margin-bottom: 14px;
      color: #334155;
    }
    p {
      margin-bottom: 1.6em;
      text-align: justify;
      font-size: 1.05rem;
      color: #334155;
    }
    hr {
      border: 0;
      height: 1px;
      background: #e2e8f0;
      margin: 50px 0;
    }
    ul, ol {
      margin-bottom: 1.6em;
      padding-left: 28px;
    }
    li {
      margin-bottom: 8px;
      color: #334155;
    }
    /* Style sobre pour les images médicales */
    .book-figure {
      margin: 35px auto;
      text-align: center;
      max-width: 720px;
    }
    .book-figure img {
      max-width: 100%;
      max-height: 520px;
      height: auto;
      border-radius: 10px;
      box-shadow: 0 6px 25px rgba(0,0,0,0.08);
      border: 1px solid #e2e8f0;
      display: inline-block;
    }
    .book-figure figcaption {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.88rem;
      color: #64748b;
      margin-top: 10px;
      font-style: italic;
    }
    /* Puces personnalisées élégantes */
    .bullet-diamond {
      color: #0d9488;
      font-weight: bold;
      margin-right: 6px;
    }
    .bullet-check {
      color: #059669;
      font-weight: bold;
      margin-right: 6px;
    }
    .bullet-cross {
      color: #dc2626;
      font-weight: bold;
      margin-right: 6px;
    }
    @media print {
      body { background: white; }
      .book-container { box-shadow: none; padding: 0; margin: 0; max-width: 100%; border-radius: 0; }
      h1, h2 { page-break-before: always; }
      .book-figure { page-break-inside: avoid; }
      .book-figure img { max-height: 420px; }
      p, li { orphans: 3; widows: 3; }
    }
  </style>
</head>
<body>
  <div class="book-container">
""")

    in_list = False
    for line in lines:
        line_s = line.strip()
        if not line_s:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Détection des images Markdown : ![alt](src)
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', line_s)
        if img_match:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            alt_text = img_match.group(1).strip()
            src_url = img_match.group(2).strip()
            caption_html = ""
            if alt_text and not alt_text.startswith("Illustration principale"):
                caption_html = f"<figcaption>{html.escape(alt_text)}</figcaption>"
            html_lines.append(f"""
            <figure class="book-figure">
              <img src="{html.escape(src_url)}" alt="{html.escape(alt_text)}" loading="lazy">
              {caption_html}
            </figure>
            """)
            continue

        if line_s.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title_text = line_s[2:].strip()
            html_lines.append(f"<h1>{html.escape(title_text)}</h1>")
        elif line_s.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title_text = line_s[3:].strip()
            html_lines.append(f"<h2>{html.escape(title_text)}</h2>")
        elif line_s.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title_text = line_s[4:].strip()
            html_lines.append(f"<h3>{html.escape(title_text)}</h3>")
        elif line_s.startswith("- ") or line_s.startswith("◆ ") or line_s.startswith("✓ ") or line_s.startswith("✗ "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            
            bullet_prefix = ""
            if line_s.startswith("◆ "):
                bullet_prefix = '<span class="bullet-diamond">◆</span> '
                item_text = line_s[2:].strip()
            elif line_s.startswith("✓ "):
                bullet_prefix = '<span class="bullet-check">✓</span> '
                item_text = line_s[2:].strip()
            elif line_s.startswith("✗ "):
                bullet_prefix = '<span class="bullet-cross">✗</span> '
                item_text = line_s[2:].strip()
            else:
                item_text = line_s[2:].strip()

            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(item_text))
            item_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', item_text)
            html_lines.append(f"<li>{bullet_prefix}{item_text}</li>")
        elif line_s == "---" or line_s.startswith("====="):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<hr>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(line_s))
            p_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_text)
            html_lines.append(f"<p>{p_text}</p>")

    if in_list:
        html_lines.append("</ul>")

    html_lines.append("""
  </div>
</body>
</html>
""")

    out_path = 'livre_osteomagazine/livre_complet.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    print(f"Livre HTML épuré généré dans : {out_path}")

if __name__ == '__main__':
    md_to_html()
