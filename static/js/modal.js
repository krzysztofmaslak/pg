// Angular UI  , Warning this is not the official version. It is customized. -maxisam
angular.module('ui.bootstrap.modal', []).directive('modal', ['$parse', function ($parse) {

    var body = angular.element(document.getElementsByTagName('body')[0]);
    var defaultOpts = {
        backdrop: true,
        escape: true
    };
    return {
        restrict: 'ECA',
        link: function (scope, elm, attrs) {
            var backdropEl;
            var opts = angular.extend(defaultOpts, scope.$eval(attrs.uiOptions || attrs.bsOptions || attrs.options));
            var shownExpr = attrs.modal || attrs.show;
            var setClosed;
            if (attrs.close) {
                setClosed = function () {
                    scope.$apply(attrs.close);
                };
            } else {
                setClosed = function () {
                    scope.$apply(function () {
                        $parse(shownExpr).assign(scope, false);
                    });
                };
            }
            elm.addClass('modal');
            if (opts.backdrop && !backdropEl) {
                backdropEl = angular.element('<div class="modal-backdrop ngModal"></div>');
                backdropEl.css('display', 'none');
                elm.parent().append(backdropEl);
            }
            function setSize(scope, elm, width, height) {

                var footerH = jq(elm).find('.modal-footer').outerHeight();
                width && elm.css({ 'width': width + 'px', 'margin-left': (-width / 2) + 'px' });
                height && elm.css({ 'height': height + 'px', 'margin-top': (-height / 2) + 'px' });
                //console.log(headerFooterH);

                height && scope.$watch(function (s) {
                    return elm.find('.modal-header').height();
                }, function (newVal) {
                    elm.find('.modal-body').css({
                        'height': function () {
                            return (height - footerH - jq(elm).find('.modal-header').outerHeight(true) - 30) + 'px';
                        }
                    });
                }, true);
                height || scope.$watch(function (s) {
                    return elm.height();
                }, function (newVal) {
                    elm.css({
                        'margin-top': function () {
                            return (-newVal / 2) + 'px';
                        }
                    });
                }, true);

            }
            function setShown(shown) {
                scope.$apply(function () {
                    model.assign(scope, shown);
                });
            }

            function escapeClose(evt) {
                if (evt.which === 27) { setClosed(); }
            }
            function clickClose() {
                setClosed();
            }

            function close() {
                if (opts.escape) { body.unbind('keyup', escapeClose); }
                if (opts.backdrop) {
                    backdropEl.css('display', 'none').removeClass('in');
                    backdropEl.unbind('click', clickClose);
                }
                elm.css('display', 'none').removeClass('in');
                body.removeClass('modal-open');
            }
            function open() {
                if (opts.escape) { body.bind('keyup', escapeClose); }

                if (opts.backdrop) {
                    backdropEl.css('display', 'block').addClass('in');
                    backdropEl.bind('click', clickClose);
                }
                elm.css('display', 'block').addClass('in');
                body.addClass('modal-open');
                setSize(scope, elm, attrs.width, attrs.height);
            }
            scope.$watch(shownExpr, function (isShown, oldShown) {
                if (isShown) {
                    open();
                } else {
                    close();
                }
            });
        }
    };
}]);