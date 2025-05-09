__version__ = "1.3.1"

from .eeg_graph_representation import EEGGraphProcessor
from .edf_loader import EDFLoader

__all__ = ["EEGGraphProcessor",
           "EDFLoader",]