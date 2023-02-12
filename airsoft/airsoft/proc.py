from airsoft_teams.forms import TeamPostForm

def context(request):
    c = {}
    c['TeamPostForm'] = TeamPostForm()

    return c