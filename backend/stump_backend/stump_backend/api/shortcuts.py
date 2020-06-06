
def get_current_location(request):
    '''
    Returns the current lat / lon value for the user
    '''
    if request is None:
        return (None, None)

    if request.user is not None and request.user.is_authenticated:
        return (request.user.latitude, request.user.longitude)

    if request.session is not None and 'my_location' in request.session:
        my_location = request.session['my_location']
        if 'latitude' in my_location and 'longitude' in my_location:
            return (my_location['latitude'], my_location['longitude'])

    # Fall thru
    return (None, None)
