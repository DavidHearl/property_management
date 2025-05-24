from django.shortcuts import render
from .models import Property
from datetime import date
from math import pow

def calculate_amortization_schedule(principal, annual_rate, term_years, start_date):
    schedule = []

    monthly_rate = (annual_rate / 100) / 12
    months = term_years * 12
    monthly_payment = principal * monthly_rate * pow(1 + monthly_rate, months) / (pow(1 + monthly_rate, months) - 1)

    balance = principal
    current_date = start_date

    for i in range(months):
        interest = balance * monthly_rate
        principal_paid = monthly_payment - interest
        balance -= principal_paid

        schedule.append({
            "year": current_date.year,
            "month": current_date.month,
            "payment": round(monthly_payment, 2),
            "interest_paid": round(interest, 2),
            "principal_paid": round(principal_paid, 2),
            "principal_left": round(balance, 2)
        })

        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    return schedule

def home(request):
    tax_percent = 20
    mgmt_fee_percent = 7
    today = date.today()

    properties = Property.objects.prefetch_related("mortgages").all()
    enriched_properties = []

    for prop in properties:
        renovation = float(prop.renovation_cost or 0)
        data = {
            "property": prop,
            "capital_gain_net": None,
            "capital_gain_taxable": None,
            "schedule_entry": None,
            "monthly_profit_net": None,
        }

        if prop.current_value:
            gain = float(prop.current_value) - float(prop.purchase_price)
            taxed_gain = gain * (1 - tax_percent / 100)
            net_gain = taxed_gain - renovation

            data["capital_gain_taxed"] = round(taxed_gain, 2)
            data["capital_gain_net"] = round(net_gain, 2)

        if prop.rental_income and prop.mortgages.exists():
            mortgage = prop.mortgages.first()
            if all([mortgage.principal, mortgage.interest_rate, mortgage.term_years, mortgage.start_date]):
                schedule = calculate_amortization_schedule(
                    float(mortgage.principal),
                    float(mortgage.interest_rate),
                    int(mortgage.term_years),
                    mortgage.start_date
                )

                months_elapsed = (today.year - mortgage.start_date.year) * 12 + (today.month - mortgage.start_date.month)
                if 0 <= months_elapsed < len(schedule):
                    entry = schedule[months_elapsed]
                    data["schedule_entry"] = entry

                    rent = float(prop.rental_income)
                    mgmt_fee = rent * (mgmt_fee_percent / 100)
                    adjusted_rent = rent - mgmt_fee
                    taxable = adjusted_rent - entry["interest_paid"]
                    net_profit = taxable * (1 - tax_percent / 100)
                    data["monthly_profit_net"] = round(net_profit, 2)

        enriched_properties.append(data)

    return render(request, 'properties/home.html', {
        "properties": enriched_properties,
        "tax_percent": tax_percent,
        "mgmt_fee_percent": mgmt_fee_percent,
    })
