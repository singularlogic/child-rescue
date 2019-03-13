from core.cases.models import DemographicData, MedicalData, SocialData, PhysicalData, ProfileData


class CaseUtils(object):

    @staticmethod
    def get_demographic_data(child_id, case_id):
        return DemographicData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_medical_data(child_id, case_id):
        return MedicalData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_social_data(child_id, case_id):
        return SocialData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_physical_data(child_id, case_id):
        return PhysicalData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_profile_data(child_id, case_id):
        return ProfileData.objects.get(child=child_id, case=case_id)
