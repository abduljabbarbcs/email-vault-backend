from flask import Flask, request
from flask_cors import CORS
from api.signup import signup_bp
from api.signin import signin_bp
from api.reset_password import reset_bp
from api.resend_email import resend_bp
from middlewares.sanitize_middleware import RequestSanitizationMiddleware

app = Flask(__name__)
# sanitizer = RequestSanitizationMiddleware(app)

# Register authentication routes
app.register_blueprint(signup_bp, url_prefix='/api/signup')
app.register_blueprint(signin_bp, url_prefix='/api/signin')
app.register_blueprint(reset_bp, url_prefix='/api/reset')
app.register_blueprint(resend_bp, url_prefix='/api/resend-email')
CORS(app, support_credentials=False, origins=["*"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
