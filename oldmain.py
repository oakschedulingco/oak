import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def get_position_data(zip_code):
    # Define the base URL
    base_url = f"http://api.zippopotam.us/us/{zip_code}"

    try:
        # Make a GET request to the API
        response = requests.get(base_url)
        # Parse the JSON re
        # sponse
        data = response.json()

        # Extract latitude and longitude and state
        latitude = data["places"][0]["latitude"]
        longitude = data["places"][0]["longitude"]
        state = data["places"][0]["state abbreviation"]

        return latitude, longitude, state

    # Handle exceptions
    except (requests.exceptions.RequestException, KeyError, IndexError):
        print("Failed to retrieve data from the API or no data available for the provided zip code.")


NAME_CSRF = "_csrf"
NAME_CSRF_HEADER = "_csrf_header"


def fetch_csrf_token():
    logging.info('fetching csrf token')
    url = 'https://www.walgreens.com/findcare/schedule-vaccine/timeslots'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find("meta", attrs={"name": "_csrf"})
    csrf_header = soup.find("meta", attrs={"name": "_csrf_header"})
    logging.info('got csrf token!')
    return (csrf_header.get("content"), csrf.get("content"), resp.cookies)


hdr, tkn, cookies = fetch_csrf_token()


zip = input("What is your zip code?\n")
# Call the function and store the returned values
latitude, longitude, state = get_position_data(zip)

