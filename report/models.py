from django.db import models

from django.db import models


class Unit(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return 'U' + str(self.id) + ' - ' + self.name


class Person(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return 'P' + str(self.id) + ' - ' + self.first_name + " " + self.last_name + ": " + self.description


class Report(models.Model):
    date = models.DateField(auto_now=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return 'R' + str(self.id)


class ReportEntry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    report = models.ForeignKey(Report, related_name='report_entries', on_delete=models.CASCADE)

    def __str__(self):
        return 'RE' + str(self.id)