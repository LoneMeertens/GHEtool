***********************************************************
Inter sizing tool comparison
***********************************************************
Ahmadfard and Bernier (2019) [1]_ developed a comprehensive set of test cases designed to compare geothermal software tools,
ultimately aiming at enhancing the reliability of design methods for sizing vertical ground heat exchangers. 
They reviewed existing tests and proposed four test cases that cover a wide range of conditions, 
from single boreholes to extensive borefields with varying annual ground thermal imbalances. 
They then conducted an inter-model comparison of twelve sizing tools, including several commercially available 
software programs (such as EED, GLHEpro, and DTS) and different forms of the ASHRAE sizing equation. The L2-, L3-, and L4-sizing methods of 
GHEtool were validated using this openly accessible document.

The results below can also be found in the :download:`excel document <Comparing_sizingtools_spreadsheet.xlsx>`.

+++++++++++++++++++++
Test 1
+++++++++++++++++++++

The first test case consists of a synthetically generated balanced load profile, either as a ground load or a building load. 
This test assumes that a single borehole handles the load without borehole-to-borehole thermal interference. An analysis of 
the first two sets in Test 1a shows that the various sizing tools provide results that are in relatively good agreement. 
For the first set, where the equivalent borehole resistance (Rb) are calculated by the tool themselves, borehole depths ranging from 
54.8 to 62.1 m are observed. The GHEtool L2-, L3-, and L4-methods yielded depths of 59.4 m (1.2% deviation), 59.6 m (1.6% deviation), 
and 56.3 m (-4.0% deviation), respectively. The GHEtool L4-method's slightly lower result is likely due to its use of hourly
values instead of a 6-hour peak duration. This result is in line with the other L4 tools. The borehole thermal resistance evaluated with
GHEtool was 0.128 m.K/W for all methods, consistent with other values for this parameter. 

.. list-table:: Calculated borehole depths for Test 1a with a peak load duration of 6 hours and Rb calculated by tool.
   :header-rows: 1

   * - Sizing method 
     - Borehole depth [m]
     - Difference from mean [%]
     - Calculated Rb* [m.K/W]
   * - L2
     - 59.4
     - 1.2
     - 0.128
   * - L3
     - 59.6 
     - 1.6
     - 0.128
   * - L4
     - 56.3 
     - -4.0
     - 0.128
   * - mean
     - 58.2
     -
     - 0.124
   * - min
     - 54.8
     -
     - 0.120
   * - max
     - 62.1 
     - 
     - 0.128

When the same Rb value (0.13 m.K/W) was used for all tools in the second set of Test 1a, the 
borehole depths ranged from 56.5 to 63.7 m, with a mean of 59.8 m. The GHEtool L2- and L3-methods produced depths of 
59.8 m (-0.3% deviation) and 60.0 m (0.0% deviation), respectively, while the L4-method gave a slightly shorter depth 
of 56.7 m (-5.4% deviation), consistent with other L4-methods. The differences in Rb evaluation across all tools in Test 1a 
were limited, indicating no significant flaws among the tools. Therefore, the remainder of this 
validation will discuss the performance for imposed values for Rb only. 

.. list-table:: Calculated borehole depths for Test 1a with a peak load duration of 6 hours and imposed Rb*=0.13 m.K/W.
   :header-rows: 1

   * - Sizing method 
     - Borehole depth [m]
     - Difference from mean [%]
     - Imposed Rb* = 0.13 [m.K/W]
   * - L2
     - 59.8
     - -0.3
     - 0.13
   * - L3
     - 60.0
     - 0.0
     - 0.13
   * - L4
     - 56.7
     - -5.4
     - 0.13
   * - mean
     - 59.8
     -
     - 
   * - min
     - 56.5
     -
     - 
   * - max
     - 63.7 
     - 
     - 

The same reasoning applies to the results obtained for Test 1b. The GHEtool L2- and L3-methods both resulted in depths of 76.7 m, 
consistent with the mean value of all tools, which is 76.1 m. The L4-method again provides a slightly lower value of 72.5 m, which 
is in line with other L4-methods. 


.. list-table:: Calculated borehole depths for Test 1b with  a peak load duration of 6 hours and imposed Rb*=0.13 m.K/W.
   :header-rows: 1

   * - Sizing method 
     - Borehole depth [m]
     - Difference from mean [%]
     - Imposed Rb* = 0.13 [m.K/W]
   * - L2
     - 76.7
     - 0.8
     - 0.13
   * - L3
     - 76.7
     - 0.8
     - 0.13
   * - L4
     - 72.5
     - -4.7
     - 0.13
   * - mean
     - 76.1
     -
     - 
   * - min
     - 71.3
     -
     - 
   * - max
     - 81.3
     - 
     - 
