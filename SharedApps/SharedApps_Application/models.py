from django.db import models



class certificateDb(models.Model):
	Dev = 1
	QA = 2
	UAT = 3
	Production = 4
	environment_TYPES = (	(Dev, 'Dev'),	(QA, 'QA'),	(UAT, 'UAT'),	(Production, 'Production'), )
	application = models.CharField(db_column='Application', max_length=255, blank=True, null=True)  # Field name made lowercase.
	startdate = models.DateField(null=True)
	expiredate = models.DateField(null=True)
	environment_type = models.PositiveSmallIntegerField(choices=environment_TYPES)
	File = models.FileField(upload_to='CSR/', null=True , blank = True)
	bytes = models.BinaryField(blank=True, editable = True)
	def __str__(self):
		return self.application


class serviceDb(models.Model):
	Dev = 1
	QA = 2
	UAT = 3
	Production = 4
	environment_TYPES = (	(Dev, 'Dev'),	(QA, 'QA'),	(UAT, 'UAT'),	(Production, 'Production'), )
	application = models.CharField(db_column='Application', max_length=255, blank=True, null=True)  # Field name made lowercase.
	startdate = models.DateField(null=True)
	expiredate = models.DateField(null=True)
	environment_type = models.PositiveSmallIntegerField(choices=environment_TYPES)

class servic(models.Model):
	application = models.CharField(db_column='Application', max_length=255, blank=True, null=True)  # Field name made lowercase.
	startdate = models.DateField(null=True)