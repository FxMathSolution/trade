from django.http import HttpResponse
from myapp.models import ProviderDeal  # Replace with your Django model for provider deals

def provider(request):
    # Get parameters from the request
    status = int(request.GET.get('status', '-1'))
    provider = request.GET.get('provider')
    broker = request.GET.get('broker')
    account_no = request.GET.get('account_no')
    ticket = request.GET.get('ticket')
    ip = request.GET.get('ip', '')[:50]
    computer = request.GET.get('computer')
    delay = request.GET.get('delay')

    # Process the request based on the status parameter
    if status == 1:
        symbol = request.GET.get('symbol')
        type_ = request.GET.get('type')
        lot = request.GET.get('lot')
        balance = request.GET.get('balance')
        equity = request.GET.get('equity')
        open_time = request.GET.get('open_time')
        open_price = request.GET.get('open_price')
        sl = request.GET.get('sl')
        tp = request.GET.get('tp')

        # Save the provider deal to the database
        deal = ProviderDeal.objects.create(
            provider=provider,
            broker=broker,
            account_no=account_no,
            ticket=ticket,
            symbol=symbol,
            type_=type_,
            lot=lot,
            balance=balance,
            equity=equity,
            open_time=open_time,
            open_price=open_price,
            sl=sl,
            tp=tp,
            ip=ip,
            computer=computer,
            delay=delay,
        )

    elif status == 2:
        close_price = request.GET.get('close_price')
        profit = request.GET.get('profit')
        commission = request.GET.get('commission')
        swap = request.GET.get('swap')

        # Update the provider deal in the database
        deal = ProviderDeal.objects.filter(
            provider=provider,
            broker=broker,
            account_no=account_no,
            ticket=ticket,
        ).update(
            close_price=close_price,
            profit=profit,
            commission=commission,
            swap=swap,
            ip=ip,
            computer=computer,
            delay=delay,
        )

    elif status == 3:
        # Delete the provider deal from the database
        ProviderDeal.objects.filter(
            provider=provider,
            broker=broker,
            account_no=account_no,
            ticket=ticket,
        ).delete()

    elif status == 4:
        open_price = request.GET.get('open_price')
        sl = request.GET.get('sl')
        tp = request.GET.get('tp')

        # Update the provider deal in the database
        deal = ProviderDeal.objects.filter(
            provider=provider,
            broker=broker,
            account_no=account_no,
            ticket=ticket,
        ).update(
            open_price=open_price,
            sl=sl,
            tp=tp,
            ip=ip,
            computer=computer,
            delay=delay,
        )

    elif status == 5:
        old_ticket = request.GET.get('old_ticket')
        lot = request.GET.get('lot')
        old_lot = request.GET.get('old_lot')

        # Save the suborder to the database
        deal = ProviderDeal.objects.create(
            provider=provider,
            broker=broker,
            account_no=account_no,
            ticket=ticket,
            old_ticket=old_ticket,
            lot=lot,
            old_lot=old_lot,
            ip=ip,
            computer=computer,
            delay=delay,
        )

    else:
        # Invalid status parameter
        return HttpResponse('-1<br>invalid parameter format')

    # Return the response
    if deal:
        return HttpResponse(f'{deal.id}<br>succeeded')
    else:
        return HttpResponse(f'{deal}<br>{error}')
