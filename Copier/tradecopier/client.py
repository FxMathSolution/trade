from django.http import HttpResponse
from myapp.db import db
from myapp.config import new_order, close_order, delete_order, modify_order, sub_order

def client(request):
    if 'status' in request.GET: 
        status = int(request.GET.get('status'))
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'client' in request.GET: 
        client = request.GET.get('client')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'broker' in request.GET: 
        broker = request.GET.get('broker')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'account_no' in request.GET: 
        account_no = request.GET.get('account_no')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'computer' in request.GET: 
        computer = request.GET.get('computer')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'ip' in request.GET: 
        ip = request.GET.get('ip')[:50]
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'prd_id' in request.GET: 
        prd_id = request.GET.get('prd_id')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'ticket' in request.GET: 
        ticket = request.GET.get('ticket')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    if 'delay' in request.GET: 
        delay = request.GET.get('delay')
    else: 
        return HttpResponse('-1<br>invalid parameter format')
    
    db_obj = db()
    error = ''
    
    if status == new_order:
        if 'symbol' in request.GET: 
            symbol = request.GET.get('symbol')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'type' in request.GET: 
            type = request.GET.get('type')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'lot' in request.GET: 
            lot = request.GET.get('lot')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'balance' in request.GET: 
            balance = request.GET.get('balance')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'equity' in request.GET: 
            equity = request.GET.get('equity')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'open_time' in request.GET: 
            open_time = request.GET.get('open_time')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'open_price' in request.GET: 
            open_price = request.GET.get('open_price')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'sl' in request.GET: 
            sl = request.GET.get('sl')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'tp' in request.GET: 
            tp = request.GET.get('tp')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        
        id = db_obj.add_client_deal(client, broker, account_no, prd_id, ticket, symbol, type, lot,
                                    balance, equity, open_time, open_price, sl, tp, ip, computer, delay, error)
        if id < 0:
            return HttpResponse(str(id) + '<br>' + error)
        else:
            return HttpResponse(str(id) + '<br>succeeded')
        
    elif status == close_order:
        if 'close_price' in request.GET: 
            close_price = request.GET.get('close_price')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'profit' in request.GET: 
            profit = request.GET.get('profit')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'commission' in request.GET: 
            commission = request.GET.get('commission')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'swap' in request.GET: 
            swap = request.GET.get('swap')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        
        id = db_obj.close_client_deal(client, broker, account_no, prd_id, ticket, close_price, profit,
                                      commission, swap, ip, computer, delay, error)
        if id < 0:
            return HttpResponse(str(id) + '<br>' + error)
        else:
            return HttpResponse(str(id) + '<br>succeeded')
        
    elif status == delete_order:
        id = db_obj.delete_client_deal(client, broker, account_no, prd_id, ticket, ip, computer, delay, error)
        if id < 0:
            return HttpResponse(str(id) + '<br>' + error)
        else:
            return HttpResponse(str(id) + '<br>succeeded')
        
    elif status == modify_order:
        if 'open_price' in request.GET: 
            open_price = request.GET.get('open_price')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'sl' in request.GET: 
            sl = request.GET.get('sl')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'tp' in request.GET: 
            tp = request.GET.get('tp')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        
        id = db_obj.modify_client_deal(client, broker, account_no, prd_id, ticket, open_price, sl, tp,
                                       ip, computer, delay, error)
        if id < 0:
            return HttpResponse(str(id) + '<br>' + error)
        else:
            return HttpResponse(str(id) + '<br>succeeded')
        
    elif status == sub_order:
        if 'old_ticket' in request.GET: 
            old_ticket = request.GET.get('old_ticket')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'lot' in request.GET: 
            lot = request.GET.get('lot')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        if 'old_lot' in request.GET: 
            old_lot = request.GET.get('old_lot')
        else: 
            return HttpResponse('-1<br>invalid parameter format')
        
        id = db_obj.suborder_client_deal(client, broker, account_no, prd_id, old_ticket, ticket,
                                         old_lot, lot, ip, computer, delay, error)
        if id < 0:
            return HttpResponse(str(id) + '<br>' + error)
        else:
            return HttpResponse(str(id) + '<br>succeeded')
