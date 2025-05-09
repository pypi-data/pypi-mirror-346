"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: urls.py

brief:
This file defines routing for each plugin view.
"""
from django.urls import path
from . import views

# this must be named same as the plugin
app_name = 'module_swap'

urlpatterns = [
    path('step1/', views.Step1SelectView.as_view(), name='step1_select'),
    path('step2/', views.Step2BayView.as_view(), name='step2_bay'),
    path('link/', views.LinkModuleInventoryView.as_view(), name='link_module_inventory_create'),
    path('link/<int:link_id>/', views.LinkModuleInventoryView.as_view(),
        name='link_module_inventory_edit'),
    path('link/list/', views.LinkModuleInventoryListView.as_view(),
        name='link_module_inventory_list'),
    path('link/<int:pk>/delete/', views.DeleteModuleInventoryLinkView.as_view(),
        name='link_module_inventory_delete'),
]
