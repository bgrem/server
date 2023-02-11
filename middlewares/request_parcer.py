from functools import wraps
from models.Error import Error
from utils.common import CommonUtils
from flask import request

class RequestParcer:

    def validate_request(request_body_template: dict = {}, request_files_template: dict = {}):
        """
        request_body_template: The key should be the key of the request body and the value should be the type of it, if no type then it should be None.
        request_files_template: The key should be the name of the file expected and the value should be None.

        """
        def _validate_request(f):
            @wraps(f)
            def __validate_request(*args,**kwargs):
                RequestParcer.validate_request_body(request_body_template, []) 
                RequestParcer.validate_request_files(request_files_template)
                return f(*args,**kwargs)
            return __validate_request
        return _validate_request
    
    def validate_request_body(request_body_template: dict, key_list: list = []):
        request_body = request.get_json(silent = True)
        if not request_body and len(request_body_template.keys()) != 0:
            raise Error("request body not provided", 400)
        # `required_type` can be a dict or a type class. TODO: Find a better name for that variable.
        for (key, required_type) in request_body_template.items():
            (is_key_exists, value, missing_key) = CommonUtils.get_value_from_dict_with_list(key_list=key_list + [key],target_dict=request_body)
            if not is_key_exists:
                raise Error(f"'{missing_key}' is not provided", 400)
            if isinstance(required_type,dict):
                if not isinstance(value,dict):
                    raise Error(f"'{key}' is not the correct type", 400, {"required_type":"dict"})
                # The adding and poping of the key list is to update the `key_list` properly.
                key_list.append(key)
                RequestParcer.validate_request_body(required_type,key_list)
                key_list.pop()
            elif isinstance(required_type,type):
                if not request_body:
                    raise Error("No request body provided",400)
                if not isinstance(value,required_type):
                    raise Error(f"'{key}' is not the correct type", 400, {"required_type":required_type.__name__})
        return True

    def validate_request_files(request_files_template: dict):
        # TODO: Find edge cases
        for (file_key,value) in request_files_template.items():
            file = request.files.get(file_key)
            if not file:
                raise Error(f"'{file_key}' file not found",400)
        return True