from core.models import Node
from market.models import Account


def user_market(request):

    context = {}
    if request.user.is_superuser:
        context['nodes'] = Node.objects.all()
    elif request.user.is_authenticated:
        accounts = Account.objects.filter(owner=request.user)
        if accounts.count() == 1:
            context['account'] = accounts.first()
            context['market'] = context['account'].node

    return {
        'global': context
    }
