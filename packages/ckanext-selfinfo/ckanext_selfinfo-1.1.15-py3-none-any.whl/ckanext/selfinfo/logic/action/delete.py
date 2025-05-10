from __future__ import annotations

import logging

from ckanext.selfinfo import utils

log = logging.getLogger(__name__)


def selfinfo_delete_profile(context, data_dict):
    return utils.selfinfo_delete_redis_key(data_dict.get("profile", ""))
