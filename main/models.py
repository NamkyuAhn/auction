from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'categories'

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    start_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(1)])
    expire_date = models.DateField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'items'

class Item_Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name = 'item_image')
    image = models.FileField(upload_to="item_images")
    
    class Meta:
      db_table = 'item_images'

class Item_Entry(models.Model):
    item = models.ForeignKey('main.Item', on_delete = models.CASCADE, related_name = 'item_entry')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(1)])
    entered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'item_entries'

