#!/usr/bin/env python3
from configman import (
    configuration,
    Namespace
)
from configman.converters import (
    class_converter
)

from iostreams import (
    StdInStream,
    StdOutStream
)

from transforms import (
    PassThrough
)

required_config = Namespace()
required_config.namespace("input")
required_config.input.add_option(
    name="implementation",
    default=StdInStream,
    from_string_converter=class_converter
)
required_config.namespace("transform")
required_config.transform.add_option(
    name="implementation",
    default=PassThrough,
    from_string_converter=class_converter
)
required_config.namespace("output")
required_config.output.add_option(
    name="implementation",
    default=StdOutStream,
    from_string_converter=class_converter
)

config = configuration(required_config)

in_stream = config.input.implementation(config.input)
transform = config.transform.implementation(config.transform)
out_stream = config.output.implementation(config.output)

for message in in_stream:
    out_stream.send(transform(message))

out_stream.close()





