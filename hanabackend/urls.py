from django.urls import path, include, re_path
from django.http import HttpResponse
from . import views

urlpatterns = [
    # re_path(r"^index/", core_views.index, name="index"),
    re_path(
        r"^category/(?P<slug>[a-z0-9-_]+?)-(?P<category_id>[0-9]+)/$",
        views.category_index,
        name="category"),

    re_path(r"^detail/(?P<product_id>[0-9]+)/$",
        views.product_details,
        name="productdetail"),
]
