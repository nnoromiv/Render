from happy_again.apis.users.email_languages.en import en
from happy_again.apis.users.email_languages.it import it

class UsersUtils:
    
    _language_map = {
        'en': en,
        'it': it
    }
    
    _pdf_map = {
        'en': 'Info_Sheet_ENG.pdf',
        'it': 'Info_Sheet_ITA.pdf'
    }

    @staticmethod
    def select_lan(language):
        """Returns the language module based on the given language code."""
        return UsersUtils._language_map.get(language, en)  # Default to English

    @staticmethod
    def select_pdf(language):
        """Returns the PDF filename based on the given language code."""
        return UsersUtils._pdf_map.get(language, 'Info_Sheet_ENG.pdf')  # Default to English PDF          

    @staticmethod
    def is_user_valid(user, admins, no_vouchers):
        for admin in admins:
            if user['user_id'] == admin.id:
                return 0
        for i in no_vouchers:
            if user['user_id'] == i.id:
                return 0
        return 1