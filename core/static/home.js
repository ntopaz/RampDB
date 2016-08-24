var app = angular.module('homeApp', []);

app.controller('myCtrl', function ($scope, $http) {
	$scope.loading = true;
	$scope.errorflag = false;
	$scope.main_loading = false;
	$scope.results = false;
	$scope.home = true;
	$http.get('core/db_status')
	.then(function(response){
		$scope.data = response.data;
		$scope.loading = false;
		$scope.results = true;
	});

	$scope.Submit = function() {
		$scope.main_loading = true;
		$scope.errorflag = false;
		$http.post("core/calculate_results/",{"protein":$scope.proteintext,"ligand":$scope.ligandtext})
		.then(function(response) {
			if ('error' in response.data){
				$scope.error = response.data['error'];
				$scope.main_loading = false;
				$scope.errorflag = true;
			}
			else {
			$scope.main_loading = false;
			$scope.organism = response.data['start']['match']['organism'];
			$scope.source = response.data['start']['match']['source'];
			$scope.id = response.data['start']['match']['id'];
			$scope.url = $scope.source.concat('/protein/',$scope.id);
			$scope.quer_name = response.data['start']['name'];
			$scope.family = response.data['start']['match']['family'];
			$scope.family_short = response.data['start']['match']['family_short'];
			$scope.confidence = response.data['start']['match']['ident'];
			var my_msa = response.data['msa'];
			console.log(my_msa)
			if ($scope.confidence > 75){
				$scope.highConf = true;
			}
			else{
				$scope.highConf = false;
			}
			console.log($scope.results);
			$scope.home = false;
        	        $http.post("core/interactions",{'family':$scope.family})
	                .then(function(response) {
				$scope.interactions = response.data;
				console.log($scope.interactions);
			});
			var opts = ({
			el: sequence,
			seqs: msa.io.fasta.parse(my_msa),
			});
 			opts.colorscheme = {scheme:"taylor"};
			opts.vis = {labelId: false, textVisible: true, labelNameLength:100};
			opts.zoomer = {alignmentHeight: 65,alignmentWidth: "425", rowHeight: 30, columnWidth:20,
					labelLineHeight:"25px",labelNameLength: 75, labelFontsize:19,residueFont:"21"};
			var m = new msa(opts);
			m.render();
			}
		});
	};
	$scope.Example = function() {
		$scope.proteintext = ">gi|7592833|dbj|BAA94425.1| receptor activity modifying protein 1 [Rattus norvegicus]\r\nMALGLRGLPRRGLWLLLVHHLFMVTACRDPDYGTLIQELCLSRFKEDMETIGKTLWCDWGKTIGSYGELTHCTKLVANKIGCFWPNPEVDKFFIAVHHRYFSKCPVSGRALRDPPNSILCPFIVLPITVTLLMTALVVWRSKRTEGIV"
	};
	$scope.LigandSelected = function() {
		$scope.ligandtext = $scope.commonLigands;
	};
});

