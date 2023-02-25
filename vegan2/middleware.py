from django.middleware.csrf import rotate_token

class CsrfRotateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rotate_token(request)
        response = self.get_response(request)
        return response
