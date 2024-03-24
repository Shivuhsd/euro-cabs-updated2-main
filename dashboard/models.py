from django.db import models
import uuid
import users.models
import accounts.models

# Create your models here.
# class airportRates(models.Model):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     airportName = models.CharField(max_length=200, blank = False)
#     timeStamp = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return self.airportName



# class airportCity(models.Model):
#     id = models.UUIDField(primary_key = True, editable=False, default = uuid.uuid4)
#     fromCity = models.ForeignKey("airportRates", on_delete=models.CASCADE)
#     to = models.CharField(max_length=50, blank = False)
#     dayRate = models.DecimalField(max_digits=100, decimal_places=2)
#     nightRate = models.DecimalField(max_digits=5, decimal_places=2)
#     timeStamp = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.to

class Airports(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    name = models.CharField(max_length=100, blank = False)
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    

class City(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    name = models.CharField(max_length = 100, blank = False)
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    

class Rates(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    airport = models.ForeignKey(Airports, on_delete = models.CASCADE)
    city = models.ForeignKey(City, on_delete = models.CASCADE)
    airport_name = models.CharField(max_length=30, blank = True)
    city_name = models.CharField(max_length=30)
    nightRate = models.CharField(max_length = 20, blank = True)
    dayRate = models.CharField(max_length = 20, blank = True)
    time_stamp = models.DateTimeField(auto_now_add = True)
    who_created = models.ForeignKey(accounts.models.CustomUser, on_delete = models.PROTECT)
    

class businessForm(models.Model):
    #COMPANY DETAILS
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    Company_Name = models.CharField(max_length=200, blank=False, null=False)
    Nature_Of_Business = models.CharField(max_length=500, blank=False, null=False)
    Website_Address = models.URLField(blank=False, null=False)
    Year_Company_Est = models.CharField(max_length=4, blank=False, null=False)

    #CONTACT DETAILS
    contactName = models.CharField(max_length=200, blank=False, null=False)
    Job_Title = models.CharField(max_length=200, blank=False, null=False)
    Department = models.CharField(max_length=100, blank=False, null=False)
    TelePhone_Number = models.CharField(max_length=15, blank=False, null=False)
    Email_Address = models.EmailField(blank=False, null=False)

    #ACCOUNT DETAILS
    Monthly_Credit_Amount = models.CharField(max_length=200, blank = False, null=False)
    Monthly_Spend = models.CharField(blank = False, max_length=50, null=False)
    Authorised_By = models.CharField(blank=False, max_length=50, null=False)
    

    #TERMS AND CONDITIONS
    Terms_And_Conditions = models.BooleanField(blank=False, default=False)

    #TIME STAMP
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Company_Name
    

# Model to Store Fleet
class Fleet(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    Plate_Number = models.CharField(max_length = 10, null = True)
    Make_or_Model = models.CharField(max_length = 20, null = True)
    PH_or_HC = models.CharField(max_length = 2, null = True)
    Number_Plate = models.CharField(max_length = 20, null = True)
    Color = models.CharField(max_length = 20, null = True)
    Plate_Expiry_Date = models.DateField(null = True)
    MOT_Expiry_Date = models.DateField(null = True)


#Reply from Customers for complaint
class ReplyCus(models.Model):
    id = models.UUIDField(primary_key = True, editable= False, default = uuid.uuid4)
    com_id = models.ForeignKey(users.models.ComplaintForm, on_delete = models.PROTECT)
    which_mes = models.ForeignKey(users.models.Reply, on_delete = models.PROTECT)
    reply_mes = models.TextField(null = True)
    time_stamp = models.DateTimeField(auto_now_add = True)

    
