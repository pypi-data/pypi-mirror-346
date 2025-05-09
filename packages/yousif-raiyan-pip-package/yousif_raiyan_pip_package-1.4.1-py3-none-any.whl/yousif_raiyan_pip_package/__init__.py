__version__ = "1.4.1"

from .eeg_graph_representation import EEGGraphProcessor
from .edf_loader import EDFLoader
from .trigger_detector import TriggerDetector

__all__ = ["EEGGraphProcessor",
           "EDFLoader",
           "TriggerDetector"]