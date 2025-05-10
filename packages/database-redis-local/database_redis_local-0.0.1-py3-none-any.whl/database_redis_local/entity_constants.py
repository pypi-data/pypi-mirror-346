# TODO Please rename the filename from entity_constants.py to your entity. If your entity is country please change the file name to country_constants.py
from logger_local.LoggerComponentEnum import LoggerComponentEnum

WHATSAPP_MESSAGE_INFORU_API_TYPE_ID = 8

WHATSAPP_LOGGER_COMPONENT_ID = 298
WHATSAPP_LOGGER_COMPONENT_NAME = "WhatsApp_InforU_SERVERLESS_PYTHON"
WHATSAPP_DEVELOPER_EMAIL = "tal.g@circ.zone"


# Please change everywhere there is "DatabaseRedis" to your entity name i.e. "Country"  (Please pay attention the C is in uppercase)
class DatabaseRedisLocalConstants:
    """This is a class of all the constants of DatabaseRedis"""

    # TODO Please update your email
    DEVELOPER_EMAIL = 'tal.r@circ.zone'

    # TODO Please change everywhere in the code "DATABASE_REDIS_LOCAL" to "COUNTRY_LOCAL_PYTHON" in case your entity is Country.
    # TODO Please send a message in the Slack to #request-to-open-component-id and get your COMPONENT_ID
    # For example COUNTRY_COMPONENT_ID = 34324
    DATABASE_REDIS_LOCAL_COMPONENT_ID = 299
    # TODO Please write your own COMPONENT_NAME
    DATABASE_REDIS_LOCAL_COMPONENT_NAME = 'DatabaseRedis local Python package'
    DATABASE_REDIS_LOCAL_CODE_LOGGER_OBJECT = {
        'component_id': DATABASE_REDIS_LOCAL_COMPONENT_ID,
        'component_name': DATABASE_REDIS_LOCAL_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    DATABASE_REDIS_LOCAL_TEST_LOGGER_OBJECT = {
        'component_id': DATABASE_REDIS_LOCAL_COMPONENT_ID,
        'component_name': DATABASE_REDIS_LOCAL_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,  # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }

    UNKNOWN_DatabaseRedis_ID = 0

    # TODO Please update if you need default values i.e. for testing
    # DEFAULT_XXX_NAME = None
    # DEFAULT_XXX_NAME = None

    DatabaseRedis_SCHEMA_NAME = 'DatabaseRedis_schema'
    DatabaseRedis_TABLE_NAME = 'DatabaseRedis_table'
    DatabaseRedis_VIEW_NAME = 'DatabaseRedis_view'
    DatabaseRedis_ML_TABLE_NAME = 'DatabaseRedis_ml_table'  # TODO In case you don't use ML table, delete this
    DatabaseRedis_ML_VIEW_NAME = 'DatabaseRedis_ml_view'
    DatabaseRedis_COLUMN_NAME = 'DatabaseRedis_id'


def get_logger_object(category: str = LoggerComponentEnum.ComponentCategory.Code):
    if category == LoggerComponentEnum.ComponentCategory.Code:
        return {
            'component_id': WHATSAPP_LOGGER_COMPONENT_ID,
            'component_name': WHATSAPP_LOGGER_COMPONENT_NAME,
            'component_category': LoggerComponentEnum.ComponentCategory.Code,
            'developer_email': WHATSAPP_DEVELOPER_EMAIL
        }
    elif category == LoggerComponentEnum.ComponentCategory.Unit_Test:
        return {
            'component_id': WHATSAPP_LOGGER_COMPONENT_ID,
            'component_name': WHATSAPP_LOGGER_COMPONENT_NAME,
            'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test,
            'developer_email': WHATSAPP_DEVELOPER_EMAIL
        }
