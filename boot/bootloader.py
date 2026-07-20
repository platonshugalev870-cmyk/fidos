import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sacred.frequencies import DivineFrequency
from kernel.kernel import GodKernel
def bootstrap():
    freq = DivineFrequency()
    freq.calibrate()
    kernel = GodKernel()
    kernel.initialize()
    kernel.boot_sequence()
    return kernel