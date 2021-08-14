import json
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from users.models import UserProfile
from bookings.forms import AddBookingForm, AddGuestForm, UpdateBookingForm
from bookings.models import Booking, BookingNote, Guest, MainGuestBookingMapping, ReOrderStringLogic
from collections import defaultdict
from bookings.utils import reArrangeOrder


@login_required(login_url='login')
def getAllBooking(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company = userProfile.company

    # Guset and Booking mapped model
    bookings = MainGuestBookingMapping.objects.filter(
        company=company,
        is_canceled=False,
        is_completed=False).order_by('-date_created')

    # Logic String of Company Booking
    reOrderLogic, created = ReOrderStringLogic.objects.get_or_create(
        company=company)

    # Append ids of booking from guestVsBooking Mapping in id_list
    id_list = []
    for item in bookings:
        id_list.append(item.booking.id)

    # Seperate booking ids on basis of their booking status
    allIds = []
    if (reOrderLogic.stage_1 is not None) and (
            reOrderLogic.stage_1 != ''):
        allIds.append(reOrderLogic.stage_1.split(','))

    if (reOrderLogic.stage_2 is not None) and (
            reOrderLogic.stage_2 != ''):
        allIds.append(reOrderLogic.stage_2.split(','))

    if (reOrderLogic.stage_3 is not None) and (
            reOrderLogic.stage_3 != ''):
        allIds.append(reOrderLogic.stage_3.split(','))

    if (reOrderLogic.stage_4 is not None) and (
            reOrderLogic.stage_4 != ''):
        allIds.append(reOrderLogic.stage_4.split(','))

    if (reOrderLogic.stage_5 is not None) and (
            reOrderLogic.stage_5 != ''):
        allIds.append(reOrderLogic.stage_5.split(','))

    if (reOrderLogic.stage_6 is not None) and (
            reOrderLogic.stage_6 != ''):
        allIds.append(reOrderLogic.stage_6.split(','))

    print("order Ids: ", allIds)

    columnOrder = defaultdict(list)
    for ids in allIds:
        for id in ids:
            # print("id: ", id) id_list contains id in int form
            #  while id here is in str form
            if int(id) in id_list:
                newObj = bookings.filter(booking=id)
                columnOrder[newObj[0].booking.booking_status].append(newObj[0])

    # print("columnOrder: ", type(columnOrder))
    # print("columnOrder: ", columnOrder)
    # for column in columnOrder['stage_1']:
    #     print("column: ", column)

    context = {
        "userProfile": userProfile,
        "bookings": bookings,
        "columnOrder": columnOrder,
    }

    return render(request, 'bookings/all_bookings.html', context)


@login_required(login_url='login')
def addBooking(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company = userProfile.company

    if request.method == 'POST':
        bookingFormPOST = AddBookingForm(company, request.POST)
        guestFormPOST = AddGuestForm(request.POST, request.FILES)

        # if bookingFormPOST.is_valid():
        #     print("booking form valid")
        # if guestFormPOST.is_valid():
        #     print("guest form valid")
        if bookingFormPOST.is_valid() and guestFormPOST.is_valid():

            # Save bookin object
            newBookingObj = bookingFormPOST.save(commit=False)
            newBookingObj.company = company
            newBookingObj.added_by = user
            newBookingObj.save()

            # Save main Guest object
            newMainGuestObj = guestFormPOST.save(commit=False)
            newMainGuestObj.booking = newBookingObj
            newMainGuestObj.added_by = user
            newMainGuestObj.save()

            # Map Main Guest to Booking
            MainGuestBookingMapping.objects.create(
                company=company,
                booking=newBookingObj,
                main_guest=newMainGuestObj,
                added_by=user
            )
            # Saving Reorder String
            bookingReorderLogic, create = ReOrderStringLogic.objects.get_or_create(
                company=company)

            if bookingReorderLogic.stage_1 == "" or bookingReorderLogic.stage_1 is None:
                bookingReorderLogic.stage_1 = str(newBookingObj.id)
            else:
                bookingReorderLogic.stage_1 += ',' + str(newBookingObj.id)
            bookingReorderLogic.save()

            return redirect('get_all_booking')
        else:
            print("add Landlord form not valid")
            # Send form with error

            return redirect('add_booking')

    # Get request
    else:
        bookingForm = AddBookingForm(company=company)
        guestForm = AddGuestForm()

        context = {
            "userProfile": userProfile,
            "guestForm": guestForm,
            "bookingForm": bookingForm,
        }
        return render(request, 'bookings/add_booking.html', context)


@login_required(login_url='login')
def getBookingDetails(request, booking_id):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    try:
        booking = Booking.objects.get(id=booking_id, is_deleted=False)
        bookingVsGuestMapping = MainGuestBookingMapping.objects.get(
            booking=booking)
    except booking.DoesNotExist:
        raise Http404()

    # If Booking does not belong to the company. send Error msg
    if booking.company != userProfile.company:
        return HttpResponseForbidden()

    # Post method to update landlord profile deails
    if request.method == 'POST':
        updateBookingForm = UpdateBookingForm(request.POST, instance=booking)

        if updateBookingForm.is_valid():
            # print("Form valid")
            updateBookingForm.save()
            return redirect('booking_details', booking_id=booking_id)
        else:
            print("form is not valid")

    # Get Method
    else:
        main_guest = MainGuestBookingMapping.objects.get(booking=booking)
        guests = Guest.objects.filter(
            booking=booking, is_deleted=False).order_by('-date_created')

        bookingNote = BookingNote.objects.filter(
            booking=booking, is_deleted=False).order_by('-date_created')

        addGuestForm = AddGuestForm()
        updateBookingForm = UpdateBookingForm(instance=booking)

        context = {
            "userProfile": userProfile,
            "booking": booking,
            "bookingVsGuestMapping": bookingVsGuestMapping,
            "bookingNote": bookingNote,
            "main_guest": main_guest,
            "guests": guests,
            "form": updateBookingForm,
            "guestForm": addGuestForm,
        }
        return render(request, 'bookings/booking_details.html', context)


# Booking canceled (Update Logic after canceled)
@login_required(login_url='login')
def cancelBooking(request, booking_id):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)

        try:
            booking = Booking.objects.get(id=booking_id, is_deleted=False)

            # If Booking does not belong to the company. send Error msg
            if booking.company != userProfile.company:
                return HttpResponseForbidden()

            bookingVsGuest = MainGuestBookingMapping.objects.get(
                booking=booking)
            bookingVsGuest.is_canceled = True
            bookingVsGuest.save()

            # logicOrder = ReOrderStringLogic.objects.get(
            #     company=userProfile.company)

        except Booking.DoesNotExist:
            raise Http404()

        return redirect('booking_details', booking_id=booking_id)


# Booking completed (Update Logic after canceled)
@login_required(login_url='login')
def bookingCompleted(request, booking_id):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)

        try:
            booking = Booking.objects.get(id=booking_id, is_deleted=False)
            # If Booking does not belong to the company. send Error msg
            if booking.company != userProfile.company:
                return HttpResponseForbidden()

            bookingVsGuest = MainGuestBookingMapping.objects.get(
                booking=booking)
            bookingVsGuest.is_completed = True
            bookingVsGuest.save()

        except Booking.DoesNotExist:
            raise Http404()

        return redirect('booking_details', booking_id=booking_id)


