# Leuven city-scale collective borefield — back-of-envelope study

## Context

Leuven wants to understand, before committing to detailed thermal-interference modeling, roughly how big a single collective borehole field would need to be if all the city's heat demand were served by one BEO field with a fixed 6 m grid spacing — and how that area compares to the city's own footprint. This gives policymakers an intuitive "back of the envelope" sense of scale before the expensive, granular interference study.

The starting point is a colleague's notebook (`WarmtevraagLeuven_v1.ipynb`) that already pulls Flanders' official per-statistical-sector heat-demand dataset and scales a representative residential hourly shape by it — but it currently mixes residential (kv) and industrial (gv) demand into one worst-worst-case number, has two broken/hard-coded paths, and never persists its output. GHEtool (already checked out in this repo, to be pip-installed into the user's own environment) provides the borefield sizing engine, but has no built-in "solve for area/count at a fixed depth" method — that needs a small custom loop, following the pattern already used in `GHEtool/Examples/find_optimal_borefield.py`.

Three demand cases are wanted eventually (current mixed load, kv-only, and a more realistic cooling+flat-industry variant) but only **case (a) — current mixed kv+gv load, heating only** — is being implemented end-to-end now. The pipeline should be structured so cases (b) and (c) are just parameter changes later, not rewrites.

Confirmed decisions:
- **Sector scope**: keep the colleague's existing filter `statsec_code.str.startswith("24062A")` (Leuven centrum), not the full merged municipality. This is a deliberate, revisitable scope choice, not a bug fix.
- **Notebook 1 handling**: refactor `WarmtevraagLeuven_v1.ipynb` in place (fix paths, persist output, structure into an a/b/c-ready function) rather than leaving it untouched.
- **Ground data**: use DOV's official `pydov` Python package to pull real borehole/lithology records near Leuven centrum, identify the dominant formation(s) in the top 100 m, and apply literature thermal-conductivity values per formation (from the published Flanders shallow-geothermal conductivity study) — DOV has no simple point-query API for conductivity itself. Ground temperature uses GHEtool's `GroundTemperatureGradient` with the standard Belgian ~10.5 °C surface reference and ~3 °C/100 m gradient.

## Step 1 — Refactor `WarmtevraagLeuven_v1.ipynb`

File: `C:\Users\u0169319\GHEtool\UrbanLab\WarmtevraagLeuven_v1.ipynb`

- Fix the Fluvius CSV path to the file's real location (`C:\Users\u0169319\GHEtool\UrbanLab\P6269_1_50_DMK_Sample_Gas_2024.csv`), and drop/remove the dead `statsec` cell (hard-coded path on another machine, unused).
- Keep the WFS pull (`gdf`) and the `24062A` centrum filter (`verbruik_leuven`) as-is.
- Wrap the normalized-profile + scaling logic (currently cells 7–8) into a small function, e.g. `build_hourly_heat_demand(fluvius_df, total_demand_mwh, case="a")`, that for `case="a"` reproduces today's behavior exactly (residential Fluvius shape scaled by `tot_warmtevraag_mwh`, i.e. kv+gv combined) — this is the intentional worst-worst-case. Leave clear TODO stubs (not full implementations) for `case="b"` (scale only by `wv_kv_tot_mwh`) and `case="c"` (add cooling + flat industrial profile instead of residential-shaped), so a future session can extend without restructuring.
- Fix the unit ambiguity noted during exploration (comment says "#MWh" but a `*1000` is applied) — resolve to a single clearly-labeled unit (kWh) and document it in one short comment.
- **Persist the output**: save `scaled_leuven_heat_demand_profile` (case a) to `C:\Users\u0169319\GHEtool\UrbanLab\load_profile_case_a.parquet` (indexed by hourly timestamp, kWh/h column), so the sizing notebook doesn't need to re-run this notebook.
- Add 1–2 short markdown cells documenting what the notebook does (it currently has none), since a second notebook will depend on its output.

## Step 2 — New sizing notebook

File: `C:\Users\u0169319\GHEtool\UrbanLab\BorefieldSizingLeuven_v1.ipynb`

**Setup**
- `pip install GHEtool pydov` into the user's dedicated environment; `import GHEtool as ghe`.
- Load `load_profile_case_a.parquet` from Step 1.

**Ground properties (DOV via pydov)**
- Use `pydov`'s `BoringSearch` (+ lithology/informal-stratigraphy search) within a bounding box around Leuven centrum to pull real borehole logs and characterize the dominant lithology in the top ~100 m (Leuven is expected to show Boom Clay / Diest / Brusseliaan-type formations — confirm from actual query results, don't assume).
- Map the identified formation(s) to literature thermal conductivity values (document the source/table inline as a comment, since this is the one step without a direct programmatic value).
- Ground model: `ghe.GroundTemperatureGradient(k_s=<from pydov+literature>, T_g=10.5, gradient=3.0)` (default volumetric heat capacity unless pydov data suggests otherwise).
- Note the DOV/pydov step as the weakest link in the chain (literature lookup, not a direct measurement) — call this out explicitly in a markdown cell as an assumption for the reader.

