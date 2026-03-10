from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True) # “I will ACCEPT this field, but I will NEVER SHOW it.”

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]  # pass2 is me defining
        extra_kwargs = {"password": {"write_only": True}}  # set password field as write only 
        
    def save(self): # Logic must ALWAYS run, no matter where the object is created
        password = self.validated_data['password'] # Access pass 1 from validated data
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"Error":"P1 and P2 should be same"})

        if User.objects.filter(email=self.validated_data['email']).exists(): 
            raise serializers.ValidationError({"Error":"Email already exists!"})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password) # HASHES THE PASSWORD
        account.save()
        return account # CONTAINS EMAIL AND USERNAME
        

""" by default django doesn't support same email"""
