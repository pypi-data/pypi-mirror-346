from mobio.libs.ciphers import MobioCrypt4

from .call_api import CallAPI
from .config import (
    CodeErrorDecrypt, CodeErrorEncrypt
)
from .utils import (
    split_list, build_response_from_list
)


class EncryptFieldUtils:

    @classmethod
    def get_info_field_config(cls, merchant_id, module, field):
        field_config = {}
        try:
            fields_config = CallAPI.get_list_fields_config_encrypt(merchant_id, module)
            if fields_config:
                for item in fields_config:
                    if item.get("enc_level") == "enc_frontend":
                        # voi level nay ko can sdk ma hoa, module tu convert ve ***
                        continue
                    if item.get("field") == field and module == item.get("module"):
                        field_config.update({
                            "kms_id": item.get("kms_id"),
                            "kms_info": item.get("kms_info"),
                        })
                        break

        except Exception as e:
            print("admin_sdk::get_kms_id_from_fields_config: error: {}".format(e))
        return field_config

    @staticmethod
    def build_response_from_list(list_value):
        data = {}
        for item in list_value:
            data[item] = item
        return {"code": 200, "data": data}

    @classmethod
    def encrypt_field_by_config(cls, merchant_id, module, field, values):
        field_config = cls.get_info_field_config(merchant_id, module, field)
        data_response = cls.process_encrypt_by_kms(values, field_config)
        return data_response

    @staticmethod
    def process_kms_mobio_encrypt(values):
        data = {}
        data_error = {}
        for item in values:
            if not item:
                continue
            try:
                item_format = MobioCrypt4.e1(item)
            except:
                item_format = None
            if item_format:
                data[item] = item_format
            else:
                data_error[item] = CodeErrorEncrypt.encrypt_error
        return {"data": data, "data_error": data_error}

    @classmethod
    def decrypt_field_by_config(cls, merchant_id, module, field, values):
        field_config = cls.get_info_field_config(merchant_id, module, field)
        data_response = cls.process_decrypt_by_kms(values, field_config)
        return data_response

    @staticmethod
    def process_kms_mobio_decrypt(values):
        data = {}
        data_error = {}
        for item in values:
            if not item:
                continue
            try:
                item_format = MobioCrypt4.d1(item, enc='UTF-8')
            except:
                item_format = None
            if item_format:
                data[item] = item_format
            else:
                data_error[item] = CodeErrorDecrypt.decrypt_error
        return {"data": data, "data_error": data_error}

    @staticmethod
    def process_kms_viettel_encrypt(kms_info, list_data):
        data_response = {"data": {}, "data_error": {}}
        try:
            kms_id = kms_info.get("kms_id")
            access_token = CallAPI.kms_viettel_get_token(kms_id)
            if access_token:
                list_chunk = split_list(list_data, 50)
                for chunk in list_chunk:
                    data_result = CallAPI.request_kms_viettel_encrypt(kms_info, access_token, chunk)
                    data_response["data"].update(data_result.get("data", {}))
                    data_response["data_error"].update(data_result.get("data_error", {}))
                return data_response
        except Exception as er:
            print("admin_sdk::process_kms_viettel_encrypt: error: {}".format(er))
        data_response["data_error"] = CallAPI.build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
        return data_response

    @staticmethod
    def process_kms_viettel_decrypt(kms_info, list_data):
        data_response = {"data": {}, "data_error": {}}
        try:
            kms_id = kms_info.get("kms_id")
            access_token = CallAPI.kms_viettel_get_token(kms_id)
            if access_token:
                list_chunk = split_list(list_data, 50)
                for chunk in list_chunk:
                    data_result = CallAPI.request_kms_viettel_decrypt(kms_info, access_token, chunk)
                    data_response["data"].update(data_result.get("data", {}))
                    data_response["data_error"].update(data_result.get("data_error", {}))
                return data_response
        except Exception as er:
            print("admin_sdk::process_kms_viettel_decrypt: error: {}".format(er))
        data_response["data_error"] = CallAPI.build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
        return data_response

    @classmethod
    def process_decrypt_by_kms(cls, values, field_config):
        kms_id, kms_info = None, None
        if field_config and isinstance(field_config, dict):
            kms_id = field_config.get("kms_id")
            kms_info = field_config.get("kms_info")
        if isinstance(values, str):
            values = [values]
        if kms_id and kms_info:
            kms_type = kms_info.get("kms_type", "kms_mobio")
            if kms_type == "kms_mobio":
                data_response = cls.process_kms_mobio_decrypt(values)
            elif kms_type == "kms_viettel":
                data_response = cls.process_kms_viettel_decrypt(kms_info, values)
            else:
                data_response = build_response_from_list(values)
        else:
            data_response = build_response_from_list(values)
        return data_response

    @classmethod
    def process_encrypt_by_kms(cls, values, field_config):
        kms_id, kms_info = None, None
        if field_config and isinstance(field_config, dict):
            kms_id = field_config.get("kms_id")
            kms_info = field_config.get("kms_info")
        if isinstance(values, str):
            values = [values]
        if kms_id and kms_info:
            kms_type = kms_info.get("kms_type", "kms_mobio")
            if kms_type == "kms_mobio":
                data_response = cls.process_kms_mobio_encrypt(values)
            elif kms_type == "kms_viettel":
                data_response = cls.process_kms_viettel_encrypt(kms_info, values)
            else:
                data_response = build_response_from_list(values)
        else:
            data_response = build_response_from_list(values)
        return data_response

    @staticmethod
    def masking_value_by_config(value, format_logic, use_format="allow", symbol_mas="*"):
        value = str(value)
        start = end = 0
        if use_format == "allow" and isinstance(format_logic, dict):
            start = int(format_logic.get("start", 0)) if isinstance(format_logic.get(
                "start", 0), (int, float)) and format_logic.get("start", 0) > 0 else 0
            end = int(format_logic.get("end", 0)) if isinstance(format_logic.get(
                "end", 0), (int, float)) and format_logic.get("end", 0) > 0 else 0
        len_value = len(value)
        if start + end + 3 > len_value:
            return symbol_mas * len_value
        value_end = ""
        if end > 0:
            value_end = value[-end:]
        return value[:start] + symbol_mas * (len_value - start - end) + value_end
