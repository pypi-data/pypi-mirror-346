"""
slide/_slide
~~~~~~~~~~~~
"""

from ._analysis import AnalysisLoader
from ._annotation import AnnotationIO
from ._input import InputIO
from ._log import params, set_global_verbosity


class SLIDE(InputIO, AnnotationIO, AnalysisLoader):
    """
    SLIDE: A class for ranked list analysis and annotation support.

    The SLIDE class provides tools for loading and transforming ranked feature lists,
    validating data formats, integrating external annotation, and enabling downstream
    functional analysis or visualization based on ranked relationships.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the SLIDE class with configuration settings.

        Args:
            verbose (bool): If False, suppresses all log messages to the console. Defaults to True.
        """
        # Set global verbosity for logging
        set_global_verbosity(verbose)
        # Provide public access to network parameters
        self.params = params
        # Lazily initialize submodules with access to parent SLIDE instance
        self._input = InputIO()
        self._annotation = AnnotationIO()
        self._analysis = AnalysisLoader()

    @property
    def input(self):
        return self._input

    @property
    def annotation(self):
        return self._annotation

    @property
    def analysis(self):
        return self._analysis
