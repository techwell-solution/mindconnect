from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully. We will get back to you soon.")
            return redirect ('contact')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact.html', {'form': form})
            
