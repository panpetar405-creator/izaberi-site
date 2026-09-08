import json, os

BASE_CSS = """
:root{--bg:#f7f7f4;--ink:#111;--muted:#70706b;--line:#deded7;--card:#fff;--accent:#111;--max:1180px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{text-decoration:none;color:inherit}.wrap{max-width:var(--max);margin:auto;padding:0 28px}
header{height:76px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between}
.logo{font-weight:900;letter-spacing:-.05em;font-size:25px}.nav{display:flex;gap:30px;font-size:14px;color:#444}.nav a:hover{color:#000}
.btn{border:0;background:#111;color:white;border-radius:11px;padding:0 25px;height:48px;font-weight:700;font-size:14px;cursor:pointer}
section{padding:60px 0}
.rank-tag{font-size:12px;color:#777;letter-spacing:.08em;text-transform:uppercase}
.page-head{padding:50px 0 20px}
.page-head h1{font-size:clamp(34px,5vw,52px);letter-spacing:-.05em;margin:0 0 10px;max-width:800px}
.page-head p{color:var(--muted);font-size:18px;margin:0}
.choices{display:flex;flex-wrap:wrap;gap:9px;margin:26px 0 10px}
.pill{border:1px solid var(--line);border-radius:99px;padding:10px 14px;font-size:13px;background:#fff}
.results{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
.product{border:1px solid var(--line);border-radius:16px;padding:22px;background:#fff;display:flex;flex-direction:column;gap:10px}
.product-img{width:calc(100% + 44px);margin:-22px -22px 4px;height:160px;object-fit:cover;border-radius:16px 16px 0 0;background:#eeeee8;display:block}
.product b{font-size:18px}.product .price{color:#777;font-size:14px}
.product p.bul{color:#333;font-size:13px;line-height:1.8;margin:0}
.product p.why{color:#777;font-size:13px;line-height:1.6;margin:0;border-top:1px solid var(--line);padding-top:10px}
footer{border-top:1px solid var(--line);padding:35px 0 50px;color:#777;font-size:13px;display:flex;justify-content:space-between}
@media(max-width:800px){.nav{display:none}.results{grid-template-columns:1fr}}
"""

PAGE_TMPL = """<!doctype html>
<html lang="sr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{question} — IZABERI</title>
<meta name="description" content="{question} Uporedi najbolje opcije i izaberi na osnovu onoga sto ti je najvaznije.">
<style>{css}</style>
</head>
<body>
<header><div class="wrap" style="width:100%;display:flex;align-items:center;justify-content:space-between">
<a class="logo" href="../index.html">IZABERI</a>
<nav class="nav"><a href="../index.html#kategorije">Kategorije</a><a href="../index.html#kako">Kako radi</a><a href="../index.html#popularno">Najnovije</a></nav>
</div></header>
<main class="wrap">
<div class="page-head">
<div class="rank-tag">{category}</div>
<h1>{question}</h1>
<p>{subtitle}</p>
<div class="choices">{pills}</div>
</div>
<div class="results">{products}</div>
</main>
<footer><div class="wrap" style="width:100%;display:flex;justify-content:space-between"><span>IZABERI</span><span>Ne trazi vise. Izaberi bolje.</span></div></footer>
</body></html>
"""

PRODUCT_TMPL = """<div class="product">
<img class="product-img" src="{image}" alt="{name}" loading="lazy" onerror="this.onerror=null;this.src='https://placehold.co/400x300/eeeee8/70706b?text=Slika+nedostupna';">
<div class="rank-tag">{rank}</div>
<b>{name}</b>
<div class="price">{price}</div>
<p class="bul">{bullets}</p>
<p class="why">{why}</p>
<a class="btn" style="text-align:center;line-height:48px" href="{link}">POGLEDAJ PONUDU</a>
</div>"""

PLACEHOLDER_IMAGE = "https://placehold.co/400x300/eeeee8/70706b?text=Uskoro+slika"

def build():
    with open("data/decisions.json", encoding="utf-8") as f:
        decisions = json.load(f)
    os.makedirs("pages", exist_ok=True)
    for d in decisions:
        products_html = "\n".join(
            PRODUCT_TMPL.format(
                rank=p["rank"], name=p["name"], price=p["price"],
                bullets="<br>".join(p["bullets"]), why=p["why"],
                link=p["affiliate_link"],
                image=p.get("image") or PLACEHOLDER_IMAGE
            ) for p in d["products"]
        )
        pills_html = "".join(f'<span class="pill">{p}</span>' for p in d["priorities"])
        html = PAGE_TMPL.format(
            question=d["question"], category=d["category"], subtitle=d["subtitle"],
            pills=pills_html, products=products_html, css=BASE_CSS
        )
        out_path = f"pages/{d['slug']}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("generated:", out_path)

if __name__ == "__main__":
    build()
