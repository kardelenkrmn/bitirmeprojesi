from django.db import models
from django.contrib.auth.models import User




class Product(models.Model):
    GEEKS_CHOICES = ( 
    ("Rent", "Rent"), 
    ("Sale", "Sale"), 
)
    BRAND_CHOICES = ( 
    ("Building", "Building"), 
    ("Detached", "Detached"), 
)
    CITY_CHOICES = ( 
    ("istanbul", "İstanbul"), 
    ("ankara", "Ankara"), 
)
    ROOM_CHOICES = ( 
    ("1+1", "1+1"), 
    ("2+1", "2+1"), 
    ("3+1", "3+1"),
    ("4+1", "4+1"),
    ("5+1", "5+1"),
    ("6+1", "6+1"),
    ("7+1", "7+1"),

)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    durum = models.CharField(choices=GEEKS_CHOICES, max_length=50, null=True)
    brand = models.CharField(choices=BRAND_CHOICES, max_length=50, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="Product Image", null=True)
    price = models.IntegerField(null=True)
    location = models.CharField(choices=CITY_CHOICES,max_length=50, null=True)
    adres = models.TextField(null=True)
    metre = models.IntegerField(null=True)
    room_number = models.CharField(choices=ROOM_CHOICES, max_length=50, null=True)
    kat_sayısı = models.IntegerField(null=True)
    asansor = models.BooleanField(null=True)
    güvenlik= models.BooleanField(null=True)
    otopark = models.BooleanField(null=True)
    havuz = models.BooleanField(null=True)
    favori = models.ManyToManyField(User, related_name="FavoriyeEkleyenler", verbose_name=("Favoriye ekleyenler"))


    def _str_(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Ürünler"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Product Image")

class Profil(models.Model):#her kullanıcının 1 tane hesabı olması üye olurken girdiği özellikler.kullanıcı girerken diyerlerini number ve birthdayt  içeride dolduruyor.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    birtdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Profiller"

class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adress = models.TextField(null=True, blank=True)
    province = models.CharField(max_length=150,null=True, blank=True)
    district = models.CharField(max_length=150,null=True, blank=True)
    neighbourhood = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Adresler"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Yorumlar"


class Text(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)


