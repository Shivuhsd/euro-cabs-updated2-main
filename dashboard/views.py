from django.core.mail import EmailMessage
from io import BytesIO
from django.shortcuts import render, redirect
from django.urls import reverse
import users.models
import users.custom
import users.forms
import accounts.models
from . models import businessForm, Fleet, ReplyCus, Airports, City, Rates, SchoolContract, TrackSchoolContract
from django.http import HttpResponse, JsonResponse
from .forms import MyFleets, MyReply, MyAirport, MyCity, MyRates, MySchoolContract
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone, date
from . utils import SendMail
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.template.loader import render_to_string
import os
from django.template.loader import get_template
from xhtml2pdf import pisa
import calendar
from openpyxl import Workbook

# Create your views here.

# Fuction to Load Dashboard of the Admin
@login_required
def adminDashborad(request):
    if request.user.is_superuser:
        total_complaints = len(users.models.ComplaintForm.objects.all())
        total_Business_query = len(businessForm.objects.all())
        total_Routes = len(Rates.objects.all())
        total_cities = len(City.objects.all())
        total_airports = len(Airports.objects.all())
        total_Fleet = len(Fleet.objects.all())

        month_names = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
        ]

        data = users.models.ComplaintForm.objects.all()
        today = datetime.now().month
        data_one = len(data.filter(created_at__month = today))

        two = datetime.now() - timedelta(days=30)
        data_two = len(data.filter(created_at__month = two.month))

        three = datetime.now() - timedelta(days=60)
        data_three = len(data.filter(created_at__month = three.month))

        four = datetime.now() - timedelta(days=90)
        data_four = len(data.filter(created_at__month = four.month))

        months_data = [data_one, data_two, data_three, data_four]

        month_name = []
        j = 0
        while(j < 4):
            month_name.append(month_names[today-1])
            today -= 1
            j += 1

        month_name.reverse()
        months_data.reverse()
    
        context = {
            'total_business_query': total_Business_query,
            'total_airports': total_airports,
            'total_cities': total_cities,
            'total_Routes': total_Routes,
            'total_Fleet': total_Fleet,
            'total_complaints': total_complaints,
            # 'data_for_chart': data_for_chart,
            'months': month_name,
            'data': months_data
        }
        return render(request, 'admin/dashboard.html', context)
    return render(request, 'admin/notAuthorised.html')

# Function to Load the Complaints to the user

def complaints(request):
    if request.user.is_superuser:
        data = users.models.ComplaintForm.objects.filter(opened = False)

        context = {
            'complaints': data
        }
    else:
        return render(request, 'admin/notAuthorised.html')
    return render(request, 'admin/complaints.html', context)


# Function to Display the Complaint to Admin

def showComplaint(request, pk):
    if request.user.is_superuser:
       


        # try:
            cusreply = ''
            data = users.models.ComplaintForm.objects.get(id = pk)

            replys = users.models.Reply.objects.filter(com_id = data.id)
            
            
            cusreply = ReplyCus.objects.filter(com_id = data.id)
            
            

            if request.method == 'POST':
                mesage = request.POST['reply-message']
                form = MyReply({'messages' : mesage, 'com_id' : data, 'who_sent' : request.user})
                subject = "Hello, This is a  message from Eurocabs for your Complaint.."
                
                try:
                    if form.is_valid():
                        obj = form.save(commit = False)
                        current_site = get_current_site(request)
                        dom = current_site.domain
                        messag = "Hey, Hello " + data.userName + "\nComplaint ID: " + data.ComplintId + "\n\n" + mesage +"\n\nIf you want to reply for this message click on below link \n\n"+ dom+"/users/comreply/" + str(data.id) +"/"+str(obj.id) +"\n\nThank You EuroCabs.."
                        SendMail(data.mail, messag, subject)
                        obj.save()
                except InterruptedError:
                    messages.error(request, "Sorry Can't Send Mail... Try Again..")


            context = {
                'data': data,
                'reply': replys,
                'cusreply': cusreply
            }
            
            # for i in replys:
            #     for j in cusreply:
            #         if i.id in cusreply_dict:
            #             print("id Reply :" + str(i.id) + "---- Id CusReply" + str(j.which_mes.id))
            #             print("Hello This is Customer Reply..." + j.reply_mes)

            return render(request, 'admin/showComplaint.html', context)
        # except:
        #     return custom404(request)
        
    else:
        return render(request, 'admin/notAuthorised.html')

