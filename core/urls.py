from django import views
from django.urls import path, include
from core.views import add_to_cart, ajax_add_review, ajax_contact_form, cart_view, category_list_view, category_product_list__view, checkout_view, customer_dashboard, delete_item_from_cart, filter_product, index, make_address_default, order_detail, order_confirmation_view, product_detail_view, product_list_view, search_view, tag_list, update_cart, vendor_detail_view, vendor_list_view, contact, about_us, purchase_guide, privacy_policy, terms_of_service

app_name = "core"

urlpatterns = [

    # Homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),

    # Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list__view, name="category-product-list"),

    # Vendor
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),

    # Tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    # Add Review
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),

    # Search
    path("search/", search_view, name="search"),
    

    # Filter product URL
    path("filter-products/", filter_product, name="filter-product"),

    # Add to cart URL
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    # Cart Page URL
    path("cart/", cart_view, name="cart"),

    # Delete ITem from Cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    # Update  Cart
    path("update-cart/", update_cart, name="update-cart"),

      # Checkout  URL
    path("checkout/", checkout_view, name="checkout"),

    
    # Order Confirmation
    path('order-confirmation/<int:order_id>/', order_confirmation_view, name='order-confirmation'),

    
      
          

    # Dashboard URL
    path("dashboard/", customer_dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),

    # Making address defaulty
    path("make-default-address/", make_address_default, name="make-default-address"),

    

    path("contact/", contact, name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

    path("about_us/", about_us, name="about_us"),
    path("purchase_guide/", purchase_guide, name="purchase_guide"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("terms_of_service/", terms_of_service, name="terms_of_service"),
    
]