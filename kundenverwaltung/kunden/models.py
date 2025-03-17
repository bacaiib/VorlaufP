from django.db import models

class Kunde(models.Model):
    kunden_nr = models.AutoField(primary_key=True)
    firma = models.CharField(max_length=60)
    anschrift = models.CharField(max_length=60)
    telefon_nr = models.CharField(max_length=20, blank=True)
    fax_nr = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    stadt = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firma} ({self.kunden_nr})"

class Vermerk(models.Model):
    gespraechs_id = models.AutoField(primary_key=True)
    datum = models.DateField(auto_now_add=True)
    uhrzeit = models.TimeField()
    kontaktart = models.CharField(
        max_length=18,
        choices=[('Eingehender Anruf', 'Anruf von'),
                 ('Ausgehender Anruf', 'Anruf bei'),
                 ('Im Büro', 'Besuch von'),
                 ('Beim Kunden', 'Besuch bei')],
        default='Anruf'
    )
    anrede = models.CharField(
        max_length=10,
        choices=[('Herr', 'Herr'), ('Frau', 'Frau'), ('Divers', 'Divers')],
        default='Herr'
    )
    name = models.CharField(max_length=30)
    betreff = models.CharField(max_length=40)
    wunsch = models.CharField(
        max_length=20,
        choices=[('wünscht Rückruf', 'wünscht Rückruf'), ('wünscht Termin', 'wünscht Termin'), ('ruft wieder zurück', 'ruft wieder an')],
        default='wünscht Rückruf'
    )
    gespraechsinhalt = models.TextField()
    firmen_id = models.ForeignKey(Kunde, on_delete=models.CASCADE, related_name='vermerke')

    aufgenommen = models.CharField(max_length=40, default='')
    verfuegung = models.CharField(max_length=40, default='')

    def save(self, *args, **kwargs):
        if not self.pk:
            from django.utils import timezone
            self.uhrzeit = timezone.localtime(timezone.now()).time().replace(second=0, microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Gespräch {self.gespraechs_id} für {self.firmen_id.firma}"

# Create your models here.
