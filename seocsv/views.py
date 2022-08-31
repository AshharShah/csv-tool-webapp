from django.shortcuts import render
import urllib.request
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup

#from serpapi import GoogleSearch
import pandas as pd

# Create your views here.
from django.http import HttpResponse
from django.template import loader

@csrf_exempt
def index(request):
    template = loader.get_template('home.html')
    return render(request,'home.html')

@csrf_exempt
def output(request):
    print("posted")
    print(type(request.FILES['file']))
    file = pd.read_csv(request.FILES['file'])
    file = file.iloc[:, [0, 1]]
    # getting the keywords and values from out csv file
    keys = file.iloc[:, 0]
    values = file.iloc[:, 1]

    # displaying the dataframe
    print(file)

    # lists that will contain the required data that is to be appeneded to our dataframe
    totResults = []
    kgrs = []
    # lop to get data against each keyword in the dataframe
    for i in range(keys.shape[0]):
        keyToSearch = str(keys[i])
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
        URL     = "https://www.google.com/search?q=Allintitle:" + str(keyToSearch)
        result = requests.get(URL, headers=headers)    
        soup = BeautifulSoup(result.content, 'html.parser')
        total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False) # this will give you the outer text which is like 'About 1,410,000,000 results'
        results_num = ''.join([num for num in total_results_text if num.isdigit()]) # now will clean it up and remove all the characters that are not a number .
        print("Keyword: " + keyToSearch)
        print("Values: " + str(values[i]))
        print("Total Results: " +str(results_num))
        totResults.append(int(results_num))
        kgr = int(results_num)/values[i]
        print("KGR: " + str(kgr) + "\n\n")
        kgrs.append(round(float(kgr), 2))
    print("The List Of Results: ")
    print(totResults)
    print("The List Of KGRS: ")
    print(kgrs)
    # appending the required columns to our dataframe
    file["Allintitle (Google Search Results)"] = totResults
    file["KGR"] = kgrs
    # displaying the final dataframe
    print(file)
    print(file.to_html())
    return render(request,'output.html', {"df":file})