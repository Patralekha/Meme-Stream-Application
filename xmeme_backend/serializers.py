from rest_framework import serializers
from .models import Meme
import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.forms import URLField

#EmptySerializer class
class EmptySerializer(serializers.Serializer):
    pass


#MemeSerializer and MemeUpdateSerializer are serializers for assessment url endpoints
class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ('id', 'name', 'url', 'caption')

#MemeUpdateSerializer used by partial_update view for editing a meme
class MemeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ('id', 'url', 'caption')


#MemeSerializer1 and MemeUpdateSerializer1 are custom serializers for publicly deployed endpoints used by frontend
#contain additional fields like creationDateTime,lastUpdate
class MemeSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ('id', 'name', 'url', 'caption',
                  'creationDateTime', 'lastUpdate')

#MemeUpdateSerializer1 used by partial_update view for editing a meme and recording date and time of edit
class MemeUpdateSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ('id', 'url', 'caption', 'creationDateTime', 'lastUpdate')
