from configman import (
    configuration,
    Namespace
)
from configman.converter import (
    classConverter
)

required_config = Namespace()
required_config.add_option(
    name="input.implementation",
    from_string_converted=classConverter
)
required_config.add_option(
    name="transform.implemenation",
    from_string_converted=classConverter
)
required_config.add_option(
    name="output.implementation",
    from_string_converted=classConverter
)

config = configuration(required_config)

in_stream = config.input.implementation(config.input)
transform = config.transform.implementation(config.transform)
out_stream = config.output.implementation(config.output)

for message in in_stream:
    out_stream(transform(message))
    
    
    
    
    