from typing import List
from util.exception import IMException
from model.profile.account import Account
from model.profile.vouch import Vouch
from model.profile.vouch_request import VouchRequest

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
            VouchRequest.delete_by_ids(top.id, bottom.id)
        return 'Vouch request accepted'
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
