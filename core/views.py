from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import requests

def home(request):
    if request.method == "POST":
        if request.POST.get("problems") == 'problems':
            tag = request.POST['tag']
            return redirect("problems",tag,1)
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

def problems(request,id,tag):
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
    if request.method == "POST":
        if request.POST.get("next") == 'next':
            id=id+1
            return redirect("problems",tag,id)
        elif request.POST.get("prev") == 'prev':
            if id>1:
                id=id-1
            else:
                pass
            return redirect("problems",tag,id)
        elif request.POST.get("home") == 'home':
            return redirect("home")
    Pages=int(len(tmp)/10)+1
    return render(request,"main/problems.html",{"problems":data1,"id":id,"Prev":Prev,"Next":Next,"tag":tag,"Pages":Pages})


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