# Add Booking Guest post request
@ login_required(login_url='login')
def addGuest(request, booking_id):
    if request.method == 'POST':
        user = request.user
        try:
            booking = Booking.objects.get(id=booking_id, is_deleted=False)
        except Booking.DoesNotExist:
            raise Http404()

        guestForm = AddGuestForm(request.POST, request.FILES)

        if guestForm.is_valid():
            print("guest form valid")
            newGuestObj = guestForm.save(commit=False)
            newGuestObj.booking = booking
            newGuestObj.added_by = user
            newGuestObj.save()

        return redirect('booking_details', booking_id=booking_id)


@ login_required(login_url='login')
def deleteGuest(request, guest_id):
    try:
        guest = Guest.objects.get(id=guest_id, is_deleted=False)
    except Guest.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        guest.is_deleted = True
        guest.save()

        return redirect('booking_details', booking_id=guest.booking.id)


@ login_required(login_url='login')
def updateGuest(request, guest_id):
    try:
        guest = Guest.objects.get(id=guest_id, is_deleted=False)
    except Guest.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        guest.name = request.POST['name']
        guest.email = request.POST['email']
        guest.phone = request.POST['phone']
        guest.age = request.POST['age']
        guest.gender = request.POST['gender']
        guest.document_type = request.POST['document_type']

        if request.FILES['file_one']:
            guest.file_one = request.FILES['file_one']
        if request.FILES['file_two']:
            guest.file_one = request.FILES['file_two']
        guest.save()

        return redirect('booking_details', booking_id=guest.booking.id)


