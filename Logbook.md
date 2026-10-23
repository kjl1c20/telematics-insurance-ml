# Data Audit
Input dataset has been audited and the audit result can be found in explore.ipynb. This synthetic dataset has no null values and duplicates thus all 100,000 data entries are kept.

The synthetic data was provided with policy duration, number of claims and claim amount. In this case, we can easily compute the pure premium, frequency and average claim amount. 

The duration are currently in days instead of years. Need to convert to duration unit to years. 

intensity08 most likely represents the number of sudden accelerations of at least 8 mph/s per 1,000 miles (based on research). Each entries means how many times it occurs. It is a count variable.

-----------------------------------------

The telematics model contains a lot of nested threshold of the same underlying driving behavior. For example, we have acceleration at different values. We have turning at different values. We can't just plug in every single column in there into our machine learning model and basically run it. The below are the columns that we need to identify the right threshold:

Accel, at 6, 8, 9, 11, 12 and 14
Brake, at the same thresholds
Left turn intensity, from 08 to 12
Right turn intensity, from 08 to 12
Pct.drive 2hrs, 3hrs and 4hrs

I would need to isolate each group and test it and loop through it. Will pick the lowest number as a starting column for each group. Will create a new notebook for that.

# Threshold selection
Confirmed the threshold columns are cumulative: Brake.06 is always >= Brake.08 >= Brake.09.
Brake.11, 12 and 14 correlate at 0.92 to 0.98 with each other. Keeping them all made
coefficients flip sign (Brake.09 was -0.08), which makes no sense for harder braking.

Method: greedy search, one group at a time. Start every group at its lowest threshold,
swap through each option in one group, keep the lowest mean CV deviance, move to the next group.
Only the training split is used. Same folds (random_state=42) for every run.

Result: the lowest threshold won in every group.
- Brake.06: clear win, beats Brake.08 on 5/5 folds by 0.0014
- Pct.drive.2hrs: small but consistent, 5/5 folds
- Accel.06: weak, 4/5 folds
- Left and right turn: ties, kept lowest threshold as tiebreak

20 columns dropped, saved to drop_columns.json and loaded in the main notebook.

Next is investigate, is there a pattern in which individual day metric and see if there is a better way in handling 50 territories. Need to look into claim severity model next.