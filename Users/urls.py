from django.urls import path
from .views import signup,signUpBtnClick,save_food_data,user_list,save_activity_data,view_user_data,view_date_data,delete_user

urlpatterns = [
    path('', signup, name='signup'),
    path('userList/', user_list, name='user_list'),
    path('signUpBtnClick/', signUpBtnClick, name='signUpBtnClick'),
    path('save_food_data/', save_food_data, name='save_food_data'),
    path('save_activity_data/', save_activity_data, name='save_activity_data'),
    path('userList/view_user_data/<int:id>', view_user_data, name='view_user_data'),
    path('view_date_data/', view_date_data, name='view_date_data'),
    path('delete-user/', delete_user, name='delete_user'),
    ]