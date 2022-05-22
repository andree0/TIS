# Generated by Django 3.2.7 on 2022-05-08 17:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('edited_date', models.DateField(auto_now=True)),
                ('finish_date', models.DateField(null=True)),
                ('status', models.PositiveIntegerField(
                        choices=[(0, 'Inventory'), (1, 'Valorization'), (2, 'Tree management')],
                        default=0
                    )),
                ('principal', models.CharField(max_length=64)),
                ('principal_address', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('latin_name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['latin_name'],
            },
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('lp', models.PositiveIntegerField(default=1)),
                ('height', models.PositiveIntegerField(
                    help_text='Height of tree mansured from base to top of tree.',
                    verbose_name='Height [meters]')),
                ('crown_width', models.PositiveIntegerField(
                    help_text='Tree crown width measured at its widest point.',
                    verbose_name='Crown width [meters]')),
                ('roloff', models.PositiveSmallIntegerField(
                    choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')],
                    default=0,
                    help_text='Crown structure and tree vitality in Roloff scale.')),
                ('is_existing', models.BooleanField(default=True)),
                ('inventory', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='TIS_app.inventory')),
                ('species', models.ForeignKey(
                    help_text='Basic tree species found in Poland.',
                    on_delete=django.db.models.deletion.CASCADE, to='TIS_app.species')),
            ],
            options={
                'unique_together': {('lp', 'inventory')},
            },
        ),
        migrations.CreateModel(
            name='ValorizationTree',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(
                    choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                    default=5)),
                ('is_biocenotic', models.BooleanField(default=False)),
                ('tree', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='TIS_app.tree')),
            ],
        ),
        migrations.CreateModel(
            name='TreeComment',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('tree', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='TIS_app.tree')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('image', models.ImageField(upload_to='tree_photos')),
                ('tree', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='TIS_app.tree')),
            ],
        ),
        migrations.CreateModel(
            name='ManagementTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('procedure', models.PositiveSmallIntegerField(
                    choices=[(0, 'ok'), (1, 'intervention'), (2, 'removal')], default=0)),
                ('tree', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='TIS_app.tree')),
            ],
        ),
        migrations.CreateModel(
            name='Circuit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('value', models.PositiveIntegerField(
                    help_text='Circuit of a single trunk at a height of DBH'
                              '(breast height diameter).',
                    validators=[
                        django.core.validators.MinValueValidator(1),
                        django.core.validators.MaxValueValidator(600)
                    ],
                    verbose_name='Circuit')),
                ('tree', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='TIS_app.tree')),
            ],
        ),
    ]
