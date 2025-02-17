from sqlalchemy.inspection import inspect
import re
from flask import Response, json
from flask import current_app
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask_jwt_extended import decode_token


class Helper: 
    
    @staticmethod
    def object_to_dict(obj):
        return {
            k: v.value if hasattr(v, 'value') else v
            for k, v in inspect(obj).attrs.items()
        }
    
    def merged_record(self, record):
        result = []
        
        for db, user_info in record:
                if user_info is None:
                    record = {
                        **self.object_to_dict(db),
                        "lc_flag": None
                    }
                else:
                    record = {
                        **self.object_to_dict(db),
                        "lc_flag": user_info.lc_flag
                    }
                result.append(record)
                
        return result
    
    @staticmethod
    def email_validator(email):
        """Validates an email address format."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def create_error_response(status_code, message):
        """Generates a reusable error response in JSON format."""
        response = {
            "statusCode": status_code,
            "message": message,
        }
        return Response(json.dumps(response), status=status_code, mimetype='application/json')

    @staticmethod
    def create_success_response(message, data={}):
        """Generates a reusable success response in JSON format."""
        response = {
            "message": "Success" if message == "" else message,
            **data
        }
        
        return Response(json.dumps(response), status=200, mimetype='application/json')

    @staticmethod
    def method_not_allowed():
        """Generates a reusable method error response in JSON format."""
        response = {
            "statusCode": 405, 
            "message": "Method Not Allowed",
            "data": "This requests is not allowed for this endpoint."
        }
        return Response(json.dumps(response), status=405, mimetype='application/json')

    @staticmethod
    def internal_server_error():
        """Generates a reusable error response in JSON format."""
        response = {
            "statusCode": 500, 
            "message": "Internal Server Error",
            "data": "An Unexpected error has occurred."
        }
        return Response(json.dumps(response), status=500, mimetype='application/json')
    
    @staticmethod
    def validate_jwt_token(token):
        try:
            user = decode_token(token)
            return user
        except ExpiredSignatureError:
            current_app.logger.info("Token expired")
            # return Response("Token expired", status=401)
            return Helper.create_error_response(401, "Token expired")
        except InvalidTokenError:
            # If the token is invalid for any other reason, return an error message
            return Helper.create_error_response(401, "Invalid token.")  

