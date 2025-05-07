from enum import IntEnum
from typing import Any, Generic, Protocol, TypeVar

_T = TypeVar("_T")

class Pointer(Protocol[_T]):
    contents: _T

_R = TypeVar("_R")

class CallResult(Generic[_R]):
    rval: _R
    def __getitem__(self, item: str) -> Any: ...

class lib:
    LIBSIGROK_LIBSIGROK_H: None
    SR_MAX_CHANNELNAME_LEN: int
    SR_API: None
    SR_PRIV: None
    SR_OK: int
    SR_ERR: int
    SR_ERR_MALLOC: int
    SR_ERR_ARG: int
    SR_ERR_BUG: int
    SR_ERR_SAMPLERATE: int
    SR_ERR_NA: int
    SR_ERR_DEV_CLOSED: int
    SR_ERR_TIMEOUT: int
    SR_ERR_CHANNEL_GROUP: int
    SR_ERR_DATA: int
    SR_ERR_IO: int
    SR_LOG_NONE: int
    SR_LOG_ERR: int
    SR_LOG_WARN: int
    SR_LOG_INFO: int
    SR_LOG_DBG: int
    SR_LOG_SPEW: int
    SR_T_UINT64: int
    SR_T_STRING: int
    SR_T_BOOL: int
    SR_T_FLOAT: int
    SR_T_RATIONAL_PERIOD: int
    SR_T_RATIONAL_VOLT: int
    SR_T_KEYVALUE: int
    SR_T_UINT64_RANGE: int
    SR_T_DOUBLE_RANGE: int
    SR_T_INT32: int
    SR_T_MQ: int
    SR_DF_HEADER: int
    SR_DF_END: int
    SR_DF_META: int
    SR_DF_TRIGGER: int
    SR_DF_LOGIC: int
    SR_DF_FRAME_BEGIN: int
    SR_DF_FRAME_END: int
    SR_DF_ANALOG: int
    SR_MQ_VOLTAGE: int
    SR_MQ_CURRENT: int
    SR_MQ_RESISTANCE: int
    SR_MQ_CAPACITANCE: int
    SR_MQ_TEMPERATURE: int
    SR_MQ_FREQUENCY: int
    SR_MQ_DUTY_CYCLE: int
    SR_MQ_CONTINUITY: int
    SR_MQ_PULSE_WIDTH: int
    SR_MQ_CONDUCTANCE: int
    SR_MQ_POWER: int
    SR_MQ_GAIN: int
    SR_MQ_SOUND_PRESSURE_LEVEL: int
    SR_MQ_CARBON_MONOXIDE: int
    SR_MQ_RELATIVE_HUMIDITY: int
    SR_MQ_TIME: int
    SR_MQ_WIND_SPEED: int
    SR_MQ_PRESSURE: int
    SR_MQ_PARALLEL_INDUCTANCE: int
    SR_MQ_PARALLEL_CAPACITANCE: int
    SR_MQ_PARALLEL_RESISTANCE: int
    SR_MQ_SERIES_INDUCTANCE: int
    SR_MQ_SERIES_CAPACITANCE: int
    SR_MQ_SERIES_RESISTANCE: int
    SR_MQ_DISSIPATION_FACTOR: int
    SR_MQ_QUALITY_FACTOR: int
    SR_MQ_PHASE_ANGLE: int
    SR_MQ_DIFFERENCE: int
    SR_MQ_COUNT: int
    SR_MQ_POWER_FACTOR: int
    SR_MQ_APPARENT_POWER: int
    SR_MQ_MASS: int
    SR_MQ_HARMONIC_RATIO: int
    SR_UNIT_VOLT: int
    SR_UNIT_AMPERE: int
    SR_UNIT_OHM: int
    SR_UNIT_FARAD: int
    SR_UNIT_KELVIN: int
    SR_UNIT_CELSIUS: int
    SR_UNIT_FAHRENHEIT: int
    SR_UNIT_HERTZ: int
    SR_UNIT_PERCENTAGE: int
    SR_UNIT_BOOLEAN: int
    SR_UNIT_SECOND: int
    SR_UNIT_SIEMENS: int
    SR_UNIT_DECIBEL_MW: int
    SR_UNIT_DECIBEL_VOLT: int
    SR_UNIT_UNITLESS: int
    SR_UNIT_DECIBEL_SPL: int
    SR_UNIT_CONCENTRATION: int
    SR_UNIT_REVOLUTIONS_PER_MINUTE: int
    SR_UNIT_VOLT_AMPERE: int
    SR_UNIT_WATT: int
    SR_UNIT_WATT_HOUR: int
    SR_UNIT_METER_SECOND: int
    SR_UNIT_HECTOPASCAL: int
    SR_UNIT_HUMIDITY_293K: int
    SR_UNIT_DEGREE: int
    SR_UNIT_HENRY: int
    SR_UNIT_GRAM: int
    SR_UNIT_CARAT: int
    SR_UNIT_OUNCE: int
    SR_UNIT_TROY_OUNCE: int
    SR_UNIT_POUND: int
    SR_UNIT_PENNYWEIGHT: int
    SR_UNIT_GRAIN: int
    SR_UNIT_TAEL: int
    SR_UNIT_MOMME: int
    SR_UNIT_TOLA: int
    SR_UNIT_PIECE: int
    SR_MQFLAG_AC: int
    SR_MQFLAG_DC: int
    SR_MQFLAG_RMS: int
    SR_MQFLAG_DIODE: int
    SR_MQFLAG_HOLD: int
    SR_MQFLAG_MAX: int
    SR_MQFLAG_MIN: int
    SR_MQFLAG_AUTORANGE: int
    SR_MQFLAG_RELATIVE: int
    SR_MQFLAG_SPL_FREQ_WEIGHT_A: int
    SR_MQFLAG_SPL_FREQ_WEIGHT_C: int
    SR_MQFLAG_SPL_FREQ_WEIGHT_Z: int
    SR_MQFLAG_SPL_FREQ_WEIGHT_FLAT: int
    SR_MQFLAG_SPL_TIME_WEIGHT_S: int
    SR_MQFLAG_SPL_TIME_WEIGHT_F: int
    SR_MQFLAG_SPL_LAT: int
    SR_MQFLAG_SPL_PCT_OVER_ALARM: int
    SR_MQFLAG_DURATION: int
    SR_MQFLAG_AVG: int
    SR_MQFLAG_REFERENCE: int
    SR_MQFLAG_UNSTABLE: int
    SR_MQFLAG_FOUR_WIRE: int
    SR_TRIGGER_ZERO: int
    SR_TRIGGER_ONE: int
    SR_TRIGGER_RISING: int
    SR_TRIGGER_FALLING: int
    SR_TRIGGER_EDGE: int
    SR_TRIGGER_OVER: int
    SR_TRIGGER_UNDER: int
    SR_RESOURCE_FIRMWARE: int
    SR_OUTPUT_INTERNAL_IO_HANDLING: int
    SR_CHANNEL_LOGIC: int
    SR_CHANNEL_ANALOG: int
    SR_KEY_CONFIG: int
    SR_KEY_MQ: int
    SR_KEY_MQFLAGS: int
    SR_CONF_GET: int
    SR_CONF_SET: int
    SR_CONF_LIST: int
    SR_CONF_LOGIC_ANALYZER: int
    SR_CONF_OSCILLOSCOPE: int
    SR_CONF_MULTIMETER: int
    SR_CONF_DEMO_DEV: int
    SR_CONF_SOUNDLEVELMETER: int
    SR_CONF_THERMOMETER: int
    SR_CONF_HYGROMETER: int
    SR_CONF_ENERGYMETER: int
    SR_CONF_DEMODULATOR: int
    SR_CONF_POWER_SUPPLY: int
    SR_CONF_LCRMETER: int
    SR_CONF_ELECTRONIC_LOAD: int
    SR_CONF_SCALE: int
    SR_CONF_SIGNAL_GENERATOR: int
    SR_CONF_POWERMETER: int
    SR_CONF_CONN: int
    SR_CONF_SERIALCOMM: int
    SR_CONF_MODBUSADDR: int
    SR_CONF_SAMPLERATE: int
    SR_CONF_CAPTURE_RATIO: int
    SR_CONF_PATTERN_MODE: int
    SR_CONF_RLE: int
    SR_CONF_TRIGGER_SLOPE: int
    SR_CONF_AVERAGING: int
    SR_CONF_AVG_SAMPLES: int
    SR_CONF_TRIGGER_SOURCE: int
    SR_CONF_HORIZ_TRIGGERPOS: int
    SR_CONF_BUFFERSIZE: int
    SR_CONF_TIMEBASE: int
    SR_CONF_FILTER: int
    SR_CONF_VDIV: int
    SR_CONF_COUPLING: int
    SR_CONF_TRIGGER_MATCH: int
    SR_CONF_SAMPLE_INTERVAL: int
    SR_CONF_NUM_HDIV: int
    SR_CONF_NUM_VDIV: int
    SR_CONF_SPL_WEIGHT_FREQ: int
    SR_CONF_SPL_WEIGHT_TIME: int
    SR_CONF_SPL_MEASUREMENT_RANGE: int
    SR_CONF_HOLD_MAX: int
    SR_CONF_HOLD_MIN: int
    SR_CONF_VOLTAGE_THRESHOLD: int
    SR_CONF_EXTERNAL_CLOCK: int
    SR_CONF_SWAP: int
    SR_CONF_CENTER_FREQUENCY: int
    SR_CONF_NUM_LOGIC_CHANNELS: int
    SR_CONF_NUM_ANALOG_CHANNELS: int
    SR_CONF_VOLTAGE: int
    SR_CONF_VOLTAGE_TARGET: int
    SR_CONF_CURRENT: int
    SR_CONF_CURRENT_LIMIT: int
    SR_CONF_ENABLED: int
    SR_CONF_CHANNEL_CONFIG: int
    SR_CONF_OVER_VOLTAGE_PROTECTION_ENABLED: int
    SR_CONF_OVER_VOLTAGE_PROTECTION_ACTIVE: int
    SR_CONF_OVER_VOLTAGE_PROTECTION_THRESHOLD: int
    SR_CONF_OVER_CURRENT_PROTECTION_ENABLED: int
    SR_CONF_OVER_CURRENT_PROTECTION_ACTIVE: int
    SR_CONF_OVER_CURRENT_PROTECTION_THRESHOLD: int
    SR_CONF_CLOCK_EDGE: int
    SR_CONF_AMPLITUDE: int
    SR_CONF_REGULATION: int
    SR_CONF_OVER_TEMPERATURE_PROTECTION: int
    SR_CONF_OUTPUT_FREQUENCY: int
    SR_CONF_OUTPUT_FREQUENCY_TARGET: int
    SR_CONF_MEASURED_QUANTITY: int
    SR_CONF_EQUIV_CIRCUIT_MODEL: int
    SR_CONF_OVER_TEMPERATURE_PROTECTION_ACTIVE: int
    SR_CONF_UNDER_VOLTAGE_CONDITION: int
    SR_CONF_UNDER_VOLTAGE_CONDITION_ACTIVE: int
    SR_CONF_TRIGGER_LEVEL: int
    SR_CONF_UNDER_VOLTAGE_CONDITION_THRESHOLD: int
    SR_CONF_EXTERNAL_CLOCK_SOURCE: int
    SR_CONF_OFFSET: int
    SR_CONF_TRIGGER_PATTERN: int
    SR_CONF_HIGH_RESOLUTION: int
    SR_CONF_PEAK_DETECTION: int
    SR_CONF_LOGIC_THRESHOLD: int
    SR_CONF_LOGIC_THRESHOLD_CUSTOM: int
    SR_CONF_RANGE: int
    SR_CONF_DIGITS: int
    SR_CONF_SESSIONFILE: int
    SR_CONF_CAPTUREFILE: int
    SR_CONF_CAPTURE_UNITSIZE: int
    SR_CONF_POWER_OFF: int
    SR_CONF_DATA_SOURCE: int
    SR_CONF_PROBE_FACTOR: int
    SR_CONF_ADC_POWERLINE_CYCLES: int
    SR_CONF_LIMIT_MSEC: int
    SR_CONF_LIMIT_SAMPLES: int
    SR_CONF_LIMIT_FRAMES: int
    SR_CONF_CONTINUOUS: int
    SR_CONF_DATALOG: int
    SR_CONF_DEVICE_MODE: int
    SR_CONF_TEST_MODE: int
    SR_INST_USB: int
    SR_INST_SERIAL: int
    SR_INST_SCPI: int
    SR_INST_USER: int
    SR_INST_MODBUS: int
    SR_ST_NOT_FOUND: int
    SR_ST_INITIALIZING: int
    SR_ST_INACTIVE: int
    SR_ST_ACTIVE: int
    SR_ST_STOPPING: int
    LIBSIGROK_VERSION_H: None
    SR_PACKAGE_VERSION_MAJOR: int
    SR_PACKAGE_VERSION_MINOR: int
    SR_PACKAGE_VERSION_MICRO: int
    SR_PACKAGE_VERSION_STRING: str
    SR_LIB_VERSION_CURRENT: int
    SR_LIB_VERSION_REVISION: int
    SR_LIB_VERSION_AGE: int
    SR_LIB_VERSION_STRING: str
    LIBSIGROK_PROTO_H: None
    g_slist_free1: None
    G_MININT8: None
    G_MAXINT8: int
    G_MAXUINT8: int
    G_MININT16: None
    G_MAXINT16: int
    G_MAXUINT16: int
    G_MININT32: None
    G_MAXINT32: int
    G_MAXUINT32: int
    G_MININT64: None
    G_MAXINT64: None
    G_MAXUINT64: None
    G_E: float
    G_LN2: float
    G_LN10: float
    G_PI: float
    G_PI_2: float
    G_PI_4: float
    G_SQRT2: float
    G_LITTLE_ENDIAN: int
    G_BIG_ENDIAN: int
    G_PDP_ENDIAN: int
    G_IEEE754_FLOAT_BIAS: int
    G_IEEE754_DOUBLE_BIAS: int
    G_LOG_2_BASE_10: float
    G_VARIANT_PARSE_ERROR: None
    G_VARIANT_CLASS_BOOLEAN: str
    G_VARIANT_PARSE_ERROR_FAILED: int
    G_VARIANT_PARSE_ERROR_BASIC_TYPE_EXPECTED: int
    G_VARIANT_PARSE_ERROR_CANNOT_INFER_TYPE: int
    G_VARIANT_PARSE_ERROR_DEFINITE_TYPE_EXPECTED: int
    G_VARIANT_PARSE_ERROR_INPUT_NOT_AT_END: int
    G_VARIANT_PARSE_ERROR_INVALID_CHARACTER: int
    G_VARIANT_PARSE_ERROR_INVALID_FORMAT_STRING: int
    G_VARIANT_PARSE_ERROR_INVALID_OBJECT_PATH: int
    G_VARIANT_PARSE_ERROR_INVALID_SIGNATURE: int
    G_VARIANT_PARSE_ERROR_INVALID_TYPE_STRING: int
    G_VARIANT_PARSE_ERROR_NO_COMMON_TYPE: int
    G_VARIANT_PARSE_ERROR_NUMBER_OUT_OF_RANGE: int
    G_VARIANT_PARSE_ERROR_NUMBER_TOO_BIG: int
    G_VARIANT_PARSE_ERROR_TYPE_ERROR: int
    G_VARIANT_PARSE_ERROR_UNEXPECTED_TOKEN: int
    G_VARIANT_PARSE_ERROR_UNKNOWN_KEYWORD: int
    G_VARIANT_PARSE_ERROR_UNTERMINATED_STRING_CONSTANT: int
    G_VARIANT_PARSE_ERROR_VALUE_EXPECTED: int
    G_VARIANT_PARSE_ERROR_RECURSION: int
    G_PRIORITY_HIGH: int
    G_PRIORITY_DEFAULT: int
    G_PRIORITY_HIGH_IDLE: int
    G_PRIORITY_DEFAULT_IDLE: int
    G_PRIORITY_LOW: int
    G_SOURCE_REMOVE: None
    G_SOURCE_CONTINUE: None
    G_MAIN_CONTEXT_FLAGS_NONE: int
    G_MAIN_CONTEXT_FLAGS_OWNERLESS_POLLING: int
    GLIB_AVAILABLE_TYPE_IN_2_64: None
    g_timeout_funcs: None
    g_child_watch_funcs: None
    g_idle_funcs: None
    GSList: None
    gchar: None
    gshort: None
    glong: None
    gint: None
    gboolean: None
    guchar: None
    gushort: None
    gulong: None
    guint: None
    gfloat: None
    gdouble: None
    GDoubleIEEE754: None
    GFloatIEEE754: None
    grefcount: None
    gatomicrefcount: None
    GVariant: None
    GVariantClass: None
    GVariantIter: None
    GVariantBuilder: None
    GVariantParseError: None
    GVariantDict: None
    GBytes: None
    GArray: None
    GByteArray: None
    GPtrArray: None
    GMainContextFlags: None
    GMainContext: None
    GMainLoop: None
    GSource: None
    GSourcePrivate: None
    GSourceCallbackFuncs: None
    GSourceFuncs: None
    guint64: None
    class type_sr_error_code(IntEnum):
        SR_OK = 0
        SR_ERR = -1
        SR_ERR_MALLOC = -2
        SR_ERR_ARG = -3
        SR_ERR_BUG = -4
        SR_ERR_SAMPLERATE = -5
        SR_ERR_NA = -6
        SR_ERR_DEV_CLOSED = -7
        SR_ERR_TIMEOUT = -8
        SR_ERR_CHANNEL_GROUP = -9
        SR_ERR_DATA = -10
        SR_ERR_IO = -11

    class type_sr_loglevel(IntEnum):
        SR_LOG_NONE = 0
        SR_LOG_ERR = 1
        SR_LOG_WARN = 2
        SR_LOG_INFO = 3
        SR_LOG_DBG = 4
        SR_LOG_SPEW = 5

    class type_sr_datatype(IntEnum):
        SR_T_UINT64 = 10000
        SR_T_STRING = 10001
        SR_T_BOOL = 10002
        SR_T_FLOAT = 10003
        SR_T_RATIONAL_PERIOD = 10004
        SR_T_RATIONAL_VOLT = 10005
        SR_T_KEYVALUE = 10006
        SR_T_UINT64_RANGE = 10007
        SR_T_DOUBLE_RANGE = 10008
        SR_T_INT32 = 10009
        SR_T_MQ = 10010

    class type_sr_packettype(IntEnum):
        SR_DF_HEADER = 10000
        SR_DF_END = 10001
        SR_DF_META = 10002
        SR_DF_TRIGGER = 10003
        SR_DF_LOGIC = 10004
        SR_DF_FRAME_BEGIN = 10005
        SR_DF_FRAME_END = 10006
        SR_DF_ANALOG = 10007

    class type_sr_mq(IntEnum):
        SR_MQ_VOLTAGE = 10000
        SR_MQ_CURRENT = 10001
        SR_MQ_RESISTANCE = 10002
        SR_MQ_CAPACITANCE = 10003
        SR_MQ_TEMPERATURE = 10004
        SR_MQ_FREQUENCY = 10005
        SR_MQ_DUTY_CYCLE = 10006
        SR_MQ_CONTINUITY = 10007
        SR_MQ_PULSE_WIDTH = 10008
        SR_MQ_CONDUCTANCE = 10009
        SR_MQ_POWER = 10010
        SR_MQ_GAIN = 10011
        SR_MQ_SOUND_PRESSURE_LEVEL = 10012
        SR_MQ_CARBON_MONOXIDE = 10013
        SR_MQ_RELATIVE_HUMIDITY = 10014
        SR_MQ_TIME = 10015
        SR_MQ_WIND_SPEED = 10016
        SR_MQ_PRESSURE = 10017
        SR_MQ_PARALLEL_INDUCTANCE = 10018
        SR_MQ_PARALLEL_CAPACITANCE = 10019
        SR_MQ_PARALLEL_RESISTANCE = 10020
        SR_MQ_SERIES_INDUCTANCE = 10021
        SR_MQ_SERIES_CAPACITANCE = 10022
        SR_MQ_SERIES_RESISTANCE = 10023
        SR_MQ_DISSIPATION_FACTOR = 10024
        SR_MQ_QUALITY_FACTOR = 10025
        SR_MQ_PHASE_ANGLE = 10026
        SR_MQ_DIFFERENCE = 10027
        SR_MQ_COUNT = 10028
        SR_MQ_POWER_FACTOR = 10029
        SR_MQ_APPARENT_POWER = 10030
        SR_MQ_MASS = 10031
        SR_MQ_HARMONIC_RATIO = 10032

    class type_sr_unit(IntEnum):
        SR_UNIT_VOLT = 10000
        SR_UNIT_AMPERE = 10001
        SR_UNIT_OHM = 10002
        SR_UNIT_FARAD = 10003
        SR_UNIT_KELVIN = 10004
        SR_UNIT_CELSIUS = 10005
        SR_UNIT_FAHRENHEIT = 10006
        SR_UNIT_HERTZ = 10007
        SR_UNIT_PERCENTAGE = 10008
        SR_UNIT_BOOLEAN = 10009
        SR_UNIT_SECOND = 10010
        SR_UNIT_SIEMENS = 10011
        SR_UNIT_DECIBEL_MW = 10012
        SR_UNIT_DECIBEL_VOLT = 10013
        SR_UNIT_UNITLESS = 10014
        SR_UNIT_DECIBEL_SPL = 10015
        SR_UNIT_CONCENTRATION = 10016
        SR_UNIT_REVOLUTIONS_PER_MINUTE = 10017
        SR_UNIT_VOLT_AMPERE = 10018
        SR_UNIT_WATT = 10019
        SR_UNIT_WATT_HOUR = 10020
        SR_UNIT_METER_SECOND = 10021
        SR_UNIT_HECTOPASCAL = 10022
        SR_UNIT_HUMIDITY_293K = 10023
        SR_UNIT_DEGREE = 10024
        SR_UNIT_HENRY = 10025
        SR_UNIT_GRAM = 10026
        SR_UNIT_CARAT = 10027
        SR_UNIT_OUNCE = 10028
        SR_UNIT_TROY_OUNCE = 10029
        SR_UNIT_POUND = 10030
        SR_UNIT_PENNYWEIGHT = 10031
        SR_UNIT_GRAIN = 10032
        SR_UNIT_TAEL = 10033
        SR_UNIT_MOMME = 10034
        SR_UNIT_TOLA = 10035
        SR_UNIT_PIECE = 10036

    class type_sr_mqflag(IntEnum):
        SR_MQFLAG_AC = 1
        SR_MQFLAG_DC = 2
        SR_MQFLAG_RMS = 4
        SR_MQFLAG_DIODE = 8
        SR_MQFLAG_HOLD = 16
        SR_MQFLAG_MAX = 32
        SR_MQFLAG_MIN = 64
        SR_MQFLAG_AUTORANGE = 128
        SR_MQFLAG_RELATIVE = 256
        SR_MQFLAG_SPL_FREQ_WEIGHT_A = 512
        SR_MQFLAG_SPL_FREQ_WEIGHT_C = 1024
        SR_MQFLAG_SPL_FREQ_WEIGHT_Z = 2048
        SR_MQFLAG_SPL_FREQ_WEIGHT_FLAT = 4096
        SR_MQFLAG_SPL_TIME_WEIGHT_S = 8192
        SR_MQFLAG_SPL_TIME_WEIGHT_F = 16384
        SR_MQFLAG_SPL_LAT = 32768
        SR_MQFLAG_SPL_PCT_OVER_ALARM = 65536
        SR_MQFLAG_DURATION = 131072
        SR_MQFLAG_AVG = 262144
        SR_MQFLAG_REFERENCE = 524288
        SR_MQFLAG_UNSTABLE = 1048576
        SR_MQFLAG_FOUR_WIRE = 2097152

    class type_sr_trigger_matches(IntEnum):
        SR_TRIGGER_ZERO = 1
        SR_TRIGGER_ONE = 2
        SR_TRIGGER_RISING = 3
        SR_TRIGGER_FALLING = 4
        SR_TRIGGER_EDGE = 5
        SR_TRIGGER_OVER = 6
        SR_TRIGGER_UNDER = 7

    class type_sr_resource_type(IntEnum):
        SR_RESOURCE_FIRMWARE = 1

    class type_sr_output_flag(IntEnum):
        SR_OUTPUT_INTERNAL_IO_HANDLING = 1

    class type_sr_channeltype(IntEnum):
        SR_CHANNEL_LOGIC = 10000
        SR_CHANNEL_ANALOG = 10001

    class type_sr_keytype(IntEnum):
        SR_KEY_CONFIG = 0
        SR_KEY_MQ = 1
        SR_KEY_MQFLAGS = 2

    class type_sr_configcap(IntEnum):
        SR_CONF_GET = 2147483648
        SR_CONF_SET = 1073741824
        SR_CONF_LIST = 536870912

    class type_sr_configkey(IntEnum):
        SR_CONF_LOGIC_ANALYZER = 10000
        SR_CONF_OSCILLOSCOPE = 10001
        SR_CONF_MULTIMETER = 10002
        SR_CONF_DEMO_DEV = 10003
        SR_CONF_SOUNDLEVELMETER = 10004
        SR_CONF_THERMOMETER = 10005
        SR_CONF_HYGROMETER = 10006
        SR_CONF_ENERGYMETER = 10007
        SR_CONF_DEMODULATOR = 10008
        SR_CONF_POWER_SUPPLY = 10009
        SR_CONF_LCRMETER = 10010
        SR_CONF_ELECTRONIC_LOAD = 10011
        SR_CONF_SCALE = 10012
        SR_CONF_SIGNAL_GENERATOR = 10013
        SR_CONF_POWERMETER = 10014
        SR_CONF_CONN = 20000
        SR_CONF_SERIALCOMM = 20001
        SR_CONF_MODBUSADDR = 20002
        SR_CONF_SAMPLERATE = 30000
        SR_CONF_CAPTURE_RATIO = 30001
        SR_CONF_PATTERN_MODE = 30002
        SR_CONF_RLE = 30003
        SR_CONF_TRIGGER_SLOPE = 30004
        SR_CONF_AVERAGING = 30005
        SR_CONF_AVG_SAMPLES = 30006
        SR_CONF_TRIGGER_SOURCE = 30007
        SR_CONF_HORIZ_TRIGGERPOS = 30008
        SR_CONF_BUFFERSIZE = 30009
        SR_CONF_TIMEBASE = 30010
        SR_CONF_FILTER = 30011
        SR_CONF_VDIV = 30012
        SR_CONF_COUPLING = 30013
        SR_CONF_TRIGGER_MATCH = 30014
        SR_CONF_SAMPLE_INTERVAL = 30015
        SR_CONF_NUM_HDIV = 30016
        SR_CONF_NUM_VDIV = 30017
        SR_CONF_SPL_WEIGHT_FREQ = 30018
        SR_CONF_SPL_WEIGHT_TIME = 30019
        SR_CONF_SPL_MEASUREMENT_RANGE = 30020
        SR_CONF_HOLD_MAX = 30021
        SR_CONF_HOLD_MIN = 30022
        SR_CONF_VOLTAGE_THRESHOLD = 30023
        SR_CONF_EXTERNAL_CLOCK = 30024
        SR_CONF_SWAP = 30025
        SR_CONF_CENTER_FREQUENCY = 30026
        SR_CONF_NUM_LOGIC_CHANNELS = 30027
        SR_CONF_NUM_ANALOG_CHANNELS = 30028
        SR_CONF_VOLTAGE = 30029
        SR_CONF_VOLTAGE_TARGET = 30030
        SR_CONF_CURRENT = 30031
        SR_CONF_CURRENT_LIMIT = 30032
        SR_CONF_ENABLED = 30033
        SR_CONF_CHANNEL_CONFIG = 30034
        SR_CONF_OVER_VOLTAGE_PROTECTION_ENABLED = 30035
        SR_CONF_OVER_VOLTAGE_PROTECTION_ACTIVE = 30036
        SR_CONF_OVER_VOLTAGE_PROTECTION_THRESHOLD = 30037
        SR_CONF_OVER_CURRENT_PROTECTION_ENABLED = 30038
        SR_CONF_OVER_CURRENT_PROTECTION_ACTIVE = 30039
        SR_CONF_OVER_CURRENT_PROTECTION_THRESHOLD = 30040
        SR_CONF_CLOCK_EDGE = 30041
        SR_CONF_AMPLITUDE = 30042
        SR_CONF_REGULATION = 30043
        SR_CONF_OVER_TEMPERATURE_PROTECTION = 30044
        SR_CONF_OUTPUT_FREQUENCY = 30045
        SR_CONF_OUTPUT_FREQUENCY_TARGET = 30046
        SR_CONF_MEASURED_QUANTITY = 30047
        SR_CONF_EQUIV_CIRCUIT_MODEL = 30048
        SR_CONF_OVER_TEMPERATURE_PROTECTION_ACTIVE = 30049
        SR_CONF_UNDER_VOLTAGE_CONDITION = 30050
        SR_CONF_UNDER_VOLTAGE_CONDITION_ACTIVE = 30051
        SR_CONF_TRIGGER_LEVEL = 30052
        SR_CONF_UNDER_VOLTAGE_CONDITION_THRESHOLD = 30053
        SR_CONF_EXTERNAL_CLOCK_SOURCE = 30054
        SR_CONF_OFFSET = 30055
        SR_CONF_TRIGGER_PATTERN = 30056
        SR_CONF_HIGH_RESOLUTION = 30057
        SR_CONF_PEAK_DETECTION = 30058
        SR_CONF_LOGIC_THRESHOLD = 30059
        SR_CONF_LOGIC_THRESHOLD_CUSTOM = 30060
        SR_CONF_RANGE = 30061
        SR_CONF_DIGITS = 30062
        SR_CONF_SESSIONFILE = 40000
        SR_CONF_CAPTUREFILE = 40001
        SR_CONF_CAPTURE_UNITSIZE = 40002
        SR_CONF_POWER_OFF = 40003
        SR_CONF_DATA_SOURCE = 40004
        SR_CONF_PROBE_FACTOR = 40005
        SR_CONF_ADC_POWERLINE_CYCLES = 40006
        SR_CONF_LIMIT_MSEC = 50000
        SR_CONF_LIMIT_SAMPLES = 50001
        SR_CONF_LIMIT_FRAMES = 50002
        SR_CONF_CONTINUOUS = 50003
        SR_CONF_DATALOG = 50004
        SR_CONF_DEVICE_MODE = 50005
        SR_CONF_TEST_MODE = 50006

    class type_sr_dev_inst_type(IntEnum):
        SR_INST_USB = 10000
        SR_INST_SERIAL = 10001
        SR_INST_SCPI = 10002
        SR_INST_USER = 10003
        SR_INST_MODBUS = 10004

    class type_sr_dev_inst_status(IntEnum):
        SR_ST_NOT_FOUND = 10000
        SR_ST_INITIALIZING = 10001
        SR_ST_INACTIVE = 10002
        SR_ST_ACTIVE = 10003
        SR_ST_STOPPING = 10004

    class type_anon_enum0(IntEnum):
        G_VARIANT_PARSE_ERROR_FAILED = 0
        G_VARIANT_PARSE_ERROR_BASIC_TYPE_EXPECTED = 1
        G_VARIANT_PARSE_ERROR_CANNOT_INFER_TYPE = 2
        G_VARIANT_PARSE_ERROR_DEFINITE_TYPE_EXPECTED = 3
        G_VARIANT_PARSE_ERROR_INPUT_NOT_AT_END = 4
        G_VARIANT_PARSE_ERROR_INVALID_CHARACTER = 5
        G_VARIANT_PARSE_ERROR_INVALID_FORMAT_STRING = 6
        G_VARIANT_PARSE_ERROR_INVALID_OBJECT_PATH = 7
        G_VARIANT_PARSE_ERROR_INVALID_SIGNATURE = 8
        G_VARIANT_PARSE_ERROR_INVALID_TYPE_STRING = 9
        G_VARIANT_PARSE_ERROR_NO_COMMON_TYPE = 10
        G_VARIANT_PARSE_ERROR_NUMBER_OUT_OF_RANGE = 11
        G_VARIANT_PARSE_ERROR_NUMBER_TOO_BIG = 12
        G_VARIANT_PARSE_ERROR_TYPE_ERROR = 13
        G_VARIANT_PARSE_ERROR_UNEXPECTED_TOKEN = 14
        G_VARIANT_PARSE_ERROR_UNKNOWN_KEYWORD = 15
        G_VARIANT_PARSE_ERROR_UNTERMINATED_STRING_CONSTANT = 16
        G_VARIANT_PARSE_ERROR_VALUE_EXPECTED = 17
        G_VARIANT_PARSE_ERROR_RECURSION = 18

    class type_anon_enum1(IntEnum):
        G_MAIN_CONTEXT_FLAGS_NONE = 0
        G_MAIN_CONTEXT_FLAGS_OWNERLESS_POLLING = 1

    class type_sr_trigger(Protocol):
        name: bytes
        stages: Any

    sr_trigger: type_sr_trigger
    class type_sr_trigger_stage(Protocol):
        stage: int
        matches: Any

    sr_trigger_stage: type_sr_trigger_stage
    class type_sr_channel(Protocol):
        sdi: Any
        index: int
        type: int
        enabled: Any
        name: bytes
        priv: Any

    sr_channel: type_sr_channel
    class type_sr_trigger_match(Protocol):
        channel: Any
        match: int
        value: Any

    sr_trigger_match: type_sr_trigger_match
    class type_sr_context(Protocol):
        ...

    sr_context: type_sr_context
    class type_sr_session(Protocol):
        ...

    sr_session: type_sr_session
    class type_sr_rational(Protocol):
        p: Any
        q: Any

    sr_rational: type_sr_rational
    class type_sr_datafeed_packet(Protocol):
        type: Any
        payload: Any

    sr_datafeed_packet: type_sr_datafeed_packet
    class type_timeval(Protocol):
        ...

    timeval: type_timeval
    class type_sr_datafeed_header(Protocol):
        feed_version: int
        starttime: Any

    sr_datafeed_header: type_sr_datafeed_header
    class type_sr_datafeed_meta(Protocol):
        config: Any

    sr_datafeed_meta: type_sr_datafeed_meta
    class type_sr_datafeed_logic(Protocol):
        length: Any
        unitsize: Any
        data: Any

    sr_datafeed_logic: type_sr_datafeed_logic
    class type_sr_analog_encoding(Protocol):
        unitsize: Any
        is_signed: Any
        is_float: Any
        is_bigendian: Any
        digits: Any
        is_digits_decimal: Any
        scale: Any
        offset: Any

    sr_analog_encoding: type_sr_analog_encoding
    class type_sr_analog_meaning(Protocol):
        mq: Any
        unit: Any
        mqflags: Any
        channels: Any

    sr_analog_meaning: type_sr_analog_meaning
    class type_sr_analog_spec(Protocol):
        spec_digits: Any

    sr_analog_spec: type_sr_analog_spec
    class type_sr_datafeed_analog(Protocol):
        data: Any
        num_samples: Any
        encoding: Any
        meaning: Any
        spec: Any

    sr_datafeed_analog: type_sr_datafeed_analog
    class type_sr_option(Protocol):
        id: bytes
        name: bytes
        desc: bytes
        values: Any

    sr_option: type_sr_option
    class type_sr_resource(Protocol):
        size: Any
        handle: Any
        type: int

    sr_resource: type_sr_resource
    class type_sr_input(Protocol):
        ...

    sr_input: type_sr_input
    class type_sr_input_module(Protocol):
        ...

    sr_input_module: type_sr_input_module
    class type_sr_output(Protocol):
        ...

    sr_output: type_sr_output
    class type_sr_output_module(Protocol):
        ...

    sr_output_module: type_sr_output_module
    class type_sr_transform(Protocol):
        ...

    sr_transform: type_sr_transform
    class type_sr_transform_module(Protocol):
        ...

    sr_transform_module: type_sr_transform_module
    class type_sr_dev_inst(Protocol):
        ...

    sr_dev_inst: type_sr_dev_inst
    class type_sr_channel_group(Protocol):
        name: bytes
        channels: Any
        priv: Any

    sr_channel_group: type_sr_channel_group
    class type_sr_config(Protocol):
        key: Any
        data: Any

    sr_config: type_sr_config
    class type_sr_key_info(Protocol):
        key: Any
        datatype: int
        id: bytes
        name: bytes
        description: bytes

    sr_key_info: type_sr_key_info
    class type_sr_dev_driver(Protocol):
        name: bytes
        longname: bytes
        api_version: int
        init: int
        cleanup: int
        scan: Any
        dev_list: Any
        dev_clear: int
        config_get: int
        config_set: int
        config_channel_set: int
        config_commit: int
        config_list: int
        dev_open: int
        dev_close: int
        dev_acquisition_start: int
        dev_acquisition_stop: int
        context: Any

    sr_dev_driver: type_sr_dev_driver
    class type_sr_serial_port(Protocol):
        name: bytes
        description: bytes

    sr_serial_port: type_sr_serial_port
    class type_anon_struct0(Protocol):
        partial_magic: Any
        type: Any
        y: Any

    anon_struct0: type_anon_struct0
    class type_anon_struct1(Protocol):
        asv: Any
        partial_magic: Any
        y: Any

    anon_struct1: type_anon_struct1
    @staticmethod
    def sr_analog_to_float(analog: Any = None, buf: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_analog_si_prefix(
        value: Any = None, digits: Any = None
    ) -> CallResult[bytes]: ...
    @staticmethod
    def sr_analog_si_prefix_friendly(unit: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_analog_unit_to_string(
        analog: Any = None, result: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_rational_set(
        r: Any = None, p: Any = None, q: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def sr_rational_eq(a: Any = None, b: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_rational_mult(
        res: Any = None, a: Any = None, b: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_rational_div(
        res: Any = None, num: Any = None, div: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_init(ctx: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_exit(ctx: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_buildinfo_libs_get() -> CallResult[int]: ...
    @staticmethod
    def sr_buildinfo_host_get() -> CallResult[bytes]: ...
    @staticmethod
    def sr_buildinfo_scpi_backends_get() -> CallResult[bytes]: ...
    @staticmethod
    def sr_a2l_threshold(
        analog: Any = None, threshold: Any = None, output: Any = None, count: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_a2l_schmitt_trigger(
        analog: Any = None,
        lo_thr: Any = None,
        hi_thr: Any = None,
        state: Any = None,
        output: Any = None,
        count: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_log_loglevel_set(loglevel: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_log_loglevel_get() -> CallResult[int]: ...
    @staticmethod
    def sr_log_callback_set(cb: Any = None, cb_data: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_log_callback_set_default() -> CallResult[int]: ...
    @staticmethod
    def sr_log_callback_get(cb: Any = None, cb_data: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_channel_name_set(
        channel: Any = None, name: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_channel_enable(
        channel: Any = None, state: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_has_option(sdi: Any = None, key: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_dev_config_capabilities_list(
        sdi: Any = None, cg: Any = None, key: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_options(
        driver: Any = None, sdi: Any = None, cg: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_list(driver: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_clear(driver: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_open(sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_close(sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_inst_driver_get(sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_inst_vendor_get(sdi: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_dev_inst_model_get(sdi: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_dev_inst_version_get(sdi: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_dev_inst_sernum_get(sdi: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_dev_inst_connid_get(sdi: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_dev_inst_channels_get(sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_inst_channel_groups_get(sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_inst_user_new(
        vendor: Any = None, model: Any = None, version: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_dev_inst_channel_add(
        sdi: Any = None, index: Any = None, type_: Any = None, name: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_driver_list(ctx: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_driver_init(ctx: Any = None, driver: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_driver_scan_options_list(driver: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_driver_scan(driver: Any = None, options: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_config_get(
        driver: Any = None,
        sdi: Any = None,
        cg: Any = None,
        key: Any = None,
        data: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_config_set(
        sdi: Any = None, cg: Any = None, key: Any = None, data: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_config_commit(sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_config_list(
        driver: Any = None,
        sdi: Any = None,
        cg: Any = None,
        key: Any = None,
        data: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_key_info_get(keytype: Any = None, key: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_key_info_name_get(
        keytype: Any = None, keyid: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_trigger_get(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_load(
        ctx: Any = None, filename: Any = None, session: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_new(ctx: Any = None, session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_destroy(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_dev_remove_all(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_dev_add(session: Any = None, sdi: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_dev_remove(
        session: Any = None, sdi: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_dev_list(
        session: Any = None, devlist: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_trigger_set(
        session: Any = None, trig: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_datafeed_callback_remove_all(
        session: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_datafeed_callback_add(
        session: Any = None, cb: Any = None, cb_data: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_session_start(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_run(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_stop(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_is_running(session: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_session_stopped_callback_set(
        session: Any = None, cb: Any = None, cb_data: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_packet_copy(packet: Any = None, copy: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_packet_free(packet: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_input_list() -> CallResult[int]: ...
    @staticmethod
    def sr_input_id_get(imod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_input_name_get(imod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_input_description_get(imod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_input_extensions_get(imod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_input_find(id_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_options_get(imod: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_options_free(options: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_input_new(imod: Any = None, options: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_scan_buffer(buf: Any = None, in_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_scan_file(
        filename: Any = None, in_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_input_module_get(in_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_dev_inst_get(in_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_send(in_: Any = None, buf: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_end(in_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_reset(in_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_input_free(in_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_output_list() -> CallResult[int]: ...
    @staticmethod
    def sr_output_id_get(omod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_output_name_get(omod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_output_description_get(omod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_output_extensions_get(omod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_output_find(id_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_output_options_get(omod: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_output_options_free(opts: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_output_new(
        omod: Any = None, params: Any = None, sdi: Any = None, filename: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_output_test_flag(omod: Any = None, flag: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_output_send(
        o: Any = None, packet: Any = None, out: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_output_free(o: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_transform_list() -> CallResult[int]: ...
    @staticmethod
    def sr_transform_id_get(tmod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_transform_name_get(tmod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_transform_description_get(tmod: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_transform_find(id_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_transform_options_get(tmod: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_transform_options_free(opts: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_transform_new(
        tmod: Any = None, params: Any = None, sdi: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_transform_free(t: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_trigger_new(name: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_trigger_free(trig: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_trigger_stage_add(trig: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_trigger_match_add(
        stage: Any = None, ch: Any = None, trigger_match: Any = None, value: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_serial_list(driver: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_serial_free(serial: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_resourcepaths_get(res_type: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_resource_set_hooks(
        ctx: Any = None,
        open_cb: Any = None,
        close_cb: Any = None,
        read_cb: Any = None,
        cb_data: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_si_string_u64(x: Any = None, unit: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_samplerate_string(samplerate: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_period_string(v_p: Any = None, v_q: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_voltage_string(v_p: Any = None, v_q: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_parse_sizestring(
        sizestring: Any = None, size: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_parse_timestring(timestring: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_parse_boolstring(boolstring: Any = None) -> CallResult[None]: ...
    @staticmethod
    def sr_parse_period(
        periodstr: Any = None, p: Any = None, q: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_parse_voltage(
        voltstr: Any = None, p: Any = None, q: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_vsprintf_ascii(
        buf: Any = None, format_: Any = None, args: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_vsnprintf_ascii(
        buf: Any = None, buf_size: Any = None, format_: Any = None, args: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def sr_parse_rational(str_: Any = None, ret: Any = None) -> CallResult[int]: ...
    @staticmethod
    def sr_package_version_major_get() -> CallResult[int]: ...
    @staticmethod
    def sr_package_version_minor_get() -> CallResult[int]: ...
    @staticmethod
    def sr_package_version_micro_get() -> CallResult[int]: ...
    @staticmethod
    def sr_package_version_string_get() -> CallResult[bytes]: ...
    @staticmethod
    def sr_lib_version_current_get() -> CallResult[int]: ...
    @staticmethod
    def sr_lib_version_revision_get() -> CallResult[int]: ...
    @staticmethod
    def sr_lib_version_age_get() -> CallResult[int]: ...
    @staticmethod
    def sr_lib_version_string_get() -> CallResult[bytes]: ...
    @staticmethod
    def sr_strerror(error_code: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def sr_strerror_name(error_code: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def g_slist_free(list_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_slist_free_1(list_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_slist_free_full(
        list_: Any = None, free_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_slist_nth(list_: Any = None, n: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_slist_find(list_: Any = None, data: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_slist_find_custom(
        list_: Any = None, data: Any = None, func: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_slist_position(list_: Any = None, llink: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_slist_index(list_: Any = None, data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_slist_last(list_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_slist_length(list_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_slist_foreach(
        list_: Any = None, func: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_slist_nth_data(list_: Any = None, n: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_clear_slist(
        slist_ptr: Any = None, destroy: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def GLIB_DEPRECATED_TYPE_IN_2_62_FOR() -> CallResult[None]: ...
    @staticmethod
    def g_variant_unref(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_ref(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_ref_sink(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_is_floating(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_take_ref(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_type(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_type_string(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_is_of_type(
        value: Any = None, type_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_is_container(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_classify(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_new_boolean(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_byte(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_int16(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_uint16(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_int32(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_uint32(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_int64(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_uint64(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_handle(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_double(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_string(string: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_take_string(string: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_object_path(object_path: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_is_object_path(string: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_new_signature(signature: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_is_signature(string: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_new_variant(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_strv(strv: Any = None, length: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_objv(strv: Any = None, length: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_bytestring(string: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_bytestring_array(
        strv: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_fixed_array(
        element_type: Any = None,
        elements: Any = None,
        n_elements: Any = None,
        element_size: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_boolean(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_byte(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_int16(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_uint16(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_int32(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_uint32(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_int64(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_uint64(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_handle(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_double(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_variant(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_string(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dup_string(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_strv(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dup_strv(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_objv(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dup_objv(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_bytestring(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dup_bytestring(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_bytestring_array(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dup_bytestring_array(
        value: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_maybe(
        child_type: Any = None, child: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_array(
        child_type: Any = None, children: Any = None, n_children: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_tuple(
        children: Any = None, n_children: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_dict_entry(
        key: Any = None, value: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_maybe(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_n_children(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_child_value(
        value: Any = None, index_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_lookup_value(
        dictionary: Any = None, key: Any = None, expected_type: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_fixed_array(
        value: Any = None, n_elements: Any = None, element_size: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_size(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_data(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_data_as_bytes(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_store(value: Any = None, data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_print(
        value: Any = None, type_annotate: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_print_string(
        value: Any = None, string: Any = None, type_annotate: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_hash(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_equal(one: Any = None, two: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_get_normal_form(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_is_normal_form(value: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_byteswap(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_from_bytes(
        type_: Any = None, bytes_: Any = None, trusted: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_from_data(
        type_: Any = None,
        data: Any = None,
        size: Any = None,
        trusted: Any = None,
        notify: Any = None,
        user_data: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_iter_new(value: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_iter_init(
        iter_: Any = None, value: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_iter_copy(iter_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_iter_n_children(iter_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_iter_free(iter_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_iter_next_value(iter_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_parser_get_error_quark() -> CallResult[None]: ...
    @staticmethod
    def g_variant_parse_error_quark() -> CallResult[None]: ...
    @staticmethod
    def g_variant_builder_new(type_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_builder_unref(builder: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_builder_ref(builder: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_builder_init(
        builder: Any = None, type_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_builder_end(builder: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_builder_clear(builder: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_builder_open(
        builder: Any = None, type_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_builder_close(builder: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_builder_add_value(
        builder: Any = None, value: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_new_va(
        format_string: Any = None, endptr: Any = None, app: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_get_va(
        value: Any = None,
        format_string: Any = None,
        endptr: Any = None,
        app: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_check_format_string(
        value: Any = None, format_string: Any = None, copy_only: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_parse(
        type_: Any = None,
        text: Any = None,
        limit: Any = None,
        endptr: Any = None,
        error: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_new_parsed_va(
        format_: Any = None, app: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_parse_error_print_context(
        error: Any = None, source_str: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_compare(one: Any = None, two: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_dict_new(from_asv: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dict_init(
        dict_: Any = None, from_asv: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_dict_lookup_value(
        dict_: Any = None, key: Any = None, expected_type: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dict_contains(
        dict_: Any = None, key: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_dict_insert_value(
        dict_: Any = None, key: Any = None, value: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_dict_remove(
        dict_: Any = None, key: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_variant_dict_clear(dict_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_variant_dict_end(dict_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dict_ref(dict_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_variant_dict_unref(dict_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_array_new(
        zero_terminated: Any = None, clear_: Any = None, element_size: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_new_take(
        data: Any = None, len_: Any = None, clear: Any = None, element_size: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_new_take_zero_terminated(
        data: Any = None, clear: Any = None, element_size: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_steal(array: Any = None, len_: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_array_sized_new(
        zero_terminated: Any = None,
        clear_: Any = None,
        element_size: Any = None,
        reserved_size: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_copy(array: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_array_free(
        array: Any = None, free_segment: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_ref(array: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_array_unref(array: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_array_get_element_size(array: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_array_append_vals(
        array: Any = None, data: Any = None, len_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_prepend_vals(
        array: Any = None, data: Any = None, len_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_insert_vals(
        array: Any = None, index_: Any = None, data: Any = None, len_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_set_size(array: Any = None, length: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_array_remove_index(
        array: Any = None, index_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_remove_index_fast(
        array: Any = None, index_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_remove_range(
        array: Any = None, index_: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_array_sort(
        array: Any = None, compare_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_array_sort_with_data(
        array: Any = None, compare_func: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_array_binary_search(
        array: Any = None,
        target: Any = None,
        compare_func: Any = None,
        out_match_index: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_array_set_clear_func(
        array: Any = None, clear_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_new() -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_with_free_func(
        element_free_func: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_take(
        data: Any = None, len_: Any = None, element_free_func: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_from_array(
        data: Any = None,
        len_: Any = None,
        copy_func: Any = None,
        copy_func_user_data: Any = None,
        element_free_func: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_steal(array: Any = None, len_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_copy(
        array: Any = None, func: Any = None, user_data: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_sized_new(reserved_size: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_full(
        reserved_size: Any = None, element_free_func: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_null_terminated(
        reserved_size: Any = None,
        element_free_func: Any = None,
        null_terminated: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_take_null_terminated(
        data: Any = None, element_free_func: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_new_from_null_terminated_array(
        data: Any = None,
        copy_func: Any = None,
        copy_func_user_data: Any = None,
        element_free_func: Any = None,
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_free(
        array: Any = None, free_seg: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_ref(array: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_unref(array: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_set_free_func(
        array: Any = None, element_free_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_set_size(
        array: Any = None, length: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_remove_index(
        array: Any = None, index_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_remove_index_fast(
        array: Any = None, index_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_steal_index(
        array: Any = None, index_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_steal_index_fast(
        array: Any = None, index_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_remove(array: Any = None, data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_remove_fast(
        array: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_remove_range(
        array: Any = None, index_: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_ptr_array_add(array: Any = None, data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_extend(
        array_to_extend: Any = None,
        array: Any = None,
        func: Any = None,
        user_data: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_extend_and_steal(
        array_to_extend: Any = None, array: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_insert(
        array: Any = None, index_: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_sort(
        array: Any = None, compare_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_sort_with_data(
        array: Any = None, compare_func: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_sort_values(
        array: Any = None, compare_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_sort_values_with_data(
        array: Any = None, compare_func: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_foreach(
        array: Any = None, func: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_find(
        haystack: Any = None, needle: Any = None, index_: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_find_with_equal_func(
        haystack: Any = None,
        needle: Any = None,
        equal_func: Any = None,
        index_: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_ptr_array_is_null_terminated(array: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_byte_array_new() -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_new_take(
        data: Any = None, len_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_steal(array: Any = None, len_: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_sized_new(reserved_size: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_free(
        array: Any = None, free_segment: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_free_to_bytes(array: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_ref(array: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_unref(array: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_byte_array_append(
        array: Any = None, data: Any = None, len_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_prepend(
        array: Any = None, data: Any = None, len_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_set_size(
        array: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_remove_index(
        array: Any = None, index_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_remove_index_fast(
        array: Any = None, index_: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_remove_range(
        array: Any = None, index_: Any = None, length: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_byte_array_sort(
        array: Any = None, compare_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_byte_array_sort_with_data(
        array: Any = None, compare_func: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_new() -> CallResult[int]: ...
    @staticmethod
    def g_main_context_new_with_flags(flags: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_main_context_ref(context: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_main_context_unref(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_default() -> CallResult[int]: ...
    @staticmethod
    def g_main_context_iteration(
        context: Any = None, may_block: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_pending(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_find_source_by_id(
        context: Any = None, source_id: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_main_context_find_source_by_user_data(
        context: Any = None, user_data: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_main_context_find_source_by_funcs_user_data(
        context: Any = None, funcs: Any = None, user_data: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_main_context_wakeup(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_acquire(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_release(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_is_owner(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_wait(
        context: Any = None, cond: Any = None, mutex: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_prepare(
        context: Any = None, priority: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_query(
        context: Any = None,
        max_priority: Any = None,
        timeout_: Any = None,
        fds: Any = None,
        n_fds: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_check(
        context: Any = None,
        max_priority: Any = None,
        fds: Any = None,
        n_fds: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_dispatch(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_set_poll_func(
        context: Any = None, func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_get_poll_func(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_add_poll(
        context: Any = None, fd: Any = None, priority: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_remove_poll(
        context: Any = None, fd: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_depth() -> CallResult[None]: ...
    @staticmethod
    def g_main_current_source() -> CallResult[int]: ...
    @staticmethod
    def g_main_context_push_thread_default(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_pop_thread_default(context: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_get_thread_default() -> CallResult[int]: ...
    @staticmethod
    def g_main_context_ref_thread_default() -> CallResult[int]: ...
    @staticmethod
    def g_main_context_pusher_new(main_context: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_main_context_pusher_free(pusher: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_loop_new(
        context: Any = None, is_running: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_main_loop_run(loop: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_loop_quit(loop: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_loop_ref(loop: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_main_loop_unref(loop: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_loop_is_running(loop: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_loop_get_context(loop: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_source_new(
        source_funcs: Any = None, struct_size: Any = None
    ) -> CallResult[int]: ...
    @staticmethod
    def g_source_set_dispose_function(
        source: Any = None, dispose: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_ref(source: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_source_unref(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_attach(
        source: Any = None, context: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_destroy(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_priority(
        source: Any = None, priority: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_priority(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_can_recurse(
        source: Any = None, can_recurse: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_can_recurse(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_id(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_context(source: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_source_set_callback(
        source: Any = None, func: Any = None, data: Any = None, notify: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_funcs(
        source: Any = None, funcs: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_is_destroyed(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_name(source: Any = None, name: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_static_name(
        source: Any = None, name: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_name(source: Any = None) -> CallResult[bytes]: ...
    @staticmethod
    def g_source_set_name_by_id(
        tag: Any = None, name: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_ready_time(
        source: Any = None, ready_time: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_ready_time(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_set_callback_indirect(
        source: Any = None, callback_data: Any = None, callback_funcs: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_add_poll(source: Any = None, fd: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_remove_poll(
        source: Any = None, fd: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_add_child_source(
        source: Any = None, child_source: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_remove_child_source(
        source: Any = None, child_source: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_current_time(
        source: Any = None, timeval: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_source_get_time(source: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_idle_source_new() -> CallResult[int]: ...
    @staticmethod
    def g_child_watch_source_new(pid: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_timeout_source_new(interval: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_timeout_source_new_seconds(interval: Any = None) -> CallResult[int]: ...
    @staticmethod
    def g_get_current_time(result: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_get_monotonic_time() -> CallResult[None]: ...
    @staticmethod
    def g_get_real_time() -> CallResult[None]: ...
    @staticmethod
    def g_source_remove(tag: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_remove_by_user_data(user_data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_source_remove_by_funcs_user_data(
        funcs: Any = None, user_data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_clear_handle_id(
        tag_ptr: Any = None, clear_func: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_timeout_add_full(
        priority: Any = None,
        interval: Any = None,
        function: Any = None,
        data: Any = None,
        notify: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_timeout_add(
        interval: Any = None, function: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_timeout_add_once(
        interval: Any = None, function: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_timeout_add_seconds_full(
        priority: Any = None,
        interval: Any = None,
        function: Any = None,
        data: Any = None,
        notify: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_timeout_add_seconds(
        interval: Any = None, function: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_timeout_add_seconds_once(
        interval: Any = None, function: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_child_watch_add_full(
        priority: Any = None,
        pid: Any = None,
        function: Any = None,
        data: Any = None,
        notify: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_child_watch_add(
        pid: Any = None, function: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_idle_add(function: Any = None, data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_idle_add_full(
        priority: Any = None, function: Any = None, data: Any = None, notify: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_idle_add_once(function: Any = None, data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_idle_remove_by_data(data: Any = None) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_invoke_full(
        context: Any = None,
        priority: Any = None,
        function: Any = None,
        data: Any = None,
        notify: Any = None,
    ) -> CallResult[None]: ...
    @staticmethod
    def g_main_context_invoke(
        context: Any = None, function: Any = None, data: Any = None
    ) -> CallResult[None]: ...
    @staticmethod
    def g_steal_fd(fd_ptr: Any = None) -> CallResult[int]: ...
