class Error(Exception):
    def __init__(
        self,
        message:str,
        status_code:int,
        extra_fields:dict = {}
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.extra_fields = extra_fields
