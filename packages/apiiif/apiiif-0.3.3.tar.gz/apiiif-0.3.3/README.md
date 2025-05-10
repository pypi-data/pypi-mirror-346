# apiiif

[![PyPI - Version](https://img.shields.io/pypi/v/apiiif.svg)](https://pypi.org/project/apiiif)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/apiiif.svg)](https://pypi.org/project/apiiif)

---

`apiiif` is a IIIF Presentation API 3.0 library inspired by the excellent [iiif-prezi3](https://github.com/iiif-prezi/iiif-prezi3) library.

This has been developed primarily for use on [CSNTM's upcoming image website](https://collections.csntm.org) and, therefore, has a few requirements that make it more suitable than other solutions:

- We need a library with comprehensive IDE support.
  - no monkey patching
  - consistent type-hinting
  - No code-gen
- simple useage
  - currently supports only the creation of IIIF presentation resources
  - does not consume resources
- uses [pydantic](https://github.com/pydantic/pydantic) for modeling and serialization.

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install apiiif
```

## License

`apiiif` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
