from yeeducli.openapi.token.token import Token
from yeeducli.utility.json_utils import *
import sys

# Token


def create_token(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Token.create_token(
            json_data
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_tokens(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Token.list_tokens(
            json_data.get("page_number"),
            json_data.get("limit")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_token(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Token.delete_token(
            json_data.get('token_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
