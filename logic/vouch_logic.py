from typing import List
from config.config import config
from util.exception import IMException
from model.profile.account import Account
from model.profile.vouch import Vouch
from model.profile.vouch_request import VouchRequest
from model.event.vouch_request import VouchEvent, VouchEventType

def get_requests(account: Account) -> List[VouchRequest]:
    result = []
    result += VouchRequest.find_by_top_id(account.id)
    result += VouchRequest.find_by_bottom_id(account.id)
    return result

def make_request(requester: Account, top: Account, bottom: Account):
    # check if both same
    if top.id == bottom.id:
        raise IMException('Cannot vouch self')
    # check in vouch table
    if Vouch.find_by_ids(top.id, bottom.id):
        raise IMException('Vouch already exists')
    # check if requester is one of the accounts
    if requester.id != top.id and requester.id != bottom.id:
        raise IMException('Requester must be present in vouch request')
    # check in vouch_request table
    vr = VouchRequest.find_by_ids(top.id, bottom.id)
    if vr:
        # accept
        if requester.id == top.id:
            vr.top_accept = True
        if requester.id == bottom.id:
            vr.bottom_accept = True
        vr.save_to_db()
        #if both accepted make new vouch
        if vr.top_accept and vr.bottom_accept:
            vouch = Vouch(top.id, bottom.id)
            vouch.save_to_db()
            vre = VouchEvent(VouchEventType.start, requester.id, top.id, bottom.id)
            vre.save_to_db()
            update_vouching_resource(bottom)
            VouchRequest.delete_by_ids(top.id, bottom.id)
            return 'Vouch request accepted'
        raise IMException('Vouch request already sent')
    # make vouch_request
    vr = VouchRequest(top.id, bottom.id)
    # accept requester
    if requester.id == top.id:
        vr.top_accept = True
    elif requester.id == bottom.id:
        vr.bottom_accept = True
    else:
        raise IMException('Requester not present in vouch request')
    vr.save_to_db()
    return 'Vouch request sent'

def remove_vouch_request(requester: Account, top: Account, bottom: Account):
    # check if both same
    if top.id == bottom.id:
        raise IMException('Cannot vouch self')
    # check if requester is one of the accounts
    if requester.id != top.id and requester.id != bottom.id:
        raise IMException('Requester must be present in vouch request')
    # check in vouch_request table
    VouchRequest.delete_by_ids(top.id, bottom.id)
    return 'Deleted request'

def remove_vouch(requester: Account, top: Account, bottom: Account):
    # check if both same
    if top.id == bottom.id:
        raise IMException('Cannot vouch self')
    # check if requester is one of the accounts
    if requester.id != top.id and requester.id != bottom.id:
        raise IMException('Requester must be present in vouch request')
    Vouch.delete_by_ids(top.id, bottom.id)
    vre = VouchEvent(VouchEventType.stop, requester.id, top.id, bottom.id)
    vre.save_to_db()
    update_vouching_resource(bottom)
    return 'Deleted vouch'

def get_vouches(account: Account) -> List[Vouch]:
    result = []
    result += Vouch.find_by_top_id(account.id)
    result += Vouch.find_by_bottom_id(account.id)
    return result

def update_vouching_resource(account: Account):
    vouches = VouchRequest.find_by_bottom_id(account.id)
    new_speed = speed_per_vouch_nbr(len(vouches))
    pass

resource_speed_per_vouch_cache = {}
def speed_per_vouch_nbr(vouch_nbr: int):
    global resource_speed_per_vouch_cache
    if not resource_speed_per_vouch_cache:
        for item in config['vouch']['resource_speed_per_vouch'].split(','):
            subitem = item.split(':')
            resource_speed_per_vouch_cache[int(subitem[0])] = float(subitem[1])
    current_speed = 0
    for key, value in resource_speed_per_vouch_cache.items():
        if vouch_nbr == key:
            return value
        elif vouch_nbr > key:
            current_speed = value
    return current_speed