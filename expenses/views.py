from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExpensesSerializer
from .models import Expenses
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class ExpenseListApi(ListCreateAPIView):
    serializer_class = ExpensesSerializer
    queryset = Expenses.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class ExpenseDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Expenses.objects.all()
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

# class ExpensesApiView(APIView):

#     def get_permissions(self):
#         """
#         Instantiates and returns the list of permissions that this view requires.
#         """
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         elif self.request.method == 'POST':
#             return [IsAuthenticated()]
#         return super().get_permissions()

#     serializer_class = ExpensesSerializer
#     def get(self, request):
#         expense_obj = Expenses.objects.all()
#         serializer = self.serializer_class(expense_obj, many=True)
#         return Response({'status': 202, 'payload': serializer.data})
    

#     def post(self, request):
#         serializer = self.serializer_class(data = request.data)

#         if not serializer.is_valid():
#             return Response({'status':403, 'errors': serializer.errors, 'message': 'data is not validate'})
        
#         serializer.save()
#         return Response({'status': 200, 'payload': serializer.data, 'message': 'data successfully saved'})

#     def put(self, request):
#         pass

#     def patch(self, request):

#         try:

#             id = request.GET.get('id')
#             expense_obj = Expenses.objects.get(id = id)
#             # student_obj = Student.objects.get(id = request.data['id'])
#             serializer = ExpensesSerializer(expense_obj, data = request.data, partial=True)  # by using partial=True it will update data partially then we don't have to use patch method
#             if not serializer.is_valid():
#                 return Response({'status':403, 'errors': serializer.errors, 'message': 'data is not validate'})
            
#             serializer.save()
#             return Response({'status': 200, 'payload': serializer.data, 'message': 'data successfully updated'})

            
#         except Exception as e:
#             print(e)
#             return Response({'status': 403, 'message': 'invalid id'})

#     def delete(self, request):
#         try:
#             id = request.GET.get('id')       #we can get id also like this
#             expense_obj = Expenses.objects.get(id=id)
#             expense_obj.delete()
#             return Response({'status': 200, 'massage': 'data successfully deleted'})
#         except Exception as e:
#             print(e)
#             return Response({'status': 403, 'message': 'invalid id'}) 