+++++++++++++++++++++
Test 2 
+++++++++++++++++++++

Shonder et al. (2000) [4]_ utilized data from an elementary school in Lincoln, Nebraska, for an inter-model comparison nearly two
decades ago. With advancements in sizing tools, this case was revisited for current validation. The test case involves a 
borefield of 12×10 boreholes, each 73 m deep and spaced 6 m apart. The test uses a specific load profile 
with monthly peak building loads of varying durations, ranging from 1 to 11 hours. 

.. list-table:: Calculated borehole depths for Test 2 with a peak load duration of 6 hours (L2, L3) and imposed Rb*=0.113 m.K/W.
   :header-rows: 1

   * - Sizing method 
     - Borehole depth [m]
     - Difference from mean [%]
     - Imposed Rb* = 0.113 [m.K/W]
   * - L2
     - 77.5
     - -11.6
     - 0.113
   * - L3
     - 79.6
     - -9.1
     - 0.113
   * - L4
     - 85.0
     - -2.9
     - 0.113
   * - mean
     - 87.6
     -
     - 
   * - min
     - 77.5
     -
     - 
   * - max
     - 102.0
     - 
     - 

When the same Rb value (0.13 m.K/W) was used for all tools, the borehole depths ranged from 77.5 to 102.0 m, with an 
average of 83.7 m. The GHEtool L2- and L3-methods produced depths of 77.5 m (-11.6% deviation) and 79.6 m
(-9.1% deviation), respectively, while the L4-method yielded a higher depth of 85.0 m (-2.9% deviation). For this 
specific imposed load profile, it is clear that the L4-method should be preferred over the L2- and L3-methods in GHEtool, 
due to the very specific imposed monthly peak loads which differ from the default 6-hour peak load in GHEtool.

+++++++++++++++++++++
Test 3
+++++++++++++++++++++

Monzó et al. (2000) [3]_ proposed a methodology to size the borefield in the first year of operation, with a monthly resolution (L3).
Test 3 employs the hourly, cooling-dominated ground load profile which they used to test their methodology.
This test is important because it represents scenarios where the fluid temperature limitation occurs in the first year of operation
Therefore, sizing tools that do not consider these first-year limitations, but only size based on end-of-period 
limitations, will yield inaccurate results. 

.. list-table:: Calculated borehole depths for Test 3 with a peak load duration of 6 hours and imposed Rb*=0.1 m.K/W.
   :header-rows: 1

   * - Sizing method 
     - Borehole depth [m]
     - Difference from mean [%]
     - Imposed Rb* = 0.1 [m.K/W]
   * - L2
     - 107.5
     - 6.4
     - 0.1
   * - L3
     - 107.4
     - 6.2
     - 0.1
   * - L4
     - 107.4
     - 6.2
     - 0.1
   * - mean
     - 101.1
     -
     - 
   * - min
     - 85.9
     -
     - 
   * - max
     - 115.0
     - 
     - 

When the same Rb value (0.113 m.K/W) was used for all tools, the borehole depths ranged from 85.9 to 115.0 m, with an 
average of 101.0 m. This high variability in required borehole depth underscores the importance of using a sizing tool 
that also considers the first year of operation. Sizing with the GHEtool L2-method resulted in a borehole depth of 
107.5 m (6.4% deviation), while both the L3- and L4-methods produced depths of 107.4 m (6.2% deviation). These three
methods yielded nearly identical results, indicating their reliability. All three methods resulted in higher borehole 
depths compared to the mean, where all twelve other sizing tools are included. The explanation is straightforward: sizing 
tools that do not account for first-year limitations will in this case undersize the borefield, leading to operational problems 
during the initial years.


.. list-table:: Calculated borehole depths for Test 3 for different spacing (B [m]) and design period (p [years]).
   :header-rows: 1

   * - Sizing method 
     - p=1, B=3 
     - p=1, B=5 
     - p=1, B=7 
     - p=10, B=3 
     - p=10, B=5 
     - p=10, B=7 
   * - L2
     - 113.4
     - 107.5
     - 107.1
     - 113.4
     - 107.5
     - 107.1
   * - L3
     - 118.4
     - 107.5
     - 107.1
     - 118.1
     - 107.4
     - 106.9
   * - L4
     - 114.4
     - 107.4 
     - 107.4
     - 114.1
     - 107.4
     - 108.3
   * - mean
     - 117.8
     - 110.7
     - 110.5
     - 101.2
     - 101.1
     - 104.6
   * - min
     - 105.0
     - 104.6
     - 106.3
     - 77.0
     - 85.9
     - 93.2
   * - max
     - 130.6
     - 115.0
     - 115.0
     - 130.6
     - 115.0
     - 115.0