# Define the API endpoint and request headers
url = "https://www.walgreens.com/hcschedulersvc/svc/v8/immunizationLocations/timeslots"
headers = {
    'authority': 'www.walgreens.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json; charset=UTF-8',
    'cookie': 'bm_sv=78EBB16704736281930059DE5FB0C476~YAAQbustF7/ARFWNAQAAe8/BbxblArftvhS9ZEjDnIq9MWs1hVDe+iNL2dexS3UXGvEXILfCupeVvLXXvhMrlb/VIhiutz15gmpiQ1fbGezz+UNTJN4kis4AT8Otd9XgzKd8JOaH/+dgh5DjtV1JS68Y7uPN6hCocZlAY9z1Ms1hKyi67FPYV1LWsG/TPtsyRl1gDXRMD1dknNhLWVKjGPxhvph8IJ/Zs8nlbPh977dhHnkduJVU/F93FFOqWVNgqfRGew==~1; akavpau_walgreens=1706977289~id=25ca6a24d28cf89c692ca47a9420de31; AMCV_5E16123F5245B2970A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19757%7CMCMID%7C44436038680678690821642679102271972767%7CMCOPTOUT-1706984188s%7CNONE%7CvVersion%7C5.5.0; gpv_Page=https%3A%2F%2Fwww.walgreens.com%2Ffindcare%2Fschedule-vaccine%2Ftimeslots; s_ips=489; s_ppv=wg%253Afindcare%253Avaccinations%253Aappointment%253Aselector%2C24%2C24%2C24%2C489%2C4%2C1; s_sq=%5B%5BB%5D%5D; s_tp=2067; _abck=B9DFBD7AF9712B78FC4877D06BFF430B~0~YAAQbustF7S+RFWNAQAAqXHBbwsDOV5p6kWSZipD5RfT507ysA8cz0zjrR5lvjo8XNp0hDh4EVAg4q1tEDBNp7H9zH6/EUPnk0R55NKzDZz5abykbLpP5EBhQOYnOJz9MywUxWrlJJUu65qFTxEKyKqK9Nr28wn6mGlkIoalqI/uqS3a+SRNTRg99/QhkIhmEfDcEpS5dBvs/9BUiiq+dY6HM2Dnnn88CiFzkCEyAIGeSKGIAiWSX/F5WHRwXa97acT98oE0hbXDNjj4z66c4f/ZUNSLFAKHRjdKofFFchjM+hYsSLwfuxCderLiEdSiCvG1X3GAi3gJ7CD/mIbeM7osGGMxJQzStRPoNVWJn7M9UtUIv8Xm1PXaRR8ge2L9LK6ht0vjPDY+44n/wU5b3NYaB+8wf8bPDNQ3TQ==~-1~-1~-1; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Feb+03+2024+11%3A15%3A16+GMT-0500+(Eastern+Standard+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=aa111558-817e-494d-9731-28841251ab25&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0007%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0005%3A1&AwaitingReconsent=false; Tld-kampyleSessionPageCounter=3; USER_LOC=2%2BsKJSc9HtI2vlhveh6gobCYcCnAzYMls1GZ3v0cie7ZJzUi6y3EiFwTrfVWN%2BG4; at_check=true; mbox=PC#b88251db9e7043c998a6c19c30378dbc.34_0#1770221717|session#32e52c8779d84413b2ee23dea0695a35#1706978777; s_cc=true; fc_vexp=true; fc_vnum=1; mdLogger=false; bm_mi=E5251BE034ABEC632BD740ABE6D7C1F9~YAAQbustFwm8RFWNAQAAGq/AbxaHd4EjdVeYM9tlDS5Qum+YORzpGl1j8tFSPzIosiorRBg0KWtKUw6UV15T8nmePAw75z0pth05g0Hs7V64tWxVkcHTUo8Bznf8zH+21FCOcDLHGbdkYjcOmSfbFA51fS1VefV0+7+6dP7OZW+7Pj3FSWSJg6IsPHqwMRqHwMIQ9pu9ryyhzLnuK5GLk585weLOEtJh3jWoPfJszzkXWFHOxTmmfY58iNZ8fcRXQWW5HQZF1b31ChfiXcnL4E3xTHZ6jUnbOkKBz8/agMTBn5FuhiH1DVXdYIT0Nn5y4rlgfSO1dFT0CBiHWsv/uHJWIUvV1wIv5MA=~1; v2H=t; inqBSes_10008114=; inqSession_10008114=%7B%22_svMs%22%3A-1%2C%22_aTyp%22%3A3%2C%22sR%22%3A0%2C%22a%22%3A%22%7B%7D%22%2C%22me%22%3A%22PROD%22%2C%22al%22%3A%22en%22%2C%22lG%22%3A0%2C%22enG%22%3A1%2C%22sU%22%3A%22%22%2C%22maG%22%3A10008370%2C%22mbU%22%3A19001408%2C%22pcID%22%3A%7B%7D%2C%22C2CM%22%3A%7B%7D%2C%22CHM%22%3A%7B%22pmor%22%3Afalse%7D%2C%22auu%22%3A0%2C%22chat%22%3A%7B%22aMsgCnt%22%3A0%2C%22cMsgCnt%22%3A0%2C%22launchPageId%22%3A-1%7D%2C%22_ssID%22%3A%2276810010296583363732%22%2C%22rd%22%3A%22%22%2C%22sest%22%3A%22%22%2C%22_sT%22%3A5%2C%22ltt%22%3A1706976898261%2C%22bL%22%3A%22en-US%22%7D; inqState_10008114=%7B%22VA%22%3A%5B%5D%2C%22_loy%22%3A2%2C%22_ssQ%22%3A%5B%222024-02-03T16%3A14%3A53.050Z%22%2C%222024-02-03T01%3A34%3A24.933Z%22%5D%2C%22_slq%22%3A%5B%5D%2C%22_cct%22%3A0%2C%22_sqc%22%3A0%2C%22_slc%22%3A0%2C%22cfl%22%3A9223372036854776000%2C%22LDM%22%3A%7B%22lh%22%3A%5B%7B%22id%22%3A38454152%2C%22cg%22%3A%5B0%5D%7D%2C%7B%22id%22%3A38454118%2C%22cg%22%3A%5B%5D%7D%2C%7B%22id%22%3A38454152%2C%22cg%22%3A%5B0%5D%7D%2C%7B%22id%22%3A38454152%2C%22cg%22%3A%5B0%5D%7D%2C%7B%22id%22%3A38454118%2C%22cg%22%3A%5B%5D%7D%5D%7D%2C%22CHM%22%3A%7B%7D%2C%22fst%22%3A1706924064933%2C%22lst%22%3A1706976893050%2C%22_ist%22%3A%22ELIGIBLE%22%2C%22_sesT%22%3A327%7D; inqVital_10008114=%7B%22INQ%22%3A%7B%22custID%22%3A%227681001029658336373%22%7D%2C%22v%22%3A3%2C%22vcnt%22%3A8%2C%22vtime%22%3A1706976898261%2C%22_acid%22%3A%22-1%22%2C%22_ss%22%3A%22unsold%22%2C%22CHM%22%3A%7B%22lpt%22%3A0%2C%22lastChat%22%3A%7B%7D%2C%22lastCallId%22%3A0%7D%2C%22_is%22%3A1706976898261%2C%22_iID%22%3A%2276810010296583363731%22%2C%22_ig%22%3A%22CHAT%22%7D; str=%7B%22lt%22%3A%2235.48077808%22%2C%22lg%22%3A%22-80.85834862%22%2C%22sId%22%3A%2217234%22%2C%22st%22%3A%2221500%20CATAWBA%20AVE%22%2C%22ct%22%3A%22Cornelius%22%2C%22stat%22%3A%22NC%22%2C%22zp%22%3A%2228031%22%2C%22sdp%22%3A%221%22%2C%22odd%22%3A%221%22%2C%22bot%22%3A%22N%22%2C%22csc%22%3A%220%22%2C%22bag%22%3A%220%22%2C%22t4hr%22%3A%22N%22%2C%22curb%22%3A%220%22%2C%22oddalc%22%3A%220%22%2C%22dsch%22%3A%221%22%2C%22pom%22%3A%2210.00%22%2C%22sddth%22%3A%2235.00%22%2C%22by%22%3A%221%22%2C%22int%22%3A%22Southwest%20corner%20of%20CATAWBA%20AVENUE%20%26%20MAIN%20STREET%22%2C%22stt%22%3A%2201%22%2C%22nc%22%3A%22f%22%2C%22oddalcdops%22%3A%5B%224%22%2C%22103%22%2C%22912%22%2C%224%22%2C%223%22%2C%22911%22%2C%222%22%2C%22910%22%5D%2C%22sdpalcdops%22%3A%5B%5D%2C%22df%22%3A%225.99%22%2C%22FE_tc%22%3A%22f%22%2C%22RX_tc%22%3A%22f%22%2C%22FE_rh%22%3A%22f%22%2C%22RX_rh%22%3A%22f%22%2C%22ro%22%3A%22f%22%7D; dtm_token=AQEHdvM6peRWNAFxvlLIAQEBAQA; dtm_token_sc=AAAGd_I7pOVXNQBwv1PJAAAAAAE; _mibhv=anon-1706924066058-9413572761_6787; Tld-kampyleUserPercentile=43.295609919709364; Tld-kampyleUserSession=1706976892703; Tld-kampyleUserSessionsCount=2; gRxAlDis=N; AMCVS_5E16123F5245B2970A490D45%40AdobeOrg=1; XSRF-TOKEN=DeYyklNowZMJ5Q==.RLMjHaloAtCafpGE/BwVgdAc1dKp/+BBR697HQqbu/w=; uts=1706976891476; AKA_A2=A; ak_bmsc=7A170F09CCE54E975A3D1C948BAE66ED~000000000000000000000000000000~YAAQbustF0qzRFWNAQAA1gq/bxaSyObs1PdiSoxEsho7xpyYC2noPqg1iEorljt6wBIPsfzc8n4sblHweu8sN2W7+5Faa3fTjlPgV2qVQdqDwRTW32v65p9eNl7lews3jqIFV1jE8RHYUA1f3NQagH369K8uSkds66trBcnQajmla9+LYFWrUwiVFnoPKjMFt9wSwyXHH2yDweaVhfODv1R1boABoaFUWIklRczsX2MG+Vg7tcjOVlfv9IG6y6oD5q2h2umKmUBfYmGmNzYGN42zcZIU0831EX4NOKpOqXB2I0fBYyVmz4+gMUuMJf2Omx0Jq/Mk2XrvgkV4aFFwoKKgawSjenXYOOdlX31HxLeIuj6DDyWxtbgtHdYzhamuYy3q/nafmrWV6jQD; bm_sz=12F07D044BB14EA44C2A9AC44307256F~YAAQbustF0uzRFWNAQAA1gq/bxaxdvxdlzb7iCsLZ5v7bnY1GX4VBJieX4z+ZkHsjaBDUhRg0XPI/qbWn1H0cO1MvFM5Lkt/bZfh9mtRYtY1liwQyisu9Xpj9ifMhVMpq/TTBGYJ6XNM1IvuelmLKcSadJECC8R4C2ncQC+o562IHkaLYDld43uBBmzwCe/SdoJP8MGPVLMwEFysEhqocjwyiHZaFRIJt7JrLjcQCjznf3EftZ5lgpsCaayrtBlvt7j1+UXHQxT9E7H2Iv4ktysLZtsHq0ZklZpbP1ivjx9D+51xI0/VWyGxaE4AuJsmKhM7ACQIp+MYWCE7CJY1OA==~3291205~3552565; dtCookie=v_4_srv_28_sn_A83A710FD96FEC38BD80F99BF2033698_perc_100000_ol_0_mul_1_app-3A0eed2717dafcc06d_1_rcs-3Acss_0; session_id=0e11c78c-bbf7-4b76-bbf2-ad99d0c2b8a4; kampyle_userid=37b3-681b-44f1-d715-777e-7a22-ab01-0187; wag_sid=8ru4o49iic9ry7co0j43o974; akacd_prod-pr=1709516061~rv=19~id=385cbea3f504a3b7d65364b89421e885',
    'origin': 'https://www.walgreens.com',
    'referer': 'https://www.walgreens.com/findcare/schedule-vaccine/timeslots',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'transactionid': '4de3e140-c62c-42f2-8be0-1bad58571659',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/116.0.0.0 Mobile Safari/537.36',
    hdr: tkn
}

# Define the request payload
data = {
    "position": {
        "latitude": float(latitude),
        "longitude": float(longitude)
    },
    "state": state,
    "vaccine": [{
        "code": "150",
        "preferredManufacturer": []
    }],
    "appointmentAvailability": {
        "startDateTime": "2024-02-03"
    },
    "filter": {
        "radius": 25,
        "size": 25,
        "pageNo": 1,
        "includeUnavailableStores": False
    },
    "serviceId": "99",
    "restriction": {
        "dob": "1980-01-01"
    }
}

response = requests.post(url, headers=headers, json=data, cookies=cookies)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # The request was successful
    if response.content:
        # The response contains data
        print("The POST request returned data.")
    else:
        # The response is empty
        print("The POST request did not return any data.")
else:
    # The request was not successful, handle the error
    print(f"Request failed with status code {response.status_code}")
# Parse the JSON response
response_data = response.json()
print(response_data)

# Extract locationId, date, and numberOfSlotsAvailable
store_info = []

for i in response_data:
    print(i)
