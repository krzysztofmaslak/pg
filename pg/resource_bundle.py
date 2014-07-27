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
                'register_account_name':'Account name',
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
                'offer_preview':'Preview',
                'offer_your_basket_is_empty':'Your basket is empty.',
                'offer_add_to_basket':'Add to basket',
                'offer_saved_successfully':'Offer saved successfully',
                'offer_list_delete_confirm':'Are you sure you want to delete selected offer ?',
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
                'order_list_refund':'Refund',
                'order_list_refund_confirm':'Are you sure you want to refund selected payment ?',
                'order_list_number':'Order number',
                'order_list_date':'Date',
                'order_list_total':'Total',
                'order_list_fee':'Fee',
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
                'order_confirmation':'Order confirmation',
                'admin_title':'Payment Gateway Admin',
                'admin_menu_administrator': 'Administrator',
                'admin_menu_offers': 'Offers',
                'admin_menu_orders': 'Orders',
                'admin_menu_withdraw': 'Withdraw',
                'admin_menu_traffic':'Traffic',
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
        elif lang=='fr':
            return {
                'contact_message_success':'Votre message a été acceptée, nous vous répondrons sous peu',
                'contact_title':'Envoyez-nous un message',
                'contact_email':'Email',
                'contact_email_placeholder':'Email',
                'contact_message':'Message',
                'contact_btn':'Envoyer',
                'need_an_account':'Besoin d&#39;un compte?',
                'contact':'Contacter',
                'copy_to_clipboard':'Copier au presse-papiers',
                'checkout_product_title':'Titre du produit',
                'checkout_delete_product':'Supprimer produit',
                'already_a_member':'Déjà inscrit ?',
                'you_are_no_longer_logged_in':'Vous n&#39;êtes plus connecté',
                'new_password_title':'Réinitialiser le mot de passe',
                'new_password_password':'Mot de passe',
                'new_password_placeholder':'Mot de passe',
                'new_password_confirm_password':'Confirmez le mot de passe',
                'new_password_confirm_password_placeholder':'Confirmez le mot de passe',
                'new_password_btn':'Réinitialiser le mot de passe',
                'new_password_mismatch':'S&#39;il vous plaît retapez votre mot de passe',
                'registration_email_subject':'S&#39;inscrire email',
                'login_title':'Se connecter',
                'login_username':'Email',
                'login_username_placeholder':'Email',
                'login_password':'Mot de passe',
                'login_password_placeholder': 'Mot de passe',
                'login_btn':'Valider',
                'login_remind_me_my_password':'Mot de passe oublié ?',
                'login_wrong_username_or_password':'Votre identifiant ou mot de passe est incorrect.',
                'login_user_inactive':'L&#39;utilisateur est inactif, vérifiez dans votre boîte aux lettres pour les instructions pour terminer le processus d&#39;inscription',
                'register_account_name':'Nom de la société',
                'register_title':'S&#39;inscrire',
                'register_username':'Email',
                'register_username_placeholder':'Email',
                'register_password':'Mot de passe',
                'register_password_placeholder':'Mot de passe',
                'register_user_already_exist':'Vous avez déjà créé un Compte avec cette adresse e-mail. Merci de saisir une adresse différente.',
                'register_success':'Pour activer votre Compte, veuillez cliquer sur le lien figurant dans l&#39;email de confirmation que nous venons de vous adresser.',
                'reset_password_title':'Récupérer votre mot de passe',
                'reset_password_username':'Email',
                'reset_password_placeholder':'Email',
                'reset_password_btn':'Valider',
                'reset_password_link_info':'Un email vient de vous être envoyé. Vous y trouverez les informations pour modifier votre mot de passe.',
                'reset_password_no_email':'Nous n&#39;avons pas pu trouver compte avec cette adresse email.',
                'register_btn':'S&#39;inscrire',
                'offer_preview':'Avant-première',
                'offer_your_basket_is_empty':'Votre panier est vide.',
                'offer_add_to_basket':'Ajouter au panier',
                'offer_saved_successfully':'Offre enregistré avec succès',
                'offer_list_delete_confirm':'Etes-vous sûr de vouloir supprimer offre choisie?',
                'offer_list_title': 'Titre',
                'offer_list_creation_date': 'Date de création',
                'offer_list_edit': 'Modifier',
                'offer_list_delete': 'Effacer',
                'offer_list_next': 'Suivant',
                'offer_list_previous': 'Précédent',
                'offer_list_add_new_offer': 'Ajouter une nouvelle offre',
                'offer_form_title': 'Titre de l&#39;Offre',
                'offer_form_creation_date': 'Date de création',
                'offer_form_direct_link': 'Lien direct',
                'offer_form_products': 'Produits',
                'offer_form_multiple_variations': 'Variations multiples',
                'offer_form_multiple_variations_no': 'Aucun',
                'offer_form_multiple_variations_yes': 'Oui',
                'offer_form_quantity': 'Quantité',
                'offer_form_net': 'Net',
                'offer_form_tax': 'Impôt',
                'offer_form_shipping': 'Livraison',
                'offer_form_shipping_additional':'Frais de port supplémentaires',
                'offer_form_delete_variation': 'Aupprimer variation',
                'offer_form_add_more_variations':'Ajouter plus de variations',
                'offer_form_photos': 'Photos',
                'offer_form_currency':'Monnaie',
                'offer_form_add_product':'Ajouter le produit',
                'offer_form_save_offer':'Enregistrer offre',
                'offer_form_please_select':'--S&#39;il vous plaît sélectionnez--',
                'offer_form_variation': 'Variation',
                'order_saved_successfully':'Les données sauvegardées avec succès',
                'order_list_refund':'Rembourse',
                'order_list_refund_confirm':'Etes-vous sûr de vouloir rembourser le paiement sélectionné?',
                'order_list_number':'Numéro de commande',
                'order_list_date':'Date',
                'order_list_total':'Total',
                'order_list_fee':'Frais',
                'order_list_show':'Montrer',
                'order_list_previous':'Précédent',
                'order_list_next':'Suivant',
                'order_list_no_orders':'Il n&#39;y a pas de commandes',
                'order_form_number':'Numéro de commande',
                'order_form_total':'Total',
                'order_form_first_name':'Prénom',
                'order_form_last_name':'Nom de famille',
                'order_form_email':'Email',
                'order_form_address1':'Adresse1',
                'order_form_address2':'Adresse2',
                'order_form_county':'Région',
                'order_form_postal_code': 'Code Postal',
                'order_form_country':'Pays',
                'order_form_city':'Ville',
                'order_form_company':'Entreprise',
                'order_form_phone_number':'Numéro de téléphone',
                'order_form_order_item_title':'Titre',
                'order_form_order_item_quantity':'Quantité',
                'order_form_order_item_net':'Net',
                'order_form_order_item_tax':'Impôt',
                'order_confirmation':'Confirmation de commande',
                'admin_title':'Passerelle de paiement d&#39;administration',
                'admin_menu_administrator': 'Administrateur',
                'admin_menu_offers': 'Offres',
                'admin_menu_orders': 'Orders',
                'admin_menu_withdraw': 'Retirer',
                'admin_menu_traffic':'Commerce',
                'admin_menu_settings': 'Paramètres',
                'admin_menu_logout': 'Déconnexion',
                'other_products_you_might_like':'Autres produits qui pourraient vous intéresser',
             'admin_confirmation_email_subject':'Commande # {0} confirmation de paiement: {1}',
             'order_summary':'Résumé de la commande',
             'subtotal':'SUBTOTAL',
             'loading': 'Chargement',
             'login': 'Se connecter',
             'register': 'S&#39;inscrire',
             'your_balance_is':'Votre solde est:',
             'withdraw_amount':'Retirer montant',
             'request_withdrawal': 'Demande de retrait',
             'withdrawal_date': 'Date',
             'withdrawal_status': 'Statut',
             'withdrawal_amount': 'Montant',
             'withdrawal_processed': 'Traité',
             'withdrawal_pending': 'En attendant',
             'iban': 'IBAN',
             'bic': 'BIC',
             'request_taken_successfully':'Votre demande a été prise avec succès',
             'not_enough_funds':"Vous n&#39;avez pas assez de fonds",
             'reset_password': 'Réinitialiser le mot de passe',
             'tax':'Tax',
             'shipping':'Livraison',
             'total':'Total',
             'billing_and_shipping':'Facturation et Expédition',
             'billing_info':'Renseignements de facturation',
             'first_name':'Prénom',
             'last_name':'Nom de famille',
             'address_1':'Adresse 1',
             'address_2':'Adresse 2 (en option)',
             'country':'Pays',
             'county':'Région',
             'city':'Ville',
             'post_code':'Code postal',
             'email':'Email (requis)',
             'email_opt':'Email (en option)',
             'use_above_for_shipping':'Utilisez dessus de l&#39;information pour l&#39;expédition',
             'shipping_info':'Expédition',
             'company':'Entreprise (en option)',
             'phone':'Numéro de téléphone # (en option)',
             'subscribe':'Abonnez-vous à recevoir des courriels promotionnels occasionnels. Nous ne communiquerons pas vos renseignements personnels.',
             'payment_options':'Options de paiement',
             'card_number':'Numéro de la carte:',
             'expires':'Expire:',
             'name_on_card':'Nom sur la carte:',
             'card_code':'Code de la carte:',
             'alternative':'Alternative',
             'pay':'Payer',
             'payment_with_paypal':'paiement avec PayPal',
             'after_clicking':'après avoir cliqué sur',
             'dont_have_account':"Ne pas avoir un compte PayPal?",
             'payment_accepted': 'Votre paiement a été accepté',
             'quantity':'Quantité:',
             'country_au':'Australie',
             'country_at':'Autriche',
             'country_be':'Belgique',
             'country_ca':'Canada',
             'country_hr':'Croatie',
             'country_cz':'République tchèque',
             'country_dk':'Danemark',
             'country_fi':'Finlande',
             'country_fr':'France',
             'country_de':'Allemagne',
             'country_gi':'Gibraltar',
             'country_gb':'Grande-Bretagne',
             'country_gr':'Grèce',
             'country_gl':'Groenland',
             'country_gg':'Guernesey',
             'country_va':'Saint-Siège (Vatican)',
             'country_hk':'Hong Kong',
             'country_hu':'Hongrie',
             'country_is':'Islande',
             'country_ie':'Irlande',
             'country_im':'Ile de Man',
             'country_it':'Italie',
             'country_jp':'Japon',
             'country_je':'Jersey',
             'country_li':'Liechtenstein',
             'country_lt':'Lituanie',
             'country_lu':'Luxembourg',
             'country_nl':'Pays-Bas',
             'country_nz':'Nouvelle-Zélande',
             'country_no':'Norvège',
             'country_pl':'Pologne',
             'country_pt':'Portugal',
             'country_ru':'Fédération de Russie',
             'country_sg':'Singapour',
             'country_sk':'Slovaquie (République slovaque)',
             'country_za':'Afrique du Sud',
             'country_es':'Espagne',
             'country_se':'Suède',
             'country_ch':'Suisse',
             'country_uk':'Royaume-Uni',
             'country_us':'États-Unis d&#39;Amérique'
            }
        else:
            pass
