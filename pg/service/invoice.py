from pg import model, resource_bundle, app

__author__ = 'krzysztof.maslak'
import datetime
import requests

class An:
    def __init__(self, **entries): self.__dict__.update(entries)

class InvoiceService:
    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def generate_invoice_number(self):
        return model.Invoice.query.filter(model.Invoice.creation_date>datetime.date(datetime.date.today().year,1, 1)).count()

    def generate_invoice(self, account_id, invoice, messages, language):
        data = {'invoice': invoice, messages: messages, language: language}
        r = requests.post(self.ioc.get_config()['INVOICE_SERVICE_URL'], data=data)
        invoices_dir = self.ioc.get_config()['INVOICES_DIR']
        file_name = invoices_dir+'/'+account_id+'/'+invoice.reference_number
        chunk_size = 512
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
        return file_name

    def new_invoice_from_order(self, order):
        if isinstance(order, model.Order):
            invoice = model.Invoice()
            invoice.reference_number = order.order_number
            invoice.invoice_number = self.generate_invoice_number()+"/"+ datetime.date.today().year
            ps = self.ioc.new_property_service()
            invoice.issue_city = ps.find_value_by_code(order.offer.account, 'invoice.issue.city')
            issuer = model.InvoiceIssuer(ps.find_value_by_code(order.offer.account, 'invoice.issue.name'),
                                   ps.find_value_by_code(order.offer.account, 'invoice.issue.address'),
                                   ps.find_value_by_code(order.offer.account, 'invoice.issue.city'),
                                   ps.find_value_by_code(order.offer.account, 'invoice.issue.vatNumber'),
                                   ps.find_value_by_code(order.offer.account, 'invoice.issue.country'))
            invoice.issuers.append(issuer)
            app.db.session.commit()
            invoice_items = []
            shipping = 0.0
            for item in order.offer.items:
                if item.variations is not None and len(item.variations)>0:
                    for iv in item.variations:
                        tax_value = iv.net*iv.quantity*iv.tax/100
                        total_value = iv.net*iv.quantity + tax_value
                        if iv.quantity==1:
                            shipping += iv.shipping
                        else:
                            for c in range(iv.quantity-1):
                                if iv.shipping_additional is not None:
                                    shipping += iv.shipping_additional
                                else:
                                    shipping += iv.shipping
                        invoice_items.append(An(title=item.title+' '+iv.title,
                                                quantity=iv.quantity, net_price=iv.net,
                                                net_value=iv.net*iv.quantity,
                                                vat_percentage=iv.tax, vat_value = tax_value, total=total_value))
                else:
                    tax_value = item.net*item.quantity*item.tax/100
                    total_value = item.net*item.quantity + tax_value
                    if item.quantity==1:
                        shipping += item.shipping
                    else:
                        for c in range(item.quantity-1):
                            if item.shipping_additional is not None:
                                shipping += item.shipping_additional
                            else:
                                shipping += item.shipping
                    invoice_items.append(An(title=item.title, quantity=item.quantity, net_price=item.net,
                                            net_value=item.net*item.quantity,
                                            vat_percentage=item.tax, vat_value = tax_value, total=total_value))
            invoice.items = invoice_items
            invoice.shipping = An(title=item.title, quantity=item.quantity, net_price=item.net,
                                            net_value=item.net*item.quantity,
                                            vat_percentage=item.tax, vat_value = tax_value, total=total_value)
            messages = resource_bundle.ResourceBundle()
            invoice_items.append(An(title=messages.get_text(order.lang, "shipping"), total=shipping))
            invoice.subtotals = {}
            for i in invoice_items:
                if invoice.subtotals[item.vat_percentage] is not None:
                    invoice.subtotals[item.vat_percentage] = An(net=i.net_value+invoice.subtotals[item.vat_percentage].net,
                                                                vat=i.vat_value+invoice.subtotals[item.vat_percentage].vat,
                                                                total=i.total+invoice.subtotals[item.vat_percentage].total)
                else:
                    invoice.subtotals[item.vat_percentage] = An(net=i.net_value, vat=i.vat_value, total=i.total)
    # //                for(int i=0;i<100;i++){
    # //                    TotalPriceBlock bl = inmap.get((100-i)+"");
    # //                    if(bl!=null){
    # //                        invoiceSubtotals.add(
    # //                                InvoiceSubtotal.InvoiceSubtotalBuilder.invoiceSubtotal()
    # //                                        .withNetprice(bl.getNetprice())
    # //                                        .withTotalprice(bl.getTotalprice())
    # //                                        .withVatPercentage(bl.getVat())
    # //                                        .withVatprice(bl.getVat())
    # //                                        .build()
    # //                        );
    # //                    }
    # //                }
            messages = {'invoicing_invoice_jm_title':messages.get_text(order.lang, 'unit'),
                        'invoicing_invoice_no':messages.get_text(order.lang, 'ret_short'),
                        'invoicing_invoice_system_name':messages.get_text(order.lang, 'returns_info'),
                        'invoicing_invoice_system_name':messages.get_text(order.lang, 'invoice_thank_you')}
            return self.generate_invoice(order.offer.account_id, invoice, messages, order.lang)
        else:
            raise TypeError("Expected Order type in InvoiceService.new_invoice_from_order %s"%type(order))