import re
from pprint import pprint
from typing import Type

from django.db.models import IntegerField, Model, Field
from django.db.models.query import QuerySet

from api.models import Account


def marker_wrapper_printer(*args):
    for arg in args:
        print('*' * 20)
        pprint(arg)
        print('*' * 20)


def dynamically_aggregate_query_set(model: Type[Model], qs, func, field_type: Type[Field] = IntegerField, exclude=None):
    """
    dynamic aggregation on a queryset, will aggregate the given function on all fields of the given type on the given
    queryset with excluding option.

    :param model: the model to aggregate on
    :param field_type: filter fields of the query set by field type this, defaults to Integer Field
    :param qs: queryset to perform aggregation on
    :param func: Aggregation function to apply
    :param exclude: fields names to exclude
    """
    exclude_fields = exclude if exclude else []
    model_fields = model._meta.get_fields()

    int_fields = [field for field in model_fields if isinstance(field, field_type)
                  and field.name not in exclude_fields]

    aggregation_fields = dict([(f'{field.name}_{func.__name__.lower()}', func(f'{field.name}'))
                               for field in int_fields])

    return qs.aggregate(**aggregation_fields)


conversion_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def convert_camel_to_snake_case(key: str, remove_white_space=False):
    """
    converts a camel cased string to snake cased
    """
    name = conversion_pattern.sub('_', key).lower()
    return name if remove_white_space is False else name.replace(' ', '')


def convert_dict_keys_to_camel_case(obj):
    data = {convert_camel_to_snake_case(k): v for k, v in obj.items()}
    return data


def get_all_accounts() -> QuerySet[Account]:
    return Account.objects.all()
