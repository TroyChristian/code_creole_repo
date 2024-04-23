# middlewares.py or a suitable module in your Django project

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import LANGUAGE_SESSION_KEY
from .utilities import get_current_language  # Adjust the import path as necessary

class CustomLocaleMiddleware(MiddlewareMixin):
	def process_request(self, request):
		# Get the current language; this will return 'ht' as default if none is set
		language = get_current_language(request)

		# Activate the language for the current session
		translation.activate(language)
		request.LANGUAGE_CODE = language

		# Ensure the language is stored in the session for future requests
		if hasattr(request, 'session'):
			request.session[LANGUAGE_SESSION_KEY] = language
