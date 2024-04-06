import dashboard.models
from django.forms import ModelForm
from . models import DriverFiles


class MyBusinessForm(ModelForm):
    class Meta:
        model = dashboard.models.businessForm
        exclude = ('timeStamp', 'id')


class MyDriver(ModelForm):
    class Meta:
        model = DriverFiles
        exclude = ('driver_id','all_files_flag','accept_flag')