from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from users.models import UserProfile
from landlords.forms import AddLandlordForm, AddLandlordDocForm
from bookings.models import Booking, BookingNote, Guest


@login_required(login_url='login')
def getAllBooking(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    bookings = Booking.objects.filter(
        company=userProfile.company,
        is_deleted=False).order_by('-date_created')

    context = {
        "userProfile": userProfile,
        "bookings": bookings,
    }
    return render(request, 'bookings/all_bookings.html', context)


@login_required(login_url='login')
def addBooking(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        landlordForm = AddLandlordForm(request.POST)

        if landlordForm.is_valid():
            # print("land lord form valid")
            newLandlordObj = landlordForm.save(commit=False)
            newLandlordObj.managed_by = userProfile.company
            newLandlordObj.added_by = user
            newLandlordObj.save()

            return redirect('get_all_landlord')
        else:
            print("add Landlord form not valid")

    # Get request
    else:
        form = AddLandlordForm()

        context = {
            "userProfile": userProfile,
            "form": form,
        }
        return render(request, 'landlords/add_landlord.html', context)


@login_required(login_url='login')
def getBookingDetails(request, landlord_id):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    try:
        landlord = Landlord.objects.get(id=landlord_id, is_deleted=False)
    except Landlord.DoesNotExist:
        raise Http404()

    # If landlord does not belong to the company. send Error msg
    if landlord.managed_by != userProfile.company:
        return HttpResponseForbidden()

    # Post method to update landlord profile deails
    if request.method == 'POST':
        landlordForm = AddLandlordForm(request.POST, instance=landlord)

        if landlordForm.is_valid():
            print("Form valid")
            landlordForm.save()
            return redirect('landlord_profile', landlord_id=landlord_id)
        else:
            print("form is not valid")
    else:

        landlordNote = LandlordNote.objects.filter(
            landlord=landlord,
            is_deleted=False).order_by('-date_created')

        landlordDoc = LandlordDocument.objects.filter(
            landlord=landlord,
            is_deleted=False).order_by('-date_created')

        updateLandlordForm = AddLandlordForm(instance=landlord)

        addLandlordDocForm = AddLandlordDocForm()

        context = {
            "userProfile": userProfile,
            "landlord": landlord,
            "landlordNote": landlordNote,
            "landlordDoc": landlordDoc,
            "form": updateLandlordForm,
            "doc_form": addLandlordDocForm,
        }
        return render(request, 'landlords/landlord_profile.html', context)


@login_required(login_url='login')
def deleteBooking(request, landlord_id):
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


# Add Booking note post request
@ login_required(login_url='login')
def addBookingNote(request, landlord_id):
    if request.method == 'POST':
        user = request.user
        note = request.POST['landlord_note']

        try:
            landlord = Landlord.objects.get(id=landlord_id, is_deleted=False)
        except Landlord.DoesNotExist:
            raise Http404()

        LandlordNote.objects.create(
            landlord=landlord,
            landlord_note=note,
            updated_by=user
        )

        return redirect('landlord_profile', landlord_id=landlord_id)


@ login_required(login_url='login')
def deleteBookingNote(request, landlord_note_id):
    try:
        landlordNote = LandlordNote.objects.get(
            id=landlord_note_id, is_deleted=False)
    except LandlordNote.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        landlordNote.is_deleted = True
        landlordNote.save()

        return redirect(
            'landlord_profile', landlord_id=landlordNote.landlord.id)
