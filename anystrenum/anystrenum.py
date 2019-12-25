import abc
from enum import Enum as FastEnum, EnumMeta, _EnumDict, auto
from enum import Enum
from typing import List, Callable, AnyStr, Set, Type, Any

VALUES_GENERATOR_ATTR = '__values_generator__'


class BaseTypedEnum(Enum):
    __values_generator__: Callable[[str], Any]


class TypedEnumMeta(EnumMeta):
    # It's here to avoid 'got an unexpected keyword argument' TypeError
    @classmethod
    def __prepare__(mcs, *args, converter: Callable[[AnyStr], AnyStr] = None, **kwargs):
        return super().__prepare__(*args, **kwargs)

    def __new__(mcs, cls, bases, class_dict, converter: Callable[[AnyStr], AnyStr] = None):
        mixin_type, base_enum = mcs._get_mixins_(bases)
        if not issubclass(base_enum, BaseTypedEnum):
            raise TypeError(f'Unexpected Enum type \'{base_enum.__name__}\'. '
                            f'Only {BaseTypedEnum.__name__} and its subclasses are allowed')

        for name, type_hint in class_dict.get('__annotations__', {}).items():
            if name.startswith('_'):
                continue
            mcs.check_type_equals(type_hint, mixin_type)
            if name not in class_dict:
                class_dict[name] = auto()  # so it will be processed in _generate_next_value_

        return super().__new__(mcs, cls, bases, new_class_dict)

    @staticmethod
    def check_type_equals(type_to_check: Any, allowed_type: Type[Any]):
        if type_to_check is not allowed_type:
            raise TypeError(f'Unexpected type {getattr(type_to_check, "__name__", type_to_check)}'
                            f', allowed type: {allowed_type.__name__}')

    @staticmethod
    def _get_mixins_(bases):
        """
        Returns true member_type
        """
        if not bases:
            return object, Enum

        def _find_data_type(bases):
            for chain in bases:
                for base in chain.__mro__:
                    if base is object:
                        continue
                    # changed from 'elif '__new__' in base.__dict__`, as it was skipping subclasses of base type
                    elif hasattr(base, '__new__') and not issubclass(base, Enum):
                        return base

        # ensure final parent class is an Enum derivative, find any concrete
        # data type, and check that Enum has no members
        first_enum = bases[-1]
        if not issubclass(first_enum, Enum):
            raise TypeError("new enumerations should be created as "
                            "`EnumName([mixin_type, ...] [data_type,] enum_type)`")
        member_type = _find_data_type(bases) or object
        if first_enum._member_names_:
            raise TypeError("Cannot extend enumerations")
        return member_type, first_enum


class BaseAnyStrEnum(BaseTypedEnum):
    __values_generator__: Callable[[str], AnyStr] = None

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


class StrEnum(str, BaseAnyStrEnum, metaclass=TypedEnumMeta):
    __values_generator__: Callable[[str], str] = None

    @classmethod
    def _generate_next_value_(cls, name, *_):
        if cls.__values_generator__ is not None:
            return cls.__values_generator__(name)
        return name

    def __str__(self):
        return self.value


class BytesEnum(bytes, BaseAnyStrEnum, metaclass=TypedEnumMeta):
    __values_generator__: Callable[[bytes], bytes] = None

    def __str__(self):
        return str(self.value)

    @classmethod
    def _generate_next_value_(cls, name, *_):
        name = bytes(name, 'utf-8')

        if cls.__values_generator__ is not None:
            name = cls.__values_generator__(name)
        return name


class IntEnum(int, BaseTypedEnum, metaclass=TypedEnumMeta):
    __values_generator__: Callable[[str, ...], int] = None
