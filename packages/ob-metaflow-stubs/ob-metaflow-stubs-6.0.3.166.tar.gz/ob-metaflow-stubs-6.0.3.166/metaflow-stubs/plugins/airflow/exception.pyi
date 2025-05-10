######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.11.2+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-09T17:10:54.046219                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

