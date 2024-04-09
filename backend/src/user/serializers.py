from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('is_admin', 'username', 'password')

    def create(self, validated_data):
        if validated_data['is_admin']:
            create_func = User.objects.create_superuser
        else:
            create_func = User.objects.create_user

        user = create_func(username=validated_data['username'],
                           password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'username', 'password', 'is_active',
                  'is_admin')

    def update(self, instance, validated_data):
        print(validated_data)
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active',
                                                instance.is_active)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)

        # Update password
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        return self.update(instance, validated_data)
