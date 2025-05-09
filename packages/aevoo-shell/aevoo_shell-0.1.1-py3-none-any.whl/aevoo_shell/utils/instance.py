from __future__ import annotations

import gzip
import os
from base64 import b64decode
from typing import TYPE_CHECKING

from aevoo_tosca.v2.properties_attributes_parameters.parameter import (
    ParameterDefinition,
)

if TYPE_CHECKING:
    from aevoo_tosca.v2.properties_attributes_parameters.schema import (
        SchemaDefinition,
    )


def data_parse(data, details: ParameterDefinition | SchemaDefinition):
    if details.type in ("yaml", "string"):
        if isinstance(data, bytes):
            data = data.decode()
        return data
    if details.type == "b64":
        data = b64decode(data)
    elif details.type == "gzip":
        data = gzip.decompress(data)
    if details.entry_schema is not None:
        return data_parse(data, details.entry_schema)


def secret_write_to(
    details,
    secret: str,
    file: str,
):
    if os.path.exists(file):
        raise Exception("file exist")
    if not os.path.exists(os.path.dirname(file)):
        raise Exception("Directory not exist")

    details = ParameterDefinition(**details)
    secret = data_parse(secret, details)
    with open(file, "w") as f:
        f.write(secret)
