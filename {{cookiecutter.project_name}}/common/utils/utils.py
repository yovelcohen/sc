import functools
import re
from logging import warning
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


def get_view_methods(view, schema=None):
    return [
        getattr(view, item) for item in dir(view) if callable(getattr(view, item)) and (
                item in view.http_method_names
                or item in (schema or view.schema).method_mapping.values()
                or item == 'list'
                or hasattr(getattr(view, item), 'mapping')
        )
    ]


def extend_schema_view(**kwargs):
    """
    Convenience decorator for the "view" kind. Intended for annotating derived view methods that
    are are not directly present in the view (usually methods like ``list`` or ``retrieve``).
    Spares you from overriding methods like ``list``, only to perform a super call in the body
    so that you have have something to attach ``@extend_schema`` to.
    :param kwargs: method names as argument names and ``extend_schema()`` calls as values
    """

    def wrapping_decorator(method_decorator, method):
        @method_decorator
        @functools.wraps(method)
        def wrapped_method(self, request, *args, **kwargs):
            return method(self, request, *args, **kwargs)

        return wrapped_method

    def decorator(view):
        view_methods = {m.__name__: m for m in get_view_methods(view)}

        for method_name, method_decorator in kwargs.items():
            if method_name not in view_methods:
                warning(
                    f'@extend_schema_view argument "{method_name}" was not found on view '
                    f'{view.__name__}. method override for "{method_name}" will be ignored.'
                )
                continue

            method = view_methods[method_name]
            # the context of derived methods must not be altered, as it belongs to the other
            # class. create a new context via the wrapping_decorator so the schema can be safely
            # stored in the wrapped_method. methods belonging to the view can be safely altered.
            if method_name in view.__dict__:
                method_decorator(method)
            else:
                setattr(view, method_name, wrapping_decorator(method_decorator, method))
        return view

    return decorator
