###############################################################################
import mixpanel
import os
import uuid

###############################################################################
TOKEN = '6e7ecd86cf4fa3cf08ddaf8ab3de81d6'

###############################################################################
def people_set(properties={}):
    try:
        distinct_id = get_distinct_id()

        if distinct_id:
            mp = mixpanel.Mixpanel(TOKEN)
            mp.people_set(distinct_id, properties)
            Log.Info('[BitTorrent][Tracking] Sent people properties')
    except Exception as exception:
        Log.Error('[BitTorrent][Tracking] Unhandled exception: {0}'.format(exception))

###############################################################################
def track(event, properties={}):
    try:
        distinct_id = get_distinct_id()

        if distinct_id:
            properties['Server OS']       = str(Platform.OS)
            properties['Server CPU']      = str(Platform.CPU)
            properties['Client Product']  = str(Client.Product)
            properties['Client Platform'] = str(Client.Platform)
            properties['Channel Version'] = SharedCodeService.common.VERSION

            mp = mixpanel.Mixpanel(TOKEN)
            mp.track(distinct_id, event, properties)
            Log.Info('[BitTorrent][Tracking] Sent tracking event: {0}'.format(event))
    except Exception as exception:
        Log.Error('[BitTorrent][Tracking] Unhandled exception: {0}'.format(exception))

###############################################################################
def get_distinct_id():
    user_id_file_path = os.path.join(get_bundle_dir(), 'user_id.txt')
    if not os.path.isfile(user_id_file_path):
        user_id_file_fd = os.open(user_id_file_path, os.O_CREAT | os.O_RDWR)
        os.write(user_id_file_fd, uuid.uuid4().hex)
        os.close(user_id_file_fd)

    if os.path.isfile(user_id_file_path):
        user_id_file_fd      = os.open(user_id_file_path, os.O_RDONLY)
        user_id_file_content = os.read(user_id_file_fd, 1024)
        os.close(user_id_file_fd)
    else:
        user_id_file_content = None

    return user_id_file_content

###############################################################################
def get_bundle_dir():
    bundle_directory = os.path.join(os.getcwd(), '..', '..', '..', 'Plug-ins', 'BitTorrent.bundle')
    bundle_directory = bundle_directory.replace('\\\\?\\', '')
    return os.path.normpath(bundle_directory)