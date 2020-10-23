import uuid
from util.exception import IMException
from model.profile.account import Account
from model.profile.vouch import Vouch
from model.profile.vouch_request import VouchRequest

def make_request(requester: uuid, top_id: uuid, bottom_id: uuid):
    # check in vouch table
    if Vouch.find_by_ids(top_id, bottom_id):
        raise IMException('Vouch already exists')
    # check in vouch_request table
    if VouchRequest.find_by_ids(top_id, bottom_id):
        raise IMException('Vouch request already exists')
    # make vouch_request
    vr = VouchRequest(top_id, bottom_id)
    # accept requester
    if requester == top_id:
        vr.top_accept = True
    if requester == bottom_id:
        vr.bottom_accept = True
    vr.save_to_db()

def accept_request(accepter: uuid, top_id: uuid, bottom_id: uuid):
    #find vouch_request
    vr = VouchRequest.find_by_ids(top_id, bottom_id)
    if not vr:
        raise IMException('Vouch request not found')
    #set accept
    if accepter == top_id:
        vr.top_accept = True
    if accepter == bottom_id:
        vr.bottom_accept = True
    vr.save_to_db()
    #if both accepted make new vouch
    if vr.top_accept and vr.bottom_accept:
        vouch = Vouch(top_id, bottom_id)
        vouch.save_to_db()
        VouchRequest.delete_by_ids(top_id, bottom_id)