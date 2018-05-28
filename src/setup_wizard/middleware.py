from django.db import connection

class ApplicationInstalled:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        #try:
        cursor = connection.cursor()
        if not cursor:
            raise ApplicationNotInstalled("There is no valid database connection. Please check your settings to make sure that the provided credentials are correct")
        table_names = connection.introspection.get_table_list(cursor)
        if len(table_names) == 0:
            raise ApplicationNotInstalled("There are no tables in the database. Please run initial setup to initialize the database")
        #except:
            #raise Exception("There are no tables in the database. Please run initial setup to initialize the database")
        #    pass


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class ApplicationNotInstalled(Exception):
    pass