from util.exception import IMException
from model.profile.account import Account
from model.profile.vouch import Vouch
from model.profile.vouch_request import VouchRequest

def make_request(requester: Account, top: Account, bottom: Account):
    # check if both same
    if top.id == bottom.id:
        raise IMException('Cannot vouch self')
    # check in vouch table
    if Vouch.find_by_ids(top.id, bottom.id):
        raise IMException('Vouch already exists')
    # check in vouch_request table
    if VouchRequest.find_by_ids(top.id, bottom.id):
        raise IMException('Vouch request already exists')
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

def accept_request(accepter: Account, top: Account, bottom: Account):
    #find vouch_request
    vr = VouchRequest.find_by_ids(top.id, bottom.id)
    if not vr:
        raise IMException('Vouch request not found')
    #set accept
    if accepter == top.id:
        vr.top_accept = True
    if accepter == bottom.id:
        vr.bottom_accept = True
    # vr.save_to_db()
    #if both accepted make new vouch
    if vr.top_accept and vr.bottom_accept:
        vouch = Vouch(top.id, bottom.id)
        vouch.save_to_db()
        VouchRequest.delete_by_ids(top.id, bottom.id)