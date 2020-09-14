#! /usr/bin/python3

import sys
import os
import nltk
import random

# pip3 install scikit-learn
# Импорт методов для Векторизации данных из DataSet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Импорт методов для Классификации
from sklearn.linear_model import LogisticRegression

# Импорт методов для тестового разбиения DataSet
from sklearn.model_selection import train_test_split

# Добавляем путь к родительской директории
two_up = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(two_up)

# Есть 2 различных DataSet
from nlp_bot.DataSet.DataSet_2 import BOT_CONFIG
# from nlp_bot.DataSet.DataSet_1 import BOT_CONFIG


"""
Создаем бота для работы с NLP.
1 - Используем правила, тоесть заранее  заготовленные ответы, а четко
    поставленные вопросы. Тоесть четткое правило поведения, на четко
    поставленный intent(намеренье).
2 - Если четкого intent не нашлось, то используем Генеративную Модель
    generative model, которая из больщого числа фраз вернет максимально
    соответствующий ответ.
3 - Если ничего не сработало, то используем заглушки
"""


def trace(object):
    print('==============')
    print(object)
    print('==============')


def get_default_response():
    """Метод Заглушка, возвращает дефолтное значение."""
    candidates = BOT_CONFIG['failure_responses']
    return random.choice(candidates)


def generative_answer():
    """Генерация Ответа при помощи Генеративнйо Модели."""
    return None


def get_intent(text):
    """Поиск Интентов, четко поставленых намерений пользователя."""

    for intent_name, intent_data in BOT_CONFIG['intents'].items():
        for example in intent_data['examples']:
            distance = nltk.edit_distance(text.lower(), example.lower())
            # print(distance, distance / len(example)*100)
            if distance / len(example) < 0.4:
                return intent_name



# TODO Тут написать код для генерации ответа на четкий интент
def get_response_by_intent(intent):
    """Генерация ответа на сполученный Интент."""
    candidates = BOT_CONFIG['intents'][intent]['responses']
    return random.choice(candidates)


def get_answer(text):
    """Основной метод поиска ответ на поставленный пользователем вопрос"""

    # TODO Ищем Четкое намеренье пользователя.
    intent = get_intent(text)

    if intent:
        return get_response_by_intent(intent)

    # TODO Используем Генеративную модель.
    # response = generative_answer(text)
    response = generative_answer()

    if response:
        return response

    # TODO Если ничего не сработало, то используем метод заглушку.
    return get_default_response()


def prepareVectorize():
    """Метод подготовки(Классификаци) нашего DataSet для векторизации"""
    dataset = []
    for intent, intent_data in BOT_CONFIG['intents'].items():
        for example in intent_data['examples']:
            dataset.append([example, intent])
    return dataset


def vectorizationDataSet(dataset):
    """ВЕКТОРИЗАЦИЯ нашего DataSet
    Тут используется метод работы 'Мешок слов' методом CountVectorizer()
    Можно былобы использовать метод TfidfVectorizer() более сложный метод для
    векторизации.
    """
    x_text = [x for x, y in dataset]
    y = [y for x, y in dataset]

    vectorizer = CountVectorizer()
    # vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(x_text)

    text = 'ну привтеики как дела?'
    result_vector = vectorizer.transform([text])
    # print(result_vector.toarray())




    # Вывести весь список слов что были встрчены,
    # print(vectorizer.get_feature_names())
    # если фраза простая то значения может встречаться очень редко
    # print(X.toarray()[0])
    # print(X.toarray())

    # for elem in x_text[:100]:
    # for elem in y:
    #     print(elem)
    classification_method(X, y, result_vector)


def classification_method(X, y, result_vector):
    """КЛАССИФИКАЦИЯ
    Алгоритмов классификации довольно много, и разделены они по тематике, типо
    Линейной регрессии, SGD классификация .... используем Логичексуцю Регрессию.
    """
    # Скармливаем Векторизированные данные нашему алгоритму линейной регрессии
    # Так сказать обучаем нашу машину,
    clf = LogisticRegression()

    # clf.fit(X, y)
    tester_split_dataset(clf, X, y)

    # # print(clf.predict(X[:100]))
    #
    # # Посмотреть какие классы есть у классификатора
    # trace(clf.classes_)
    #
    # # Посмотретреть какие вероятности соотношения текста и Классов Интентов
    # trace(clf.predict_proba(result_vector))
    #
    # trace(clf.predict(result_vector))




def tester_split_dataset(clf, X, y):
    """Тестирование
    Делаем случайное деление нашего DataSet на 2 части для
    обучения и для теста, далее если модель обучившись на одной части
    сможет предсказывать другую, то можно говорить о хороших вероятностях
    нашей обученной мождели."""

    # Метод тестового разделения Dataset 2 части
    X_train, X_test, y_train, y_test = train_test_split(
                                                            X,
                                                            y,
                                                            test_size=0.33,
                                                            # random_state=42
                                                        )
    clf.fit(X_train, y_train)

    # Тест,оказать процент совпадения
    test_result = clf.score(X_test, y_test)
    print(test_result)


def start_app():
    while True:
        """Старт процессу бесконечного опроса, в ожиданнии вопроса от пользователя."""
        question = input("Ввод: ")
        print(get_answer(question))


def run():
    """Метод запуска приложения."""
    pass


def nlp_bot_get_message(question):
    """Метод получения сообщения от пользователя."""

    print('============'*10)
    print(type(question))
    print(question)
    print('============'*10)

    answer = get_answer(question)
    print(type(question))
    print('Вопрос = ', question)
    print('Ответ = ', answer)
    return answer

# start_app()
# vectorizationDataSet(prepareVectorize())


