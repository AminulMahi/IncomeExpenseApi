from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ExpenseListApi.as_view(), name="expenses"),
    path('<int:id>', views.ExpenseDetailApi.as_view(), name="expense"),
]