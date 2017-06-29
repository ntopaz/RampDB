var app = angular.module('protApp', ['ngSanitize']);

app.config(['$compileProvider',
    function ($compileProvider) {
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|file|blob):/);
}]);

app.controller('protCtrl', function ($scope, $http, $sce) {
	var query = window.location.search;
	if (query.substring(0,1) == '?') {
		query = query.substring(1);
	}
	$http.get('core/get_prot')
	.then(function(response){
		$scope.ramp_data = response.data["Ramp"];
		$scope.gpcr_data = response.data["GPCR"];
	});
	$scope.query = query.replace(/_/g," ");
	console.log($scope.query);
	$http.post("core/get_family/",{"family":$scope.query})
		.then(function(response) {
			$scope.prot_name = response.data[$scope.query]["name"];
			$scope.name_short = response.data[$scope.query]["name_short"];
			$scope.pdb_id = response.data[$scope.query]["pdb_id"];	
			$scope.gtp_id = response.data[$scope.query]["gtp_id"];
			if ($scope.pdb_id != "None"){	
			$scope.pdb_link = "http://www.rcsb.org/pdb/explore/explore.do?pdbId="+$scope.pdb_id;
			$scope.pdb_flag = true;
			}
			else{
			$scope.pdb_flag = false;
			$scope.pdb_link = "Not Found on PDB";				
			}
			$scope.gtp_link = "http://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId="+$scope.gtp_id;			
		});	
	$scope.backtoHome = function() {
		window.history.back();
	};		
	$scope.popProtein = function(my_val) {
		$scope.my_val = my_val;
		$scope.my_val = $scope.my_val.replace(/\s/g,"_");
		window.location = "/protein?" + $scope.my_val;

	};		
	 $http.post("core/interactions",{'family':$scope.query})
	.success(function(data) {
		if ('ramp' in data){
			$scope.ramp_quer = true;
			$scope.interactions = data['interactions'];
		}
		else{
			$scope.gpcr_quer = true;
			$scope.interactions = data['interactions'];
		}
	});
});					


