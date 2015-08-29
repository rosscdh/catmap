var app = angular.module('DashboardApp', [
    'ui.router',
    'ngResource',
    'angularMoment',
    'angular-loading-bar',
    'daterangepicker',
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
    'DashboardService',
    function ($scope, $q, DashboardService) {

        $scope.datepicker_date = new Date();
        $scope.date_from = new Date();
        $scope.date_to = new Date();

  $scope.labels = ["Download Sales", "In-Store Sales", "Mail-Order Sales", "Tele Sales", "Corporate Sales"];
  $scope.data = [300, 500, 100, 40, 120];

        var init = function () {
            DashboardService.initial().then(function success (data) {
                console.log(data);
                $scope.initial = data;

                $scope.date_from = data.min_date;
                $scope.date_to = data.max_date;
                $scope.datepicker_date = {'startDate': $scope.date_from, 'endDate': $scope.date_to};

                DashboardService.query($scope.date, $scope.date).then(function success (data) {
                    $scope.data = data;
                });
            });
            //$scope.data = DashboardService.query($scope.date, $scope.date);
        };

        init(); // initialize
    }
])// end controller


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
                    'cache': true,
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
