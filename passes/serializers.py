from rest_framework import serializers
from .models import User, Coordinates, Level, Pass, Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude', 'height']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'title']

class PassSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordinatesSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Pass
        fields = [
            'id', 'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'user', 'coords', 'level', 'images', 'status'
        ]
        read_only_fields = ['status']

        def create(self, validated_data):
            user_data = validated_data.pop('user')
            coords_data = validated_data.pop('coords')
            level_data = validated_data.pop('level')
            images_data = validated_data.pop('images', [])

            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults=user_data
            )
            coords = Coordinates.objects.create(**coords_data)
            level = Level.objects.create(**level_data)
            pas = Pass.objects.create(
                user=user,
                coords=coords,
                level=level,
                status='new',
                **validated_data
            )
            for img_data in images_data:
                Image.objects.create(pass_object=pas, **img_data)
                return pas

        def update(self, instance, validated_data):
            if instance.status != 'new':
                raise serializers.ValidationError("Редактирование запрещено: статус не 'new'")
            if 'user' in validated_data:
                raise serializers.ValidationError("Нельзя изменять данные пользователя")

            coords_data = validated_data.pop('coords', None)
            if coords_data:
                coords = instance.coords
                for attr, value in coords_data.items():
                    setattr(coords, attr, value)
                coords.save()

            level_data = validated_data.pop('level', None)
            if level_data:
                level = instance.level
                for attr, value in level_data.items():
                    setattr(level, attr, value)
                level.save()

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance