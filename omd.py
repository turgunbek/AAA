def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()

def step2_umbrella():
    """
    case of 1st choice - answer 'yes'
    """
    msg_1 = 'Утка-маляр таки взяла зонт.'
    msg_2 = 'В бар. Зонт. Утка! Ещё и маляр? КАРЛ! Что мы курим?'
    print('\033[91m {}\033[00m'.format(msg_1))
    print('\033[94m {}\033[00m'.format(msg_2))

def step2_no_umbrella():
    """
    case of 2nd choice - answer 'no'
    """
    msg_1 = 'Утка-маляр всё-таки не взяла зонт.'
    msg_2 = 'Да ладно? Серьезно? А вдруг дождь ' + \
        ''.join([u'\u0336{}'.format(c) for c in ' на улице ']) + ' в баре...'
    print('\033[91m {}\033[00m'.format(msg_1))
    print('\033[94m {}\033[00m'.format(msg_2))

if __name__ == '__main__':
    step1()