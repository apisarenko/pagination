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
    paginator = Paginator(station_list, 10)
    page_number = request.GET.get('page')

    if page_number == None:
        page_number = 1
    page_object = paginator.get_page(page_number)

    if page_object.has_next() == True:
        next_page = reverse(viewname='bus_stations') + '?' \
                    + urllib.parse.urlencode({'page': (str(int(page_number) + 1))})
    else:
        next_page = ''

    if page_object.has_previous() == True:
        prev_page = reverse(viewname='bus_stations') + '?' \
                    + urllib.parse.urlencode({'page': (str(int(page_number) - 1))})
    else:
        prev_page = ''

    return render_to_response('index.html', context={
        'bus_stations': paginator.page(page_number),
        'current_page': page_number,
        'prev_page_url': prev_page,
        'next_page_url': next_page
    })
