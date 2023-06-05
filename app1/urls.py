from django.urls import path
from app1 import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('login_page',views.loginPage,name="login"),
    path('logOutt',views.logoutUser,name="logout"),
    path('register_page',views.registerUser,name="register"),

    path('', views.home, name="home"),
    path('index', views.home, name="home"),
    path('contactUs', views.contactUs, name="contactUs"),

    path('dashboard', views.dashboard, name="dashboard"),
    path('news', views.news, name="news"),
    path('helpcenter', views.helpcenter, name="helpcenter"),

    path('addSymbol', views.addSymbol, name="addSymbol"),
    path('prediction', views.prediction, name="prediction"),
    
    path('myexpense', views.myexpense, name="myexpense"),
    path('addexpense', views.addexpense, name="addexpense"),
    path('editexpense/<int:id>', views.editexpense, name="editexpense"),
    path('deleteexpense/<int:id>', views.deleteexpense, name="deleteexpense"),
    path('search-expense', csrf_exempt(views.search_expense) , name="search-expense"),
    path('expense_category_summary', csrf_exempt(views.expense_category_summary) , name="expense_category_summary"),

    # path('showName', views.showName, name="showName"),

]

