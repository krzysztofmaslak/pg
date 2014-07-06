from multiprocessing.context import Process
from pg import model

__author__ = 'krzysztof.maslak'

from pg import resource_bundle

class PaymentProcessorService:
    def __init__(self, ioc, logger):
        super().__init__()
        self.ioc = ioc
        self.logger = logger

    def process_paid_order(self, order):
        self.logger.info(order.order_number+" - process")
        self.ioc.new_order_service().process_paid_order(order)
        p = Process(target=self.inform_customer, args=(self.ioc, order,))
        p.start()
        p.join()

    def generate_invoice(self, order):
        return self.ioc.new_inovice_service().new_invoice_from_order(order)

    def inform_customer(self, ioc, order):
        # invoice = self.generate_invoice(order)
        customer_email = model.Email()
        customer_email.type = "PURCHASE_CONFIRMATION"
        customer_email.ref_id = order.id
        ps = self.ioc.new_property_service()
        customer_email.from_address = ps.find_value_by_code(order.offer.account, 'sales.email')
        customer_email.to_address = order.billing.first().email
        customer_email.language = order.lang
        customer_email.subject = ps.find_value_by_code(order.offer.account, 'order_confirmation')
        # customer_email.addon1 = invoice.file_name
        # customer_email.addon2 = invoice.id
        self.ioc.new_email_service().save(customer_email)
        order.confirmation_email = 1
        model.base.db.session.commit()

        admin_confirmation_email_subject = resource_bundle.ResourceBundle().get_text(order.offer.account.lang, 'admin_confirmation_email_subject')
        admin_email = model.Email()
        admin_email.type = 'PURCHASE_CONFIRMATION_ADMIN'
        admin_email.from_address = ps.find_value_by_code(order.offer.account, 'sales.email')
        admin_email.to_address = ps.find_value_by_code(order.offer.account, 'sales.email')
        admin_email.subject = admin_confirmation_email_subject.format(order.order_number, str(ioc.new_order_service().find_order_total(order)))
        self.ioc.new_email_service().save(admin_email)
