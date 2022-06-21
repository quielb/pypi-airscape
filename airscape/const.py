DEFAULT_TIMEOUT = 5
MAX_FAN_SPEED = {"default": 10, "1.7WHF": 2, "3.5eWHF": 7, "4.4eWHF": 6}
STATUS_KEYS = {
    "fanspd": "fanspd",
    "doorinprocess": "doorinprocess",
    "timeremaining": "timeremaining",
    "macaddr": "macaddr",
    "ipaddr": "ipaddr",
    "model": "model",
    "softver": "softver",
    "interlock1": "interlock1",
    "interlock2": "interlock2",
    "cfm": "cfm",
    "power": "power",
    "inside": "house_temp",
    "attic": "attic_temp",
    "oa": "oa_temp",
    "dip_switches": "DIPS",
    "remote_switch": "switch2",
    "setpoint": "Setpoint",
    "dns": "DNS1",
}
CAST_TO_INT = [
    "fanspd",
    "timeremaining",
    "cfm",
    "power",
    "inside",
    "attic",
    "oa",
    "doorinprocess",
]
