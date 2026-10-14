import urllib.request, json, re

req = urllib.request.Request('https://osteomagazine.com/api/v1/posts?limit=5', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for p in data:
        print('TITRE:', p.get('title'))
        print('  Cover image:', p.get('cover_image'))
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', p.get('body_html', ''))
        print('  Images dans body_html:', len(imgs))
        if imgs:
            print('   -> exemple:', imgs[0][:90])
