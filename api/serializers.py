from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ExamRequest, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('role', 'academic_level', 'institution')


class ExamRequestSerializer(serializers.ModelSerializer):
    requester = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ExamRequest
        fields = ('id', 'requester', 'exam_date', 'location', 'faculty', 'branch', 'semester', 'module_name' ,'status')

class ApplicationSerializer(serializers.ModelSerializer):
    # full User object for the scribe
    scribe = UserSerializer(read_only=True)

    # name of the exam instead of just ID
    exam_request = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'scribe', 'exam_request', 'status', 'created_at')
