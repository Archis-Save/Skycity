# Order Channel Performance and Market Share Analytics — SkyCity Auckland Restaurants & Bars

## Overview
Historical analytics of In-Store, Uber Eats, DoorDash and Self-Delivery ordering channels.

## Dataset
- Records: 1,696
- Unique restaurants: 1,696
- Subregions: CBD, North Shore, South Auckland, West Auckland
- Cuisines: 8
- Segments: 4
- Represented orders: 2,019,134

## Validation
All 1,696 records reconcile exactly: channel order counts sum to MonthlyOrders.

The supplied InStoreShare and delivery-channel shares are retained according to their definitions. Overall channel share is recalculated from channel order counts, rather than forcing the supplied share fields to sum to 100%.

## Overall Channel Share
- Uber Eats: 39.6%
- DoorDash: 21.6%
- Self-Delivery: 20.4%
- In-Store: 18.4%

## Key Findings
- Average combined Uber Eats + DoorDash dependence: 62.3%
- Records at or above 70% combined aggregator dependence: 603
- Records with any single channel at or above 70%: 0
- Uber Eats is the largest channel by total represented order volume.

## Dashboard
Includes channel mix, subregion heatmap, cuisine/segment comparisons, dependency risk, channel diversity, revenue and net-profit comparisons.

## Run
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Interpretation
The channel shares describe the supplied dataset, not necessarily the entire Auckland hospitality market. Market representativeness should be confirmed before using the results as city-wide market-share estimates. Financial values are based on the supplied cost and commission assumptions.
