from django.conf.urls import url, include
from . import views


more = [
	url(r'^(?P<category_slug>[\w-]+)', views.gallery_view_with_category, name='shop-gallery-view-category')

]

urlpatterns = [
	url(r'^gallery$', views.gallery_view, name='shop-gallery-view'),
    url(r'^gallery/', include(more)),
    url(r'^(?P<item_category>[\w-]+)/(?P<item_slug>[\w-]+)', views.item_detail_view, name='shop-item-detail-view'),
]


