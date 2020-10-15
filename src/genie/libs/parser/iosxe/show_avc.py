import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional


# =====================================
# Schema for:
#  * 'show avc sd-service info summary'
# =====================================
class ShowAvcSdServiceInfoSummarySchema(MetaParser):
    """Schema for show avc sd-service info summary."""

    schema = {
        Optional("active_controller"): {
            Optional("ip"): str,
            "status": str,
            Optional("type"): "Primary",
        },
        Optional("device"): {
            "id": str,
            "address": str,
            "segment_name": str,
        },
        "sdavc": {"status": str},
    }


# =====================================
# Parser for:
#  * 'show avc sd-service info summary'
# =====================================
class ShowAvcSdServiceInfoSummary(ShowAvcSdServiceInfoSummarySchema):
    """Parser for show avc sd-service info summary"""

    cli_command = ["show avc sd-service info summary"]

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command[0])

        # Status: CONNECTED
        # Device ID: sd-sw2.lab.com
        # Device segment name: core-pop
        # Device address: 10.18.29.33

        # Active controller:
        #    Type  : Primary
        #    IP    : 10.11.236.21
        #    Status: Connected
        #    Last connection: 18:42:02.000 UTC Fri Oct 2 2020

        avc_connected_capture = (
            # Status: CONNECTED
            r"^Status: (?P<sdavc_status>CONNECTED)\s+"
            # Device ID: sd-sw2.lab.com
            r"Device ID: (?P<device_id>\S+)\s+"
            # Device segment name: core-pop
            r"Device segment name: (?P<device_segment_name>\S+)\s+"
            # Device address: 10.18.29.33
            r"Device address: (?P<device_address>\d+\.\d+\.\d+\.\d+|\S+\:\:\S+\:\S+\:\S+\:\S+)\s+"
            # Active controller:
            r"Active controller:\s+"
            #    Type  : Primary
            r"Type\s+: (?P<active_controller_type>\S+)\s+"
            #    IP    : 10.11.236.21
            r"IP\s+: (?P<active_controller_ip>\d+\.\d+\.\d+\.\d+|\S+\:\:\S+\:\S+\:\S+\:\S+)\s+"
            #    Status: Connected
            r"Status: (?P<active_controller_status>\S+)\s+"
            #    Last connection: 18:42:02.000 UTC Fri Oct 2 2020
            r"Last connection: (?P<active_contoller_last_connection>.+)$"
        )

        # Status: DISCONNECTED

        # Device ID:
        # Device segment name: global (default)
        # Device address: 0.0.0.0

        # Controller address isn't configured

        avc_disconnected_capture = (
            # Status: DISCONNECTED
            r"^Status: (?P<sdavc_status>DISCONNECTED)\s+"
            # Device ID:
            r"Device ID: (?P<device_id>)\s+"
            # Device segment name: global (default)
            r"Device segment name: (?P<device_segment_name>\S+) \(default\)\s+"
            # Device address: 0.0.0.0
            r"Device address: (?P<device_address>\d+\.\d+\.\d+\.\d+|\S+\:\:\S+\:\S+\:\S+\:\S+)\s+"
        )

        # SD-AVC is disabled

        avc_disabled_capture = (
            # SD-AVC is disabled
            r"^SD-AVC is disabled"
        )

        avc_info_obj = {}

        capture_list = [
            avc_connected_capture,
            avc_disconnected_capture,
            avc_disabled_capture,
        ]

        for capture in capture_list:
            if re.search(capture, output, re.MULTILINE):
                search = re.search(capture, output, re.MULTILINE)

                if capture == avc_connected_capture or avc_disconnected_capture:

                    key_list = ["sdavc", "active_controller", "device"]

                    group = search.groupdict()

                    # iterate through key_list to format the keys in group
                    for key in key_list:
                        new_group = {key: {}}

                        for item in group:
                            # if the key from key_list is found in item
                            if f"{key}_" in item:
                                # replace the key and update with new_dict
                                new_key = re.sub(f"{key}_", "", item)
                                new_dict = {new_key: group[item]}
                                new_group[key].update(new_dict)

                        avc_info_obj.update(new_group)

                    # if active_controller is an empty dict, update it to show it's not configured
                    if not avc_info_obj["active_controller"].get("status"):
                        avc_info_obj["active_controller"] = {"status": "not configured"}

                if capture == avc_disabled_capture:
                    avc_info_obj = {"sdavc": {"status": "DISABLED"}}

        return avc_info_obj