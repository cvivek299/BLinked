from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.contrib.auth.models import User as AuthUser
from blink.models import User, Education, School
from django.contrib import messages
from .forms import AddEducationForm, EditDetailsForm

"""
    Blockchain imports
"""
from werkzeug.utils import secure_filename
from django.core.files.storage import default_storage
import json
import hashlib
from .merkletools import MerkleTools
from .blockchain import Blockchain
from django.contrib.auth.decorators import login_required


def index(request, username):
    """
    Renders the user profile page

    :param request: request from client
    :param username: username of the profile page
    :return: user profile page
    """

    profileUser = None
    try:
        profileUser = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "username does not exists")
        return HttpResponseRedirect("/")

    degrees = Education.objects.filter(user=profileUser)

    template = loader.get_template('userprofile/index.html')
    context = {
        'page': 'profile',
        'user': request.user,
        'profileUser': profileUser,
        'degrees': degrees,
    }
    return HttpResponse(template.render(context, request))


@login_required
def addEducation(request):
    """
    Add Education

    :param request: request from client
    :return: add education page
    """

    user = request.user
    profileUser = User.objects.get(username=user.username)

    if request.method == 'POST':

        form = AddEducationForm(request.POST, request.FILES)

        if form.is_valid():
            schoolName = form.cleaned_data["schoolName"]
            degree = form.cleaned_data["degree"]
            fieldOfStudy = form.cleaned_data["fieldOfStudy"]
            startYear = form.cleaned_data["startYear"]
            endYear = form.cleaned_data["endYear"]
            additionalNotes = form.cleaned_data["additionalNotes"]

            try:
                school = School.objects.get(schoolName=schoolName)
            except School.DoesNotExist:
                messages.error(request, "school does not exists")
                return HttpResponseRedirect("#")

            jsonFile = request.FILES['json']
            if (jsonFile is None) or jsonFile.name == '':
                messages.error(request, "file error")
                return HttpResponseRedirect("#")

            jsonName = secure_filename(jsonFile.name)
            default_storage.save(jsonName, jsonFile)
            receiptJsonData = json.loads(default_storage.open(jsonName).read())

            print(jsonName)
            print(receiptJsonData)
            data = receiptJsonData['studentId'] + receiptJsonData['cpi'] + receiptJsonData['name'] + \
                   receiptJsonData['year'] + receiptJsonData['institution'] + receiptJsonData['degree']
            print(data)

            data = data.encode()
            data = hashlib.sha3_256(data).hexdigest()

            mt = MerkleTools(hash_type='sha3_256')
            print("proof" + mt.validate_proof(receiptJsonData['merklePath'], data))
            merkleRoot = mt.validate_proof(receiptJsonData['merklePath'], data)
            try:
                bc = Blockchain()
                res = bc.verifyBatchMerkleRoot(receiptJsonData["institution"], receiptJsonData["year"], merkleRoot)
            except:
                messages.error(request, "An error occured in blockchain")
                return HttpResponseRedirect("#")


            if schoolName.lower() != receiptJsonData["institution"].lower() or profileUser.name.lower() != \
                    receiptJsonData[
                        "name"].lower() or str(startYear) != str(receiptJsonData["year"]) or degree.lower() != receiptJsonData[
                "degree"].lower():
                messages.error(request, "Details provided were incorrect and doesn't match the certificate")
                res = False

            legitimate = res
            Education(user=profileUser, school=school, degree=degree, fieldOfStudy=fieldOfStudy, startYear=startYear,
                      endYear=endYear, certificate=receiptJsonData, additionalNotes=additionalNotes,
                      legitimate=legitimate).save()

            messages.success(request, "Data successfully updated")
            return HttpResponseRedirect("/profile/{0}".format(user.username))
        else:
            messages.error(request, "Field errors")
            return HttpResponseRedirect("#")
    elif request.method == 'GET':
        form = AddEducationForm()

    template = loader.get_template('userprofile/addEducation.html')
    context = {
        'page': 'Add Education',
        'user': request.user,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def editDetails(request):
    """
    Edit profile page details

    :param request: request from client
    :return: edit page
    """
    user = request.user
    bUser = User.objects.get(username=user.username)
    if request.method == 'POST':

        form = EditDetailsForm(request.POST, request.FILES, instance=bUser)

        if form.is_valid():
            form.save()
            messages.success(request, "Data successfully updated")
            return HttpResponseRedirect("/profile/{0}".format(user.username))
        else:
            messages.error(request, "Field errors")
            return HttpResponseRedirect("#")
    elif request.method == 'GET':
        form = EditDetailsForm(instance=bUser)

    template = loader.get_template('userprofile/editDetails.html')
    context = {
        'page': 'Edit Details',
        'user': request.user,
        'form': form,
    }
    return HttpResponse(template.render(context, request))
