from django.conf.urls import url, include
from . import views


more = [
	url(r'^(?P<category_slug>[\w-]+)', views.gallery_view_with_category, name='shop-gallery-view-category')

]

urlpatterns = [
	url(r'^gallery/$', views.gallery_view, name='shop-gallery-view'),
    url(r'^gallery/', include(more)),
    url(r'^toggle_cart/(?P<item_id>[0-9]+)/$', views.toggle_cart_view, name='shop-togglecart-view'),
    url(r'^confirm_item_prices/(?P<item_ids_string>[\w-]*)/$', views.confirm_selected_item_prices, name='shop-getitemprices'),    
    url(r'^detail/(?P<item_category>[\w-]+)/(?P<item_slug>[\w-]+)', views.item_detail_view, name='shop-item-detail-view'),
    url(r'^order/$', views.CartView.as_view(), name='shop-cart-view'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='shop-checkout-view'),
    url(r'^order/success/$', views.success_order_view, name='shop-order-success-view'),
    url(r'^order/paid/$',views.AlreadyPaid.as_view(), name='shop-already-paid'),

]


