from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from helpers.pdf import render_pdf_response
from market.models import Account, Provider
import urllib.parse


class MemberCheck(TemplateView):
    template_name = 'member/check_outside_app.html'


class CheckMemberStatus(TemplateView):
    template_name = 'member/check_form.html'

    def get_member_status(self, member_id):
        status_info = {}
        member = Account.objects.filter(member_id=member_id).first()
        if member is not None:
            status_info['member_type'] = 'person'
            status_info['is_intercoop'] = member.is_intercoop
        else:
            member = Account.objects.filter(member_id=member_id).first()
            if member is None:
                return None
            status_info['member_type'] = 'entity'
        status_info['is_active'] = not member.inactive
        return status_info

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'member_id' in kwargs:
            member_id = kwargs['member_id']
            context['member_id'] = member_id
            status = self.get_member_status(member_id)
            if status is None:
                context['member_not_found'] = True
            else:
                context['status'] = status

        return context

    def post(self, request, *args, **kwargs):
        kwargs['member_id'] = self.request.POST.get('member_id', None)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def get_card_data(member_type, member):
    params = f'?city={member.node.id}&member_id={member.member_id}'
    member_data_url = settings.BASESITE_URL + reverse('market:member_check') + params

    card_data = {
        'member': {
            'member_type': member_type,
            'member_id': member.member_id,
        },
        'display_name': member.display_name,
        'profile_image': member.profile_image,
        'member_qr': urllib.parse.quote(member_data_url),
    }

    if member_type == 'consumer':
        card_data['member']['is_intercoop'] = member.is_intercoop

    return card_data


@login_required
def member_card(request):
    account = Account.objects.filter(owner=request.user).first()
    member_type = 'provider' if isinstance(account, Provider) else 'consumer'
    card_data = get_card_data(member_type, account)
    return render(request, 'member/card.html', card_data)


@login_required
def member_card_pdf(request):
    account = Account.objects.filter(owner=request.user).first()
    member_type = 'provider' if isinstance(account, Provider) else 'consumer'
    card_data = get_card_data(member_type, account)

    filename = 'carnet_mesm'
    return render_pdf_response(request, 'member/card_pdf.html', card_data, filename=filename)
