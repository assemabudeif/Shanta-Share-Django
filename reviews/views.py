from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsDriverOrClient  

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsDriverOrClient]  

    def perform_create(self, serializer):
        user = self.request.user
        client = getattr(user, 'client', None)
        driver = getattr(user, 'driver', None)

        # # Ensure that we save either client or driver, not both
        # if client:
        #     serializer.save(client=client)
        # elif driver:
        #     serializer.save(driver=driver)
        # else:
        #     # Handle case where user is neither a client nor a driver
        serializer.save()
