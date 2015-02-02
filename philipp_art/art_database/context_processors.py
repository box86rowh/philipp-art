from .models import Location

def base(request):
    locations = Location.objects.all()
    return {
        'locations': locations,
    }