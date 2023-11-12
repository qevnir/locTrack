from django.shortcuts import render
from django.http import FileResponse, JsonResponse, HttpResponse
from django.conf import settings
from django.core.serializers import serialize
from .models import TrackPoint, Location, Category
from collections import defaultdict
from django.contrib.gis.geos import Polygon
import json

import gpxpy
import os

from django.template import loader


def trackpoints(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    trackpoints = TrackPoint.objects.filter(timestamp__range=[start,end])
    trackpoints_serialized = serialize('geojson', trackpoints, geometry_field='point',fields=('timestamp',))

    return JsonResponse(trackpoints_serialized, safe=False)

def import_data_gpx(request):

    for key in request.FILES:

        print(request.FILES[key])
        file_name = request.FILES[key]
        gpx = gpxpy.parse(file_name)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    print('Point at ({0},{1}) -> {2} at time {3}'
                          .format(point.latitude, point.latitude, point.elevation, point.time))

                    TrackPoint.objects.create_trackpoint(point)

    return HttpResponse(status=200)

def new_location(request):
    # TODO: validation of input
    # TODO: exception on record creation
    
    req_json = json.loads(request.body)

    coords = json.loads(request.body)['polygon']['geometry']['coordinates'][0]
    coords.append(coords[0])
    print(req_json['categoryID'])
    category_object = Category.objects.get(id=int(req_json['categoryID']))

    location = Location(name=req_json['name'],
                 category=category_object,
                 time_until_visited=int(req_json['timeUntilVisited']),
                 color=req_json['color'],
                 polygon=Polygon(coords))

    location.save()
                                             
    return HttpResponse(status=200)



def all_locations(request):
    locations = Location.objects.all()
    locations_serialized = serialize('geojson', locations ,geometry_field='polygon',fields=('pk','name','color'))
    return JsonResponse(locations_serialized, safe=False)


def all_categories(request):
    
    categories = Category.objects.all() 
    categories_serialized = serialize('json', categories, fields=('pk', 'name','color','parent'))
  
    return JsonResponse(categories_serialized, safe=False)
    
def child_categories(request):
    category_id = request.GET.get('categoryID')
    categories = Category.objects.filter(parent=category_id)
    categories_serialized = serialize('json', categories, fields=('pk', 'name','color', 'parent'))

    return JsonResponse(categories_serialized, safe=False)

def new_category(request):
    req_json = json.loads(request.body)
    if req_json['parent'] != None:
        parent_object = Category.objects.get(id=int(req_json['parent']))
        new_category = Category(name=req_json['name'],
                                color=req_json['color'],
                                parent=parent_object)
    else:
        new_category = Category(name=req_json['name'],
                                color=req_json['color'])

    new_category.save()
    return HttpResponse(status=200)

def remove_category(request):
    category_id = json.loads(request.body)['categoryID']
    print(category_id)
    category = Category.objects.get(pk=category_id)
    category.delete()

    return HttpResponse(status=200)
