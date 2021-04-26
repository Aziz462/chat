def check_password(z):
    en_1 = 'qwertyuiop'
    en_2 = 'asdfghjkl'
    en_3 = 'zxcvbnm'
    r_1 = 'йцукенгшщзхъ'
    r_2 = 'фывапролджэ'
    r_3 = 'ячсмитьбю'
    numbers = '1234567890'
    CAPS_ru = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    CAPS_en = 'QWERTYUIOPSDFGHJKLZXCVBNM'
    small_ru = 'йцукенгшщзхъфывапролджэячсмитьбю'
    small_en = 'qwertyuiopasdfghjklzxcvbnm'


    if len(z) <= 8:
        return 'Пароль слишком короткий, попробуйте ещё раз'
    else:
        CAPSf = False
        smallf = False
        numbersf = False
        for i in z:
            if i in CAPS_ru:
                CAPSf = True
            elif i in CAPS_en:
                CAPSf = True
            elif i in small_ru:
                smallf = True
            elif i in small_en:
                smallf = True
            elif i in numbers:
                numbersf = True
        if not CAPSf or not smallf:
            return 'В пароле присутствуют символы только одного регистра, попробуйте ещё раз'
        else:
            if not numbersf:
                return 'В пароле отсутствуют цифры, попробуйте ещё раз'
            else:
                for j in range(0, len(z) - 2):
                    if z[j:j + 3].lower() in en_1 or \
                       z[j:j + 3].lower() in en_2 or \
                       z[j:j + 3].lower() in en_3:
                        return 'В пароле подряд идущие символы, попробуйте ещё раз'
                    if z[j:j + 3].lower() in r_1 or \
                       z[j:j + 3].lower() in r_2 or \
                       z[j:j + 3].lower() in r_3:
                        return 'В пароле подряд идущие символы, попробуйте ещё раз'
                return 'ok'


