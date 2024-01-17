from django.urls import path
from .import views
urlpatterns = [
   path('signup/',views.register,name='signup'),
   # path('login/',views.user_login,name='login'),
   path('login/',views.UserLoginView.as_view(),name='login'),
   # path('logout/',views.user_logout,name='logout'),
   path('logout/',views.user_logout,name='logout'),
   path('organize_event/',views.organize_event,name='organize_event'),
   path('profile/edit',views.edit_profile,name='edit_profile'),
   path('profile/',views.profile,name='profile'),
   # path('profile/edit/<int:id>',views.UpdateProfileView.as_view(),name='edit_profile'),
#    path('profile/edit/pass_change',views.pass_change,name='pass_change'),
   path('active/<uid64>/<token>',views.activate,name='activate'),
]