import json

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.generic import TemplateView, ListView, UpdateView

from .helpers.check_null import check_null_value
from .htmx_crud.htmx_crud import elements_list, element_create, element_update, element_delete
from .models import Supplier, MeatType, DispatchNote, Company
from .forms import SupplierForm, MeatTypeForm, DispatchNoteMultiFormAP, CompanyForm, DispatchNoteMultiFormSid
from .print.accept_meat import generate_accept_form
from .print.accept_meat_small import generate_accept_form_small

# from .import_docs.import_docs import import_docs, import_supplier, import_notes


# Supplier views
@login_required
def supplier_list(request):
    template = 'list_supplier.html'
    return render(request, template)


@login_required
def supplier_table(request):
    object_type = Supplier
    template = 'table_supplier.html'
    url = 'table_supplier'
    return elements_list(request, object_type, template, url)


@login_required
def supplier_create(request):
    form_type = SupplierForm
    return element_create(request, form_type)


@login_required
def supplier_update(request, pk):
    object_type = Supplier
    form_type = SupplierForm
    return element_update(request, pk, object_type, form_type)


@login_required
def supplier_delete(request, pk):
    object_type = Supplier
    url = 'delete_supplier'
    return element_delete(request, pk, object_type, url)


# search supplier for new disnote form
@login_required
def search_supplier(request):
    query = request.GET.get('supplier-id_supplier', '')

    all_suppliers = Supplier.objects.all()
    if query:
        suppliers = all_suppliers.filter(id_supplier__icontains=query)
    else:
        suppliers = []

    context = {'suppliers': suppliers}
    return render(request, 'search_results.html', context)


# list view with search
@login_required
def list_search_view_ap(request):
    search = request.GET.get("search")
    page = request.GET.get("page")
    notes = DispatchNote.objects.filter(company=Company.objects.first()).order_by("-id")
    if search:
        notes = notes.filter(Q(supplier__name__icontains=search) | Q(doc_number__icontains=search)).order_by("-id")
    else:
        search = ''

    paginator = Paginator(notes, 10)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    link = 'list_search_view_ap'

    context = {"page_obj": page_obj, "search": search, "link": link}
    return render(request, "dispatch_list_ap.html", context)


@login_required
def list_search_view_sid(request):
    search = request.GET.get("search")
    page = request.GET.get("page")
    notes = DispatchNote.objects.filter(company=Company.objects.last()).order_by("-id")
    if search:
        notes = notes.filter(Q(supplier__name__icontains=search) | Q(doc_number__icontains=search)).order_by("-id")
    else:
        search = ''

    paginator = Paginator(notes, 10)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    link = 'list_search_view_sid'

    context = {"page_obj": page_obj, "search": search, "link": link}
    return render(request, "dispatch_list_sid.html", context)


@login_required
def meat_list(request):
    template = 'list_meat.html'
    return render(request, template)


@login_required
def meat_table(request):
    object_type = MeatType
    template = 'table_meat.html'
    url = 'table_supplier'
    return elements_list(request, object_type, template, url)


@user_passes_test(lambda u: u.is_superuser)
def meat_create(request):
    form_type = MeatTypeForm
    return element_create(request, form_type)


@user_passes_test(lambda u: u.is_superuser)
def meat_update(request, pk):
    object_type = MeatType
    form_type = MeatTypeForm
    return element_update(request, pk, object_type, form_type)


@user_passes_test(lambda u: u.is_superuser)
def meat_delete(request, pk):
    object_type = MeatType
    url = 'delete_meat'
    return element_delete(request, pk, object_type, url)


# DispatchNote views
@login_required
def index(request):
    return render(request, 'dispatch_home_ap.html')


@login_required
def index_sid(request):
    return render(request, 'dispatch_home_sid.html')


@method_decorator(login_required, name='dispatch')
class DispatchNoteListView(ListView):
    model = DispatchNote
    # context_object_name = 'dispatch_notes'
    template_name = 'dispatch_list.html'
    paginate_by = 10

    def get_queryset(self):
        return DispatchNote.objects.order_by("-id")


