Programs:
	CMPT310-ASN2.py - Used for finding the colouring for graphs that use the input specified in the Assignment spec
	CMPT310-ASN2-ComplexGraphs.py - Used for finding the colouring for the complex graphs found at http://mat.gsia.cmu.edu/COLOR/instances.html (minus the header information at the top of the file)
Prerequisites:
	These programs require Python version 2.7 in order to run.

Running:
	CMPT310-ASN2:
		for running on the default settings (using the Minimum Remaining Values (and Degree Heuristic) and the Least Constraining Value heuristic):
			python CMPT310-ASN2.py <graph fileName>
		for running with custom settings (Minimum Remaining Values and the Least Constraining Value heuristics can be turned on or off):
			python CMPT310-ASN2.py <graph fileName> <optional: use MRV heuristic; 'true'/'false'> <optional: use LCV heuristic; 'true'/'false'>

	CMPT310-ASN2-ComplexGraphs:
		for running on the default settings (using the Minimum Remaining Values (and Degree Heuristic) and the Least Constraining Value heuristic):
			python CMPT310-ASN2-ComplexGraphs.py <complex graph fileName> <numColours>
		for running with custom settings (Minimum Remaining Values and the Least Constraining Value heuristics can be turned on or off):
			python CMPT310-ASN2-ComplexGraphs.py <complex graph fileName> <numColours> <optional: use MRV heuristic; 'true'/'false'> <optional: use LCV heuristic; 'true'/'false'>
		
Examples:
	CMPT310-ASN2:
		python CMPT310-ASN2.py Asst2.data.txt
		python CMPT310-ASN2.py Asst2.data.txt true false
		python CMPT310-ASN2.py Asst2.data.txt false true
		python CMPT310-ASN2.py Asst2.data.txt false false

	CMPT310-ASN2-ComplexGraphs:
		python CMPT310-ASN2-ComplexGraphs.py queen8_12.data 12 
		python CMPT310-ASN2-ComplexGraphs.py queen8_12.data 12 true false
		python CMPT310-ASN2-ComplexGraphs.py queen8_12.data 12 false true
		python CMPT310-ASN2-ComplexGraphs.py queen8_12.data 12 false false