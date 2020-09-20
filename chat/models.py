from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    """Base (abstract) model for all the objects to have common fields"""
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Message(BaseModel):
    """Model to store the messages"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_author")
    content = models.TextField()

    def __str__(self):
        """string representation of the message"""
        return str(self.author.username) + ": " + str(self.content)

    @classmethod
    def last_10_messages(cls):
        """will return last 10 Message objects"""
        return cls.objects.order_by('-created_at').all()[:10]
