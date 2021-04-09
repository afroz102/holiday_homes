from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))


generate_token = TokenGenerator()


def validateRegisterForm(data):
    response = {
        "msg": "",
        "error": False,
    }
    if (data['company_name'] is None or data['company_name'] == '') or (
        data['first_name'] is None or data['first_name'] == '') or (
            data['last_name'] is None or data['last_name'] == '') or (
                data['email'] is None or data['email'] == '') or (
                    data['password'] is None or data['password'] == ''):
        response['msg'] = "Please fill all the fields"
        response['error'] = True
        return response

    if len(data['password']) < 6:
        response['msg'] = "passwords should be atleast 6 characters long"
        response['error'] = True
        return response

    if data['password'] != data['password2']:
        response['msg'] = "Password do not matches"
        response['error'] = True
        return response

    try:
        user = User.objects.get(email=data['email'])
        if user and user.is_active is True:
            response['msg'] = "Email is taken"
            response['error'] = True
            return response

    except Exception as identifier:
        return response

    return response


def addUserFormValidate(email, f_name, l_name, access_type):
    response = {
        "error": False,
        "msg": ''
    }
    if (email is None or email == '') or (f_name is None or f_name == '') or (
            l_name is None or l_name == '') or (
                access_type is None or access_type == ''):
        response.error = True
        response.msg = "Please Fill all the fields"
        return response
    try:
        if User.objects.get(email=email):
            response.error = True
            response.msg = 'User already exists with this email'
            return response

    except Exception as identifier:
        pass

    return response
