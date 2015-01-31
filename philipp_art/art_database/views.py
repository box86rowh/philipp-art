from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect

@login_required
def home(request):
    return render_to_response('home.html',
                          [],
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