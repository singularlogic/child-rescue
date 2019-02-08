from organizations.models import Organization


class OrganizationUtils(object):

    @staticmethod
    def get_name(organization_id):
        return Organization.objects.get(id=organization_id).name
