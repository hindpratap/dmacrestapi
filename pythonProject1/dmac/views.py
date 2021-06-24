from django.shortcuts import render,redirect
import pandas as pd
from sqlalchemy import create_engine
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
# from models import legacytable1
from django.conf import settings
# from django.contrib.auth import logout
from django.http import JsonResponse
import psycopg2
from iteration_utilities import unique_everseen
import json

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
    todo = [
            {"id": "01", "name": "abhinav"},
            {"id": "02", "name": "ashish"},
            {"id": "03", "name": "ankit"},
            {"id": "04", "name": "suresh"}
        ]
    done = [
        {"id":"01","address":"rrrr"},
        {"id":"02","address":"tttt"},
        {"id":"03","address":"yyyy"},
        {"id":"04","address":"cvcvcv"}
      ]
    #  studentID=[
    #     {"id":"01","phone":"2344342"},
    #     {"id":"02","phone":"3434343"},
    #     {"id":"03","phone":"4334345"},
    #     {"id":"04","phone":"4545455"}
    # ]
    try:
        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # # df1.to_sql('dmac', engine, if_exists='append')
        df_aws = pd.read_sql_query('select * from "legacytable1"', con=engine)
        df_aws1 = pd.read_sql_query('select * from "legacytable2"', con=engine)
        df_aws2 = pd.read_sql_query("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';", con=engine)
        tablename_list = list(df_aws2["relname"])
    except:
        df_aws = pd.DataFrame(todo)
        df_aws1 = pd.DataFrame(done)
        tablename_list=["table1","table2","table3"]
        df_aws2="hello dmac"


    kit=df_aws
    data=kit.to_dict(orient='records')
    data1=df_aws1.to_json(orient='records')
    data2=kit.to_json(orient='records')
    data3=kit.to_json(orient='index')
    data4=kit.to_json(orient='columns')
    # data5=df_aws2.to_json(orient='records')
    print(type(data))
    # print(df_aws)
    print("Hello Hind this is your updated dataframe of D-mac")
    return render(request,'dmac/login.html',{'df_aws':df_aws,'data':data,'data1':data1,'data2':data2,'data3':data3,'data4':data4,'df_aws2':df_aws2,'tablename_list':tablename_list})


def Table(request):
    todo = [
        {"id": "01", "name": "abhinav"},
        {"id": "02", "name": "ashish"},
        {"id": "03", "name": "ankit"},
        {"id": "04", "name": "suresh"}
    ]
    try:
        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # # df1.to_sql('dmac', engine, if_exists='append')
        l1 = pd.read_sql_query('select * from "legacytable1"', con=engine)
        l2 = pd.read_sql_query('select * from "legacytable1"', con=engine)
        l3 = pd.read_sql_query('select * from "legacytable1"', con=engine)
        # Manipulate DataFrame using to_html() function
        table1 = l1.to_html()
        table2 = l2.to_html()
        table3 = l3.to_html()
    except:
        l1=pd.DataFrame(todo)
        table1 = l1.to_html()


    return HttpResponse(table1)


def merge_table(request):
    try:
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
    except:
        tablex="now you are not connected to database."


    return HttpResponse(tablex)


def finaljson(request):
    try:
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
        return render(request, 'dmac/product.html', {'tablex': tablex, 'fitdata': fitdata})
    except:
        mergedata1 = [
            {"id": "03", "name": "ankit"},
            {"id": "03", "address": "yyyy"},
            {"id": "02", "phone": "3434343"},
            {"id": "03", "phone": "23344"},
            {"id": "01", "address": "rrrr"},
        ]

        # tablex = final.to_json(orient='records')
        # code for reshape json and remove redundancy
        plusdata = mergedata1
        print(plusdata)
        plusdata.sort(key=lambda item: item.get("id"))
        print(plusdata)
        for i in range(len(plusdata) - 1):
            if (plusdata[i]["id"] == plusdata[i + 1]["id"]):
                plusdata[i].update(plusdata[i + 1])

        for i in range(len(plusdata) - 1):
            if (plusdata[i]["id"] == plusdata[i + 1]["id"]):
                plusdata[i].update(plusdata[i + 1])
                plusdata[i + 1].update(plusdata[i])
        fitdata = list(unique_everseen(plusdata, key=lambda item: frozenset(item.items())))
        print(fitdata)
        return render(request, 'dmac/product.html', {'fitdata': fitdata})


