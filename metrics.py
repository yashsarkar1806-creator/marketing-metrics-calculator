"""Unit-economics calculator for DTC and SaaS marketers.

Pure Python (standard library only). Use it as a CLI or import the functions.
"""
from __future__ import annotations

import argparse
import json
import sys


def _div(a: float, b: float) -> float | None:
    return None if not b else a / b


def cac(marketing_spend: float, new_customers: int) -> float | None:
    """Customer acquisition cost = spend / new customers."""
    return _div(marketing_spend, new_customers)


def roas(revenue: float, ad_spend: float) -> float | None:
    """Return on ad spend = attributed revenue / ad spend (e.g. 3.2 means $3.20 per $1)."""
    return _div(revenue, ad_spend)


def break_even_roas(gross_margin: float) -> float | None:
    """ROAS needed to cover product cost on the first order = 1 / gross margin."""
    return _div(1, gross_margin)


def ltv_dtc(aov: float, orders_per_year: float, years: float, gross_margin: float) -> float:
    """DTC (e-commerce) gross-margin LTV = AOV x purchase frequency x lifespan x margin."""
    return aov * orders_per_year * years * gross_margin


def ltv_saas(arpa_monthly: float, gross_margin: float, monthly_churn: float) -> float | None:
    """SaaS LTV = monthly ARPA x gross margin / monthly churn rate."""
    return _div(arpa_monthly * gross_margin, monthly_churn)


def payback_months(cac_value: float, monthly_gross_profit_per_customer: float) -> float | None:
    """Months of gross profit needed to earn back CAC."""
    return _div(cac_value, monthly_gross_profit_per_customer)


def conversion_rate(conversions: int, visitors: int) -> float | None:
    return _div(conversions, visitors)


def rating(ltv_cac: float | None) -> str:
    if ltv_cac is None:
        return "n/a"
    if ltv_cac < 1:
        return "losing money on every customer"
    if ltv_cac < 3:
        return "below the common 3:1 benchmark"
    if ltv_cac <= 5:
        return "healthy (around the 3:1 to 5:1 rule of thumb)"
    return "very strong, possibly under-investing in growth"


def report(model: str, p: dict) -> dict:
    """Compute a full unit-economics report for a 'dtc' or 'saas' business."""
    c = cac(p["spend"], p["new_customers"])
    out: dict = {"model": model, "cac": c}
    if model == "dtc":
        ltv = ltv_dtc(p["aov"], p["orders_per_year"], p["years"], p["gross_margin"])
        monthly_gp = p["aov"] * p["orders_per_year"] * p["gross_margin"] / 12
        out.update(
            roas=roas(p["revenue"], p["spend"]) if "revenue" in p else None,
            break_even_roas=break_even_roas(p["gross_margin"]),
        )
    elif model == "saas":
        ltv = ltv_saas(p["arpa_monthly"], p["gross_margin"], p["monthly_churn"])
        monthly_gp = p["arpa_monthly"] * p["gross_margin"]
    else:
        raise ValueError("model must be 'dtc' or 'saas'")
    out["ltv"] = ltv
    out["ltv_to_cac"] = _div(ltv, c) if (ltv is not None and c) else None
    out["payback_months"] = payback_months(c, monthly_gp) if c is not None else None
    out["verdict"] = rating(out["ltv_to_cac"])
    return out


def fmt(report_: dict) -> str:
    def money(v):
        return "n/a" if v is None else f"${v:,.2f}"

    def num(v, suffix=""):
        return "n/a" if v is None else f"{v:,.2f}{suffix}"

    lines = [f"Unit economics ({ {'dtc': 'DTC', 'saas': 'SaaS'}[report_['model']] })", "-" * 34,
             f"CAC               {money(report_['cac'])}",
             f"LTV (gross)       {money(report_['ltv'])}",
             f"LTV:CAC           {num(report_['ltv_to_cac'], ':1')}",
             f"CAC payback       {num(report_['payback_months'], ' months')}"]
    if report_["model"] == "dtc":
        lines += [f"ROAS              {num(report_.get('roas'), 'x')}",
                  f"Break-even ROAS   {num(report_.get('break_even_roas'), 'x')}"]
    lines.append(f"Verdict           {report_['verdict']}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="CAC / LTV / ROAS / payback calculator for DTC and SaaS.")
    ap.add_argument("model", choices=["dtc", "saas"])
    ap.add_argument("--file", help="JSON file with inputs (see examples/)")
    ap.add_argument("--spend", type=float, help="Marketing/ad spend for the period")
    ap.add_argument("--new-customers", type=int)
    ap.add_argument("--revenue", type=float, help="DTC: attributed revenue for ROAS")
    ap.add_argument("--aov", type=float, help="DTC: average order value")
    ap.add_argument("--orders-per-year", type=float, help="DTC: purchases per customer per year")
    ap.add_argument("--years", type=float, help="DTC: expected customer lifespan in years")
    ap.add_argument("--arpa-monthly", type=float, help="SaaS: average revenue per account per month")
    ap.add_argument("--monthly-churn", type=float, help="SaaS: monthly churn rate, e.g. 0.03")
    ap.add_argument("--gross-margin", type=float, help="Gross margin as a decimal, e.g. 0.65")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of a table")
    a = ap.parse_args(argv)

    params = json.load(open(a.file)) if a.file else {}
    for k, v in vars(a).items():
        if v is not None and k not in ("model", "file", "json"):
            params[k] = v
    try:
        r = report(a.model, params)
    except KeyError as e:
        ap.error(f"missing input: {e.args[0].replace('_', '-')}")
    print(json.dumps(r, indent=2) if a.json else fmt(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
