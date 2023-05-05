import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import copier_users


@csrf_exempt
def authenticate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Retrieve user information from database
        try:
            user = copier_users.objects.get(Email=data['email'])
        except copier_users.DoesNotExist:
            return JsonResponse({'error': 'User not found'})
        
        # Check password
        if user.Password == data['password']:
            # Return user information in JSON response
            return JsonResponse({
                'userId': user.UserID,
                'firstName': user.FirstName,
                'lastName': user.LastName,
                'email': user.Email,
                'phone': user.Phone,
                'status': user.Status,
            })
        else:
            return JsonResponse({'error': 'Invalid password'})
    else:
        return HttpResponseBadRequest()