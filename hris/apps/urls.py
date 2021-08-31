from django.urls import path, include

urlpatterns = [
    path("users/", include("hris.users.api.urls")),
    path("employees/", include("hris.apps.employees.urls")),
    path("jobs/", include("hris.apps.jobs.urls")),
    path("departments/", include("hris.apps.departments.urls")),
    path("attendance/", include("hris.apps.attendance.urls")),
    path("leave/", include("hris.apps.leaves.urls")),
    path("engagements/", include("hris.apps.engagements.urls")),
    path("surveys/", include("hris.apps.surveys.urls")),
    path("companies/", include("hris.apps.companies.urls")),
]