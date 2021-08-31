from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'employees'

router = DefaultRouter()

router.register('list', EmployeeViewset, basename='employee-details')
router.register('education', EmployeeEducationViewset, basename='employee-education')
router.register('job-history', EmployeeJobHistoryViewset, basename='employee-job-history')
router.register('exams-taken', EmployeeExamsTakenViewset, basename='employee-exams-taken')
router.register('seminars-taken', EmployeeSeminarsTakenViewset, basename='employee-seminars-taken')
router.register('skills', EmployeeSkillsViewset, basename='employee-skills')
router.register('family', EmployeeFamilyViewset, basename='employee-family')
router.register('sibling', EmployeeSiblingViewset, basename='employee-sibling')
router.register('married', EmployeeMarriedViewset, basename='employee-married')
router.register('children', EmployeeChildrenViewset, basename='employee-children')
router.register('med-history', EmployeeMedicalHistoryViewset, basename='employee-med-history')
router.register('reference', EmployeeReferenceViewset, basename='employee-reference')
router.register('org', EmployeeOrganizationViewset, basename='employee-org')
router.register('offense', EmployeeOffenseViewset, basename='employee-offense')
router.register('emergency', EmployeeEmergencyViewset, basename='employee-emergency')
router.register('documents', EmployeeDocumentsViewset, basename='employee-documents')
router.register('signature', EmployeeSignatureViewset, basename='employee-signature')

urlpatterns = [
    path('', include(router.urls)),
    path('register', EmployeeRegisterView.as_view(), name='employee-register'),
    path('login-hr', EmployeeHRLoginView.as_view(), name='employee-login-hr'),
    path('login', EmployeeLoginView.as_view(), name='employee-login'),
    path('is_authenticated', IsAuthenticatedView.as_view(), name='is_authenticated'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('logout', EmployeeLogoutView.as_view(), name='employee-logout'),

    # Retrieve by Employee ID
    path('job-history', EmployeeJobHistoryRetrieveView.as_view(), name='employee-job-history-retrieve'),
    path('exams-taken', EmployeeExamsTakenRetrieveView.as_view(), name='employee-exams-taken-retrieve'),
    path('seminars-taken', EmployeeSeminarsTakenRetrieveView.as_view(), name='employee-seminars-taken-retrieve'),
    path('sibling', EmployeeSiblingRetrieveView.as_view(), name='employee-sibling-retrieve'),
    path('children', EmployeeChildrenRetrieveView.as_view(), name='employee-children-retrieve'),
    path('reference', EmployeeReferenceRetrieveView.as_view(), name='employee-reference-retrieve'),
    path('org', EmployeeOrganizationRetrieveView.as_view(), name='employee-org-retrieve'),
    path('documents', EmployeeDocumentsRetrieveView.as_view(), name='employee-documents-retrieve'),
]
