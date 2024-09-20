from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    # client_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'client', 'client_name', 'driver', 'rating', 'review_text', 'review_date']

    def get_client_name(self, obj):
        if obj.client:
            return obj.client.name  

    # هنا بنجيب صورة الـ Client
    # def get_client_picture(self, obj):
    #     if obj.client:
    #         return obj.client.profile_picture  
    #     return None
