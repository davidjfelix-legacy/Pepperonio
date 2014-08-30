from rest_framework import serializers
from .models import (
	HotPizzasUser,
	Product,
	ProductType,
	ProductConfiguration,
	CustomerInformation,
	Location
)

class LocationSerializer(serializers.HyperlinkedModelSerializer):
	
	class Meta:
		model = Location
		fields = (
			'longitude',
			'latitude'
		)


class HotPizzasUserSerializer(serializers.HyperlinkedModelSerializer):
	
	class Meta:
		model = HotPizzasUser
		

class ProductSerializer(serializers.HyperlinkedModelSerializer):

	longitude = serializers.Field(source='location.longitude')
	latitude = serializers.Field(source='location.latitude')
	configurations= serializers.RelatedField(many=True)

	class Meta:
		model = Product
		fields = (
			'url',
			'cook_time',
			'expiration_time',
			'base_price',
			'delivered',
			'request_time',
			'customer',
			'configurations',
			'longitude',
			'latitude',
		)


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):	

	class Meta:
		model = ProductType
		fields = (
			'url',
			'name',
			'configurations',
		)


class ProductConfigurationSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = ProductConfiguration
		fields = (
			'url',
			'description',
			'product_type'
		)

