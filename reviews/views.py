from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsDriverOrClient

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsDriverOrClient]

    def get_queryset(self):
        # Filter reviews by the driver's ID
        user = self.request.user
        driver = getattr(user, 'driver', None)

        if driver:
            # Return only reviews related to the logged-in driver
            return Review.objects.filter(driver=driver).all()
        else:
            # If the user is not a driver, return an empty queryset
            return Review.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        client = getattr(user, 'client', None)
        driver = getattr(user, 'driver', None)

        # Save the review with either the client or driver
        if client:
            serializer.save(client=client)
        elif driver:
            serializer.save(driver=driver)
        else:
            # Handle the case where the user is neither a client nor a driver
            serializer.save()
