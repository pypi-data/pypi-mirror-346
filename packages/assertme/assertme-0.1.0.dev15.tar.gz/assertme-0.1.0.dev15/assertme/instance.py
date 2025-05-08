from typing import Annotated, Type

from pydantic import Strict

from assertme.pydantic import WithPydantic


class InstanceOf(WithPydantic):
    instance_type: Type | tuple[Type]

    def __init__(self, instance_type: Type | tuple[Type]):
        super().__init__(Annotated[instance_type, Strict])
