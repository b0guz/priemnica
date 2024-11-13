import json

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

PAGE_SIZE = 10


def elements_list(request, object_type, template, url):
    element_list = object_type.objects.get_queryset().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(element_list, PAGE_SIZE)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, template, {'page_obj': page_obj, 'link': url})


def element_create(request, form_type, modal_form='includes/modal_form.html'):
    if request.method == 'POST':
        form = form_type(request.POST)
    else:
        form = form_type()
        return render(request, modal_form, {'form': form, })

    return save_elements_form(request, form, None, modal_form)


def element_update(request, pk, object_type, form_type, modal_form='includes/modal_form.html'):
    element = get_object_or_404(object_type, pk=pk)
    if request.method == 'POST':
        form = form_type(request.POST, instance=element)
    else:
        form = form_type(instance=element)
        return render(request, modal_form, {'form': form, 'element': element})

    return save_elements_form(request, form, element, modal_form)


def save_elements_form(request, form, element, modal_form):
    if form.is_valid():
        form.save()
        title = next(iter(form.cleaned_data))
        short_name = form.cleaned_data.get(title)
        message = f'{short_name}'
        if element:
            message += " edited"
        else:
            message += " added"

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "elementListChanged": None,
                    "showMessage": message
                })
            })
    else:
        return render(request, modal_form, {'form': form, 'element': element})


def element_delete_modal(request, pk, object_type, url):
    element = get_object_or_404(object_type, pk=pk)
    return render(request, 'includes/modal_delete.html', {
        'element': element, 'link': url
    })


def element_delete(request, pk, object_type, url):
    element = get_object_or_404(object_type, pk=pk)
    if request.method == 'POST':

        try:
            element.delete()
        except ProtectedError:
            messages.error(request, u"ERROR. This element is use. You can't delete it.", 'danger')
            return render(request, 'includes/modal_delete.html', {'element': element, 'link': url})

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "elementListChanged": None,
                    "showMessage": f"{element} deleted"
                })
            }
        )
    else:
        return render(request, 'includes/modal_delete.html', {
            'element': element, 'link': url
        })
