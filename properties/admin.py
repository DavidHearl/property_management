from django.contrib import admin
from .models import Property, Mortgage

class MortgageInline(admin.TabularInline):
    model = Mortgage
    extra = 1  # Show one blank form by default

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'purchase_price', 'current_value', 'is_rented')
    list_filter = ('is_rented',)
    search_fields = ('street',)
    inlines = [MortgageInline]

@admin.register(Mortgage)
class MortgageAdmin(admin.ModelAdmin):
    list_display = ('property', 'lender', 'principal', 'interest_rate', 'term_years', 'start_date')
    list_filter = ('lender', 'start_date')
    search_fields = ('property__street', 'lender')
