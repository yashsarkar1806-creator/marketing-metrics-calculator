# Marketing Metrics Calculator (CAC · LTV · ROAS · Payback)

A small, dependency-free Python tool that answers the question every DTC brand and SaaS startup
asks: **"Is our customer acquisition actually profitable?"** It also includes a one-page
[metrics cheat sheet](CHEATSHEET.md) with formulas, uses and common pitfalls.

## The problem

Marketers report ROAS, finance asks about LTV:CAC and payback, and the formulas differ between
e-commerce (DTC) and subscription (SaaS) businesses. Mixing revenue-based and margin-based numbers
leads to bad budget decisions.

## The approach

* Two business models:
  * **DTC**: LTV = AOV × orders per year × years retained × gross margin; plus ROAS and **break-even ROAS** (1 ÷ margin).
  * **SaaS**: LTV = monthly ARPA × gross margin ÷ monthly churn.
* Outputs **CAC, LTV, LTV:CAC, CAC payback (months)** and a plain-English verdict against the common 3:1 rule of thumb.
* Margin-based LTV throughout, so it's a fair comparison to CAC.
* Inputs from CLI flags or a JSON file. Standard library only, with unit tests.

## How to run

Requires Python 3.9+. Nothing to install.

```bash
git clone https://github.com/yashsarkar1806-creator/marketing-metrics-calculator.git
cd marketing-metrics-calculator

# from an example file
python3 metrics.py dtc  --file examples/dtc_skincare.json
python3 metrics.py saas --file examples/saas_startup.json

# or with flags
python3 metrics.py saas --spend 40000 --new-customers 80 --arpa-monthly 120 --gross-margin 0.8 --monthly-churn 0.025

# JSON output for spreadsheets / other tools
python3 metrics.py dtc --file examples/dtc_skincare.json --json

# tests
python3 -m unittest discover -s tests
```

## Sample output

> The example inputs are **illustrative numbers for fictional companies**, not real company data.

DTC skincare brand (`examples/dtc_skincare.json`):

```
Unit economics (DTC)
----------------------------------
CAC               $50.00
LTV (gross)       $210.80
LTV:CAC           4.22:1
CAC payback       5.69 months
ROAS              2.80x
Break-even ROAS   1.47x
Verdict           healthy (around the 3:1 to 5:1 rule of thumb)
```

B2B SaaS startup (`examples/saas_startup.json`):

```
Unit economics (SaaS)
----------------------------------
CAC               $500.00
LTV (gross)       $3,840.00
LTV:CAC           7.68:1
CAC payback       5.21 months
Verdict           very strong, possibly under-investing in growth
```

**How to read it:** the DTC brand's 2.8x ROAS is well above its 1.47x break-even ROAS, so first orders
are profitable, and LTV:CAC of about 4:1 leaves room to scale spend. The SaaS startup's 7.7:1 ratio and
roughly 5-month payback suggest it could probably spend more aggressively on acquisition.

## What this shows

* Working knowledge of **unit economics and marketing ROI**, and the differences between DTC and SaaS models.
* Turning formulas into a tested, reusable tool instead of a one-off spreadsheet.
* Explaining numbers in a way that helps marketing and finance make budget decisions.

## More projects

* Ideas list: [marketing-ai-ideas](https://github.com/yashsarkar1806-creator/marketing-ai-ideas), small and medium marketing project ideas for DTC and tech brands
* [utm-builder](https://github.com/yashsarkar1806-creator/utm-builder): UTM link builder and campaign naming convention
* [dtc-review-sentiment-analysis](https://github.com/yashsarkar1806-creator/dtc-review-sentiment-analysis): sentiment and themes in product reviews
* [dtc-saas-campaign-dashboard](https://github.com/yashsarkar1806-creator/dtc-saas-campaign-dashboard): channel, funnel and ROAS analysis

## License

MIT, see [LICENSE](LICENSE). Built by Yash Sarkar.
