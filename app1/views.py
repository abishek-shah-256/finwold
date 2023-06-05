from django.shortcuts import render,redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
# from django.contrib.auth.models import User
from app1.models import User, Contact_Us
from app1.models import CompanyName, Expense, Category, News

from django.http import JsonResponse
from django.views.decorators.http import require_GET
import datetime

#machinelearning import
import yfinance as yf
import plotly.graph_objs as go
from .utils import prediction_model

from stocksymbol import StockSymbol
api_key = 'dde14364-9628-416c-ad3e-f7d90723082b'
ss = StockSymbol(api_key)



def loginPage(request):
    page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('username').lower()
        password = request.POST.get("password");

        try:
            user = User.objects.get(username = name)  
             
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request,username=name,password=password)    
        if user is not None:
            login(request,user)
            # return redirect('home')
            return redirect('dashboard')
        else:
            messages.error(request,'password does not matched')  
             
    context = {'page':page}

    return render(request,'app1/login_register.html',context)
# ----------------------------------------LOGIN PAGE ENDS---------------------------------------------------------

def logoutUser(request):
    logout(request)
    return redirect('home')
# ----------------------------------------LOGOUT PAGE ENDS---------------------------------------------------------



def registerUser(request):
    page = 'register' 
    context ={'page':page,'form':CreateUserForm()}

    if request.method == 'POST':

        form = CreateUserForm(request.POST)   
        if(form.is_valid()):
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            messages.success(request,'User successfully registered')
            return redirect('login')
        else:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                messages.error(request,'two password does not matched')
                return render(request,'app1/login_register.html',context)


            messages.error(request,' Error registering the user') 
            messages.error(request,' - password must be at least 9 character') 
            messages.error(request,' - password must contains letters and numbers') 
            
    return render(request,'app1/login_register.html',context)
# ----------------------------------------REGISTER PAGE ENDS---------------------------------------------------------

 
def home(request):
    return render(request, 'app1/home.html')
# ----------------------------------------HOME page ENDS---------------------------------------------------------

def helpcenter(request):
    return render(request, 'app1/helpcenter.html')
# ----------------------------------------HELP CENTER page ENDS---------------------------------------------------------


def contactUs(request):

    if request.method == 'POST':
        name = request.POST['name']
        email= request.POST['email']
        message = request.POST['message']

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'app1/contactUs.html')
        
        Contact_Us.objects.create(name = name, email = email, message = message)                                      
        messages.success(request, 'Message sent successfully')

    return render(request, 'app1/contactUs.html')
# ----------------------------------------CONTACT_US PAGE ENDS---------------------------------------------------------


@login_required(login_url='login')
def dashboard(request):

    try:
        # ticker_symbol = "^GSPC"
        ticker_symbol = "^IXIC"
        # Geting the data for the ticker
        ticker_data = yf.Ticker(ticker_symbol).history(period="5y")
        ticker_fullname = yf.Ticker(ticker_symbol).info
        # print(ticker_data)
        full_name = ticker_fullname.get("shortName")
        # print(full_name)

        layout = go.Layout(width=1200, height=500)
        # Create the candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=ticker_data.index,
                                            open=ticker_data['Open'],
                                            high=ticker_data['High'],
                                            low=ticker_data['Low'],
                                            close=ticker_data['Close'])], layout=layout)
        # Seting the layout of the chart
        fig.update_layout(
            title=f"Candlestick Chart for - {full_name[:7]} Stock Exchange (5 year - present)",
            xaxis_title="Date",
            yaxis_title="Price in ($)"
            # ,template="plotly_dark"
        )
        # Converting the figure to HTML and pass it to the template
        chart_html = fig.to_html(full_html=False)


        news = News.objects.order_by('-date')[:3]

    except:
        messages.error(request,"Internet connection ko necessary")
        results=CompanyName.objects.all
        return render(request, "app1/dashboard.html",{"showName":results})

    
    #getting the company names from the database
    results=CompanyName.objects.all
    return render(request, 'app1/dashboard.html', {'chart_html': chart_html, 'ticker_data': ticker_data, "showName":results, 'news': news})
