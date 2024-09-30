from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework_simplejwt.authentication import JWTAuthentication

from orders.models import Order
from project import settings

# Create your views here.

PAYMOB_API_KEY = "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1RrM01UTXhMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuLUJ5UHc2R0otTXlKNzYtY0pfSmJWNVZtdUtNd2tLRndDeXM3MG9Vd0hSYk5sY05UWEZQR1EyXzJULThLQi1pNmFESmRhMXZ2U093QmIwajI1X3UxV1E="


def get_auth_token():
    url = "https://accept.paymob.com/api/auth/tokens"
    headers = {
        "Content-Type": "application/json",
    }
    data = {"api_key": PAYMOB_API_KEY}

    response = requests.post(url, json=data)

    if response.status_code == 201:
        return response.json().get("token")
    else:
        raise Exception(f"Error authenticating with Paymob: {response.content}")


def create_order(amount_cents=1000, currency="EGP", auth_token=get_auth_token()):
    url = "https://accept.paymob.com/api/ecommerce/orders"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    data = {
        "delivery_needed": "false",
        "amount_cents": amount_cents,
        "currency": currency,
        "items": [],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return response.json().get("id")
    else:
        raise Exception(f"Error creating order: {response.content}")


def generate_payment_key(
    amount_cents, order_id, user, integration_id=4839275, auth_token=get_auth_token()
):
    url = "https://accept.paymob.com/api/acceptance/payment_keys"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    data = {
        "amount_cents": amount_cents,
        "expiration": 3600,
        "order_id": order_id,
        "billing_data": {
            "apartment": "NA",
            "email": user.email or user.username,
            "floor": "NA",
            "first_name": user.first_name or user.username,
            "last_name": user.last_name or user.username,
            "street": "NA",
            "building": "NA",
            "phone_number": "NA",
            "shipping_method": "NA",
            "postal_code": "NA",
            "city": "NA",
            "country": "EG",
            "state": "NA",
        },
        "currency": "EGP",
        "integration_id": integration_id,
        "lock_order_when_paid": "false",
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return response.json().get("token")
    else:
        raise Exception(f"Error generating payment key: {response.content}")


def redirect_to_paymob(token):
    return (
        f"https://accept.paymob.com/api/acceptance/iframes/870346?payment_token={token}"
    )


@api_view(["POST", "GET"])
def payment_callback(request):
    try:
        paymob_order_id = request.query_params.get("order")
        order = Order.objects.get(paymob_order_id=paymob_order_id)
        order.payment_status = Order.PaymentStatus.PAID
        order.status = Order.Status.IN_PROGRESS
        order.save()
        email = EmailMessage(
            subject="User Payed for Order",
            body=f"""
            Your order has been successfully paid.
            Name: {order.client.name}
            Email: {order.client.email}
            Phone: {order.client.phone_numbers.first().phone_number}
            Created At: {order.created_at}
            Amount: {order.post.delivery_fee}
            
            Please contact client to deliver.
            
            Thank you.
        """,
            from_email=settings.EMAIL_HOST_USER,
            to=[order.post.created_by.user.email],
        )
        email.send()
    except Exception as e:
        print(str(e))

    return Response({"status": "success", "message": "Payment received successfully"})


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(["POST"])
def generate_iframe(request):
    amount_cents = request.data.get("amount_cents")
    auth_token = get_auth_token()
    user = request.user
    order_id = create_order(
        amount_cents=amount_cents, currency="EGP", auth_token=auth_token
    )
    token = generate_payment_key(
        amount_cents=amount_cents, order_id=order_id, auth_token=auth_token, user=user
    )
    return Response({"iframe": redirect_to_paymob(token)})


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(["POST"])
def pay_now(request):
    try:
        order = Order.objects.get(id=request.data.get("order_id"))
        amount_cents = round(order.post.delivery_fee) * 100
        print(amount_cents)
        auth_token = get_auth_token()
        user = request.user
        order_id = create_order(
            amount_cents=amount_cents, currency="EGP", auth_token=auth_token
        )
        token = generate_payment_key(
            amount_cents=amount_cents,
            order_id=order_id,
            auth_token=auth_token,
            user=user,
        )
        order.paymob_order_id = order_id
        return Response({"iframe": redirect_to_paymob(token)}, status=200)
    except Exception as e:
        print(str(e))
        return Response({"message": str(e)}, status=400)
