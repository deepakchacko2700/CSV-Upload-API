from rest_framework import serializers 
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate_age(self, age):
        """
        validate whether age is in between 0 and 120
        """
        if age < 0 or age > 120:
            raise serializers.ValidationError('Age should be  between 0 and 120')
        return age
    
