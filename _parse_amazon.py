import re, json

with open(r'C:\Users\iamdo\.claude\projects\D--work-private-yjsplan\a47e6a1e-622a-4a06-8a80-d80980f90f8a\tool-results\mcp-playwright-browser_navigate-1771157718932.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

data = json.loads(raw)
content = data[0]['text'] if data else ''

# Products are in link elements with /dp/ASIN/ URLs
# Pattern: link "TITLE" [ref=...] [cursor=pointer]:\n ... /url: /dp/ASIN/...
products = []
# Find all /dp/ URLs with their context
dp_pattern = re.compile(r'/dp/([A-Z0-9]{10})/ref=sr_1_(\d+)')
for m in dp_pattern.finditer(content):
    asin = m.group(1)
    rank = int(m.group(2))
    pos = m.start()
    
    # Look backwards for the link title
    before = content[max(0,pos-500):pos]
    title_m = re.search(r'link "(.+?)" \[ref=', before)
    title = title_m.group(1) if title_m else ''
    
    # Look forward for rating, reviews, price
    after = content[pos:pos+3000]
    
    rating_m = re.search(r'"(\d\.\d) out of 5 stars', after)
    rating = rating_m.group(1) if rating_m else ''
    
    review_m = re.search(r'(\d[\d,.]+[kK]?) ratings', after)
    reviews = review_m.group(1) if review_m else ''
    
    price_m = re.search(r'\$(\d+\.\d+)', after)
    price = price_m.group(1) if price_m else ''
    
    bought_m = re.search(r'(\d+[kK]?\+?) bought in past month', after)
    bought = bought_m.group(1) if bought_m else ''
    
    if title and len(title) > 20 and rank <= 25:
        products.append({'rank': rank, 'title': title[:120], 'asin': asin, 'rating': rating, 'reviews': reviews, 'price': price, 'bought': bought})

# Deduplicate by ASIN, keep lowest rank
seen = set()
unique = []
products.sort(key=lambda x: x['rank'])
for p in products:
    if p['asin'] not in seen:
        seen.add(p['asin'])
        unique.append(p)

print(f'Found {len(unique)} unique products')
for p in unique[:20]:
    print(f"{p['rank']}. {p['title']}")
    print(f"   ASIN: {p['asin']} | Rating: {p['rating']} | Reviews: {p['reviews']} | Price: ${p['price']} | Bought: {p['bought']}")
