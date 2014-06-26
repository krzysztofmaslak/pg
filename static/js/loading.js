angular.module('LoadingModule', ['ui.bootstrap.modal'])
    .config(function ($httpProvider) {
        $httpProvider.responseInterceptors.push('onCompleteInterceptor');
    })
    .factory('onCompleteInterceptor', function ($q, $window, LoadingSrv) {
        return function (promise) {
            return promise.then(function (response) {
                // do something on success
                LoadingSrv.requestCount--;
                return response;

            }, function (response) {
                // do something on error
                LoadingSrv.requestCount--;
                return $q.reject(response);
            });
        };
    })
    .service('onStartInterceptor', function (LoadingSrv) {
        this.startSending = function (data, headersGetter) {
            LoadingSrv.requestCount++;
            return data;
        };
    })
    .factory('LoadingSrv', function () {
        return {
            requestCount: 0,
            isLoadingShown: function () {
                return this.requestCount > 0;
            }
        };
    })
    .run(function ($http, onStartInterceptor) {
        $http.defaults.transformRequest.push(onStartInterceptor.startSending);
    })
    .directive('loading', function (LoadingSrv) {
        return {
            restrict: 'A',
            replace: true,
            template: '<div modal width="250" height="140" show="isshown" options="options" id="Loading"><div class="modal-body">Loading</div></div>',
            controller: function ($scope, $element, $attrs, LoadingSrv) {
                $scope.$watch(function () { return LoadingSrv.requestCount; }, function (newVal) {
                    $scope.isshown = LoadingSrv.isLoadingShown();
                }, true);
                $scope.options = {
                    backdrop: true,
                    escape: false
                };
            }
        };
    });
