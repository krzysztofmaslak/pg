'use strict';
/* JSHint: declare global variables that JSHint should ignore */
/*global angular:false, HHAppCtrl:false, ErrorCtrl:false, MyCtrl1:false, MyCtrl2:false, PaymentCtrl:false */
// Declare app level module which depends on filters, directives and services
String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
String.prototype.replaceAll = function( token, newToken, ignoreCase ) {
    var _token;
    var str = this + "";
    var i = -1;

    if ( typeof token === "string" ) {

        if ( ignoreCase ) {

            _token = token.toLowerCase();

            while( (
                i = str.toLowerCase().indexOf(
                    token, i >= 0 ? i + newToken.length : 0
                ) ) !== -1
            ) {
                str = str.substring( 0, i ) +
                    newToken +
                    str.substring( i + token.length );
            }

        } else {
            return this.split( token ).join( newToken );
        }

    }
    return str;
};
window.showLoadingIndicator = function() {
    jq('#loadingIndicator').css('display', 'block');
    jq('#loadingIndicator').addClass('hover');
}
window.hideLoadingIndicator = function() {
    jq('#loadingIndicator').css('display', 'none');
    jq('#loadingIndicator').removeClass('hover');
}
window.clickOnParentSibling = function(element, nodeType) {
    if ( element.childNodes && element.childNodes.length!=0 ) {
        for(var i=0;i<element.childNodes.length;i++) {
            if ( element.childNodes[i].nodeName.toLowerCase()==nodeType ) {
                element.childNodes[i].click();
                return false;
            }
        }
    }
    if ( element.parentNode!=null ) {
        return clickOnParentSibling(element.parentNode, nodeType)
    }
}
angular.module('pgadminapp', ['ngRoute', 'hh.filters', 'hh.services', 'hh.directives', 'hh.controllers', 'LoadingModule', 'ui.bootstrap.modal']).
	config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/landing',      {templateUrl: '/static/${pom.version}/partials/admin/landing.html'});
        $routeProvider.when('/offers',      {templateUrl: '/static/${pom.version}/partials/admin/offer.html'});
        $routeProvider.when('/orders',      {templateUrl: '/static/${pom.version}/partials/admin/order.html'});
        $routeProvider.when('/withdraw',      {templateUrl: '/static/${pom.version}/partials/admin/withdraw.html'});
        $routeProvider.when('/settings',      {templateUrl: '/static/${pom.version}/partials/admin/settings.html'});
        $routeProvider.otherwise({redirectTo: '/landing'});
	}]);
angular.module('pgapp', ['ngRoute', 'hh.filters', 'hh.services', 'hh.directives', 'hh.controllers', 'ui.bootstrap.modal']).
    config(['$routeProvider', '$sceProvider', function($routeProvider, $sceProvider) {
        $routeProvider.when('/checkout',      {templateUrl: '/static/${pom.version}/partials/checkout.html'});
        $routeProvider.otherwise({redirectTo: '/checkout'});
        $sceProvider.enabled(false);
    }]);