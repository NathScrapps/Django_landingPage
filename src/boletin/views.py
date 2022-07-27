from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import RegModelForm, ContactForm
from .models import Registrado
from boletin import forms

# Create your views here.
def inicio(request):
    titulo = "Bienvenidxs"
    if request.user.is_authenticated:
        titulo = "Bienvenidx %s" %(request.user) 
    form = RegModelForm(request.POST or None)
    context = {
        "titulo": titulo,
        "form": form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.nombre:
            instance.nombre = "Usuario"
        instance.save()
        context = {
            "titulo": "Gracias %s!" %(instance.nombre)
        }

    if request.user.is_authenticated and request.user.is_staff:
        queryset = Registrado.objects.all()
        context = {
            "queryset": queryset,
        }
    return render(request, "inicio.html", context)

def contact(request):
    titulo = "Formulario de contacto"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # for key, value in form.cleaned_data.items():
        #     print(key, ":", value)

        # for key in form.cleaned_data:
        #     print(key)
        #     print(form.cleaned_data.get(key))
        form_nombre = form.cleaned_data.get("nombre")
        form_email = form.cleaned_data.get("email")
        form_mensaje = form.cleaned_data.get("mensaje")

        asunto = 'Form de contacto'
        email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
        email_from = settings.EMAIL_HOST_USER
        email_to = [email_from, "natanael639@gmail.com"]
        send_mail(asunto,
            email_mensaje,
            email_from,
            [email_to],
            fail_silently=False
        )
    context = {
        "contact_form": form,
        "titulo": titulo,
    }
    return render(request, "forms.html", context)