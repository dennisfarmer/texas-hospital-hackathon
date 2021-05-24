from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    # implementing orders.foods.backup_custom_food within
    # orders.order_forms.MenuItemCreationForm
    # instead of using a signal so that only foods which are created via
    # the website forms (and not by the commandline / scripts) are backed
    # up
    #def ready(self):
        #import orders.signals
