from django.contrib import admin

# Register your models here.
from app1.models import User, CompanyName, Expense, Category, Contact_Us, News

admin.site.register(User)
admin.site.register(Contact_Us)
admin.site.register(CompanyName)
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(News)