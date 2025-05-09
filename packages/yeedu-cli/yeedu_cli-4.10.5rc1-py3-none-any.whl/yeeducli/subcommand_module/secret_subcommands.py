from yeeducli.openapi.secret.user_secret import UserSecret
from yeeducli.utility.logger_utils import Logger
from yeeducli.openapi.secret.tenant_secret import TenantSecret
from yeeducli.openapi.secret.workspace_secret import WorkspaceSecret
from yeeducli.utility.json_utils import trim_namespace_json, change_output, confirm_output, remove_output, process_null_values
import sys

logger = Logger.get_logger(__name__, True)

def create_tenant_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = TenantSecret.create_tenant_secret(json_data)

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def edit_tenant_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        tenant_secret_id = json_data.pop("tenant_secret_id", None)

        response_json = TenantSecret.update_tenant_secret(
            tenant_secret_id,
            process_null_values(json_data)
        )

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def list_tenant_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = TenantSecret.list_tenant_secrets(
            json_data.get("limit"),
            json_data.get("page_number"),
            json_data.get("secret_type"),
            json_data.get("tenant_secret_id")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_tenant_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = TenantSecret.search_tenant_secrets(
            json_data.get("secret_name"),
            json_data.get("secret_type"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def delete_tenant_secret(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = TenantSecret.delete_tenant_secret(
            json_data.get('tenant_secret_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def create_user_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = UserSecret.create_user_secret(json_data)

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def edit_user_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        user_secret_id = json_data.pop("user_secret_id", None)

        response_json = UserSecret.update_user_secret(
            user_secret_id,
            process_null_values(json_data)
        )

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def list_user_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = UserSecret.list_user_secrets(
            json_data.get("limit"),
            json_data.get("page_number"),
            json_data.get("secret_type"),
            json_data.get("user_secret_id")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def search_user_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = UserSecret.search_user_secrets(
            json_data.get("secret_name"),
            json_data.get("secret_type"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def delete_user_secret(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = UserSecret.delete_user_secret(
            json_data.get('user_secret_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def create_workspace_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        workspace_id = json_data.pop("workspace_id", None)
        workspace_name = json_data.pop("workspace_name", None)

        response_json = WorkspaceSecret.create_workspace_secret(
            workspace_id,
            workspace_name,
            json_data
        )

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_workspace_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        workspace_id = json_data.pop("workspace_id", None)
        workspace_name = json_data.pop("workspace_name", None)
        workspace_secret_id = json_data.pop("workspace_secret_id", None)

        response_json = WorkspaceSecret.update_workspace_secret(
            workspace_id,
            workspace_name,
            workspace_secret_id,
            process_null_values(json_data)
        )
        
        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def list_workspace_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceSecret.list_workspace_secrets(
            json_data.get("limit"),
            json_data.get("page_number"),
            json_data.get("workspace_id"),
            json_data.get("workspace_name"),
            json_data.get("secret_type"),
            json_data.get("workspace_secret_id")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def search_workspace_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceSecret.search_workspace_secrets(
            json_data.get("workspace_id"),
            json_data.get("workspace_name"),
            json_data.get("secret_name"),
            json_data.get("secret_type"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e) 
        sys.exit(-1)

def delete_workspace_secret(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceSecret.delete_workspace_secret(
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('workspace_secret_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)