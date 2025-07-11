from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import SkinTone, Color, SkinTonePalette
from app.utils import extract_undertone, UNDERTONE_COLOR_MAP

@receiver(post_save, sender=SkinTone)
def auto_generate_palettes(sender, instance, created, **kwargs):
    if not created:
        return

    undertone = extract_undertone(instance.name)
    if not undertone:
        return

    color_names = UNDERTONE_COLOR_MAP.get(undertone, [])
    for color in Color.objects.filter(name__in=color_names):
        SkinTonePalette.objects.get_or_create(skin_tone=instance, color_hex=color.hex_code)
