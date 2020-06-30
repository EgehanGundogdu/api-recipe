from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as auth_password_validator  # noqa
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as BaseAuthTokenSerializer  # noqa
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the user instances.
    """
    class Meta:
        model = get_user_model()
        fields = [
            "email", "password", "first_name", "last_name"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        """
        Validates to password value with built in
        django auth password validators.
        """
        try:
            auth_password_validator(value, self.instance)
            return value
        except serializers.ValidationError:
            raise serializers.ValidationError(self.errors['password'])

    def create(self, validated_data):
        """
        Create new user with validated data.
        uses the create_user method of the defined user model
        instead of the default model create method."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


class AuthTokenSerializer(BaseAuthTokenSerializer):
    """
    Authentication token serializer. Retrieves credentials \
    and tries to authenticate user.
    Inheriting the default rest framework obtain token serializer.
    Username field has been deprecated.
    """
    email = serializers.EmailField(label=_('email'))
    username = None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(
                    msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(
                msg, code='authorization')

        attrs['user'] = user
        return attrs
