| experiment   | variant                        | mode     |   projects |   runs | uses_true_labels   | branches                                                               |
|:-------------|:-------------------------------|:---------|-----------:|-------:|:-------------------|:-----------------------------------------------------------------------|
| A3           | strata_180_365                 | complete |         10 |     50 | True               | zealous-lamport                                                        |
| A3           | strata_30_180                  | complete |         10 |     50 | True               | zealous-lamport                                                        |
| A3           | strata_365_730                 | complete |         10 |     50 | True               | zealous-lamport                                                        |
| A3           | strata_730_inf                 | complete |         10 |     50 | True               | zealous-lamport                                                        |
| A4           | decomp_L1_W30_gap730           | complete |         10 |     20 | True               | zealous-lamport                                                        |
| A4           | nowait_gap730                  | complete |         10 |     20 | False              | zealous-lamport                                                        |
| A4           | oracle_gap730                  | complete |         10 |     20 | True               | zealous-lamport                                                        |
| A4           | wait_W30_gap730                | complete |         10 |     20 | False              | zealous-lamport                                                        |
| A4           | wait_W90_gap730                | complete |         10 |     20 | False              | zealous-lamport                                                        |
| B1           | strata90_180_365               | partial  |          2 |     10 | True               | zealous-lamport                                                        |
| B1           | strata90_365_730               | partial  |          2 |     10 | True               | zealous-lamport                                                        |
| B1           | strata90_730_inf               | partial  |          2 |     10 | True               | zealous-lamport                                                        |
| B1           | strata90_90_180                | partial  |          3 |     11 | True               | zealous-lamport                                                        |
| E1           | awt_e0.4                       | complete |         10 |     50 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E1           | law_lagakos_model              | complete |         10 |     50 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E1           | law_lagakos_model_gmax_lat     | complete |         10 |     50 | False              | dreamy-fermat                                                          |
| E1           | law_lagakos_model_gmax_lat     | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | nowait                         | complete |         10 |     50 | False              | dreamy-fermat, keen-edison, magical-bardeen, zealous-lamport, zen-cray |
| E1           | nowait                         | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | odasc_W15_gmax_lat             | complete |         10 |     50 | False              | dreamy-fermat                                                          |
| E1           | odasc_W15_gmax_lat             | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | odasc_W30                      | complete |         10 |     50 | False              | dreamy-fermat                                                          |
| E1           | odasc_W30                      | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | oracle                         | complete |         10 |     50 | False              | dreamy-fermat, keen-edison, magical-bardeen, zealous-lamport, zen-cray |
| E1           | oracle                         | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | orb_W90                        | complete |         10 |     50 | False              | dreamy-fermat, keen-edison, magical-bardeen, zealous-lamport, zen-cray |
| E1           | orb_W90                        | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | wait_W30_gmax_lat              | complete |         10 |     50 | False              | dreamy-fermat                                                          |
| E1           | wait_W30_gmax_lat              | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E1           | wait_W90                       | complete |         10 |     50 | False              | dreamy-fermat, keen-edison, magical-bardeen, zealous-lamport, zen-cray |
| E1           | wait_W90                       | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E2           | law_lagakos_base               | partial  |          3 |     13 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E2           | law_lagakos_base_gmax_lat      | partial  |          5 |     25 | False              | dreamy-fermat                                                          |
| E2           | law_lagakos_base_gmax_lat      | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E2           | law_lagakos_model              | partial  |          5 |     22 | False              | dreamy-fermat                                                          |
| E2           | law_lagakos_model              | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E2           | law_naive_base                 | partial  |          2 |     10 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E2           | law_naive_model                | partial  |          2 |     10 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E2           | law_naive_model_gmax_lat       | partial  |          4 |     20 | False              | dreamy-fermat                                                          |
| E2           | law_naive_model_gmax_lat       | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E2           | nowait_gmax_lat                | partial  |          4 |     20 | False              | dreamy-fermat                                                          |
| E2           | nowait_gmax_lat                | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E3           | law_lagakos_model_ds2          | partial  |          3 |     15 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3           | law_lagakos_model_gmax_lat_ds2 | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E3           | nowait_ds2                     | partial  |          3 |     15 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3           | odasc_W15_gmax_lat_ds2         | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E3           | odasc_W30_ds2                  | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E3           | orb_W90_ds2                    | partial  |          3 |     15 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3           | wait_W90_ds2                   | partial  |          3 |     11 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3           | wait_W90_ds2                   | smoke    |          1 |      1 | False              | dreamy-fermat                                                          |
| E3b          | decomp_L1_W30                  | complete |         10 |     50 | True               | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3b          | decomp_L1_W90                  | complete |         10 |     50 | True               | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3b          | decomp_L2_W30                  | complete |         10 |     50 | True               | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3b          | decomp_L2_W90                  | complete |         10 |     50 | True               | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3b          | wait_W30                       | complete |         10 |     50 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |
| E3b          | wait_W90                       | complete |         10 |     50 | False              | keen-edison, magical-bardeen, zealous-lamport, zen-cray                |