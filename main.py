import webview

if __name__ == "__main__":
    webview.create_window("Morpho The Converter", url="./frontend/index.html", frameless=True)
    webview.start()
    