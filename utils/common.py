from models.Error import Error

class CommonUtils:
    def get_response(message:str,status_code:int,extra_fields:dict = {}):
        return { "message":message, "data":extra_fields }, status_code
    
    def get_error_response(error:Error):
        return { "message":error.message, "data":error.extra_fields }, error.status_code
    
    def get_value_from_dict_with_list(key_list:list,target_dict:dict) -> tuple:
        """
        This function returns a tuple where the first value will be if that key exists,
        and the second value will be the value,
        and the third value will be the missing key if a key is missing

        """
        value = target_dict
        for key in key_list:
            if key in value:
                value = value[key]
            else:
                return (False, None, key)
        return (True, value, None)