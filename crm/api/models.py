from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + self.last_name
