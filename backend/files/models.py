# files/models.py

from django.conf import settings
from string import punctuation
from users.models import User
from django.db import models
import datetime
import uuid
import os

# Create your models here.


def generate_unique_filename(instance, filename):
    # extracting submitted user file name and extension by replacing every space ' ' by undescore '_'
    file_name, file_extension = os.path.splitext(filename.replace(' ', '_'))
    # for security purpose, i get ride of any special character present in file_name and replace all spaces with underscore
    safeParse = lambda x: x not in punctuation+'\t'
    file_name = ''.join(list(filter(safeParse, file_name)))
    # current timestamp will be added to fileName for uniqueness
    currentTimestamp = str(datetime.datetime.now().timestamp()).replace('.', '')
    # here, we get ride of any mark (.) because datetime.datetime.now() is a floatting number
    if file_extension :
        # adding extension to fileName
        fileName = f"{file_name}_{currentTimestamp}{file_extension}"
    else :
        # empty extension are replacing by .data
        fileName = f"{file_name}_{currentTimestamp}.data"
    # each user file will be stored in a particular folder, that folder is his/her id converted back to integer
    folderName = int(instance.uploader_id)
    # before returning, let's modify idToInteger field of file_instance
    instance.idToInteger = int(str(instance.id).replace('-', ''), 16) # what i do is just converting back the uuid field (instance.id) to integer
    # returning where to upload the in-proccess user file
    return f"{folderName}/{fileName}"


class File(models.Model):
    # instead of using default integer incremental, i use UUID one to set up id field for better security 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    # then, keeping in mind the horodatage (date and time) when upload has been done via upload_dateinfos
    upload_dateinfos = models.DateTimeField(auto_now_add=True)
    # to keep track of the one behind that upload, i set up uploader field
    uploader = models.ForeignKey(User, null=True, to_field='id', on_delete=models.CASCADE, related_name='uploader')
    # finaaly come, the uploaded file store in document field
    document = models.FileField(upload_to=generate_unique_filename, default=None)
    # this field is just the id field converting back to integer
    idToInteger = models.CharField(max_length=64, default=0, unique=True)
    # i use CharField instead of BigIntegerField because BigInteger won't support it as it is very large integer

    class Meta:
        ordering = ['-upload_dateinfos'] # this will order files in our database from latest upload_dateinfos to oldest

