from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class RoleBasedAccessMiddleware:
    """
    Middleware to protect routes based on user roles.
    Example rules:
        /api/admin/  -> Admin only
        /api/legal/  -> Legal only
        /api/pm/     -> PM only
        /api/sales/  -> Sales only
    """

    ROLE_PATH_MAP = {
        'Admin': '/api/admin/',
        'Legal': '/api/legal/',
        'PM': '/api/pm/',
        'Sales': '/api/sales/',
    }

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        path = request.path

        # Skip non-API routes
        if not path.startswith('/api/') or 'register' in path or 'login' in path:
            return self.get_response(request)

        # Check if path matches a protected role path
        for role, required_path in self.ROLE_PATH_MAP.items():
            if path.startswith(required_path):
                # Authenticate user with JWT
                try:
                    user, token = self.jwt_authenticator.authenticate(request)
                    if not user:
                        return JsonResponse({'error': 'Authentication required'}, status=401)
                    if user.role != role:
                        return JsonResponse({'error': f'{role} role required'}, status=403)
                except AuthenticationFailed as e:
                    return JsonResponse({'error': str(e)}, status=401)
                break  # No need to check other roles

        return self.get_response(request)
