from datetime import datetime
import json
import requests
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import copier_users, copier_accounts


@csrf_exempt
def client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user information
        user = copier_users.objects.get(UserID=data['userId'])
        account = copier_accounts.objects.get(id=data['accountId'], UserID=user.id)
        
        # Create order data
        order_data = {
            'orderId': data['orderId'],
            'orderType': data['orderType'],
            'symbol': data['symbol'],
            'lots': data['lots'],
            'openPrice': data['openPrice'],
            'stopLoss': data['stopLoss'],
            'takeProfit': data['takeProfit'],
            'closePrice': data['closePrice'],
            'swap': data['swap'],
            'profit': data['profit'],
            'commission': data['commission'],
            'comment': data['comment'],
            'magicNumber': data['magicNumber'],
            'openTime': int(data['openTime']),
            'closeTime': int(data['closeTime']),
            'isClosed': data['isClosed'],
            'isDeleted': data['isDeleted'],
        }
        
        # Send order data to provider
        url = f'https://api.provider.com/orders?token={account.Token}'
        response = requests.post(url, json={'token': account.Token, 'orders': [order_data]})
        
        # Process response from provider
        if response.status_code == 200:
            # Update order in database
            try:
                existing_order = copier_orders.objects.get(OrderID=data['orderId'], AccountID=account.id)
                existing_order.SL = data['stopLoss']
                existing_order.TP = data['takeProfit']
                existing_order.IsClosed = data['isClosed']
                existing_order.IsDeleted = data['isDeleted']
                existing_order.IsUpdated = 1
                existing_order.IsSynced = 1
                existing_order.ModifiedDate = datetime.now()
                existing_order.save()
            except copier_orders.DoesNotExist:
                # Create new order in database
                new_order = copier_orders(
                    OrderID=data['orderId'],
                    OrderType=data['orderType'],
                    Symbol=data['symbol'],
                    Lots=data['lots'],
                    OpenPrice=data['openPrice'],
                    SL=data['stopLoss'],
                    TP=data['takeProfit'],
                    ClosePrice=data['closePrice'],
                    Swap=data['swap'],
                    Profit=data['profit'],
                    Commission=data['commission'],
                    Comment=data['comment'],
                    MagicNumber=data['magicNumber'],
                    OrderTime=datetime.fromtimestamp(data['openTime']),
                    CloseTime=datetime.fromtimestamp(data['closeTime']),
                    AccountID=account.id,
                    IsClosed=data['isClosed'],
                    IsDeleted=data['isDeleted'],
                    IsUpdated=1,
                    IsSynced=1,
                    CreatedDate=datetime.now(),
                    ModifiedDate=datetime.now()
                )
                new_order.save()
            
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'error': 'Failed to send order data to provider'})
    else:
        return HttpResponseBadRequest()