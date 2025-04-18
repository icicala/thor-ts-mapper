from thor_ts_mapper.logger_config import LoggerConfig
from thor_ts_mapper.thor_mapper_json import THORMapperJson
from thor_ts_mapper.thor_json_log_version import THORJSONLogVersionMapper

@THORJSONLogVersionMapper.log_version("v1.0.0")
class THORMapperJsonV2(THORMapperJson):

    THOR_TIMESTAMP_FIELD = "time"
    THOR_MESSAGE_FIELD = "message"
    THOR_MODULE_FIELD = "module"
