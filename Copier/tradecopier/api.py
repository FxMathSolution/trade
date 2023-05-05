import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import copier_users, copier_accounts
import requests


@csrf_exempt
def api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        account = copier_accounts.objects.get(id=data['accountId'], UserID=user.id)
        
        # Create command data
        command_data = {
            'command': data['command'],
            'parameters': data['parameters'],
        }
        
        # Send command data to provider
        url = f'https://api.provider.com/commands?token={account.Token}'
        response = requests.post(url, json={'token': account.Token, 'commands': [command_data]})
        
        # Process response from provider
        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse({'status': 'OK', 'data': response_data})
        else:
            return JsonResponse({'error': 'Failed to send command data to provider'})
    else:
        return HttpResponseBadRequest()