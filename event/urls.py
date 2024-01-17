from django.urls import path
from .import views
urlpatterns = [
   # path('add/',views.add_posts,name='add_posts'),
   path('add/',views.AddEventView.as_view(),name='add_events'),
   # path('edit/<int:id>',views.edit_posts,name='edit_posts'),
   path('edit/<int:id>',views.EditEventView.as_view(),name='edit_events'),
   # path('delete/<int:id>',views.delete_posts,name='delete_posts')
   path('delete/<int:id>',views.DeleteEventView.as_view(),name='delete_events'),
   path('detail_view/<int:id>', views.DetailEventView.as_view(), name='detail_event'),
   path('accept_event/<int:id>/', views.accept_event, name='accept_event'),
   path('attendee_list/<int:id>/', views.attendee_list, name='attendee_list'),
]