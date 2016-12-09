from mido import (
    MidiFile,
    MidiTrack,
    Message
)
import sys

from configman import (
    Namespace,
    RequiredConfig
)

class FileStream(RequiredConfig):
    required_config = Namespace()
    required_config.add_option(
        name="pathname"
    )

    def __init__(self, config):
        self.config = config
        self.pathname = config.pathname


class FileInputStream(FileStream):
    def __init__(self, config):
        super(FileInputStream, self).__init__(config)
        self.midi_file = MidiFile(self.pathname)

    def __iter__(self):
        for message in self.midi_file.play():
            yield message


class FileOutputStream(FileStream):
    def __init__(self, config):
        super(FileOutputStream, self).__init__(config)
        self.output_file = MidiFile()
        self.track = MidiTrack()
        self.output_file.tracks.append(self.track)

    def send(self, message):
        self.track.append(message)

    def close(self):
        self.output_file.save(self.pathname)


class StdInStream(RequiredConfig):
    required_config = Namespace()

    def __init__(self, config):
        self.config = config

    def __iter__(self):
        for line in sys.stdin:
            line = line.strip().strip(">")
            parts = line.split(" ")
            message_type = parts[1]
            kwargs = {}
            for key_value in parts[2:]:
                key, value = key_value.split("=")
                if value[-1] == ">":
                    value = value[:-1]
                kwargs[key] = int(value)
            yield Message(message_type, **kwargs)


class StdOutStream(RequiredConfig):
    required_config = Namespace()

    def __init__(self, config):
        self.config = config

    def send(self, message):
        print (repr(message))

    def close(self):
        pass

from mido.sockets import (
    PortServer,
    connect
)

class NetworkStream(RequiredConfig):
    required_config = Namespace()
    required_config.add_option(
        name="port",
        default=9000,
    )
    required_config.add_option(
        name="host",
        default="localhost",
    )

    def __init__(self, config):
        self.config = config
        self.host = config.host
        self.port = config.port


class NetworkInStream(NetworkStream):

    def __init__(self, config):
        super(NetworkInStream, self).__init__(config)
        self.server = PortServer(self.host, self.port)

    def __iter__(self):
        for message in self.server:
            yield message


class NetworkOutStream(NetworkStream):

    def __init__(self, config):
        super(NetworkOutStream, self).__init__(config)
        self.connection = connect(self.host, self.port)

    def send(self, message):
        self.connection.send(message)

    def close(self):
        self.connection.close()