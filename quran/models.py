from django.db import models

class Sura(models.Model):
    """Sura (chapter) of the Quran"""

    REVELATION_CHOICES = (
        ('Meccan', 'Meccan'),
        ('Medinan', 'Medinan'),
    )

    number = models.IntegerField(primary_key=True, verbose_name='Sura Number')
    name = models.CharField(max_length=50, verbose_name='Sura Name')
    tname = models.CharField(max_length=50, verbose_name='English Transliterated Name')
    ename = models.CharField(max_length=50, verbose_name='English Name')
    order = models.IntegerField(verbose_name='Revelation Order')
    type = models.CharField(max_length=7, choices=REVELATION_CHOICES, verbose_name='')
    rukus = models.IntegerField(verbose_name='Number of Rukus')
    bismillah = models.CharField(max_length=50, blank=True, verbose_name='Bismillah')

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return self.name


class Aya(models.Model):
    """Aya (verse) of the Quran"""

    number = models.IntegerField(verbose_name='Aya Number')
    sura = models.ForeignKey(Sura, db_index=True)
    text = models.TextField()

    class Meta:
        unique_together = (('number', 'sura'))
        ordering = ['number']

    def __unicode__(self):
        return self.text


class Root(models.Model):
    """Root word"""

    letters = models.CharField(max_length=10, unique=True, db_index=True) # to my knowledge, there is no root with more than 7 letters

    def __unicode__(self):
        return self.letters


class Word(models.Model):
    """Arabic word in the Quran"""

    aya = models.ForeignKey(Aya, db_index=True)
    number = models.IntegerField()
    token = models.CharField(max_length=50, db_index=True)
    root = models.ForeignKey(Root, null=True, db_index=True)

    class Meta:
        unique_together = (('aya', 'number'))
        ordering = ['number']

    def __unicode__(self):
        return self.token