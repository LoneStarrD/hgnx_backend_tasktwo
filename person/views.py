from .models import Person
from .serializers import PersonSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse


class PersonListView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def perform_create(self, serializer):
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers={'Location': reverse('person-list')})


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def perform_update(self, serializer):
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Location': reverse('person-detail', args=[serializer.instance.pk])})

    def perform_destroy(self, instance):
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT, headers={'Location': reverse('person-list')})