# files/views.py

from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .serializers import FileListSerializer, FileDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import messages
from rest_framework import status
from django.conf import settings
from users.models import User
from .forms import FileForm
from .models import File
import jwt
import os

# Create your views here.

@api_view(['GET']) # to only accept HTTP GET method
def token_verification(request):
    userToken = request.headers['Authorization'].replace('Bearer ', '')
    data = jwt.decode(userToken, settings.SECRET_KEY, algorithms=["HS256"])
    userInstance = User.objects.get(id=data['user_id'])
    greet = 'Brother ' if (userInstance.genre == 'mal') else 'Sister '
    userInfos = {
        'name': greet + userInstance.username,
        # 'mail': userInstance.email,
        # 'joinAt': userInstance.date_joined,
        # 'role': 'admin' if userInstance.is_superuser else 'user'
    }
    return Response({'name': userInfos.get('name')}, status=status.HTTP_200_OK)


# N.B.: With API view, all HTTP methods related to RESTfull API should be manually definded so as to work properly
class FileAPIView(APIView):
    # To access this API view, requesters should authenticate themselves using JWT Token
    authentication_classes = [JWTAuthentication] # authentication method to use so as to access the API view
    permission_classes = [IsAuthenticated] # permission needed to access the API view

    # defining get method process
    def get(self, request, *args, **kwargs):
        # extracting the authenticated user from request
        user = request.user
        try:
            getParams = request.GET
            # search parameter is used to filter filenames
            searchParam = None
            if ('search' in getParams) and (len(getParams) == 1):
                searchParam = getParams.get('search').lower()
            # when none params is provided in the request, we proceed as normal
            if not (searchParam or getParams) :
                possibleParameter = self.kwargs.get('file_id')
                if not possibleParameter:
                    # getting all File objects stored in database
                    files = File.objects.filter(uploader=user)
                    # passing that bunch of data to our serializer, many=True specify that a list will be passed
                    serializer = FileListSerializer(files, many=True)
                else:
                    # getting all File objects stored in database
                    file = File.objects.get(idToInteger=possibleParameter)
                    if file.uploader != user:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
                    # passing that bunch of data to our serializer, many=True specify that a list will be passed
                    # i don't know here, but when deleting many=True, i got an empty list as result
                    serializer = FileDetailSerializer(file)
                # returning the processing result of either FileListSerializer or FileDetailSerializer over that bunch of data
                return Response(serializer.data, status=status.HTTP_200_OK) 
            else:
                # for search parameter's presence, i filter according to filename
                serializer = FileListSerializer(File.objects.filter(uploader=user), many=True)
                data = list(filter(lambda file: searchParam in file['document'].lower(), serializer.data))
                return Response(data, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # defining post method process
    def post(self, request, *args, **kwargs):
        # try:
            # extracting some variables from the incoming request : the method POST, the in transit FILES and the connected USER
            post = request.POST # the method POST
            files = request.FILES # the in transit FILES
            user = request.user # the connected USER
            # looking over each key in files [files is a MultiValueDict]
            fileTags = list(files.keys())
            for tag in fileTags:
                # for each key field found in files, we retrieve all values associated using getlist() [considering the case where multiple files are sent]
                for file in files.getlist(tag):
                    # using a form to nicely handle upload entity registration according to connected user
                    form = FileForm(post, {'document': file})
                    # saving the model instance without pushing it into the databse
                    file_instance = form.save(commit=False)
                    # setting the uploader
                    file_instance.uploader = user
                    # saving the model instance into the database
                    file_instance.save()
                return Response(status=status.HTTP_201_CREATED)
        # except:
        #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # defining delete method process
    def delete(self, request, file_id):
        # trying to get the file associated to the given file_id
        try:
            fileRequested = File.objects.get(idToInteger=file_id)
            # if uploader of this file doesn't match the current authenticated user, i send a 401 status code to client
            if fileRequested.uploader != request.user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            # after that, i remove the file from media folder
            # os.remove(settings.MEDIA_ROOT / fileRequested.document.name) # for media storage
            fileRequested.document.delete()
        except FileNotFoundError:
            pass
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # and finally, i remove the object referenced
        fileRequested.delete()
        # now, deletion is successfull
        return Response(status=status.HTTP_200_OK)


# for a particular user, this function retrieves the names of all files been uploaded
def one_user_files(userInstance) :
    # first, we get all files uploaded by the user 
    userFiles = File.objects.filter(uploader=userInstance)
    # for each file, we retrieve the corresponding name
    # to be fast i use [map(function, iterable)] method in python
    retrieveFilename = lambda currentFile : currentFile.document.name.split('/')[-1] # the function defined
    files = list(map(retrieveFilename, userFiles)) # using map to get extract the name from current user uploaded files
    # returning files
    return files


# this view handles our custorm form defined in files/forms.py
def upload_form_view(request):
    # user should be authenticated before submitting anything inside the form
    if request.user.is_authenticated:
        # POST request will particularly holds our attention for user/form data processing
        if request.method == 'POST':
            # document is the name field bound to input file in the form
            # we got the file upload by the user
            files = request.FILES.getlist('document')
            for file in files :
                # we filled the form with data coming from POST and the file being uploaded
                # by default, django applied get(<name>) to the second argument to retrieve the file
                # that's why i use a [dictionary {<name>: <file>}] here
                form = FileForm(request.POST, {'document': file})
                # as soon as the form has been validated, we process the form data and save the model instance
                if form.is_valid():
                    # saving the model instance without pushing it into the database
                    file_instance = form.save(commit=False)
                    # setting the uploader
                    file_instance.uploader = request.user
                    # saving the model instance into the database
                    file_instance.save()
                    # making the user aware of the success of his or her upload by creating a success message
                    messages.success(request, f"{form.cleaned_data['document']} has been uploaded successfully!")
                    # re-emptying 😅 the form
                    form = FileForm()
        else:
            # creating a new empty form
            form = FileForm()
        
        # then, we set the context variable
        context = {'form': form, 'files': one_user_files(request.user)}
        # passing the context to the template and redering it
        return render(request, 'file.html', context=context)
    else:
        # in case the user is not authenticated, we warn him or her about that
        messages.warning(request, 'You should better log in at /login before pursuing.')
        # then we redirect him or her to the login page
        # here, i just use login logic provided by admin endpoint
        return redirect('login')
