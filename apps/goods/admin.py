from django.contrib import admin
from goods.models import GoodsType, IndexGoodsBanner, GoodsSKU, Goods, IndexTypeGoodsBanner


# Create your tests here.

class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'detail']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10

class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ['type', 'goods','name','desc','price','unite','image','stock','sales','status']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10


class IndexTypeGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['type', 'sku', 'display_type', 'index']
    list_filter = ['sku']
    search_fields = ['sku']
    list_per_page = 10


admin.site.register(GoodsType)
admin.site.register(IndexGoodsBanner)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin)
