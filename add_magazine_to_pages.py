import re

pages = [
    {
        "file": "osteopathe-marseillan.html",
        "city": "Marseillan"
    },
    {
        "file": "osteopathe-agde.html",
        "city": "Agde"
    },
    {
        "file": "osteopathe-pezenas.html",
        "city": "Pézenas"
    },
    {
        "file": "osteopathe-meze.html",
        "city": "Mèze"
    }
]

blog_section = """
  <!-- Section Osteomagazine -->
  <section id="blog" class="py-24 bg-slate-900 text-white border-y border-teal-900/50">
    <div class="container mx-auto px-4 max-w-4xl text-center">
        <span class="text-xs font-black text-teal-400 uppercase tracking-widest block mb-3">Publication clinique & Vulgarisation médicale</span>
        <h2 class="text-3xl md:text-5xl font-black mb-4 tracking-tighter">Le Magazine Santé par Frédéric Murria</h2>
        <p class="text-xl text-teal-300 mb-12 italic font-medium">Comprendre vos maux de dos, la biomécanique et l'imagerie médicale</p>
        
        <div id="blog-container">
            <div class="bg-white/5 p-8 md:p-10 rounded-3xl border-2 border-white/10 hover:border-teal-400 transition-all group backdrop-blur-md">
                <span class="text-xs font-black text-teal-400 uppercase tracking-widest mb-4 block underline italic">Dernier article à la une d'Osteomagazine :</span>
                <a id="latest-post-title" href="https://osteomagazine.com" target="_blank" class="text-2xl md:text-3xl font-black text-white group-hover:text-teal-400 leading-tight block mb-4 transition">
                    Chargement de l'actualité...
                </a>
                <p id="latest-post-desc" class="text-teal-100 mb-8 text-base md:text-lg line-clamp-3 italic leading-relaxed"></p>
                <div class="flex flex-col sm:flex-row justify-center gap-4">
                  <a id="latest-post-btn" href="https://osteomagazine.com" target="_blank" class="inline-block bg-teal-500 text-slate-900 font-black px-8 py-3.5 rounded-full shadow-2xl hover:bg-teal-400 transition transform group-hover:scale-105 text-sm uppercase tracking-wider">
                      Lire l'article complet
                  </a>
                  <a href="https://osteomagazine.com" target="_blank" class="inline-block bg-transparent text-white border-2 border-teal-400 font-black px-8 py-3.5 rounded-full hover:bg-teal-400/20 transition text-sm uppercase tracking-wider">
                      Explorer Osteomagazine.com (78+ articles)
                  </a>
                </div>
            </div>
        </div>
    </div>
  </section>
"""

footer_card = """
        <div class="max-w-2xl mx-auto bg-slate-900 p-6 rounded-2xl border border-slate-800 mt-8 mb-6 text-center">
          <p class="text-sm text-slate-300 mb-2">
            <strong class="text-teal-400">Osteomagazine.com</strong> : découvrez la publication santé et vulgarisation clinique rédigée par Frédéric Murria.
          </p>
          <a href="https://osteomagazine.com" target="_blank" class="text-xs uppercase tracking-widest font-black text-teal-400 hover:text-teal-300 underline inline-flex items-center gap-2">
            Accéder aux 78+ guides cliniques & imagerie <i class="fas fa-external-link-alt text-[10px]"></i>
          </a>
        </div>
"""

js_snippet = """
    // RSS OSTEOMAGAZINE - Titre + Apercu dynamique
    fetch('https://api.rss2json.com/v1/api.json?rss_url=https://osteomagazine.com/feed')
    .then(res => res.json())
    .then(data => {
        if (data.status === 'ok' && data.items && data.items.length > 0) {
            const post = data.items[0];
            const titleEl = document.getElementById('latest-post-title');
            const descEl = document.getElementById('latest-post-desc');
            const btnEl = document.getElementById('latest-post-btn');
            if (titleEl) {
                titleEl.innerText = post.title;
                titleEl.href = post.link;
            }
            if (descEl) {
                let preview = post.description.replace(/<[^>]*>?/gm, '');
                descEl.innerText = preview.substring(0, 180) + '...';
            }
            if (btnEl) {
                btnEl.href = post.link;
            }
        }
    })
    .catch(() => {
        const titleEl = document.getElementById('latest-post-title');
        if (titleEl) {
            titleEl.innerText = "Consulter les articles cliniques sur Osteomagazine.com";
        }
    });
"""

for item in pages:
    filepath = item["file"]
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update navbar if not already updated
    if '<a href="#blog"' not in content:
        content = content.replace(
            '<a href="#contact" class="nav-link hover:text-teal-400 transition">Contact</a>',
            '<a href="#blog" class="nav-link hover:text-teal-400 transition">Magazine</a>\n            <a href="#faq" class="nav-link hover:text-teal-400 transition">FAQ</a>\n            <a href="#contact" class="nav-link hover:text-teal-400 transition">Contact</a>'
        )

    # 2. Insert blog section before <section id="faq"
    if 'id="blog"' not in content and '<section id="faq"' in content:
        content = content.replace('<section id="faq"', blog_section + '\n  <section id="faq"')

    # 3. Insert footer card if not already present
    if 'Osteomagazine.com' not in content:
        content = content.replace(
            '<div class="max-w-3xl mx-auto border-t border-slate-800 pt-8 mt-8">',
            footer_card + '\n        <div class="max-w-3xl mx-auto border-t border-slate-800 pt-8 mt-8">'
        )

    # 4. Insert JS snippet if not present
    if 'fetch(\'https://api.rss2json.com/v1/api.json?rss_url=https://osteomagazine.com/feed\')' not in content:
        content = content.replace('const form = document.getElementById("contact-form");', js_snippet + '\n    const form = document.getElementById("contact-form");')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Page {filepath} enrichie avec succès !")
