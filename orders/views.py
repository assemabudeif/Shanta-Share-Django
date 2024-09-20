from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import UserType
from orders.models import Order
from orders.serializers import POSTOrdersSerializer, GETOrdersSerializer
from posts.models import Post


# Create your views here.

# For Client
class ClientOrderView(APIView):
    permission_classes([IsAuthenticated])
    authentication_classes([JWTAuthentication])

    def get(self, request):
        if request.user.user_type == UserType.CLIENT:
            order_id = request.query_params.get('order_id')
            try:
                order = Order.objects.all().get(id=order_id, client=self.request.user)
                serializer = GETOrdersSerializer(order)
                return Response({
                    "status": "success",
                    "message": "Order found successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            except Order.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Order not found"
                }, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "Only clients can see their orders"
            }, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if request.user.user_type == UserType.CLIENT:
            data = request.data
            data["client"] = request.user.id
            serializer = POSTOrdersSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Order added successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "status": "error",
                "message": "Failed to add order, data is not valid",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "Only clients can create orders"
            }, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request):
        order_id = self.request.query_params.get('order_id')
        if request.user.user_type == UserType.CLIENT:
            print(request.method)
            try:
                order = Order.objects.all().get(id=order_id, client=request.user)
                serializer = POSTOrdersSerializer(order, data=request.data)
                print(serializer)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status": "success",
                        "message": "Order updated successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
                return Response({
                    "status": "error",
                    "message": "Failed to update order, data is not valid",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            except Order.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Order not found"
                }, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "Only clients can update their orders"
            }, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        order_id = self.request.query_params.get('order_id')
        if request.user.user_type == UserType.CLIENT:
            try:
                order = Order.objects.all().get(id=order_id, client=request.user)
                order.delete()
                return Response({
                    "status": "success",
                    "message": "Order deleted successfully",
                }, status=status.HTTP_200_OK)

            except Order.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Order not found"
                }, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "Only clients can delete their orders"
            }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_clients_orders(request):
    if request.user.user_type == UserType.CLIENT:
        orders = Order.objects.filter(client=request.user)
        serializer = GETOrdersSerializer(orders, many=True)
        return Response({
            "status": "success",
            "message": "Orders found successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "message": "Only clients can see their orders"
        }, status=status.HTTP_403_FORBIDDEN)


# For Driver
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_driver_orders(request):
    if request.user.user_type == UserType.DRIVER:
        orders = Order.objects.all()
        print(request.user.id)
        for order in orders:
            if order.post.created_by.id != request.user.id:
                orders = orders.exclude(id=order.id)

        serializer = GETOrdersSerializer(orders, many=True)
        return Response({
            "status": "success",
            "message": "Orders found successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "message": "Only drivers can see their orders"
        }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_driver_single_order(request):
    if request.user.user_type == UserType.DRIVER:
        order_id = request.query_params.get('order_id')
        try:
            order = Order.objects.all().get(id=order_id)
            if order.post.created_by.id == request.user.id:
                serializer = GETOrdersSerializer(order)
                return Response({
                    "status": "success",
                    "message": "Order found successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "You are not authorized to see this order"
                }, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            "status": "error",
            "message": "Only drivers can see their orders"
        }, status=status.HTTP_403_FORBIDDEN)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_order_status(request):
    order_status_list = ['pending', 'in_progress', 'completed', 'canceled', 'rejected']

    if request.user.user_type == UserType.DRIVER:
        order_id = request.query_params.get('order_id')
        order_status = request.query_params.get('order_status')
        try:
            order = Order.objects.all().get(id=order_id)
            if order.post.created_by.id == request.user.id:
                if order_status in order_status_list:
                    order.status = order_status
                    # if order_status == 'completed':
                    #     order.payment_status = 'paid'
                    order.save()
                    return Response({
                        "status": "success",
                        "message": "Order status updated successfully",
                        "data": GETOrdersSerializer(order).data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error",
                        "message": "Invalid order status"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "status": "error",
                    "message": "You are not authorized to see this order"
                }, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "status": "error",
            "message": "Only drivers can change their orders status"
        }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_post_orders(request):
    if request.user.user_type == UserType.DRIVER:
        post_id = request.query_params.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
            if post.created_by.id == request.user.id:
                orders = Order.objects.filter(post=post)
                serializer = GETOrdersSerializer(orders, many=True)
                return Response({
                    "status": "success",
                    "message": "Orders found successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Not allowed to see other drivers orders"
                }, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Post not found"
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            "status": "error",
            "message": "Only clients can see their orders"
        }, status=status.HTTP_403_FORBIDDEN)


# For Admin
class AdminOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        print(f"User: {request.user}")
        if request.user.admin:
            orders = Order.objects.all()
            serializer = GETOrdersSerializer(orders, many=True)
            return Response({
                "status": "success",
                "message": "Orders found successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "message": "Only admins can see all orders"
            }, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request):
        if request.user.user_type == UserType.ADMIN:
            try:
                order_id = request.data.get('order_id')
                order = Order.objects.get(id=order_id)
                serializer = POSTOrdersSerializer(order, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status": "success",
                        "message": "Order updated successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)

                return Response({
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            except Order.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Order not found"
                }, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "Only admins can update orders"
            }, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        if request.user.user_type == UserType.ADMIN:
            try:
                order_id = request.data.get('order_id')
                order = Order.objects.get(id=order_id)
                order.delete()
                return Response({
                    "status": "success",
                    "message": "Order deleted successfully"
                }, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Order not found"
                }, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "message": "Only admins can delete orders"
            }, status=status.HTTP_403_FORBIDDEN)
