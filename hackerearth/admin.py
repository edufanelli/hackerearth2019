from django.contrib import admin
from .models import Failure
from .models import Client
from .models import Product
from .models import Order
from .models import Conveyor_belt
from .models import Alocation
from .models import Conversation_bot_context
# Register your models here.
admin.site.register(Failure)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Conveyor_belt)
admin.site.register(Alocation)
admin.site.register(Conversation_bot_context)
