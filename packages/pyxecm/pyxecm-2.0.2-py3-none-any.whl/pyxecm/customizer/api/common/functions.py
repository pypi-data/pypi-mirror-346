"""Define common functions."""

import logging

from pyxecm.customizer.api.common.payload_list import PayloadList
from pyxecm.customizer.api.settings import CustomizerAPISettings, api_settings
from pyxecm.customizer.k8s import K8s

logger = logging.getLogger("pyxecm.customizer.api")

# Create a LOCK dict for singleton logs collection
LOGS_LOCK = {}
# Initialize the globel Payloadlist object
PAYLOAD_LIST = PayloadList(logger=logger)


def get_k8s_object() -> K8s:
    """Get an instance of a K8s object.

    Returns:
        K8s: Return a K8s object

    """

    return K8s(logger=logger, namespace=api_settings.namespace)


def get_settings() -> CustomizerAPISettings:
    """Get the API Settings object.

    Returns:
        CustomizerPISettings: Returns the API Settings

    """

    return api_settings


def get_otcs_logs_lock() -> dict:
    """Get the Logs LOCK dict.

    Returns:
        The dict with all LOCKS for the logs

    """

    return LOGS_LOCK
