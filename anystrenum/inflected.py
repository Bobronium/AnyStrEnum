import functools
from typing import Callable

try:
    import inflection
except ImportError:
    raise RuntimeError(f'"inflection" module not found, install it with pip install -U anystrenum[inflection]')

from anystrenum import StrEnum, BytesEnum

__all__ = [
    'CamelizeStrEnum',
    'TitelizeStrEnum',
    'SingularizeStrEnum',
    'DasherizeStrEnum',
    'HumanizeStrEnum',
    'PluralizeStrEnum',
    'TableizeStrEnum',
    'UnderscoreStrEnum',

    'CamelizeByteEnum',
    'DasherizeByteEnum',
    'HumanizeByteEnum',
    'PluralizeByteEnum',
    'SingularizeByteEnum',
    'TableizeByteEnum',
    'TitelizeByteEnum',
    'UnderscoreByteEnum'
]


def to_bytes(func: Callable[[str], str]):
    @functools.wraps(func)
    def new_func(byte_string: bytes):
        return func(byte_string.decode()).encode()

    return new_func


class CamelizeStrEnum(StrEnum):
    __converter__ = inflection.camelize


class TitelizeStrEnum(StrEnum):
    __converter__ = inflection.titleize


class HumanizeStrEnum(StrEnum):
    __converter__ = inflection.humanize


class DasherizeStrEnum(StrEnum):
    __converter__ = inflection.dasherize


class UnderscoreStrEnum(StrEnum):
    __converter__ = inflection.underscore


class PluralizeStrEnum(StrEnum):
    __converter__ = inflection.pluralize


class SingularizeStrEnum(StrEnum):
    __converter__ = inflection.singularize


class TableizeStrEnum(StrEnum):
    __converter__ = inflection.tableize


class CamelizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.camelize)


class TitelizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.titleize)


class HumanizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.humanize)


class DasherizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.dasherize)


class UnderscoreByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.underscore)


class PluralizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.pluralize)


class SingularizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.singularize)


class TableizeByteEnum(BytesEnum):
    __converter__ = to_bytes(inflection.tableize)
