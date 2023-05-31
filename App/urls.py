from . import views 
from django.urls import path


urlpatterns = [
   path('',views.index,name='home'),
    path('login',views.loginn,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    # path('view/<int:product_id>/', views.view_product, name='view'),
    path('view/<int:product_id>/',views.view_product, name='view'),
    # path('product/<int:product_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
    # path('cart/', views.show_cart, name='showcart'),
    # path('cart-to-cart/',views.add_to_cart, name='add_to_cart'),
    
    # path('cart/delete/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    # path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),


    # path("checkout/", views.show_cart,name="checkout"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
     path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),



    path('create/', views.create_product, name='create_product'),
    # path('list/', views.product_list, name='product_list'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
   
]
