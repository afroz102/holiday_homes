from django.http.response import JsonResponse, Http404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from users.decorators import unauthenticated_user
from users.models import UserCompany, UserToCompanyMapping, UserProfile
from users.sendEmail import sendEmail, sendEmailInvitationToUser
from users.utils import generate_token, validateRegisterForm, addUserFormValidate
from django.contrib.auth.decorators import login_required
from users.randomPwdGenerator import generateRandomPass
from users.forms import AddInternalUserForm1, AddInternalUserForm2
# from users.sendEmail import


# Register Company and send invation link to user email
@unauthenticated_user
def register_user(request):
    if request.method == 'GET':
        return render(request, 'auth/register.html')

    if request.method == 'POST':

        context = {'data': request.POST}

        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        validatePostForm = validateRegisterForm(request.POST)

        # print("validatePostForm: ", validatePostForm)

        if validatePostForm['error']:
            messages.add_message(request, messages.ERROR,
                                 validatePostForm['msg'])

            return render(request, 'auth/register.html', context, status=400)

        # Create a new User
        newUser, created = User.objects.get_or_create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        if created:
            newUser.set_password(password)
        newUser.is_active = False
        newUser.save()

        # Create an Company Object, user as super admin
        newCompanyObject = UserCompany.objects.create(
            super_admin=newUser,
            company_name=company_name,
        )
        # print("newAgencyObject: ", newAgencyObject)

        # Create a User Profile Table with user and agency
        newUserProfile = UserProfile.objects.create(
            user=newUser,
            company=newCompanyObject,
        )

        # Create a user to agency mapping, user as super-admin
        UserToCompanyMapping.objects.create(
            user_profile=newUserProfile,
            company=newCompanyObject,
            access_type="super-admin"
        )

        # Send registration email to user email
        sendEmail(request, newUser)

        # print("sendingEmail: ", sendingEmail)

        messages.add_message(request, messages.SUCCESS,
                             'A link has been sent to your email.'
                             'click on the link to activate your account.')

        return redirect('login')


# Account activation
def activate_account(request, uidb64, token):
    try:
        # checking if the uid is same as user.id sent from the host
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as identifier:
        user = None

    # if id matches set user as verified and save
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'account activated successfully')
        return redirect('login')

    # else return to activation failed page to show error message
    return render(request, 'auth/activate_failed.html', status=401)


# Login User
@unauthenticated_user
def login_user(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')

    if request.method == "POST":
        context = {
            'data': request.POST,
        }

        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == '' or password == '':
            messages.add_message(request, messages.ERROR,
                                 'Please fill all the fields')
            return render(request, 'auth/login.html', status=401,
                          context=context)

        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, username=email, password=password)
        # print("user: ", user)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Email or Password is Wrong')
            return render(request, 'auth/login.html', status=401,
                          context=context)

        login(request, user)

        return redirect('dashboard')


def logoutUser(request):
    logout(request)
    return redirect('login')

# All User


@login_required(login_url='login')
def getAllUser(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    inUsers = UserProfile.objects.filter(
        company=userProfile.company.id, is_deleted=False)

    userToCompany = UserToCompanyMapping.objects.filter(
        company=userProfile.company.id)

    # print("clients: ", clients)
    context = {
        "userProfile": userProfile,
        "inUsers": inUsers,
        "userToAgency": userToCompany,
    }
    return render(request, 'internal_user/internal_users.html', context)


@login_required(login_url='login')
def addUser(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company = UserCompany.objects.get(id=userProfile.company.id)
    form1 = AddInternalUserForm1()
    form2 = AddInternalUserForm2()
    context = {
        "userProfile": userProfile,
        "form1": form1,
        "form2": form2
    }

    if request.method == 'POST':
        context = {
            "userProfile": userProfile,
            "form1": form1,
            "form2": form2,
            'data': request.POST
        }
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        access_type = request.POST.get('access_type')
        password = generateRandomPass()

        validateForm = addUserFormValidate(
            email, first_name, last_name, access_type)

        if validateForm['error']:
            messages.add_message(request, messages.ERROR, validateForm['msg'])
            return render(request, 'internal_user/add_user_form.html',
                          context, status=400)

        newUser = User.objects.create_user(username=email, email=email)
        newUser.set_password(password)
        newUser.first_name = first_name
        newUser.last_name = last_name
        newUser.save()

        # Create a userprofile with user and agency
        newUserProfile = UserProfile.objects.create(
            user=newUser, company=company)
        # newUserProfile.save()

        # Map user to agency
        UserToCompanyMapping.objects.create(
            user_profile=newUserProfile,
            company=company,
            access_type=access_type
        )

        # Send invitation mail to user email
        sendEmailInvitationToUser(request, newUser, password)

        messages.add_message(request, messages.SUCCESS,
                             'The Invitaion link has been sent to user.')
        return render(request, 'internal_user/add_user_form.html',
                      context, status=200)

    return render(request, 'internal_user/add_user_form.html', context)


@login_required(login_url='login')
def userProfile(request, user_id):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company = UserCompany.objects.get(id=userProfile.company.id)

    internalUser = UserProfile.objects.get(id=user_id)
    # inUserProfileDetails, created = UserProfileDetail.objects.get_or_create(
    #     user=user, agency=agency)

    if internalUser.company != userProfile.company:
        return JsonResponse({
            "status": "Error",
            "msg": "You are not authorized"
        })

    userToCompany = UserToCompanyMapping.objects.filter(
        user_profile=internalUser, company=company).first()
    # print("userToAgency: ", userToAgency)

    # form1 = UpdateInUserForm1(instance=inUser.user)  # user
    # form2 = UpdateInUserForm2(instance=inUserProfileDetails)  # UserProfile
    # form3 = AddInUserForm2(instance=userToAgency)  # Userprofile Agency Mapping
    # userNote = UserProfileNote.objects.filter(
    #     user_profile=inUser, is_deleted=False)

    context = {
        # 'form1': form1,
        # 'form2': form2,
        # "form3": form3,
        "user": internalUser,
        # "doc_form": doc_form,
        # "userNote": userNote,
        "userToCompany": userToCompany,
        "userProfile": userProfile,
    }
    if request.method == 'POST':
        # userStatus = request.POST['active_status']
        form1Data = UpdateInUserForm1(request.POST, instance=inUser.user)
        form2Data = UpdateInUserForm2(
            request.POST, request.FILES, instance=inUserProfileDetails)
        form3Data = AddInUserForm2(request.POST, instance=userToAgency)

        # print("form1 Data: ", form1Data)

        if form1Data.is_valid() and form2Data.is_valid() and form3Data.is_valid():
            print("form is valid")
            form1Data.save()
            form2Data.save()
            form3Data.save()
            # if userStatus == 'inactive':
            #     form1Data.is_active = False
            # form1Data.save()
            return redirect('in_user', in_user_id=in_user_id)

    return render(request, 'internal_user/in_user_profile.html', context)
