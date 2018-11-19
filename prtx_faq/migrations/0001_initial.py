# Generated by Django 2.1.2 on 2018-11-13 21:17

import django.db.models.deletion
import i18nfield.fields
from django.db import migrations, models
from prtx_faq.prtx import PRTX


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (('event', '0017_auto_20180922_0511') if PRTX == 'pretalx' else ('pretixbase', '0101_auto_20181025_2255')),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', i18nfield.fields.I18nCharField(verbose_name='Question')),
                ('answer', i18nfield.fields.I18nTextField(verbose_name='Answer')),
                ('tags', models.CharField(blank=True, help_text='Tags can help people find related questions. Please enter the tags separated by commas.', max_length=180, null=True, verbose_name='Tags')),
                ('position', models.PositiveIntegerField(verbose_name='Position')),
            ],
            options={
                'ordering': ('category__position', 'position', 'id'),
            },
        ),
        migrations.CreateModel(
            name='FAQCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18nfield.fields.I18nCharField(verbose_name='Name', max_length=180)),
                ('position', models.PositiveIntegerField(verbose_name='Position')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faq_categories', to='event.Event' if PRTX == 'pretalx' else 'pretixbase.Event')),
            ],
            options={
                'ordering': ('position', 'id'),
            },
        ),
        migrations.AddField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='prtx_faq.FAQCategory', verbose_name='Category'),
        ),
        migrations.AlterUniqueTogether(
            name='faqcategory',
            unique_together={('event', 'name')},
        ),
    ]
