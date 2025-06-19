from dotenv import load_dotenv
import app.controllers.SynchronisationHandler as synchronizationHandler

def main() -> None:
    load_dotenv(override=True)
    sync = synchronizationHandler.SynchronizationHandler()
    sync.run()

if __name__ == "__main__":
    main()