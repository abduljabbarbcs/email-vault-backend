# middlewares/sanitize_middleware.py
import bleach
from flask import request, current_app
import json

class RequestSanitizationMiddleware:
    def __init__(self, app):
        self.app = app
        self.app.before_request(self.sanitize_request_body)

    def sanitize_request_body(self):
        if request.is_json:
            try:
                # Fetch the original JSON data
                body = request.get_json(force=True)
                # Sanitize it
                sanitized_body = self.sanitize_input(body)
                # Update request.data and request._cached_json
                request.data = json.dumps(sanitized_body).encode('utf-8')
                request._cached_json = sanitized_body
            except Exception as e:
                current_app.logger.error(f"Error sanitizing request: {e}")

    def sanitize_input(self, data):
        if isinstance(data, dict):
            return {key: self.sanitize_input(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_input(item) for item in data]
        elif isinstance(data, str):
            return bleach.clean(data)
        else:
            return data
