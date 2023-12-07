import collections
import numpy as np

def freq_values(props, prop):

    """
    Подсчитывает частоту встречаемости значений необходимого поля
    """

    properties_count = dict(collections.Counter(props))
    items = []
    for p in set(props):
        item = dict()
        item[prop] = p
        item['count'] = properties_count[p]
        items.append(item)

    return items

def count_stats(values):

    '''
    Принимает список значений, возвращает словарь с результатами вычислений суммы значений,
    минимального и максимального значений, среднего арифметического значения и стандартного отклонения
    '''

    stats = {
        'sum_value': round(sum(values), 1),
        'min_value': min(values),
        'max_value': max(values),
        'average_value': round(np.mean(values), 2)
    }
    return stats