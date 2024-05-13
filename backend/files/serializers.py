# files/serializers.py

from rest_framework import serializers
from django.conf import settings
from .models import File

# custom model File serializer when the action is listing (a generic get request)
class FileListSerializer(serializers.ModelSerializer):
    # telling my serializer to consider the idToInteger field as id one and displaying it to user
    # in another word, i move idToInteger field to id field on my model
    id = serializers.CharField(source='idToInteger')

    # adding a new custom field to the serializer
    link = serializers.SerializerMethodField()
 
    # this function is helpful when it comes to modify how data will look like to users
    # here i just modify the formatting of document field
    def to_representation(self, instance):
        data = super().to_representation(instance)
        fileInProcess = data['document'].split('/')[-1].split('_')
        data['document'] = ''.join(fileInProcess[0:-1]) + '.' + fileInProcess[-1].split('.')[-1]
        return data

    class Meta:
        # using the custom File model
        model = File
        # only id and document fields will be displayed to users
        fields = ['id', 'document', 'upload_dateinfos', 'link']

    # thi is where i set the custom link variable
    def get_link(self, fileObject):
        return f"http://{settings.FTP_HOST}/{fileObject.document}"


# i do not really need FileDetailSerializer anymore
# i just use it here for testing my FileAPIView
# custom model File serializer when the action is detailing view (a parameterized get request)
class FileDetailSerializer(serializers.ModelSerializer):

    # same as previous
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['document'] = data['document'].split('/')[-1]
        return data

    class Meta:
        # using the custom File model
        model = File
        # only id, document  and upload_dateinfos fields will be displayed to users
        fields = ['document', 'upload_dateinfos']
