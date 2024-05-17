from django.core.mail import send_mail
from . models import Rates

def SendMail(email, message, subject):
    send_mail(
        subject,
        message, 
        'eurocabs@noreply.com',
        [email],
        fail_silently=False
    )

# To Find Out Duplicate Route in Admin Panel
    
def DuplicateRoute(cit, airp):
    try:
        air = Rates.objects.filter(airport = airp)
        air.get(city = cit)
        return True
    except:
        return False
    
# TO Get Complaints of Last Six Days
    



