from django.db import migrations


def init_last_member_id(apps, schema_editor):
    Node = apps.get_model('core', 'Node')
    Account = apps.get_model('market', 'Account')

    for node in Node.objects.all():
        member_ids = Account.objects.filter(node=node, member_id__isnull=False).values_list('member_id', flat=True)
        numbers = [int(member_id.strip()) for member_id in member_ids if member_id.strip().isdigit()]
        node.last_member_id = max(numbers, default=0)
        node.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_node_last_member_id'),
        ('market', '0017_separate_address'),
    ]

    operations = [
        migrations.RunPython(init_last_member_id, migrations.RunPython.noop),
    ]
