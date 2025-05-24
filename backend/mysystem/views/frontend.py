from django.shortcuts import render

#h5端页面
def h5web(request):
    return render(request,"h5/index.html")