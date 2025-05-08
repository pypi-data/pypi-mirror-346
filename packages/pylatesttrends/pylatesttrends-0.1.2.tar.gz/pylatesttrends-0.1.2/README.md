# pylatesttrends

A Python package that scrapes Google Trends.

## Installation

```bash
pip install pylatesttrends
```

## Usage

You can pass mandatory `geo` which takes ISO country code to get the trends from google. Other parameters are optional but follow a proper structure which is give under the Examples headings. The result value will be the pandas dataframe.

```python
from pylatesttrends import generate_payload, get_trends

payload = generate_payload("US")

result = get_trends(payload)
```

The `get_trends` also takes another optional argument which is a minimal logging that takes one of two values `print` or `logging`. When given `print` it prints logs using the native python print while `logging` uses the logging package.

```python
result = get_trends(payload, "print")
```

## Examples for Payload

### 1. Started Trending

```python
payload = generate_payload("US", start_trending="48h")
```

Following values can be used:

```plaintext
4h, 24h, 48h, 7d,
```

### 2. Category

```python
payload = generate_payload("US", category="Beauty and Fashion")
```

Following values can be used:

```plaintext
Autos and Vehicles, Beauty and Fashion, Business and Finance, Climate, Entertainment, Food and Drink, Games, Health, Hobbies and Leisure, Jobs and Education, Law and Government, Other, Pets and Animals, Politics, Science, Shopping, Sports, Technology, Travel and Transportation
```

### 3. Trend Status Active Trends

```python
payload = generate_payload("US", trend_status_active_trends=False) # value can be boolean
```

### 4. Sort By

```python
payload = generate_payload("US", sort_by="Beauty and Fashion")
```

Following values can be used:

```plaintext
title, search-volume, recency, relevance
```

### 5. Geo

```python
payload = generate_payload(geo="US")
```

Following values can be used:

```plaintext
AF, AX, AL, DZ, AS, AD, AO, AI, AQ, AG, AR, AM, AW, AU, AT, AZ, BS, BH, BD, BB, BY, BE, BZ, BJ, BM, BT, BO, BQ, BA, BW, BV, BR, IO, BN, BG, BF, BI, CV, KH, CM, CA, KY, CF, TD, CL, CN, CX, CC, CO, KM, CG, CD, CK, CR, CI, HR, CU, CW, CY, CZ, DK, DJ, DM, DO, EC, EG, SV, GQ, ER, EE, SZ, ET, FK, FO, FJ, FI, FR, GF, PF, TF, GA, GM, GE, DE, GH, GI, GR, GL, GD, GP, GU, GT, GG, GN, GW, GY, HT, HM, VA, HN, HK, HU, IS, IN, ID, IR, IQ, IE, IM, IL, IT, JM, JP, JE, JO, KZ, KE, KI, KP, KR, KW, KG, LA, LV, LB, LS, LR, LY, LI, LT, LU, MO, MG, MW, MY, MV, ML, MT, MH, MQ, MR, MU, YT, MX, FM, MD, MC, MN, ME, MS, MA, MZ, MM, NA, NR, NP, NL, NC, NZ, NI, NE, NG, NU, NF, MK, MP, NO, OM, PK, PW, PS, PA, PG, PY, PE, PH, PN, PL, PT, PR, QA, RE, RO, RU, RW, BL, SH, KN, LC, MF, PM, VC, WS, SM, ST, SA, SN, RS, SC, SL, SG, SX, SK, SI, SB, SO, ZA, GS, SS, ES, LK, SD, SR, SJ, SE, CH, SY, TW, TJ, TZ, TH, TL, TG, TK, TO, TT, TN, TR, TM, TC, TV, UG, UA, AE, GB, US, UM, UY, UZ, VU, VE, VN, VG, VI, WF, EH, YE, ZM, ZW, 
```

### 5. BaseUrl

Base Url can also be updated

```python
payload = generate_payload(geo="US", base_url="https://")
```
