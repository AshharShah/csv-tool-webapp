from django.shortcuts import render
import urllib.request
import json
from django.views.decorators.csrf import csrf_exempt

from serpapi import GoogleSearch
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
    # url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + request.POST['user_input']
    # response = urllib.request.urlopen(url)
    # result = json.loads(response.read())
    # context = {'word':result[0]['word'], 'meanings':result[0]['meanings']}
    # return render(request, 'output.html', context)
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
        print("Keyword: " + keyToSearch)
        print("Values: " + str(values[i]))
        params = {
            "q": keyToSearch,
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "output": "JSON",
            "api_key": "de33899a76f4499a591a33eab0383513a713a19c86c7e7f16685e829c2c49989"
        }
        # making a api call to search the provided paramater data
        search = GoogleSearch(params)
        dict_results = search.get_dict()
        # filtering the data to get the required variable that is the total number of searches
        d1 = dict_results["search_information"]
        d2 = d1["total_results"]
        print("Total Results: " + str(d2))
        totResults.append(int(d2))
        kgr = d2/values[i]
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