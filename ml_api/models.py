from django.db import models

class HousePrediction(models.Model):
    crim = models.FloatField()
    zn = models.FloatField()
    indus = models.FloatField()
    chas = models.FloatField()
    nox = models.FloatField()
    rm = models.FloatField()
    age = models.FloatField()
    dis = models.FloatField()
    rad = models.FloatField()
    tax = models.FloatField()
    ptratio = models.FloatField()
    b = models.FloatField()
    lstat = models.FloatField()
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
