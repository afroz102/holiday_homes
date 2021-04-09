from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from users.models import UserProfile
from units.models import Unit, UnitNote
from units.forms import AddUnitForm, UpdateUnitForm


@login_required(login_url='login')
def getAllUnit(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    units = Unit.objects.filter(
        company=userProfile.company,
        is_deleted=False).order_by('-date_created')

    context = {
        "userProfile": userProfile,
        "units": units,
    }
    return render(request, 'units/units.html', context)


@login_required(login_url='login')
def addUnit(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company = userProfile.company

    if request.method == 'POST':
        unitForm = AddUnitForm(company, request.POST, request.FILES)

        if unitForm.is_valid():
            # print("land lord form valid")
            newUnitObj = unitForm.save(commit=False)
            newUnitObj.company = company
            newUnitObj.added_by = user
            newUnitObj.save()

            return redirect('get_all_unit')
        else:
            print("add Landlord form not valid")

    # Get request
    else:
        form = AddUnitForm(managed_by=company)

        context = {
            "userProfile": userProfile,
            "form": form,
        }
        return render(request, 'units/add_unit.html', context)


@login_required(login_url='login')
def getUnitDetails(request, unit_id):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    try:
        unit = Unit.objects.get(id=unit_id, is_deleted=False)
    except Unit.DoesNotExist:
        raise Http404()

    print("UNIT/flat: ", unit)

    # If landlord does not belong to the company. send Error msg
    if unit.company != userProfile.company:
        return HttpResponseForbidden()

    # Post method to update landlord profile deails
    if request.method == 'POST':
        updateUnitForm = UpdateUnitForm(request.POST, instance=unit)

        if updateUnitForm.is_valid():
            print("Form valid")
            updateUnitForm.save()
            return redirect('unit_details', unit_id=unit_id)
        else:
            print("form is not valid")
    else:

        unitNote = UnitNote.objects.filter(
            unit=unit,
            is_deleted=False).order_by('-date_created')

        updateUnitForm = UpdateUnitForm(instance=unit)

        # addLandlordDocForm = AddLandlordDocForm()

        context = {
            "userProfile": userProfile,
            "unit": unit,
            "unitNote": unitNote,
            "form": updateUnitForm,
        }
        return render(request, 'units/unit_details.html', context)


@login_required(login_url='login')
def deleteUnit(request, landlord_id):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)

        try:
            landlord = Landlord.objects.get(id=landlord_id, is_deleted=False)
        except Landlord.DoesNotExist:
            raise Http404()

        # If landlord does not belong to the company. send Error msg
        if landlord.managed_by != userProfile.company:
            return HttpResponseForbidden()

        landlord.is_deleted = True
        landlord.save()
        return redirect('get_all_landlord')


# Add client note post request
@ login_required(login_url='login')
def addUnitNote(request, unit_id):
    if request.method == 'POST':
        user = request.user
        note = request.POST['unit_note']

        try:
            unit = Unit.objects.get(id=unit_id, is_deleted=False)
        except Unit.DoesNotExist:
            raise Http404()

        UnitNote.objects.create(
            unit=unit,
            unit_note=note,
            updated_by=user
        )

        return redirect('unit_details', unit_id=unit_id)


@ login_required(login_url='login')
def deleteUnitNote(request, unit_note_id):
    try:
        unitNote = UnitNote.objects.get(
            id=unit_note_id, is_deleted=False)
    except UnitNote.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        unitNote.is_deleted = True
        unitNote.save()

        return redirect('unit_details', unit_id=unitNote.unit.id)


@ login_required(login_url='login')
def updateUnitNote(request, unit_note_id):
    try:
        unitNote = UnitNote.objects.get(
            id=unit_note_id, is_deleted=False)
    except UnitNote.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        updatedNote = request.POST['unit_note']
        unitNote.unit_note = updatedNote
        unitNote.save()

        return redirect('unit_details', unit_id=unitNote.unit.id)
