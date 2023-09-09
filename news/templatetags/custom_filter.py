from django import template
#from .bad_words import bad_words

register = template.Library()

@register.filter(name='Censor')
def Censor(value):
    file_path = 'bad_words.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()  # Читаем содержимое файла и удаляем лишние пробелы и символы новой строки
        bad_words = content.split(',')  # Разделяем строку по запятой и создаем массив

    censored_value = value
    for word in bad_words:
        censored_value = censored_value.replace(word, '*****')
    return censored_value