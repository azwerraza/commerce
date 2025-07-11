from django.contrib import admin
from .models import Product, Contact_us, Order, ProductImage, Size, News, Comment, SkinTone, SkinTonePalette, LegalDocument, Wishlist, Color
from django.contrib import admin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "No Image"

    preview.allow_tags = True


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'price', 'display_sizes', 'Availability', 'date')
    list_filter = ('Availability', 'date', 'available_sizes')
    search_fields = ('name', 'description')
    filter_horizontal = ('available_sizes',)  # Adds a nice selector for sizes

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'image', 'price', 'Availability')  # 👈 Here!
        }),
        ('Product Details', {
            'fields': ('description', 'shirt_details', 'trouser_details',
                       'fabric', 'color', 'color_hex', 'weight')
        }),
        ('Sizes', {
            'fields': ('available_sizes',)
        }),
        ('Additional Information', {
            'fields': ('care_instructions', 'disclaimer'),
            'classes': ('collapse',)
        }),
    )

    def display_sizes(self, obj):
        return ", ".join([size.name for size in obj.available_sizes.all()])

    display_sizes.short_description = 'Available Sizes'


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'price', 'size', 'quantity', 'total', 'date')
    search_fields = ('user__username', 'product', 'size')
    list_filter = ('date', 'user')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "No Image"

    preview_image.allow_tags = True

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'likes')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    filter_horizontal = ('related_products',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'news', 'created_at')
    search_fields = ('name', 'content')
    list_filter = ('created_at',)

# skin
class SkinTonePaletteInline(admin.TabularInline):
    model = SkinTonePalette
    extra = 1  # number of blank forms

class SkinToneAdmin(admin.ModelAdmin):
    inlines = [SkinTonePaletteInline]

class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {"slug": ("title",)}


class SkinToneAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_hex')

admin.site.register(Color)
admin.site.register(SkinTone, SkinToneAdmin)
admin.site.register(SkinTonePalette)  # Optional: if you want separate access too


admin.site.register(Wishlist)
admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact_us, ContactUsAdmin)
admin.site.register(Order, OrderAdmin)
