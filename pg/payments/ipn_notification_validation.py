import requests

__author__ = 'root'


class IPNNotificationValidation:
    cmd = "_notify-validate"
    verified = "VERIFIED"

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def validate(self, message):
        nvp_string = "cmd=" + self.cmd + "&"
        fullMessage = message.full_message
        nvp_string = nvp_string + fullMessage
        paypal_url = ''
        if self.ioc.get_config()['ENVIRONMENT']=='PRODUCTION':
            paypal_url = self.ioc.get_config()['prod.paypal.url']+"/cgi-bin/webscr"
        else:
            paypal_url = self.ioc.get_config()['paypal.url']+"/cgi-bin/webscr"
        response = requests.post(paypal_url, data=nvp_string)

        if response is not None:
            return response==self.verified and message.payment_status=='Completed'
        return False
