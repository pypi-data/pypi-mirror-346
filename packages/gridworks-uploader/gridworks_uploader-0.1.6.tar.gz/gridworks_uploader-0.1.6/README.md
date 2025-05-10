# Gridworks Uploader

[![PyPI](https://img.shields.io/pypi/v/gridworks-uploader.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/gridworks-uploader.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-uploader)][python version]
[![License](https://img.shields.io/pypi/l/gridworks-uploader)][license]

[![Read the documentation at https://gridworks-uploader.readthedocs.io/](https://img.shields.io/readthedocs/gridworks-uploader/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/SmoothStoneComputing/gridworks-uploader/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/SmoothStoneComputing/gridworks-uploader/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]

[pypi_]: https://pypi.org/project/gridworks-uploader/
[status]: https://pypi.org/project/gridworks-uploader/
[python version]: https://pypi.org/project/gridworks-uploader
[read the docs]: https://gridworks-uploader.readthedocs.io/
[tests]: https://github.com/SmoothStoneComputing/gridworks-uploader/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/anschweitzer/gridworks-uploader
[pre-commit]: https://github.com/pre-commit/pre-commit

This package provides a reliable upload service using the [gridworks-protocol]. 

The upload services communicates upstream using MQTT. Clients deliver data to
the service for reliable delivery using http. For [example](./src/gwupload/stubs/client/client.py): 

```python
    import random
    import time
    from typing import Literal
    
    import httpx
    from gwproto.messages import EventBase
    
    
    class SomeData(EventBase):
        TimestampUTC: float
        Reading: float
        TypeName: Literal["gridworks.event.some.data"] = "gridworks.event.some.data"
    
    
    if __name__ == "__main__":
        httpx.post(
            "http://127.0.0.1:8080/events",
            json=SomeData(
                TimestampUTC=round(time.time(), 3),
                Reading=round(random.random(), 3),
            ).model_dump(),
        )
```

## Experimentation

To experiment with this package you must run the upload service, and, if you
want to watch your messages delivered to a stub ingester, you must also run an
MQTT broker and the stub ingester. 

To set up the MQTT broker, follow the [gridworks-proactor instructions].

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv tool install -p 3.12 poetry=1.8.5
git clone https://github.com/SmoothStoneComputing/gridworks-uploader.git
cd gridworks-uploader
```
Create a `.env` file in the base direcory of the repo with the contents:  

```
UPLOADER_APP_lONG_NAME = "test.uploader"
UPLOADER_APP_INGESTER_LONG_NAME = "test.ingester"
STUB_INGESTER_APP_lONG_NAME = "test.ingester"
STUB_INGESTER_APP_UPLOADER_LONG_NAME = "test.uploader"
```

Then run these commands 

```shell
poetry install --sync --with dev
poetry shell
gwcert ca create test-ca
gwup gen-test-certs
gwup stubs ingester gen-test-certs

# Open 3 terminals. In each terminal, cd to the gridworks-uploader repo and 
# run: 
poetry shell 

# In the ingester terminal run: 
gwup stubs ingester run --log-events

# In the uploader terminal run: 
gwup run --message-summary

# In the client terminal run:
gwup stubs client run 
# OR
python src/gwupload/stubs/client/client.py 
```


## Features

- TODO

## Requirements

- TODO

## Installation

You can install _Gridworks Uploader_ via [pip] from [PyPI]:

```console
$ pip install gridworks-uploader
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Gridworks Uploader_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/SmoothStoneComputing/gridworks-uploader/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/SmoothStoneComputing/gridworks-uploader/blob/dev/LICENSE
[contributor guide]: https://github.com/SmoothStoneComputing/gridworks-uploader/blob/main/CONTRIBUTING.md
[command-line reference]: https://gridworks-uploader.readthedocs.io/en/latest/usage.html


[gridworks-protocol]: https://github.com/thegridelectric/gridworks-protocol 
[gridworks-proactor instructions]: https://github.com/SmoothStoneComputing/gridworks-proactor/tree/2.X/has-a?tab=readme-ov-file#requirements