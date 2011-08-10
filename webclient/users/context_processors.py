def auth(request):
    if (request.user):
        return {'user': request.user}
    else:
        return {}
