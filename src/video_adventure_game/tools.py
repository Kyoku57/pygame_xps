def update_splash_text(message, close=False):
    """Use by pyinstaller to enhance message in splash screen"""
    print(message)
    try:
        import pyi_splash
        pyi_splash.update_text(message)
        if close is True:
             pyi_splash.close()
    except:
        pass