# Add Booking note post request
@ login_required(login_url='login')
def addBookingNote(request, booking_id):
    if request.method == 'POST':
        user = request.user
        note = request.POST['booking_note']

        try:
            booking = Booking.objects.get(id=booking_id, is_deleted=False)
        except Booking.DoesNotExist:
            raise Http404()

        BookingNote.objects.create(
            booking=booking,
            booking_note=note,
            updated_by=user
        )

        return redirect('booking_details', booking_id=booking_id)


@ login_required(login_url='login')
def deleteBookingNote(request, booking_note_id):
    try:
        bookingNote = BookingNote.objects.get(
            id=booking_note_id, is_deleted=False)
    except BookingNote.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        bookingNote.is_deleted = True
        bookingNote.save()

        return redirect('booking_details', booking_id=bookingNote.booking.id)


@ login_required(login_url='login')
def updateBookingNote(request, booking_note_id):
    try:
        bookingNote = BookingNote.objects.get(
            id=booking_note_id, is_deleted=False)
    except BookingNote.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        updatedNote = request.POST['booking_note']
        bookingNote.booking_note = updatedNote
        bookingNote.save()

        return redirect('booking_details', booking_id=bookingNote.booking.id)


@login_required(login_url='login')
def updateBookingStatus(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        data = json.loads(request.body)

        bookingId = data['bookingId']
        prevStatus = data['prevStatus']
        updatedStatus = data['updatedStatus']
        strObj = data['strObj']
        # print("prevStatus: ", prevStatus)
        # print("updatedStatus: ", updatedStatus)
        # print("strObj: ", strObj)

        booking = Booking.objects.get(id=bookingId)
        booking.booking_status = updatedStatus
        booking.save()

        reOrderLogic = ReOrderStringLogic.objects.get(
            company=userProfile.company)

        if prevStatus == "stage_1":
            reOrderLogic.stage_1 = strObj['movedFrom']
        elif prevStatus == "stage_2":
            reOrderLogic.stage_2 = strObj['movedFrom']
        elif prevStatus == "stage_3":
            reOrderLogic.stage_3 = strObj['movedFrom']
        elif prevStatus == "stage_4":
            reOrderLogic.stage_4 = strObj['movedFrom']
        elif prevStatus == "stage_5":
            reOrderLogic.stage_5 = strObj['movedFrom']
        elif prevStatus == "stage_6":
            reOrderLogic.stage_6 = strObj['movedFrom']
        elif prevStatus == "stage_7":
            reOrderLogic.stage_7 = strObj['movedFrom']

        if updatedStatus == "stage_1":
            reOrderLogic.stage_1 = strObj['movedTo']
        elif updatedStatus == "stage_2":
            reOrderLogic.stage_2 = strObj['movedTo']
        elif updatedStatus == "stage_3":
            reOrderLogic.stage_3 = strObj['movedTo']
        elif updatedStatus == "stage_4":
            reOrderLogic.stage_4 = strObj['movedTo']
        elif updatedStatus == "stage_5":
            reOrderLogic.stage_5 = strObj['movedTo']
        elif updatedStatus == "stage_6":
            reOrderLogic.stage_6 = strObj['movedTo']
        elif updatedStatus == "stage_7":
            reOrderLogic.stage_7 = strObj['movedTo']

        reOrderLogic.save()

    return JsonResponse({"msg": "state updated"})


@login_required(login_url='login')
def updateBookingStatusInProfile(request):
    data = json.loads(request.body)
    bookingId = data['bookingId']
    prevStatus = data['prevBookingStatus']
    updatedStatus = data['currentBookingStatus']

    # print("data: ", data)

    try:
        booking = Booking.objects.get(id=bookingId)

        # print("booking.booking_status: ", booking.booking_status)

        # Updatading booking status
        booking.booking_status = updatedStatus
        booking.save()
    except Booking.DoesNotExist:
        raise Http404()

    # guestVsBooking = MainGuestBookingMapping.objects.get(booking=booking)
    reOrderLogic = ReOrderStringLogic.objects.get(
        company=booking.company)

    if prevStatus == "stage_1":
        reOrderLogic.stage_1 = reArrangeOrder(
            reOrderLogic.stage_1, bookingId)

    elif prevStatus == "stage_2":
        reOrderLogic.stage_2 = reArrangeOrder(
            reOrderLogic.stage_2, bookingId)

    elif prevStatus == "stage_3":
        reOrderLogic.stage_3 = reArrangeOrder(
            reOrderLogic.stage_3, bookingId)

    elif prevStatus == "stage_4":
        reOrderLogic.stage_4 = reArrangeOrder(
            reOrderLogic.stage_4, bookingId)

    elif prevStatus == "stage_5":
        reOrderLogic.stage_5 = reArrangeOrder(
            reOrderLogic.stage_5, bookingId)

    elif prevStatus == "stage_6":
        reOrderLogic.stage_6 = reArrangeOrder(
            reOrderLogic.stage_6, bookingId)

    elif prevStatus == "stage_7":
        reOrderLogic.stage_7 = reArrangeOrder(
            reOrderLogic.stage_7, bookingId)

    if updatedStatus == "stage_1":
        if reOrderLogic.stage_1 == "" or reOrderLogic.stage_1 is None:
            reOrderLogic.stage_1 = str(bookingId)
        else:
            reOrderLogic.stage_1 += ',' + str(bookingId)

    elif updatedStatus == "stage_2":
        if reOrderLogic.stage_2 == "" or reOrderLogic.stage_2 is None:
            reOrderLogic.stage_2 = str(bookingId)
        else:
            reOrderLogic.stage_2 += ',' + str(bookingId)

    elif updatedStatus == "stage_3":
        if reOrderLogic.stage_3 == "" or reOrderLogic.stage_3 is None:
            reOrderLogic.stage_3 = str(bookingId)
        else:
            reOrderLogic.stage_3 += ',' + str(bookingId)

    elif updatedStatus == "stage_4":
        if reOrderLogic.stage_4 == "" or reOrderLogic.stage_4 is None:
            reOrderLogic.stage_4 = str(bookingId)
        else:
            reOrderLogic.stage_4 += ',' + str(bookingId)

    elif updatedStatus == "stage_5":
        if reOrderLogic.stage_5 == "" or reOrderLogic.stage_5 is None:
            reOrderLogic.stage_5 = str(bookingId)
        else:
            reOrderLogic.stage_5 += ',' + str(bookingId)

    elif updatedStatus == "stage_6":
        if reOrderLogic.stage_6 == "" or reOrderLogic.stage_6 is None:
            reOrderLogic.stage_6 = str(bookingId)
        else:
            reOrderLogic.stage_6 += ',' + str(bookingId)

    elif updatedStatus == "stage_7":
        if reOrderLogic.stage_7 == "" or reOrderLogic.stage_6 is None:
            reOrderLogic.stage_7 = str(bookingId)
        else:
            reOrderLogic.stage_7 += ',' + str(bookingId)
    reOrderLogic.save()

    return JsonResponse({"msg": "updated"})
