# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/ltm/monitor/wap' resources
# =============================================


class LtmMonitorWapSchema(MetaParser):

    schema = {}


class LtmMonitorWap(LtmMonitorWapSchema):
    """ To F5 resource for /mgmt/tm/ltm/monitor/wap
    """

    cli_command = "/mgmt/tm/ltm/monitor/wap"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
