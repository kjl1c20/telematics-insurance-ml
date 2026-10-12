# Data Audit
Input dataset has been audited and the audit result can be found in explore.ipynb. This synthetic dataset has no null values and duplicates thus all 10,000 data entries are kept.

The synthetic data was provided with policy duration, number of claims and claim amount. In this case, we can easily compute the pure premium, frequency and average claim amount. 

The duration are currently in days instead of years. Need to convert to duration unit to years. 

intensity08 most likely represents the number of sudden accelerations of at least 8 mph/s per 1,000 miles (based on research). Each entries means how many times it occurs. It is a count variable.