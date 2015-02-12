from django.db import models
from django.template.defaultfilters import slugify
import os

class Location(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    
    def photo(self):
        return  self.pieces().count() > 0 and self.pieces()[:1].get().photo() or 'no_image.jpg'
    
    def pieces(self):
        return ArtPiece.objects.filter(location = self.pk)
    
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
    
    def photo(self):
        print self.photos().count()
        return  self.photos().count() > 0 and self.photos()[:1].get().image or 'no_image.jpg'    

    def photos(self):
        return ArtPiecePhoto.objects.filter(piece = self.pk)
    
    def documents(self):
        return ArtPieceDocument.objects.filter(piece = self.pk)    
    
    def slug(self):
        return slugify(self.title) if self.title else 'piece-' + str(self.pk)

    def __str__(self):
        return "%s" % self.title
    
class ArtPiecePhoto(models.Model):
    filename = models.CharField(max_length=200)
    piece = models.ForeignKey(ArtPiece)
    image = models.FileField(upload_to="", null = True)
    
    def __str__(self):
        return "%s" % self.filename
    
class ArtPieceDocument(models.Model):
    document = models.FileField(upload_to="", null = True)
    piece = models.ForeignKey(ArtPiece)
    
    def filename(self):
        return os.path.basename(self.document.name)    
    
    def __str__(self):
        return "%s" % self.document   