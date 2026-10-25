"""HTTP layer: polite fetching with delay, User-Agent and status check."""

import time
import requests

DEFAULT_USER_AGENT = "PK-PJN-Scrapper/1.0"

class Fetcher:
    """Downloads pages, waiting at least 'delay' seconds between requests.  """

    def __init__(
            self,
            delay: float = 0.5,
            timeout: float = 10.0,
            user_agent: str = DEFAULT_USER_AGENT
    ) -> None:
        self._delay = delay
        self._timeout = timeout
        self._session = requests.Session() #Jedno połączenie używane wielokrotnie
        self._session.headers["User-Agent"] = user_agent
        self._last_request_at: float | None = None

    def fetch(self, url: str) -> bytes:
        """Returns raw page bytes. Raises requests.HTTPError on 4xx/5xx."""
        self._wait_politely()
        response = self._session.get(url, timeout=self._timeout)
        self._last_request_at = time.monotonic() #zwraca liczbę sekund
        response.raise_for_status() #Jeśli bląd to rzuca wyjątek
        return response.content # surowe bajty

    def _wait_politely(self) -> None:
        if self._last_request_at is None:
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._delay:
            time.sleep(self._delay - elapsed)