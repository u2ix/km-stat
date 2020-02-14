# Generated by Django 3.0.3 on 2020-02-12 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exportkontrollstatistiken', '0020_auto_20191026_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laender',
            name='gruppen',
            field=models.ManyToManyField(to='exportkontrollstatistiken.Laendergruppen'),
        ),
        migrations.CreateModel(
            name='GeschaefteKriegsmaterialNachKategorieEndempfaengerstaat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromDate', models.DateField()),
                ('toDate', models.DateField()),
                ('KM1', models.PositiveIntegerField(blank=True, null=True)),
                ('KM2', models.PositiveIntegerField(blank=True, null=True)),
                ('KM3', models.PositiveIntegerField(blank=True, null=True)),
                ('KM4', models.PositiveIntegerField(blank=True, null=True)),
                ('KM5', models.PositiveIntegerField(blank=True, null=True)),
                ('KM6', models.PositiveIntegerField(blank=True, null=True)),
                ('KM7', models.PositiveIntegerField(blank=True, null=True)),
                ('KM8', models.PositiveIntegerField(blank=True, null=True)),
                ('KM9', models.PositiveIntegerField(blank=True, null=True)),
                ('KM10', models.PositiveIntegerField(blank=True, null=True)),
                ('KM11', models.PositiveIntegerField(blank=True, null=True)),
                ('KM12', models.PositiveIntegerField(blank=True, null=True)),
                ('KM13', models.PositiveIntegerField(blank=True, null=True)),
                ('KM14', models.PositiveIntegerField(blank=True, null=True)),
                ('KM15', models.PositiveIntegerField(blank=True, null=True)),
                ('KM16', models.PositiveIntegerField(blank=True, null=True)),
                ('KM17', models.PositiveIntegerField(blank=True, null=True)),
                ('KM18', models.PositiveIntegerField(blank=True, null=True)),
                ('KM19', models.PositiveIntegerField(blank=True, null=True)),
                ('KM20', models.PositiveIntegerField(blank=True, null=True)),
                ('KM21', models.PositiveIntegerField(blank=True, null=True)),
                ('KM22', models.PositiveIntegerField(blank=True, null=True)),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exportkontrollstatistiken.Laendergruppen')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exportkontrollstatistiken.Laender')),
                ('sources', models.ManyToManyField(to='exportkontrollstatistiken.QuellenGeschaefte')),
            ],
        ),
    ]
