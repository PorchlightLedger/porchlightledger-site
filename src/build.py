#!/usr/bin/env python3
"""Generates index.html from product data. Prices verified from the live Etsy shop page snapshot (Oct 3, 2026)."""
import html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = "https://www.etsy.com/listing/"
SHOP = "https://www.etsy.com/shop/PorchlightLedger"
# (listing id, name, image, price, benefit)
MONEY = [
 ("4587773080","Debt Payoff Planner","debt-payoff","8.99","Compare Snowball and Avalanche and see your debt-free date, with a month-by-month payment plan."),
 ("4587774776","Monthly Budget Planner","monthly-budget","7.99","Zero-based budget with 12 monthly tabs, so every dollar has a job before the month starts."),
 ("4587815514","Paycheck Budget Planner","paycheck-budget","5.99","Assign bills to each payday, whether you're paid weekly, biweekly or twice a month."),
 ("4587769437","Sinking Funds Tracker","sinking-funds","5.99","Set a goal and a date for once-a-year costs and know exactly what to save each month."),
 ("4587772765","Bill Payment Tracker","bill-payment","4.99","Every bill, its due date and whether it's paid, all year on one page."),
 ("4587778214","Net Worth Tracker","net-worth","5.99","A monthly snapshot of what you own and owe, with a dashboard that shows your progress."),
 ("4587778812","Holiday Budget and Gift Planner","holiday-budget","5.99","Set a holiday budget and track gifts, food, travel and decor before December sneaks up."),
 ("4587779330","2027 Annual Budget and Money Goals Planner","annual-budget-2027","7.99","Plan the year ahead, set money goals and review how the year went."),
 ("4587773147","100 Envelope Savings Tracker","envelope-savings","4.99","100 envelope, 52 week and no-spend challenges that make saving feel like a game."),
 ("4587812451","Subscription Tracker","subscription-tracker","3.99","List every subscription and free trial, see the real monthly cost and cut what you don't use."),
 ("4587775360","Mortgage Payoff Calculator","mortgage-payoff","6.99","See how extra payments cut years and interest off your mortgage."),
]
HOME = [
 ("4587780419","Family Emergency Binder","emergency-binder","9.99"),
 ("4587781246","Tax Prep Organizer","tax-prep","6.99"),
 ("4587779075","Home Inventory for Insurance","home-inventory","6.99"),
 ("4587812227","Home Buying Planner","home-buying","7.99"),
 ("4587816224","Home Renovation Budget Planner","home-renovation","6.99"),
 ("4587775584","Home Maintenance Schedule","home-maintenance","5.99"),
 ("4587819474","Utility Bill Tracker","utility-bill","4.99"),
 ("4587775796","Mileage Log","mileage-log","5.99"),
]
h = html.escape
def card(i,n,img,p,b):
    return f'''      <article class="card">
        <a href="{E}{i}" target="_blank" rel="noopener"><img src="img/{img}.jpg" alt="{h(n)} spreadsheet mockup" width="800" height="600" loading="lazy"></a>
        <div class="card-body">
          <h3>{h(n)}</h3>
          <p>{h(b)}</p>
          <div class="card-foot"><span class="price">${p}</span><a class="btn btn-small" href="{E}{i}" target="_blank" rel="noopener">View on Etsy</a></div>
        </div>
      </article>'''
def mini(i,n,img,p):
    return f'''      <a class="mini" href="{E}{i}" target="_blank" rel="noopener"><img src="img/{img}.jpg" alt="{h(n)} mockup" width="800" height="600" loading="lazy"><span class="mini-name">{h(n)}</span><span class="price">${p}</span></a>'''
t = (ROOT/"src/index.template.html").read_text()
t = t.replace("{{MONEY}}", "\n".join(card(*x) for x in MONEY)).replace("{{HOME}}", "\n".join(mini(*x) for x in HOME))
(ROOT/"index.html").write_text(t)
print("index.html written")
