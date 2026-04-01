from rest_framework import serializers
from .models import Media, Settings, Country, Region, District, OurInstagramStory, CustomerFeedback


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'type']


class SettingsSerializer(serializers.ModelSerializer):
    home_image = MediaSerializer(read_only=True)
    home_image_id = serializers.PrimaryKeyRelatedField(
        queryset=Media.objects.all(), source='home_image', write_only=True
    )

    class Meta:
        model = Settings
        fields = ['id', 'home_image', 'home_image_id', 'home_title', 'home_subtitle']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'code']


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source='region', write_only=True
    )

    class Meta:
        model = District
        fields = ['id', 'name', 'region', 'region_id']


class OurInstagramStorySerializer(serializers.ModelSerializer):
    image = MediaSerializer(read_only=True)
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=Media.objects.all(), source='image', write_only=True
    )

    class Meta:
        model = OurInstagramStory
        fields = ['id', 'image', 'image_id', 'story_link']


class CustomerFeedbackSerializer(serializers.ModelSerializer):
    customer_image = MediaSerializer(read_only=True)
    customer_image_id = serializers.PrimaryKeyRelatedField(
        queryset=Media.objects.all(), source='customer_image', write_only=True, allow_null=True
    )

    class Meta:
        model = CustomerFeedback
        fields = [
            'id', 'description', 'rank',
            'customer_name', 'customer_position',
            'customer_image', 'customer_image_id'
        ]