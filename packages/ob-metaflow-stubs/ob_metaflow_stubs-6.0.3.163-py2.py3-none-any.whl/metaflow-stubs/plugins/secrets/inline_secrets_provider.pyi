######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.11.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-06T23:22:15.475170                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import abc
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.secrets
    import abc

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

