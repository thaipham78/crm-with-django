from rest_framework import serializers
from .models import Company, Contact
import re


def is_name_valid(val):
    regex = r"^[a-zA-Z\s]+$"
    if re.fullmatch(regex, val) == None:
        raise serializers.ValidationError("Invalid Name")
    return val


def is_email_valid(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, email) == None:
        raise serializers.ValidationError("Invalid Email")


def is_phone_valid(val):
    regex = r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    if re.fullmatch(regex, val) == None:
        raise serializers.ValidationError("Invalid phone number")
    return val


def is_company_phone_exists(self, val):
    request = self.context.get("request")
    if request.method == "POST":
        status = Company.objects.filter(phone=val).exists()
        if status:
            raise serializers.ValidationError("Phone exists")
        return val

    if request.method == "PUT":
        company_id = self.context.get("id")
        status = Company.objects.filter(phone=val).exclude(id=company_id).exists()
        if status:
            raise serializers.ValidationError("Phone exists")
        return val


def is_contact_phone_exists(self, val):
    request = self.context.get("request")
    if request.method == "POST":
        status = Contact.objects.filter(phone=val).exists()
        if status:
            raise serializers.ValidationError("Phone exists")
        return val

    if request.method == "PUT":
        contact_id = self.context.get("id")
        status = Contact.objects.filter(phone=val).exclude(id=contact_id).exists()
        if status:
            raise serializers.ValidationError("Phone exists")
        return val


def is_company_email_exists(self, val):
    request = self.context.get("request")
    if request.method == "POST":
        status = Company.objects.filter(email=val).exists()
        if status:
            raise serializers.ValidationError("Email exists")
        return val

    if request.method == "PUT":
        company_id = self.context.get("id")
        status = Company.objects.filter(email=val).exclude(id=company_id).exists()
        if status:
            raise serializers.ValidationError("Email exists")
        return val


def is_company_name_exists(self, val):
    request = self.context.get("request")
    if request.method == "POST":
        status = Company.objects.filter(name=val).exists()
        if status:
            raise serializers.ValidationError("Name exists")
        return val

    if request.method == "PUT":
        company_id = self.context.get("id")
        status = Company.objects.filter(name=val).exclude(id=company_id).exists()
        print
        if status:
            raise serializers.ValidationError("Name exists")
        return val


def is_contact_name_exists(self, data):
    request = self.context.get("request")
    if request.method == "POST":
        contacts = Contact.objects.filter(first_name=data["first_name"])
        for item in contacts:
            if item.last_name == data["last_name"]:
                raise serializers.ValidationError("Contact name exists")
        return data
    if request.method == "PUT":
        contact_id = self.context.get("id")
        records = Contact.objects.filter(first_name=data["first_name"]).exclude(
            id=contact_id
        )

        for item in records:
            if item.last_name == data["last_name"]:
                raise serializers.ValidationError("Contact name exists")
        return data


def is_contact_email_exists(self, val):
    request = self.context.get("request")
    if request.method == "POST":
        status = Contact.objects.filter(email=val).exists()
        if status:
            raise serializers.ValidationError("Email exists")
        return val

    if request.method == "PUT":
        contact_id = self.context.get("id")
        status = Contact.objects.filter(email=val).exclude(id=contact_id).exists()
        if status:
            raise serializers.ValidationError("Email exists")
        return val


class CompanySeriallizer(serializers.ModelSerializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()

    def validate_name(self, value):
        _value = is_name_valid(value)
        _value = is_company_name_exists(self, value)
        return _value

    def validate_phone(self, value):
        _value = is_phone_valid(value)
        _value = is_company_phone_exists(value)
        return _value

    def validate_email(self, value):
        _value = is_email_valid(value)
        _value = is_company_email_exists(value)
        return _value

    class Meta:
        model = Company
        fields = ["id", "name", "phone", "email"]


class ContactSeriallizer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()

    def validate_last_name(self, value):
        _value = is_name_valid(value)
        return _value

    def validate_first_name(self, value):
        _value = is_name_valid(value)
        return _value

    def validate_phone(self, value):
        _value = is_phone_valid(value)
        _value = is_contact_phone_exists(self, value)
        return _value

    def validate_email(self, value):
        _value = is_email_valid(value)
        _value = is_contact_email_exists(self, value)
        return _value

    def validate(self, data):
        _value = is_contact_name_exists(self, data)
        return _value

    class Meta:
        model = Contact
        fields = ["id", "first_name", "last_name", "phone", "email", "company"]



   