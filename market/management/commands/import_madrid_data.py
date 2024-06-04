import json
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import Q

from authentication.models import User
from benefits.models import Benefit
from core.models import Node, Gallery, GalleryPhoto
from core.models.social_profile import SocialNetwork, ProviderSocialProfile
from market.models import Category, Consumer, Provider
from news.models import News
from offers.models import Offer

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = "%Y-%m-%d"

social_network_map = {
    'facebook_link': 'Facebook',
    'twitter_link': 'X',
    'instagram_link': 'Instagram',
    'telegram_link': 'Telegram',
}


def import_news(news, node):
    for item in news:
        news_created = News.objects.create(
            node=node,
            title=item['title'],
            description=item['description'],
            short_description=item['short_description'],
            more_info_text=item['more_info_text'],
            more_info_url=item['more_info_url'],
        )
        news_created.published_date = datetime.strptime(item['published_date'], DATETIME_FORMAT)
        news_created.banner_image.name = item['banner_image']
        news_created.banner_thumbnail.name = item['banner_thumbnail']
        news_created.save()


def import_categories(categories, node):
    for item in categories:
        Category.objects.create(
            node=node,
            id=item['id'],
            name=item['name'],
            description=item['description'],
            color=item['color'],
        )


def import_consumers(consumers, node):

    current = 0
    invalid = 0
    duplicated = 0
    cif_duplicated = 0
    save_errors = 0

    for item in consumers:

        current += 1
        print(f'Current: {current}', end='\r')

        if item['inactive'] or item['is_guest_account']:
            continue

        uuids_to_ignore = []

        if item['id'] in uuids_to_ignore:
            continue

        cif = item['nif']
        email = item['email']

        if not cif or len(cif) > 30:
            print(f"Invalid consumer nif: {item['name']} - {email} - {cif}. SKIPPING...")
            invalid += 1
            continue

        existing_consumer = Consumer.objects.filter(Q(email=email) | Q(owner__email=email)).first()
        if existing_consumer:
            duplicated += 1
            print(f"Consumer email already exists: {email}. SKIPPING...")
            continue

        existing_consumer_cif = Consumer.objects.filter(cif=cif).first()
        if existing_consumer_cif:
            cif_duplicated += 1
            print(f"Consumer CIF already exists: {cif}. SAVING ANYWAY...")

        try:
            user_created = User.objects.create(
                email=item['email'],
                first_name=item['name'],
                last_name=item['surname'],
                password=item['password'],
                node=node,
            )

            consumer_created = Consumer.objects.create(
                id=item['id'],
                node=node,
                owner=user_created,
                first_name=item['name'],
                last_name=item['surname'],
                email=item['email'],
                is_intercoop=item['is_intercoop'],
                cif=cif,
                is_active= not item['inactive'],
                member_id=item['member_id'],
                address=item['address'],
                registration_date=datetime.strptime(item['registered'], DATETIME_FORMAT),

            )
            consumer_created.profile_image.name = item['profile_image']
            consumer_created.save()
        except Exception as error:
            save_errors += 1
            print(f"Consumer save error: {email} - {cif} - {error}. Current: {current}")

    print(f'Invalid: {invalid}, duplicated email: {duplicated}, duplicated CIF: {cif_duplicated}, save_errors: {save_errors}')


def set_social_profiles(provider_data, provider_instance):

    for field in provider_data:
        if field in social_network_map and provider_data[field]:
            social_network = SocialNetwork.objects.get(name=social_network_map[field])
            url = provider_data[field]
            ProviderSocialProfile.objects.create(social_network=social_network, url=url, provider=provider_instance)


def set_categories(provider_data, provider_instance):
    if 'categories' in provider_data and provider_data['categories']:
        provider_instance.categories.set(Category.objects.filter(pk__in=provider_data['categories']))


def set_offers(provider_data, provider_instance):

    for offer in provider_data['offers']:
        offer_created = Offer.objects.create(
            provider=provider_instance,
            id=offer['id'],
            title=offer['title'],
            description=offer['description'],
            discount_percent=offer['discount_percent'],
            discounted_price=offer['discounted_price'],
            active=offer['active'],
        )

        offer_created.published_date = datetime.strptime(offer['published_date'], DATETIME_FORMAT)
        offer_created.begin_date = datetime.strptime(offer['begin_date'], DATE_FORMAT) if offer['begin_date'] else None
        offer_created.end_date = datetime.strptime(offer['end_date'], DATE_FORMAT) if offer['end_date'] else None
        offer_created.banner_image.name = offer['banner_image']
        offer_created.banner_thumbnail.name = offer['banner_thumbnail']
        offer_created.save()


