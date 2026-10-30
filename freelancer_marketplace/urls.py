from django.contrib import admin
from django.urls import path, include
from marketplace import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("", include("accounts.urls")),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("profile/", views.create_profile, name="profile"),

    path(
        "project/create/",
        views.create_project,
        name="create_project",
    ),

    path(
        "projects/",
        views.project_list,
        name="project_list",
    ),

    path(
        "projects/<int:pk>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
       "projects/<int:project_id>/bid/",
        views.apply_bid,
        name="apply_bid",
    ),

        path(
       "project/<int:project_id>/close/",
       views.close_project,
       name="close_project",
    ),

    path(
       "project/<int:project_id>/open/",
       views.open_project,
       name="open_project",
    ),

    path(
        "my-projects/",
        views.my_projects,
        name="my_projects",
    ),

    path(
       "project/<int:project_id>/edit/",
       views.edit_project,
       name="edit_project",
    ),

    path(
       "project/<int:project_id>/delete/",
       views.delete_project,
       name="delete_project",
    ),

    path(
       "my-bids/",
       views.my_bids,
       name="my_bids",
    ),

    path(
       "bid/<int:bid_id>/accept/",
       views.accept_bid,
       name="accept_bid",
    ),

    path(
       "bid/<int:bid_id>/reject/",
       views.reject_bid,
       name="reject_bid",
    ),

    path(
       "admin-dashboard/",
       views.admin_dashboard,
       name="admin_dashboard",
    ),



    path(
       "my-profile/",
       views.freelancer_profile,
       name="freelancer_profile",
    ),

    path(
       "profile/edit/",
       views.edit_profile,
       name="edit_profile",
    ),

    path(
       "notifications/",
       views.notifications,
       name="notifications",
    ),

    path(
       "project/<int:project_id>/complete/",
       views.complete_project,
       name="complete_project",
    ),

    path(
       "freelancers/",
       views.freelancer_list,
       name="freelancer_list",
    ),

    path(
       "freelancer/<int:freelancer_id>/",
       views.freelancer_profile_detail,
       name="freelancer_profile_detail",
    ),

    path(
       "project/<int:project_id>/review/",
       views.leave_review,
       name="leave_review",
    ),

    path(
       "completed-projects/",
       views.completed_projects,
       name="completed_projects",
    ),

    path(
       "settings/",
       views.account_settings,
       name="account_settings",
    ),

    path(
       "password-change/",
       auth_views.PasswordChangeView.as_view(
           template_name="accounts/password_change.html"
       ),
       name="password_change",
    ),

    path(
       "messages/",
       views.inbox,
       name="messages",
    ),

    path(
       "messages/<int:user_id>/",
       views.chat,
       name="chat",
    ),

 


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )