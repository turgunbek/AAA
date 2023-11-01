# Домашнее задание №4 по теме "Тестирование"
Здесь описано вкратце то, что было сделано, и то как запускать тесты.

## issue-01

Запускать в командной строке (терминале) (из директории, где находится этот файл "issue_01.py"), выполнив команду <div style="background-color: lightgray">python -m doctest -o NORMALIZE_WHITESPACE -v issue_01.py</div>

Как и написано в DoD, здесь имеются:

&bull; используется директива &mdash; на 1й тест использована директива ELLIPSIS

&bull; используется флаг &mdash; при запуске из командной строки использован флаг NORMALIZE_WHITESPACE

&bull; тест с message = 'SOS' &mdash; это 2й тест, видна работа флага NORMALIZE_WHITESPACE - игнорит лишние пробелы

&bull; тест с исклечением (Exception) &mdash; это последний тест, обработан случай отсутствия символа в азбуке Морзе


В файле "result issue_01.txt" приведен фрагмент из терминала с  командами и результатами запуска.

## issue-02

Запускать в командной строке (из директории, где находится этот файл "issue_02.py"), выполнив команду <div style="background-color: lightgray">python -m pytest -v .\issue_02.py</div>

Как и написано в DoD, здесь имеются минимум 3 теста.
Также здесь добавлен тест для обработки исключения <font color="gray">AssertionError</font>. Для этого в декортатор <font color="orange">@pytest.mark.parametrize()</font> передается
аргумент </font color="blue">expects_exceptions</font> булева типа со значением <font color="red">True</font> в случае возникновения <font color="gray">AssertionError</font>.

В файле "result issue_02.txt" приведен фрагмент из терминала с  командами и результатами запуска.
