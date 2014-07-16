__author__ = 'root'

class ResourceBundle:
    def get_text(self, lang, code):
        return self.get_all(lang)[code]

    def get_all(self, lang):
        if lang=='en':
            return {
                'contact_message_success':'Your message was accepted, we will respond shortly',
                'contact_title':'Send us a message',
                'contact_email':'Email address',
                'contact_email_placeholder':'Email',
                'contact_message':'Message',
                'contact_btn':'Send',
                'need_an_account':'Need an account ?',
                'contact':'Contact',
                'copy_to_clipboard':'Copy to clipboard',
                'checkout_product_title':'Product title',
                'checkout_delete_product':'Delete product',
                'already_a_member':'Already a member ?',
                'you_are_no_longer_logged_in':'You are no longer logged in.',
                'new_password_title':'Reset password',
                'new_password_password':'Password',
                'new_password_placeholder':'Password',
                'new_password_confirm_password':'Confirm password',
                'new_password_confirm_password_placeholder':'Confirm password',
                'new_password_btn':'Reset password',
                'new_password_mismatch':'Please retype your password again',
                'registration_email_subject':'Registration email',
                'login_title':'Log in',
                'login_username':'Email address',
                'login_username_placeholder':'Email',
                'login_password':'Password',
                'login_password_placeholder': 'Password',
                'login_btn':'Log in',
                'login_remind_me_my_password':'Remind me my password',
                'login_wrong_username_or_password':'Wrong username or password',
                'login_user_inactive':'User is inactive, check your mailbox for instructions to complete registration process',
                'register_title':'Register',
                'register_username':'Email address',
                'register_username_placeholder':'Email',
                'register_password':'Password',
                'register_password_placeholder':'Password',
                'register_user_already_exist':'User already exist',
                'register_success':'To finish registration, please check your mailbox for an email with activation link.',
                'reset_password_title':'Reset password',
                'reset_password_username':'Email address',
                'reset_password_placeholder':'Email',
                'reset_password_btn':'Reset password',
                'reset_password_link_info':'We have sent you an email with reset password link that when clicked will allow you to define new password.',
                'reset_password_no_email':'We couldn&#39;t find account with this email address.',
                'register_btn':'Register',
                'offer_saved_successfully':'Offer saved successfuly',
                'offer_list_title': 'Title',
                'offer_list_creation_date': 'Creation date',
                'offer_list_edit': 'Edit',
                'offer_list_delete': 'Delete',
                'offer_list_next': 'Next',
                'offer_list_previous': 'Previous',
                'offer_list_add_new_offer': 'Add new offer',
                'offer_form_title': 'Offer title',
                'offer_form_creation_date': 'Creation date',
                'offer_form_direct_link': 'Direct link',
                'offer_form_products': 'Products',
                'offer_form_multiple_variations': 'Multiple variations',
                'offer_form_multiple_variations_no': 'No',
                'offer_form_multiple_variations_yes': 'Yes',
                'offer_form_quantity': 'Quantity',
                'offer_form_net': 'Net',
                'offer_form_tax': 'Tax',
                'offer_form_shipping': 'Shipping',
                'offer_form_shipping_additional':'Shipping additional',
                'offer_form_delete_variation': 'Delete variation',
                'offer_form_add_more_variations':'Add more variations',
                'offer_form_photos': 'Photos',
                'offer_form_currency':'Currency',
                'offer_form_add_product':'Add product',
                'offer_form_save_offer':'Save offer',
                'offer_form_please_select':'--Please select--',
                'offer_form_variation': 'Variation',
                'order_saved_successfully':'Data saved successfully',
                'order_list_date':'Date',
                'order_list_total':'Total',
                'order_list_show':'Show',
                'order_list_previous':'Previous',
                'order_list_next':'Next',
                'order_list_no_orders':'There are no orders',
                'order_form_number':'Order number',
                'order_form_total':'Total',
                'order_form_first_name':'First name',
                'order_form_last_name':'Last name',
                'order_form_email':'Email',
                'order_form_address1':'Address1',
                'order_form_address2':'Address2',
                'order_form_county':'County',
                'order_form_postal_code': 'Postal code',
                'order_form_country':'Country',
                'order_form_city':'City',
                'order_form_company':'Company',
                'order_form_phone_number':'Phone number',
                'order_form_order_item_title':'Title',
                'order_form_order_item_quantity':'Quantity',
                'order_form_order_item_net':'Net',
                'order_form_order_item_tax':'Tax',
                'admin_title':'Payment Gateway Admin',
                'admin_menu_administrator': 'Administrator',
                'admin_menu_offers': 'Offers',
                'admin_menu_orders': 'Orders',
                'admin_menu_withdraw': 'Withdraw',
                'admin_menu_settings': 'Settings',
                'admin_menu_logout': 'Logout',
                'other_products_you_might_like':'Other Products You Might Like',
             'admin_confirmation_email_subject':'Order #{0} payment confirmation: {1}',
             'order_summary':'Order Summary',
             'subtotal':'SUBTOTAL',
             'loading': 'Loading',
             'login': 'Login',
             'register': 'Register',
             'your_balance_is':'Your balance is:',
             'withdraw_amount':'Withdraw amount',
             'request_withdrawal': 'Request withdrawal',
             'withdrawal_date': 'Date',
             'withdrawal_status': 'Status',
             'withdrawal_amount': 'Amount',
             'withdrawal_processed': 'Processed',
             'withdrawal_pending': 'Pending',
             'iban': 'IBAN',
             'bic': 'BIC',
             'request_taken_successfully':'Your request was taken successfully',
             'not_enough_funds':"You don&#39;t have enough funds",
             'reset_password': 'Reset password',
             'tax':'Tax',
             'shipping':'Shipping',
             'total':'Total',
             'billing_and_shipping':'Billing & Shipping',
             'billing_info':'Billing Info',
             'first_name':'First Name',
             'last_name':'Last Name',
             'address_1':'Address 1',
             'address_2':'Address 2 (optional)',
             'country':'Country',
             'county':'County',
             'city':'City',
             'post_code':'Post Code',
             'email':'Email (required)',
             'email_opt':'Email (optional)',
             'use_above_for_shipping':'Use above info for shipping',
             'shipping_info':'Shipping Info',
             'company':'Company (Optional)',
             'phone':'Phone # (Optional)',
             'subscribe':'Subscribe to receive occasional promotional emails. We will not share your personal information.',
             'payment_options':'Payment options',
             'card_number':'Card number:',
             'expires':'Expires:',
             'name_on_card':'Name on card:',
             'card_code':'Card code:',
             'alternative':'Alternative',
             'pay':'Pay',
             'payment_with_paypal':'payment with PayPal',
             'after_clicking':'After clicking',
             'dont_have_account':"Don&#39;t have a PayPal account?",
             'payment_accepted': 'Your payment has been accepted',
             'quantity':'Qty:',
             'country_au':'Australia',
             'country_at':'Austria',
             'country_be':'Belgium',
             'country_ca':'Canada',
             'country_hr':'Croatia',
             'country_cz':'Czech Republic',
             'country_dk':'Denmark',
             'country_fi':'Finland',
             'country_fr':'France',
             'country_de':'Germany',
             'country_gi':'Gibraltar',
             'country_gb':'Great Britain',
             'country_gr':'Greece',
             'country_gl':'Greenland',
             'country_gg':'Guernsey',
             'country_va':'Holy See (Vatican City State)',
             'country_hk':'Hong Kong',
             'country_hu':'Hungary',
             'country_is':'Iceland',
             'country_ie':'Ireland',
             'country_im':'Isle of Man',
             'country_it':'Italy',
             'country_jp':'Japan',
             'country_je':'Jersey',
             'country_li':'Liechtenstein',
             'country_lt':'Lithuania',
             'country_lu':'Luxembourg',
             'country_nl':'Netherlands',
             'country_nz':'New Zealand',
             'country_no':'Norway',
             'country_pl':'Poland',
             'country_pt':'Portugal',
             'country_ru':'Russian Federation',
             'country_sg':'Singapore',
             'country_sk':'Slovakia (Slovak Republic)',
             'country_za':'South Africa',
             'country_es':'Spain',
             'country_se':'Sweden',
             'country_ch':'Switzerland',
             'country_uk':'United Kingdom',
             'country_us':'United States of America'
            }
        else:
            pass
