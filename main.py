import webview

if __name__ == '__main__':
  webview.create_window("Morpho The Converter", 'frontend/index.html')
  webview.start(gui="qt")