#---------------------------------------dashboard ends-----------------------------------------------------------------------------------------------------



# @csrf_exempt
def prediction(request):
    try:
        ticker_id =request.GET.get('tickerId') if request.GET.get('tickerId') != None else '' 
        # if ticker_id != '':
        ticker_item = CompanyName.objects.get(id=ticker_id)
        # Geting the data for the ticker
        ticker_data = yf.Ticker(ticker_item.symbol).history(period="5y")
        layout = go.Layout(width=1200, height=500)
        # Create the candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=ticker_data.index,
                                            open=ticker_data['Open'],
                                            high=ticker_data['High'],
                                            low=ticker_data['Low'],
                                            close=ticker_data['Close'])], layout=layout)
        # Seting the layout of the chart
        fig.update_layout(
            title=f"Candlestick Chart for - {ticker_item.symbol} ({ticker_item.name})",
            xaxis_title="Date",
            yaxis_title="Price in ($)"
            ,template="plotly_dark"
        )
        # Converting the figure to HTML and pass it to the template
        chart_html = fig.to_html(full_html=False)

        prediction_data = prediction_model(request,ticker_item.symbol)
       
        model_predicted_df = prediction_data['model_predicted_df']  
        future_df = prediction_data['future_df']
        moving_avg = prediction_data['moving_avg']
        encoded_data = prediction_data['image']  
        encoded_data2 = prediction_data['image2']  
        accuracy_dict = prediction_data['accuracy_dict']  
        print('view vitra aayo')
        print(type(encoded_data))
        print(future_df.columns)
        # print(accuracy_dict)

        # converting the dataframe to a list of dictionaries
        rows = [future_df.iloc[i].to_dict() for i in range(len(future_df))]
        rows2 = [moving_avg.iloc[i].to_dict() for i in range(len(moving_avg))]
        rows3 = [model_predicted_df.iloc[i].to_dict() for i in range(len(model_predicted_df))]
        # print(rows3)
        # print('yo ho future')
        # print(rows)
        results=CompanyName.objects.all
        # return render(request, "app1/prediction.html",{"showName":results,"df":future_df.to_html(),"image":encoded_data})

    except:
        messages.error(request, "Please select the company's SYmbol that you want to predict the price after 10 days")
        results=CompanyName.objects.all
        return render(request, "app1/prediction2.html",{"showName":results})

    else:
        return render(request, "app1/prediction.html",{"showName":results, "candleStick":chart_html, "df1":rows, "df2":rows2, "df3":rows3, "image":encoded_data, "image2":encoded_data2, "accuracy_dict":accuracy_dict})
#---------------------------------------prediction ends-----------------------------------------------------------------------------------------------------


def addSymbol(request):
    # symbol_list_us = ss.get_symbol_list(index="DJI")
    symbol_list_us = ss.get_symbol_list(index="IXIC")
    top_20_symbol = symbol_list_us[1:20]
    top_20_symbol_s = []
    top_20_symbol_name = []

    for s in top_20_symbol:
        top_20_symbol_s.append(s['symbol'])
        top_20_symbol_name.append(s['shortName'])
        #saving in the databasee
        companyname = CompanyName(symbol=s['symbol'], name=s['shortName'])
        companyname.save()
        
    print("NASDAQ ho Hai")
    print(top_20_symbol_s,top_20_symbol_name)
    return render(request, 'app1/symbolAdded.html')
#---------------------------------------add symbol  ends-----------------------------------------------------------------------------------------------------


@login_required(login_url='login')
def news(request):
    news = News.objects.all()
    context = {'news': news}
    return render(request, 'app1/news.html', context)
