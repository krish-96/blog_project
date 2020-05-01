from django.contrib.auth.models import User, Group
from .models import Author
from django.db.models.signals import post_save
def author_profile(sender, instance, created, **kwargs):
    print('Author creations not started')
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Author.objects.create(
            name = instance,
        )
        print("Profile created successfully..")
    else:
        print('Author creations failed')

post_save.connect(author_profile, sender=User)