def posttable(request):
    return render(request,'dmac/posttable.html')

# @api_view(["POST"])
def postdata(request):
    try:
        if request.method == "POST":
            table_name = request.POST.get('table_name')
            # table_name = json.loads(table_name.body)
        print(table_name)
        table="your selected table:"+" "+table_name
        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # l3.to_sql('legacytable3', engine,  if_exists='append')
        l1 = pd.read_sql_query(f'select * from {table_name}', con=engine)
        data1 = l1.to_json(orient='records')

        return render(request,'dmac/posttable.html',{'table':table,'data1':data1})
        # return redirect('dmac:posttable')
    except:
        table_name = json.loads(request.body)
        print(table_name)
        table = "your selected table:" + " " + table_name
        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # l3.to_sql('legacytable3', engine,  if_exists='append')
        l1 = pd.read_sql_query(f'select * from {table_name}', con=engine)
        data1 = l1.to_json(orient='records')


        return JsonResponse("Ideal weight should be:" + data1, safe=False)


def concattable(request):
    return render(request,'dmac/concat.html')

# @api_view(["POST"])
def concatdata(request):
    try:
        if request.method == "POST":
            table1 = request.POST.get('table_name1')
            table2 = request.POST.get('table_name2')
            print(table1)
            print(table2)

        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # l3.to_sql('legacytable3', engine,  if_exists='append')
        l1 = pd.read_sql_query(f'select * from {table1}', con=engine)
        l2 = pd.read_sql_query(f'select * from {table2}', con=engine)
        merg1 = pd.merge(l1, l2, how="outer")
        concat = merg1.to_json(orient='records')
        # merg1["Full Name"] = merg1["First Name"] + "  " + merg1["Last Name"]

        return render(request,'dmac/concat.html',{'merg1':merg1,'concat':concat})
    except:
        table_name = json.loads(request.body)
        # table_name=pd.read_csv(request.body)
        print(table_name)

        #
        # engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # # l3.to_sql('legacytable3', engine,  if_exists='append')
        # l1 = pd.read_sql_query(f'select * from {table_name}', con=engine)
        # data1 = l1.to_json(orient='records')

        # return JsonResponse("Ideal weight should be:" + data1, safe=False)
        return JsonResponse(table_name, safe=False)



