from datetime import datetime
import json
import requests
from django.http import HttpResponseBadRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import copier_orders, copier_accounts


@csrf_exempt
def provider(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get account information
        account = copier_accounts.objects.get(Token=data['token'])
        
        # Process orders
        for order in data['orders']:
            try:
                existing_order = copier_orders.objects.get(OrderID=order['orderId'])
                
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
        
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest()