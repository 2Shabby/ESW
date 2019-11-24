from django.db import models
from django.utils  import timezone


class MainModel(models.Model):
	temp = models.DecimalField(decimal_places=3, max_digits=7, default=0)
	humidity = models.DecimalField(decimal_places=3, max_digits=7, default=0)
	energy_1 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	energy_2 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	energy_3 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	energy_4 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	energy_5 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	power_1 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	power_2 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	power_3 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	power_4 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	power_5 = models.DecimalField(decimal_places=3, max_digits=13, default=0)
	time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.pk)
