import requests
from requests import Request, Session
from requests import get
from requests import post
from bs4 import BeautifulSoup
import bs4 as bs
from flask import session




entries=('Basisvar-xdsl-prev_phone_areacode-1'
'Basisvar-router_mpls-snmp_access-1',
'Basisvar-xdsl-koloCampaign-1',
'Basisvar-vull-vull_dslam-1',
'Basisvar-line_mpls-line_floor-1',
'Basisvar-qos-advanced_service_percent-1',
'Basisvar-vull-vull_dslam_loc_id-1',
'Basisvar-product_bandwidth-product_bandwidth_down-1',
'Basisvar-mpls-headquarters-1',
'Basisvar-qos-premium_service_percent-1',
'Basisvar-router_mpls-hsrp-1',
'Basisvar-router_mpls-domain_name-1',
'Basisvar-xdsl-traffic_limit-1',
'Basisvar-xdsl-check-1',
'Basisvar-net_mpls-network-1-net_nexthop-1',
'Basisvar-mpls-line_backup-1',
'Basisvar-xdsl-installservice-1',
'Basisvar-xdsl-xdsl_wan_ip-1',
'Basisvar-hardware-username-1',
'Basisvar-xdsl-prev_phone_number-1',
'Basisvar-vdsl-nima_hostname-1',
'Basisvar-qos-standard_service_percent-1',
'Basisvar-vull-vull_phone-1',
'Basisvar-line_mpls-line_city-1',
'Basisvar-vdsl-hsi_line_backup-1',
'Basisvar-line_mpls-line_install_date_ta-1',
'Basisvar-vdsl-vdsl_guid-1',
'unlock',
'Basisvar-line_mpls-line_door-1',
'Basisvar-xdsl-suppress_uzf_mail-1',
'Basisvar-xdsl-ta_clientnr-1',
'Basisvar-mpls-vrf_id-1',
'Basisvar-line_mpls-line_street-1',
'Basisvar-xdsl-radius_max_logins-1',
'service_class_premium[]',
'Action',
'Basisvar-router_mpls-router_sn_master-1',
'Basisvar-line_mpls-line_zipcode-1',
'Submit',
'Basisvar-mpls-automatic_completion-1',
'Basisvar-net_mpls-network-1-net_config_public-1',
'Basisvar-vull-vull_line_type-1',
'Basisvar-net_mpls-network-1-net_vip-1',
'Basisvar-router_mpls-dhcp_relay_server-1',
'Basisvar-xdsl-xdsl_concentrator_submask-1',
'Basisvar-router_mpls-dhcp_active-1',
'searchStr',
'Basisvar-line_mpls-line_stairway-1',
'Basisvar-mpls-vrf_name_spoke-1',
'Basisvar-xdsl-xdsl_kuda-1',
'Basisvar-xdsl-password-1',
'Basisvar-mpls-vrf_id_spoke-1',
'Basisvar-xdsl-xdsl_speed-1',
'Basisvar-mpls-vrf_name-1',
'Basisvar-line_mpls-contact_person-1',
'Basisvar-mpls-mpls_gateway-1',
'Basisvar-xdsl-install_termin-1',
'Basisvar-line_mpls-line_housenr-1e',
'Basisvar-line_mpls-contact_phone-1e',
'PaymentSave',
'Basisvar-vull-vull_vlan-1' )

def bo_data(link,id):

    username='ahoehne'
    password='Katze7436!'
    s=requests.Session()

    s.auth=(username,password)
    c=s.get(link)
    data=s.get(link).content
    s.cookies=c.cookies
    #s.headers=c.headers
    print(c.cookies)
    print(c.headers)
    print(c.status_code)
    final_page = bs.BeautifulSoup(c.content, 'lxml')
    output=final_page.find_all('input' )

    for i in output:
        dict_data[i.parent.name]= i.attrs.get('value', 'NA')
    dict_data.pop('NA')
    

    dicto=entries_to_remove(entries, dicto)
    for i in dicto:
        print(i + ' : ' + dicto[i])
    

    return dict_data


def entries_to_remove(entries, dicto):
    for key in entries:
        if key in dicto:
            del dicto[key]

    return dicto