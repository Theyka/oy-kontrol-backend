from quart import Quart, request, jsonify, Response
from quart_cors import cors, route_cors
from hypercorn.config import Config
from hypercorn.asyncio import serve
from bs4 import BeautifulSoup
import datetime
import requests
import asyncio
import aiohttp
import sqlite3
import random
import time
import json


def sorgula(tckn):
    url = "https://sts.chp.org.tr/Default.aspx"
    headers_def = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.6",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "cookie": "ASP.NET_SessionId=x4bkfsrmeku12vs0a3louedl; __cf_bm=VADSIiyWG5QO6NJTbhZaunZ4vg14pMdVIVjGBq9kdI4-1684264689-0-AbyTOQirufFjEI+ptW2clIxgZTtqYCYOLtT9Qujk/CB8YAQvXzWuQME4KbN1WN3GFtGZQ17LOW7NbiZvGQf6b7k=",
        "Referer": "https://sts.chp.org.tr/Default.aspx",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    data_def = f"__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=ktJeM064phMGqt8I3LVn3dV8zHmaT%2BCM2dGpeCQEsYyuY2xZAThrTCyAmWEdmwR1hqez9aAxxBEsSx2Dc7q8SSJVYjM%3D&__VIEWSTATEGENERATOR=CA0B0334&__EVENTVALIDATION=jMsEFikyE5EkKn1n2%2FznrsvzXvQiMFN1EPBObGeLSKpt%2BW3yUDKzW%2BXI3OcuN1g4%2BKsuQ7t5XZhwb65GMCB4HYGjqJP2wEPkxhSvcRBUwpD886hMDtvlePrQ6BG7wl71hpMm5w%2BRaeeHM9L7oJDY0ThfUM3NI31JcC7TVspBq7lSglrs&rdveriKaynagi=1&txtTCKN={tckn}&btnSorgula=SORGULA"
    response_def = requests.post(url, headers=headers_def, data=data_def)

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.6",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "cookie": "ASP.NET_SessionId=x4bkfsrmeku12vs0a3louedl; __cf_bm=VADSIiyWG5QO6NJTbhZaunZ4vg14pMdVIVjGBq9kdI4-1684264689-0-AbyTOQirufFjEI+ptW2clIxgZTtqYCYOLtT9Qujk/CB8YAQvXzWuQME4KbN1WN3GFtGZQ17LOW7NbiZvGQf6b7k=",
        "Referer": response_def.url,
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    data = f"__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=Z23QeiTbpaaRWKFMM7cSn2LbJDSQOWUawAL8f72yBxtnLWRSBl0jO06DA8pnRmPmtVzHx2jIGAtjxBliGRGe%2BvecsSbcsP4DetOWmSdBjN30NlCHQMglIOX2WAdPSpY4cS8dzPBfQUmJRQvQejWCdlTHc8AMLLGS0oo12xZvrg9PNoF9KErtSZ%2FviTIHhiRQT%2FA63ICGyyesNQaat6izareq98Y%2BOnGUuAq1p1%2B%2BbUEB%2FDgdddOKSDNZDwq2eRs8FDFg2M0%2B2GylylPeAO7a%2BRklTFr%2B944JWFV6mm8xco2W%2Fqpw%2BuFIEtS6c4q7wVncq%2B25anC4pwWX%2B0Wm793xQSISnf%2B9Z8gYyUwTWbipnttVtOIv8ccrBumKjC2lIMBQsFkhfmme5aYB5aq9ghF637mxP%2Fa0ku3PDBrZsPmpbHj5BtmNVghh7BfDexsttPU4psKFpAhqK%2B7iHDKyCdIvZiplCfkw6P%2BU3CgGS5H5f5AJsfoLvpa7nzwQXlcBZDPs7BbESX53DXV7seeWQ8ZpH0Uqt0ifl%2FB3QN2FLPWxVpp5j833BiTj3nRsZ%2Bicg%2FhU5iGQHpQlQqtoi6IOGHIFMtcXy%2BNgSfnSIcu1QfCCzp%2FwnvK97ReOcf50SXElBCjsemTIuK51t5BaCV%2F4OpLHEbHYDvJvbvkPv27ATSd%2B%2FDVt1VwLvi6eNt2JIxBkCAHvC0ylJicMrdywAX%2BmgB7MHUkXSreISqfH6lyeFaaF5jZAyU53IziWg%2BhOSgrUDu0oJt3t8uBXnLoh0Zt5076SE14NPJupbXyLUClr3cHpPAaV6Ndgu2PE8LausfkPCklWmCMmVNsuy30EarRfV5NjdE6D4Zr3oKPpBSoN%2FtaLTXol3lqfdTWep%2F2enWBsaaFi4NtXV5uBVZyoTRtpHea6gjQ7wYvIa52N19HUYKYeNRdMIbeoBOesCCgZI1%2BaACpM%2Bn%2B9WGmZ0hf1Pee1Ksvg%2FenNv0TZoAlIi48XTCh4cgJc3W8maGu7D3XmnKQOa5018boWUd6VyNzBwXRowA9lFRnbCSNluU82M7FGC6S1uGAjpCAjZkXm2uVbAuIN80Wql39%2FWy91XedfMSQggx6bsv6VKHs%3D&__VIEWSTATEGENERATOR=F021598D&__EVENTVALIDATION=6xvrVy5ujH3NYuPRMWNpTbqy%2B2Pz8Htr6Rng3xpfHhJZliQowrPSjUDm4%2FTSGL0%2B%2Bk0jNIZhZkE4pDw9z9TNMDNh8HPoLAdEgeIHGOxNXcHhsNLgl%2FAc8nKjE4IGt8U7WKHPXLy3%2Fn6zMO1lBMahwUgfuW0vhrcv9npDnlKPRxco9nU5O9xNS8TvNI5UpQlAj6%2BqCT4P6%2FYBf8z%2BRZGhBTmPmhpPj3jF72yJLERmOaA9%2BuGBJrXg%2F0bzHDuKJgz53u08kBTHRtqzQqlytprhri2GA3%2FcMPotcI5tLe2XN60QGDjli%2BMcqz6iENjJ1esasVCqUwPIKMNlWZQ6l4jOwNscj%2FnmgS3CqNDTCJoVEh1Io2wCUi%2B1IDdjICGXfpMEgWV7U3kQW8mC%2B3A0pp6FvHRE4IixlYiR%2FDZXzKfTa3IPsbpeo7PrbcjV%2Fv7i1pQygkQHus3qTtV1RJsP3ejl39Svsp%2FNHKvxuJdU%2B8oeJ%2Bz5lm7K&btnCb=CUMHURBA%C5%9EKANI+SE%C3%87%C4%B0M+SONU%C3%87LARI&txtCbKayitliSecmen=351&txtCbOyKullanan=328&txtCbKanunGeregi=328&txtCbKullanilanToplamOy=325&txtCbItirazsizligecerli=0&txtCbItirazligecerli=0&txtCbGecerliOy=325&txtCbGercersizOy=3&txtCB1=157&txtCB2=3&txtCB3=155&txtCB4=10&txtAciklama=&KalanGoster=200&txtAdSoyad=&txtTelefon=&txtEPosta="

    response = requests.post(response_def.url, headers=headers, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    etiket = soup.find("span", {"id": "lblCbIlIlceBaslik"}).text
    sandikalani = soup.find("span", {"id": "lblCbSandikAlani"}).text
    kayitli_secmen = soup.find('input', {'name': 'txtCbKayitliSecmen'})['value']
    oy_kullanan = soup.find('input', {'name': 'txtCbOyKullanan'})['value']
    kanun_geregi_oy = soup.find('input', {'name': 'txtCbKanunGeregi'})['value']
    kullanilan_toplam_oy = soup.find('input', {'name': 'txtCbKullanilanToplamOy'})['value']
    itirazsiz_gecerli_oy = soup.find('input', {'name': 'txtCbItirazsizligecerli'})['value']
    itirazli_gecerli_oy = soup.find('input', {'name': 'txtCbItirazligecerli'})['value']
    gecerli_oy = soup.find('input', {'name': 'txtCbGecerliOy'})['value']
    gecersiz_oy = soup.find('input', {'name': 'txtCbGercersizOy'})['value']

    adaylar = soup.find_all('div', {'class': 'chp-vote-row'})
    aday_data = {}
    for aday in adaylar:
        ad = aday.find('img')['alt']
        oy = aday.find('input')['value']
        aday_data[ad] = oy

    data['konum'] = etiket
    data['okul_adi'] = sandikalani
    data['kayitli_secmen'] = kayitli_secmen
    data['oy_kullanan_kayitli_secmen'] = oy_kullanan
    data['kanun_geregi_oy_kullanan'] = kanun_geregi_oy
    data['kullanilan_toplam_oy'] = kullanilan_toplam_oy
    data['itirazsiz_gecerli_oy'] = itirazsiz_gecerli_oy
    data['itirazli_gecerli_oy'] = itirazli_gecerli_oy
    data['gecerli_oy'] = gecerli_oy
    data['gecersiz_oy'] = gecersiz_oy
    data['adaylar'] = aday_data

    return data


app = Quart(__name__)

CORS_SETTINGS = {'allow_origin': '*'}
quart_app = cors(app, **CORS_SETTINGS)


@app.route("/get_info")
async def chpfetch():
    if request.args.get('tckn'):
        try:
            return Response(response=json.dumps(sorgula(request.args.get('tckn')), ensure_ascii=False),
                            mimetype="application/json")
        except Exception as error:
            return jsonify({'error': error, 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    else:
        return jsonify({'error': 'tckn not found', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


@app.route("/oyveotesi")
async def oyveotesi():
    try:
        if request.args.get('city_name') and request.args.get('district_name') and request.args.get('ballot_box_id'):
            try:
                conn = sqlite3.connect('ovodata.sqlite')
                cursor = conn.cursor()
                get_data = cursor.execute(
                    "SELECT * FROM ovo_submissions WHERE city_name = ? AND district_name = ? AND ballot_box_id = ?", (
                    request.args.get('city_name'), request.args.get('district_name'),
                    request.args.get('ballot_box_id')))
                row = get_data.fetchone()

                cursor.execute("UPDATE status SET requests = requests+1")
                conn.commit()
                conn.close()
                if row is None:
                    return jsonify(
                        {'error': 'no information', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                else:
                    return jsonify({'id': row[0], 'city_name': row[1], 'district_name': row[2], 'ballot_box_id': row[3],
                                    'image_url': row[4], 'recep_tayyip': row[5], 'muharrem_ince': row[6],
                                    'kemal_kilicdaroglu': row[7], 'sinan_ogan': row[8]})
            except Exception as error:
                return jsonify({'error': error, 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        else:
            return jsonify({'error': 'args not found', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    except Exception as error:
        return jsonify({'error': error, 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


@app.route("/status")
async def status():
    try:
        conn = sqlite3.connect('ovodata.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM status")
        row = cursor.fetchone()
        if row is None:
            return jsonify({'error': 'no information', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        else:
            return jsonify({'requests': row[0]})
    except Exception as error:
        return jsonify({'error': error, 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


if __name__ == "__main__":
    config = Config()
    config.bind = "0.0.0.0:25696"
    asyncio.run(serve(quart_app, config=config))
