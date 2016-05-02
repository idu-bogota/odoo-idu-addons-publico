import erppeek

class Connection():
    def __init__(self, options):
        self.connection = None
        self.options = options
        
    def get_connection(self):
        server = self.options.host_openERP +':' + self.options.port_openERP
        database = self.options.db_name
        user = self.options.db_user
        password = self.options.db_password
        if self.connection == None:
            self.connection = erppeek.Client(server, database, user, password)
        return self.connection
    