var app = angular.module('homeApp', ['ngSanitize']);

app.config(['$compileProvider',
    function ($compileProvider) {
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|file|blob):/);
}]);


app.controller('myCtrl', function ($scope, $http, $sce, $window) {
	$scope.loading = true;
	$scope.gpcr_quer = false;
	$scope.ramp_quer = false;
	$scope.protein_page = false;
	$scope.ligand_page = false;
	$scope.errorflag = false;
	$scope.main_loading = false;
	$scope.results = false;
	$scope.home = true;
	$scope.t_threshold = "85"
	$http.get('core/db_status')
	.then(function(response){
		$scope.data = response.data;
		$scope.loading = false;
		$scope.results = true;
	});
	$http.get('core/get_prot')
	.then(function(response){
		$scope.ramp_data = response.data["Ramp"];
		$scope.gpcr_data = response.data["GPCR"];
	});
	$scope.Submit = function() {
		var content = "";
		$scope.main_loading = true;
		$scope.errorflag = false;
		$http.post("core/calculate_results/",{"protein":$scope.proteintext,"ligand":$scope.ligandtext, "t_score":$scope.t_threshold})
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
				$scope.length = response.data['protein']['length'];
				$scope.source = response.data['protein']['match']['source'];
				$scope.id = response.data['protein']['match']['id'];
				$scope.url = $scope.source.concat('/protein/',$scope.id);
				$scope.quer_name = response.data['protein']['name'];
				$scope.family = response.data['protein']['match']['family'];
				$scope.family_short = response.data['protein']['match']['family_short'];
				$scope.int_status = response.data['protein']['match']['int_status'];
				$scope.confidence = response.data['protein']['match']['ident'];
				$scope.eval = response.data['protein']['match']['eval'];
				$scope.max_score = response.data['protein']['match']['max_score'];
				var my_msa = response.data['msa'];
				content += "Query Name:\t" + $scope.quer_name +"\n";
				content += "Family:\t" + $scope.family +"\n";
				content += "Confidence:\t" + $scope.confidence +"\n";
				content += "E value:\t" + $scope.eval +"\n";
				content += "Max Score:\t" + $scope.max_score +"\n";
				content += "Alignment to Domain:\t\n" + my_msa +"\n";
				if ($scope.confidence > 30){
					$scope.highConf = true;
					}
				else {
					$scope.highConf = false;
					}

				var interactions = ""
				getinteraction = function () {
				return $http.post("core/interactions",{'family':$scope.family})
				.success(function(data) {
					if ('ramp' in data){
						$scope.ramp_quer = true;
						$scope.interactions = data['interactions'];
						interactions += "Interactions:\n";
						interactions += "Phenotype\tProtein\tLigand\tFunction\n";
						for (var key in $scope.interactions){
							interactions += $scope.interactions[key]["phenotype"] + "\t" +  $scope.interactions[key]["prot"] + "\t" + $scope.interactions[key]["ligand"] + "\t" +  $scope.interactions[key]["function"] +"\n";
							}

					}
					else{
						$scope.gpcr_quer = true;
						$scope.interactions = data['interactions'];
						interactions += "Interactions:\n";
						interactions += "Phenotype\tProtein\tLigand\tFunction\n";
						for (var key in $scope.interactions){
							interactions += $scope.interactions[key]["phenotype"] + "\t" +  $scope.interactions[key]["prot"] + "\t" + $scope.interactions[key]["ligand"] + "\t" +  $scope.interactions[key]["function"] +"\n";
						}

					}
					});
				}
				getinteraction().then(function(){
					content += interactions	
					let dl_blob = new Blob([content], { type: 'text/plain'});
					$scope.url_dl = (window.URL || window.webkitURL).createObjectURL(dl_blob);
					});
				var opts = ({
				el: sequence,
				seqs: msa.io.fasta.parse(my_msa),
					});
 				opts.colorscheme = {scheme:"taylor"};
				opts.vis = {labelId: false, textVisible: true, labelNameLength:100};
				opts.zoomer = {alignmentHeight: 65,alignmentWidth: "500", rowHeight: 30, columnWidth:15,
						labelLineHeight:"25px",labelNameLength: 75, labelFontsize:19,residueFont:"19"};
				var m = new msa(opts);
				m.render();

				}
			else if ('ligand' in response.data){
				$scope.main_loading = false;
				$scope.img_loaded = false;
				$scope.ligand_page = true;
				$scope.home = false;
				$scope.peptide = false
				$scope.query_name = response.data['ligand']['query_name'];
				$scope.match_name = response.data['ligand']['match']['name'];
				$scope.inchi_key = response.data['ligand']['match']['inchi_key'];
				$scope.chem_id = response.data['ligand']['match']['chem_id'];
				$scope.sequence = response.data['ligand']['match']['sequence'];
				$scope.lig_type = response.data['ligand']['match']['lig_type'];
				if ($scope.lig_type == "Peptide") {
				$scope.peptide = true
				}
				$scope.gtp_id = response.data['ligand']['match']['gtp_id'];
				$scope.url = "http://guidetopharmacology.org/GRAC/LigandDisplayForward?tab=summary&ligandId=" + $scope.gtp_id;
				$scope.molecular_formula = response.data['ligand']['match']['molecular_formula'].replace(/(\d+)/g,"<sub>$1</sub>");
				$scope.molecular_weight = response.data['ligand']['match']['molecular_weight'];
				if ($scope.molecular_weight != "N/A"){
					$scope.molecular_weight += " g/mol";
				}
				content += "Query Name:\t" + $scope.query_name +"\n";
				content += "Match Name:\t" + $scope.match_name +"\n";
				content += "PubChem ID:\t" + $scope.chem_id +"\n";
				content += "Inchi Key:\t" + $scope.inchi_key +"\n";
				content += "URL:\t" + $scope.url +"\n";
				var interactions = ""
        	        	getliginteraction = function () {
				return $http.post("core/ligand_int",{'ligand_name':$scope.match_name})
	                	.success(function(data) {
					$scope.interactions = data;
					$scope.references = data['interactions']['references'];
					if ($scope.interactions) {
						interactions += "Interactions:\n";
						interactions += "Phenotype\tProtein\tLigand\tAffinity\n";
						for (var key in $scope.interactions){
							interactions += $scope.interactions[key]["phenotype"] + "\t" +  $scope.interactions[key]["ramp"] + "\t" + $scope.interactions[key]["gpcr"] + "\t" +  $scope.interactions[key]["function"] +"\n";
						}
						}
					});
				}
				getliginteraction().then(function(){
					content += interactions
					let dl_blob = new Blob([content], { type: 'text/plain'});
					$scope.url_dl = (window.URL || window.webkitURL).createObjectURL(dl_blob);
					});
				console.log($scope.chem_id);
				if ($scope.chem_id != "Not on PubChem") {
				var img_get_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + $scope.chem_id + "/PNG?record_type=2d&image_size=large";
        	        	$http.get(img_get_url, {responseType: "arraybuffer"})
	                	.then(function(response) {
					let blob = new Blob([response.data], {type: 'image/png'});
					$scope.ligand_img = (window.URL || window.webkitURL).createObjectURL(blob);
					$scope.img_loaded = true;
					});
				}
				}

			});
		};

	$scope.rampStrongExample = function() {
		$scope.proteintext = ">Ramp_Strong_Example\nMALGLRGLPRRGLWLLLVHHLFMVTACRDPDYGTLIQELCLSRFKEDMETIGKTLWCDWGKTIGSYGELTHCTKLVANKIGCFWPNPEVDKFFIAVHHRYFSKCPVSGRALRDPPNSILCPFIVLPITVTLLMTALVVWRSKRTEGIV"
	};
	$scope.gpcrStrongExample = function() {
		$scope.proteintext = ">GPCR_Strong_Example\nMRFTFTRQFLAFFILISNPASILPRSENLTFPTFEPEPYLYSVGRKKLVDAQYRCYDRMQQLPPYEGEGPYCNRTWDGWMCWDDTPAGVLSVQLCPDYFPDFDPTEKVTKYCDESGVWFKHPENNRTWSNYTLCNAFTPEKLQNAYVLYYLAIVGHSMSIITLVVSLGIFVYFRSLGCQRVTLHKNMFLTYILNSMIIIIHLVEVVPNGELVRKDPVSCKILHFFHQYMMACNYFWMLCEGIYLHTLIVVSVFNEAKHLRWYYLLGWGFPLVPTTIHAITRALYFNDNCWISVDTHLLYIIHGPVMVALVVNFFFLLNIVRVLVTKMRETHEAESYMYLKAVKATMILVPLLGIQFVVFPWRPSNKVLGKIYDYFMHSLIHFQGFFVATIYCFCNNEVQTTLKRQWAQFKIQWNQRWGTRPSNRSAAARAAAAAAEAGGDNIPVYICHQEPRNDPPNNQGEEGAEMIVLNIIEKESSA"
	};
	$scope.gpcrWeakExample = function() {
		$scope.proteintext = ">GPCR_Weak_Example\nMMKDAMLRIACLIILQMFPDRTSPKHTATMFTSSGQTTLSPQPIDFRSSTDSNARSENTSIRDPAIEEACNEYRSIAANYTNKREVLERIMTSQAACQVIHFCEMENKFDGFCPSMIDGLGTCFHQSKSGQTASVSCLEELNGIPYNTSDTVTRKCLEGGRWENRSEYNCRPILDEIVCKDVAEFFHTYGFTPKEKQPCEIHFANVVKISMAGRGLSLFTLIVAFIIFCSIRSQWSYRSGCLYIIHWNFVMSLMLRNVLWICLYLFMGFSNNENKTIICPIMVTVFNYGQTTSYCWMFLEGIYLHRYVAIQLGNDDKLSWRFYVTVGWGFPVLIMSAWAATKSVLETGTCWLPGQSLSNADYIFKVPVLIALLINFVIMINVIRILVVKLCNPPARRPADGSSIESTHYFKTAKAALVLFPLLGLTYVLFIISPGYGTTGETVFLYFNTVLDSFQGFFVCLVYYYAHHDVQVEVSKKLRRVKSCFMCTNRKEYSRQNQWSRHLSRSKQANGCAGNKRNRSITLVTSALNPSPEIIETENRDISHENTSDDNQITNGLECTSFFTETSELSKPKDLT"
	};
	$scope.rampWeakExample = function() {
		$scope.proteintext = ">Ramp_Weak_Example\nMTDNSQNINSSLRKQNKTLEQRKWGSYRVIGLPQDSSKDDIELNCSASTNIDTSGLSKFEEEERIKKNKKVKESSDYLLDYQEKVNLISTELNKVVEKYGLELTDFRMIYNQYTSRIDNCRTWDEVNKVIDEIKSEIEFFYQLRENHFKRQIDSGFTPNEVLCAHLVLVIPAVIFMTSILIWLLSITQKNKDGL"
	};
	$scope.LigandSelected = function() {
		$scope.ligandtext = $scope.commonLigands;
	};
	$scope.backtoHome = function() {
		$scope.home = true;
		$scope.protein_page = false;
		$scope.ligand_page = false;
		$scope.ramp_quer = false;
		$scope.gpcr_quer = false;
	};
	$scope.popProtein = function(my_val) {
		$scope.my_val = my_val;
		$scope.my_val = $scope.my_val.replace(/\s/g,"_");
		window.location = "/protein?" + $scope.my_val;

	};	
});

app.directive('myRepeatDirective',function() {
	return function(scope,element,attrs){		
		if (scope.$last){
			scope.show_element=true;
			document.getElementById("my_spinner").style.display = "none";
		}
	};
})
