from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from assistant_app import views
urlpatterns = [path("admin/", admin.site.urls), path("", views.home, name="home"), path("register/", views.register_view, name="register"), path("login/", views.login_view, name="login"), path("logout/", views.logout_view, name="logout"), path("chat/", views.chat_view, name="chat"), path("chat/new/", views.new_chat_view, name="new_chat"), path("chat/<int:session_id>/", views.chat_view, name="chat_session"), path("documents/", views.documents_view, name="documents"), path("documents/<int:document_id>/delete/", views.delete_document_view, name="delete_document")]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