**Load**
- Build both a monthly-aggregated load (`MonthlyGeothermalLoadAbsolute`, from summing/peaking the hourly series per month) for the fast search loop, and keep the full hourly series for a final validation pass.
- `simulation_period = 40` on whichever load object is used.
- Heating-only for case (a): extraction load only, no injection/cooling.
- Set reasonable fixed defaults for Rb (~0.12 K/W, typical single U-tube) and fluid temperature limits (e.g. 0 °C min / 16 °C max), documented as assumptions consistent with GHEtool's example scripts — not the focus of this back-of-envelope study.

**Fixed-depth sizing loop** (pattern from `GHEtool/Examples/find_optimal_borefield.py`, since GHEtool has no built-in inverse solve-for-area method):
```python
borefield = ghe.Borefield(ground_data=ground_data, load=monthly_load)
borefield.Rb = 0.12
borefield.set_max_fluid_temperature(16)
borefield.set_min_fluid_temperature(0)

N = start_count
while True:
    side = int(np.ceil(np.sqrt(N)))
    borefield.create_rectangular_borefield(side, side, 6, 6, 100, 1, 0.075)
    depth_needed = borefield.size_L3()
    if depth_needed <= 100:
        break
    N += step
```
- Once found, validate the winning configuration with `size_L4()` on the full hourly load as a sanity check (L3 monthly for the search loop is fast; L4 hourly confirms accuracy for the final answer).
- Report: `number_of_boreholes`, field footprint area (`(side-1)*6` per side, plus note that real extent is slightly larger due to borehole radius/edge buffer), total drilled length.

**Comparison to city area**
- Compute Leuven centrum's area directly from `verbruik_leuven.geometry` (sum of polygon areas in its native projected CRS, in m² → convert to ha/km²) rather than hardcoding a figure — reuses Step 1's `gdf`/`verbruik_leuven` output.
- Report the borefield footprint as a percentage of that area.

## Step 3 — Maps

In the same sizing notebook (or a final section of it):
- Plot the Leuven centrum sector boundary (reusing the geopandas approach from Notebook 1 — no basemap library is currently installed, so keep it consistent plain-geopandas/matplotlib unless the user wants to add `contextily` for a basemap).
- Overlay the sized borefield's footprint (as a scaled rectangle/patch, using real borehole `(x, y)` coordinates from `borefield.borefield`) at true scale on or beside the city map, so the size difference is visually obvious.
- Include a small summary table/annotation: total heat demand (GWh/yr), number of boreholes, total drilled length (m), field area (ha), % of Leuven centrum area.

## Verification

- Run both notebooks top-to-bottom in the user's environment (`jupyter nbconvert --execute` or interactively) and confirm: Step 1 produces a saved parquet with sane hourly kWh values (order of magnitude check against `tot_warmtevraag_mwh`), Step 2's sizing loop converges to a required depth ≤ 100 m with a plausible borehole count (sanity-check against a rough manual estimate — total GWh/yr ÷ typical extraction per borehole), and Step 3 renders a map where the borefield footprint is visibly plausible relative to Leuven centrum's outline.
- Flag clearly in the notebook (markdown) which numbers are hard assumptions (Rb, fluid temp limits, DOV-derived conductivity) versus directly computed from data, so the reader can judge sensitivity.
