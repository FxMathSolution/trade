from datetime import datetime
from django.shortcuts import render
from .models import ClientDeal

def get_client_deals(request):
    client = request.GET.get('client')
    account_no = request.GET.get('account_no')
    delay = int(request.GET.get('delay', 0))
    exceptions = request.GET.get('exceptions', '0')

    if not all([client, account_no]):
        return render(request, 'error.html', {'message': 'Invalid parameters'})

    deals = ClientDeal.objects.filter(client=client, account_no=account_no)

    formatted_deals = []
    for deal in deals:
        date = datetime.now()
        date2 = deal.catch_time
        late = (date - date2).total_seconds()
        formatted_deal = {
            'status': deal.status,
            'id': deal.id,
            'late': late,
            'cld_ticket': deal.cld_ticket,
            'type': deal.type,
            'lot': deal.lot,
            'open_price': deal.open_price,
            'sl': deal.sl,
            'tp': deal.tp,
            'symbol': deal.symbol,
            'balance': deal.balance,
            'equity': deal.equity,
            'old_lot': deal.old_lot,
            'close_price': deal.close_price,
        }
        formatted_deals.append(formatted_deal)

    return render(request, 'deals.html', {'deals': formatted_deals})
