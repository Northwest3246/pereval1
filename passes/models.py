from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+79991234567'"
            )
        ]
    )

    def __str__(self):
        return f"{self.name} {self.fam}"

    class Meta:
        db_table = 'users'

class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    height = models.IntegerField()

    def __str__(self):
        return f"({self.latitude}, {self.longitude}) @ {self.height}m"

    class Meta:
        db_table = 'coordinates'

class Level(models.Model):
    LEVEL_CHOICES = [
        ('', 'Нет'),
        ('1А', '1А'),
        ('2А', '2А'),
        ('3А', '3А'),
        ('4А', '4А'),
        ('5А', '5А')
    ]
    winter = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)
    summer = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)
    autumn = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)
    spring = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"W:{self.winter} S:{self.summer} A:{self.autumn} Sp:{self.spring}"

    class Meta:
        db_table = 'levels'

class Pass(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('pending', 'В модерации'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]
    beauty_title = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True, null=True)
    connect = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'passes'

class Image(models.Model):
    pass_object = models.ForeignKey(Pass, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title or "Изображение"

        class Meta:
            db_table = 'images'

# Create your models here.
