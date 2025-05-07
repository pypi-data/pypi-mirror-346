######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.11.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-07T07:24:19.650281                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from .exception import MetaflowException as MetaflowException

class PyLintWarn(metaflow.exception.MetaflowException, metaclass=type):
    ...

class PyLint(object, metaclass=type):
    def __init__(self, fname):
        ...
    def has_pylint(self):
        ...
    def run(self, logger = None, warnings = False, pylint_config = []):
        ...
    ...

