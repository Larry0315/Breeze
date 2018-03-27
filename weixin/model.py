
class WeiXinModel:

    def __init__(self, group_name: str, content: str, from_app: str="", event_id: int=0, event_type: bool=False):
        self.group: str = group_name
        self.content: str = content
        self.from_app: str = from_app
        self.event_id: int = event_id
        self.event_type: bool = event_type
