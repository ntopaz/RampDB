var app = angular.module('homeApp', ['ngSanitize']);

app.controller('myCtrl', function ($scope, $http, $sce) {
	$scope.loading = true;
	$scope.protein_page = false;
	$scope.ligand_page = false;
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

			else if ('protein' in response.data){
				$scope.main_loading = false;
				$scope.home = false;
				$scope.protein_page = true;
				$scope.organism = response.data['protein']['match']['organism'];
				$scope.source = response.data['protein']['match']['source'];
				$scope.id = response.data['protein']['match']['id'];
				$scope.url = $scope.source.concat('/protein/',$scope.id);
				$scope.quer_name = response.data['protein']['name'];
				$scope.family = response.data['protein']['match']['family'];
				$scope.family_short = response.data['protein']['match']['family_short'];
				$scope.confidence = response.data['protein']['match']['ident'];
				var my_msa = response.data['msa'];
				console.log(my_msa)
				if ($scope.confidence > 75){
					$scope.highConf = true;
					}
				else {
					$scope.highConf = false;
					}

				console.log($scope.results);
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

			else if ('ligand' in response.data){
				$scope.main_loading = false;
				$scope.ligand_page = true;
				$scope.home = false;
				$scope.query_name = response.data['ligand']['query_name'];
				$scope.match_name = response.data['ligand']['match']['name'];
				$scope.inchi_key = response.data['ligand']['match']['inchi_key'];
				$scope.chem_id = response.data['ligand']['match']['chem_id'];
				$scope.molecular_formula = response.data['ligand']['match']['molecular_formula'].replace(/(\d+)/g,"<sub>$1</sub>");
				console.log($scope.molecular_formula);
				$scope.molecular_weight = response.data['ligand']['match']['molecular_weight'];
				var img_get_url = 'pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/' + $scope.chem_id + '/PNG?record_type=2d&image_size=large';
        	        	$http.get(img_get_url)
	                	.then(function(response) {
					$scope.img = response.data;
					console.log($scope.img);
					});
				}
			});
		};

	$scope.Example = function() {
		$scope.proteintext = ">gi|7592833|dbj|BAA94425.1| receptor activity modifying protein 1 [Rattus norvegicus]\r\nMALGLRGLPRRGLWLLLVHHLFMVTACRDPDYGTLIQELCLSRFKEDMETIGKTLWCDWGKTIGSYGELTHCTKLVANKIGCFWPNPEVDKFFIAVHHRYFSKCPVSGRALRDPPNSILCPFIVLPITVTLLMTALVVWRSKRTEGIV"
	};
	$scope.LigandSelected = function() {
		$scope.ligandtext = $scope.commonLigands;
	};
	$scope.backtoHome = function() {
		$scope.home = true;
		$scope.protein_page = false;
		$scope.ligand_page = false;
	};
});

