from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from .models import Location
from django.shortcuts import get_object_or_404

@login_required
def home(request):
    locations = Location.objects.all()
    return render_to_response('home.html',
                          {"locations": locations},
                          context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST' :
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)      
    
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect('/accounts/login')
    else:
        return render(request, 'login.html')
    
@login_required
def edit_location(request, id):
    if id != '0' :
        location = get_object_or_404(Location,pk=id)
        print location
    else:
        location = Location()
    if request.method == 'POST' :
        location.title = request.POST.get('title', '')
        location.address = request.POST.get('address', '')
        location.save()
        return HttpResponseRedirect('/locations/%s/edit' % location.pk)
    else:
        return render_to_response('edit_location.html',
                              {"location" : location},
                              context_instance=RequestContext(request))