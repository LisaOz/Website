"""
Function to attach a receiver function to the (many-to-many) m2m_changed signal.
The users_like_changed function is registered with the @receiver() decorator and is attached
to the m2m_changed signal. The function is then connected to the Image.users_like.through
so that the function is only called when the m2m_changed_signal is launched by the sender.
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs): # receiver
    
    instance.total_likes = instance.users_like.count()
   
    instance.save()