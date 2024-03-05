from .stats import Stats


class Mappings:
    def __init__(self, default_user: int = 1):
        self.suites = {}
        self.users = {}
        self.types = {}
        self.priorities = {}
        self.result_statuses = {}
        self.case_statuses = {}
        self.custom_fields = {}
        self.configurations = {}
        self.projects = []
        self.attachments_map = {}
        self.shared_steps = {}

        # A map of TestIT project ids to Qase project codes
        self.project_map = {}
        # Step fields. Used to determine if a field is a step field or not during import
        self.step_fields = []

        self.refs_id = None
        
        self.qase_fields_type = {
            "number": 0,
            "string": 1,
            "text": 2,
            "selectbox": 3,
            "checkbox": 4,
            "radio": 5,
            "multiselect": 6,
            "url": 7,
            "user": 8,
            "datetime": 9,
        }

        self.default_user = default_user
        self.stats = Stats()


    def get_user_id(self, id: int) -> int:
        if (id in self.users):
            return self.users[id]
        return self.default_user  