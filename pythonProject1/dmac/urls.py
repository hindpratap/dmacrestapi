from django.urls import path
from . import views
# from tableview import views

app_name = 'dmac'
urlpatterns = [
    path('', views.adminhome, name='adminhome'),
    # path('', views.glogin, name='glogin'),
    path('mergetable/', views.merge_table, name='mergetable'),
    path('table/', views.Table, name ="table"),
    path('finaljson/', views.finaljson, name ="finaljson"),
]