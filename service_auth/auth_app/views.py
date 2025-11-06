from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def token_obtain(request):
    username = request.data.get('username')
    if username:
        user = type('U', (object,), {'id':1, 'username':username})()
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})
    return Response({'detail': 'credentials required'}, status=400)
