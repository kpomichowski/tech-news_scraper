import requests


class WebScraper:
    """ 
        The WebScraper class, based on the providing url, makes the GET request for resources.
        The WebScraper uses the API requests library.
    """


    def __init__(self):
        # Initalize the url attribute
        ...

    def get(self, url):
        # Realize the request GET method
        self.request = requests.get(url)
        return self.request

    def response_status(self):
        # Check the response status (Raise the HTTPError, when request status < 400)
        if not self.request.ok:
            raise requests.HTTPError('Request could not be realized. HTTP Error')

        return self.request.status_code



