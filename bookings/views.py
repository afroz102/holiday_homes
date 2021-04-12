from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from users.models import UserProfile
from bookings.forms import AddBookingForm, AddGuestForm, UpdateBookingForm
from bookings.models import Booking, BookingNote, Guest, MainGuestBookingMapping, ReOrderStringLogic


@login_required(login_url='login')
def getAllBooking(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    bookings = MainGuestBookingMapping.objects.filter(
        company=userProfile.company).order_by('-date_created')

    context = {
        "userProfile": userProfile,
        "bookings": bookings,
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

            bookingReorderLogic.lead = str(newBookingObj.id)
            bookingReorderLogic.save()
            # if shortlistedOrder is None or shortlistedOrder == '':
            #     jobReorderLogic.shortlisted = str(resumeId)
            # else:
            #     jobReorderLogic.shortlisted = shortlistedOrder + \
            #         ',' + str(resumeId)

            return redirect('get_all_booking')
        else:
            print("add Landlord form not valid")

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
            "bookingNote": bookingNote,
            "main_guest": main_guest,
            "guests": guests,
            "form": updateBookingForm,
            "guestForm": addGuestForm,
        }
        return render(request, 'bookings/booking_details.html', context)


@login_required(login_url='login')
def deleteBooking(request, booking_id):
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
    user = request.user
    try:
        UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return JsonResponse({"msg": "Not Authorized"})

    if request.method == 'POST':
        data = json.loads(request.body)
        # print("Data: ", data)
        jobId = data['jobId']
        resumeId = data['resumeId']
        prevStatus = data['prevStatus']
        updatedStatus = data['updatedStatus']
        strObj = data['strObj']

        candidateToBeUpdated = ResumeToJobMapping.objects.get(
            job=jobId, resume=resumeId)

        reOrderLogic = ReOrderStringLogic.objects.get(job=jobId)

        if prevStatus == "shortlisted":
            reOrderLogic.shortlisted = strObj['movedFrom']
        elif prevStatus == "approved":
            reOrderLogic.approved = strObj['movedFrom']
        elif prevStatus == "scheduled":
            reOrderLogic.scheduled = strObj['movedFrom']
        elif prevStatus == "selected":
            reOrderLogic.selected = strObj['movedFrom']
        elif prevStatus == "joined":
            reOrderLogic.joined = strObj['movedFrom']
        elif prevStatus == "rejected":
            reOrderLogic.rejected = strObj['movedFrom']

        if updatedStatus == "shortlisted":
            reOrderLogic.shortlisted = strObj['movedTo']
        elif updatedStatus == "approved":
            reOrderLogic.approved = strObj['movedTo']
        elif updatedStatus == "scheduled":
            reOrderLogic.scheduled = strObj['movedTo']
        elif updatedStatus == "selected":
            reOrderLogic.selected = strObj['movedTo']
        elif updatedStatus == "joined":
            reOrderLogic.joined = strObj['movedTo']
        elif updatedStatus == "rejected":
            reOrderLogic.rejected = strObj['movedTo']

        reOrderLogic.save()

        candidateToBeUpdated.applicationStatus = updatedStatus

        candidateToBeUpdated.save()

    return JsonResponse({"msg": "state updated"})


@login_required(login_url='login')
def updateBookingStatusInProfile(request):
    data = json.loads(request.body)
    statusBeforeShuffle = data['statusBeforeShuffle']
    statusAfterShuffle = data['statusAfterShuffle']
    bookingId = data['booking_id']

    resumeVsJob = ResumeToJobMapping.objects.get(id=resumeVsJobId)
    reOrderLogic = ReOrderStringLogic.objects.get(
        job=resumeVsJob.job.id)

    if statusBeforeShuffle == "shortlisted":
        reOrderLogic.shortlisted = reArrangeOrder(
            reOrderLogic.shortlisted, resumeId)

    elif statusBeforeShuffle == "approved":
        reOrderLogic.approved = reArrangeOrder(
            reOrderLogic.approved, resumeId)

    elif statusBeforeShuffle == "scheduled":
        reOrderLogic.scheduled = reArrangeOrder(
            reOrderLogic.scheduled, resumeId)

    elif statusBeforeShuffle == "selected":
        reOrderLogic.selected = reArrangeOrder(
            reOrderLogic.selected, resumeId)

    elif statusBeforeShuffle == "joined":
        reOrderLogic.joined = reArrangeOrder(
            reOrderLogic.joined, resumeId)

    elif statusBeforeShuffle == "rejected":
        reOrderLogic.rejected = reArrangeOrder(
            reOrderLogic.rejected, resumeId)

    if statusAfterShuffle == "shortlisted":
        if reOrderLogic.shortlisted == "" or reOrderLogic.shortlisted is None:
            reOrderLogic.shortlisted = str(resumeId)
        else:
            reOrderLogic.shortlisted += ',' + str(resumeId)

    elif statusAfterShuffle == "approved":
        if reOrderLogic.approved == "" or reOrderLogic.approved is None:
            reOrderLogic.approved = str(resumeId)
        else:
            reOrderLogic.approved += ',' + str(resumeId)

    elif statusAfterShuffle == "scheduled":
        if reOrderLogic.scheduled == "" or reOrderLogic.scheduled is None:
            reOrderLogic.scheduled = str(resumeId)
        else:
            reOrderLogic.scheduled += ',' + str(resumeId)

    elif statusAfterShuffle == "selected":
        if reOrderLogic.selected == "" or reOrderLogic.selected is None:
            reOrderLogic.selected = str(resumeId)
        else:
            reOrderLogic.selected += ',' + str(resumeId)

    elif statusAfterShuffle == "joined":
        if reOrderLogic.joined == "" or reOrderLogic.joined is None:
            reOrderLogic.joined = str(resumeId)
        else:
            reOrderLogic.joined += ',' + str(resumeId)

    elif statusAfterShuffle == "rejected":
        if reOrderLogic.rejected == "" or reOrderLogic.rejected is None:
            reOrderLogic.rejected = str(resumeId)
        else:
            reOrderLogic.rejected += ',' + str(resumeId)
    reOrderLogic.save()

    resumeVsJob.applicationStatus = statusAfterShuffle
    resumeVsJob.save()
    return JsonResponse({"msg": "hello"})
