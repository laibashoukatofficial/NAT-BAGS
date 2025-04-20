
from django.http import JsonResponse

from django.shortcuts import redirect, render, get_object_or_404
from requests import session
from taggit.models import Tag
from core.models import Product, Category, Vendor, CartOrder, CartOrderProducts, ProductImages, ProductReview, Address
from userauths.models import ContactUs, Profile
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .forms import CheckoutForm
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.decorators import login_required

import calendar
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth
from django.core import serializers

def index(request):
    # bannanas = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True).order_by("-id")

    context = {
        "products":products
    }

    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tags = Tag.objects.all().order_by("-id")[:6]

    context = {
        "products":products,
        "tags":tags,
    }

    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories":categories
    }
    return render(request, 'core/category-list.html', context)


def category_product_list__view(request, cid):

    category = Category.objects.get(cid=cid) # food, Cosmetics
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "core/category-product-list.html", context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, "core/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published").order_by("-id")

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "core/vendor-detail.html", context)


def product_detail_view(request, pid):
    try:
        product = Product.objects.get(pid=pid)
    except Product.DoesNotExist:
        # Handle case where product with pid does not exist
        return render(request, "core/product-not-found.html")

    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product Review form
    review_form = ProductReviewForm()

    address = None
    make_review = True

    if request.user.is_authenticated:
        try:
            address = Address.objects.get(status=True, user=request.user)
            user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

            if user_review_count > 0:
                make_review = False
        except Address.DoesNotExist:
            # Handle case where the user does not have an address
            address = None  # or handle accordingly based on your requirements

    p_image = product.p_images.all()

    context = {
        "p": product,
        "address": address,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
    }

    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):

    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag
    }

    return render(request, "core/tag.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user 

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
    {
        'bool': True,
        'context': context,
        'average_reviews': average_reviews
    }
    )


def search_view(request):
    query = request.GET.get("q")
    products = Product.objects.none()
    categories = Category.objects.none()

    if query:
        # Search by product title
        products_by_title = Product.objects.filter(title__icontains=query).order_by("-date")
        
        # Search by category title
        categories = Category.objects.filter(title__icontains=query)
        products_by_category = Product.objects.filter(category__in=categories).order_by("-date")

        # Combine querysets
        products = products_by_title | products_by_category

    context = {
        "products": products.distinct(),  # Use distinct() to avoid duplicate entries
        "query": query,
    }
    return render(request, "core/search.html", context)



def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")


    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)


    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct() 
    else:
        products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct() 
    else:
        products = Product.objects.filter(product_status="published").order_by("-id").distinct()    
    
       

    
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:

            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})



def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact_phone = form.cleaned_data['contact_phone']
            shipping_address = form.cleaned_data['shipping_address']
            billing_address = form.cleaned_data['billing_address']
            payment_method = form.cleaned_data['payment_method']

            if 'cart_data_obj' in request.session:
                cart_data = request.session['cart_data_obj']
                total_amount = sum(int(item['qty']) * float(item['price']) for p_id, item in cart_data.items())

                # Create Order Object
                order = CartOrder.objects.create(
                    user=request.user,
                    price=total_amount,
                    payment_method=payment_method,
                    shipping_address=shipping_address,
                    billing_address=billing_address,
                )

                cart_order_products = []
                for p_id, item in cart_data.items():
                    product_total = int(item['qty']) * float(item['price'])
                    cart_order_product = CartOrderProducts(
                        order=order,
                        invoice_no="INVOICE_NO-" + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=item['qty'],
                        price=item['price'],
                        total=product_total
                    )
                    cart_order_products.append(cart_order_product)

                CartOrderProducts.objects.bulk_create(cart_order_products)

                # Clear the cart data from session after order placement
                del request.session['cart_data_obj']

                # Send order confirmation email
                send_order_confirmation_email(request.user.email, order)

                # Display payment completed message
                messages.success(request, "Payment completed successfully. Your order has been placed.")

                return redirect('core:order-confirmation', order_id=order.id)
            else:
                messages.warning(request, "Your cart is empty.")
    else:
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            total_amount = sum(int(item['qty']) * float(item['price']) for p_id, item in cart_data.items())
            form = CheckoutForm()
        else:
            messages.warning(request, "Your cart is empty.")
            return redirect('core:cart')

    context = {
        'form': form,
        'cart_data': cart_data,
        'total_amount': total_amount
    }
    return render(request, "core/checkout.html", context)

@login_required
def order_confirmation_view(request, order_id):
    order = CartOrder.objects.get(id=order_id, user=request.user)
    return render(request, 'core/order_confirmation.html', {'order': order})



def send_order_confirmation_email(email, order):
    subject = 'Order Confirmation '
    html_message = render_to_string('core/order_confirmation_email.html', {'order': order})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'your_email@example.com', [email], html_message=html_message)
                






@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)


    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("core:dashboard")
    else:
        print("Error")
    
    user_profile = Profile.objects.get(user=request.user)
    print("user profile is: #########################",  user_profile)

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=order)

    
    context = {
        "order_items": order_items,
    }
    return render(request, 'core/order-detail.html', context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


        
# Other Pages 
def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data":data})


def about_us(request):
    return render(request, "core/about_us.html")


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def terms_of_service(request):
    return render(request, "core/terms_of_service.html")


