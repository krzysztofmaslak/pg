'use strict';

/* Directives */

/* JSHint: declare global variables that JSHint should ignore */
/*global angular:false console:false alert:false */

angular.module('hh.directives', [])

/**
 * Directive which allows an AngularJS-aware 'onblur' handler to be attached to an input element
 */
    .directive('notags', [ function () {
        return {
            require: 'ngModel',
            link: function (scope, elm, attr, ctrl) {
                scope.$watch(attr.ngModel, function (newValue, oldValue) {
                    if (newValue && newValue !== undefined && newValue.match) {
                        if (newValue.match(/<(.|\n)*?>/g)) {
                            ctrl.$setValidity('hasTags', false);
                        } else {
                            ctrl.$setValidity('hasTags', true);
                        }
                    }
                });
            }
        };
    }])
    .directive("inputRequired", function () {
        function isEmpty(value) {
            return typeof value == 'undefined' || value === '' || value === null || value !== value;
        }

        return {
            require: '?ngModel',
            link: function (scope, elm, attr, ctrl) {
                if (!ctrl)
                    return;
                var attr_required = true;
                var validator = function (value) {
                    if (attr_required && (isEmpty(value) || value === false)) {
                        ctrl.$setValidity('required', false);
                        return;
                    } else {
                        ctrl.$setValidity('required', true);
                        return value;
                    }
                };

                ctrl.$formatters.push(validator);
                ctrl.$parsers.unshift(validator);

                attr.$observe('inputRequired', function (value) {
                    attr_required = value === 'true';
                    validator(ctrl.$viewValue);
                });
            }
        };
    })
    .directive("money", function ($filter, $locale) {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, el, attr, ctrl) {
                // format on init
                formatMoney();

                function formatMoney() {
                    var value = ctrl.$modelValue;
                    try {
                        if (value && value !== undefined && value !== null) {
                            value = value + '';
                            var validFloat = parseFloat(value);
                            if (!isNaN(validFloat) && (value.split(".").length - 1) < 2) {
                                ctrl.$setValidity('notANumber', true);
                                // remove all separaters first
                                var groupsep = $locale.NUMBER_FORMATS.GROUP_SEP;
                                var re = new RegExp(groupsep, 'g');
                                value = String(value).replace(re, '');

                                // render
                                ctrl.$viewValue = value;
                                ctrl.$render();
                            } else {
                                ctrl.$setValidity('notANumber', false);
                            }
                        }
                    } catch (e) {
                        ctrl.$setValidity('notANumber', false);
                    }
                };

                // subscribe on changes
                scope.$watch(attr.ngModel, function () {
                    formatMoney();
                });
            }
        };
    })
    .directive('ngModelOnblur', [ '$timeout', function ($timeout) {
        return {
            restrict: 'A',
            priority: 1,
            require: 'ngModel',
            link: function (scope, elem, attr, ngModelCtrl) {
                if (attr.type === 'radio' || attr.type === 'checkbox')
                    return;
                function isEmpty(value) {
                    return typeof value == 'undefined' || value === '' || value === null || value !== value;
                }

                elem.unbind('input').unbind('keydown').unbind('change');
                elem.bind('blur', function () {
                    scope.$apply(function () {
                        var value = elem.val();
                        if (!(isEmpty(ngModelCtrl.$viewValue) && isEmpty(value))) {
                            ngModelCtrl.$used = true;
                            value = value.trim();
                        }
                        ngModelCtrl.$setViewValue(value);
                    });
                });
            }
        };
    }]).directive('selectOnblur', function () {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elem, attr, ngModelCtrl) {
                //apply only to select lists
                if (elem.length < 1 || (elem[0].nodeName && elem[0].nodeName.toUpperCase() !== 'SELECT')) {
                    return;
                }
                function isEmpty(value) {
                    return typeof value == 'undefined' || value === '' || value === null || value !== value;
                }

                var listToUse = [];
                scope.$watch(attr.selectOnblur, function (newVal, oldVal) {
                    listToUse = newVal;
                });

                elem.unbind('change');
                // Android browser doesnt have 'blur' event: it uses mouseleave and mouseenter instead of blur and focus respectively
                var isAndroid = (navigator.userAgent.match(/Android/i) ? true : false);
                var updateEvent = function (event) {
                    scope.$apply(function () {
                        //get the real value from the listToUse based on elem.val() index
                        var index = parseInt(elem.val(), 10);
                        var value = null;
                        if (index >= 0 && index < listToUse.length) {
                            value = listToUse[index].code;
                        }
                        if (!(isEmpty(ngModelCtrl.$viewValue) && isEmpty(value))) {
                            ngModelCtrl.$used = true;
                            if ('blur' == event) {
                                ngModelCtrl.$modified = true;
                            }
                        }
                        ngModelCtrl.$setViewValue(value);
                    });
                };
                elem.bind((isAndroid ? 'mouseleave' : 'blur'), function () {
                    updateEvent('blur')
                });
                elem.bind('change', function () {
                    updateEvent('change')
                });
            }
        };
    })
    .directive('nullifempty', [ function () {
        return {
            require: 'ngModel',
            link: function (scope, elm, attr, ctrl) {
                ctrl.$parsers.unshift(function (value) {
                    return value === '' ? null : value;
                });
            }
        };
    }])
    .directive('imagecheck', function () {
        return function (scope, element, attrs, ctrl) {
            scope.$watch(attrs.imagepresent, function (newValue, oldValue) {
                if (newValue && newValue !== undefined && newValue) {
                    if (window.resourcePresent(attrs.imagecheck)) {
                        jq(element).css('display', 'block');
                        jq(element).attr('src', attrs.imagecheck);
                    }
                }
            });
        };
    })
    .directive('popover', function () {
         return {
             restrict: 'A',
             link: function (scope, elem, attrs) {
                jq(elem).popover({
                    trigger: 'focus',
                    title: attrs.popovertitle
                })
             }
         }
    })
    .directive('fancybox', ['$timeout', function (timer) {
         return {
             restrict: 'A',
             link: function (scope, elem, attrs) {
                var initFancybox = function () {
                    jq('a.productImage').fancybox({
                        'titleShow' : true,
                        'titlePosition' : 'over',
                        'titleFormat' : function(title, currentArray, currentIndex, currentOpts) {
                            return '<span id="fancybox-title-over">Image ' + (currentIndex + 1) + ' / ' + currentArray.length + ' </span>';
                        }
                    });
                }
                timer(initFancybox, 2000);
             }
         }
    }])
    .directive('imageupload', function () {
        return function (scope, element, attrs, ctrl) {
            jq(element).attr('data-url', "/api/image/" + attrs.uploaditemid + '/' + attrs.uploadtarget + '/' + attrs.uploadtargetid);
            jq(element).fileupload({
                dataType: 'json',
                autoUpload: true,
                done: function (e, data) {
                    console.log('done');
                    var thumbnail = jq('.thumbnail', jq(this).parent());
                    thumbnail.css('display', 'block')
                    thumbnail.attr('src', thumbnail.attr('imagecheck'));
                    jq('#thumbnail_remove_'+attrs.uploadtarget+'_'+attrs.uploadtargetid).css('display', 'block');
                }
            });
        };
    })
    .directive('selectRequired', function () {
        return {
            restrict: 'A', //attribute only
            require: 'ngModel',
            link: function (scope, elem, attr, ctrl) {
                //get the regex flags from the regex-validate-flags="" attribute (optional)
                //var flags = attr.regexValidateFlags || 'i';   //case insensitive

                //create the regex obj.
                //var regex = new RegExp(attr.regexValidate, flags);
                function isUndefined(value) {
                    return typeof value == 'undefined';
                }

                function isEmpty(value) {
                    return isUndefined(value) || value === '' || value === null || value !== value;
                }

                if (!ctrl)
                    return;
                var attr_required = true;
                var validator = function (value) {
                    if (attr_required && (isEmpty(value) || value === false)) {
                        ctrl.$setValidity('required', false);
                        return '';
                    } else {
                        ctrl.$setValidity('required', true);
                        return value;
                    }
                };

                ctrl.$formatters.push(validator);
                ctrl.$parsers.unshift(validator);

                attr.$observe('selectRequired', function (value) {
                    attr_required = value === 'true';
                    validator(ctrl.$viewValue);
                });
            }
        };
    })
    .directive('onBlur', function () {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var expression = attrs.onBlur;
                console.log('Linking directive onblur with expression %o for element %o', expression, element);
                element[0].onblur = function () {
                    scope.$eval(expression);
                    scope.$digest();
                };
            }
        };
    })
    .directive('bnLazySrc', [ '$window', '$document', function ($window, $document) {
        return {
            restrict: 'A',
            link: function ($scope, element, attributes) {
                var lazyLoader = (function () {
                    var images = [];
                    var renderTimer = null;
                    var renderDelay = 100;
                    var win = jq($window);
                    var doc = $document;
                    var documentHeight = doc.height();
                    var documentTimer = null;
                    var documentDelay = 2000;
                    var isWatchingWindow = false;

                    function addImage(image) {
                        images.push(image);
                        if (!renderTimer) {
                            startRenderTimer();
                        }
                        if (!isWatchingWindow) {
                            startWatchingWindow();
                        }
                    }

                    function removeImage(image) {
                        for (var i = 0; i < images.length; i++) {
                            if (images[ i ] === image) {
                                images.splice(i, 1);
                                break;
                            }
                        }
                        if (!images.length) {
                            clearRenderTimer();
                            stopWatchingWindow();
                        }
                    }

                    function checkDocumentHeight() {
                        if (renderTimer) {
                            return;
                        }
                        var currentDocumentHeight = doc.height();
                        if (currentDocumentHeight === documentHeight) {
                            return;
                        }
                        documentHeight = currentDocumentHeight;
                        startRenderTimer();
                    }

                    function checkImages() {
                        console.log("Checking for visible images...");
                        var visible = [];
                        var hidden = [];
                        var windowHeight = win.height();
                        var scrollTop = win.scrollTop();
                        var topFoldOffset = scrollTop;
                        var bottomFoldOffset = ( topFoldOffset + windowHeight );
                        for (var i = 0; i < images.length; i++) {
                            var image = images[ i ];
                            if (image.isVisible(topFoldOffset, bottomFoldOffset)) {
                                visible.push(image);
                            } else {
                                hidden.push(image);
                            }
                        }
                        for (var i = 0; i < visible.length; i++) {
                            visible[ i ].render();
                        }
                        images = hidden;
                        clearRenderTimer();
                        if (!images.length) {
                            stopWatchingWindow();
                        }
                    }

                    function clearRenderTimer() {
                        clearTimeout(renderTimer);
                        renderTimer = null;
                    }

                    function startRenderTimer() {
                        renderTimer = setTimeout(checkImages, renderDelay);
                    }

                    function startWatchingWindow() {
                        isWatchingWindow = true;
                        win.on("resize.bnLazySrc", windowChanged);
                        win.on("scroll.bnLazySrc", windowChanged);
                        documentTimer = setInterval(checkDocumentHeight, documentDelay);
                    }

                    function stopWatchingWindow() {
                        isWatchingWindow = false;
                        win.off("resize.bnLazySrc");
                        win.off("scroll.bnLazySrc");
                        clearInterval(documentTimer);
                    }

                    function windowChanged() {
                        if (!renderTimer) {
                            startRenderTimer();
                        }
                    }

                    return({
                        addImage: addImage,
                        removeImage: removeImage
                    });
                })();


                function LazyImage(element) {
                    var source = null;
                    var isRendered = false;
                    var height = null;

                    function isVisible(topFoldOffset, bottomFoldOffset) {
                        if (!element.is(":visible")) {
                            return( false );
                        }
                        if (height === null) {
                            height = element.height();
                        }
                        var top = element.offset().top;
                        var bottom = ( top + height );
                        return(
                            (
                                ( top <= bottomFoldOffset ) &&
                                    ( top >= topFoldOffset )
                                )
                                ||
                                (
                                    ( bottom <= bottomFoldOffset ) &&
                                        ( bottom >= topFoldOffset )
                                    )
                                ||
                                (
                                    ( top <= topFoldOffset ) &&
                                        ( bottom >= bottomFoldOffset )
                                    )
                            );
                    }

                    function render() {
                        isRendered = true;
                        renderSource();
                    }

                    function setSource(newSource) {
                        source = newSource;
                        if (isRendered) {
                            renderSource();
                        }
                    }

                    function renderSource() {
                        element[ 0 ].src = source;
                    }

                    return({
                        isVisible: isVisible,
                        render: render,
                        setSource: setSource
                    });
                }

                var lazyImage = new LazyImage(element);

                // Start watching the image for changes in its
                // visibility.
                lazyLoader.addImage(lazyImage);

                // Since the lazy-src will likely need some sort
                // of string interpolation, we don't want to
                attributes.$observe(
                    "bnLazySrc",
                    function (newSource) {
                        lazyImage.setSource(newSource);
                    }
                );
                $scope.$on(
                    "$destroy",
                    function () {
                        lazyLoader.removeImage(lazyImage);
                    }
                );
            }
        };
    }]);