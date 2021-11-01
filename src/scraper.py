import requests
from dtparser import DataParser


class WebScraper:
    """ 
        The WebScraper class, based on the providing url, makes the GET request for resources.
        The WebScraper uses the API requests library.
    """

    def get(self, url):
        # Realize the request GET method
        self.request = requests.get(url)
        return self.request

    def response_status(self):
        # Check the response status (Raise the HTTPError, when request status < 400)
        if not self.request.ok:
            raise requests.HTTPError('Request could not be realized. HTTP Error')

        return dict(status=self.request.status_code)


    def content(self):
        # Return the body from GET request method
        if not self.request:
            raise ValueError('The request was invalid or no content.')
        self.dp = DataParser(self.request)
        content = self.dp.read_content()
        return content

    def json(self):
        if not self.request:
            raise ValueError('The JSON is unable to save an empty file.')
        self.dp.to_json()



