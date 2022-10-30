from kavenegar import *


def send_otp_code(phonenumebr, code):
    try:
        api = KavenegarAPI('4B706468316673354B4D307A3569354538584B76494D43586256704E6965536F7A2B4D70694664784B66553D')
        params = {
            'sender': '2000500666',
            'receptor': str(phonenumebr),
            'message': f"You're verify code is {code}"
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)