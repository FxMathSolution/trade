from django.shortcuts import render

import json
import random
import string
import time
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import copier_users, copier_accounts, copier_orders, copier_logs


# Constants
COMMAND_OPEN_ORDER = 'open_order'
COMMAND_MODIFY_ORDER = 'modify_order'
COMMAND_CLOSE_ORDER = 'close_order'


# Functions
def get_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_time_offset():
    return time.timezone if (time.localtime().tm_isdst == 0) else time.altzone


def is_assoc_array(arr):
    return isinstance(arr, dict) and bool(arr) and all(isinstance(key, str) for key in arr.keys())


# Views
def index(request):
    return render(request, 'index.html')


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
            'token': account.Token,
        }
        
        # Send command to server
        response = requests.post(account.BrokerName, json=command_data)
        
        # Log command and response
        log_data = {
            'AccountID': account.id,
            'OrderID': None,
            'Message': f"{data['command']}: {response.text}",
        }
        copier_logs.objects.create(**log_data)
        
        # Return response from server
        return JsonResponse(response.json())
    else:
        return HttpResponseBadRequest()
        

@csrf_exempt
def add_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        
        # Check if user has reached maximum number of accounts
        if copier_accounts.objects.filter(UserID=user.id).count() >= MAX_ACCOUNTS:
            return JsonResponse({'error': 'Maximum number of accounts reached'})
        
        # Get token from server
        token_data = {
            'command': 'get_token',
            'parameters': {
                'login': data['login'],
                'password': data['password'],
            },
        }
        response = requests.post(data['brokerName'], json=token_data)
        
        # Check response from server
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to get token from server'})
        
        # Save account information to database
        account_data = {
            'UserID': user.id,
            'AccountNumber': data['accountNumber'],
            'BrokerName': data['brokerName'],
            'Token': response.text,
            'Status': 'active',
        }
        account = copier_accounts.objects.create(**account_data)
        
        # Log addition of account
        log_data = {
            'AccountID': account.id,
            'OrderID': None,
            'Message': f"Account added ({account.AccountNumber} - {account.BrokerName})",
        }
        copier_logs.objects.create(**log_data)
        
        # Return success response
        return JsonResponse({'success': True})
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def modify_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        account = copier_accounts.objects.get(id=data['accountId'], UserID=user.id)
        
        # Get token from server
        token_data = {
            'command': 'get_token',
            'parameters': {
                'login': data['login'],
                'password': data['password'],
            },
        }
        response = requests.post(data['brokerName'], json=token_data)
        
        # Check response from server
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to get token from server'})
        
        # Update account information in database
        account.Token = response.text
        account.Status = data['status']
        account.save()
        
        # Log modification of account
        log_data = {
            'AccountID': account.id,
            'OrderID': None,
            'Message': f"Account modified ({account.AccountNumber} - {account.BrokerName})",
        }
        copier_logs.objects.create(**log_data)
        
        # Return success response
        return JsonResponse({'success': True})
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        account = copier_accounts.objects.get(id=data['accountId'], UserID=user.id)
        
        # Delete account from database
        account.delete()
        
        # Log deletion of account
        log_data = {
            'AccountID': account.id,
            'OrderID': None,
            'Message': f"Account deleted ({account.AccountNumber} - {account.BrokerName})",
        }
        copier_logs.objects.create(**log_data)
        
        # Return success response
        return JsonResponse({'success': True})
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def get_accounts(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        
        # Retrieve accounts for user
        accounts = copier_accounts.objects.filter(UserID=user.id)
        
        # Return accounts in JSON response
        return JsonResponse({
            'accounts': [
                {
                    'id': account.id,
                    'accountNumber': account.AccountNumber,
                    'brokerName': account.BrokerName,
                    'status': account.Status,
                } for account in accounts
            ]
        })
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def get_orders(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        account = copier_accounts.objects.get(id=data['accountId'], UserID=user.id)
        
        # Retrieve orders for account
        orders = copier_orders.objects.filter(AccountID=account.id)
        
        # Return orders in JSON response
        return JsonResponse({
            'orders': [
                {
                    'id': order.id,
                    'orderId': order.OrderID,
                    'symbol': order.Symbol,
                    'type': order.Type,
                    'volume': order.Volume,
                    'openTime': str(order.OpenTime),
                    'openPrice': order.OpenPrice,
                    'sl': order.SL,
                    'tp': order.TP,
                    'closeTime': str(order.CloseTime) if order.CloseTime else None,
                    'closePrice': order.ClosePrice,
                    'commission': order.Commission,
                    'swap': order.Swap,
                    'profit': order.Profit,
                    'status': order.Status,
                } for order in orders
            ]
        })
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def get_logs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        account = copier_accounts.objects.get(id=data['accountId'], UserID=user.id)
        
        # Retrieve logs for account
        logs = copier_logs.objects.filter(AccountID=account.id).order_by('-LogTime')[:50]
        
        # Return logs in JSON response
        return JsonResponse({
            'logs': [
                {
                    'id': log.id,
                    'orderId': log.OrderID,
                    'logTime': str(log.LogTime),
                    'message': log.Message,
                } for log in logs
            ]
        })
    else:
        return HttpResponseBadRequest()
