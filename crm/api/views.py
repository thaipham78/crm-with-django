from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Company, Contact
from .serializers import CompanySeriallizer, ContactSeriallizer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class CompanyListApiView(APIView):
    permission_classes = [IsAuthenticated]
    # 1. List all
    def get(self, request, *args, **kwargs):
        offset = request.query_params.get("offset")
        limit = request.query_params.get("limit")
        companies = Company.objects.all()[offset:limit]
        serializer = CompanySeriallizer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "phone": request.data.get("phone"),
            "email": request.data.get("email"),
        }
        serializer = CompanySeriallizer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, company_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, company_id, *args, **kwargs):
        """
        Retrieves the Todo with given todo_id
        """
        record = self.get_object(company_id)
        if not record:
            return Response(
                {"res": "Company with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CompanySeriallizer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, company_id, *args, **kwargs):
        """
        Updates the todo item with given todo_id if exists
        """
        record = self.get_object(company_id)
        if not record:
            return Response(
                {"res": "Company with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "name": request.data.get("name"),
            "phone": request.data.get("phone"),
            "email": request.data.get("email"),
        }
        serializer = CompanySeriallizer(
            instance=record,
            data=data,
            partial=True,
            context={"request": request, "id": company_id},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, company_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        record = self.get_object(company_id)
        if not record:
            return Response(
                {"res": "Company with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)


class ContactListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # 1. List all
    def get(self, request, *args, **kwargs):
        offset = request.query_params.get("offset")
        limit = request.query_params.get("limit")
        contacts = Contact.objects.all()[offset:limit]
        serializer = ContactSeriallizer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone": request.data.get("phone"),
            "email": request.data.get("email"),
            "company": request.data.get("company_id"),
        }
        serializer = ContactSeriallizer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, contact_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, contact_id, *args, **kwargs):
        """
        Retrieves the Todo with given todo_id
        """
        record = self.get_object(contact_id)
        if not record:
            return Response(
                {"res": "Contact with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ContactSeriallizer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, contact_id, *args, **kwargs):
        """
        Updates the todo item with given todo_id if exists
        """
        record = self.get_object(contact_id)
        if not record:
            return Response(
                {"res": "Contact with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone": request.data.get("phone"),
            "email": request.data.get("email"),
            "company": request.data.get("company_id"),
        }
        serializer = ContactSeriallizer(
            instance=record,
            data=data,
            partial=True,
            context={"request": request, "id": contact_id},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, contact_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        record = self.get_object(contact_id)
        if not record:
            return Response(
                {"res": "Contact with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    # permission_classes = []

    def post(self, request):
        name = request.data.get("name")
        password = request.data.get("password")
        print(name,password)
        incoming_user = authenticate(username=name, password=password)

        if incoming_user is not None:
            token = Token.objects.create(user=incoming_user)

            response = {"message": "Login Successfull", "tokens": token.key}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid name or password"})

    def get(self, request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


