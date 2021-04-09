import random


def generateRandomPass():
    characters = list('abcdefghijklmnopqrstuvwxyz')
    characters.extend('ABCDEFGHIJHIJKLMNOPQRSTUVWXYZ')
    characters.extend('0123456789')
    characters.extend('!@#$%^&*()-')

    thepassword = ''
    for i in range(10):
        thepassword += random.choice(characters)

    return thepassword
