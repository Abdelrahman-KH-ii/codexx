def active_language(request):
    lang = request.COOKIES.get('nexus_lang', 'ar')
    return {
        'active_lang': lang,
        'is_ar': lang == 'ar',
        'is_en': lang == 'en',
    }
