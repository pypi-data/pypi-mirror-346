import requests
import pyotp
import json
from dotenv import load_dotenv
import os
import pathlib
import http.cookiejar as cj
from v3cap.captcha import get_recaptcha_token as fetch_recaptcha_token

load_dotenv()

# Get config directory in user's home
def get_config_dir():
    config_dir = pathlib.Path.home() / ".config" / "tbd-api"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

# Default cookies file path in user's home directory
default_cookies_file = str(get_config_dir() / "cookies.txt")
cookies_file = os.environ.get("COOKIES_PATH", default_cookies_file)

session = requests.Session()
headers = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}


def set_credentials(username=None, password=None, totp_secret=None):
    """Set credentials as environment variables"""
    if username:
        os.environ["USERNAME"] = username
    if password:
        os.environ["PASSWORD"] = password
    if totp_secret:
        os.environ["TOTP_SECRET"] = totp_secret


def get_recaptcha_token():
    print("🔄 Requesting reCAPTCHA token...")
    try:
        token = fetch_recaptcha_token(
            site_key="6Lci27UZAAAAAPMvFNNodcgJhYyB8D3MrnaowTqe",
            page_url="https://www.torrentbd.net"
        )
        if not token:
            raise ValueError("No token returned")
        print("✅ reCAPTCHA token received")
        return token
    except Exception as e:
        print(f"❌ Failed to get reCAPTCHA token: {e}")
        exit(1)


def is_cookie_file_valid(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return len(f.read().strip()) > 0
    except:
        return False


def check_login_status():
    global cookies_file
    # Update cookies file path from environment if set
    cookies_file = os.environ.get("COOKIES_PATH", default_cookies_file)
    
    logged_in = False
    if os.path.exists(cookies_file) and is_cookie_file_valid(cookies_file):
        print(f"🍪 Loading cookies from {cookies_file}...")
        cookiejar = cj.MozillaCookieJar(cookies_file)
        try:
            cookiejar.load(ignore_discard=True, ignore_expires=True)
            session.cookies = cookiejar
        except Exception as e:
            print(f"⚠️ Failed to load cookies properly: {e}")
        else:
            try:
                resp = session.get("https://www.torrentbd.net/", headers=headers)
                if "home - torrentbd" in resp.text.lower():
                    print("✅ Cookies are valid. Already logged in.")
                    logged_in = True
                else:
                    print("⚠️ Cookies loaded but user seems not logged in.")
            except Exception as e:
                print(f"❌ Failed to verify login: {e}")
    else:
        print(f"📂 No valid cookie file at {cookies_file}.")
    return logged_in


def login():
    # Check for required credentials
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    totp_secret = os.environ.get("TOTP_SECRET")
    
    if not all([username, password, totp_secret]):
        print("❌ Missing credentials. Please provide username, password, and TOTP secret.")
        print("   Use --username, --password, --totp-secret options or set environment variables.")
        exit(1)
    
    token = get_recaptcha_token()
    otp = pyotp.TOTP(totp_secret).now()
    print(f"🔐 Generated OTP: {otp}")

    payload = {
        "username": username,
        "password": password,
        "auth_login": "",
        "recaptcha_token": token,
        "otp": otp,
        "login_phase": "2",
        "_remember": "yes",
        "extra": ""
    }

    try:
        response = session.post("https://www.torrentbd.net/ajtakelogin.php", data=payload, headers=headers)
        if "login successful" in response.text.lower():
            print("✅ Login successful!")
            # Ensure directory exists
            os.makedirs(os.path.dirname(cookies_file), exist_ok=True)
            # Save cookies
            cookiejar_obj = cj.MozillaCookieJar(cookies_file)
            for c in session.cookies:
                cookiejar_obj.set_cookie(c)
            cookiejar_obj.save(ignore_discard=True, ignore_expires=True)
            print(f"🍪 Cookies saved to {cookies_file}")
        else:
            print("❌ Login failed. Check credentials or CAPTCHA.")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Login request failed: {e}")


if __name__ == "__main__":
    if not check_login_status():
        login()
