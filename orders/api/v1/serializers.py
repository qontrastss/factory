from rest_framework import serializers

from orders.models import AttachmentOrder, Order


class OrderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentOrder
        fields = ['id', 'file']


class OrderSerializer(serializers.ModelSerializer):
    files = OrderFileSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['title', 'files']

    def create(self, validated_data):
        request = self.context.get('request')
        instance = self.Meta.model(**validated_data)
        instance.user = request.user if not request.user.is_anonymous else None
        instance.save()

        for file in request.FILES.getlist("files"):
            AttachmentOrder.objects.create(order=instance, file=file)
        return instance


class OrderDetailSerializer(serializers.ModelSerializer):
    files = OrderFileSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'
