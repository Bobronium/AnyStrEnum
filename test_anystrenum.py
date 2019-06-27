from enum import auto, IntEnum, Enum

import pytest

from anystrenum import StrEnum, BaseAnyStrEnum, BytesEnum, AnyStrEnumMeta, auto_str, StrItem, BytesItem
from anystrenum.inflected import CamelizeByteEnum, CamelizeStrEnum


class Weekday(StrEnum):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


def test_basic_str_enum():
    assert Weekday.monday == 'monday'
    assert Weekday.monday == Weekday.monday.value
    assert isinstance(Weekday.monday, str)
    assert isinstance(Weekday.monday.value, str)
    assert f'Today is {Weekday.monday}' == 'Today is monday'


class CapitalizeStrEnum(StrEnum, converter=lambda s: str.capitalize(s)):
    ...


class CoolGuy(CapitalizeStrEnum):
    pavel: str
    keanu: str
    alex: str
    elon: str
    chuck: str


def test_subclass_with_converter():
    assert CoolGuy.pavel == 'Pavel'
    assert CoolGuy.pavel.startswith('P')


class ChatType(StrEnum):
    private: str
    group: str = auto_str(converter=lambda name: 'super_' + name)


def test_item():
    assert ChatType.group == 'super_group'
    assert ChatType.private == 'private'


class HttpMethod(StrEnum):
    GET = auto()  # You can do that, but it's pointless though. Use 'GET: str' instead
    HEAD: str
    POST: str
    PUT: str
    DELETE: str
    CONNECT: str
    OPTIONS: str
    TRACE: str
    PATCH: str


def test_compatibility_with_irgeek_str_enum():
    assert isinstance(HttpMethod.GET, str)
    assert isinstance(HttpMethod.GET.value, str)
    assert str(HttpMethod.GET) == "GET"

    assert isinstance(HttpMethod.POST, str)
    assert isinstance(HttpMethod.POST.value, str)
    assert str(HttpMethod.POST) == "POST"


class ContentType(StrEnum, converter=lambda s: s.replace('_', '/', 1), sep='-'):
    application_json: str
    application_octet_stream: str
    application_x_json_stream: str
    audio_mpeg: str
    audio_pcm: str
    audio_ogg: str


class BytesContentType(BytesEnum, converter=lambda s: s.replace(b'_', b'/', 1), sep=b'-'):
    application_json: bytes
    application_octet_stream: bytes
    application_x_json_stream: bytes
    audio_mpeg: bytes
    audio_pcm: bytes
    audio_ogg: bytes


def test_converter_and_sep():
    assert ContentType.application_x_json_stream == 'application/x-json-stream'
    assert ContentType.audio_mpeg == 'audio/mpeg'


def test_search():
    expected_result = {ContentType.application_octet_stream, ContentType.application_x_json_stream}
    assert ContentType.filter(startswith='a', contains='-', endswith='m') == expected_result

    expected_result = {ContentType.audio_mpeg, ContentType.audio_ogg, ContentType.audio_pcm}
    assert ContentType.filter(startswith='app', inverse=True) == expected_result

    expected_result = {ContentType.audio_mpeg}
    assert ContentType.filter(contained_in='Usually content type for MP3 audio is audio/mpeg') == expected_result

    expected_result = {BytesContentType.application_octet_stream, BytesContentType.application_x_json_stream}
    assert BytesContentType.filter(startswith=b'a', contains=b'-', endswith=b'm') == expected_result

    expected_result = {BytesContentType.audio_mpeg, BytesContentType.audio_ogg, BytesContentType.audio_pcm}
    assert BytesContentType.filter(startswith=b'app', inverse=True) == expected_result

    expected_result = {BytesContentType.audio_mpeg}
    assert BytesContentType.filter(contained_in=b'Usually content type for MP3 audio is audio/mpeg') == expected_result


def test_wrong_member_types():
    with pytest.raises(TypeError) as e:
        class FakeShinyStrEnum(StrEnum):
            foo: MyShinyStr  # This line will cause an exception

        print(FakeShinyStrEnum)
    assert str(e.value) == "Unexpected type MyShinyStr, allowed type: str"

    with pytest.raises(TypeError) as e:
        class FakeShinyBytesEnum(BytesEnum):
            bar: MyShinyBytes  # This line will cause an exception

        print(FakeShinyBytesEnum)
    assert str(e.value) == "Unexpected type MyShinyBytes, allowed type: bytes"

    with pytest.raises(TypeError) as e:
        class MyShinyBytesStrEnum(MyShinyBytes, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
            __item_type__ = StrItem
            oh_noo: MyShinyStr  # Still can't do this

        print(MyShinyBytesStrEnum)
    assert str(e.value) == 'Unexpected type MyShinyStr, allowed type: MyShinyBytes'

    with pytest.raises(TypeError) as e:
        class MyShinyBytesStrEnum(MyShinyBytes, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
            __item_type__ = BytesItem
            oh_noo: bytes  # And this

        print(MyShinyBytesStrEnum)
    assert str(e.value) == 'Unexpected type bytes, allowed type: MyShinyBytes'


class MyShinyStr(str):
    def shout(self):
        return self.upper() + '!!!'


class MyShinyBytes(bytes):
    def shout(self):
        return self.upper() + b'!!!'


class MyShinyStrItem(StrItem):
    def generate_value(self, name: str) -> MyShinyStr:
        return MyShinyStr(super().generate_value(name))


class MyShinyBytesItem(BytesItem):
    def generate_value(self, name: str) -> MyShinyBytes:
        return MyShinyBytes(super().generate_value(name))


class MyShinyStrEnum(MyShinyStr, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
    __item_type__ = MyShinyStrItem


class StrFooBar(MyShinyStrEnum):
    foo: MyShinyStr
    bar: MyShinyStr


class MyShinyBytesEnum(MyShinyBytes, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
    __item_type__ = MyShinyBytesItem


class BytesFooBar(MyShinyBytesEnum):
    foo: MyShinyBytes
    bar: MyShinyBytes


def test_custom_member_types():
    assert isinstance(StrFooBar.foo, MyShinyStr)
    assert isinstance(StrFooBar.foo, str)
    assert StrFooBar.foo.shout() == 'FOO!!!'

    assert isinstance(BytesFooBar.bar, MyShinyBytes)
    assert isinstance(BytesFooBar.bar, bytes)
    assert BytesFooBar.bar == b'bar'
    assert BytesFooBar.bar.shout() == b'BAR!!!'


def test_wrong_mixins():
    for unexpected_mixin in (bool, list, set, bytearray, frozenset, dict, object, pytest.Item):
        mixin_name = unexpected_mixin.__name__
        expected_message = f"Unexpected mixin type '{mixin_name}'. Only str, bytes and their subclasses are allowed"

        with pytest.raises(TypeError) as e:
            class MyStrEnum(unexpected_mixin, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
                ...

            print(MyStrEnum)
        assert str(e.value) == expected_message

        with pytest.raises(TypeError) as e:
            class MyBytesEnum(unexpected_mixin, BaseAnyStrEnum, metaclass=AnyStrEnumMeta):
                ...

            print(MyBytesEnum)
        assert str(e.value) == expected_message

    for unexpected_enum in (IntEnum, Enum):
        enum_name = unexpected_enum.__name__
        with pytest.raises(TypeError) as e:
            class MyStrEnum(str, unexpected_enum, metaclass=AnyStrEnumMeta):
                pass

            print(MyStrEnum)
        assert str(
            e.value
        ) == f'Unexpected Enum type \'{enum_name}\'. Only BaseAnyStrEnum and its subclasses are allowed'
