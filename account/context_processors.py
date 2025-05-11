from account.views import checkSession, get_contacts

def render_context(request):
    return {'sessionActive':checkSession(request.user), 'contacts':get_contacts(request)}