#Function To Accept the Token

def tokenAccepted(request, pk):
    try:
        data = users.models.ComplaintForm.objects.get(id = pk)
        data.opened = True
        data.ongoing = True
        data.save()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'failed'})
    

def Resolved(request, pk):
    try:
        data = users.models.ComplaintForm.objects.get(id = pk)
        data.ongoing = False
        data.closed = True
        data.save()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'failed'})
   



def addCity(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            cityName = request.POST['cityName']
            city = City(name = cityName)
            city.save()
            messages.success(request, "City Added Succesfully")
            return redirect("addAirports")

# Fucntion to Add Airports to the list

def addAirports(request):
    if request.user.is_superuser:
        routes = Rates.objects.all()
        if request.method == 'POST':
            airportName = request.POST['airportName']
            airport = Airports(name = airportName)
            airport.save()
            messages.success(request, "Airport Added Successfully..")

        airports = Airports.objects.all()
        cities = City.objects.all()
        context = {
            # 'data': data
            'airports': airports, 
            'cities': cities,
            'routes': routes
        }
        return render(request, 'admin/addAirport.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')

def airportManage(request, pk):
    if request.user.is_superuser:
        data = Airports.objects.get(id = pk)
        form = MyAirport(instance = data)
        if request.method == 'POST':
            form = MyAirport(request.POST, instance=data)
            if form.is_valid():
                form.save()
        context = {
            'form': form,
            'data': data
        }

        return render(request, 'admin/editAirport.html', context)


# Function to Manage the City
    
def cityManage(request, pk):
    if request.user.is_superuser:
        data = City.objects.get(id = pk)
        form = MyCity(instance = data)
        if request.method == 'POST':
            data = MyCity(request.POST, instance = data)
            if data.is_valid():
                data.save()
                return redirect("addAirports")
            else:
                messages.error("Something Went Wrong...")
        context = {
            'form': form,
            'data': data
        }
        return render(request, 'admin/editCity.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')


# Custom View for 404(Page Not Found)
def custom404(request, exception = None):
    return render(request, 'admin/404.html', status=404)



# Function to Edit the City
def CreateRoute(request):
    cities = City.objects.all()
    airports = Airports.objects.all()
    if request.method == 'POST':
        airport = request.POST['airport']
        city = request.POST['city']
        dayRate = request.POST['dayRate']
        nightRate = request.POST['nightRate']

        airp = airports.get(id = airport)
        cit = cities.get(id = city)
        
        try:
            air = Rates.objects.filter(airport = airp)
            air.get(city = cit)
            messages.error(request, "There is Already a Route....")
        except:
            data = Rates(airport = airp, city = cit, dayRate = dayRate, nightRate = nightRate, airport_name = airp.name, city_name = cit.name, who_created = request.user)
            data.save()
            messages.success(request, "Route Created Successfully..")

    context = {
        'cities': cities,
        'airports': airports
    }
    return render(request, 'admin/createRoute.html', context)

# Function to Delete the City

def deleteCity(request, pk):
    if request.user.is_superuser:
        data = City.objects.get(id = pk)
        data.delete()
        return redirect('addAirports')
    else:
        return render(request, 'admin/notAuthorised.html')


# Function to Delete the Airport

def deleteAirport(request, pk):
    if request.user.is_superuser:
        data = Airports.objects.get(id = pk)
        data.delete()
        return redirect('addAirports')
    else:
        return render(request, 'admin/notAuthorised.html')


#To Fecth All Business Forms

def businessForms(request):
    if request.user.is_superuser:
        data = businessForm.objects.all()

        context = {
            'data': data
        }
        return render(request, 'admin/businessForms.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')


#To Fetch Single Business Form
def businessFormView(request, pk):
    if request.user.is_superuser:
        data = businessForm.objects.get(id = pk)

        context = {
            'data':data
        }
        return render(request, 'admin/businessFormView.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')
    

# Function to View Old Complaints
@login_required(login_url='userLogin')
def oldComplaints(request):
    data = users.models.ComplaintForm.objects.filter(closed = True)

    context = {
        'complaints': data
    }

    return render(request, 'admin/oldComplaints.html', context)

def onGoing(request):
    data = users.models.ComplaintForm.objects.filter(ongoing = True)

    context = {
        'complaints':data
    }

    return render(request, 'admin/ongoingCom.html', context)


@login_required(login_url='userLogin')
def DriverFiles(request):
    data = users.models.DriverFiles.objects.filter(accept_flag = False)

    drivers = users.models.DriverFiles.objects.filter(accept_flag = True)

    context = {
        'data':data,
        'drivers':drivers
    }
    return render(request, 'admin/driverFiles.html', context)



# Function to view Driver Files for verification
@login_required(login_url='userLogin')
def DriverFilesView(request, pk):
    user = accounts.models.CustomUser.objects.get(id = pk)
    exuser = accounts.models.ExtendUser.objects.get(id_user = user)
    driverFiles = users.models.DriverFiles.objects.get(driver_id = user)

    if request.method == 'POST':
        if driverFiles.all_files_flag == True:
            driverFiles.accept_flag = True
            driverFiles.save()
        else:
            messages.error("Someting Went Wrong")


    context = {
        'user':user,
        'exuser': exuser,
        'driverFiles': driverFiles
    }

    return render(request, 'admin/driverfilesView.html', context)



# Function to handle the fleet
def MyFleet(request):
    form = MyFleets()
    if request.method == 'POST':
        plate_number = request.POST['plate-number']
        make = request.POST['make']
        phhc = request.POST['phhc']
        number_plate = request.POST['number-plate']
        color = request.POST['color']
        ped1 = request.POST['ped']
        # ped = datetime.strptime(ped1, '%Y-%m-%d').date()
        med1 = request.POST['med']
        # med = datetime.strptime(med1, '%Y-%m-%d').date()

        try:
            form = Fleet(
            Plate_Number = plate_number,
            Make_or_Model = make,
            PH_or_HC = phhc,
            Number_Plate = number_plate,
            Color = color,
            Plate_Expiry_Date = ped1,
            MOT_Expiry_Date = med1
            )

            form.save()
            messages.success(request, "Vehicle Added..")
        except ValueError:
            messages.error(request, "Invalid Values...")


        # data = MyFleets(request.POST)
        # if data.is_valid():
        #     data.save()
    
    context = {
        'form': form
    }
    return render(request, 'admin/myfleet.html', context)


def ManageFleet(request):
    context = {}
    today = datetime.now().date()
    fleet_info_list = []
    mot_list = []
    if request.method == 'GET':
        q = request.GET['q']
        if q == 'all' or q == None:
            threshhold = today + timedelta(days=60)
            Pexp = Fleet.objects.all()
            for i in Pexp:
                if i.Plate_Expiry_Date <= threshhold:
                    fleet_info_list.append(i)
            
            for j in Pexp:
                if j.MOT_Expiry_Date <= threshhold:
                    mot_list.append(j)
        
            context = {
                'mot': mot_list,
                'exwar': fleet_info_list,
                'data' : Pexp
            }
        
        if q == 'warning':
            threshhold = today + timedelta(days=60)
            Pexp = Fleet.objects.all()
            for i in Pexp:
                if i.Plate_Expiry_Date <= threshhold:
                    fleet_info_list.append(i)
            
            for j in Pexp:
                if j.MOT_Expiry_Date <= threshhold:
                    mot_list.append(j)
        
            context = {
                'mot': mot_list,
                'exwar': fleet_info_list,
                # 'data' : Pexp
            }
        
        if q == 'exp':
            threshhold = today
            Pexp = Fleet.objects.all()
            for i in Pexp:
                if i.Plate_Expiry_Date < threshhold:
                    fleet_info_list.append(i)
            
            for j in Pexp:
                if j.MOT_Expiry_Date < threshhold:
                    mot_list.append(j)
        
            context = {
                'exps': 'exps',
                'mot': mot_list,
                'exwar': fleet_info_list,
                # 'data' : Pexp
            }

    return render(request, 'admin/managefleet.html', context)





def EditFleet(request, pk):
    if request.user.is_superuser:

        data = Fleet.objects.get(id = pk)
        form = MyFleets(instance=data)
        

        if request.method == 'POST':
            datas = MyFleets(request.POST, instance=data)
            if datas.is_valid():
                datas.save()
                messages.success(request, 'Succesfully Updated The Vehicle Information')
                return redirect(reverse('editfleet', args=[pk]))
            # obj = datas.save(commit=False)
            # obj.fromCity = aid
            # obj.save()
            else:
                messages.error(request, "Sorry, Something Went Wrong, Check Your Inputs...")
        # else:
        #     messages.error(request, "I think you sent a bad request, for security issues we cannot allow your submit")
        

        context = {
            'form': form,
            'data': data
        }

    return render(request, 'admin/editfleet.html', context)

def DeleteFleet(request, pk):
    data = Fleet.objects.get(id = pk)
    data.delete()
    messages.success(request, "Deleted Successfully..")
    return render(request, 'admin/managefleet.html')


# View to Edit a Route
def EditRoute(request, pk):
    data = Rates.objects.get(id = pk)
    form = MyRates(instance= data)

    if request.method == 'POST':
        dat = MyRates(request.POST, instance=data)
        if dat.is_valid():
            obj = dat.save(commit= False)
            obj.who_created = request.user
            obj.save()
            messages.success(request, 'Route Updated Successfully..')
            return redirect(reverse('editroute', args=[pk]))
        else:
            messages.error(request, 'Something Went Wrong..')

    context = {
        'form':form,
    }
    return render(request, 'admin/editRoute.html', context)

# View to Delete a Route
def DeleteRoute(request, pk):
    data = Rates.objects.get(id = pk)
    data.delete()
    messages.success(request, "Route Deleted Successfully...")
    return redirect('addAirports')


# A FUNCTION FOR ADDING A DRIVER BY ADMIN

def Adddriver(request):
    form = users.forms.MyDriver
    if request.method == 'POST':
        email = request.POST['email']
        name = str(request.POST['name'])
        phone = str(request.POST['phone'])
        try:
            password = users.custom.generate_unique_random_numbers(10)
            data = accounts.models.CustomUser.objects.create_user(username=email, email=email, password=password, is_active = True, first_name = name)

            form = accounts.models.ExtendUser(phone_number = phone, id_user = data, phone_code = "+91")
            form.save()
            
            subject = "Driver Application Status"
            mess = "Hi, "+name+ "/nYou have Selected as a Driver at EuroCabs /n/n"+"Account Details:/n email: "+ email +"/nPassword: "+password +"/n/nDo Not Share This Password With Anyone Else.../n/nThank You"
            
            SendMail(email, mess, subject)

            data = users.forms.MyDriver(request.POST, request.FILES)
            if data.is_valid():
                obj = data.save(commit=False)
                obj.driver_id = request.user
                obj.all_files_flag = True
                obj.save()
                return redirect('driverFiles')
            else:
                messages.error(request, 'Something Went Wrong')
        except:
            messages.error(request, "User With This Email Already Exists...")
    context = {
        'form':form
    }
    return render(request, 'admin/adddriveradmin.html', context)


def ExpiryMail(request, pk, email):
    data = Fleet.objects.get(id = pk)
    # email = email
    subject = "Regarding the Expiry of the Vehicle Documents"
    message = "Hello, From 'Eurocabs.uk' "+ "\n\nPlate Number: " + str(data.Plate_Number) + "\n\nMake or Model: " + str(data.Make_or_Model) + "\n\nPH or HC: "+ str(data.PH_or_HC) + "\n\nNumber Plate: " + str(data.Number_Plate) + "\n\nColor: "+ str(data.Color) + "\n\nPlate Expiry Date: "+ str(data.Plate_Expiry_Date) + "\n\nMOT Expiry Date: " + str(data.MOT_Expiry_Date) + "\n\nThank You"

    SendMail(email, message, subject)

    return JsonResponse({"status":"ok"})

from django import forms
class FileUploadForm(forms.Form):
    files = forms.FileField(widget=forms.TextInput(attrs={"name": "images",
            "type": "File",
            "class": "form-control",'multiple': True}))


def FleetMail(request, pk):
    data = Fleet.objects.get(id = pk)
    form = FileUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        mail = request.POST['email']
        sub = request.POST['subject']
        mes = request.POST['message']
        uploaded_files = request.FILES.getlist('files')
       
        try:
            request.POST['include']
            inlcude = request.POST['include']
        except:
            inlcude = "off"
        

        template = get_template('admin/mail.html')
        html = template.render({'data': data})

        # Create a PDF
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            return HttpResponse('Error generating PDF: %s' % pisa_status.err)

        # Send email with PDF attachment
        subject = sub
        message = mes
        email = EmailMessage(subject, message, 'eurocabs.uk', [mail])
        for file in uploaded_files:
            email.attach(file.name, file.read(), file.content_type)
        if inlcude == "on":
            email.attach('Vehicle_info.pdf', pdf_file.getvalue(), 'application/pdf')
        email.send()

       
    #     # To Create a data in html file
    #     html_content = render_to_string('admin/mail.html', {'data':data})


    #     # Creating a temporary html file to render html file
    #     pdf_content = HTML(string=html_content).write_pdf()

    # # Create a temporary PDF file
    #     pdf_file_path = os.path.join(settings.BASE_DIR, 'temp.pdf')
    #     with open(pdf_file_path, 'wb') as pdf_file:
    #         pdf_file.write(pdf_content)

    #     # Send PDF via email
    #     subject = sub
    #     message = mes
    #     email = EmailMessage(subject, message, "eurocabsnoreply", [mail])
    #     email.attach_file(pdf_file_path)
    #     email.send()

    #     # Delete temporary PDF file
    #     os.remove(pdf_file_path)

    else:
        pass
    context = {
        'data':data,
        'form':form
    }
    return render(request, 'admin/fleetmail.html', context)



def AddSchoolContract(request):
    form = MySchoolContract
    if request.method == 'POST':
        data = MySchoolContract(request.POST)
        if data.is_valid():
            data.save()
            return redirect('schoolcontractall')
        else:
            messages.error(request, 'Something Went Wrong..!')

    context = {
        'form':form
    }
    return render(request, 'admin/schoolContractadd.html', context)


def SchoolContractEdit(request, pk):
    data = SchoolContract.objects.get(id = pk)
    form = MySchoolContract(instance=data)
    if request.method == 'POST':
        sform = MySchoolContract(request.POST, instance=data)
        if sform.is_valid():
            sform.save()
            return redirect('schoolcontractall')
        else:
            messages.error(request, 'Something Went Wrong..!')


    context = {
        'form':form,
        'data':data
    }
    return render(request, 'admin/schoolcontractedit.html', context)


class EventCalendar(calendar.HTMLCalendar):
    def __init__(self, events):
        super().__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        events_from_day = events.filter(date__day=day)
        events_html = "<ul>"
        status_color = None

        for event in events_from_day:
            events_html += f"<h4>{event.status}</h4>"
            if event.status == 'Completed':
                status_color = 'green'
            elif event.status == 'No Fare':
                status_color = 'red'
            elif event.status == 'No School':
                status_color = 'purple'

        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            if status_color:
                return f'<td class="{self.cssclasses[weekday]}" style="background-color: {status_color}">{day}{events_html}</td>'
            return f'<td class="{self.cssclasses[weekday]}">{day}{events_html}</td>'

    def formatmonth(self, theyear, themonth, withyear=True):
        events = self.events.filter(date__year=theyear, date__month=themonth)
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatweek(self, theweek, events):
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return f'<tr>{s}</tr>'

# def calendar_view(request, year, month):
#     year = int(year)
#     month = int(month)
#     cal = EventCalendar(TrackSchoolContract.objects.all())
#     html_calendar = cal.formatmonth(year, month)
#     return render(request, 'calendarapp/calendar.html', {'calendar': html_calendar, 'year': year, 'month': month})


# View To Show The School Contract Details

def SchoolContractView(request, pk):
    today = date.today()
    formatted_today = today.strftime('%Y-%m-%d')
    data = SchoolContract.objects.get(id = pk)

    if request.method == 'POST':
        status = request.POST['status']
        dat = request.POST['date']
        check_date = datetime.strptime(dat, '%Y-%m-%d').date()

        check = TrackSchoolContract.objects.filter(date=check_date).exists()

        if check:
            messages.error(request, "Already Exists")
        else:
            try:
                form = TrackSchoolContract(contract = data, date = dat, status = status)
                form.save()
            except:
                messages.error(request, "Something Went Wrong..")

    now = datetime.now()
    year = int(now.year)
    month = int(now.month)
    cal = EventCalendar(TrackSchoolContract.objects.all())
    html_calendar = cal.formatmonth(year, month)
    context = {
        'data':data,
        'today': formatted_today,
        'calendar': html_calendar,
        'year': year, 
        'month': month
    }
    return render(request, 'admin/schoolcontractview.html', context)


def SchoolContractDelete(request, pk):
    data = SchoolContract.objects.get(id = pk)
    data.delete()
    return render(request, "admin/schoolcontractall.html")


from datetime import datetime, timedelta
from django.utils import timezone

def SchoolContractall(request):
    current_date = timezone.now()
    one_month_from_now = current_date + timedelta(days=30)
    exp = SchoolContract.objects.filter(end_date__lte = one_month_from_now)
    data = SchoolContract.objects.all()
    context = {
        'data':data,
        'exp':exp
    }
    return render(request, "admin/schoolcontractall.html", context)



# View to Create a Contract Report in xlsl

def ContractReport(request, pk):
    if request.method == "POST":
        year = int(request.POST['year'])
        month = int(request.POST['month'])

    # Filter contracts by the specific month
        contract = TrackSchoolContract.objects.filter(
            contract = pk,
            date__year=year,
            date__month=month
        ).exists()

        if contract:
            contracts = TrackSchoolContract.objects.filter(
            contract = pk,
            date__year=year,
            date__month=month
            )
            
            wb = Workbook()
            ws = wb.active
            ws.title = f"Contracts {year}-{month:02d}"

            # Write headers
            headers = ['Contract School Name', 'Date', 'Status']
            ws.append(headers)

            # Write data
            for contract in contracts:
                ws.append([
                    str(contract.contract),  # Adjust if you need to access specific fields
                    contract.date.strftime('%Y-%m-%d') if contract.date else '',
                    contract.status,
                    # contract.time_stamp.strftime('%Y-%m-%d %H:%M:%S')
                ])

            # Prepare the response
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = f'attachment; filename="contracts_{year}_{month:02d}.xlsx"'

            # Save the workbook to the response
            wb.save(response)

            return response
        else:
            messages.error(request, "Data Not Found")
            return redirect(reverse('viewschoolcontract', args=[pk]))
    else:
        messages.error(request, "Data Not Found")
        return HttpResponse("nothing")


        # Create an Excel workbook and sheet
        










