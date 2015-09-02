var app = angular.module('DashboardApp', [
    'ui.router',
    'ngResource',
    'angularMoment',
    'angular-loading-bar',
    'daterangepicker',
    'smart-table',
    'chart.js',
])


app.config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/html/partials/_job_list.html",
            controller: "DashboardController"
        })
})


app.controller("DashboardController", [
    '$scope',
    '$q',
    '$filter',
    '$location',
    'DashboardService',
    function ($scope, $q, $filter, $location, DashboardService) {

        $scope.full_cat_list = [];
        $scope.cat_list = [];

        $('.date-picker').on('apply.daterangepicker', function(ev, picker) {
            if (picker.startDate.format('YYYY-MM-DD') != $location.search().date_from || picker.endDate.format('YYYY-MM-DD') != $location.search().date_to) {
                $location.search('date_from', picker.startDate.format('YYYY-MM-DD'));
                $location.search('date_to', picker.endDate.format('YYYY-MM-DD'));
            }
        });

        // watch for GET changes
        $scope.$watch(function(){ return $location.search() }, function(){
          query_data($location.search().date_from, $location.search().date_to);
        }, true);

        var query_data = function (date_from, date_to) {
            DashboardService.query(date_from, date_to).then(function success (data) {
                //$scope.data = data;
                $scope.gender_data = {
                    'labels': ['Male', 'Female', 'Unspecified'],
                    'data': [data.gender.male, data.gender.female, data.gender.unspecified],
                }
                $scope.desexedgender_data = {
                    'labels': ['Male', 'Female', 'Unspecified'],
                    'data': [data.gender.desexed.male, data.gender.desexed.female, data.gender.desexed.unspecified],
                }
                angular.copy(data.cats, $scope.full_cat_list)
                angular.copy(data.cats, $scope.cat_list)

                // Actions
                $scope.actions = {
                    'labels': Object.keys(data.actions),
                    'series': Object.keys(data.actions[Object.keys(data.actions)[0]]),
                    'data': [],
                };
                angular.forEach($scope.actions.labels, function(label, index) {
                    //$scope.actions.data.push(Object.keys(data.actions[label]));
                    var row = [];
                    angular.forEach(data.actions[label], function (value, key) {
                        row.push(value);
                    });
                    $scope.actions.data.push(row);
                });
            });
        };

        var init = function () {
            DashboardService.initial().then(function success (data) {
                $scope.date_from = moment(data.min_date);
                $scope.date_to = moment(data.max_date);
                $scope.datepicker_date = {
                    'locale': {
                        'format': 'YYYY-MM-DD'
                    },
                    'startDate': $scope.date_from,
                    'endDate': $scope.date_to
                };
            });

        };

        init(); // initialize
    }
])// end controller

app.directive('eventLog', function() {
  return {
    restrict: 'C',
    scope: {
      events: '=events'
    },
    //template: '<ol><li ng-repeat="event in events track by $index"><em>{{ event.status }}</em><br/>{{ event.source }}, {{ event.lost_found_address }}<br/><small>{{ event.date_of | date }}</small></li></ol>'
    template: '<div ng-repeat="event in events track by $index" class="list-group"><a href="#" class="list-group-item"><b class="list-group-item-heading">{{ event.status }}</b><p class="list-group-item-text">{{ event.source }}, {{ event.lost_found_address }}<br/><small>{{ event.date_of | date }}</small></p></a></div>'
  };
});

app.factory('DashboardService', [
    '$q',
    '$log',
    '$resource',
    function($q, $log, $resource) {

        function dashboardAPI() {
            return $resource('/api/v1/dashboard/', {}, {
                'initial': {
                    'url': '/api/v1/dashboard/initial',
                    'cache': false,
                    'isArray': false
                },
                'query': {
                    'cache': false,
                    'isArray': false
                },
            });
        };

        return {
            initial: function () {
                var deferred = $q.defer();
                var api = dashboardAPI();
                var data = {};
                api.initial({},
                    function success(response) {
                        data = response.toJSON();
                        deferred.resolve(data);
                    },
                    function error(err) {
                        data.results = [];
                        deferred.reject(err);
                    }
                );
                return deferred.promise;
            },
            query: function (date_from, date_to) {
                var deferred = $q.defer();
                var api = dashboardAPI();
                var data = {};
                //console.log({'date_from': date_from, 'date_to': date_to})
                api.query({'date_from': date_from, 'date_to': date_to},
                    function success(response) {
                        data = response.toJSON();
                        deferred.resolve(data);
                    },
                    function error(err) {
                        data.results = [];
                        deferred.reject(err);
                    }
                );
                return deferred.promise;
            }
        };// end signleton return
    }
]); // end service