#---------------------------------------news ends  ends-----------------------------------------------------------------------------------------------------


@login_required(login_url='login')
def myexpense(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-id')
    paginator = Paginator(expenses,4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
            'expenses':expenses,
            'page_obj':page_obj
    }

    return render(request, 'app1/myexpense.html', context)
# ----------------------------------------EXPENSE FRONT PAGE ENDS---------------------------------------------------------



@login_required(login_url='login')
def addexpense(request):
    categories = Category.objects.all
    context = {
        'categories': categories,
        'values': request.POST
    }
 
    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        expense_date= request.POST['expense_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'app1/addexpense.html', context)
        
        elif category == '':
            messages.error(request, 'category is required')
            return render(request, 'app1/addexpense.html', context)
        
        elif not description:
            messages.error(request, 'description is required')
            return render(request, 'app1/addexpense.html', context)
 
        elif expense_date == '':
            messages.error(request, 'dateis required')
            return render(request, 'app1/addexpense.html', context)
        
        Expense.objects.create(owner = request.user,
                               amount = amount,
                               category = category,
                               description = description,
                               date = expense_date
                               )
        print(type(amount))
        

        messages.success(request, 'Expense added successfully')
        return redirect('myexpense')

    return render(request, 'app1/addexpense.html', context)
# ----------------------------------------ADD EXPENSE ENDS---------------------------------------------------------



@login_required(login_url='login')
def editexpense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all

    context = {
        'expense': expense,
        'values': expense,
        'categories':categories
 
        
    }
    print(context)

    if request.method == 'GET':
        return render(request, 'app1/editexpense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        expense_date= request.POST['expense_date']

        # try:
        #     float(amount)

        # except:
        #     messages.error(request, 'please enter number in digit')
        #     return render(request, 'app1/editexpense.html', context)

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'app1/editexpense.html', context)
        
        elif category == '':
            messages.error(request, 'category is required')
            return render(request, 'app1/editexpense.html', context)
        
        elif not description:
            messages.error(request, 'description is required')
            return render(request, 'app1/editexpense.html', context)
 
        elif expense_date == '':
            messages.error(request, 'dateis required')
            return render(request, 'app1/editexpense.html', context)
        
        amt = amount

        expense.owner = request.user
        expense.amount = amt
        expense.category = category
        expense.description = description
        expense.date = expense_date
        
        print(type(amount))

        expense.save()

        messages.success(request, 'Expense updated successfully')
        return redirect('myexpense')
    

    else:
        messages.info(request, 'Handling Update form')
        return render(request, 'app1/editexpense.html', context)
# ----------------------------------------EDIT EXPENSE ENDS---------------------------------------------------------




@login_required(login_url='login')
def deleteexpense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('myexpense')
# ----------------------------------------DELETE EXPENSE ENDS---------------------------------------------------------



# ---------------search field of my expense starts--------------------------
# @login_required(login_url='login')
def search_expense(request):
    
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expense = Expense.objects.filter(
            amount__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            date__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            description__icontains = search_str, owner = request.user) | Expense.objects.filter(
            category__icontains = search_str, owner = request.user)
            
        data = expense.values()
        

    return JsonResponse(list(data), safe = False)
# ---------------search field of my expense ends--------------------------


# ---------------------------------------- DOUGHNUT CHART OF EXPENSE KO STARTS---------------------------------------------------------
def expense_category_summary(request):
    todays_date = datetime.date.today()
    delta = datetime.timedelta(days = 30)
    thirty_days_ago = todays_date - delta  

    category_totals = {}
    for expense in Expense.objects.filter(date__gte = thirty_days_ago, owner = request.user):
        category = expense.category
        amount = expense.amount
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    # for category, total in category_totals.items():
    #     print(f"{category}: {total}")
        
    return JsonResponse({'expense_category_data': category_totals}, safe = False)
# ----------------------------------------EXPENSE CHART ENDS---------------------------------------------------------
