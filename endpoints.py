#! /usr/bin/env python3

local_ip = "127.0.0.1"
port = 5000
base_url = f"https://{local_ip}:{port}/v1/api"

# Static and dynamic endpoints

endpoints = {
        'reauth': base_url + '/iserver/reauthenticate',
        'auth_status': base_url + '/iserver/auth/status',
        'accounts': base_url + '/iserver/accounts',
        'place_order': base_url + f'/iserver/account/accountId/orders',
        'reply': base_url + f'/iserver/reply/replyId',
        }
