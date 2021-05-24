#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from .models import Menu_Item
#from .foods import backup_custom_food

# unused, see orders.order_forms.MenuItemCreationForm
#@receiver(post_save, sender=Menu_Item)
#def create_menu_item(sender, instance, created, **kwargs):
    #if created:
        #backup_custom_food(
            #instance.pk,
            #instance.name,
            #instance.food_group
        #)

