from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_category_options_alter_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                related_name='products',
                to='api.category',
            ),
        ),
    ]
