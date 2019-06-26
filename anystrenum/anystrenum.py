import abc
from enum import Enum, EnumMeta, _EnumDict, auto
from typing import List, Callable, AnyStr, Set, TypeVar, Type, Any

SEP_ATTR = "__sep__"
CONVERTER_ATTR = "__converter__"
ITEM_TYPE_ATTR = '__item_type__'


class BaseStrEnumItem(metaclass=abc.ABCMeta):
    sep: AnyStr
    converter: Callable[[AnyStr], AnyStr]

    @abc.abstractmethod
    def __init__(self, sep: AnyStr = None, converter: Callable[[AnyStr], AnyStr] = None):
        self.sep = sep
        self.converter = converter

    @abc.abstractmethod
    def convert(self, name: str) -> AnyStr:
        pass


class BaseAnyStrEnum(Enum):

    @classmethod
    def filter(cls,
               contains: AnyStr = None, *,
               contained_in: AnyStr = None,
               startswith: AnyStr = None,
               endswith: AnyStr = None,
               case_sensitive: bool = False,
               intersection: bool = True,
               inverse: bool = False) -> Set['StrEnum']:
        """
        :param contains: filter all enum members which are contain some substring
        :param startswith: filter all enum members which are start with some substring
        :param endswith: filter all enum members which are end with some substring
        :param contained_in: filter all enum members which are substrings of some string
        :param case_sensitive: defines whether found values must match case of given string
        :param inverse: if True, all enum members except found will be returned
        :param intersection: indicates whether function should return all found objects or their interception

        :return: all found enums
        """

        def prepare(value):
            if case_sensitive:
                return value
            return value.lower()

        found_sets: List[set] = []
        if contains:
            contains = prepare(contains)
            found_sets.append({e for e in cls if contains in prepare(e)})
        if startswith:
            startswith = prepare(startswith)
            found_sets.append({e for e in cls if prepare(e).startswith(startswith)})
        if endswith:
            endswith = prepare(endswith)
            found_sets.append({e for e in cls if prepare(e).endswith(endswith)})
        if contained_in:
            contained_in = prepare(contained_in)
            found_sets.append({e for e in cls if prepare(e) in contained_in})

        if not found_sets:
            return set()

        if intersection:
            found = found_sets[0].intersection(*found_sets[1:])
        else:
            found = found_sets[0].union(*found_sets[1:])

        if inverse:
            return {e for e in cls} - found

        return found

    def _generate_next_value_(*_):
        return auto()


class AnyStrEnumMeta(EnumMeta):
    # It's here to avoid 'got an unexpected keyword argument' TypeError
    @classmethod
    def __prepare__(mcs, *args, sep: AnyStr = None, converter: Callable[[AnyStr], AnyStr] = None, **kwargs):
        return super().__prepare__(*args, **kwargs)

    def __new__(mcs, cls, bases, class_dict, sep: AnyStr = None, converter: Callable[[AnyStr], AnyStr] = None):
        mixin_type, enum_type = mcs._get_mixins_(bases)
        if not issubclass(enum_type, BaseAnyStrEnum):
            raise TypeError(f'Unexpected Enum type \'{enum_type.__name__}\'. '
                            f'Only {BaseAnyStrEnum.__name__} and its subclasses are allowed')
        elif not issubclass(mixin_type, (str, bytes)):
            raise TypeError(f'Unexpected mixin type \'{mixin_type.__name__}\'. '
                            f'Only str, bytes and their subclasses are allowed')

        # Resolving Item class for mixin_type
        item_type = class_dict.get(ITEM_TYPE_ATTR, getattr(enum_type, ITEM_TYPE_ATTR, None))
        if item_type is None:
            raise NotImplementedError(f'{cls} must implement {ITEM_TYPE_ATTR}')
        elif not issubclass(item_type, BaseStrEnumItem):
            raise TypeError(f'{item_type.__name__} must be type of {BaseStrEnumItem.__name__}')

        # Trying to get sep and converter from class dict and base classes
        if sep is None:
            sep = class_dict.get(SEP_ATTR) or getattr(enum_type, SEP_ATTR, None)
        if converter is None:
            converter = class_dict.get(CONVERTER_ATTR) or getattr(enum_type, CONVERTER_ATTR, None)

        item_converter = item_type(sep=sep, converter=converter)

        new_class_dict = _EnumDict()
        for name, type_hint in class_dict.get('__annotations__', {}).items():
            if name.startswith('_') or name in class_dict:
                continue
            mcs.check_type_equals(type_hint, mixin_type)
            value = item_converter.convert(name)
            new_class_dict[name] = value
            mcs.check_type_equals(type(value), mixin_type)

        for name, value in class_dict.items():
            if isinstance(value, BaseStrEnumItem):
                value = value.convert(name)
                mcs.check_type_equals(type(value), mixin_type)
            elif isinstance(value, auto):
                value = item_converter.convert(name)
                mcs.check_type_equals(type(value), mixin_type)

            new_class_dict[name] = value

        new_class_dict[SEP_ATTR] = sep
        new_class_dict[CONVERTER_ATTR] = converter

        return super().__new__(mcs, cls, bases, new_class_dict)

    @staticmethod
    def check_type_equals(type_to_check: Any, allowed_type: Type[Any]):
        if isinstance(type_to_check, TypeVar):
            if len(type_to_check.__constraints__) > 1:
                raise TypeError(f'Only {allowed_type.__name__} is allowed, '
                                f'not {type_to_check} {type_to_check.__constraints__}')

            elif type_to_check.__constraints__[0] is not allowed_type:
                raise TypeError(f'Unexpected type {type_to_check.__constraints__[0].__name__}, '
                                f'allowed type: {allowed_type.__name__}')

        elif type_to_check is not allowed_type:
            raise TypeError(f'Unexpected type {getattr(type_to_check, "__name__", type_to_check)}'
                            f', allowed type: {allowed_type.__name__}')


class StrItem(BaseStrEnumItem):
    # https://youtrack.jetbrains.com/issue/PY-24426
    # noinspection PyMissingConstructor
    def __init__(self, sep: AnyStr = None, converter: Callable[[str], str] = None):
        self.sep = sep
        self.converter = converter

    def convert(self, name: str) -> str:
        if self.converter:
            name = self.converter(name)
        if self.sep:
            name = name.replace('_', self.sep)

        return name


class BytesItem(BaseStrEnumItem):
    # https://youtrack.jetbrains.com/issue/PY-24426
    # noinspection PyMissingConstructor
    def __init__(self, sep: AnyStr = None, converter: Callable[[bytes], bytes] = None):
        self.sep = sep
        self.converter = converter

    def convert(self, name: str) -> bytes:
        name = bytes(name, 'utf8')

        if self.converter:
            name = self.converter(name)
        if self.sep:
            name = name.replace(b'_', self.sep)

        return name


auto_str = StrItem
auto_bytes = BytesItem


class StrEnum(str, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
    __item_type__ = StrItem

    def __str__(self):
        return self.value


class BytesEnum(bytes, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
    __item_type__ = BytesItem

    def __str__(self):
        return str(self.value)
