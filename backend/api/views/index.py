from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='../index.html'))


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        response = self.http_method_not_allowed(request, *args, **kwargs)
        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
        return response
