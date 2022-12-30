import easygui as g
def ask_yes_no(question, title='Game'):
    '''Спрашивает вопрос'''
    responce=g.ynbox(question, title=title)
    return responce
def ask_number(question, low, high,title='Game'):
    '''Просит ввести число из заданого диапазона'''
    responce=g.integerbox(question, lowerbound=low, upperbound=high, title=title)
    return responce
if __name__=='__main__':
    g.msgbox('Вы запустили модуль, а не импортировали его')
    g.msgbox('Тестирование')
    answer=ask_yes_no('Продолжаем тестирование')
    g.msgbox('Функция да_нет вернула '+str(answer))
    answer=ask_number('введите число от одного до десяти', 1, 10)
    g.msgbox('Функция ask_number вернула '+str(answer))