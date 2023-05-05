from datetime import datetime
import json
import requests
from django.http import JsonResponse
from .models import copier_orders, copier_users, copier_accounts


def get_client_deals(request):
    if request.method == 'GET':
        # Get user information
        user = copier_users.objects.get(UserID=request.GET['userId'])
        account = copier_accounts.objects.get(id=request.GET['accountId'])
        
        # Retrieve orders from server
        url = f'https://api.server.com/orders?token={account.Token}&accountId={account.AccountNumber}'
        response = requests.get(url)
        data = response.json()
        
        # Process orders
        orders = []
        for order in data['orders']:
            try:
                existing_order = copier_orders.objects.get(OrderID=order['orderId'], AccountID=account.id)
                
                # Update existing order
                existing_order.SL = order['stopLoss']
                existing_order.TP = order['takeProfit']
                existing_order.ClosePrice = order['closePrice']
                existing_order.Swap = order['swap']
                existing_order.Profit = order['profit']
                existing_order.Commission = order['commission']
                existing_order.IsClosed = order['isClosed']
                existing_order.IsDeleted = order['isDeleted']
                existing_order.IsUpdated = 1
                existing_order.IsSynced = 1
                existing_order.ModifiedDate = datetime.now()
                existing_order.save()
                
                # Add existing order to list
                orders.append({
                    'orderId': existing_order.OrderID,
                    'orderType': existing_order.OrderType,
                    'symbol': existing_order.Symbol,
                    'lots': existing_order.Lots,
                    'openPrice': existing_order.OpenPrice,
                    'stopLoss': existing_order.SL,
                    'takeProfit': existing_order.TP,
                    'closePrice': existing_order.ClosePrice,
                    'swap': existing_order.Swap,
                    'profit': existing_order.Profit,
                    'commission': existing_order.Commission,
                    'comment': existing_order.Comment,
                    'magicNumber': existing_order.MagicNumber,
                    'openTime': int(existing_order.OrderTime.timestamp()),
                    'closeTime': int(existing_order.CloseTime.timestamp()),
                    'isClosed': existing_order.IsClosed,
                    'isDeleted': existing_order.IsDeleted,
                })
            except copier_orders.DoesNotExist:
                # Create new order
                new_order = copier_orders(
                    OrderID=order['orderId'],
                    OrderType=order['orderType'],
                    Symbol=order['symbol'],
                    Lots=order['lots'],
                    OpenPrice=order['openPrice'],
                    SL=order['stopLoss'],
                    TP=order['takeProfit'],
                    ClosePrice=order['closePrice'],
                    Swap=order['swap'],
                    Profit=order['profit'],
                    Commission=order['commission'],
                    Comment=order['comment'],
                    MagicNumber=order['magicNumber'],
                    OrderTime=datetime.fromtimestamp(order['openTime']),
                    CloseTime=datetime.fromtimestamp(order['closeTime']),
                    AccountID=account.id,
                    IsClosed=order['isClosed'],
                    IsDeleted=order['isDeleted'],
                    IsUpdated=1,
                    IsSynced=1,
                    CreatedDate=datetime.now(),
                    ModifiedDate=datetime.now()
                )
                new_order.save()
                
                # Add new order to list
                orders.append({
                    'orderId': new_order.OrderID,
                    'orderType': new_order.OrderType,
                    'symbol': new_order.Symbol,
                    'lots': new_order.Lots,
                    'openPrice': new_order.OpenPrice,
                    'stopLoss': new_order.SL,
                    'takeProfit': new_order.TP,
                    'closePrice': new_order.ClosePrice,
                    'swap': new_order.Swap,
                    'profit': new_order.Profit,
                    'commission': new_order.Commission,
                    'comment': new_order.Comment,
                    'magicNumber': new_order.MagicNumber,
                    'openTime': int(new_order.OrderTime.timestamp()),
                    'closeTime': int(new_order.CloseTime.timestamp()),
                    'isClosed': new_order.IsClosed,
                    'isDeleted': new_order.IsDeleted,
                })
        
        # Return orders as JSON response
        return JsonResponse({'orders': orders})
    else:
        return JsonResponse({'error': 'Invalid request method'})