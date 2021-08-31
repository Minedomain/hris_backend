from rest_framework.permissions import BasePermission

class IsHRDepartment(BasePermission):
    message = 'Only the HR has permission.'

    def has_permission(self, request, view):
      try:
        if request.user.department_role == 'HR':
          return True
        else:
          return False
      except:
        return False
