from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Location
from .models import ArtPiece
from .models import ArtPiecePhoto
from django.shortcuts import get_object_or_404
from sorl.thumbnail import get_thumbnail
import logging
import json
import xlsxwriter
from xlsxwriter.workbook import Workbook
from django.conf import settings
from zipfile import ZipFile
import datetime
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

@login_required
def home(request):
    print settings.PROJECT_ROOT
    
    print "WOO"
    
    locations = Location.objects.all()
    return render_to_response('home.html',
                          {"locations": locations},
                          context_instance=RequestContext(request))

@login_required
def batch_import(request):
    locations = Location.objects.all()
    return render_to_response('batch_upload.html',
                              {"locations": locations},
                              context_instance=RequestContext(request))

@login_required
def art_list(request,id=None):
    if id == None:
        location = None
        pieces = ArtPiece.objects.all()
    else:
        location = Location.objects.get(pk = id)
        pieces = location.pieces()

    return render_to_response('art_list.html',
                              {"pieces": pieces, "location" : location},
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
@login_required
def edit_piece(request, id):
    locations = Location.objects.all()
    if id != '0' :
        piece = get_object_or_404(ArtPiece,pk=id)
    else:
        piece = ArtPiece()
    if request.method == 'POST' :
        piece.title = request.POST.get('title', '')
        piece.artist = request.POST.get('artist', '')
        piece.notes = request.POST.get('notes', '')
        piece.location = Location.objects.get(pk = request.POST.get('location', ''))
        piece.purchase_date = request.POST.get('purchase_date', '')
        piece.purchase_price = request.POST.get('purchase_price', '')
        piece.save()
        return HttpResponseRedirect('/pieces/%s/edit' % piece.pk)
    else:
        return render_to_response('edit_piece.html',
                                  {"piece" : piece, "locations": locations,},
                                  context_instance=RequestContext(request))
    
@login_required
@csrf_exempt
def delete_piece(request, piece_id):
    piece = get_object_or_404(ArtPiece,pk=piece_id)
    piece.delete()
    return HttpResponse("OK")


@login_required
@csrf_exempt
def delete_photo(request, piece_id, photo_id):
    image = ArtPiecePhoto.objects.get(pk=photo_id)
    image.delete()
    return HttpResponse("OK")

@login_required
def export_photos(request):
    
    clist = request.GET.get('include', '')
    joe = clist.split(',')
    
    in_memory = StringIO.StringIO()  
    zip = ZipFile(in_memory, "a")      
    
    for piece in ArtPiece.objects.filter(pk__in=joe):
        #create a folder for the zip
        slug = piece.slug()
        count = 0
        for photo in piece.photos() :
            #add photo to zip
            filename = slug + `count` + '.jpg'
            zip.write(settings.PROJECT_ROOT + photo.image.url,arcname=filename)
            count+=1
    
    zip.close()
            
    #return zip file
    response = HttpResponse(content_type="application/zip")  
    response["Content-Disposition"] = "attachment; filename=photos.zip"  

    in_memory.seek(0)      
    response.write(in_memory.read())

    return response  

@login_required
@csrf_exempt
def export(request):
    clist = request.GET.get('include', '')
    joe = clist.split(',')
    
    output = StringIO.StringIO()
    workbook = Workbook(output)    
    worksheet = workbook.add_worksheet()
    
    row = 1
    
    header_format = workbook.add_format()
    header_format.set_bold()
    header_format.set_text_wrap()
    
    inner_format = workbook.add_format()
    inner_format.set_text_wrap()
    
    curr_format = workbook.add_format()
    curr_format.set_num_format('#,##0.00')
    
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    
    worksheet.set_column(0, 0, 5)
    worksheet.set_column(1, 2, 20)
    worksheet.set_column(3, 4, 10)
    worksheet.set_column(5, 5, 40)
    worksheet.set_column(6, 6, 60)
    
    worksheet.write(0,0,'ID',header_format)
    worksheet.write(0,1,'Title',header_format)
    worksheet.write(0,2,'Artist',header_format)
    worksheet.write(0,3,'Purchase Date',header_format)
    worksheet.write(0,4,'Purchase Price',header_format)
    worksheet.write(0,5,'Notes',header_format)
    worksheet.write(0,6,'Image',header_format)
    
    for piece in ArtPiece.objects.filter(pk__in=joe):
        worksheet.set_row(row, 100)
        
        worksheet.write(row,0, piece.pk,inner_format)
        worksheet.write(row,1,piece.title,inner_format)
        worksheet.write(row,2,piece.artist,inner_format)
        worksheet.write(row,3,piece.purchase_date,date_format)
        worksheet.write(row,4,piece.purchase_price, curr_format)
        worksheet.write(row,5,piece.notes,inner_format)
        
        url = settings.PROJECT_ROOT + piece.photo().url
        thumb = get_thumbnail(url, '100x100', crop='center', quality=99)
        worksheet.insert_image('G' + `row`, settings.PROJECT_ROOT + thumb.url)
        
        row = row + 1
    
    workbook.close()
    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=art-export.xlsx"
    
    return response   
    

@login_required
@csrf_exempt
def add_photo_to_piece(request, id):
    log = logging.getLogger(__name__)
    if request.method == 'POST':
        print 'POST'
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        print 'Got file: "'+str(filename)+'"'
    
        #writing file manually into model
        #because we don't need form of any type.
        image = ArtPiecePhoto()
        image.filename = ''
        image.image=file
        image.piece = ArtPiece.objects.get(pk=id)
        image.save()
        print 'File saving done'
    
        #getting url for photo deletion
        file_delete_url = '/delete/'
    
        #getting file url here
        file_url = '/'
    
        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url
    
        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size,
                       "id":image.pk,
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = json.dumps(result)
        return HttpResponse(response_data, content_type='application/json')
    else:
        return HttpResponse("", content_type='application/json')
    
@login_required
@csrf_exempt
def add_with_photo(request, id):
    log = logging.getLogger(__name__)
    if request.method == 'POST':
        print 'POST'
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        print 'Got file: "'+str(filename)+'"'

        #create new piece and save
        piece = ArtPiece()
        piece.title = ''
        piece.artist = ''
        piece.notes = ''
        piece.location = Location.objects.get(pk = id)
        piece.purchase_date = datetime.datetime.now()
        piece.purchase_price = 0
        piece.save()
        
        image = ArtPiecePhoto()
        image.filename = ''
        image.image=file
        image.piece = piece
        image.save()

        #getting url for photo deletion
        file_delete_url = '/delete/'

        #getting file url here
        file_url = '/'

        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size,
                       "id":image.pk,
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = json.dumps(result)
        return HttpResponse(response_data, content_type='application/json')
    else:
        return HttpResponse("", content_type='application/json')    