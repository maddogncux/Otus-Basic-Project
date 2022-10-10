from django.db import models

# Create your models here.





class EventReg(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="event_reg")
    teams = models.ManyToManyField("event.RegisteredTeam", blank=True, related_name="regd_teams")
    # opened = models.BooleanField()
    sides = models.ManyToManyField("event.Sides", related_name="sIDES", blank=True)
    additionalservice = models.ManyToManyField("event.AdditionalServices", blank=True)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.event.name


@receiver(signal=post_save, sender=Event)
def reg_saved_handler(instance: Event, created: bool, **kwargs):
    if not created:
        return

    EventReg.objects.create(event=instance)