@login_required
def add_dispatch_note_ap(request):
    if request.method == "POST":
        form = DispatchNoteMultiFormAP(request.POST)

        supplier = None
        new_supplier = False

        form_supplier = form['supplier']
        supplier_id = form_supplier['id_supplier'].value()

        try:
            supplier = Supplier.objects.get(id_supplier=supplier_id)
        except ObjectDoesNotExist:
            new_supplier = True

        if new_supplier is False:
            form = form['dispatch_note']

        if form.is_valid():
            if new_supplier:
                supplier = form['supplier'].save()
                dispatch_note = form['dispatch_note'].save(commit=False)
            else:
                dispatch_note = form.save(commit=False)

            dispatch_note.supplier = supplier
            dispatch_note.company = Company.objects.first()
            dispatch_note.created_by = request.user

            last_item = DispatchNote.objects.filter(company=dispatch_note.company).order_by('-id').first()
            if last_item is not None:
                if dispatch_note.doc_date.year == last_item.doc_date.year:
                    dispatch_note.index = last_item.index + 1
                else:
                    dispatch_note.index = 1
            else:
                dispatch_note.index = 1

            if dispatch_note.quantity == 0:
                dispatch_note.quantity = None
            if dispatch_note.total_mass == 0:
                dispatch_note.total_mass = None
            if dispatch_note.mass == 0:
                dispatch_note.mass = None

            if dispatch_note.meat_type.pk != 1:
                dispatch_note.passports = None
                dispatch_note.certificate_id = None
                dispatch_note.certificate_number = None

            dispatch_note.save()

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "dispatchNoteListChanged": None,
                        "showMessage": f"{dispatch_note.doc_number} added."
                    })
                })
        else:
            form = DispatchNoteMultiFormAP(data=request.POST)
    else:
        form = DispatchNoteMultiFormAP()

    return render(request, 'dispatch_form.html', {
        'form': form,
    })


@login_required
def add_dispatch_note_sid(request):
    if request.method == "POST":
        form = DispatchNoteMultiFormSid(request.POST)

        supplier = None
        new_supplier = False

        form_supplier = form['supplier']
        supplier_id = form_supplier['id_supplier'].value()

        try:
            supplier = Supplier.objects.get(id_supplier=supplier_id)
        except ObjectDoesNotExist:
            new_supplier = True

        if new_supplier is False:
            form = form['dispatch_note']

        if form.is_valid():
            if new_supplier:
                supplier = form['supplier'].save()
                dispatch_note = form['dispatch_note'].save(commit=False)
            else:
                dispatch_note = form.save(commit=False)

            dispatch_note.supplier = supplier
            dispatch_note.company = Company.objects.last()
            dispatch_note.created_by = request.user

            last_item = DispatchNote.objects.filter(company=dispatch_note.company).order_by('-id').first()
            if last_item is not None:
                if dispatch_note.doc_date.year == last_item.doc_date.year:
                    dispatch_note.index = last_item.index + 1
                else:
                    dispatch_note.index = 1
            else:
                dispatch_note.index = 1

            if dispatch_note.quantity == 0:
                dispatch_note.quantity = None
            if dispatch_note.total_mass == 0:
                dispatch_note.total_mass = None
            if dispatch_note.mass == 0:
                dispatch_note.mass = None

            if dispatch_note.meat_type.pk != 1:
                dispatch_note.passports = None
                dispatch_note.certificate_id = None
                dispatch_note.certificate_number = None

            dispatch_note.save()

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "dispatchNoteListChanged": None,
                        "showMessage": f"{dispatch_note.doc_number} added."
                    })
                })
        else:
            print(form.errors)
            form = DispatchNoteMultiFormSid()
    else:
        form = DispatchNoteMultiFormSid()

    return render(request, 'dispatch_form.html', {
        'form': form,
    })