@csrf_exempt
def article_list(request):

    if request.method == 'GET':
        articles = Lead.objects.all()
        serializer =LeadSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        s1=data["table1"]
        s2=data["table2"]
        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # l3.to_sql('legacytable3', engine,  if_exists='append')
        l1 = pd.read_sql_query(f'select * from {s1}', con=engine)
        l2 = pd.read_sql_query(f'select * from {s2}', con=engine)
        merg1 = pd.merge(l1, l2, how="outer")
        print(merg1)
        concat = merg1.to_json(orient='records')
        final=json.loads(concat)
        print(final)
        print(type(final))
        serializer = LeadSerializer(data=data)
        # print(serializer.data["table1"])
        # print(serializer.data["table2"])

        # if serializer.is_valid():
        #     serializer.save()
        # return concat
        return JsonResponse(final, safe=False)
        # return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def tab_details(request):
        data = JSONParser().parse(request)
        print(type(data))
        # s1=data["table1"]
        engine = create_engine('postgresql://postgres:Programming123@localhost:5432/postgres')
        # # l3.to_sql('legacytable3', engine,  if_exists='append')
        l1 = pd.read_sql_query(f'select * from {data}', con=engine)
        print(l1)
        # l2 = pd.read_sql_query(f'select * from {s2}', con=engine)
        # merg1 = pd.merge(l1, l2, how="outer")
        # print(merg1)
        concat = l1.to_json(orient='records')
        final=json.loads(concat)

        return JsonResponse(final, safe=False)
        # return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def jsonreducer(request):
    data = JSONParser().parse(request)
    print(data)
    plusdata = data
    print(plusdata)
    plusdata.sort(key=lambda item: item.get("id"))
    print(plusdata)
    for i in range(len(plusdata) - 1):
        if (plusdata[i]["id"] == plusdata[i + 1]["id"]):
            plusdata[i].update(plusdata[i + 1])

    for i in range(len(plusdata) - 1):
        if (plusdata[i]["id"] == plusdata[i + 1]["id"]):
            plusdata[i].update(plusdata[i + 1])
            plusdata[i + 1].update(plusdata[i])
    fitdata = list(unique_everseen(plusdata, key=lambda item: frozenset(item.items())))

    # concat = l1.to_json(orient='records')
    # final = json.loads(concat)

    return JsonResponse(fitdata, safe=False)
    # return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def save_json_to_table(request):
    data = JSONParser().parse(request)
    # data = request.data
    mdata=pd.DataFrame(data)
    print(mdata)
    print(data)


    concat = mdata.to_json(orient='records')
    final = json.loads(concat)

    return JsonResponse(final, safe=False)
    # return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def twotables(request):
    # table_name = JSONParser().parse(request)
    table_name = json.loads(request.body)
    colfunctionlist=[]
    mainvalues=[]
    maincolumns=[]
    engine = create_engine('postgresql://postgres:Programming1234@localhost:5432/postgres')

    for i in range(len(table_name)):
        l1 = pd.read_sql_query(f'select * from {table_name[i]}', con=engine)
        mkt = l1.iloc[0:, 1:]
        dataft = mkt.to_json(orient='records')
        # print(dataft)


        s1 = json.loads(dataft)
        colfunctionlist.append(s1)
        # valuess1 = [list(x.values()) for x in s1]
        # # d_cities = dict.fromkeys(cities, 'UK')
        # mainvalues.append(valuess1)
        # columnss1 = [list(x.keys()) for x in s1][0]
        # maincolumns.append(columnss1)


        # concat = maincolumns.to_json(orient='records')
        # final = json.loads(maincolumns)

    return JsonResponse(colfunctionlist, safe=False)
    # return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def connections(request):
    if request.method == "POST":
        host = request.POST.get("host")

        username = request.POST.get('username')
        password = request.POST.get('password')
        database = request.POST.get('database')

    #     print(host)
    # # print(data)
    # print(username)
    # print(password)
    # print(database)
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password)
        strl="connection successful....."


        return JsonResponse(strl, safe=False)
    except:
        strl="connection failed.Check your credentials."
        return JsonResponse(strl, safe=False)





def table_names(request):
    global engine
    engine = create_engine('postgresql://postgres:Programming1234@localhost:5432/postgres')
    df_aws2 = pd.read_sql_query("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';",
                                con=engine)
    tablename_list = list(df_aws2["relname"])
    concat = df_aws2.to_json(orient='records')
    final = json.loads(concat)


    return JsonResponse(final, safe=False)
    # return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def display_singletable(request):

    if request.method == "POST":
        table = request.POST.get("table")
        engine = create_engine('postgresql://postgres:Programming1234@localhost:5432/postgres')
        l1 = pd.read_sql_query(f'select * from {table}', con=engine)
        mkt = l1.iloc[0:, 1:]
        dataft = mkt.to_json(orient='records')
        final = json.loads(dataft)

    return JsonResponse(final, safe=False)
    # return JsonResponse(serializer.errors, status=400)

def tables(request):
    return render(request,'dmac/table.html')

