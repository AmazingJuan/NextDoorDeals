from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, BussinessAccount, PersonAccount, UserType, Role, Message, Subscription
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import AccountForm, NaturalForm, BussinesForm, loginForm, EditAccountForm
from django.core.exceptions import ValidationError
from .utilities import getRole
from property.models import Appointment, AppointmentStatus
from django.contrib import messages
import io
import base64
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt 
import json
from django.views.decorators.csrf import csrf_exempt
import stripe 
from django.conf import settings
from django.urls import reverse
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkSession(user):
    return (user and user.is_authenticated and hasattr(User.objects.get(username=user.username), 'account'))

def signupSuccess(request):
     
     return render(request, 'success.html')

def posses_subscription(user):
    


    if isinstance(user, str): 
        cont = 0
        url = user
        username = url.strip("/").split("/")[-1]
        try:
            account = Account.objects.get(user__username=username)
            subscriptions = Subscription.objects.filter(belongs_to=account)

            for subscription in subscriptions:
                if subscription.is_active:
                    cont += 1
            return cont > 0    
        except:
            return None
    else:
        if checkSession(user):
            cont = 0
            account = user.account
            subscriptions = Subscription.objects.filter(belongs_to=account)
            for subscription in subscriptions:
                if subscription.is_active:
                    cont += 1
            return cont > 0


def createUser(request):
        regularForm = AccountForm(request.POST)
        regularForm.is_valid()
        regularForm = regularForm.cleaned_data
        personForm = NaturalForm(request.POST)
        personForm.is_valid()
        personForm = personForm.cleaned_data

        bussinesForm = BussinesForm(request.POST)
        bussinesForm.is_valid()
        bussinesForm = bussinesForm.cleaned_data
        
        if User.objects.filter(username=regularForm["username"]).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('signup')

        if User.objects.filter(email=regularForm["email"]).exists():
            messages.error(request, "Email already registered. Please use a different email address.")
            return redirect('signup')

        if Account.objects.filter(phone=regularForm["phone"]).exists():
            messages.error(request, "Phone number already registered. Please use a different phone number.")
            return redirect('signup')

        user = User.objects.create_user(username = regularForm["username"], password = regularForm["password"], email = regularForm["email"])
        if(regularForm["userType"] == 'persona'):
            userType = 1
        else:
            userType = 2
        role = Role.objects.get(idRole = int(regularForm["role"]) - 1)

        cuenta = Account(user = user, phone = regularForm["phone"], userType = UserType.objects.get(idUserType=userType), role = role)
        cuenta.save()

        if(regularForm["userType"] == 'persona'):

            persona = PersonAccount(associatedAccount = cuenta, firstName = personForm["firstName"], lastName = personForm["lastName"])
            persona.save()
        else:
            negocio = BussinessAccount(associatedAccount = cuenta, nitBussinessAccount = bussinesForm["nit"], nameBussiness = bussinesForm["name"])
            negocio.save()
        login(request, user)
        return redirect('SUsuccess')


def signup(request): 
    if request.method == "POST":
        return createUser(request)
    else:
        naturalForm = NaturalForm()
        accountForm = AccountForm()
        bussinesForm = BussinesForm()
        return render(request, 'signup.html', {"userType": accountForm, "naturalForm" : naturalForm, "roles": getRole(), "requestPath":request.path, "bussinesForm":bussinesForm})


def loginUser(request): 
     
    if request.method == "POST":
            form = loginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = loginForm()
        
        form.label_suffix = "" 
    return render(request, 'login.html', {'loginForm':form})

def logout_logic(request):
    logout(request)
    return redirect('home')

def generate_bar_chart(data_dict, title, xlabel, ylabel):
    matplotlib.use('Agg')
    sorted_data = sorted(data_dict.items())
    keys = [str(k) for k, _ in sorted_data]
    values = [v for _, v in sorted_data]

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        keys,
        values,
        color=sns.color_palette("husl", len(keys)),
        edgecolor='black',
        linewidth=0.5
    )

    for bar in bars:
        bar.set_linewidth(1)
        bar.set_linestyle('-')
        bar.set_alpha(0.9)
        bar.set_zorder(3)

    plt.title(title, fontsize=18, weight='bold')
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    plt.close()

    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return graphic


