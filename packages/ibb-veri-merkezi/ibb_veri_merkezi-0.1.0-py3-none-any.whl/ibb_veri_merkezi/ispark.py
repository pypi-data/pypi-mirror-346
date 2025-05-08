import pandas as pd
import requests


def get_parking_lots(to_frame=False):
    """
    İstanbul Büyükşehir Belediyesi'nin (İBB) İSPARK API'sinden tüm otoparkların listesini alır.

    Args:
        to_frame (bool): Eğer `True` olarak ayarlanırsa, sonuç bir pandas DataFrame olarak döner.
                         Aksi takdirde JSON formatında döner.

    Returns:
        Union[List[dict], pd.DataFrame, dict]:
            - Başarılı isteklerde: Tüm otopark bilgilerini içeren JSON listesi veya DataFrame.
            - Başarısız isteklerde: {'message': 'No data', 'status_code': ...} şeklinde bir sözlük.
    """

    url = 'https://api.ibb.gov.tr/ispark/Park'
    res = requests.get(url)
    if res.status_code == 200:
        if to_frame:
            return pd.DataFrame(res.json())
        else:
            return res.json()
    else:
        return {'message': 'No data', 'status_code': res.status_code}


def get_parking_lot(park_id):
    """
    Belirli bir İSPARK otoparkının detaylı bilgilerini getirir.

    Args:
        park_id (int): Detayları istenen otoparkın ID numarası.

    Returns:
        Union[dict]:
            - Başarılı isteklerde: Otoparka ait detaylı bilgi içeren bir sözlük.
            - parkID değeri 0 ise: {'message': 'No data', 'status_code': 404}
            - Başarısız isteklerde: {'message': 'No data', 'status_code': ...}
    """

    url = f'https://api.ibb.gov.tr/ispark/ParkDetay?id={park_id}'
    res = requests.get(url)
    if res.status_code == 200:
        park = res.json()[0]
        if park['parkID'] == 0:
            return {'message': 'No data', 'status_code': 404}
        return park
    else:
        return {'message': 'No data', 'status_code': res.status_code}


if __name__ == '__main__':
    pass
    # print(get_parking_lots(to_frame=True))
    # print(get_parking_lot(1487))
