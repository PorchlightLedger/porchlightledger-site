#!/usr/bin/env python3
"""Generates index.html from product data.

Prices verified from the live Etsy shop page snapshot (Oct 3, 2026).
To enable on-site checkout for a product later, set its "checkout_url"
(e.g. a hosted checkout / payment link). Empty = no Buy now button (Etsy link only).
Then run: python3 src/build.py
"""
import html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = "https://www.etsy.com/listing/"
h = html.escape

def P(etsy_id, name, img, price, blurb, group, checkout_url=""):
    return dict(etsy_id=etsy_id, name=name, img=img, price=price, blurb=blurb, group=group, checkout_url=checkout_url)

PRODUCTS = [
 P("4587781978","Household Finance Bundle","bundle","19.99","Six matching money templates in one download, $40.94 if bought separately.","bundle"),
 P("4587773080","Debt Payoff Planner","debt-payoff","8.99","Compare Snowball and Avalanche and see your debt-free date, with a month-by-month payment plan.","money"),
 P("4587774776","Monthly Budget Planner","monthly-budget","7.99","Zero-based budget with 12 monthly tabs, so every dollar has a job before the month starts.","money"),
 P("4587815514","Paycheck Budget Planner","paycheck-budget","5.99","Assign bills to each payday, whether you're paid weekly, biweekly or twice a month.","money"),
 P("4587769437","Sinking Funds Tracker","sinking-funds","5.99","Set a goal and a date for once-a-year costs and know exactly what to save each month.","money"),
 P("4587772765","Bill Payment Tracker","bill-payment","4.99","Every bill, its due date and whether it's paid, all year on one page.","money"),
 P("4587778214","Net Worth Tracker","net-worth","5.99","A monthly snapshot of what you own and owe, with a dashboard that shows your progress.","money"),
 P("4587778812","Holiday Budget and Gift Planner","holiday-budget","5.99","Set a holiday budget and track gifts, food, travel and decor before December sneaks up.","money"),
 P("4587779330","2027 Annual Budget and Money Goals Planner","annual-budget-2027","7.99","Plan the year ahead, set money goals and review how the year went.","money"),
 P("4587773147","100 Envelope Savings Tracker","envelope-savings","4.99","100 envelope, 52 week and no-spend challenges that make saving feel like a game.","money"),
 P("4587812451","Subscription Tracker","subscription-tracker","3.99","List every subscription and free trial, see the real monthly cost and cut what you don't use.","money"),
 P("4587775360","Mortgage Payoff Calculator","mortgage-payoff","6.99","See how extra payments cut years and interest off your mortgage.","money"),
 P("4587780419","Family Emergency Binder","emergency-binder","9.99","Contacts, medical info, accounts and bills in one organized place for when it matters.","home"),
 P("4587781246","2026 Tax Prep Organizer","tax-prep","6.99","A document checklist plus donation and medical receipt logs to make tax time calmer.","home"),
 P("4587779075","Home Inventory for Insurance","home-inventory","6.99","List belongings, serial numbers and receipts so an insurance claim is easier.","home"),
 P("4587812227","Home Buying Planner","home-buying","7.99","Score the houses you tour and track your down payment savings.","home"),
 P("4587816224","Home Renovation Budget Planner","home-renovation","6.99","Budget a remodel, compare quotes and keep a punch list.","home"),
 P("4587775584","Home Maintenance Schedule","home-maintenance","5.99","Seasonal checklists and a repair log so small fixes don't become big ones.","home"),
 P("4587819474","Utility Bill Tracker","utility-bill","4.99","Log energy bills and usage to spot changes month to month.","home"),
 P("4587775796","Mileage Log","mileage-log","5.99","Record business and personal trips in one simple log.","home"),
]
GROUPS = [("bundle","All-in-one bundle"),("money","Money planners"),("home","Home &amp; family records")]
BY_ID = {p["etsy_id"]: p for p in PRODUCTS}

def buy_now(p):
    if p["checkout_url"]:
        return f'<a class="btn btn-small btn-warm" href="{h(p["checkout_url"])}">Buy now</a>'
    return ""

def card(p):
    url = E + p["etsy_id"]
    best = '<span class="tag">All-in-one</span>' if p["group"] == "bundle" else ""
    return f'''      <article class="card{' card-wide' if p["group"] == "bundle" else ''}" id="p-{p["etsy_id"]}">
        <a class="card-img" href="{url}" target="_blank" rel="noopener">{best}<img src="img/{p["img"]}.jpg" alt="{h(p["name"])} mockup" width="800" height="600" loading="lazy"></a>
        <div class="card-body">
          <div class="card-head"><h4>{h(p["name"])}</h4><span class="price">${p["price"]}</span></div>
          <p>{h(p["blurb"])}</p>
          <div class="card-actions">
            <a class="btn btn-small" href="{url}" target="_blank" rel="noopener">Buy on Etsy</a>
            {buy_now(p)}
          </div>
        </div>
      </article>'''

def shop():
    out = []
    for g, label in GROUPS:
        items = [p for p in PRODUCTS if p["group"] == g]
        out.append(f'    <h3 class="shop-group">{label} <span class="count">{len(items)}</span></h3>\n    <div class="grid">\n' + "\n".join(card(p) for p in items) + "\n    </div>")
    return "\n".join(out)

def plink(i):
    p = BY_ID[i]
    return f'<a href="#p-{i}">{h(p["name"])}</a> <span class="price-inline">${p["price"]}</span>'

t = (ROOT/"src/index.template.html").read_text()
def jsonld():
    import json
    items = []
    for n, p in enumerate(PRODUCTS, 1):
        items.append({"@type": "ListItem", "position": n, "item": {
            "@type": "Product", "name": p["name"], "description": p["blurb"],
            "image": f"https://porchlightledger.com/img/{p['img']}.jpg",
            "url": E + p["etsy_id"], "sku": p["etsy_id"],
            "brand": {"@type": "Brand", "name": "Porchlight Ledger"},
            "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "USD",
                       "availability": "https://schema.org/InStock", "url": E + p["etsy_id"]}}})
    data = {"@context": "https://schema.org", "@type": "ItemList", "name": "Porchlight Ledger planners", "itemListElement": items}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'

t = t.replace("{{JSONLD}}", jsonld())
t = t.replace("{{SHOP}}", shop()).replace("{{COUNT}}", str(len(PRODUCTS)))
import re
t = re.sub(r"\{\{LINK:(\d+)\}\}", lambda m: plink(m.group(1)), t)
(ROOT/"index.html").write_text(t)
print(f"index.html written ({len(PRODUCTS)} products)")
