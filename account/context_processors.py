from account.views import checkSession, get_contacts, posses_subscription

def render_context(request):
    return {'sessionActive':checkSession(request.user), 'contacts':get_contacts(request), 'has_subscription':posses_subscription(request.user)}