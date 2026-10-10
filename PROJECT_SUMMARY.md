# What Determines the Price of a Used Car in South Africa, and Which Vehicles Offer the Best Value?

**Findings summary** · Analysis of 9,992 cleaned used-vehicle listings (January to September 2026) · Power BI

---

## Executive summary

Age and model explain almost everything about a used car's price in this dataset. Once you know a car's make, model and age, you can predict its price to within a few percent. Mileage adds a little more. Everything else I tested (transmission, service history, number of previous owners, province, colour) adds essentially nothing.

Value loss is steep and similar across the market. A car loses about half its value by 6 to 8 years and about two-thirds by 9 years or more, and premium brands depreciate at almost the same rate as mass-market brands. Pricing is far less consistent than the underlying economics: about 4 in 10 listings are priced more than 10% away from comparable cars, which creates a clear opportunity to flag bargains and overpriced listings.

| Headline number | Value |
|---|---|
| Listings analysed | 9,992 |
| Average / median price | R318,726 / R277,678 |
| Share of price variation explained by make, model and age | about 95% |
| Value kept after 3-5 / 6-8 / 9+ years | 74% / 53% / 36% |
| Listings priced below / fairly / above similar cars | 20% / 60% / 20% |
| Best-value listings found | 230 |

---

## The six business questions

### 1. Which brands are most popular?

Toyota dominates with 1,948 listings (19.5% of the market), followed by Volkswagen (1,097, 11.0%) and Ford (841, 8.4%). Those three brands account for about 39% of all listings. Suzuki and BMW complete the top five, and BMW is the only premium brand among them. Premium brands make up about 18% of listings and mass-market brands about 82%.

The top models are all Toyotas: Hilux (351), Corolla Cross (347), Corolla (346), Starlet (308) and RAV4 (303).

### 2. Which cars retain their value?

Comparing the median price of older cars with the median price of 0 to 2 year old cars of the same kind:

| Age | Value kept |
|---|---|
| 3-5 years | about 74% |
| 6-8 years | about 53% |
| 9+ years | about 36% |

Brand matters less than people assume. At 6 to 8 years, brands with at least 50 listings keep between about 47% (Mazda) and 59% (BMW) of their value, a spread of 12 points. At model level, Renault Clio (about 62%) holds value best and Renault Duster (about 45%) holds it worst.

Premium and mass-market cars follow almost the same depreciation curve. Four years in, both retain about 70% of their age-zero price, and by 12 years both are at 28% to 29%. Expensive models do not hold their value any better or worse than cheap ones: the correlation between a model's price and its retention is close to zero.

### 3. What factors drive vehicle prices?

| Factor | Effect on price |
|---|---|
| **Age** | Very strong. Average price falls from R542K for a brand-new-age car to R154K at 12 years |
| **Mileage** | Very strong. R536K under 20,000 km, down to R170K above 150,000 km |
| **Make and model** | Very strong. Model alone explains about half of price variation |
| **Vehicle type** | Strong. Hatchbacks average R151K, sedans R276K, SUVs R383K and bakkies R398K |
| **Fuel type** | Strong, but overlaps with vehicle type. Petrol averages R281K against R404K to R429K for diesel, hybrid and electric, partly because diesel is concentrated in bakkies and SUVs |
| **Engine size** | Moderate (correlation about 0.4) |
| **Transmission** | Negligible |
| **Service history** | Negligible. Full, partial and no service history average within R5,000 of each other |
| **Previous owners** | None |
| **Province, colour** | None |

To quantify this, I fitted a simple model of log price. Age alone explains about 48% of the variation, and model alone about 49%. Together they explain about 95%. Adding mileage raises that to about 97%. Adding transmission, service history, province and colour to the model changes nothing.

### 4. Which provinces have the highest demand?

Measured by listing volume (the data has no views or enquiries), demand is concentrated in three provinces: Gauteng (3,157 listings, 31.6%), Western Cape (1,881, 18.8%) and KwaZulu-Natal (1,507, 15.1%). Together they hold about 65% of all listings. Northern Cape is the smallest market with 209 listings.

### 5. Are listings priced competitively?

Each listing was compared with the average price of cars of the same make, model and year.

- 60% are priced fairly (within 10% of comparable cars)
- 20% are priced at least 10% below
- 20% are priced at least 10% above

So pricing is inconsistent: 4 in 10 listings sit well away from the benchmark. This does not vary much by province. The share of below-market listings ranges only from about 18% (Mpumalanga) to 24% (Northern Cape). The data has no seller-type column, so I could not split dealers from private sellers, and the analysis answers the question for listings in general.

### 6. Which vehicles offer the best value?

A cheaper listing is often just a higher-mileage car (the correlation between price gap and mileage gap is about -0.4). To avoid recommending those, I defined a **best-value** listing as one that meets all four conditions:

1. Priced at least 10% below comparable cars
2. Mileage at or below the average for comparable cars
3. At least 5 comparable cars in the group, so the benchmark is reliable
4. Full service history

This gives **230 listings**. They are concentrated in Gauteng (79), Western Cape (48) and Limpopo (25), and by brand in Toyota (46), Volkswagen (27) and Ford (22), which largely mirrors market size.

---

## What this means for a used-car marketplace

1. **Offer a price guide built on make, model and age.** These three factors explain about 95% of price variation, so a guide built on them would be accurate enough to flag listings priced more than 10% away from the benchmark.
2. **Surface best-value listings.** The 230 listings that are cheap, low-mileage and fully serviced are the ones buyers most want to see. A "best value" badge based on the four rules above is simple to build and explain.
3. **Do not expect service history or ownership count to explain price.** In this data they do not, so a pricing tool does not need to rely on them. (See the limitations below before drawing a general conclusion.)
4. **Prioritise supply and marketing in the three largest provinces,** while treating that as a listing-volume signal and not as proof of demand.
5. **Set buyer expectations on depreciation.** A car loses about a quarter of its value by 3 to 5 years and roughly half by 6 to 8, whatever the brand.

---

## Data quality notes

The raw file contained 10,025 rows. I removed 25 duplicates, 4 listings with impossible or outlier years, and 4 with impossible prices, leaving 9,992. I standardised brand names (63 spellings of 20 brands), provinces, fuel types and transmissions, set 4 impossible mileage values and the 0.0 L engine size of 116 electric vehicles to blank, and filled blank City, Colour and Service_History values with "Unknown".

Two patterns look like placeholder values: 459 listings at exactly 2,500 km and 37 at exactly R59,900. I kept these rows and flagged them (494 in total, `Placeholder_Flag`). They are priced about 4% above comparable cars on average, but the dashboard conclusions hold with or without them.

---

## Limitations

- **No seller type.** Dealers cannot be separated from private sellers.
- **No demand measure.** There are no views, enquiries or days-to-sell figures, so listing volume stands in for demand.
- **No original price.** Retention compares different cars of the same model at different ages at one point in time. It is a market snapshot, not the tracked depreciation of individual cars.
- **Benchmarks are internal.** "Below market" means below the average of comparable cars in this dataset, not below an official valuation guide.
- **Age and mileage are correlated,** so their separate effects are hard to untangle. The model estimate treats them jointly.
- **Missing condition information.** Accident history, trim level and condition are not in the data, so "best value" is a shortlist, not a guarantee.
- **Validate before generalising.** Some results, such as service history having no effect on price, differ from what is commonly reported in the market. They should be checked against live listing data before being treated as general facts.
