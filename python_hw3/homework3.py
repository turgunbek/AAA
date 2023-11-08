from string import punctuation
from numpy import log
from numpy import round as np_round


class CountVectorizer:
    """ Класс для работы с текстовым корпусом.
    ==========================================================================
    Содержит 3 атрибута (экземпляра):

    lowercase = True (default), если приводим все токены к нижнему регистру,
                иначе оставляем текст как есть
    dict_tokens - словарь для отображения токенов в индексы
    feature_names - список для хранения имён признаков

    ==========================================================================
    А также содержит 4 метода (экземпляра):

    __clear_corpus_from_specsymbols()
    __make_dict_tokens()
    fit_transform()
    get_feature_names()
    """

    def __init__(self, lowercase: bool = True):
        self.lowercase = lowercase  # по дефолту все токены -> в нижний регистр
        self.dict_tokens = {}  # Словарь для отображения токенов в индексы
        self.feature_names = []  # Список для хранения имен признаков

    def __clear_corpus_from_specsymbols(self, corpus: list[str]) -> list[str]:
        """приватный метод, служащий для очискти входного корпуса слов
        от спецсимволов: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        """
        corpus_cleaned = [
            document.translate(str.maketrans('', '', punctuation))
            for document in corpus
            ]
        return corpus_cleaned

    def __make_dict_tokens(self, corpus: list[str]) -> dict[str]:
        """приватный метод, создаёт словарь с ключами из
        уникальных токенов и значениями из чисел 0,1,2,..
        """
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

    def fit_transform(self, corpus: list[str]) -> list[list[int]]:
        """возвращает терм-документную матрицу.
        Подразумевается вызов этого метода до вызова метода get_feature_names()
        (также как и в классе sklearn.feature_extraction.text.CountVectorizer)
        """
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
                str.maketrans('', '', punctuation))
            if self.lowercase:
                tokens = doc_without_symbols.lower().split()
            else:
                tokens = doc_without_symbols.split()
            count_matrix[i] = [
                tokens.count(feature) for feature in self.feature_names
                ]

        return count_matrix

    def get_feature_names(self) -> list[str]:
        """возвращает имена всех уникальных токенов, причём
        функция не подразумевает входных аргументов, и поэтому будет возвращать
        список токенов, полученных с последнего вызова fit_transform()
        (Т.е. метод работает по аналогии с оригинальным классом
        sklearn.feature_extraction.text.CountVectorizer)
        Если же предварительно fit_transform() не вызван, то выведет
        соответствующее сообщение.
        """
        if self.feature_names:
            return self.feature_names
        else:
            print('There is no any features! Firstly get fit_transform()!')

    def tf_transform(self, corpus: list[str]) -> list[list[float]]:
        """возращает tf_matrix (term-frequency) заданного корпуса слов
        """
        count_matrix = self.fit_transform(corpus)
        return [[el/sum(line) for el in line] for line in count_matrix]

    def idf_transform(self, corpus: list[str]) -> list[float]:
        """возвращает idf_matrix (inverse document-frequency) корпуса слов
        """
        count_matrix = self.fit_transform(corpus)
        n_docs = len(count_matrix)
        res = []
        for row in zip(*count_matrix):
            counter = sum(int(num > 0) for num in row)
            res.append(log((n_docs + 1) / (counter + 1)) + 1)
        return res


class TfidfTransformer:
    """ Класс для работы с tf, idf матрицами.
    ==========================================================================
    Содержит метод (экземпляра) fit_transform():
    """

    def fit_transform(self, countmatrix: list[list[int]]) -> list[list[float]]:
        """возвращает tfidf = tf * idf заданной матрицы countmatrix
        """
        n_docs = len(countmatrix)
        n_tokens = len(countmatrix[0])
        tf = [[el/sum(line) for el in line] for line in countmatrix]
        idf = []
        for row in zip(*countmatrix):
            counter = sum(int(num > 0) for num in row)
            idf.append(log((n_docs + 1) / (counter + 1)) + 1)
        tfidf_matrix = []
        for k in range(n_docs):
            tfidf_matrix.append([tf[k][i] * idf[i] for i in range(n_tokens)])
        return tfidf_matrix


class TfidfVectorizer(CountVectorizer):
    """ Класс, наследующий CountVectorizer, и композитный с TfidfTransformer
    ==========================================================================
    Переопределяет метод (экземпляра) fit_transform()
    """
    def __init__(self, tf_class=TfidfTransformer, lowercase=True):
        super().__init__(lowercase=lowercase)
        self.transformer = tf_class()

    def fit_transform(self, corpus: list[str]) -> list[list[float]]:
        count_matrix_numbers = super().fit_transform(corpus)
        return self.transformer.fit_transform(count_matrix_numbers)


if __name__ == '__main__':
    print('Задания #1-2-3: CountVectorizer: ', end='')
    print('fit_transform(), tf_transform(), idf_transform()')

    corpus1 = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
        ]
    corpus2 = [
        'Мне нравятся данные',
        'Мне очень нравятся данные',
        'особенно большие данные',
        'Здесь просто проверка на кириллицу'
    ]
    corpus3 = [
        'Ave, Caesar, ave!',
        'Morituri te salutant!!!',
        'Caesar: Wow, I am cool dude',
        'Morituri: Oh yeah, very cool guy! Very cool, yeah'
    ]

    corpuses = [corpus1, corpus2, corpus3]

    vectorizer = CountVectorizer()

    for i, corpus in enumerate(corpuses):
        print(f'coprus #{i + 1}:')
        count_matrix = vectorizer.fit_transform(corpus)
        tf_matrix = vectorizer.tf_transform(corpus)
        idf_matrix = vectorizer.idf_transform(corpus)
        print(count_matrix)
        print(vectorizer.get_feature_names())
        print(np_round(tf_matrix, 3))
        print(np_round(idf_matrix, 3))
        print()

    print('Задание #4: TfidfTransformer().fit_transform()')
    count_matrix = [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    ]
    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(count_matrix)
    print(np_round(tfidf_matrix, 3))
    print()

    print('Задание #5: TfidfVectorizer().fit_transform()')
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer_tfid = TfidfVectorizer()
    tfidf_matrix = vectorizer_tfid.fit_transform(corpus)
    print(vectorizer_tfid.get_feature_names())
    print(np_round(tfidf_matrix, 3))