def statistic_images(user):
    all_visits = user.visits.all()
    visit_count_by_year = {}
    visit_count_by_month = {}
    visit_count_by_weekday = {}
    months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ]
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for visit in all_visits:
        visit_date = visit.date
        year = visit_date.year
        visit_count_by_year[year] = visit_count_by_year.get(year, 0) + 1
        month = visit_date.month
        visit_count_by_month[month] = visit_count_by_month.get(month, 0) + 1
        weekday = visit_date.weekday()
        visit_count_by_weekday[weekday] = visit_count_by_weekday.get(weekday, 0) + 1

    visit_count_by_month_text = {months[key-1]: value for key, value in visit_count_by_month.items()}

    graphic_by_year = generate_bar_chart(visit_count_by_year, 'Visits per year', 'Year', 'Visits count')
    graphic_by_month = generate_bar_chart(visit_count_by_month_text, 'Visits per month', 'Month', 'Visits count')
    visit_count_by_weekday_text = {weekdays[key]: value for key, value in visit_count_by_weekday.items()}
    graphic_by_weekday = generate_bar_chart(visit_count_by_weekday_text, 'Visits per weekday', 'Weekday', 'Visits count')

    return graphic_by_year, graphic_by_month, graphic_by_weekday,

def edit_profile(request, username, wanna_save):
    user_to_edit = request.user
    if request.user != user_to_edit:
        messages.error(request, "You are not allowed to edit this profile")
        return redirect('view_profile', username=username)
    
    if wanna_save:
        form = EditAccountForm(request.POST or None, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Profile edited succesfully')
            return redirect('view_profile', username=user_to_edit.username)
    else:
        form = EditAccountForm(user=request.user)
    
    return render(request, 'editProfile.html', {
        'form': form,
        'profile_user': user_to_edit.account})


def view_profile(request, username):
    profile_user = Account.objects.get(user__username__iexact=username)
    if request.POST:
        if request.POST.get("action") == "rate":
            if profile_user.rating_count == 0:
                profile_user.rating = request.POST.get('rating')
            else:
                profile_user.rating = (profile_user.rating*profile_user.rating_count + int(request.POST.get('rating')))/(profile_user.rating_count + 1)
            profile_user.rating_count = profile_user.rating_count+1 
            profile_user.save()
            request.POST = None
        else:
            if request.POST.get("action") == "edit_profile":
                wanna_save = False
            else:
                wanna_save = True
            return edit_profile(request, username, wanna_save)
        

    if request.user.username == profile_user.user.username:
        is_same_user = True
        graph1, graph2, graph3 = statistic_images(profile_user)
    else:
        is_same_user = False
        graph1 = None
        graph2 = None
        graph3 = None
    return render(request, 'profile.html', {'profile_user':profile_user, 'is_same_user': is_same_user, 'graphic_year':graph1, 'graphic_month':graph2, 'graphic_weekday':graph3})
    try:
        ...
    except:
        return redirect('error')


def get_contacts(request):
    if checkSession(request.user):
        user = request.user.account

        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

        latest_messages = {}

        for message in messages:
            contact = message.receiver if message.sender == user else message.sender
            if contact not in latest_messages:
                latest_messages[contact] = message.timestamp

        contacts = sorted(latest_messages.keys(), key=lambda c: latest_messages[c], reverse=True)
        return contacts
    else:
        return None


def retrieve_appointments(account):
    if account.role.nameRole == 'Seller':
        appointments = Appointment.objects.filter(property__associatedAccount = account)
    else:
        appointments = Appointment.objects.filter(requester = account)
    return appointments

def update_appointment_status(action, appointment):
    if action == 'approve':
        appointment.status = AppointmentStatus.objects.get(name = 'Approved')
        for i in Appointment.objects.filter(date = appointment.date):
            if i != appointment:
                i.status = AppointmentStatus.objects.get(name = 'Rejected')
                i.save()
    else:
        appointment.status = AppointmentStatus.objects.get(name = 'Rejected')
    appointment.save()

def show_appointments(request):
    if request.POST:
        appointment = Appointment.objects.get(id = int(request.POST.get('appointment_id')))
        update_appointment_status(request.POST.get('action'), appointment)
        return redirect('appointments')
    else:
        associatedAccount = request.user.account
        appointments = retrieve_appointments(associatedAccount)
        return render(request, 'appointments.html', {"appointments": appointments, "current_account":associatedAccount})
    try:
        ...
    except:
        ...
 

def get_chat_history(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No estás autenticado'}, status=401)
    
    try:
        user = request.user.account
        chat_partner = Account.objects.get(user__username__iexact=username)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    messages = Message.objects.filter(
        (Q(sender=user) & Q(receiver=chat_partner)) | 
        (Q(sender=chat_partner) & Q(receiver=user))
    ).order_by('timestamp')

    messages_data = [
        {'sender': message.sender.user.username, 'content': message.content, 'timestamp': message.timestamp}
        for message in messages
    ]

    return JsonResponse({'messages': messages_data})

@csrf_exempt
def send_message(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No estás autenticado'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        message_content = data.get('message')
        receiver_username = data.get('receiver')

        if not message_content:
            return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)
        if not receiver_username:
            return JsonResponse({'error': 'Usuario receptor no especificado'}, status=400)
        
        user = request.user.account
        try:
            chat_partner = Account.objects.get(user__username__iexact=receiver_username)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Usuario receptor no existe'}, status=404)

        message = Message.objects.create(
            sender=user,
            receiver=chat_partner,
            content=message_content
        )
        
        timestamp = message.timestamp
        if hasattr(timestamp, 'isoformat'):
            timestamp = timestamp.isoformat()

        message_data = {
            'sender': message.sender.user.username,
            'content': message.content,
            'timestamp': timestamp
        }

        return JsonResponse({'message': message_data}, status=201)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
         
def subscription(request):
    return render(request, 'subscription.html')      

def info_subscription(request):
    has_subscription = False
    subscription = None
    
    if checkSession(request.user):
        has_subscription = posses_subscription(request.user)
        if has_subscription:
            subscription = Subscription.objects.filter(
                belongs_to=request.user.account, 
                is_active=True
            ).first()
    
    return render(request, 'subscription.html', {
        'has_subscription': has_subscription,
        'subscription': subscription
    })
    

def cancel_subscription(request):
    if request.method == 'POST':
        subscription = Subscription.objects.filter(
            belongs_to=request.user.account,
            is_active=True
        ).first()

        if subscription:
            subscription.delete()
            cancelled = True
        else:
            cancelled = False

        return render(request, 'cancel_subscription.html', {'cancelled': cancelled})

    return render(request, 'cancel_subscription.html', {'cancelled': False})


def create_checkout_session(request):
    if request.method == 'POST':
        if request.POST.get('period') == "monthly":
            price = "price_1ROC28PTfWgceLfwdM86isby"
            type = "monthly"
        else:
            price = "price_1ROCgwPTfWgceLfw1fzX5puD"
            type = "annual"
        try:
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=request.build_absolute_uri(reverse('pay_success')),
                cancel_url=request.build_absolute_uri(reverse('pay_fail')),
            )
            
            Subscription.objects.create(belongs_to = request.user.account, type = type)

            return HttpResponseRedirect(session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def success(request):
    account = request.user.account
    subscriptions = Subscription.objects.filter(belongs_to=account)
    print(len(subscriptions))
    last_subscription = subscriptions.last()

    if last_subscription:
        last_subscription.is_active = True
        last_subscription.save()
    return render(request, 'checkout_success.html')
    
def fail(request):

    subscriptions = Subscription.objects.filter(belongs_to = request.user.account)
    for subscription in subscriptions:
        if not subscription.is_active:
            subscription.delete()
            continue
    return render(request, 'checkout_fail.html')
