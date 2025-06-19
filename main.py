from dotenv import load_dotenv
from app.controllers.app import GuiApp

def main() -> None:
    load_dotenv(override=True)

    app = GuiApp()
    app.run()

if __name__ == "__main__":
    main()