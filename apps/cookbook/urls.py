from django.urls import path, include
from . import views

urlpatterns = [
    path('/<int:user_id>',views.userpage),
    path('/<int:user_id>/family',views.gotofamilypage),
    path('/<int:user_id>/joinfamily',views.joinfamily),
    path('/<int:user_id>/<int:family_id>',views.familypage),
    path('/<int:user_id>/newrecipecard',views.newrecipecard),
    path('/<int:user_id>/addrecipe',views.addrecipe),
    path('/<int:user_id>/deleterecipe',views.deleterecipe),
    path('/<int:user_id>/editrecipecard',views.editrecipecard),
    path('/<int:user_id>/editrecipe',views.editrecipe),
    path('/<int:recipe_id>/postcomment',views.postcomment),
    path('/<int:family_id>/leavefamily',views.leavefamily),
    path('/<int:family_id>/postmessage',views.postmessage),
    path('/<int:family_id>/deletemessage',views.deletemessage),
    # path('/<int:user_id>//gotofamily',views.gotofamily),
]