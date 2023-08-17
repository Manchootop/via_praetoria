from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password')

    # Fix problem with password in plain text
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        return super().validate(data)

    # Remove password from response
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('password')
        return result
