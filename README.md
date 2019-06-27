# AnyStrEnum
[![Python 3.7](https://img.shields.io/badge/Python%203.7-blue.svg)](https://python.org) 
[![PyPi Package Version](https://img.shields.io/pypi/v/AnyStrEnum.svg)](https://pypi.python.org/pypi/AnyStrEnum)

Elegant implementation of Enum which inherits from str or bytes
## As simple as this
```python
from anystrenum import StrEnum

class Season(StrEnum):
    spring: str
    summer: str
    autumn: str
    winter: str
    
print(Season.summer)
print(isinstance(Season.summer, str))
# summer
# True
```

# Features
- Easy assignment with type hinting (No need to use auto() or another stubs)
- Automatic name generation with support of custom converters or separators
- Method to filter members (contains, contained_by, startswith, endswith)
- Custom str and bytes types support

# Installation
```bash
$ pip install AnyStrEnum
```

# Examples
## Using custom words separator
To automatically replace all underscores (`_`) in names to something more suitable, use `sep` parameter:
```python
from anystrenum import StrEnum

class Region(StrEnum, sep='-'):
    us_east_1: str
    us_west_1: str
    ca_central_1: str
    cn_northwest_1: str
    eu_central_1: str
    eu_west_1: str
    eu_north_2: str
    sa_east_1: str
    
    
print(Region.us_east_1)
# us-east-1
```

## Using str converter and custom words separator
If you need to apply to your names more changes, you can use `converter` parameter. Pass a function in here which will be called on every member
```python
from anystrenum import StrEnum

class ContentType(StrEnum, converter=lambda s: s.replace('_', '/', 1), sep='-'):
    application_json: str
    application_octet_stream: str
    application_x_json_stream: str
    audio_mpeg: str
    audio_pcm: str
    audio_ogg: str
    
    
print(ContentType.application_octet_stream)
# application/octet-stream
```
As you can see from an example, firstly, names will be converted with our lambda function and then, 
remaining underscores will be replaced with given separator

## Filtering enum members
###### Using enums from previous examples
```python
print(ContentType.filter(contains='-', startswith='a', endswith='m'))
# {<ContentType.application_octet_stream: 'application/octet-stream'>, 
# <ContentType.application_x_json_stream: 'application/x-json-stream'>}

print(ContentType.filter(contained_in='Usually content type for MP3 is audio/mpeg'))
# {<ContentType.audio_mpeg: 'audio/mpeg'>}

print(Region.filter(startswith='eu', endswith='1'))
# {<Region.eu_west_1: 'eu-west-1'>, <Region.eu_central_1: 'eu-central-1'>}
```
