# Generated by Django 5.1.4 on 2025-02-24 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_postmodel_message_postmodel_subject_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmodel',
            name='comment_on_the_post',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='message',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='your_email',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='your_name',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_on_the_post', models.TextField(blank=True, null=True)),
                ('your_name', models.CharField(blank=True, max_length=30, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(blank=True, max_length=30, null=True)),
                ('your_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogs.postmodel')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
