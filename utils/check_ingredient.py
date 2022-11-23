import string
from django.http import HttpResponse

lst = ['tomato', 'mea2t', 'milk']


def char_ingredient(args):
    for ingredient in args:
        for symbol in ingredient:
            if symbol in string.digits or symbol in string.punctuation:
                break
        else:
            continue
        # return HttpResponse(f'{ingredient} - Punctuation marks and/or numbers in the ingredient are found')
        return f'{ingredient} - Punctuation marks and/or numbers in the ingredient are found'


if __name__ == '__main__':

    a = char_ingredient(lst)
    print(a)
