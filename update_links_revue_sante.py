import re

files = [
    "index.html",
    "osteopathe-marseillan.html",
    "osteopathe-agde.html",
    "osteopathe-pezenas.html",
    "osteopathe-meze.html"
]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()

    # Link in navbar
    c = c.replace(
        '<a href="#blog" class="nav-link hover:text-teal-400 transition">Magazine</a>',
        '<a href="./revue-sante.html" class="nav-link hover:text-teal-400 transition">Revue Santé</a>'
    )

    # Secondary button in blog section to view the hub
    c = c.replace(
        'Explorer Osteomagazine.com (78+ articles)',
        'Accéder aux dossiers cliniques (Revue Santé)'
    )
    c = c.replace(
        'href="https://osteomagazine.com" target="_blank" class="inline-block bg-transparent text-white border-2 border-teal-400 font-black px-8 py-3.5 rounded-full hover:bg-teal-400/20 transition text-sm uppercase tracking-wider"',
        'href="./revue-sante.html" class="inline-block bg-transparent text-white border-2 border-teal-400 font-black px-8 py-3.5 rounded-full hover:bg-teal-400/20 transition text-sm uppercase tracking-wider"'
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Lien Revue Santé mis à jour dans {fpath}")
