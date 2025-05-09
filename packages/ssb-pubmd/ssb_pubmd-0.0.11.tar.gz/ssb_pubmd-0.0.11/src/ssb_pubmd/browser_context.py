from playwright.sync_api import BrowserContext
from playwright.sync_api import StorageState
from playwright.sync_api import sync_playwright

from .markdown_syncer import Response

BROWSER_CONTEXT_FILE = "browser_context.json"


class BrowserRequestContext:
    """This class is used to create a logged in browser context from which to send requests."""

    def __init__(self) -> None:
        """Initializes an empty browser context object."""
        self._storage_state_path: str = BROWSER_CONTEXT_FILE
        self._context: BrowserContext | None = None

    def create_new(self, login_url: str) -> tuple[str, StorageState]:
        """Creates a browser context by opening a login page and waiting for it to be closed by user.

        This function also saves the browser context to a file for later use.
        """
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)

        self._context = browser.new_context()
        login_page = self._context.new_page()

        login_page.goto(login_url)
        login_page.wait_for_event("close", timeout=0)

        storage_state = self._context.storage_state(path=self._storage_state_path)

        return self._storage_state_path, storage_state

    def recreate_from_file(self) -> BrowserContext:
        """Recreates a browser context object from a file."""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)

        self._context = browser.new_context(storage_state=self._storage_state_path)

        return self._context

    def send_request(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
    ) -> Response:
        """Sends a request to the specified url, optionally with headers and data, within the browser context."""
        if self._context is None:
            raise ValueError("Browser context has not been created.")

        # print(self._context.cookies(url))

        api_response = self._context.request.post(
            url,
            data=data,
        )

        try:
            body = api_response.json()
            body = dict(body)
        except Exception:
            body = None

        response = Response(
            status_code=api_response.status,
            body=body,
        )

        return response
