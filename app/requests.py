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
        get_quote = url.read()
        get_quote_response = json.loads(get_quote)

        quote_results = []
        
        author = get_quote_response.get('author')
        quote = get_quote_response.get('quote')

        if author and quote:
            quote_object = Quote(author,quote)
            quote_results.append(quote_object)

    return quote_results
