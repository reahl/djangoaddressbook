from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddressForm
from .models import Address, UserError
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction

def index(request):
    addresses = Address.objects.all()
    return render(request, 'index.html', {'addresses': addresses})


class AddAddressView(CreateView):
    template_name = 'add.html'
    model = Address
    fields = ['name', 'email_address']
    success_url = "/"


# def add(request):
#     if request.method == 'POST':
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = AddressForm()
#     return render(request, 'add.html', {'form': form})

# class EditAddressView(UpdateView):
#     template_name = 'edit.html'
#     model = Address
#     fields = ['name', 'email_address']
#     success_url = '/'


def edit(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            if 'delete' in request.POST:
                address.delete()
            elif 'do_something_complicated' in request.POST:
                try:
                    with transaction.atomic():
                        address.do_something_complicated()
                        address.save()
                except UserError as e:
                    messages.error(request, str(e))
            else:
                form.save()
            return redirect('index')
    else:
        form = AddressForm(instance=address)
    return render(request, 'edit.html', {'form': form})

