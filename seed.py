import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hardware.settings')
django.setup()

from core.models import Category, Product

def seed_data():
    # Categories
    power_tools, _ = Category.objects.get_or_create(name='Power Tools', slug='power-tools', icon='⚡')
    hand_tools, _ = Category.objects.get_or_create(name='Hand Tools', slug='hand-tools', icon='🔨')
    safety_gear, _ = Category.objects.get_or_create(name='Safety Gear', slug='safety-gear', icon='🛡️')
    plumbing, _ = Category.objects.get_or_create(name='Plumbing', slug='plumbing', icon='🚰')

    # Products
    products_data = [
        {
            'category': power_tools,
            'name': 'Power Drill Pro X',
            'description': 'Industrial grade brushless motor drill with 20V battery and rapid charger.',
            'price': 199.99,
            'stock': 15,
            'is_featured': True
        },
        {
            'category': hand_tools,
            'name': 'Premium Wrench Set',
            'description': '12-piece chrome vanadium steel wrench set with polished finish.',
            'price': 49.99,
            'stock': 25,
            'is_featured': True
        },
        {
            'category': safety_gear,
            'name': 'Industrial Helmet',
            'description': 'High-impact ABS plastic helmet with adjustable suspension and chin strap.',
            'price': 29.99,
            'stock': 50,
            'is_featured': False
        },
        {
            'category': power_tools,
            'name': 'Circular Saw 1500W',
            'description': 'Powerful 1500W circular saw with laser guide and dust extraction.',
            'price': 149.99,
            'stock': 8,
            'is_featured': False
        },
        {
            'category': plumbing,
            'name': 'Heavy Duty Pipe Wrench',
            'description': '18-inch cast iron pipe wrench with induction hardened jaws.',
            'price': 39.99,
            'stock': 12,
            'is_featured': True
        }
    ]

    for p_data in products_data:
        Product.objects.get_or_create(
            name=p_data['name'],
            defaults=p_data
        )
    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
