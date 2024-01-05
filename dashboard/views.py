from django.shortcuts import render, redirect
from django.urls import reverse
import users.models
import accounts.models
from . models import airportRates, airportCity, businessForm, Fleet, ReplyCus
from django.http import HttpResponse, JsonResponse
from .forms import MyAirportCity, MyFleets, MyReply
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from . utils import SendMail
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

# Fuction to Load Dashboard of the Admin
@login_required
def adminDashborad(request):
    if request.user.is_superuser:
        return render(request, 'admin/dashboard.html')
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
                
                # try:
                if form.is_valid():
                    obj = form.save(commit = False)
                    current_site = get_current_site(request)
                    dom = current_site.domain
                    messag = "Hey, Hello " + data.userName + "\nComplaint ID: " + data.ComplintId + "\n\n" + mesage +"\n\nIf you want to reply for this message click on below link \n\n"+ dom+"/users/comreply/" + str(data.id) +"/"+str(obj.id) +"\n\nThank You EuroCabs.."
                    SendMail(data.mail, messag, subject)
                    obj.save()
                # except InterruptedError:
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
   

# Fucntion to Add Airports to the list

def addAirports(request):
    if request.user.is_superuser:
        data = airportRates.objects.all()
    
        if request.method == 'POST':
            airportName = request.POST['airportName']
            try:
                form = airportRates(airportName = airportName)
                form.save()
            except:
                print("Something Went Wrong")

        context = {
            'data': data
        }
        return render(request, 'admin/addAirport.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')


# Function to Manage the City
    
def cityManage(request, pk):
    if request.user.is_superuser:
        form = MyAirportCity()
        aid = airportRates.objects.get(id = pk)
        data = airportCity.objects.filter(fromCity = pk)
        if request.method == 'POST':
            data = MyAirportCity(request.POST)
            if data.is_valid():
                obj = data.save(commit=False)
                obj.fromCity = aid
                obj.save()
                return redirect(reverse('cityManage', args = [pk]))
            else:
                messages.error("Something Went Wrong...")
                # print("Some Thing is Wrong in your data")
        # cityName = request.POST['cityName']
        # day = request.POST['day']
        # night = request.POST['night']
        # form = airportCity(fromCity = aid, to = cityName, dayRate = day, nightRate = night)
        # try:
        #     form.save()
        # except:
        #     print("Something Went Wrong..")
        context = {
            'data': data,
            'form': form,
            'aid': aid
        }
        return render(request, 'admin/cityManage.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')


# Custom View for 404(Page Not Found)

def custom404(request, exception = None):
    return render(request, 'admin/404.html', status=404)



# Function to Edit the City

def editCity(request, pk):
    if request.user.is_superuser:

        data = airportCity.objects.get(id = pk)
        form = MyAirportCity(instance=data)
        aid = airportRates.objects.get(id = data.fromCity.id)

        if request.method == 'POST':
            datas = MyAirportCity(request.POST, instance=data)
            if datas.is_valid():
                datas.save()
                return redirect(reverse('cityManage', args=[aid.id]))
            # obj = datas.save(commit=False)
            # obj.fromCity = aid
            # obj.save()
            else:
                messages.error(request, "Sorry, Something Went Wrong, Check Your Inputs...")
        else:
            messages.error(request, "I think you sent a bad request, for security issues we cannot allow your submit")
        

        context = {
            'form': form
        }

        return render(request, 'admin/editCity.html', context)
    else:
        return render(request, 'admin/notAuthorised.html')

# Function to Delete the City

def deleteCity(request, pk):
    if request.user.is_superuser:
        data = airportCity.objects.get(id = pk)
        aid = airportRates.objects.get(id = data.fromCity.id)

        data.delete()
        return redirect(reverse('cityManage', args=[aid.id]))
    else:
        return render(request, 'admin/notAuthorised.html')


# Function to Delete the Airport

def deleteAirport(request, pk):
    if request.user.is_superuser:
        data = airportRates.objects.get(id = pk)
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
    context = {
        'data':data
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