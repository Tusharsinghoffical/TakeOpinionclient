from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Hospital


def hospitals_list(request: HttpRequest) -> HttpResponse:
    hospitals = Hospital.objects.all()
    return render(request, "hospitals/list.html", {"hospitals": hospitals})


def hospital_detail(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    return render(request, "hospitals/detail.html", {"hospital": hospital})

# Create your views here.
