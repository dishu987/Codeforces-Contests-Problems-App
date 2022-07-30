from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import requests

def home(request):
    if request.method == "POST":
        if request.POST.get("problems") == 'problems':
            tag = request.POST['tag']
            return redirect("problems",tag,1,"index","0")
        elif request.POST.get("contests") == 'contests':
            gym = request.POST.getlist("gym")
            # print(gym)
            url_str = " "
            if gym==['on']:
                url_str="gym=true"
            else:
                url_str="gym=false"
            return redirect("contests",1,url_str)
    return render(request,"main/home.html")
 
def problems(request,id,tag,sortby,reverse):
    Prev=False
    Next=False
    if tag=="all":
        data = requests.get('https://codeforces.com/api/problemset.problems').json()
    else:
        data = requests.get('https://codeforces.com/api/problemset.problems?tags='+tag).json()
    tmp=list()
    if data['status']=="FAILED":
        pass
    else:
        tmp=data['result']['problems']
    data1=list()
    if id==1:
        Prev=True
        Next=False
    elif id>int(len(tmp)/10):
        Next=True
        Prev=False
    count=0
    for d in tmp:
        if count<id*10 and count>=10*(id-1):
            data1.append(d)
        count=count+1
    if sortby=="index":
        if reverse=="1":
            data1.sort(key=lambda row:(row["index"]),reverse=True)
        else:
            data1.sort(key=lambda row:(row["index"]),reverse=False)
    elif sortby=="name":
        if reverse=='1':
            data1.sort(key=lambda row:(row["name"]),reverse=True)
        else:
            data1.sort(key=lambda row:(row["name"]),reverse=False)
    elif sortby=="tags":    
        if reverse=='1':
            data1.sort(key=lambda row:(len(row["tags"])),reverse=True)
        else:
            data1.sort(key=lambda row:(len(row["tags"])),reverse=False)
    if request.method == "POST":
        if request.POST.get("next") == 'next':
            id=id+1
            return redirect("problems",tag,id,sortby,reverse)
        elif request.POST.get("prev") == 'prev':
            if id>1:
                id=id-1
            else:
                pass
            return redirect("problems",tag,1,sortby,reverse)
        elif request.POST.get("home") == 'home':
            return redirect("home")
        elif request.POST.get("sorting") == 'sorting':
            decending = request.POST.getlist("decending")
            sort_by = request.POST.getlist("btnradio")
            # print(sort_by)
            # print(decending)
            if sort_by==["index"]:
                sortby="index"
                if decending==['on']:
                    reverse="1"
                    data1.sort(key=lambda row:(row["index"]),reverse=True)
                else:
                    reverse="0"
                    data1.sort(key=lambda row:(row["index"]),reverse=False)
            elif sort_by==["name"]:
                sortby="name"
                if decending==['on']:
                    reverse="1"
                    data1.sort(key=lambda row:(row["name"]),reverse=True)
                else:
                    reverse="0"
                    data1.sort(key=lambda row:(row["name"]),reverse=False)
            elif sort_by==["tags"]:  
                sortby="tags"  
                if decending==['on']:
                    reverse="1"
                    data1.sort(key=lambda row:(len(row["tags"])),reverse=True)
                else:
                    reverse="0"
                    data1.sort(key=lambda row:(len(row["tags"])),reverse=False)
            return redirect("problems",tag,id,sortby,reverse)
    Pages=int(len(tmp)/10)+1
    Context = {
        "problems":data1,
        "id":id,
        "Prev":Prev,
        "Next":Next,
        "tag":tag,
        "Pages":Pages,
        "reverse":reverse,
        "sortby":sortby,
    }
    return render(request,"main/problems.html",Context)


# Contests Page:
def contests(request,id,url_str):
    Prev=False
    Next=False
    data = requests.get('https://codeforces.com/api/contest.list?'+url_str).json()
    contest = list()
    if data['status'] == "FAILED":
        pass
    else:
        contest = data['result']
    data1 = list()
    if id==1:
        Prev=True
        Next=False
    elif id>int(len(contest)/10):
        Next=True
        Prev=False
    count=0
    Pages=int(len(contest)/10)+1
    for d in contest:
        if count<id*10 and count>=10*(id-1):
            data1.append(d)
        count=count+1
    if request.method == "POST":
        if request.POST.get("next") == 'next':
            id=id+1
            return redirect("contests",id,url_str)
        elif request.POST.get("prev") == 'prev':
            if id>1:
                id=id-1
            else:
                pass
            return redirect("contests",id,url_str)
        elif request.POST.get("home") == 'home':
            return redirect("home")
    return render(request,"main/contests.html",{"contests":data1,"id":id,"Prev":Prev,"Next":Next,"url_str":url_str,"Pages":Pages})

#Error404 Page
def error_404_view(request,exception):
    return render(request,"main/404_error.html")
 
def error_500_view(request):
    return render(request,"main/404_error.html") 