from django.shortcuts import get_object_or_404, render, redirect
from .models import Data
from django.http import HttpResponse
from .forms import PostForm
from .forms import SearchForm
from django.utils import timezone
import requests
import json
from .kmp import *

def index(request):
    return render(request, 'ChainLicense/index.html')

# 아래에 블록체인 api 입력 및 로직 구현합니다.
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()

            headers = {
                'Content-type': 'application/json',
            }
            data = {"data" : post.contents}
            data = json.dumps(data)
            response = requests.post('http://localhost:3001/mineBlock', headers=headers, data=data)
            
            post.save()
            return redirect('post_detail', seq=post.seq)
    else:
        form = PostForm()
    return render(request, 'ChainLicense/post_edit.html', {'form': form})

def post_detail(request, seq):
    #data = get_object_or_404(Data, seq=seq)
    response = requests.get('http://localhost:3001/blocks').json()
    for i in response:
        if i.get('data') == seq:
            data = i
        else:
            data = "Not Found"
    return render(request, 'ChainLicense/post_detail.html', {'data': data})

def post_compare(request):
    response = requests.get('http://localhost:3001/blocks').json()
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            print(search.contents)
            for i in response:
                #print(i.get('data'))
                result_temp = KMPSearch(search.contents,i.get('data'))
                if result_temp is not None:
                    print(i)
                    return render(request, 'ChainLicense/post_list.html', i)

            #datas = Data.objects.filter(name=search.contents, author=search.author)
            #return render(request, 'ChainLicense/post_list.html', result_temp_lists)

    form = PostForm()
    return render(request, 'ChainLicense/post_compare.html', {'form': form})

def post_list(request):
    #datas = Data.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    response = requests.get('http://localhost:3001/blocks').json()
    return render(request, 'ChainLicense/post_list.html', {'datas': response})