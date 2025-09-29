# Декоратор
# — это вызываемый объект, который позволяет изменить поведение функции (до применения или после), не меняя ее кода.

# Декоратор принимает на вход вызываемый объект и возвращает вызываемый объект.

# Важно помнить что:
# - функции являются объектами — они могут быть присвоены переменным, переданы другим функциям и возвращены из них;
# - функции могут быть определены внутри других функций, и дочерняя функция может захватывать локальное
#   состояние родительской функции (лексическое замыкание)

import inspect
import time


# Самый простой декоратор может выглядеть так, декоратор принимает на вход функцию и ее же отдает:
def null_decorator(func):
    decorator_name = inspect.currentframe().f_code.co_name
    print(f"Мы в декораторе {decorator_name}!")
    return func


@null_decorator
def foo():
    function_name = inspect.currentframe().f_code.co_name
    print(f"Сейчас выполняется функция {function_name}")


foo()


# Если убрать синтаксический сахар в виде @null_decorator, то получится, что мы сначала определяем функцию,
# а потом применяем к ней декоратор (то есть применяем декоратор динамически)
def greet():  # шаг 1 - определяем функцию
    function_name = inspect.currentframe().f_code.co_name
    print(f"Сейчас выполняется функция {function_name}")
    return "Здарова, бандиты!"


yet_another_greet = null_decorator(greet)  # шаг 2 - применяем декоратор
yet_another_greet()


# Идем дальше, видим более полезный декоратор @benchmark_decorator, который считает время выполнения функции
# и показывает результат выполнения функции:

def benchmark_decorator(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f"Время выполнения: {end - start} секунд. Результат выполнения: {result}")
        return result
    return wrapper


@benchmark_decorator
def yet_another_greet():
    function_name = inspect.currentframe().f_code.co_name
    print(f"Сейчас выполняется функция {function_name}")
    return "Здарова, бандиты!"


yet_another_greet()


# А теперь мы применяем декоратор benchmark_decorator динамически, без синтаксического сахара
def one_more_yet_another_greet():
    function_name = inspect.currentframe().f_code.co_name
    print(f"Сейчас выполняется функция {function_name}")
    return "Здарова, бандиты!"


# То есть benchmark_decorator сначала отдаст wrapper, не выполняя его
wrapper_for_one_more_yet_another_greet = benchmark_decorator(one_more_yet_another_greet)
# И вот теперь выполним wrapper
wrapper_for_one_more_yet_another_greet()


# А теперь ситуация, когда функция принимает аргументы:

def useful_decorator(func):
    # Сюда передается функция (func, то есть get_sum_of_two_elements), она еще не
    # вызывалась, аргументы не будут видны

    def wrapper(*args, **kwargs):
        print(f"Подготовка к выполнению функции: {func.__name__}")
        res = func(*args, **kwargs)  # Прокидываем args и kwargs
        print(f"Функция {func.__name__} выполнена")
        return res
    return wrapper


@useful_decorator
def get_sum_of_two_elements(a, b):
    function_name = inspect.currentframe().f_code.co_name
    sum_of_two_elements = a + b
    print(f"Результат выполнения функции {function_name}: {sum_of_two_elements}")
    return sum_of_two_elements


get_sum_of_two_elements(3, 4)

# Если бы мы динамически применяли декоратор, это выглядело бы так:
# wrapper = useful_decorator(get_sum_of_two_elements)
# wrapper(3, 4)


# И еще пример декоратора, теперь - параметризованный:
def top_layer(limit):  # вызов функции top_layer вернет функцию middle_layer
    def middle_layer(func):  # вызов функции middle_layer вернет функцию wrapper
        def wrapper(*args, **kwargs):  # вызов функции wrapper вернет функцию result_array
            result_array = []

            while wrapper.calls_count < limit:
                wrapper.calls_count += 1
                sum_res = func(*args, **kwargs)
                result_array.append(sum_res)

            return result_array

        wrapper.calls_count = 0  # Чтобы позже увидеть фактическое количество вызовов функции
        return wrapper

    return middle_layer


@top_layer(3)  # Хотим, чтобы функция вызывалась 3 раза
def get_sum_of_two_elements(a, b):
    function_name = inspect.currentframe().f_code.co_name
    sum_of_two_elements = a + b
    print(f"Результат выполнения {function_name}: {sum_of_two_elements}")
    return sum_of_two_elements


func_result = get_sum_of_two_elements(5, 6)
print(func_result)

# Проверяем сколько раз вызывалась функция
assert get_sum_of_two_elements.calls_count == 3

# Если бы мы динамически применяли декоратор, это выглядело бы так:
# middle_layer = top_layer(3)
# wrapper = middle_layer(get_sum_of_two_elements)
# func_result = wrapper(3, 3)

# Или вот так, поскольку мы хотим знать количество вызовов функции
# wrapper = top_layer(3)(get_sum_of_two_elements)
# func_result = wrapper(3, 3)

# print(func_result)
# assert wrapper.calls_count == 3
