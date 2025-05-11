from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, BussinessAccount, PersonAccount, UserType, Role, Message
from django.db.models import Q
from django.http import JsonResponse
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



def checkSession(user):
    return (user and user.is_authenticated and hasattr(User.objects.get(username=user.username), 'account'))

def signupSuccess(request):
     
     return render(request, 'success.html')

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
                    return redirect('home')  # Cambia 'home' por la URL de la página de inicio
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
    # Ordenar los datos
    sorted_data = sorted(data_dict.items())
    keys = [str(k) for k, _ in sorted_data]
    values = [v for _, v in sorted_data]

    # Usar estilo bonito de Seaborn
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))


    # Crear gráfico de barras estilizado
    bars = plt.bar(
        keys,
        values,
        color=sns.color_palette("husl", len(keys)),
        edgecolor='black',
        linewidth=0.5
    )

    # Redondear las esquinas superiores de las barras
    for bar in bars:
        bar.set_linewidth(1)
        bar.set_linestyle('-')
        bar.set_alpha(0.9)
        bar.set_zorder(3)

    # Títulos y etiquetas
    plt.title(title, fontsize=18, weight='bold')
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    # Ajustar espaciado para las etiquetas
    plt.tight_layout()

    # Guardar la imagen en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    plt.close()

    # Codificar la imagen en base64
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
        print("entre aki no se pq")
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
    print(request.user.account.role.nameRole == "Buyer")
    return render(request, 'profile.html', {'profile_user':profile_user, 'is_same_user': is_same_user, 'graphic_year':graph1, 'graphic_month':graph2, 'graphic_weekday':graph3})
    try:
        ...
    except:
        return redirect('error')


def get_contacts(request):
    user = request.user.account

    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

    latest_messages = {}

    for message in messages:
        contact = message.receiver if message.sender == user else message.sender
        if contact not in latest_messages:
            latest_messages[contact] = message.timestamp  # Solo se guarda el primero (más reciente por orden)

    # Ordenar contactos por el timestamp más reciente
    contacts = sorted(latest_messages.keys(), key=lambda c: latest_messages[c], reverse=True)
    print(contacts)
    return contacts


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
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_content = data.get('message')
            reciever_username = data.get('receiver')

            # Asegurarse de que el mensaje no esté vacío
            if not message_content:
                return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)
            
            user = request.user.account
            chat_partner = Account.objects.get(user__username__iexact=reciever_username)
            print(chat_partner)

            # Crear el nuevo mensaje
            message = Message.objects.create(
                sender=user,
                receiver=chat_partner,
                content=message_content
            )
            
            # Devolver el mensaje en la respuesta
            message_data = {
                'sender': message.sender.user.username,
                'content': message.content,
                'timestamp': message.timestamp
            }

            return JsonResponse({'message': message_data}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
         
        
        
    


