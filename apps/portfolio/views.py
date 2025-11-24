from django.conf import settings
from django.views.generic.base import TemplateView
from .models import Personal, About, Experience, Description, Education, Technology, Portfolio
from .forms import ContactForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from operator import attrgetter
from django.db.models import Q
from django.http import JsonResponse

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


class HomePageView(TemplateView):
    template_name = 'portfolio/portfolio_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal'] = Personal.objects.all()
        context['about'] = About.objects.all()
        context['technologies'] = Technology.objects.all()
        context['portfolio'] = Portfolio.objects.all()
        context['contact_form'] = ContactForm()
        context['message_sent'] = False
        return context

    def post(self, request, *args, **kwargs):
        print("⚡ POST RECIBIDO")
        form = ContactForm(request.POST)
        print("POST DATA:", request.POST)
        print("ERRORES FORM:", form.errors)
        print(form.errors)
        if form.is_valid():
            print("✅ FORMULARIO VÁLIDO")
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_body = (
                f"Nuevo mensaje desde tu portafolio:\n\n"
                f"Nombre: {your_name}\n"
                f"Email: {your_email}\n"
                f"Asunto: {subject}\n\n"
                f"Mensaje:\n{message}"
            )

            send_mail(
                subject=f"[PORTFOLIO] {subject}",
                message=email_body,
                from_email=settings.EMAIL_HOST_USER,  # tu Gmail
                recipient_list=[settings.EMAIL_HOST_USER],  # te lo envías a ti
                fail_silently=False,
            )

            return JsonResponse({'status': 'success', 'message_sent': True})
        else:
            print("❌ FORMULARIO INVÁLIDO")
            errors = {field: form.errors[field][0] for field in form.errors}
            return JsonResponse({'status': 'error', 'errors': errors})


class DigitalCVPageView(TemplateView):
    template_name = 'portfolio/digital_cv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiences = Experience.objects.all()

        for experience in experiences:
            descriptions = Description.objects.filter(experience=experience).order_by('order_number')
            experience.descriptions.set(descriptions)

        context['experiences'] = experiences
        context['personal'] = Personal.objects.all()
        context['education'] = Education.objects.all()
        context['technologies'] = Technology.objects.all()
        context['portfolio'] = Portfolio.objects.filter(
            Q(filter='filter-certification')
        )
        
        grouped_portfolio = {}
        portfolios = sorted(context['portfolio'], key=attrgetter('year'), reverse=True) 
        for item in portfolios:
            issuer_name = item.issuer.name if item.issuer else "Unknown Issuer"
            if issuer_name not in grouped_portfolio:
                grouped_portfolio[issuer_name] = []
            grouped_portfolio[issuer_name].append(item)

        context['grouped_portfolio'] = grouped_portfolio

        return context
    
    
def handle_not_found(request, exception):
    return render(request, "layouts/page-404.html")
    