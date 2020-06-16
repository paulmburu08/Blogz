import urllib.request,json
from .models import Quote

api = None

def configure_request(app):
    global api
    api = app.config['API']

def get_quotes():
    '''
    Function that gets the json response to our url request
    '''
    with urllib.request.urlopen(api) as url:
        get_quote = url.read
        get_quote_response = json.loads(get_quote)

        quote_results = None

        quote_results = process_results(get_quote_response)

    return quote_results

def process_results(quotes):

    quote_results = []
    for quote in quotes:
        author = quote.get('author')
        quote = quote.get('quote')

        if get_quote_response['author'] and get_quote_response['quote']:
            quote_object = Quote(author,quote)
            quote_results.append(quote_object)

    return quote_results