from pg.model.ipn import IpnMessage

__author__ = 'root'


class IPNMessageParser:
    def __init__(self, form):
        super().__init__()
        self.form = form

    def parse(self):
        full_message = ''
        for k, v in self.form:
            if len(full_message)>0:
                full_message = full_message+'&'
            full_message = full_message+k+'='+v
        ipn_message = IpnMessage()
        ipn_message.full_message = full_message
        for k, v in self.form:
            self.add_variable(ipn_message, k, v)
        return ipn_message

    def add_variable(self, ipn_message, name, value):
        if name=="txn_type":
            ipn_message.transaction_type = value
        elif name=='payment_status':
            ipn_message.payment_status = value
        elif name=='mc_gross':
            ipn_message.mc_gross = value
        elif name=='mc_currency':
            ipn_message.mc_currency = value
        elif name=='item_number':
            ipn_message.item_number = value
        elif name=='custom':
            ipn_message.custom = value
        elif name=='txn_id':
            ipn_message.txn_id=value
        elif name=='subscr_id':
            ipn_message.subscr_id=value
        elif name=='payer_email':
            ipn_message.payer_email = value