The effects of spacing and design period were also considered in Test 3. The results indicate stable outcomes for the three 
different GHEtool methods regarding design period variations, as GHEtool accounts for first-year limitations. It can be observed
that the L3-method predicts a slightly higher variability in required borehole depths for different variations in spacing.

+++++++++++++++++++++
Test 4
+++++++++++++++++++++

Test 4 features a relatively high annual ground load imbalance with peak load conditions occurring during cooling operations. 
This profile serves as an effective test for evaluating the long-term borehole thermal interference effects. 
The borefield depth is calculated for a design period of 20 years for 25 boreholes, each with a borehole thermal resistance 
of 0.2 m.K/W. 

.. list-table:: Calculated borehole depths for Test 4 with  a peak load duration of 6 hours and imposed Rb*=0.2 m.K/W

   * - Sizing method 
     - Borehole depth [m]
     - Difference from mean [%]
     - Imposed Rb* = 0.2 [m.K/W]
   * - L2
     - 121.5
     - 1.9
     - 0.2
   * - L3
     - 122.2
     - 2.5
     - 0.2
   * - L4
     - 120.0
     - 0.6
     - 0.2
   * - mean
     - 119.2
     -
     - 
   * - min
     - 93.0
     -
     - 
   * - max
     - 128.9
     - 
     - 

When the same Rb value (0.2 m.K/W) was used for all tools, the borehole depths ranged from 93.0 to 128.0 m, with an 
average of 119.2 m. The GHEtool L2- and L3-methods produced depths of 121.5 me (1.9% deviation) and 122.2 m 
(2.5% deviation), respectively, while the L4-method yielded a slightly shorter depth of 120.0 m (0.6% deviation). 
These results indicate that all three GHEtool methods effectively account for long-term borehole thermal interference effects. 


+++++++++++++++++++++++++++++
Sensitivity analysis Test 4
+++++++++++++++++++++++++++++


The final results present a sensitivity analysis on Test 4, examining the relative variation in borehole depth in response to 
changes in five parameters: peak load magnitude (qh), thermal conductivity (kg), borehole spacing (B), ground temperature (Tg), 
and the total number of boreholes.


.. list-table:: Relative variations in borehole depth [%] for sensitivity analysis on Test 4
   :header-rows: 1

   * - Sizing method 
     - L from Test 4 [m]
     - qh=-125758.1 [W]
     - qh=-153704.4 [W]
     - ks=1.5 [W/(m.K)]
     - ks=2.3 [W/(m.K)]
     - B=6 [m]
     - B=10 [m]
     - Tg=10 [°C]
     - Tg=20 [°C]
     - 3x3 [bores]
     - 7x7 [bores]
   * - L2
     - 121.5
     - -5.9	
     - 5.2 	
     - 11.3	
     - -9.5	
     - 10.1	
     - -7.8	
     - -18.8	 
     - 26.6	
     - 149.0	
     - -49.4
   * - L3
     - 122.2
     - -4.9	
     - 5.1	
     - 11.4	
     - -9.6	
     - 9.6	
     - -7.5	
     - -18.7	
     - 26.5	
     - 148.0	
     - -49.2
   * - L4
     - 120.0
     - ----	
     - ----	
     - 11.5	
     - -9.7	
     - 9.4	
     - -7.6	
     - -18.8	
     - 26.5	
     - 147.9	
     - -49.3
   * - mean
     - 118.8
     - -4.7	
     - 5.0	
     - 14.3	
     - -9.6	
     - 10.8	
     - -6.5	
     - -17.9	
     - 27.2	
     - 150.4	
     - -48.8


The GHEtool results indicate that its sensitivity to the listed parameters is comparable to that of other sizing tools, 
demonstrating the robustness of GHEtool.

.. rubric:: References

.. [1] Ahmadfard M. and Bernier M., A review of vertical ground heat exchanger sizing tools including an inter-model comparison, Renewable and Sustainable Energy Reviews, Volume 110, 2019, Pages 247-265, ISSN 1364-0321, https://doi.org/10.1016/j.rser.2019.04.045
.. [2] Meertens, L., Peere, W., and Helsen, L. (2024). Influence of short-term dynamic effects on geothermal borefield size. In _Proceedings of International Ground Source Heat Pump Association Conference 2024. Montreal (Canada), 28-30 May 2024. https://doi.org/10.22488/okstate.24.000004
.. [3] Monzó P, Bernier M, Acuña J, Mogensen PA. (2016). Monthly based bore field sizing methodology with applications to optimum borehole spacing. ASHRAE Transact 2016;122(1):111–26.
.. [4] Shonder JA, Baxter VD, Hughes PJ, Thornton JW. (2000). A comparison of vertical ground heat exchanger design software for commercial applications. ASHRAE Transactions 2000;106:831–42. 