# main.py
from ui.app import ModernApp

if __name__ == "__main__":
    app = ModernApp()
    try:
        app.mainloop()
    finally:
        import asyncio
        if hasattr(app, 'loop') and app.loop.is_running():
            app.loop.call_soon_threadsafe(app.loop.stop)