@method_decorator(login_required, name='dispatch')
class EditDispatchNoteAP(UpdateView):
    model = DispatchNote
    form_class = DispatchNoteMultiFormAP
    success_url = reverse_lazy('home')
    template_name = 'dispatch_form.html'

    def get_form_kwargs(self):
        kwargs = super(EditDispatchNoteAP, self).get_form_kwargs()
        # print(f'kwargs = {kwargs}')
        current_supplier = self.object.supplier

        if 'data' in kwargs:
            old_supplier_id = self.object.supplier.id_supplier
            new_supplier_id = kwargs["data"]["supplier-id_supplier"]

            if old_supplier_id != new_supplier_id:
                try:
                    current_supplier = Supplier.objects.get(id_supplier=new_supplier_id)
                except ObjectDoesNotExist:
                    current_supplier = Supplier.objects.create(name=kwargs["data"]["supplier-name"],
                                                               id_supplier=new_supplier_id,
                                                               address=kwargs["data"]["supplier-address"])
        kwargs.update(instance={
            'dispatch_note': self.object,
            'supplier': current_supplier,
        })

        return kwargs

    def form_valid(self, form):

        supplier = form['supplier'].save()
        dispatch_note = form['dispatch_note'].save(commit=False)

        dispatch_note.supplier = supplier
        dispatch_note.company = Company.objects.first()
        dispatch_note.updated_by = self.request.user

        if dispatch_note.quantity == 0:
            dispatch_note.quantity = None
        if dispatch_note.total_mass == 0:
            dispatch_note.total_mass = None
        if dispatch_note.mass == 0:
            dispatch_note.mass = None

        if dispatch_note.meat_type.pk != 1:
            dispatch_note.passports = None
            dispatch_note.certificate_id = None
            dispatch_note.certificate_number = None

        dispatch_note.save()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "dispatchNoteListChanged": None,
                    "showMessage": f"{dispatch_note.doc_number} updated."
                })
            }
        )


@method_decorator(login_required, name='dispatch')
class EditDispatchNoteSid(UpdateView):
    model = DispatchNote
    form_class = DispatchNoteMultiFormSid
    success_url = reverse_lazy('sid_home')
    template_name = 'dispatch_form.html'

    def get_form_kwargs(self):
        kwargs = super(EditDispatchNoteSid, self).get_form_kwargs()
        # print(f'kwargs = {kwargs}')
        current_supplier = self.object.supplier

        if 'data' in kwargs:
            old_supplier_id = self.object.supplier.id_supplier
            new_supplier_id = kwargs["data"]["supplier-id_supplier"]

            if old_supplier_id != new_supplier_id:
                try:
                    current_supplier = Supplier.objects.get(id_supplier=new_supplier_id)
                except ObjectDoesNotExist:
                    current_supplier = Supplier.objects.create(name=kwargs["data"]["supplier-name"],
                                                               id_supplier=new_supplier_id,
                                                               address=kwargs["data"]["supplier-address"])
        kwargs.update(instance={
            'dispatch_note': self.object,
            'supplier': current_supplier,
        })

        return kwargs

    def form_valid(self, form):

        supplier = form['supplier'].save()
        dispatch_note = form['dispatch_note'].save(commit=False)

        dispatch_note.supplier = supplier
        dispatch_note.company = Company.objects.last()
        dispatch_note.updated_by = self.request.user

        if dispatch_note.quantity == 0:
            dispatch_note.quantity = None
        if dispatch_note.total_mass == 0:
            dispatch_note.total_mass = None
        if dispatch_note.mass == 0:
            dispatch_note.mass = None

        if dispatch_note.meat_type.pk != 1:
            dispatch_note.passports = None
            dispatch_note.certificate_id = None
            dispatch_note.certificate_number = None

        dispatch_note.save()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "dispatchNoteListChanged": None,
                    "showMessage": f"{dispatch_note.doc_number} updated."
                })
            }
        )


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def remove_dispatch_note(request, pk):
    dispatch_note = get_object_or_404(DispatchNote, pk=pk)
    dispatch_note.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "dispatchNoteListChanged": None,
                "showMessage": f"{dispatch_note.doc_number} deleted."
            })
        })


