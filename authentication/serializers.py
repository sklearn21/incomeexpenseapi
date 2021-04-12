from rest_framework.serializers import ModelSerializer
from authentication import User


class RegisterSerializer(ModelSerializer):
    """Serializer for User model."""

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        """Validation for User."""

        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters.')
        
        return attrs

    def create(self, validated_data):
        """Create user with validated data."""
        return User.objects.create_user(**validated_data)

        return super().validate(attrs)
        

