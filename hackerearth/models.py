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
    status = models.CharField(max_length=80, help_text="status")
    #default = 'Close'


    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.timestamp) + " " + self.failure_mode

class Client(models.Model):
    """
    Stores Client information.
    """
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    name = models.CharField(max_length=50, help_text="Client identification")
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.timestamp) + " " + self.client_mode

class Product(models.Model):
    """
    Stores Product information.
    """
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=50, help_text="Product identification")
    production_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.timestamp) + " " + self.product_mode

class Order(models.Model):
     """
     Stores Order information.
     """
     class Meta:
         verbose_name = 'Order'
         verbose_name_plural = 'Orders'

     order_number = models.IntegerField(help_text="order number", null=True, blank=True)
     client = models.CharField(max_length=50, help_text="Client identification")
     product = models.CharField(max_length=50, help_text="Product identification")
     quantity = models.IntegerField(help_text="Quantity", null=True, blank=True)
     deadline = models.IntegerField(help_text="Deadline (hrs)", null=True, blank=True)
     status = models.CharField(max_length=50, help_text="Status identification")
     def __str__(self):
         """
         String for representing the Model object (in Admin site etc.)
         """
         return str(self.timestamp) + " " + self.order_mode

class Conveyor_belt(models.Model):
    """
    Stores Conveyor_belt information.
     """
    class Meta:
        verbose_name = 'Conveyor belt'
        verbose_name_plural = 'Conveyor belts'

    conveyor_belt = models.CharField(max_length=5, help_text="Conveyor_belt identification")
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.timestamp) + " " + self.conveyor_belt_mode

class Alocation(models.Model):
    """
    Stores alocation information.
    """
    class Meta:
        verbose_name = 'Alocation'
        verbose_name_plural = 'Alocation'

    conveyor_belt = models.CharField(max_length=5, help_text="Conveyor_belt identification")
    order = models.IntegerField(help_text="order", null=True, blank=True)
    production_time = models.IntegerField(help_text="production time", null=True, blank=True)
    delivery_time = models.IntegerField(help_text="delivery time", null=True, blank=True)
    status = models.CharField(max_length=50, help_text="Status identification")
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.timestamp) + " " + self.alocation_mode

class Conversation_bot_context(models.Model):
    """
    Stores Conversation_context information.
    """
    class Meta:
        verbose_name = 'Conversation_context'
        verbose_name_plural = 'Conversation_contexts'

    conversation = models.CharField(max_length=50, help_text="conversation id", null=True)
    value_type = models.CharField(max_length=50, help_text="value_type identification", null=True)
    value = models.CharField(max_length=50, help_text="value identification", null=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.conversation
