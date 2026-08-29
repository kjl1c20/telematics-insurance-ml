# ML Problem Framing — Project Template

> Copy this file, rename it (e.g. `framing_churn_prediction.md`), and fill it in before writing any code.

**Project name:** *Telematics based flexible insurance*
**Date:** *2026-08-22*

---

## Step 1 — Problem Statement

**What is the problem?**

> *New drivers always needs to be subsribed to pricier insurance. If we can make use of driving data to come out with a usaged-based insurance. This could be a new product line that attracts more car insurance sales for the company*


**What is the ideal outcome?**

> *Telematics based features improves the prediction compared to just pure demographic data.*


**Existing heuristic / rule-based solution:**

> *Traditional demographic data GLM model*


**Is the heuristic sufficient?** *(Yes / No)*

> *Nope.*

> If yes — stop, don't use ML. If no — continue.

---

## Step 2 — Is ML Justified?

| Question | Your Assessment |
|---|---|
| Quality — how much better can ML realistically be? | *There is no real word quantitative comparison as I am working with synthetic data* |
| Cost — is compute + build cost justified? | *Yes, negligible* |
| Maintenance — can you retrain and monitor long-term? | *Need to figure out a source to get new data* |
| Actionability — can the prediction drive a useful action? | *Yes. We can create usage-based policy and lower the insurance package to possibly attract new car owners to subscribe to the new insurance* |

**Decision:** *(Use ML / Don't use ML)*

> *Use ML as there is potential value in the future*

---

## Step 3 — ML Framing

**Model goal** *(one sentence — what should the model predict or decide?)*

> *e.g. Predict the number of minutes a caller will wait on hold given current call centre conditions.*


**Output type** *(tick one)*:
- [ ] Binary classification
- [ ] Multiclass single-label classification
- [ ] Multiclass multi-label classification
- [x] Unidimensional regression *(e.g. predict a single number: wait time in minutes)*
- [ ] Multidimensional regression
- [ ] Generative AI

**Label (target variable):**

> *number of claims per duration*


**Candidate features:**

> Traditional/demographic: `Insured.age`, `Insured.sex`, `Marital`, `Car.age`, `Car.use`, `Credit.score`, `Region`, `Territory`, `Annual.miles.drive`, `Years.noclaims`
>
> Telematics: `Pct.drive.*` (day-of-week and rush-hour driving share), `Pct.drive.wkday`/`wkend`, `Avgdays.week`, `Total.miles.driven`, `Annual.pct.driven`, `Pct.drive.2hrs`/`3hrs`/`4hrs` (long-trip share), `Accel.*` (hard-acceleration event counts, 6 g-thresholds), `Brake.*` (hard-braking event counts, 6 g-thresholds), `Left.turn.intensity*`/`Right.turn.intensity*` (turning event intensity, 5 thresholds each)
>
> Excluded: `Duration` — used as exposure/`sample_weight`, not a predictive feature


---

## Step 4 — Metrics

**Success metric** *(business outcome — what behaviour change proves this works?)*

> No real business to measure — using model metrics (D²/lift) as a proxy for success, since there's no deployment to observe sign-up rate or loss ratio against. If piloted: sign-up rate for the usage-based tier among new/young drivers increases, since it's priced lower than the standard policy for genuinely safe drivers.


**Failure metric** *(what tells you the ML added no value?)*

> No real business to measure — using model metrics (D²/lift) as a proxy for failure too. If piloted: sign-up rate for the usage-based tier doesn't increase (though this could stem from causes other than model quality, e.g. pricing strategy or marketing, not the model itself).


**Model evaluation metric** *(e.g. RMSE, AUC-ROC, F1)*:

> *Poisson deviance and lift*


---

## Sign-off

- [ ] Problem clearly defined
- [ ] ML justified over heuristic
- [ ] Output type identified
- [ ] Success metrics defined and measurable
- [ ] Simple baseline planned before going complex
