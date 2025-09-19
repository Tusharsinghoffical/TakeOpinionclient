from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def booking_page(request: HttpRequest) -> HttpResponse:
    return render(request, "bookings/booking.html")


def post_payment(request: HttpRequest) -> HttpResponse:
    return render(request, "bookings/post_payment.html")

# Create your views here.
