import re

pages_config = [
    {
        "filename": "osteopathe-marseillan.html",
        "city": "Marseillan",
        "postcode": "34340",
        "travel_time": "7 minutes",
        "faq": [
            {
                "q": "Pourquoi consulter un ostéopathe à 7 min de Marseillan plutôt qu'en centre-ville ?",
                "a": "Le cabinet de Frédéric Murria à Pinet est situé à seulement 7 minutes de Marseillan via la D18. Le principal atout est son **parking privé gratuit dans la cour** : vous évitez ainsi les parcmètres et les difficultés de stationnement du port ou du centre-ville de Marseillan, pour une séance sans stress."
            },
            {
                "q": "Quels motifs de consultation sont traités pour les patients de Marseillan ?",
                "a": "Frédéric Murria prend en charge les **urgences du dos (lumbago, sciatique, hernie discale, cruralgie)**, les douleurs cervicales et torticolis, les migraines d'origine posturale, ainsi que les **sportifs** (activités nautiques de l'Étang de Thau, cyclistes), les nourrissons et les femmes enceintes."
            },
            {
                "q": "Comment réserver une consultation d'ostéopathie à domicile sur Marseillan (34340) ?",
                "a": "Si vous êtes dans l'incapacité de vous déplacer (dos bloqué, personne âgée), Frédéric Murria se déplace avec sa table de pratique directement à votre domicile sur **Marseillan Ville et Marseillan Plage**. Le tarif est de **70 €** pour un créneau dédié de 2h incluant le trajet et le soin."
            },
            {
                "q": "Les consultations sont-elles remboursées par ma mutuelle santé ?",
                "a": "Oui ! Même sans prise en charge par la Sécurité Sociale, la majorité des mutuelles remboursent les séances d'ostéopathie. Une facture officielle certifiée avec le **numéro ADELI 340008544** vous est délivrée en fin de consultation."
            }
        ]
    },
    {
        "filename": "osteopathe-agde.html",
        "city": "Agde",
        "postcode": "34300",
        "travel_time": "12 minutes",
        "faq": [
            {
                "q": "Quel est le temps d'accès depuis Agde et où se garer ?",
                "a": "Le cabinet est situé à seulement **12 minutes d'Agde** (environ 11 km via la D51 ou D18). Contrairement à Agde où les places sont souvent payantes ou rares en haute saison, vous bénéficiez d'un **parking privé gratuit et sécurisé dans la cour** du cabinet au 21 avenue de Pomerols à Pinet."
            },
            {
                "q": "Prenez-vous en charge les urgences de dos bloqué pour les résidents d'Agde ?",
                "a": "Oui, les créneaux d'urgence pour **lumbago violent, sciatique aiguë ou torticolis** sont prioritaires. Vous pouvez réserver directement en ligne sur Terapiz ou joindre directement Frédéric Murria au **06 70 60 59 84** pour un soulagement rapide."
            },
            {
                "q": "Consultez-vous à domicile sur Agde, Le Grau d'Agde et Cap d'Agde ?",
                "a": "Tout à fait. Frédéric Murria propose un service d'ostéopathie à domicile sur l'ensemble de la commune d'Agde (34300). La séance à domicile (70 €) comprend le déplacement avec matériel professionnel adapté."
            },
            {
                "q": "En quoi votre expertise en imagerie médicale (radios, scanner, IRM) est-elle un atout ?",
                "a": "Fort de 23 ans d'exercice en milieu hospitalier en scanner et IRM, Frédéric Murria sait décrypter vos examens d'imagerie. Cela garantit un traitement d'ostéopathie sécurisant, ciblé précisément sur les disques ou articulations en souffrance."
            }
        ]
    },
    {
        "filename": "osteopathe-pezenas.html",
        "city": "Pézenas",
        "postcode": "34120",
        "travel_time": "12 minutes",
        "faq": [
            {
                "q": "Quel est l'avantage de venir au cabinet de Pinet depuis Pézenas ?",
                "a": "Situé à 12 minutes de Pézenas par la D13 via Castelnau-de-Guers, le cabinet offre un cadre calme et surtout un **parking privé gratuit dans la cour**. C'est une alternative idéale aux contraintes d'accès et de stationnement du centre historique piétonnier de Pézenas."
            },
            {
                "q": "Comment l'ostéopathie soulage-t-elle le mal de dos chronique et la sciatique ?",
                "a": "Par des mobilisations douces et adaptées, l'ostéopathie rétablit la mobilité des articulations vertébrales, relâche les tensions musculaires profondes (psoas, diaphragme, pyramidale) et diminue la compression nerveuse responsable de la sciatique ou du lumbago."
            },
            {
                "q": "Proposez-vous des consultations d'ostéopathie à domicile sur Pézenas ?",
                "a": "Oui, Frédéric Murria intervient à domicile sur Pézenas (34120), Castelnau-de-Guers et Tourbes pour les patients à mobilité réduite, personnes âgées ou urgences dorsales (tarif de 70 € tout compris)."
            },
            {
                "q": "Les séances d'ostéopathie sont-elles remboursées par ma mutuelle ?",
                "a": "Oui, les mutuelles et complémentaires santé remboursent couramment les séances d'ostéopathie sur présentation de note d'honoraires. Le cabinet délivre une facture avec le **N° ADELI officiel (340008544)**."
            }
        ]
    },
    {
        "filename": "osteopathe-meze.html",
        "city": "Mèze",
        "postcode": "34140",
        "travel_time": "10 minutes",
        "faq": [
            {
                "q": "Quel est l'itinéraire pour venir au cabinet depuis Mèze ?",
                "a": "Depuis Mèze, prenez la D613 puis la D18 vers Pinet (environ 9 km, 10 minutes de trajet). Vous arrivez directement au 21 avenue de Pomerols avec **stationnement privé gratuit dans la cour**, sans chercher de place comme sur le port de Mèze."
            },
            {
                "q": "Prenez-vous en charge les sportifs du Bassin de Thau (voile, kitesurf, running) ?",
                "a": "Oui, l'ostéopathie est idéale pour les pratiquants de sports nautiques et terrestres de Mèze et de l'Étang de Thau : prévention des tendinites, amélioration de la mobilité d'épaules et de hanches, récupération musculaire et suivi après blessure."
            },
            {
                "q": "Intervenez-vous à domicile sur Mèze, Bouzigues et Loupian ?",
                "a": "Oui, Frédéric Murria effectue des consultations à domicile sur Mèze (34140), Bouzigues et Loupian avec table d'ostéopathie portative professionnelle au tarif de 70 €."
            },
            {
                "q": "Comment obtenir le remboursement de ma séance d'ostéopathie ?",
                "a": "À la fin de votre consultation, une facture acquittée avec le N° ADELI 340008544 de Frédéric Murria vous est immédiatement transmise pour envoi à votre mutuelle santé."
            }
        ]
    }
]