def set_benefit(provider_data, provider_instance):
    benefit = provider_data['benefit']
    if benefit:
        benefit_created = Benefit.objects.create(
            entity=provider_instance,
            benefit_for_entities=benefit['benefit_for_entities'],
            benefit_for_members=benefit['benefit_for_members'],
            includes_intercoop_members=benefit['includes_intercoop_members'],
            in_person=benefit['in_person'],
            online=benefit['online'],
            discount_code=benefit['discount_code'],
            discount_link_entities=benefit['discount_link_entities'],
            discount_link_members=benefit['discount_link_members'],
            discount_link_text=benefit['discount_link_text'],
            active=benefit['active'],
        )

        benefit_created.published_date = datetime.strptime(benefit['published_date'], DATETIME_FORMAT)
        benefit_created.last_updated = datetime.strptime(benefit['last_updated'], DATETIME_FORMAT)
        benefit_created.save()


def set_gallery(item, provider_instance):
    gallery = item['gallery_data']
    if gallery:
        gallery_created = Gallery.objects.create(title=gallery['title'])
        for photo in gallery['photos']:
            photo_created = GalleryPhoto.objects.create(
                gallery=gallery_created,
                order=photo['order'],
                title=photo['title'],
            )

            photo_created.photo.name = photo['image']
            photo_created.image_thumbnail.name = photo['image_thumbnail']
            photo_created.uploaded = datetime.strptime(photo['uploaded'], DATETIME_FORMAT)
            photo_created.save()

        provider_instance.gallery = gallery_created
        provider_instance.save()


def import_providers(providers, node):

    current = 0
    invalid = 0
    duplicated = 0
    cif_duplicated = 0
    save_errors = 0

    for item in providers:

        current += 1
        print(f'Current: {current}', end='\r')

        if item['inactive'] or item['email'] == 'etics@mercadosocial.net':
            continue

        cif = item['cif']
        email = item['email']

        if not cif or len(cif) > 30:
            print(f"Invalid provider nif: {item['name']} - {email} - {cif}. SKIPPING...")
            invalid += 1
            continue

        existing_provider = Provider.objects.filter(Q(email=email) | Q(owner__email=email)).first()
        if existing_provider:
            duplicated += 1
            print(f"Provider already exists: {item['email']}. SKIPPING...")
            continue

        existing_provider_cif = Provider.objects.filter(cif=cif).first()
        if existing_provider_cif:
            cif_duplicated += 1
            print(f"Provider CIF already exists: {cif}. SAVING ANYWAY...")

        try:
            user_created = User.objects.create(
                email=item['email'],
                first_name=item['name'],
                password=item['password'],
                node=node,
            )

            provider_created = Provider.objects.create(
                id=item['id'],
                node=node,
                owner=user_created,
                cif=cif,
                name=item['name'],
                is_active= not item['inactive'],
                email=item['email'],
                member_id=item['member_id'],
                address=item['address'],
                phone_number=item['phone_number'],
                registration_date=datetime.strptime(item['registered'], DATETIME_FORMAT),

                description=item['description'],
                short_description=item['short_description'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                num_workers=item['num_workers'],
                legal_form=item['legal_form'],
                balance_detail=item['balance_detail'],
                not_listed=item['hidden'],
                webpage_link=item['webpage_link'],

            )

            provider_created.profile_image.name = item['logo']

            set_categories(item, provider_created)

            provider_created.save()

            set_social_profiles(item, provider_created)
            set_offers(item, provider_created)
            set_benefit(item, provider_created)
            set_gallery(item, provider_created)

        except Exception as error:
            save_errors += 1
            print(f"Provider save error: {email} - {cif} - {error}. Current: {current}")

    print(f'Invalid: {invalid}, duplicated email: {duplicated}, duplicated CIF: {cif_duplicated}, save_errors: {save_errors}')


class Command(BaseCommand):
    help = 'Import all data of Madrid from old application'

    def add_arguments(self, parser):

        parser.add_argument('--node', type=int, help='Node Id of Madrid')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        with open('data/all_data.json', 'rb') as f:
            data = json.load(f)

            print("Importing news, {} items".format(len(data['news'])))
            import_news(data['news'], node)

            print("Importing categories, {} items".format(len(data['categories'])))
            import_categories(data['categories'], node)

            print("Importing providers, {} items".format(len(data['providers'])))
            import_providers(data['providers'], node)

            print("Importing consumers, {} items".format(len(data['consumers'])))
            import_consumers(data['consumers'], node)

