'''Transmutable is a Django project which provides tools for working in public'''

from tastypie.api import Api
API = Api(api_name='v0.1')

from banana.api import CompletedItemResource
