'use strict';
var notEmpty = function (col) {
    return col !== undefined && col !== null && col.length !== 0;
}
/* Controllers */
/*global console:false angular:false */
/*jslint debug: true, devel: true */

angular.module('hh.controllers', [])
    .controller('PGAppCtrl', ['$scope', '$routeParams', '$rootScope', '$location', function ($scope, $routeParams, $rootScope, $location) {
        $scope.messages = window.messages;
        $rootScope.$safeApply = function ($scope, fn) {
            fn = fn || function () {
            };
            if ($scope.$$phase) {
                //don't worry, the value gets set and AngularJS picks up on it...
                fn();
            }
            else {
                //this will fire to tell angularjs to notice that a change has happened
                //if it is outside of it's own behaviour...
                $scope.$apply(fn);
            }
        };
        $scope.formatDate = function (date) {
            if ( date==undefined )return '';
            if ( date.indexOf('T')!=-1 ) date = date.substring(0, date.indexOf('T'));
            return date;
        };
        $scope.formatPrice = function(price) {
            if ( (price+'').indexOf('.')!==-1 ) {
                price = (price+'').substring(0, (price+'').indexOf('.'))+'.'+(price+'').substring((price+'').indexOf('.')+1, 4);
            }
            if ( (price+'').indexOf('.')!=-1 && (price+'').indexOf('.')==(price+'').length-2 ) {
                price+='0';
            }
            return price;
        };
        $scope.getClientCurrency = function() {
            if ( jq('#clientCurrency').val() && jq('#clientCurrency').val()!='' ) {
                return jq('#clientCurrency').val().toLowerCase();
            } else {
                if ( jq('#clientCountry').val() && jq('#clientCountry').val()!='' ) {
                    if ( jq('#clientCountry').val().toLowerCase()=='au' ) {
                        return 'aud';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='gb' ) {
                        return 'gbp';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='dk' ) {
                        return 'dkk';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='no' ) {
                        return 'nok';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='se' ) {
                        return 'sek';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='us' ) {
                        return 'usd';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='ca' ) {
                        return 'cad';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='ca' ) {
                        return 'cad';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='nz' ) {
                        return 'nzd';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='ch' ) {
                        return 'chf';
                    } else if ( jq('#clientCountry').val().toLowerCase()=='pl' ) {
                        return 'pln';
                    }
                }
                return 'eur';
            }
        };
        $scope.formatCurrency = function(price) {
            if ( $scope.getClientCurrency()=='aud' ) {
                return '$'+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='gbp' ) {
                return '£ '+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='dkk' ) {
                return $scope.formatPrice(price)+' kr';
            } else if ( $scope.getClientCurrency()=='nok' ) {
                return 'kr '+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='sek' ) {
                return $scope.formatPrice(price)+' kr';
            } else if ( $scope.getClientCurrency()=='usd' ) {
                return '$'+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='cad' ) {
                return '$'+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='nzd' ) {
                return '$'+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='chf' ) {
                return 'CHF '+$scope.formatPrice(price);
            } else if ( $scope.getClientCurrency()=='isk' ) {
                return $scope.formatPrice(price)+' kr';
            } else if ( $scope.getClientCurrency()=='pln' ) {
                return $scope.formatPrice(price)+' zł';
            }
            return '€ '+$scope.formatPrice(price);
        };
        $scope.findCurrencyRate = function(code) {
            for(var i=0;i<window.currencies.length;i++) {
                if ( window.currencies[i].code==code ) {
                    return window.currencies[i].rate;
                }
            }
            return 0;
        }
        $scope.convertPrice = function(euroPrice) {
            euroPrice = parseFloat(euroPrice+'');
            if ( $scope.getClientCurrency()=='aud' ) {
                var rate = $scope.findCurrencyRate('aud');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='gbp' ) {
                var rate = $scope.findCurrencyRate('gbp');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='dkk' ) {
                var rate = $scope.findCurrencyRate('dkk');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='nok' ) {
                var rate = $scope.findCurrencyRate('nok');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='sek' ) {
                var rate = $scope.findCurrencyRate('sek');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='usd' ) {
                var rate = $scope.findCurrencyRate('usd');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='cad' ) {
                var rate = $scope.findCurrencyRate('cad');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='nzd' ) {
                var rate = $scope.findCurrencyRate('nzd');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='chf' ) {
                var rate = $scope.findCurrencyRate('chf');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='isk' ) {
                var rate = $scope.findCurrencyRate('isk');
                return rate*euroPrice;
            } else if ( $scope.getClientCurrency()=='pln' ) {
                var rate = $scope.findCurrencyRate('pln');
                return rate*euroPrice;
            }
            return euroPrice;
        }
    }])
    .controller('RegisterCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', 'ValidationService', function ($scope, $routeParams, $location, jaxrs, ValidationService) {
         $scope.register = {};
         $scope.save = function () {
            if ( ValidationService.validate($scope.registerForm) ) {
                jaxrs.create('register/', $scope.register, function (response, status) {
                    if ( status==409 ) {
                        $scope.error_message = response.error_message;
                    } else {
                        $scope.success_message = response.success_message;
                    }
                });
            } else {
                setTimeout(function(){
                    var top = 100000;
                    var first = null;
                    jq(".fieldError").each(function(){
                        if ( jq(this).is(':visible') && jq(this).offset().top<top ) {
                            top = jq(this).offset().top;
                            first = jq(this);
                        }
                    });
                    jq("body,html").animate({scrollTop:top-30}, 'slow');
                    if ( first!=null ) {
                        first.focus();
                    }
                }, 500);
            }
        };
    }])
    .controller('LoginCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', 'ValidationService', function ($scope, $routeParams, $location, jaxrs, ValidationService) {
         $scope.login = {};
         $scope.proceed = function () {
            if ( ValidationService.validate($scope.loginForm) ) {
                jaxrs.create('login/', $scope.login, function (response, status) {
                    if ( status==200 ) {
                        location.href='/admin/';
                    } else {
                        $scope.error_message = response.error_message;
                    }
                });
            } else {
                setTimeout(function(){
                    var top = 100000;
                    var first = null;
                    jq(".fieldError").each(function(){
                        if ( jq(this).is(':visible') && jq(this).offset().top<top ) {
                            top = jq(this).offset().top;
                            first = jq(this);
                        }
                    });
                    jq("body,html").animate({scrollTop:top-30}, 'slow');
                    if ( first!=null ) {
                        first.focus();
                    }
                }, 500);
            }
        };
    }])
    .controller('ResetPasswordCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', 'ValidationService', function ($scope, $routeParams, $location, jaxrs, ValidationService) {
         $scope.reset = {};
         $scope.proceed = function () {
            if ( ValidationService.validate($scope.resetPasswordForm) ) {
                jaxrs.create('password/reset', $scope.reset, function (response, status) {
                    if ( status==204 ) {
                        $scope.error_message = response.error_message;
                    } else {
                        $scope.success_message = response.success_message;
                    }
                });
            } else {
                setTimeout(function(){
                    var top = 100000;
                    var first = null;
                    jq(".fieldError").each(function(){
                        if ( jq(this).is(':visible') && jq(this).offset().top<top ) {
                            top = jq(this).offset().top;
                            first = jq(this);
                        }
                    });
                    jq("body,html").animate({scrollTop:top-30}, 'slow');
                    if ( first!=null ) {
                        first.focus();
                    }
                }, 500);
            }
        };
    }])
    .controller('NewPasswordCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', 'ValidationService', function ($scope, $routeParams, $location, jaxrs, ValidationService) {
         $scope.newpassword = {};
         $scope.proceed = function () {
            if ( ValidationService.validate($scope.newPasswordForm) ) {
                $scope.newpassword.h = window.getParameter('h');
                $scope.newpassword.e = window.getParameter('e');
                jaxrs.create('password/new', $scope.newpassword, function (response, status) {
                    if ( status==400 ) {
                        $scope.error_message = response.error_message;
                    } else if ( status==200 ){
                        location.href='/admin/';
                    }
                });
            } else {
                setTimeout(function(){
                    var top = 100000;
                    var first = null;
                    jq(".fieldError").each(function(){
                        if ( jq(this).is(':visible') && jq(this).offset().top<top ) {
                            top = jq(this).offset().top;
                            first = jq(this);
                        }
                    });
                    jq("body,html").animate({scrollTop:top-30}, 'slow');
                    if ( first!=null ) {
                        first.focus();
                    }
                }, 500);
            }
        };
    }])
    .controller('SettingsCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', function ($scope, $routeParams, $location, jaxrs) {

    }])
    .controller('OrderCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', function ($scope, $routeParams, $location, jaxrs) {
        $scope.orders = [];
        $scope.errors = [];
        $scope.order = null;
        $scope.current = 1;
        jaxrs.query('order/?page=1', null, function (response) {
            $scope.orders = response.orders;
            $scope.pages = Math.ceil(response.count/10);
        });
        $scope.paginatorItemClass = function (page) {
            if ($scope.current == (page + 1)) {
                return 'btn-info';
            } else {
                return 'btn-inverse';
            }
        };
        $scope.previous = function() {
            $scope.current -= 1;
            $scope.go($scope.current);
        };
        $scope.next = function() {
            $scope.current += 1;
            $scope.go($scope.current);
        };
        $scope.go = function(page) {
            $scope.current = page;
            jaxrs.query('order/?page='+$scope.current, null, function (response) {
                $scope.orders = response.orders;
            });
        };
        $scope.show = function(order) {
            $scope.order = order;
            var items = [];
            if ( $scope.order.items ) {
                for ( var i=0;i<$scope.order.items.length;i++) {
                    var item = $scope.order.items[i];
                    if ( item.variations && item.variations.length!==0 ) {
                        for(var j=0;j<item.variations.length;j++) {
                            var variation = item.variations[j];
                            items[items.length] = {title:item.title+'('+variation.title+')', quantity: variation.quantity, net:variation.net, tax:variation.tax};
                        }
                    } else {
                        items[items.length] = {title:item.title, quantity: item.quantity, net:item.net, tax:item.tax};
                    }
                }
                $scope.order.items = items;
            }
        }
    }])
    .controller('OfferCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', 'ValidationService', function ($scope, $routeParams, $location, jaxrs, ValidationService) {
        $scope.offers = [];
        $scope.errors = [];
        $scope.offer = null;
        $scope.current = 1;
        $scope.savedSuccessfully = false;
        jaxrs.query('offer/?page=1', null, function (response) {
            $scope.offers = response.offers;
            $scope.pages = Math.ceil(response.count/10);
        });
        $scope.paginatorItemClass = function (page) {
            if ($scope.current == (page + 1)) {
                return 'btn-info';
            } else {
                return 'btn-inverse';
            }
        };
        $scope.formatDate = function (date) {
            if ( date==undefined )return '';
            if ( date.indexOf('T')!=-1 ) date = date.substring(0, date.indexOf('T'));
            return date;
        };
        $scope.previous = function() {
            $scope.current -= 1;
            $scope.go($scope.current);
        };
        $scope.next = function() {
            $scope.current += 1;
            $scope.go($scope.current);
        };
        $scope.go = function(page) {
            $scope.current = page;
            jaxrs.query('offer/?page='+$scope.current, null, function (response) {
                $scope.offers = response.offers;
            });
        };
        $scope.save = function () {
            if ( ValidationService.validate($scope.offerForm) ) {
                jaxrs.create('offer/', $scope.offer, function (response) {
                    if (response.error != null) {
                        $scope.errors.length = 0;
                        $scope.errors[$scope.errors.length] = {message: response.error};
                    } else {
                        $scope.errors.length = 0;
                        $scope.offer = response;
                        $scope.dirty = false;
                        jaxrs.query('offer/?page='+$scope.current, null, function (response) {
                            $scope.offers = response.offers;
                            $scope.pages = Math.ceil(response.count/10);
                        })
                    }
                });
            }
        };
        $scope.delete = function (id) {
            if (confirm("Are you sure you want to delete")) {
                if ( $scope.offer && $scope.offer.id==id ) {
                    $scope.offer = null;
                }
                jaxrs.remove('offer', id, function (response) {
                    if (response.error != null) {
                        $scope.errors.length = 0;
                        $scope.errors[$scope.errors.length] = {message: response.error};
                    } else {
                        $scope.errors.length = 0;
                        $scope.current = 1;
                        jaxrs.query('offer/?page=1', null, function (response) {
                            $scope.offers = response.offers;
                            $scope.pages = Math.ceil(response.count/10);
                        })
                    }
                });
            }
        };
        $scope.addItem = function() {
            jaxrs.create('offer_item/new', {offer_id:$scope.offer.id}, function (response) {
                if ( !$scope.offer.items || $scope.offer.items.length==0 ) {
                    $scope.offer.items = [];
                }
                $scope.offer.items[$scope.offer.items.length] = {id:response.id};
            });
        };
        $scope.new = function() {
            jaxrs.create('offer/new', {}, function (response) {
                if (response.error != null) {
                    $scope.errors.length = 0;
                    $scope.errors[$scope.errors.length] = {message: response.error};
                } else {
                    $scope.offer = {id:response.id};
                }
            });
        };
        $scope.deleteItem = function(index) {
            $scope.offer.items.splice(index, 1);
        }
        $scope.edit = function(offer) {
            $scope.offer = offer;
        };
    }])
    .controller('ItemCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', '$timeout', 'ValidationService',
        function ($scope, $routeParams, $location, jaxrs, $timeout, ValidationService) {
            if ( $scope.item.id && $scope.item.id>0 ) {
                setTimeout(function(){
                    if ( $scope.item.multivariate && $scope.item.multivariate==1 ) {
                        jq('#multivariate'+$scope.$index).attr('checked', 'checked');
                        $scope.multivariate = 1;
                    } else {
                        jq('#simple'+$scope.$index).attr('checked', 'checked');
                        $scope.multivariate = 0;
                    }
                    $scope.$watch('multivariate', function(newValue, oldValue) {
                        if ( !$scope.item.variations ) $scope.item.variations = [];
                        if ( newValue==1 ) {
                            $scope.item.multivariate = 1;
                            if ( $scope.item.variations.length==0 ) {
                                jaxrs.create('offer_item_variation/new', {offer_item_id:$scope.item.id, count:1}, function (response) {
                                    $scope.item.variations[$scope.item.variations.length] = {placeholder:'eg. red / size 45-47', id:response[0]};
                                });
                            }
                        } else {
                            $scope.item.variations.length = 0;
                            $scope.item.multivariate = 0;
                        }
                    });
                    $scope.$digest();
                }, 500);
            }
            $scope.addVariation = function() {
                jaxrs.create('offer_item_variation/new', {offer_item_id:$scope.item.id, count:1}, function (response) {
                    $scope.item.variations[$scope.item.variations.length] = {placeholder:'eg. red / size 45-47', id:response[0]};
                });
            }
            $scope.deleteVariation = function(index) {
                $scope.item.variations.splice(index, 1);
            }
    }])
    .controller('ItemSelectionCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', '$timeout', 'ValidationService',
        function ($scope, $routeParams, $location, jaxrs, $timeout, ValidationService) {
            $scope.$watch('item.selection', function(newValue, oldValue) {
                $scope.item.quantity = 1;
                if ( $scope.item.variations ) {
                    for(var i=0;i<$scope.item.variations.length;i++) {
                        if ( $scope.item.variations[i].id==$scope.item.selection ) {
                            $scope.item.available = $scope.item.variations[i].available;
                        }
                    }
                }
            });
    }])
    .controller('WithdrawCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', '$timeout', 'ValidationService',
        function ($scope, $routeParams, $location, jaxrs, $timeout, ValidationService) {
            $scope.messages = window.messages;
            $scope.withdrawals = [];
            $scope.balance = window.balance;
            jaxrs.query('withdraw/balance', null, function (response) {
                $scope.balance = response.balance;
                $scope.withdrawals = response.withdrawals;
            });
            $scope.requestWithdrawal = function() {
                if ( ValidationService.validate($scope.withdrawForm) ) {
                    jaxrs.create('/rest/withdraw/request', {amount: $scope.amount, iban: $scope.iban, bic: $scope.bic}, function (response) {
                        $scope.balance = response.balance;
                        $scope.withdrawals = response.withdrawals;
                        $scope.savedSuccessfully = true;
                    });
                }
            }
    }])
    .controller('CheckoutCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', '$timeout', 'ValidationService', 'PaymentService',
        function ($scope, $routeParams, $location, jaxrs, $timeout, ValidationService, PaymentService) {
        $scope.language = window.language;
        $scope.quantity = 1;
        $scope.payment = {month:'', year:''};
        $scope.countries = [{code:'', label:'Country'}];
        $scope.offer = null;
        $scope.quantityMissing = false;
        $scope.paymentAccepted = false;
        $scope.url = $location.absUrl();
        $scope.url = $scope.url.substring($scope.url.lastIndexOf('/x/')+3);
        if ( $scope.url.indexOf('#')!=-1 ) {
            $scope.url = $scope.url.substring(0, $scope.url.indexOf('#'));
        }
        jaxrs.query('offer/'+$scope.url, null, function (response) {
            $scope.offer = response;
            jq('#clientCurrency').val($scope.offer.currency);
            for(var i=0;i<$scope.offer.items.length;i++) {
                var oi = $scope.offer.items[i];
                if ( oi.multivariate ) {
                    if ( !$scope.payment.items ) $scope.payment.items = [];
                    var item = {id:oi.id, title:oi.title, multivariate: true, selection:oi.variations[0].id };
                    for(var j=0;j<oi.variations.length;j++) {
                        if ( !item.variations ) item.variations = [];
                        var oiv = oi.variations[j];
                        if ( oiv.quantity>0 ) {
                            item.variations[item.variations.length] = {id:oiv.id, available:oiv.quantity, title:oiv.title, net:oiv.net, tax:oiv.tax, shipping:oiv.shipping, shipping_additional:oiv.shipping_additional}
                        }
                    }
                    if ( oi.variations[0].quantity>0 ) {
                        item.available = oi.variations[0].quantity;
                        item.quantity = 1;
                        $scope.payment.items[$scope.payment.items.length] = item;
                    }
                } else {
                    if ( !$scope.payment.items ) $scope.payment.items = [];
                    if ( oi.quantity>0 ) {
                        $scope.payment.items[$scope.payment.items.length] = {id:oi.id, available:oi.quantity, title:oi.title, net:oi.net, tax:oi.tax, shipping:oi.shipping, shipping_additional:oi.shipping_additional, quantity:1}
                    }
                }
            }
        });
        for(var i=0;i<window.countries.length;i++) {
            $scope.countries[$scope.countries.length] = {code:window.countries[i].code, label:messages['country_'+window.countries[i].code]};
        }
        $scope.billing = {same_address:true, country:''};
        $scope.shipping = null;
        if ( window.language=='fr' ) {
            $scope.billing.country='fr';
            $scope.shipping.country='fr';
        } else if ( window.language=='de' ) {
            $scope.billing.country='de';
            $scope.shipping.country='fr';
        }
        $scope.$watch('billing.same_address', function(newValue, oldValue) {
            if ( newValue ) {
                $scope.shipping = null;
            } else {
                $scope.shipping = {country:''};
            }
        });
        $scope.expiryyears = [];
        var currentYear = new Date().getFullYear();
        for(i=currentYear;i<currentYear+10;i++) {
            $scope.expiryyears[$scope.expiryyears.length] = {code:(i+'').substring(2), label: i+''};
        }
        $scope.defaultImage = function(item) {
            var img = new Image();
            img.src = '/static/images/offer_item/'+item.id+'_thumb.png';
            if ( img.height != 0 ) {
                return img.src;
            } else {
                if ( item.variations && item.variations.length!=0 ) {
                    for(var i=0;i<item.variations.length;i++) {
                        var img = new Image();
                        img.src = '/static/images/offer_item_variation/'+item.variations[i].id+'_thumb.png';
                        if ( img.height != 0 ) {
                            return img.src
                        }
                    }
                }
                // @TODO handle when there is no image at all
            }
        };
        $scope.subtotalNet = function() {
            var net = 0;
            if ( $scope.payment.items ) {
                for(var i=0;i<$scope.payment.items.length;i++) {
                    if ( $scope.payment.items[i].variations ) {
                        for(var j=0;j<$scope.payment.items[i].variations.length;j++) {
                            if ( $scope.payment.items[i].variations[j].id==$scope.payment.items[i].selection ) {
                                net += ($scope.payment.items[i].quantity*$scope.payment.items[i].variations[j].net);
                            }
                        }
                    } else {
                        net += ($scope.payment.items[i].quantity*$scope.payment.items[i].net);
                    }
                }
            }
            return net;
        };
        $scope.subtotalTax = function() {
            var tax = 0;
            if ( $scope.payment.items ) {
                for(var i=0;i<$scope.payment.items.length;i++) {
                    if ( $scope.payment.items[i].variations ) {
                        for(var j=0;j<$scope.payment.items[i].variations.length;j++) {
                            if ( $scope.payment.items[i].variations[j].id==$scope.payment.items[i].selection ) {
                                tax += ($scope.payment.items[i].quantity*$scope.payment.items[i].variations[j].tax);
                            }
                        }
                    } else {
                        tax += ($scope.payment.items[i].quantity*$scope.payment.items[i].tax);
                    }
                }
            }
            return tax;
        };
        $scope.itemPrice = function(item) {
            var price = 0;
            if (item.variations) {
                for (var j = 0; j < item.variations.length; j++) {
                    if (item.variations[j].id==item.selection) {
                        price += (item.quantity * (item.variations[j].net + item.variations[j].tax));
                    }
                }
            } else {
                price += (item.quantity * (item.net + item.tax));
            }
            return price;
        }
        $scope.shippingCost = function() {
            var shipping = 0;
            if ( $scope.payment.items ) {
                for (var i = 0; i < $scope.payment.items.length; i++) {
                    if ($scope.payment.items[i].variations) {
                        for (var j = 0; j < $scope.payment.items[i].variations.length; j++) {
                            if ($scope.payment.items[i].variations[j].id==$scope.payment.items[i].selection && $scope.payment.items[i].quantity > 0) {
                                shipping += $scope.payment.items[i].variations[j].shipping;
                                if ($scope.payment.items[i].quantity>1 ) {
                                    for (var q = 1; q < $scope.payment.items[i].quantity; q++) {
                                        if ( $scope.payment.items[i].variations[j].shipping_additional ) {
                                            shipping += $scope.payment.items[i].variations[j].shipping_additional;
                                        } else {
                                            shipping += $scope.payment.items[i].variations[j].shipping;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ($scope.payment.items[i].quantity > 0) {
                        shipping += $scope.payment.items[i].shipping;
                        if ($scope.payment.items[i].quantity > 1) {
                            for (var q = 1; q < $scope.payment.items[i].quantity; q++) {
                                if ( $scope.payment.items[i].shipping_additional ) {
                                    shipping += $scope.payment.items[i].shipping_additional;
                                } else {
                                    shipping += $scope.payment.items[i].shipping;
                                }
                            }
                        }
                    }
                }
            }
            return shipping;
        };
        $scope.total = function() {
            return $scope.subtotalNet()+$scope.subtotalTax()+$scope.shippingCost();
        };
        $scope.decreaseItemQuantity = function(item) {
            item.quantity = item.quantity - 1;
        };
        $scope.increaseItemQuantity = function(item) {
            $scope.quantityMissing = false;
            item.quantity = item.quantity + 1;
        };
        $scope.paypaylPayment = function(orderId) {
            jq('#order_id').val(orderId);
            document.paymentForm.submit();
        };
        $scope.stripePayment = function(order_id) {
            var $form = jq('#checkoutPaymentForm');

            // Disable the submit button to prevent repeated clicks
            jq('#ccPayment').prop('disabled', true);

            var stripeResponseHandler = function(status, response) {
                if (response.error) {
                    hideLoadingIndicator();
                    jq('#ccPayment').attr('disabled', false);
                    jq('#ccPaymentWait').html('');
                    // Show the errors on the form
                    $form.find('.payment-errors').text(response.error.message);
                    jq('#ccPayment').prop('disabled', false);
                    // @TODO log errors to the server
                    //window.common.logError({location:'checkout_step5', description:'payment failure', message:response.error.message});
                } else {
                    var token = function(res){
                        var jsonStr = '';
                        try {
                            jsonStr = JSON.stringify({stripe_token:res.id, order_id:order_id});
                        } catch(e) {
                            jsonStr = jq.toJSON({stripe_token:res.id, order_id:order_id});
                        }
                        jq.ajax({
                            type: "POST",
                            url: '/rest/stripe/process',
                            data: jsonStr,
                            contentType:"application/json; charset=utf-8",
                            dataType:"json",
                            success: function(response) {
                                jq('#ccPayment').attr('disabled', false);
                                jq('#ccPaymentWait').html('');
                                $scope.paymentAccepted = true;
                                $scope.$digest();
                                jq("body,html").animate({scrollTop:50}, 'slow');
                                hideLoadingIndicator();
                            },
                            error: function(response) {
                                jq('#stripeChoosePayment').click(function(event){
                                    jq('#stripePaymentFailedPanel').slideUp('slow');
                                    jq('#paymentSelectionPanel').slideDown('slow');
                                    event.preventDefault();
                                    return false;
                                });
                                jq('#stripePaymentRetry').click(function(event){
                                    jq('#stripePaymentFailedPanel').slideUp('slow');
                                    jq('#paymentSelectionPanel').slideDown('slow');
                                    makeStripePayment();
                                    event.preventDefault();
                                    return false;
                                });
                                jq('#paymentSelectionPanel').slideUp('slow');
                                jq('#stripePaymentFailedPanel').slideDown('slow');
                                jq('#stripePaymentFailedPanel').addClass('error');
                            }
                        });
                    };
                    token(response);
                }
            };
            Stripe.createToken($form, stripeResponseHandler);
        }
        $scope.$on('PaymentService:service-success', function(event, payment) {
            if ( payment.payment_method=='cc' ) {
                $scope.stripePayment(payment.order_id);
            } else {
                $scope.paypaylPayment(payment.order_id);
            }
        });
        $scope.$on('PaymentService:service-failure', function(event) {
            hideLoadingIndicator();
            jq('#ccPayment').attr('disabled', false);
            jq('#ccPaymentWait').html('');
        });
        $scope.pay = function(event, method) {
            var paymentFormValid = false;
            if ( method==='cc' && ValidationService.validate($scope.checkoutPaymentForm)) {
                paymentFormValid = true;
            }
            if ( ValidationService.validate($scope.checkoutDetailsForm) && (method!=='cc' || paymentFormValid) && $scope.total()>0 ) {
                jq('#ccPayment').attr('disabled', true);
                jq('#ccPaymentWait').html('<span class="wait">&nbsp;<img src="/static/${pom.version}/img/loading.gif" alt="" /></span>');
                showLoadingIndicator();
                PaymentService.makePayment({
                    offer_id: $scope.offer.id,
                    lang: window.language,
                    subscribe: $scope.subscribe,
                    items: $scope.payment.items,
                    billing: $scope.billing,
                    shipping: $scope.shipping,
                    payment_method: method,
                    currency: jq('#clientCurrency').val(),
                    country: window.client_country
                });
            } else {
                if ( $scope.total()<=0 ) {
                    $scope.quantityMissing = true;
                }
                setTimeout(function(){
                    var top = 100000;
                    var first = null;
                    jq(".fieldError").each(function(){
                        if ( jq(this).is(':visible') && jq(this).offset().top<top ) {
                            top = jq(this).offset().top;
                            first = jq(this);
                        }
                    });
                    jq("body,html").animate({scrollTop:top-30}, 'slow');
                    if ( first!=null ) {
                        first.focus();
                    }
                }, 500);
            }
        }
    }])
    .controller('ProductListCtrl', ['$scope', '$routeParams', '$location', 'jaxrs', function ($scope, $routeParams, $location, jaxrs) {

    }]);

