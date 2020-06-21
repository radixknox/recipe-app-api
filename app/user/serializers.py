from django.contrib.auth import get_user_model,authenticate #return the currently active user model
                                            #– the custom user model if one is specified, or User otherwise

from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email','password','name')
        extra_kwargs = {'password': {'write_only': True,'min_length':5}}


    def create(self,validate_data):
        return get_user_model().objects.create_user(**validate_data)

    def update(self,instance,validate_data):
        password = validate_data.pop('password',None)
        user = super().update(instance,validate_data)
        if password:
            user.set_password(password)
            user.save()
        return user






class AuthTokenSerializers(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
        )

        def validate(self, attrs):
            email = attrs.get('email')
            password = attrs.get('password')

            user = authenticate(
                    request=self.context.get('request'),
                    username=email,
                    password=password
            )
            if not user:
                msg = _('Invalid Credentials')
                raise serializers.ValidationError(msg,code='authorization')


            attrs['user'] = user
            return  attrs
