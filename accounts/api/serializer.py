from rest_framework import serializers
from accounts.models import Account


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    def validate(self, attrs):
        email = attrs.get('email', '')
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        username = attrs.get('username', '')
        if Account.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ('Username is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    class Meta:
        model = Account
        # Tuple of serialized model fields
        fields = ("id", "username", "email", "password", "first_name",
                  "last_name", "mobile_number", )


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ("username", "email")