def update_page_with_faq(cfg):
    fn = cfg['filename']
    print(f"Mise à jour de {fn}...")
    with open(fn, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 1. Préparation du Schema.org FAQPage
    faq_entities = []
    for item in cfg['faq']:
        clean_ans = item['a'].replace('**', '')
        q_item = "          {\n" \
                 '            "@type": "Question",\n' \
                 f'            "name": "{item["q"]}",\n' \
                 '            "acceptedAnswer": {\n' \
                 '              "@type": "Answer",\n' \
                 f'              "text": "{clean_ans}"\n' \
                 '            }\n' \
                 '          }'
        faq_entities.append(q_item)
    
    joined_entities = ',\n'.join(faq_entities)
    faq_json = f"""      ,
      {{
        "@type": "FAQPage",
        "@id": "https://rdv.osteomagazine.com/{fn}#faq",
        "mainEntity": [
{joined_entities}
        ]
      }}"""

    # Insertion du schema avant la fermeture de @graph
    if '"@type": "FAQPage"' not in html_content:
        html_content = re.sub(r'(\s*\}\s*\]\s*\}\s*<\/script>)', f'{faq_json}\n    ]\n  }}\n  </script>', html_content, count=1)

    # 2. Ajout du lien FAQ dans la navigation
    if '#faq' not in html_content:
        html_content = html_content.replace('<a href="#contact" class="nav-link hover:text-teal-400 transition">Contact</a>',
                                            '<a href="#faq" class="nav-link hover:text-teal-400 transition">FAQ</a>\n            <a href="#contact" class="nav-link hover:text-teal-400 transition">Contact</a>')

    # 3. Préparation du composant HTML FAQ Accordéon
    faq_items_html = []
    for i, item in enumerate(cfg['faq']):
        open_attr = " open" if i == 0 else ""
        formatted_a = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item['a'])
        faq_items_html.append(f"""
        <details class="group bg-white p-6 md:p-8 rounded-3xl shadow-sm border-2 border-slate-100 hover:border-teal-400 transition cursor-pointer"{open_attr}>
          <summary class="flex justify-between items-center font-black text-lg md:text-xl text-slate-900 list-none">
            <span>{item['q']}</span>
            <span class="text-teal-600 transition-transform group-open:rotate-180 text-xl"><i class="fas fa-chevron-down"></i></span>
          </summary>
          <div class="mt-4 text-slate-600 text-base md:text-lg leading-relaxed pt-4 border-t border-slate-100">
            {formatted_a}
          </div>
        </details>""")

    joined_items = ''.join(faq_items_html)
    faq_section_html = f"""
  <section id="faq" class="py-24 bg-slate-50 border-t border-slate-200">
    <div class="container mx-auto px-4 max-w-4xl">
      <div class="text-center mb-16">
        <span class="text-xs font-black text-teal-600 uppercase tracking-widest block mb-2">Questions fréquentes & Conseils locaux</span>
        <h2 class="text-3xl md:text-5xl font-black text-slate-900 tracking-tight">Vos questions d'ostéopathie à {cfg['city']}</h2>
        <p class="text-slate-600 mt-4 text-lg">Tout ce qu'il faut savoir sur l'accès depuis {cfg['city']} ({cfg['postcode']}), les urgences du dos, le remboursement mutuelle et les consultations à domicile.</p>
      </div>

      <div class="space-y-6">
{joined_items}
      </div>
    </div>
  </section>
"""

    if 'id="faq"' not in html_content:
        html_content = html_content.replace('<section id="contact"', f'{faq_section_html}\n  <section id="contact"')

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html_content)

for c in pages_config:
    update_page_with_faq(c)

print("Toutes les pages locales ont été enrichies avec succès !")
