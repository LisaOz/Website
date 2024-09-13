import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

""" 
This is a function that allows to create actions that optionally include a target object
and can be used as a shortcut to add new actions to the activity stream.
If user clicks on the button several times, the dublicate actions are not saved.
"""

def create_action(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False