######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.11.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-06T23:22:15.474467                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

