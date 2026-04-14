from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category


def index(request):
    featured_products = Product.objects.filter(is_featured=True)[:3]
    return render(request, 'core/index.html', {'featured_products': featured_products})


def products_view(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Top sales: featured products
    top_sales = Product.objects.filter(is_featured=True)[:4]
    # Spotlight: newest product
    new_product = Product.objects.order_by('-created_at').first()
    # Featured sidebar product: first featured with an image
    sidebar_product = Product.objects.filter(is_featured=True, image_url__isnull=False).exclude(image_url='').first()

    return render(request, 'core/products.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'query': query,
        'top_sales': top_sales,
        'new_product': new_product,
        'sidebar_product': sidebar_product,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'core/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def services_view(request):
    return render(request, 'core/services.html')


def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('contact')
    return render(request, 'core/contact.html')


@login_required
def profile_view(request):
    return render(request, 'core/profile.html')


# --- Cart Logic (Session based) ---

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * item_data['quantity']
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'subtotal': subtotal
        })
        
    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1}
        
    request.session['cart'] = cart
    messages.success(request, "Added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'products'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, "Removed from cart.")
        
    return redirect('cart')


def checkout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to checkout.")
        return redirect('login')
        
    if request.method == 'POST':
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully! We'll contact you soon.")
        return redirect('index')
        
    return render(request, 'core/checkout.html')


# --- Auth Views ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.POST.get('next') or 'index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username}!')
            return redirect('index')

    return render(request, 'core/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
