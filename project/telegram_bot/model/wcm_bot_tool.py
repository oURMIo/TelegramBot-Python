class WCMBotTool:
    def __init__(self, last_notif_data):
        self.last_notif_data = last_notif_data

    def __repr__(self):
        return f"WCMBotTool(last_notif_data={self.last_notif_data})"


def parse_wcmbot_tool_json(data):
    if isinstance(data, dict) and "last_notif_data" in data:
        return [WCMBotTool(last_notif_data=data["last_notif_data"])]
    return []
