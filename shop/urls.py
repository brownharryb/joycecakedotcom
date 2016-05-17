from django.conf.urls import url, include
from . import views


more = [
	url(r'^(?P<category_slug>[\w-]+)', views.gallery_view_with_category, name='shop-gallery-view-category')

]

urlpatterns = [
	url(r'^gallery/$', views.gallery_view, name='shop-gallery-view'),
    url(r'^gallery/', include(more)),
    url(r'^add_to_cart/(?P<item_id>[0-9]+)/$', views.add_to_cart_view, name='shop-addtocart-view'),
    url(r'^remove_from_cart/(?P<item_id>[0-9]+)/$', views.remove_from_cart_view, name='shop-removefromcart-view'),
    url(r'^detail/(?P<item_category>[\w-]+)/(?P<item_slug>[\w-]+)', views.item_detail_view, name='shop-item-detail-view'),
    url(r'^cart/$', views.CartView.as_view(), name='shop-cart-view'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='shop-checkout-view'),

]


