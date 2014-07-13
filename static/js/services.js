'use strict';

/* Services */

/* JSHint: declare global variables that JSHint should ignore */
/*global angular:false console:false */
/*jslint devel: true */
angular.module('hh.services', [])
/**
 * Service for retrieving/caching arrays of names/values for select lists.
 */
.factory('PaymentService', ['$http', '$rootScope', function($http, $rootScope) {

        return {
            /**
             * Retrieves the named list (from '/hh2j/rest/items/{listName}'), and stores the retrieved array of values
             * in the scope under scopeProperty (ie: 'scope[scopeProperty]').
             *
             * @listName the name of the list, eg: 'property'. This will be used to build the REST URL
             * @targetObj the target object in which the retrieved list of values will be stored
             * @property the property name under which to set the list on the target object
             */
            makePayment: function(payment) {
                var self = this;
                $http.post('/rest/payment/', payment, { timeout:600000 })
                    .success(function(response) {
                        payment.order_id = response.id;
                        $rootScope.$broadcast('PaymentService:service-success', payment);
                    })
                    .error(function(response, status) {
                        if ( status==403 ) {
                            location.reload();
                            return;
                        }
                        $rootScope.$broadcast('PaymentService:service-failure');
                    });
            }
        };
    }])
.factory('ErrorService',[function(){
	//service to assign server-generated errors for fields in a form
	//forms come from controllers and have the following format: formName.inputElement.$error.problemcategory - boolean
	//var forms={};
	return{
		//registerForm:function(form){
		//	forms[form.$name] = form;
		//},
		clearForm:function(form){
			for(var prop in form){
				if("$error" in prop){
					for(var category in prop.$error){
						delete prop.category;
					}
				}
			}
		},
		processErrors:function(form, errors){
			//errors: array of property:category
			for(var field in errors){
				if(field in form){
					form[field].$error[errors[field]] = true;
				}
			}
		}
	};
}])
.factory('ValidationService',[function(){
        return{
            validate:function(form){
                var valid = true;
                for(var k in form){
                    if (k.endsWith('Form') ) {
                        if ( !this.validate(form[k]) ) {
                            valid = false
                        }
                    } else {
                        if(k!=undefined && form[k].$invalid){
                            form[k].$dirty = true;
                            valid = false;
                        }
                    }
                }
                return valid;
            },
            clearErrors:function(form) {
                for(var k in form){
                    form[k].$invalid = false;
                    form[k].$valid = true;
                    form[k].$dirty = false;
                    if ( form[k].$error!=null && form[k].$error!=undefined)form[k].$error.required = false;
                }
            }
        };
}])
.factory('jaxrs', ['$rootScope', '$http', function($rootScope, $http) {
    return {
        //Create a db object on server
        create: function(className, data, callback) {
            $http.post(
                '/rest/'+className,
                data,
                {  timeout:600000 }
            )
                .success(function(response, status) {
                    callback(response, status);
                })
                .error(function(response, status) {
                    if ( status==403 ) {
                        location.reload();
                        return;
                    }
                    callback(response, status);
                });
        },
        //Get a db object by id
        get: function(className, objectId, callback) {

            $http.get(
                '/rest/'+className+'/'+objectId,
                {  timeout:600000 }
            ).success(function(response) {
                    $rootScope.$apply(function() { callback(null, response); });
                }).error(function(response, status) {
                    if ( status==403 ) {
                        location.reload();
                        return;
                    }
                    $rootScope.$apply(function() { callback(response.error || "Cannot get object "+className+"/"+objectId+"!"); });
                });
        },
        //Get a list of db objects with query
        query: function(className, query, callback) {
            var config = {  timeout:600000 };
            if (query) config.params = { where: query };
            $http.get(
                    '/rest/'+className,
                    config
                ).success(function(response) {
                    callback(response);
                }).error(function(response, status) {
                    if ( status==403 ) {
                        location.reload();
                        return;
                    }
                    callback(response);
                });
        },
        //Remove a db object
        remove: function(className, objectId, callback) {
            var config = {  timeout:600000 };
            $http.delete(
                    '/rest/'+className+'/'+objectId,
                config
            ).success(function(response) {
                    callback(response);
                    }).error(function(response, status) {
                    if ( status==403 ) {
                        location.reload();
                        return;
                    }
                    callback(response);
                    });
        }
        };
}]);