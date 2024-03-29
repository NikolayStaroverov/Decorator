import os
import datetime


def logger(path):
    def _logger_(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a') as f:
                start_date_time = datetime.datetime.now()
                start_day = start_date_time.date()
                start_time = start_date_time.time()
                result = old_function(*args, **kwargs)
                res_text = " ". join((old_function.__name__, str(args), str(kwargs), str(result), str(start_day), str(start_time)))
                f.write(res_text+'\n')
                return result
        return new_function
    return _logger_
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger(path)
    def hello_world():
        return 'Hello World'

    @logger(path)
    def summator(a, b=0):
        return a + b

    @logger(path)
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
