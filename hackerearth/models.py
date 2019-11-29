from django.db import models

class Failure(models.Model):
    """
    Stores Failure information.
    """
    class Meta:
        verbose_name = 'Failure'
        verbose_name_plural = 'Failures'

    sensor = models.IntegerField(help_text="Sensor number", null=True, blank=True)
    timestamp = models.DateTimeField(editable=False)
    conveyor_belt = models.CharField(max_length=10, help_text="Conveyor Belt identification")
    machine = models.CharField(max_length=80, help_text="Machine Name")
    unit  = models.CharField(max_length=80, help_text="Unit Name")
    group = models.CharField(max_length=80, help_text="Group Name")
    component = models.CharField(max_length=80, help_text="Component Name")
    failure_mode = models.CharField(max_length=80, help_text="Failure Mode Name")
    discipline = models.CharField(max_length=80, help_text="Discipline Name")
    comments = models.CharField(max_length=300, help_text="Comments")
    delay_min = models.IntegerField(help_text="Delay Min", null=True, blank=True)
    avg_repair_time = models.IntegerField(help_text="Average repair time (hours)", null=True, blank=True)
    avg_repair_cost = models.IntegerField(help_text="Average repair cost (USD)", null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.timestamp) + " " + self.failure_mode
