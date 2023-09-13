from rest_framework.generics import get_object_or_404

from .models import Person
from .serializers import PersonSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse


class CreatePersonView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'pk'

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        if lookup_value.isdigit():
            self.lookup_field = 'pk'
        else:
            self.lookup_field = 'name'
        return super().get_object()

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers={'Location': reverse('create-person')})


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Location': reverse('person-detail', args=[serializer.instance.pk])})

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, headers={'Location': reverse('create-person')})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
