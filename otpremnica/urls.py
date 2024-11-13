from django.urls import path
from . import views


urlpatterns = [
    path('suppliers/', views.supplier_list, name='list_supplier'),
    path('suppliers/table/', views.supplier_table, name='table_supplier'),
    path('suppliers/new/', views.supplier_create, name='new_supplier'),
    path('suppliers/<int:pk>/update/', views.supplier_update, name='update_supplier'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='delete_supplier'),
    path('suppliers/search_supplier/', views.search_supplier, name='search_supplier'),

    path('set/meat_type/', views.meat_list, name='list_meat'),
    path('set/meat_type/table/', views.meat_table, name='table_meat'),
    path('set/meat_type/new/', views.meat_create, name='new_meat'),
    path('set/meat_type/<int:pk>/update/', views.meat_update, name='update_meat'),
    path('set/meat_type/<int:pk>/delete/', views.meat_delete, name='delete_meat'),

    path('set/company/', views.company_list, name='list_company'),
    path('set/company/table/', views.company_table, name='table_company'),
    path('set/company/new/', views.company_create, name='new_company'),
    path('set/company/<int:pk>/update/', views.company_update, name='update_company'),
    path('set/company/<int:pk>/delete/', views.company_delete, name='delete_company'),

    path('', views.index, name='home'),
    path('sid/', views.index_sid, name='sid_home'),
    path("disnotes/search/", views.list_search_view_ap, name="list_search_view_ap"),
    path("disnotes/search_sid/", views.list_search_view_sid, name="list_search_view_sid"),
    path('disnotes/add/', views.add_dispatch_note_ap, name='add_dispatch_note_ap'),
    path('disnotes/add_sid/', views.add_dispatch_note_sid, name='add_dispatch_note_sid'),
    path('disnotes/<int:pk>/edit/', views.EditDispatchNoteAP.as_view(), name='edit_dispatch_note_ap'),
    path('disnotes/<int:pk>/edit_sid/', views.EditDispatchNoteSid.as_view(), name='edit_dispatch_note_sid'),
    path('disnotes/<int:pk>/remove/', views.remove_dispatch_note, name='remove_dispatch_note'),
    path('disnotes/<int:pk>/print/', views.print_pdf, name='print_pdf'),
    path('disnotes/<int:pk>/print2/', views.print_small_pdf, name='print_small_pdf')

]
