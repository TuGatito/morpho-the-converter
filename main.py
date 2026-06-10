import webview
from backend.api import API

if __name__ == "__main__":
    api = API()
    webview.create_window("Morpho The Converter", url="./frontend/index.html", frameless=True, js_api=api)
    webview.start()
    