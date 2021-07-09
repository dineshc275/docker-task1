from django.db import models

# Create your models here.


class Data1(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'data1'
        managed = True
