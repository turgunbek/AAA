import string


class CountVectorizer:
    """ Класс для работы с текстовым корпусом.

    Содержит 3 атрибута (экземпляра):

    lowercase = True (default), если приводим все токены к нижнему регистру,
                иначе оставляем текст как есть

    dict_tokens - словарь для отображения токенов в индексы

    feature_names - список для хранения имён признаков

    ==========================================================================
    А также содержит 4 метода (экземпляра):

    __clear_corpus_from_specsymbols() - приватный метод, служащий для очискти
    входного корпуса слов от спецсимволов: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~

    __make_dict_tokens() - приватный метод, создаёт словарь с ключами из
        уникальных токенов и значениями из чисел 0,1,2,...

    fit_transform() - возвращает терм-документную матрицу.
    Подразумевается вызов этого метода до вызова метода get_feature_names()
    (также как и в классе sklearn.feature_extraction.text.CountVectorizer)

    get_feature_names() - возвращает имена всех уникальных токенов,
    причём функция не подразумевает входных аргументов, и поэтому будет
    возвращать список токенов, полученных с последнего вызова fit_transform()
    (Т.е. метод работает по аналогии с оригинальным классом
    sklearn.feature_extraction.text.CountVectorizer)
    """

    def __init__(self, lowercase: bool = True):
        self.lowercase = lowercase  # по дефолту все токены -> в нижний регистр
        self.dict_tokens = {}  # Словарь для отображения токенов в индексы
        self.feature_names = []  # Список для хранения имен признаков

    def __clear_corpus_from_specsymbols(self, corpus: list[str]) -> list[str]:
        corpus_cleaned = [
            document.translate(str.maketrans('', '', string.punctuation))
            for document in corpus
            ]
        return corpus_cleaned

    def __make_dict_tokens(self, corpus: list[str]) -> dict[str]:
        self.dict_tokens = {}
        for document in corpus:
            if self.lowercase:
                tokens = document.lower().split()
            else:
                tokens = document.split()
            for token in tokens:
                if token not in self.dict_tokens:
                    self.dict_tokens[token] = len(self.dict_tokens)
        return self.dict_tokens

    def fit_transform(
            self,
            corpus: list[str],
            lowercase: bool = True
            ) -> list[list[int]]:
        self.lowercase = lowercase
        corpus_cleaned = self.__clear_corpus_from_specsymbols(corpus)
        self.dict_tokens = self.__make_dict_tokens(corpus_cleaned)

        self.feature_names = [feature for feature, _ in sorted(
            self.dict_tokens.items(), key=lambda x: x[1])]
        # Здесь идёт сортировка словаря по ключу, т.к. в старых версиях Python
        # словари были не упорядочены, а по логике метода требуется порядок.
        # Создание списка feature_names именно здесь обусловлено тем, что
        # подразумевается вызов метода fit_transofrm() перед вызовом метода
        # get_feature_names() (также как и в оригинальном классе из sklearn)

        n = len(self.dict_tokens)
        count_matrix = [[0] * n for _ in range(len(corpus_cleaned))]
        for i, document in enumerate(corpus_cleaned):
            doc_without_symbols = document.translate(
                str.maketrans('', '', string.punctuation))
            if self.lowercase:
                tokens = doc_without_symbols.lower().split()
            else:
                tokens = doc_without_symbols.split()
            count_matrix[i] = [
                tokens.count(feature) for feature in self.feature_names
                ]

        return count_matrix

    def get_feature_names(self) -> list[str]:
        return self.feature_names


if __name__ == '__main__':
    corpus1 = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
        ]
    corpus2 = [
        'Мне нравятся данные',
        'Мне очень нравятся данные'
    ]
    corpus3 = [
        'Ave, Caesar, ave!',
        'Morituri te salutant',
        'Caesar: Wow, I am cool dude',
        'Morituri: Oh yeah, very cool guy! Very cool, yeah'
    ]

    vectorizer = CountVectorizer()

    print('1st coprus:')
    count_matrix1 = vectorizer.fit_transform(corpus1)
    print(count_matrix1)
    print(vectorizer.get_feature_names())

    print('2nd coprus:')
    count_matrix2 = vectorizer.fit_transform(corpus2)
    print(count_matrix2)
    print(vectorizer.get_feature_names())

    print('3rd corpus:')
    count_matrix3 = vectorizer.fit_transform(corpus3)
    print(count_matrix3)
    print(vectorizer.get_feature_names())
