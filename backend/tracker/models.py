from django.db import models
class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=250)
    category = models.CharField(max_length=100)
class Snapshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="snapshots")
    source = models.CharField(max_length=100)
    url = models.URLField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    available = models.BooleanField(default=True)
    checked_at = models.DateTimeField()
    class Meta:
        ordering = ["checked_at"]
        constraints = [models.UniqueConstraint(fields=["product","source","checked_at"], name="unique_observation")]
