"""
Routes and sub-resources for the /file resource
"""
from typing import Tuple
import json
import os
from flask import Blueprint, jsonify, request, Response
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.config import Config
from csle_common.util.general_util import GeneralUtil
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
file_bp = Blueprint(
    api_constants.MGMT_WEBAPP.FILE_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.FILE_RESOURCE}")


@file_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def read_file() -> Tuple[Response, int]:
    """
    The /file resource

    :return: Reads a given file and returns its contents
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    path = json.loads(request.data)[api_constants.MGMT_WEBAPP.PATH_PROPERTY]
    config = Config.get_current_config()
    if config is None or not GeneralUtil.is_path_in_dir(path=path, directory=config.default_log_dir):
        response_str = f"{path} is not inside the CSLE log directory"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    data = ""
    if os.path.exists(path):
        with open(path, 'r') as fp:
            data = fp.read()
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
