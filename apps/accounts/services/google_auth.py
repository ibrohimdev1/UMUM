import os
import json
import urllib.request
import urllib.parse
from django.conf import settings

class GoogleAuthService:
    @classmethod
    def get_client_id(cls):
        return os.getenv('GOOGLE_CLIENT_ID')

    @classmethod
    def get_client_secret(cls):
        return os.getenv('GOOGLE_CLIENT_SECRET')

    @classmethod
    def get_redirect_uri(cls, request=None):
        if request and 'localhost' in request.get_host():
            return 'http://localhost:8000/auth/google/callback/'
        return 'http://127.0.0.1:8000/auth/google/callback/'

    @classmethod
    def is_configured(cls):
        return bool(cls.get_client_id() and cls.get_client_secret())

    @classmethod
    def get_authorization_url(cls, request):
        client_id = cls.get_client_id()
        if not client_id:
            return None, None
        redirect_uri = cls.get_redirect_uri(request)
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'select_account',
        }
        url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return url, redirect_uri

    @classmethod
    def exchange_code_for_user_info(cls, code: str, redirect_uri: str):
        client_id = cls.get_client_id()
        client_secret = cls.get_client_secret()

        token_url = "https://oauth2.googleapis.com/token"
        payload = urllib.parse.urlencode({
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }).encode('utf-8')

        req = urllib.request.Request(
            token_url,
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                token_data = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raw_err = e.read().decode('utf-8')
            try:
                err_json = json.loads(raw_err)
                err_code = err_json.get('error', '')
                err_desc = err_json.get('error_description', raw_err)
                if 'redirect_uri_mismatch' in err_code:
                    raise Exception(f"Redirect URI nomuvofiqligi: Google Cloud Console'da {redirect_uri} ruxsat berilgan manzillarga qo‘shilishi kerak.")
                elif 'invalid_client' in err_code:
                    raise Exception("Google Client ID yoki Client Secret noto‘g‘ri kiritilgan.")
                else:
                    raise Exception(f"Google xatosi ({err_code}): {err_desc}")
            except Exception:
                raise Exception(f"Google Token xatosi: {raw_err}")

        access_token = token_data.get('access_token')
        if not access_token:
            return None

        # Fetch profile information from Google
        userinfo_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
        req_info = urllib.request.Request(userinfo_url)
        try:
            with urllib.request.urlopen(req_info, timeout=12) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            raise Exception(f"Google Userinfo xatosi: {err_body}")

