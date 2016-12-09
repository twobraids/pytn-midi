from mido import (
    MidiFile,
    MidiTrack,
    Message,
    MetaMessage,
    midifiles,
    parse_string
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

        # The file may contain many tracks. Merge them into a single track,
        # since the pipeline does not care about tracks.
        track = midifiles.tracks.merge_tracks(self.midi_file.tracks)
        self.midi_file.tracks = [track]

    def __iter__(self):
        return iter(self.midi_file.tracks[0])


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


def parse_meta_message(body):
    """ Parse a MetaMessage.

    For example, parse_meta_message("track_name name='Piano left' time=0")
    returns MetaMessage('track_name', name='Piano left', time=0).
    """
    import tokenize, token

    lines = [body]
    def next_line():
        if lines:
            return lines.pop()
        else:
            return ''
    tokens = list(tokenize.generate_tokens(next_line))

    if len(tokens) == 0 or tokens[0][0] != token.NAME:
        raise ValueError("can't parse meta message type: " + body)
    message_type = tokens.pop(0)[1]

    kwargs = {}
    while len(tokens) > 0 and tokens[0][0] != token.ENDMARKER:
        if len(tokens) < 3:
            raise ValueError("unexpected end of line {!r}".format(body))
        if tokens[0][0] != token.NAME:
            raise ValueError("expected key, got {!r} in line {!r}".format(tokens[0][1], body))
        if tokens[1][1] != '=':
            raise ValueError("expected =, got {!r} in line {!r}".format(tokens[1][1], body))
        if tokens[2][0] not in (token.NUMBER, token.STRING):
            raise ValueError("expected number or string, got {!r} in line {!r}".format(tokens[2][1], body))
        name = tokens[0][1]
        value = eval(tokens[2][1])
        kwargs[name] = value
        del tokens[:3]
    return MetaMessage(message_type, **kwargs)


class StdInStream(RequiredConfig):
    required_config = Namespace()

    def __init__(self, config):
        self.config = config

    def __iter__(self):
        for line in sys.stdin:
            line = line.split('#', 1)[0].strip()
            if line.startswith('<message ') and line.endswith('>'):
                yield parse_string(line[9:-1])
            elif line.startswith('<meta message ') and line.endswith('>'):
                yield parse_meta_message(line[14:-1])
            elif line == '':
                pass
            else:
                raise ValueError("unrecognized line: " + repr(line))

class StdOutStream(RequiredConfig):
    required_config = Namespace()

    def __init__(self, config):
        self.config = config

    def send(self, message):
        print (repr(message))

    def close(self):
        pass
