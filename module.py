def spn1(json_response):
    low = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['boundedBy']['Envelope'][
        'lowerCorner']
    high = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['boundedBy']['Envelope'][
        'upperCorner']
    ll1 = list(map(float, low.split()))
    ll2 = list(map(float, high.split()))
    spn = ','.join(map(str, (abs(ll1[0] - ll2[0]), abs(ll1[1] - ll2[1]))))
    return spn