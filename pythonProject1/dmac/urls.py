from django.urls import path
from . import views
# from rest_framework import routers
# from .api import LeadViewSet
# from tableview import views

# router = routers.DefaultRouter()
# router.register('api/leads',LeadViewSet,'leads')

app_name = 'dmac'
urlpatterns = [
    path('', views.adminhome, name='adminhome'),
    # path('', views.glogin, name='glogin'),
    path('article/', views.article_list, name='glogin'),
    path('tab_details/', views.tab_details, name='tab_details'),
    path('mergetable/', views.merge_table, name='mergetable'),
    path('table/', views.Table, name ="table"),
    path('finaljson/', views.finaljson, name ="finaljson"),
    path('posttable/', views.posttable, name ="posttable"),
    path('postdata/', views.postdata, name ="postdata"),
    path('concatdata/', views.concatdata, name ="concatdata"),
    path('concattable/', views.concattable, name ="concattable"),
    path('jsonreducer/', views.jsonreducer, name ="jsonreducer"),
    path('save_json_to_table/', views.save_json_to_table, name ="save_json_to_table"),

]
# urlpatterns = router.urls