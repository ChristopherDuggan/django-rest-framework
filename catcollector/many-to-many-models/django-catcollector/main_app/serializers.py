from rest_framework import serializers
from .models import Cat, Feeding, Toy

class ToySerializer(serializers.ModelSerializer):
  class Meta:
    model = Toy
    fields = '__all__'

class CatSerializer(serializers.ModelSerializer):
  fed_for_today = serializers.SerializerMethodField()
  toys = ToySerializer(many=True, read_only=True)

  class Meta:
    model = Cat
    fields = '__all__'

  def get_fed_for_today(self, obj):
    return obj.fed_for_today()

class FeedingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feeding
    fields = '__all__'
    read_only_fields = ('cat',)
