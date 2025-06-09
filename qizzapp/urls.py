from django.urls import path
from qizzapp import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('section/',views.section,name='section'),
    path('quiz/',views.quiz,name='quiz'),
    path('section/<int:section_id>/quiz/<int:question_number>/', views.quiz_navigation_view, name='quiz_nav'),
    path('section/<int:section_id>/result/', views.quiz_result, name='quiz_result'),
    path('admin_log/',views.admin_log,name='admin_log'),
    path('table/',views.table,name='table'),

    
]
