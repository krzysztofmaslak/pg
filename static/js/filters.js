'use strict';

/* Filters */

/* JSHint: declare global variables that JSHint should ignore */
/*global angular:false */

angular.module('hh.filters', []).
    filter('nothidden', function() {
        return function(product) {
            if ( product.length>1 ) {
                var array = [];
                for(var i=0;i<product.length;i++) {
                    if ( product[i].hidden===undefined || product[i].hidden!==true ) {
                        array[array.length] = product[i];
                    }
                }
                return array;
            } else {
                if ( product.hidden===undefined || product.hidden!==true ) {
                    return product;
                } else {
                    return null;
                }
            }
        };
    })
    .filter('applicableForSupplier', function() {
        return function(items, supplierId){

            var arrayToReturn = [];
            for (var i=0; i<items.length; i++){
                if ( supplierId==null || supplierId=='' ) {
                    if ( items[i].supplierId==null )arrayToReturn.push(items[i]);
                } else if (items[i].supplierId==null || items[i].supplierId==supplierId) {
                    arrayToReturn.push(items[i]);
                }
            }

            return arrayToReturn;
        };
    })
    .filter('applicableForAge', function() {
        return function(items, age){
            var arrayToReturn = [];
            if ( items ) {
                for (var i=0; i<items.length; i++){
                    if (items[i].age==age) {
                        arrayToReturn.push(items[i]);
                    }
                }
            }
            return arrayToReturn;
        };
    })
    .filter('range', function() {
        return function(input, total) {
            total = parseInt(total);
            for (var i=1; i<=total; i++)
                input.push(i);
            return input;
        };
    })
    .filter('address', function() {
		function concat(result, value) {
			result = result || '';
			if (value !== null) {
				if (result !== '') {
					result += ', ' + value;
				}
				else {
					result += value;
				}
			}
			return result;
		}

		return function(address) {
			var lines = [];
			if (address.addressLine1 && address.addressLine1.replace(/^\s+|\s+$/g, '')) lines.push(address.addressLine1);
			if (address.addressLine2 && address.addressLine2.replace(/^\s+|\s+$/g, '')) lines.push(address.addressLine2);
			if (address.addressLine3 && address.addressLine3.replace(/^\s+|\s+$/g, '')) lines.push(address.addressLine3);

			return lines.join(', ');//.replace(/, ,/g , ',');
		};
	});
