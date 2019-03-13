from core.cases.models import DemographicData, MedicalData, PsychologicalData, PhysicalData, PersonalData, SocialMediaData


class CaseUtils(object):

    @staticmethod
    def get_demographic_data(child_id, case_id):
        return DemographicData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_medical_data(child_id, case_id):
        return MedicalData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_psychological_data(child_id, case_id):
        return PsychologicalData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_physical_data(child_id, case_id):
        return PhysicalData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_personal_data(child_id, case_id):
        return PersonalData.objects.get(child=child_id, case=case_id)

    @staticmethod
    def get_social_media_data(child_id, case_id):
        return SocialMediaData.objects.get(child=child_id, case=case_id)
