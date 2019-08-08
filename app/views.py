from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from app import settings
import csv
from django.core.paginator import Paginator
import urllib.request
import urllib.parse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    station_list = []
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for station in reader:
            station_dict = {}
            station_dict['Name'] = station['Name']
            station_dict['Street'] = station['Street']
            station_dict['District'] = station['District']
            station_list.append(station_dict)
    current_page = Paginator(station_list, 10)
    page_number = request.GET.get('page')
    page_number_1 = str(int(page_number) + 1)
    page_number_2 = str(int(page_number) - 1)

    params = urllib.parse.urlencode({'page': page_number_1})
    params_2 = urllib.parse.urlencode({'page': page_number_2})

    url = reverse(viewname='bus_stations') + '?' + params
    url_2 = reverse(viewname='bus_stations') + '?' + params_2

    if page_number == None or page_number == '1':
        page_number = 1
        prev_page = None
        next_page_url = url

    else:
        page_number = page_number
        prev_page = url_2
        next_page_url = url

    return render_to_response('index.html', context={
        'bus_stations': current_page.page(page_number),
        'current_page': page_number,
        'prev_page_url': prev_page,
        'next_page_url': next_page_url
    })
