from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Meme
from . import serializers
from datetime import date
import datetime
import re
from ural import ensure_protocol, is_url

# MemeViewSet class contains views that map to endpoints for assessment


class MemeViewSet(viewsets.ViewSet):
    # permission class is set to allow any user
    permission_classes = [AllowAny, ]
    # initially serializer class is set to default  EmptySerializer
    serializer_class = serializers.EmptySerializer

    # dictionary to map each view to its corresponding serializer class
    serializer_classes = {
        'list': serializers.MemeSerializer,
        'partial_update': serializers.MemeUpdateSerializer,
        'create': serializers.MemeSerializer,
        'retrieve': serializers.MemeSerializer
    }
    queryset = ''

    # django viewsets by default maps list view to get method to fetch collection of existing resources
    def list(self, request):
        """selects only the fields required from latest 100 records required
        reduces response time if data present is large
        orders in ascending order of creation time"""
        queryset = Meme.objects.values(
            'id', 'name', 'url', 'caption').order_by('creationDateTime')[:100]

        # maps all objects received to serializer class to get list of json objects
        serializer = serializers.MemeSerializer(queryset, many=True)

        # sends list of json objects as response
        return Response(serializer.data,status=status.HTTP_200_OK)

    # django viewsets by default maps create view to post method to create a new resource

    def create(self, request):

        #checks if url field is blank
        if request.data.get('url') == None:
            return Response({"message": "URL field cannot be blank"}, status=status.HTTP_400_BAD_REQUEST)

        #proccesses a malformed url,rejects values that do not form valid url
        schemed_url = ensure_protocol(
            request.data.get('url'), protocol='https')
        if is_url(schemed_url) == False:
            return Response({"message": "Enter a valid url"}, status=status.HTTP_400_BAD_REQUEST)

        #checks if name input contains only letters,numbers,underscore and hyphen
        pattern = "^[A-Za-z0-9_-]*$"
        name=request.data.get('name')
        if name is not None and bool(re.match(pattern, name)) == False:
            return Response({"message": "Name can contain only letters,numbers,underscore and hyphen"}, status=status.HTTP_400_BAD_REQUEST)

        # maps request data to serializer class to get an object
        serializer = serializers.MemeSerializer(data={"name": request.data.get(
            'name'), "url": schemed_url, "caption": request.data.get("caption")})

        # checks validity of the serializer object whether all required fields are present
        if serializer.is_valid():

            # extract the various parameters sent in request data
            creator = serializer.data.get('name')
            caption = serializer.data.get('caption')
            url = serializer.data.get('url')

            # set creationDateTime,creationDate,lastUpdate as current date and time
            creationDateTime = timezone.now()
            creationDate = date.today()
            updatedDateTime = timezone.now()

            # create a meme object with data extracted
            obj = Meme(caption=caption, url=schemed_url, name=creator, creationDateTime=creationDateTime,
                       creationDate=creationDate, lastUpdate=updatedDateTime)

            # check if meme object  already exists
            query_obj2 = Meme.objects.filter(url=schemed_url).filter(
                name=creator).filter(caption=caption)
            if len(query_obj2) >= 1:
                return Response({'message': 'This meme already exists'}, status=status.HTTP_409_CONFLICT)

            # if meme object does not exit create a new meme by saving it to database
            obj.save()
            # get the id of the meme object created
            postCounter = obj.id
            # return the id of the meme object created with accepted status code
            return Response({'id': str(postCounter)}, status=status.HTTP_201_CREATED)
        else:
            """if any required data was missing or if serializer object could
            not be created,return the exact serialization error that occured
            with bad request status code"""
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # django viewsets by default maps retrieve view to get method to get an existing resource by its id

    def retrieve(self, request, pk=None):
        #if id input is anything other than positive integer,return status bad request
        try:
            val = int(pk)
        except ValueError:
            return Response({"message": "Enter positive number"}, status=status.HTTP_400_BAD_REQUEST)
        
        #if id input is negative integer,return status bad request
        if int(pk) < 0:
            return Response({"message": "Enter positive number"}, status=status.HTTP_400_BAD_REQUEST)
        # get meme object by its id
        queryset = Meme.objects.filter(id=pk)
        # map the meme object to serializer class to get list of json fields
        serializer = serializers.MemeSerializer(queryset, many=True)

        """check if meme object exists,return json fields if it exists
        otherwise return http status, not found"""
        if len(queryset) == 1:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """django viewsets by default maps partial_update view to patch method to update 
    some fields of an existing resource after retrieving it by its id"""

    def partial_update(self, request, pk=None):
        #if id input is anything other than positive integer,return status bad request
        try:
            val = int(pk)
        except ValueError:
            return Response({"message": "Enter positive number"}, status=status.HTTP_400_BAD_REQUEST)
        
        #if id input is negative integer,return status bad request
        if int(pk) < 0:
            return Response({"message": "Enter positive number"}, status=status.HTTP_400_BAD_REQUEST)
        # get meme object by its id
        queryset = Meme.objects.filter(id=pk)

        # check if meme object exists,if it does not return http status not found
        if len(queryset) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data.get('name') != None:
            return Response({"message": "Creator name cannot be changed!!"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('url') == None and request.data.get('caption') == None:
            return Response({"message": "Both url and caption cannot be none"}, status=status.HTTP_400_BAD_REQUEST)

        url = request.data.get('url')
        caption = request.data.get('caption')

        # if only caption is supplied,only caption is updated
        if url == None and caption != None:
            obj = queryset[0]
            obj.caption = caption
            obj.lastUpdate = timezone.now()
            obj.save()
            # return response no content if successfully updated
            return Response(status=status.HTTP_204_NO_CONTENT)

        # if url entered has no scheme,add scheme to url and check if a valid url is formed
        schemed_url = ensure_protocol(
            request.data.get('url'), protocol='https')
        if is_url(schemed_url) == False:
            return Response({"message": "Enter a valid url"}, status=status.HTTP_400_BAD_REQUEST)

        # if meme with that id exists,map request data to serializer to extract attributes based on data supplied
        # ie either url or caption or both
        if url != None and caption != None:
            serializer = serializers.MemeUpdateSerializer(
                data={"url": schemed_url, "caption": request.data.get("caption")}, partial=True)
        else:
            serializer = serializers.MemeUpdateSerializer(
                data={"url": schemed_url}, partial=True)

        # check if serializer object is valid i.e all required fields are present and no extra fields are present
        if serializer.is_valid():
            obj = queryset[0]

            # extract the caption and url of the meme object
            oldCaption = obj.caption
            oldUrl = obj.url

            # set caption and url sent as request to new caption and new url
            newCaption = serializer.data.get('caption')
            newUrl = serializer.data.get('url')

            # check if new caption is not same as existing caption.If not then update caption field of meme object.
            if newCaption is not None and newCaption != oldCaption:
                obj.caption = newCaption
            # check if new url is not same as existing url.If not then update url field of meme object.
            if newUrl is not None and newUrl != oldUrl:
                obj.url = newUrl
            # if any of the fields were updated,set lastUpdate field of the object to current date and time
            if newUrl != oldUrl or newCaption != oldCaption:
                obj.lastUpdate = timezone.now()

            # save the meme object
            obj.save()
            # return response no content if successfully updated
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # to get serializer classes mapped to each view in the dictionary

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


# MemeViewSet class contains views that map to endpoints for custom views

class MemeFilterViewSet(viewsets.GenericViewSet):
    # permission class is set to allow any user
    permission_classes = [AllowAny, ]
    # initially serializer class is set to default  EmptySerializer
    serializer_class = serializers.EmptySerializer

    # dictionary to map each view to its corresponding serializer class
    serializer_classes = {
        'byName': serializers.MemeSerializer1,
        'byDateRange': serializers.MemeSerializer1
    }

    queryset = ''

    # to get all memes within a date range

    @action(methods=['post'], detail=False)
    def byDateRange(self, request):

        # get request data i.e start date and end date
        startDate = request.data.get('startDate')
        endDate = request.data.get('endDate')
        # if start date is greater than end date return status bad request
        if startDate > endDate:
            return Response({"message": "End date cannot be greater than start date"}, status=status.HTTP_400_BAD_REQUEST)

        # if start date is greater is equal to end date filter query by start date
        # else filter by creationDate in range
        if startDate == endDate:
            queryset = Meme.objects.filter(
                creationDate=startDate).order_by('-creationDateTime')[:100]
        else:
            queryset = Meme.objects.filter(
                creationDate__range=[startDate, endDate]).order_by('-creationDateTime')[:100]

        # map meme objects received from query to serializer to get list of json objects
        serializer = serializers.MemeSerializer1(queryset, many=True)

        # if no meme object was found by querying,return status not found else return serialized data
        if len(queryset) >= 1:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # to get all memes created by a particular person

    @action(methods=['post'], detail=False)
    def byName(self, request):
        # get request data i.e creator name
        creator = request.data.get('name')

        # filter memes by creator name
        queryset = Meme.objects.filter(
            name=creator).order_by('-creationDateTime')[:100]

        # map meme objects to serialzer to get list of json objects
        serializer = serializers.MemeSerializer1(queryset, many=True)

        # if no memes are found with creator name return status not found, else return serialized data
        if len(queryset) >= 1:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # to get latest 100 memes in descending order of their time of creation

    @action(methods=['get'], detail=False)
    def getAllMemes(self, request):
        """selects only the fields required from latest 100 records required and orders them in decreasing order
        of time of creation.Reduces response time if data present is large
        orders in ascending order of creation time"""
        queryset = Meme.objects.values(
            'id', 'name', 'url', 'caption', 'creationDateTime', 'lastUpdate').order_by('-creationDateTime')[:100]

        # maps all objects received to serializer class to get list of json objects
        serializer = serializers.MemeSerializer1(queryset, many=True)

        # sends list of json objects as response
        if len(queryset) >= 1:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # to create a meme
    @action(methods=['post'], detail=False)
    def createMeme(self, request):
        serializer = serializers.MemeSerializer1(data=request.data)
        if serializer.is_valid():
            creator = serializer.data.get('name')
            caption = serializer.data.get('caption')
            url = serializer.data.get('url')
            creationDateTime = timezone.now()
            creationDate = date.today()
            updatedDateTime = timezone.now()
            obj = Meme(caption=caption, url=url, name=creator, creationDateTime=creationDateTime,
                       creationDate=creationDate, lastUpdate=updatedDateTime)
            # check if it already exists
            query_obj2 = Meme.objects.filter(url=url).filter(
                name=creator).filter(caption=caption)
            if len(query_obj2) >= 1:
                return Response({'message': 'This meme already exists'}, status=status.HTTP_409_CONFLICT)
            obj.save()
            postCounter = obj.id
            return Response({'id': str(postCounter)}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # to get a meme by its id
    @action(methods=['get'], detail=True)
    def getMeme(self, request, pk=None):
        # get meme object by its id
        queryset = Meme.objects.filter(id=pk)
        # map the meme object to serializer class to get list of json fields
        serializer = serializers.MemeSerializer1(queryset, many=True)

        """check if meme object exists,return json fields if it exists
        otherwise return http status, not found"""
        if len(queryset) == 1:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # to update some fields of an existing meme after retrieving it by its id
    @action(methods=['patch'], detail=True)
    def updateMeme(self, request, pk=None):
        queryset = Meme.objects.filter(id=pk)
        if len(queryset) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MemeUpdateSerializer(
            data=request.data, partial=True)
        if serializer.is_valid():
            obj = queryset[0]
            oldCaption = obj.caption
            oldUrl = obj.url
            newCaption = serializer.data.get('caption')
            newUrl = serializer.data.get('url')
            updatedDateTime = timezone.now()
            if newCaption is not None and newCaption != oldCaption:
                obj.caption = newCaption
                obj.lastUpdate = updatedDateTime
            if newUrl is not None and newUrl != oldUrl:
                obj.url = newUrl
                obj.lastUpdate = updatedDateTime
            obj.save()
            return Response({"data": serializer.data}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
