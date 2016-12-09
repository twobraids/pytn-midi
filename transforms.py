from configman import (
    Namespace,
    RequiredConfig
)


class PassThrough(RequiredConfig):
    required_config = Namespace()

    def __init__(self, config):
        self.config = config

    def __call__(self, message):
        return message

