#!/usr/bin/env python

from rest_framework import generics
from rest_framework import mixins
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from ..serializers import ProductSerializer
from ..models import Product, CustomerInformation, Customer
from ..include import get_coord_offsets

class CustomerFilterMixin(object):
	
	def filter_customer(self):
		customer = self.request.user
		return Product.objects.filter(customer__user=customer)
		
		
class CustomerUndeliveredProductList(CustomerFilterMixin, mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = ProductSerializer
	
	def get_queryset(self):
		queryset = filter_customer()
		return queryset.filter(delivered__isnull=True)
		
		
class LocalizedAvailableProductList(views.APIView):

	def get(self, request, format=None):
		if 'longitude' in request.GET and 'latitude' in request.GET:
			#FIXME: !!! Ensure long and lat parse to float
			longitude = float(request.GET.get('longitude'))
			latitude = float(request.GET.get('latitude'))
			#(long_min, long_max, lat_min, lat_max) = get_coord_offsets(
			#	longitude,
			#	latitude,
			#	10,
			#	'm'
			#)
			products = Product.objects.filter(
				location__longitude__gte=-10.0,#long_min,
				location__longitude__lte=10.0,#long_max,
				location__latitude__gte=-10.0,#lat_min,
				location__latitude__lte=10.0,#lat_max
				customer__isnull=True
			)
			serializer = ProductSerializer(products, many=True)
			return Response(serializer.data)
		else: # Either longitude or latitude aren't in the request queryset
			return Response(
				{'details':'longitude and latitude must be defined in query string. Try adding "?longitude=0.0&latitude=0.0"'},
				status=status.HTTP_400_BAD_REQUEST,
			)	
		

class DriverFilterMixin(object):
	
	def filter_driver(self):
		driver = self.request.user
		return Product.objects.filter(driver__user=driver)


class DriverUnsoldProductList(DriverFilterMixin, mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = ProductSerializer
	
	def get_queryset(self):
		queryset = filter_driver()
		return queryset.filter(customer__isnull=True)


class DriverSoldProductList(DriverFilterMixin, mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = ProductSerializer
	
	def get_queryset(self):
		queryset = filter_driver()
		return queryset.filter(customer__isnull=False)

	
class DriverUndeliveredProductList(DriverFilterMixin, mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = ProductSerializer

	def get_queryset(self):
		queryset = filter_driver()
		return queryset.filter(delivered=False)

	
class DriverDeliveredProducList(DriverFilterMixin, mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = ProductSerializer
	
	def get_queryset(self):
		queryset = filter_driver()
		return queryset.filter(delivered=True)
	

class DriverSoldUndeliveredProductList(DriverFilterMixin, mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = ProductSerializer
	
	def get_queryset(self):
		queryset = filter_driver()
		return queryset.filter(delivered=False, customer__isnull=True)

