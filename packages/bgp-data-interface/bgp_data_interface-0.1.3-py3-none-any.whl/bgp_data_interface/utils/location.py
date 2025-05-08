from typing import Any

BBO = 'BBO'
ABP = 'ABP'
ABPR = 'ABPR'
BIP = 'BIP'
BPLC = 'BPLC'
GLB = 'GLB'
VHH = 'VHH'

_locations: dict[str, Any] = {
    BBO: {
        'name': 'Bang Bo',
        'abbreviation': BBO,
        'latitude': 13.4916354486428,
        'longitude': 100.85609829815238
    },
    ABP: {
        'name': 'Amata Chonburi',
        'abbreviation': ABP,
        'latitude': 13.438325247289432,
        'longitude': 101.03261043520196
    },
    ABPR: {
        'name': 'Amata Rayong',
        'abbreviation': ABPR,
        'latitude': 12.967463192203619,
        'longitude': 101.10886287800753
    },
    BIP: {
        'name': 'Bangkadi',
        'abbreviation': BIP,
        'latitude': 13.981568940669403,
        'longitude': 100.56130494764083
    },
    BPLC: {
        'name': 'Laem Chabang',
        'abbreviation': BPLC,
        'latitude': 13.088506958504015,
        'longitude': 100.90629722775577
    },
    GLB: {
        'name': 'Gerhard Link',
        'abbreviation': GLB,
        'latitude': 13.749774021289749,
        'longitude': 100.6470687945474
    },
    VHH: {
        'name': 'Veranda Hua Hin',
        'abbreviation': VHH,
        'latitude': 12.740478045961716,
        'longitude': 99.96559233685912
    }
}

def get_keys() -> list[str]:
    return list(_locations.keys())

def get_location(name: str) -> dict[str, Any]:
    return _locations.get(name, {})
