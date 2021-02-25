from django.shortcuts import render,redirect
import pandas as pd
from sqlalchemy import create_engine
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
# from models import legacytable1
from django.conf import settings
# from django.contrib.auth import logout
import psycopg2
from iteration_utilities import unique_everseen

# Create your views here.
#
# def glogin(request):
#     return render(request, 'dmac/index.html')

# Logout
# @login_required
# def logout_user(request):
#     logout(request)
#     return redirect('dmac:glogin')

# todo = [
#         {id: "01", name: "abhinav"},
#         {id: "02", name: "ashish"},
#         {id: "03", name: "ankit"},
#         {id: "04", name: "suresh"}
#     ]
# done = [
#     {id:"01",address:"rrrr"},
#     {id:"02",address:"tttt"},
#     {id:"03",address:"yyyy"},
#     {id:"04",address:"cvcvcv"}
#   ]
#  studentID=[
#     {id:"01",phone:"2344342"},
#     {id:"02",phone:"3434343"},
#     {id:"03",phone:"4334345"},
#     {id:"04",phone:"4545455"}
# ]


# @login_required
def adminhome(request):
    print("this is my df dataframe!")
    # print(df1)
    engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
    # # df1.to_sql('dmac', engine, if_exists='append')
    df_aws = pd.read_sql_query('select * from "legacytable1"', con=engine)
    df_aws1 = pd.read_sql_query('select * from "legacytable2"', con=engine)
    df_aws2 = pd.read_sql_query("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';", con=engine)
    print(df_aws2)
    print(type(df_aws2))
    print(df_aws2.columns)
    tablename_list=list(df_aws2["relname"])
    kit=df_aws
    data=kit.to_dict(orient='records')
    data1=df_aws1.to_json(orient='records')
    data2=kit.to_json(orient='records')
    data3=kit.to_json(orient='index')
    data4=kit.to_json(orient='columns')
    data5=df_aws2.to_json(orient='records')
    print(type(data))
    # print(df_aws)
    print("Hello Hind this is your updated dataframe of D-mac")
    return render(request,'dmac/login.html',{'df_aws':df_aws,'data':data,'data1':data1,'data2':data2,'data3':data3,'data4':data4,'data5':data5,'df_aws2':df_aws2,'tablename_list':tablename_list})


def Table(request):
    engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
    # # df1.to_sql('dmac', engine, if_exists='append')
    l1 = pd.read_sql_query('select * from "legacytable1"', con=engine)
    l2 = pd.read_sql_query('select * from "legacytable1"', con=engine)
    l3 = pd.read_sql_query('select * from "legacytable1"', con=engine)
    # Manipulate DataFrame using to_html() function
    table1 = l1.to_html()
    table2 = l2.to_html()
    table3 = l3.to_html()

    return HttpResponse(table1)


def merge_table(request):
    engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
    # l3.to_sql('legacytable3', engine,  if_exists='append')
    l1 = pd.read_sql_query('select * from "legacytable1"', con=engine)
    l2 = pd.read_sql_query('select * from "legacytable2"', con=engine)
    l3 = pd.read_sql_query('select * from "legacytable3"', con=engine)

    merg = pd.merge(l1, l2, on="Emp#", how="outer")
    merg1 = pd.merge(merg, l3, on="Emp#", how="outer")
    merg1["Full Name"] = merg1["First Name"] + "  " + merg1["Last Name"]

    def digit_tracker(x):
        d = str(x)
        k = len(d)
        spd = "0" * (11 - k) + d
        return spd

    merg1['uniqueid'] = merg1['Emp#'].apply(digit_tracker)
    final = merg1[["uniqueid", "Full Name", "Skills", "Technology", "Tax ID", "City", "Country Code", "Phone", "Email"]]
    final
    # final.to_sql('new_table', engine, if_exists='append')
    final.to_csv("new_table.csv")
    print("your new table is created and stored.")

    tablex = final.to_html()


    return HttpResponse(tablex)


def finaljson(request):
    engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
    # l3.to_sql('legacytable3', engine,  if_exists='append')
    l1 = pd.read_sql_query('select * from "legacytable1"', con=engine)
    l2 = pd.read_sql_query('select * from "legacytable2"', con=engine)
    l3 = pd.read_sql_query('select * from "legacytable3"', con=engine)

    merg = pd.merge(l1, l2, on="Emp#", how="outer")
    merg1 = pd.merge(merg, l3, on="Emp#", how="outer")
    merg1["Full Name"] = merg1["First Name"] + "  " + merg1["Last Name"]

    def digit_tracker(x):
        d = str(x)
        k = len(d)
        spd = "0" * (11 - k) + d
        return spd

    merg1['uniqueid'] = merg1['Emp#'].apply(digit_tracker)
    final = merg1[["uniqueid", "Full Name", "Skills", "Technology", "Tax ID", "City", "Country Code", "Phone", "Email"]]
    final
    # final.to_sql('new_table', engine, if_exists='append')
    # final.to_csv("new_table.csv")
    print("your new table is created and stored.")
    mergedata1 = [
        {"id": "03", "name": "ankit"},
        {"id": "03", "address": "yyyy"},
        {"id": "02", "phone": "3434343"},
        {"id": "03", "phone": "23344"},
        {"id": "01", "address": "rrrr"},
    ]

    tablex = final.to_json(orient='records')
    # code for reshape json and remove redundancy
    plusdata=mergedata1
    print(plusdata)
    plusdata.sort(key=lambda item: item.get("id"))
    print(plusdata)
    for i in range(len(plusdata)-1):
        if (plusdata[i]["id"] == plusdata[i + 1]["id"]):
            plusdata[i].update(plusdata[i + 1])

    for i in range(len(plusdata)-1):
        if (plusdata[i]["id"] == plusdata[i + 1]["id"]):
            plusdata[i].update(plusdata[i + 1])
            plusdata[i + 1].update(plusdata[i])
    fitdata=list(unique_everseen(plusdata, key=lambda item: frozenset(item.items())))
    print(fitdata)


    return render(request,'dmac/product.html',{'tablex':tablex,'fitdata':fitdata})


