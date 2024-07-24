# import dependencies
import base64
from pywidevine import PSSH
from pywidevine import RemoteCdm
import requests


# Defining decrypt function
def decrypt_content(in_pssh: str = None, license_url: str = None,):
    # prepare pssh
    try:
        pssh = PSSH(in_pssh)
    except Exception as error:
        return {
            'Message': str(error)
        }

    cdm = RemoteCdm(
        device_type='ANDROID',
        system_id=int(requests.post(url='https://cdrm-project.com/devine').content),
        security_level=3,
        host='https://cdrm-project.com/devine',
        secret='CDRM-Project',
        device_name='CDM'
    )

    # open CDM session
    session_id = cdm.open()
    # print(session_id)

    # Generate the challenge
    challenge = cdm.get_license_challenge(session_id, pssh)
    # print(challenge)


    try:
        # send license challenge
        license = requests.post(
            url=license_url,
            data=challenge,
        )
    except Exception as error:
        return {
            'Message': f'An error occured {error}\n\n{license.content}'
        }

    # Another try statement to parse licenses
    # print(license.content)
    try:
        cdm.parse_license(session_id, license.content)
    except Exception as error:
        return {
            'Message': f'An error occured {error}\n\n{license.content}'
        }

    # # assign variable for returned keys
    # returned_keys = ""
    # for key in cdm.get_keys(session_id):
    #     if key.type != "SIGNING":
    #         returned_keys += f"{key.kid.hex}:{key.key.hex()}\n"
    #         # print(f"{base64.encode(key.kid.hex).decode()}:{base64.encode(key.key.hex())}\n")

    # Extract keys
    returned_keys = [
            {
                "kty": "oct",
                "k": base64.b64encode(key.key).decode('utf-8').rstrip('='),
                "kid": base64.b64encode(key.kid.bytes).decode('utf-8').rstrip('=')
            }
            for key in cdm.get_keys(session_id)
            if key.type != "SIGNING"
        ]

    # close session, disposes of session data
    cdm.close(session_id)


    # Return the keys
    return {
            "keys": returned_keys,
            "type": "temporary"
        }

if __name__ == '__main__':
    pssh = "AAAAOHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABgSEI4B8Vc1oV5/rj0sQO7E0Gs4hOz7tAY="
    license_url = "https://tataplay.live.ott.irdeto.com/Widevine/getlicense?CrmId=tatasky&AccountId=tatasky&ContentId=400000119&ls_session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNvbnRyb2xfc2lnbmluZ19rZXlfcHJvZHVjdGlvbl8xNjkyMjk1MDk4NjMxIn0.eyJzdWIiOiIxMDgxMTg0MDQ0IiwiaXNlIjp0cnVlLCJqdGkiOiI3Y2UzOWQxZi02N2E4LTQxM2YtYTlhNS03OWE4NDY4YzkwNTUiLCJhaWQiOiJ0YXRhc2t5IiwiZXhwIjoxNzIxODI5OTAxLCJuYW1lIjoiUmFqIERldiIsImlhdCI6MTcyMTgxNTUwMSwiZW50IjpbeyJlcGlkIjoiU3Vic2NyaXB0aW9uX0Jyb3dzZXJfU3RyZWFtaW5nIiwiYmlkIjoiMTAwMDAwMDAwMSJ9LHsiZXBpZCI6IlN1YnNjcmlwdGlvbl9Ccm93c2VyX1N0cmVhbWluZyIsImJpZCI6IjEwMDAwMDE1MjMifSx7ImVwaWQiOiJTdWJzY3JpcHRpb25fQnJvd3Nlcl9TdHJlYW1pbmciLCJiaWQiOiIxMDAwMDAxMDM4In0seyJlcGlkIjoiU3Vic2NyaXB0aW9uX0Jyb3dzZXJfU3RyZWFtaW5nIiwiYmlkIjoiMTAwMDAwMTAzNSJ9LHsiZXBpZCI6IlN1YnNjcmlwdGlvbl9Ccm93c2VyX1N0cmVhbWluZyIsImJpZCI6IjEwMDAwMDAwMzMifSx7ImVwaWQiOiJTdWJzY3JpcHRpb25fQnJvd3Nlcl9TdHJlYW1pbmciLCJiaWQiOiIxMDAwMDAwMDAyIn0seyJlcGlkIjoiU3Vic2NyaXB0aW9uX0Jyb3dzZXJfU3RyZWFtaW5nIiwiYmlkIjoiMTAwMDAwMDAwMyJ9XSwiY3NtbyI6eyJtYXMiOiI2IiwiZHQiOiJ0cG1hIiwibWFzZCI6IjIifSwiaXNzIjoidHBtYV93ZWIifQ.gGqIKPK550PKksWNW43z8FQNM_C2KQKGbfgmU2VOxaU"
    print(decrypt_content(pssh,license_url))