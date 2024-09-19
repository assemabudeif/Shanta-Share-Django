from drf_extra_fields.fields import Base64ImageField

from authentication.models import Client
from authentication.serializers import ClientSerializer
from orders.models import Order
from rest_framework import serializers

from posts.models import Post
from posts.serializers import GETPostSerializer

# post_id = serializers.IntegerField(read_only=True)
    # client_id = serializers.IntegerField(read_only=True)
    # post = GETPostSerializer(read_only=True)
    # client = ClientSerializer(read_only=True)

    # def get_fields(self):
    #     request = self.context['request']
    #     fields = super(OrdersSerializer, self).get_fields()
    #     allowed = []
    #     if request and request.method == 'POST':
    #         allowed = ['post_id', 'client_id']
    #     else:
    #         allowed = ['post', 'client']
    #
    #     allowed_fields = {}
    #     for key in allowed:
    #         allowed_fields[key] = fields[key]
    #     return allowed_fields

    # def create(self, validated_data):
    #     post_id = validated_data.pop('post_id')
    #     client_id = validated_data.pop('client_id')
    #
    #     post = Post.objects.get(id=post_id)
    #     client = Client.objects.get(id=client_id)
    #
    #     return Order.objects.create(post=post, client=client, **validated_data)

class POSTOrdersSerializer(serializers.ModelSerializer):
    cargo_image = Base64ImageField()
    client_notes = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Order
        fields = '__all__'



class GETOrdersSerializer(serializers.ModelSerializer):
    # cargo_image = Base64ImageField()
    post = GETPostSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'