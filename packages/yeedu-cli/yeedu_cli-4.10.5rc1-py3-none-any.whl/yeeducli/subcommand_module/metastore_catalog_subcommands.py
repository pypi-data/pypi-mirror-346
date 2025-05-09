from yeeducli.openapi.metastore_catalog.metastore_catalog import MetastoreCatalog
from yeeducli.openapi.metastore_catalog.metastore_catalog_user_association import MetastoreCatalogUserAssociation
from yeeducli.openapi.metastore_catalog.metastore_catalog_workspace_association import MetastoreCatalogWorkspaceAssociation
from yeeducli.openapi.metastore_catalog.metstore_catalog_tenant_association import MetstoreCatalogTenantAssociation
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
from yeeducli.utility.json_utils import trim_namespace_json, change_output, confirm_output, remove_output
import sys

logger = Logger.get_logger(__name__, True)
CATALOG_TYPES_MAP = {"hive": "hive","databricks-unity": "unity"}

def create_metastore_catalog(args):
    try:
        catalog_type = CATALOG_TYPES_MAP[vars(args)['subcommand']]
        trim_json_data = trim_namespace_json(args)
        if catalog_type == 'hive':
          json_data = createOrUpdateHiveMetastoreConfig(change_output(remove_output(args)))
        else:
          json_data = change_output(remove_output(args))
        
        response_json = MetastoreCatalog.create_catalog(json_data,catalog_type)

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def edit_metastore_catalog(args):
    try:
        catalog_type = CATALOG_TYPES_MAP[vars(args)['subcommand']]
        trim_json_data = trim_namespace_json(args)
        if catalog_type == 'hive':
          json_data = createOrUpdateHiveMetastoreConfig(change_output(remove_output(args)))
        else:
          json_data = change_output(remove_output(args))
        metastore_catalog_id = json_data.pop("metastore_catalog_id")
        response_json = MetastoreCatalog.edit_catalog(metastore_catalog_id, process_null_values(json_data), catalog_type)

        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_metastore_catalogs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        catalog_type = json_data.pop("catalog_type", None)

        if catalog_type == None or catalog_type.upper() == "DATABRICKS UNITY" or catalog_type.upper() == "HIVE" :
            response_json = MetastoreCatalog.list_catalogs(
                json_data.get("metastore_catalog_id"),
                catalog_type,
                json_data.get("limit"),
                json_data.get("page_number")
            )
        else:
            logger.error(f"Unsupported catalog_type: {catalog_type}")
            sys.exit(-1)

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def search_metastore_catalogs(args):
    try:
      
        json_data = change_output(trim_namespace_json(args))

        catalog_type = json_data.pop("catalog_type", None)
        if catalog_type == None or catalog_type == "DATABRICKS UNITY" or catalog_type == "HIVE"  :
            response_json = MetastoreCatalog.search_catalog(
                json_data.get("metastore_catalog_name"),
                catalog_type,
                json_data.get("limit"),
                json_data.get("page_number")
            )
        else:
            logger.error(f"Unsupported catalog_type: {catalog_type}")
            sys.exit(-1)

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_metastore_catalog(args):
    try:
        catalog_type = CATALOG_TYPES_MAP[vars(args)['subcommand']]
        json_data = change_output(trim_namespace_json(args))
        metastore_catalog_id = json_data.pop("metastore_catalog_id")
        response_json = MetastoreCatalog.delete_catalog(metastore_catalog_id,catalog_type)
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
        
def link_tenant_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = MetstoreCatalogTenantAssociation.link_tenant_secret(json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def update_tenant_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = process_null_values(change_output(remove_output(args)))

        response_json = MetstoreCatalogTenantAssociation.update_tenant_secret(json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def list_linked_tenant_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetstoreCatalogTenantAssociation.list_linked_tenant_secrets(
            json_data.get("metastore_catalog_secret_tenant_id"),
            json_data.get("catalog_type"),
            json_data.get("metastore_catalog_id"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def search_linked_tenant_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetstoreCatalogTenantAssociation.search_linked_tenant_secrets(
            json_data.get("metastore_catalog_secret_tenant_id"),
            json_data.get("catalog_type"),
            json_data.get("metastore_catalog_name"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def unlink_tenant_secret(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetstoreCatalogTenantAssociation.unlink_tenant_secret(
            json_data.get("metastore_catalog_secret_tenant_id")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def link_user_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = MetastoreCatalogUserAssociation.link_user_secret(json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def update_user_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = process_null_values(change_output(remove_output(args)))

        response_json = MetastoreCatalogUserAssociation.update_user_secret(json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def list_linked_user_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetastoreCatalogUserAssociation.list_linked_user_secrets(
            json_data.get("user_id"),
            json_data.get("metastore_catalog_secret_user_id"),
            json_data.get("catalog_type"),
            json_data.get("metastore_catalog_id"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def search_linked_user_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetastoreCatalogUserAssociation.search_linked_user_secrets(
            json_data.get("user_id"),
            json_data.get("metastore_catalog_secret_user_id"),
            json_data.get("metastore_catalog_name"),
            json_data.get("catalog_type"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def unlink_user_secret(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetastoreCatalogUserAssociation.unlink_user_secret(
            json_data.get("metastore_catalog_secret_user_id")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def link_workspace_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = MetastoreCatalogWorkspaceAssociation.link_workspace_secret(json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def update_workspace_secret(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = process_null_values(change_output(remove_output(args)))

        response_json = MetastoreCatalogWorkspaceAssociation.update_workspace_secret(json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def list_linked_workspace_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetastoreCatalogWorkspaceAssociation.list_linked_workspace_secrets(
            json_data.get("workspace_id"),
            json_data.get("metastore_catalog_secret_workspace_id"),
            json_data.get("catalog_type"),
            json_data.get("metastore_catalog_id"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def search_linked_workspace_secrets(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetastoreCatalogWorkspaceAssociation.search_linked_workspace_secrets(
            json_data.get("workspace_id"),
            json_data.get("metastore_catalog_secret_workspace_id"),
            json_data.get("metastore_catalog_name"),
            json_data.get("catalog_type"),
            json_data.get("limit"),
            json_data.get("page_number")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def unlink_workspace_secret(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = MetastoreCatalogWorkspaceAssociation.unlink_workspace_secret(
            json_data.get("metastore_catalog_secret_workspace_id")
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)