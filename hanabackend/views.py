from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.core.paginator import InvalidPage, Paginator
from django.template.response import TemplateResponse
from django.conf import settings
from django.http import Http404
import random


from . import models


def get_paginator_items(items, paginate_by, page_number):
    if not page_number:
        page_number = 1
    paginator = Paginator(items, paginate_by)
    try:
        page_number = int(page_number)
    except ValueError:
        raise Http404("Page can not be converted to an int.")
    try:
        items = paginator.get_page(page_number)
    except InvalidPage as err:
        raise Http404(
            "Invalid page (%(page_number)s): %(message)s"
            % {"page_number": page_number, "message": str(err)}
        )
    return items



def Index(request):
    total = 10
    categories_list = models.Category.objects.all()
    products_list = models.Product.objects.all().prefetch_related(
        "category",
        "collections",
        "images",
        ).order_by("ordering")
    products_list = list( products_list )

    products_ordered = []
    for p in products_list:
        if p.ordering != "Null":
            products_ordered.append(p)
        else:
            break
    products_list = list(set(products_list) - set(products_ordered))
    products_list = random.sample( products_list, total-len(products_ordered) if len(products_list)>(total-len(products_ordered)) else len(products_list)  )
    products_list = products_ordered + products_list
    ctx={
        "categories_list":categories_list,
        "products_list":products_list,
                }
    return TemplateResponse( request, "index.html", ctx )


def category_index(request, slug, category_id):
    categories = models.Category.objects.all()
    category = get_object_or_404(categories, id=category_id)
    products = models.Product.objects.all().filter(category=category).prefetch_related(         "category",
        "collections",
        "images" ).order_by("ordering")
    products_list = list( products )

    products_ordered = []
    for p in products_list:
        if p.ordering != "Null":
            products_ordered.append(p)
        else:
            break
    products = list(set(products_list) - set(products_ordered))
    products = products_ordered + products
    products_paginated = get_paginator_items(
        products, settings.PAGINATE_BY, request.GET.get("page")
    )
    ctx={
        "categories":categories,
        "category": category,
        "products_paginated": products_paginated,
        "has_previous":products_paginated.has_previous(),
        "has_next":products_paginated.has_next(),
                }
    if products_paginated.has_previous():
        ctx.update({"previous_page_number":products_paginated.previous_page_number()})
    if products_paginated.has_next():
        ctx.update({"next_page_number":products_paginated.next_page_number()})

    return TemplateResponse(request, "category_product_list.html", ctx)


def product_details(request, product_id, form=None):
    products = models.Product.objects.all().prefetch_related(
        "category",
        "collections",
        "images",
        )
    product = get_object_or_404( products, id=product_id )

    product_images = list( product.images.all() )
    ctx = {
        "product": product,
        "product_images": product_images,
        }
    return TemplateResponse( request, "product_details.html", ctx )

