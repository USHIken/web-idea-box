from django.db import models

# Create your models here.

class Content(models.Model):

    SCRATCH = "scratch"
    UNITY = "unity"
    WEB = "web"
    FREE = "free"
    
    CONTENT_TYPES = (
        (SCRATCH, "Scratch"),
        (UNITY, "Unity"),
        (WEB, "Web"),
        (FREE, "Free"),
    )

    title = models.CharField(default="")
    description = models.TextField(default="")
    content_type = models.CharField(choices=CONTENT_TYPES, default=SCRATCH)