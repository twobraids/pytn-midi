from mido import (
    MidiFile,
    MidiTrack
)    

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
        self.pathname = config.pathname
        self.midi_file = MidiFile(self.pathname)
        
        
class FileInputStream(Filestream):
    def __init__(self, config):
        super(self, FileStream).__init__(config)
        self.midi_file = MidiFile(self.pathname)
        
    def __iter__(self):
        for mesage in self.midi_file.play():
            yield message
            
class FileOutputStream(FileStream):
    def __init__(self, config):
        super(self, FileStream).__init__(config)
        self.output_file = MidiFile()
        self.track = MidiTrack()
        self.output_file.append(self.track)
        
    def send(self, message):
        self.output_file.append(message)
        
    def close(self):
        self.output_file.save(self.pathname)
        
class StdInStream(RequiredConfig):
    required_config = Namespace()
    
    def __init__(self, config):
        pass
    
    def __iter__(self):
        for line in input:
            yield

class StdOutStream(RequiredConfig):
    required_config = Namespace()
    
    def __init__(self, config):
        pass
    
    def send(self, message):
        print message.__repr__()
        
    def close(self):
        pass