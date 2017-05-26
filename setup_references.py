import os, sys, json
import pprint as pp
from core.views_load_ref import load_ref

def load_reference():
	reference = {}
	list = []
	attributes = {'url':'https://www.ncbi.nlm.nih.gov/pubmed/10871296','citation':'''Tilakaratne, N., G. Christopoulos, et al. (2000). "Amylin receptor phenotypes derived from human calcitonin receptor/RAMP coexpression exhibit pharmacological differences dependent on receptor isoform and host cell environment." J Pharmacol Exp Ther 294(1): 61-72.
	Receptor activity modifying proteins (RAMPs) constitute a group of three proteins, designated as RAMP1, 2, and 3, which are able to effect functional changes in some members of the G protein-coupled receptor family. Thus, RAMP1 or RAMP3 can modify the calcitonin receptor (CTR) to also function as a high-affinity amylin receptor-like phenotype. To examine the RAMP/CTR interaction, individual RAMPs were coexpressed with either of the two human CTR (hCTR) isoforms, the insert negative (hCTR(I1-)) or the insert positive (hCTR(I1+)), in Chinese hamster ovary (CHO-P) or African monkey kidney (COS-7) cells. CHO-P cells provide an environment conducive to a low, but significant, level of amylin binding with either hCTR isoform alone, unlike in COS-7, where RAMP coexpression is imperative for amylin binding. Also, in CHO-P, hCTR(I1-) induced amylin binding with all three RAMPs, in contrast to COS-7, where only RAMP1 or RAMP3 generate an amylin receptor phenotype. hCTR(I1+) induced high-affinity amylin binding with any RAMP in either cell line. In COS-7 cells, hCTR(I1+)/RAMP-generated receptor displayed high- and low-affinity states, in contrast with the single-state binding seen with hCTR(I1-)/RAMP-generated receptor, whereas in CHO-P cells a two-affinity state receptor phenotype was evident with both hCTR isoforms. Endogenous RAMP expression is low and similar between cell lines. The results suggest that CTR/RAMP interaction in these cells is complex with other cellular factors such as the levels of different G proteins and/or receptor/RAMP stoichiometry following heterologous coexpression contributing to the ultimate receptor phenotype.'''}
	reference['Amylin receptor phenotypes derived from human calcitonin receptor/RAMP coexpression exhibit pharmacological differences dependent on receptor isoform and host cell environment'] = attributes

	attributes = {'url':'https://www.ncbi.nlm.nih.gov/pubmed/12446722','citation':'''Christopoulos, A., G. Christopoulos, et al. (2003). "Novel receptor partners and function of receptor activity-modifying proteins." J Biol Chem 278(5): 3293-3297.
	The receptor activity-modifying proteins (RAMPs) comprise a family of three accessory proteins that heterodimerize with the calcitonin receptor-like receptor (CL receptor) or with the calcitonin receptor (CTR) to generate different receptor phenotypes. However, RAMPs are more widely distributed across cell and tissue types than the CTR and CL receptor, suggesting additional roles for RAMPs in cellular processes. We have investigated the potential for RAMP interaction with a number of Class II G protein-coupled receptors (GPCRs) in addition to the CL receptor and the CTR. Using immunofluorescence confocal microscopy, we demonstrate, for the first time, that RAMPs interact with at least four additional receptors, the VPAC1 vasoactive intestinal polypeptide/pituitary adenylate cyclase-activating peptide receptor with all three RAMPs; the glucagon and PTH1 parathyroid hormone receptors with RAMP2; and the PTH2 receptor with RAMP3. Unlike the interaction of RAMPs with the CL receptor or the CTR, VPAC1R-RAMP complexes do not show altered phenotypic behavior compared with the VPAC1R alone, as determined using radioligand binding in COS-7 cells. However, the VPAC1R-RAMP2 heterodimer displays a significant enhancement of agonist-mediated phosphoinositide hydrolysis with no change in cAMP stimulation compared with the VPAC1R alone. Our findings identify a new functional consequence of RAMP-receptor interaction, suggesting that RAMPs play a more general role in modulating cell signaling through other GPCRs than is currently appreciated.'''}
	reference['Novel receptor partners and function of receptor activity-modifying proteins'] = attributes


	attributes = {'url':'https://www.ncbi.nlm.nih.gov/pubmed/21649645','citation':'''Barwell, J., J. J. Gingell, et al. (2012). "Calcitonin and calcitonin receptor-like receptors: common themes with family B GPCRs?" Br J Pharmacol 166(1): 51-65.
	The calcitonin receptor (CTR) and calcitonin receptor-like receptor (CLR) are two of the 15 human family B (or Secretin-like) GPCRs. CTR and CLR are of considerable biological interest as their pharmacology is moulded by interactions with receptor activity-modifying proteins. They also have therapeutic relevance for many conditions, such as osteoporosis, diabetes, obesity, lymphatic insufficiency, migraine and cardiovascular disease. In light of recent advances in understanding ligand docking and receptor activation in both the family as a whole and in CLR and CTR specifically, this review reflects how applicable general family B GPCR themes are to these two idiosyncratic receptors. We review the main functional domains of the receptors; the N-terminal extracellular domain, the juxtamembrane domain and ligand interface, the transmembrane domain and the intracellular C-terminal domain. Structural and functional findings from the CLR and CTR along with other family B GPCRs are critically appraised to gain insight into how these domains may function. The ability for CTR and CLR to interact with receptor activity-modifying proteins adds another level of sophistication to these receptor systems but means careful consideration is needed when trying to apply generic GPCR principles. This review encapsulates current thinking in the realm of family B GPCR research by highlighting both conflicting and recurring themes and how such findings relate to two unusual but important receptors, CTR and CLR.'''}
	reference['Calcitonin and calcitonin receptor-like receptors: common themes with family B GPCRs?'] = attributes

	attributes = {'url':'https://www.ncbi.nlm.nih.gov/pubmed/22946657','citation':'''Wootten, D., H. Lindmark, et al. (2013). "Receptor activity modifying proteins (RAMPs) interact with the VPAC2 receptor and CRF1 receptors and modulate their function." Br J Pharmacol 168(4): 822-834.
	BACKGROUND AND PURPOSE: Although it is established that the receptor activity modifying proteins (RAMPs) can interact with a number of GPCRs, little is known about the consequences of these interactions. Here the interaction of RAMPs with the glucagon-like peptide 1 receptor (GLP-1 receptor), the human vasoactive intestinal polypeptide/pituitary AC-activating peptide 2 receptor (VPAC(2)) and the type 1 corticotrophin releasing factor receptor (CRF(1)) has been examined. EXPERIMENTAL APPROACH: GPCRs were co-transfected with RAMPs in HEK 293S and CHO-K1 cells. Cell surface expression of RAMPs and GPCRs was examined by ELISA. Where there was evidence for interactions, agonist-stimulated cAMP production, Ca(2+) mobilization and GTPgammaS binding to G(s), G(i), G(12) and G(q) were examined. The ability of CRF to stimulate adrenal corticotrophic hormone release in Ramp2(+/-) mice was assessed. KEY RESULTS: The GLP-1 receptor failed to enhance the cell surface expression of any RAMP. VPAC(2) enhanced the cell surface expression of all three RAMPs. CRF(1) enhanced the cell surface expression of RAMP2; the cell surface expression of CRF(1) was also increased. There was no effect on agonist-stimulated cAMP production. However, there was enhanced G-protein coupling in a receptor and agonist-dependent manner. The CRF(1) : RAMP2 complex resulted in enhanced elevation of intracellular calcium to CRF and urocortin 1 but not sauvagine. In Ramp2(+/-) mice, there was a loss of responsiveness to CRF. CONCLUSIONS AND IMPLICATIONS: The VPAC(2) and CRF(1) receptors interact with RAMPs. This modulates G-protein coupling in an agonist-specific manner. For CRF(1), coupling to RAMP2 may be of physiological significance.'''}
	reference['Receptor activity modifying proteins (RAMPs) interact with the VPAC2 receptor and CRF1 receptors and modulate their function'] = attributes

	attributes = {'url':'https//www.ncbi.nlm.nih.gov/pubmed/12529938','citation':'''Usdin, T. B., T. I. Bonner, et al. (2002). "The parathyroid hormone 2 (PTH2) receptor." Receptors Channels 8(3-4): 211-218.
	The human PTH2 receptor binds and is activated at high potency by PTH and by the recently discovered peptide tuberoinfundibular peptide of 39 residues (TIP39). Rat and zebrafish PTH2 receptors are more weakly activated by PTH, suggesting that TIP39 may be the natural ligand for the PTH2 receptor. Unlike the PTH1 receptor, the PTH2 receptor interacts extremely weakly with parathyroid hormone-related peptide (PTHrP). The PTH2 receptor is strongly coupled to stimulation of cAMP accumulation, and more weakly, in a cell-specific manner to increases in intracellular calcium concentration. A variety of evidence supports the general model of receptor amino terminal sequences binding ligand carboxyl terminal sequences with high affinity, and ligand amino terminal sequences activating the receptor through interaction with the "juxtamembrane" portion of the receptor. The receptor is present at greatest levels in the nervous system. It is expressed in scattered cells in the cerebral cortex and basal ganglia and at relatively high abundance in the septum, midline thalamic nuclei, several hypothalamic nuclei, and the dorsal horn of the spinal cord. Peripherally, expression in pancreatic islet somatostatin cells is most dramatic. Functional hypotheses based on the receptor's distribution are being tested. Recent data support involvement in hypothalamic releasing-factor secretion and pain.'''}
	reference['The parathyroid hormone 2 (PTH2) receptor'] = attributes

	attributes = {'url':'https://www.guidetopharmacology.org/GRAC/FamilyIntroductionForward?familyId=11.','citation':'IUPHAR/BPS Guide to PHARMACOLOGY, https://www.guidetopharmacology.org/GRAC/FamilyIntroductionForward?familyId=11.'}
	reference['Calcitonin Receptors: Introduction'] = attributes

	attributes = {'url':'https//www.ncbi.nlm.nih.gov/pubmed/15494035','citation':'''Hay, D. L., G. Christopoulos, et al. (2004). "Amylin receptors: molecular composition and pharmacology." Biochem Soc Trans 32(Pt 5): 865-867.
	Several receptors which bind the hormone AMY (amylin) with high affinity have now been identified. The minimum binding unit is composed of the CT (calcitonin) receptor at its core, plus a RAMP (receptor activity modifying protein). The receptors have been named AMY(1(a)), AMY(2(a)) and AMY(3(a)) in accordance with the association of the CT receptor (CT((a))) with RAMP1, RAMP2 and RAMP3 respectively. The challenge is now to determine the localization and pharmacological nature of each of these receptors. Recent attempts to achieve these aims will be briefly discussed.'''}
	reference['Amylin receptors: molecular composition and pharmacology'] = attributes

	attributes = {'url':'https//www.ncbi.nlm.nih.gov/pubmed/16888151','citation':'''Sexton, P. M., M. Morfis, et al. (2006). "Complexing receptor pharmacology: modulation of family B G protein-coupled receptor function by RAMPs." Ann N Y Acad Sci 1070: 90-104.
	The most well-characterized subgroup of family B G protein-coupledreceptors (GPCRs) comprises receptors for peptide hormones, such as secretin, calcitonin (CT), glucagon, and vasoactive intestinal peptide (VIP). Recent data suggest that many of these receptors can interact with a novel family of GPCR accessory proteins termed receptor activity modifying proteins (RAMPs). RAMP interaction with receptors can lead to a variety of actions that include chaperoning of the receptor protein to the cell surface as is the case for the calcitonin receptor-like receptor (CLR) and the generation of novel receptor phenotypes. RAMP heterodimerization with the CLR and related CT receptor is required for the formation of specific CT gene-related peptide, adrenomedullin (AM) or amylin receptors. More recent work has revealed that the specific RAMP present in a heterodimer may modulate other functions such as receptor internalization and recycling and also the strength of activation of downstream signaling pathways. In this article we review our current state of knowledge of the consequence of RAMP interaction with family B GPCRs.'''}
	reference['Complexing receptor pharmacology: modulation of family B G protein-coupled receptor function by RAMPs'] = attributes

	load_ref(json.dumps(reference))

def main():
	load_reference()

if __name__ == "__main__":
	main()
