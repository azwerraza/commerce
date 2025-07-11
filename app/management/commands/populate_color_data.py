from django.core.management.base import BaseCommand
from django.core.files import File
import os
from app.models import (
    SkinTone, SkinUndertone, SkinTonePalette,
    ColorRecommendation, ColorAvoidance, ModelAvatar
)


class Command(BaseCommand):
    help = 'Populates the database with initial color visualizer data'

    def handle(self, *args, **options):
        # Create undertones
        warm, _ = SkinUndertone.objects.get_or_create(
            name="Warm",
            color_code="#FFD700",
            defaults={'description': 'Yellow, peachy, golden undertones'}
        )

        cool, _ = SkinUndertone.objects.get_or_create(
            name="Cool",
            color_code="#4169E1",
            defaults={'description': 'Pink, red, or bluish undertones'}
        )

        neutral, _ = SkinUndertone.objects.get_or_create(
            name="Neutral",
            color_code="#808080",
            defaults={'description': 'Balance of warm and cool undertones'}
        )

        # Create skin tones with palettes
        skin_tones_data = [
            {
                'name': 'Fair',
                'palettes': [
                    {'undertone': cool, 'color_code': '#FFF5EE'},
                    {'undertone': warm, 'color_code': '#F5DEB3'},
                    {'undertone': neutral, 'color_code': '#F5F5DC'},
                ]
            },
            {
                'name': 'Light',
                'palettes': [
                    {'undertone': cool, 'color_code': '#E6D5C3'},
                    {'undertone': warm, 'color_code': '#D2B48C'},
                    {'undertone': neutral, 'color_code': '#C8B8A8'},
                ]
            },
            {
                'name': 'Medium',
                'palettes': [
                    {'undertone': cool, 'color_code': '#C69C6D'},
                    {'undertone': warm, 'color_code': '#B87333'},
                    {'undertone': neutral, 'color_code': '#C19A6B'},
                ]
            },
            {
                'name': 'Olive',
                'palettes': [
                    {'undertone': cool, 'color_code': '#8B7355'},
                    {'undertone': warm, 'color_code': '#808000'},
                    {'undertone': neutral, 'color_code': '#6B8E23'},
                ]
            },
            {
                'name': 'Tan',
                'palettes': [
                    {'undertone': cool, 'color_code': '#D2B48C'},
                    {'undertone': warm, 'color_code': '#C68642'},
                    {'undertone': neutral, 'color_code': '#CD853F'},
                ]
            },
            {
                'name': 'Deep',
                'palettes': [
                    {'undertone': cool, 'color_code': '#5C4033'},
                    {'undertone': warm, 'color_code': '#654321'},
                    {'undertone': neutral, 'color_code': '#704214'},
                ]
            }
        ]

        for data in skin_tones_data:
            skin_tone, _ = SkinTone.objects.get_or_create(name=data['name'])
            for palette in data['palettes']:
                SkinTonePalette.objects.get_or_create(
                    skin_tone=skin_tone,
                    undertone=palette['undertone'],
                    defaults={'color_code': palette['color_code']}
                )

        # Create color recommendations
        warm_recommendations = [
            {'color_name': 'Mustard', 'recommended_color': '#FFDB58',
             'description': 'Earthy tones complement warm undertones'},
            {'color_name': 'Olive Green', 'recommended_color': '#6B8E23', 'description': 'Natural greens work well'},
            {'color_name': 'Terracotta', 'recommended_color': '#E2725B',
             'description': 'Warm earthy reds are flattering'},
            {'color_name': 'Golden Yellow', 'recommended_color': '#FFDF00',
             'description': 'Bright warm yellows pop beautifully'},
            {'color_name': 'Coral', 'recommended_color': '#FF7F50',
             'description': 'Peachy tones enhance warm complexions'}
        ]

        cool_recommendations = [
            {'color_name': 'Emerald', 'recommended_color': '#50C878',
             'description': 'Jewel tones enhance cool undertones'},
            {'color_name': 'Navy Blue', 'recommended_color': '#000080', 'description': 'Deep blues are flattering'},
            {'color_name': 'Royal Blue', 'recommended_color': '#4169E1',
             'description': 'Bright blues complement cool skin'},
            {'color_name': 'Ruby Red', 'recommended_color': '#E0115F', 'description': 'Cool reds make skin glow'},
            {'color_name': 'Lavender', 'recommended_color': '#E6E6FA',
             'description': 'Soft purples complement cool tones'}
        ]

        neutral_recommendations = [
            {'color_name': 'Dusty Rose', 'recommended_color': '#DCAE96',
             'description': 'Soft pinks work well with neutral tones'},
            {'color_name': 'Teal', 'recommended_color': '#008080', 'description': 'Balanced colors are ideal'},
            {'color_name': 'Muted Lavender', 'recommended_color': '#967BB6',
             'description': 'Soft purples flatter neutral skin'},
            {'color_name': 'Soft Grey', 'recommended_color': '#D3D3D3',
             'description': 'Neutral tones work with all greys'},
            {'color_name': 'Sage Green', 'recommended_color': '#9DC183',
             'description': 'Muted greens complement neutral skin'}
        ]

        for rec in warm_recommendations:
            ColorRecommendation.objects.get_or_create(undertone=warm, **rec)

        for rec in cool_recommendations:
            ColorRecommendation.objects.get_or_create(undertone=cool, **rec)

        for rec in neutral_recommendations:
            ColorRecommendation.objects.get_or_create(undertone=neutral, **rec)

        # Create color avoidances
        warm_avoidances = [
            {'color_name': 'Ice Blue', 'avoid_color': '#99FFFF', 'reason': 'Can make skin look sallow'},
            {'color_name': 'Pastel Pink', 'avoid_color': '#FFD1DC', 'reason': 'Can wash out warm tones'}
        ]

        cool_avoidances = [
            {'color_name': 'Orange', 'avoid_color': '#FFA500', 'reason': 'Can clash with cool undertones'},
            {'color_name': 'Gold', 'avoid_color': '#FFD700', 'reason': 'Can make skin look pale'}
        ]

        neutral_avoidances = [
            {'color_name': 'Neon', 'avoid_color': '#39FF14', 'reason': 'Too intense for neutral tones'},
            {'color_name': 'Pure White', 'avoid_color': '#FFFFFF', 'reason': 'Can be too stark'}
        ]

        for avoid in warm_avoidances:
            ColorAvoidance.objects.get_or_create(undertone=warm, **avoid)

        for avoid in cool_avoidances:
            ColorAvoidance.objects.get_or_create(undertone=cool, **avoid)

        for avoid in neutral_avoidances:
            ColorAvoidance.objects.get_or_create(undertone=neutral, **avoid)

        # Create sample avatars (you'll need to provide these images)
        avatar_data = [
            {'skin_tone': 'Fair', 'gender': 'neutral', 'image_path': 'app/static/sample_avatars/fair_neutral.png'},
            {'skin_tone': 'Fair', 'gender': 'female', 'image_path': 'app/static/sample_avatars/fair_female.jpg'},
            {'skin_tone': 'Fair', 'gender': 'male', 'image_path': 'app/static/sample_avatars/fair_male.png'},
            # Add more avatars for other skin tones
        ]

        for data in avatar_data:
            skin_tone = SkinTone.objects.get(name=data['skin_tone'])
            if not ModelAvatar.objects.filter(skin_tone=skin_tone, gender=data['gender']).exists():
                try:
                    with open(data['image_path'], 'rb') as f:
                        ModelAvatar.objects.create(
                            skin_tone=skin_tone,
                            gender=data['gender'],
                            image=File(f, name=os.path.basename(f.name))
                        )
                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(f"Avatar image not found: {data['image_path']}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated color visualizer data'))