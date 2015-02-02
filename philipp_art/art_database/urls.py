from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'art_database.views.home', name='home'),
                       url(r'^locations/(?P<id>\w+)/edit', 'art_database.views.edit_location', name='edit_location'),
                       url(r'^pieces/(?P<id>\w+)/edit', 'art_database.views.edit_piece', name='edit_piece'),
                       url(r'^pieces/add-with-photo/(?P<id>\w+)', 'art_database.views.add_with_photo', name='add_with_photo'),
                       url(r'^pieces/(?P<piece_id>\w+)/delete', 'art_database.views.delete_piece', name='delete_piece'),
                       url(r'^pieces/(?P<id>\w+)/add-photo', 'art_database.views.add_photo_to_piece', name='add_photo_to_piece'),
                       url(r'^pieces/(?P<piece_id>\w+)/photo/(?P<photo_id>\w+)/delete', 'art_database.views.delete_photo', name='delete_photo'),
                       url(r'^art-list/location/(?P<id>\w+)', 'art_database.views.art_list', name='art_list'),
                       url(r'^art-list/export-photos', 'art_database.views.export_photos', name='export_photos'),
                       url(r'^art-list/export', 'art_database.views.export', name='export'),
                       url(r'^art-list', 'art_database.views.art_list', name='art_list_1'),
                       url(r'^batch-import', 'art_database.views.batch_import', name='batch_import'),
                       url(r'^accounts/login/', 'art_database.views.login', name='login'),
)
