from django.db import models

class Location(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    
    def __str__(self):
        return "%s" % self.title

class ArtPiece(models.Model):
    title = models.CharField(max_length=200)
    purchase_price = models.DecimalField(verbose_name=None, name=None, 
                                        max_digits=10, 
                                        decimal_places=2)
    artist = models.CharField(max_length=200)
    purchase_date = models.DateField()
    notes = models.TextField()
    location = models.ForeignKey(Location)
    
    def __str__(self):
        return "%s" % self.title
    
class ArtPiecePhoto(models.Model):
    filename = models.CharField(max_length=200)
    piece = models.ForeignKey(ArtPiece)
    
    def __str__(self):
        return "%s" % self.filename