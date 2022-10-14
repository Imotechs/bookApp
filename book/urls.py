from django.urls import path
from .views import (
                    home,login,register,
                    UserProfile,AddBook,
                    EditProfile,AdminManageView,search,
                    bookcheckout,ADminManageCkeckedBooksView,
                    AdminEditBooksView,
                    )
urlpatterns = [
    path('',home, name = 'home'),
    path('accounts/login/',login, name = 'login'),
    path('account/',register, name = 'register'),
    path('profile/me/',UserProfile.as_view(),name = 'profile'),
    path('add/book/',AddBook.as_view(), name = 'add_book'),
    path('edit/profile/<int:pk>/',EditProfile.as_view(),name = 'edit_profile'),
    path('store/manager/',AdminManageView.as_view(),name = 'Admin'),
    path('search/books/',search,name = 'search'),
    path('book/checkout/<int:id>/',bookcheckout,name = 'checkout'),
    path('all/checke/books/',ADminManageCkeckedBooksView.as_view(), name = 'yet_books'),
    path('eddit/book/<int:pk>/',AdminEditBooksView.as_view(), name = 'edit')

]
