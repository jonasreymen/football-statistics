from app.sync.locator.locator import Locator

class NullLocator(Locator):
    def locate(self, obj: object) -> None:
        return