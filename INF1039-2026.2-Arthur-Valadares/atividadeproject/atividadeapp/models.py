from django.db import models

class Livro(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=70)
    genre = models.CharField(max_length=30)
    release_date = models.DateField()

class Lugar(models.Model):
    options = [("L", "Logo"), ("A", "Algum dia"), ("S", "Sonho")]
    categories = [("P", "Praia"), ("C", "Cidade"), ("N", "Natureza")]

    title = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    when = models.CharField(max_length=1, choices=options)
    category = models.CharField(max_length=1, choices=categories)
