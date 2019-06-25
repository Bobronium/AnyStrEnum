# StrEnum
[![Python 3.7](https://img.shields.io/badge/Python%203.7-blue.svg)](https://python.org) 
[![PyPi Package Version](https://img.shields.io/pypi/v/AnyStrEnum.svg)](https://pypi.python.org/pypi/AnyStrEnum)

Elegant implementation of Enum which inherits from str or bytes
 
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

##Using custom words separator
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
    
    
print(f'If you just specify the general endpoint,\n'
      f'Amazon directs your request to the {Region.us_east_1} endpoint')
# If you just specify the general endpoint, 
# Amazon directs your request to the us-east-1 endpoint'
```

##Using str converter and custom words separator
```python
from anystrenum import StrEnum

class ContentType(StrEnum, converter=lambda s: s.replace('_', '/', 1), sep='-'):
    application_json: str
    application_octet_stream: str
    application_x_json_stream: str
    audio_mpeg: str
    audio_pcm: str
    audio_ogg: str
    
    
print(f'In RFC 2046 "{ContentType.application_octet_stream}"" is defined as "arbitrary binary data"')
# In RFC 2046 "application/octet-stream" is defined as "arbitrary binary data"# 
```
As you can see from an example, first the name will be converted with our lambda function and then, 
remaining underscores will be replaced with given separator

## Filtering enum members
######Using enums from previous examples
```python
print(*ContentType.filter(contains='-', startswith='a', endswith='m'), sep=', ')
# application/octet-stream, application/x-json-stream

print(*ContentType.filter(contained_in='Usually content type for MP3 audio is audio/mpeg'))
# audio/mpeg

print(*Region.filter(startswith='eu', endswith='1'), sep=', ')
# eu-central-1, eu-west-1
```