from django.db import models


class Property(models.Model):
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField()
    sell_date = models.DateField(null=True, blank=True)
    sell_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rental_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    renovation_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number} {self.street}"


class Mortgage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="mortgages")
    lender = models.CharField(max_length=100)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_years = models.IntegerField()
    start_date = models.DateField()

    def __str__(self):
        return f"{self.lender} - {self.property}"