@csrf_exempt
def thankyou(request):
    if request.method == "POST":
        tabl = request.POST.get('jsonData')
        rules = request.POST.getlist('rules')
        desc = request.POST.get('desc')
        fit = request.POST.get('fit')
        spliter = request.POST.get('spliter')
        concat = request.POST.get('concat')
        resizer = request.POST.get('resizer')

        # fit="NAME"
        print("json data")
        print(type(tabl))
        print(tabl)
        print(fit)
        print(rules)
        sit = json.loads(tabl)
        print("sit")
        print(sit)
        frame = pd.DataFrame(sit)
        frame = frame.iloc[0:, 1:]
        plusdata1 = frame.to_json(orient='records')
        plusdata2 = json.loads(plusdata1)
        # git = {'lispr':sit}
        # print(git)

        def del_none(d):
            """
            Delete keys with the value ``None`` in a dictionary, recursively.

            This alters the input so you may wish to ``copy`` the dict first.
            """
            # For Python 3, write `list(d.items())`; `d.items()` won’t work
            # For Python 2, write `d.items()`; `d.iteritems()` won’t work
            for key, value in list(d.items()):
                if value == "":
                    del d[key]
                elif isinstance(value, dict):
                    del_none(value)
            return d  # For convenience
        listdf = []
        for f in plusdata2:
            listdf.append(del_none(f.copy()))
            print(del_none(f.copy()))



            # def del_none(f):
            #     for key, value in list(f.items()):
            #         if value is None:
            #             del f[key]
            #         elif isinstance(value, dict):
            #             del_none(value)
            #         lift.append(f)
            # # return d
            #
            # del_none(f.copy())





        print(listdf)





        # print(frame)
        # print(frame.info)

        # print(plusdata)
        # tablu = JSONParser().parse('jsonData')
        # desc = request.POST.get('desc')
        # table_name = json.loads(table_name.body)
    # print(type(plusdata))
    plusdata = listdf
    plusdata.sort(key=lambda item: item.get(fit))
    # print(plusdata)


    for i in range(len(plusdata) - 1):
        if (plusdata[i][fit] == plusdata[i + 1][fit]):
                plusdata[i].update(plusdata[i + 1])

        for i in range(len(plusdata) - 1):
            if (plusdata[i][fit] == plusdata[i + 1][fit]):
                plusdata[i].update(plusdata[i + 1])
                plusdata[i + 1].update(plusdata[i])
        fitdata = list(unique_everseen(plusdata, key=lambda item: frozenset(item.items())))
        # print(fitdata)
        l1 = pd.DataFrame(fitdata)

        # def stringify(x):
        #     fd = x[0:10]
        #     return fd
        #
        # l1["finalname"] = l1["NAME"].apply(stringify)
        #
        # print(l1)

        if spliter!=None:
            def string_split(x):
                fd = x.split(" ")
                return fd[0]

            l1["first_name"] = l1["NAME"].apply(string_split)

            def string_last(x):
                try:
                    fd = x.split(" ")
                    return fd[1]
                except:
                    pass

            l1["last_name"] = l1["NAME"].apply(string_last)

        if resizer != None:
            def digit_tracker(x):
                d = str(x)
                k = len(d)
                if k <= 8:
                    spd = "0" * (8 - k) + d
                    return spd
                else:
                    spd = d[0:8]
                    return spd

            l1['updated phone'] = l1['PHONE'].apply(digit_tracker)
        if concat !=None:
            l1["complete address"] = l1["ADDRESS 1"]+" "+l1["ADDRESS 2"]

        # l1.to_sql(desc, engine, if_exists='append')
        table1 = l1.to_html()
        kirs = l1.to_json(orient='records')
        # colfunctionlist.append(dataft)
        sk = json.loads(kirs)
        val_1 = [list(x.values()) for x in sk]
        # d_cities = dict.fromkeys(cities, 'UK')
        col_1 = [list(x.keys()) for x in sk][0]



    # print(rules[0])

    # return HttpResponse(table1)
        # concat = l1.to_json(orient='records')
        # final = json.loads(concat)
    return JsonResponse(sk, safe=False)
    # return render(request,'dmac/login-2.html',{'val_1':val_1,'col_1':col_1})



@csrf_exempt
def twotables_detail(request):
    # table_name = JSONParser().parse(request)
    # table_name = json.loads(request.body)
    table1 = request.POST.get('table1')
    table2 = request.POST.get('table2')
    table_name=[table1,table2]
    colfunctionlist=[]
    mainvalues=[]
    maincolumns=[]
    engine = create_engine('postgresql://postgres:Programming1234@localhost:5432/postgres')

    for i in range(len(table_name)):
        l1 = pd.read_sql_query(f'select * from {table_name[i]}', con=engine)
        mkt = l1.iloc[0:, 1:]
        dataft = mkt.to_json(orient='records')
        # print(dataft)


        s1 = json.loads(dataft)
        colfunctionlist.append(s1)
        # valuess1 = [list(x.values()) for x in s1]
        # # d_cities = dict.fromkeys(cities, 'UK')
        # mainvalues.append(valuess1)
        # columnss1 = [list(x.keys()) for x in s1][0]
        # maincolumns.append(columnss1)


        # concat = maincolumns.to_json(orient='records')
        # final = json.loads(maincolumns)

    return JsonResponse(colfunctionlist, safe=False)
    # return JsonResponse(serializer.errors, status=400)