@user_passes_test(lambda u: u.is_superuser)
def company_list(request):
    template = 'list_companies.html'
    return render(request, template)


@user_passes_test(lambda u: u.is_superuser)
def company_table(request):
    object_type = Company
    template = 'table_companies.html'
    url = 'table_company'
    return elements_list(request, object_type, template, url)


@user_passes_test(lambda u: u.is_superuser)
def company_create(request):
    form_type = CompanyForm
    return element_create(request, form_type)


@user_passes_test(lambda u: u.is_superuser)
def company_update(request, pk):
    object_type = Company
    form_type = CompanyForm
    return element_update(request, pk, object_type, form_type)


@user_passes_test(lambda u: u.is_superuser)
def company_delete(request, pk):
    object_type = Company
    url = 'delete_company'
    return element_delete(request, pk, object_type, url)


@require_GET
@login_required
def print_pdf(request, pk):
    note = get_object_or_404(DispatchNote, pk=pk)
    supplier = get_object_or_404(Supplier, pk=note.supplier_id)
    company = get_object_or_404(Company, pk=note.company_id)

    doc_data = {'doc_number': str(note.doc_number), 'doc_date': str(note.doc_date)}

    if supplier.id_supplier == '00000':
        supplier_data = {'supplier_name': "", 'id_supplier': "", 'address': ""}
    else:
        supplier_data = {'supplier_name': str(supplier.name), 'id_supplier': str(supplier.id_supplier),
                         'address': str(supplier.address)}

    company_data = {'company_name': str(company.name), 'id_company': str(company.id_company),
                    'address': str(company.address)}

    quantity = check_null_value(note.quantity)
    total_mass = check_null_value(note.total_mass)
    mass = check_null_value(note.mass)

    product_data = {f'product_name': str(note.meat_type), 'quantity': quantity,
                    'total_mass': total_mass, 'mass': mass}

    list_data = None

    if note.meat_type_id == 1:
        list_data = {f'passports': str(note.passports), 'certificate_id': str(note.certificate_id),
                     'certificate_number': str(note.certificate_number)}

    return generate_accept_form(doc_data, supplier_data, company_data, product_data, list_data)


@require_GET
@login_required
def print_small_pdf(request, pk):
    note = get_object_or_404(DispatchNote, pk=pk)
    supplier = get_object_or_404(Supplier, pk=note.supplier_id)
    company = get_object_or_404(Company, pk=note.company_id)

    doc_data = {'doc_number': str(note.doc_number), 'doc_date': str(note.doc_date)}

    if supplier.id_supplier == '00000':
        supplier_data = {'supplier_name': "", 'id_supplier': "", 'address': ""}
    else:
        supplier_data = {'supplier_name': str(supplier.name), 'id_supplier': str(supplier.id_supplier),
                         'address': str(supplier.address)}

    company_data = {'company_name': str(company.name), 'id_company': str(company.id_company),
                    'address': str(company.address)}

    quantity = check_null_value(note.quantity)
    total_mass = check_null_value(note.total_mass)
    mass = check_null_value(note.mass)

    product_data = {f'product_name': str(note.meat_type), 'quantity': quantity,
                    'total_mass': total_mass, 'mass': mass}

    list_data = None

    if note.meat_type_id == 1:
        list_data = {f'passports': str(note.passports), 'certificate_id': str(note.certificate_id),
                     'certificate_number': str(note.certificate_number)}

    return generate_accept_form_small(doc_data, supplier_data, company_data, product_data, list_data)


# import
"""
@user_passes_test(lambda u: u.is_superuser)
def import_data(request):
    context = import_docs(request)
    return render(request, 'test.html', context)


@user_passes_test(lambda u: u.is_superuser)
def import_data_s(request):
    context = import_supplier(request)
    return render(request, 'test.html', context)


@user_passes_test(lambda u: u.is_superuser)
def import_data_n(request):
    context = import_notes(request)
    return render(request, 'test.html', context)

"""
