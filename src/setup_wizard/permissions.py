from rest_framework import permissions
from django.db import connection

class ApplicationNotInstalled(permissions.BasePermission):
    """
    Global permission to make sure that the user requesting a given action is actually a domain administrator or a staff member
    """

    def has_permission(self, request, view):
        cursor = connection.cursor()
        table_names = connection.introspection.get_table_list(cursor)
        if len(table_names) == 0:
            return True
        else:
            return False