# authentication_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile, Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

def home(request):
    
    users = UserProfile.objects.all()[::-1][:3]
    
    for user in users:
        user_profile = UserProfile.objects.get(user=user.user)
        user.extra_photos_count = user_profile.extra_photos.count()
        user.location_info = user_profile.location_info
        user.location_2 = user_profile.location_2
    return render(request, 'rent.html', {'users': users})

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return HttpResponse("Passwords do not match. Please try again.")

        user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = UserProfile(user=user, mobile_number=mobile_number)
        user_profile.save()

        login(request, user)
        return redirect('land_lord')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('land_lord')

    return render(request, 'login.html')


@login_required
def land_lord(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    extra_photos = user_profile.extra_photos.all()
    extra_photos_count = extra_photos.count()
    print(extra_photos)

    if request.method == 'POST':
        # Update bio if provided
        bio = request.POST.get('bio', '')
        user_profile.bio = bio

        price = request.POST.get('price', '')
        user_profile.price = price

        bedroom = request.POST.get('bedroom', '')
        user_profile.bedroom = bedroom

        hallroom = request.POST.get('hallroom', '')
        user_profile.hallroom = hallroom

        kitchen = request.POST.get('kitchen', '')
        user_profile.kitchen = kitchen

        # location_info = request.POST.get('location_info', '')
        # user_profile.location_info = location_info
        
        # address= request.POST.get('address', '')
        city= request.POST.get('city', '')
        pin=request.POST.get('pin', '')
        state= request.POST.get('state', '') 
        # country =  request.POST.get('country', '')

# Concatenate the values into a single string
        location_2_value = f" {city}, {pin}, {state}"

        user_profile.location_2 = location_2_value

        profile_photo = request.FILES.get('profile_photos')
        if profile_photo:
            user_profile.profile_photo = profile_photo

        # Add extra photos if provided
        new_extra_photos = request.FILES.getlist('extra_photos')
        for photo in new_extra_photos:
            extra_image = Image.objects.create(image=photo)
            user_profile.extra_photos.add(extra_image)

        user_profile.save()
        return render(request, 'land_lord.html', {
            'user_profile': user_profile,
            'success': True
        })
        

    return render(request, 'land_lord.html', {'user_profile': user_profile, 'extra_photos': extra_photos})

def public_user_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    extra_photos = user_profile.extra_photos.all()

    return render(request, 'public_user_profile.html', {'user_profile': user_profile, 'extra_photos': extra_photos})

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        price_range = request.GET.get('price_range', '')

        filters = Q(location_info__icontains=query) | Q(location_2__icontains=query)

        if price_range:
            try:
                min_price, max_price = map(int, price_range.split('-'))
                filters &= Q(price__gte=min_price) & Q(price__lte=max_price)
            except ValueError:
                pass  # Invalid price format

        results = UserProfile.objects.filter(filters)

        return render(request, 'search.html', {
            'results': results,
            'query': query,
            'price_range': price_range
        })
    else:
        return render(request, 'search.html')

def contact(request):
    return render(request, 'contact.html')

