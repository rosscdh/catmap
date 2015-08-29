var app = angular.module('DashboardApp', [
    'ui.router',
    'ngResource',
    'angularMoment',
    'angular-loading-bar',
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

app.controller("DashboardController", ['$scope', '$q',
    function ($scope, $q) {

        $scope.date = new Date();

  $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
  $scope.series = ['Series A', 'Series B'];
  $scope.data = [
    [65, 59, 80, 81, 56, 55, 40],
    [28, 48, 40, 19, 86, 27, 90]
  ];
  $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };

    }])// end controller

app.factory('DashboardService', [
    '$q',
    '$log',
    '$resource',
    '$rootScope',
function($q, $log, $resource) {

        function dashboardAPI() {
          return $resource(
            '/api/v1/dashboard', {}, {}
          );
        };

}]);
