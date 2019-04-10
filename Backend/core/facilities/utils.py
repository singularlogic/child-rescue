
class FacilityUtils(object):

    @staticmethod
    def has_rights(role, list_of_roles):

        if role is not None and role in list_of_roles:
            return True
        else:
            return False
