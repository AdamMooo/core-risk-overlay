# Assessment — return-at-risk: does public credit/funding information move the *shape* of the forward return distribution beyond VIX?

Last updated: 2026-08-20. **STATUS: PROPOSAL. Not a charter, not a programme, not a queue.** This is the
written assessment [[CLAUDE]] §6 and [[docs/RESEARCH-PROTOCOL]] P11/P13 require before a fourth
programme may be argued. Nothing here authorises a run. No code exists and none is designed.

**What it would take to become a programme:** the two screens in §9 run and survive, and only then a
charter argued from the question. If Screen 0 fails, this document becomes a closure — and that is the
expected-value case for writing it.

---

## 1. Question

> Does publicly observable credit-market and funding information carry information about the **left tail
> of the forward return distribution of a broad equity index** that is *not already carried by VIX* — and
> specifically about the tail's **shape**, after conditional scale is accounted for?

Formally, with `R_{t->t+h}` the h-period forward log return and `tau` a lower probability level:

```
    Q_tau( R_{t->t+h} | X_t )  =  inf { q : P( R_{t->t+h} <= q | X_t ) >= tau }
```

The incumbent is `X_t = VIX_t`. The question is whether adding a credit/funding coordinate `C_t` changes
the estimate, and it is asked on **standardized** returns for the reason in §5.2.

## 2. Why it matters

It is the object in [[CLAUDE]] §4 stated exactly: `X_t -> P(adverse outcome given X_t)`. Not a return
forecast, not an asset recommendation, not an intervention. A positive answer would say *"current
conditions imply materially elevated exposure to left-tail equity risk, for a reason volatility does not
already price."* A negative answer closes an entire observable family cheaply, which is the outcome this
repository is built to produce.

It also tests the one door the three closures left open. [[README]] §3 scopes the prediction closure to
**public return-volatility estimators, on SPY, against VIX, at h=4 and h=13**, and says credit, funding,
breadth and positioning "were never tested and are out of scope rather than refuted."

## 3. What the literature already knows

Searched 2026-08-20. **This field is PROVISIONAL** — four queries is a scope check, not a literature
review, and [[docs/RESEARCH-PROTOCOL]] §0 field 3 is not discharged until a proper search is done. No run
happens before that.

| status | finding |
|---|---|
| **established** | The macro version of this question is answered positively. Adrian, Boyarchenko & Giannone, *Vulnerable Growth*, AER 2019 109(4):1263-89 — quantile regressions of forward GDP growth on a financial-conditions index: the **lower** quantile moves substantially with financial conditions while the upper quantile is stable and the median moves little. **The asymmetry, not the level, is the finding** |
| **established** | The **mean** version for equities is settled and negative. Welch & Goyal, RFS 2008 21(4):1455 — the default yield spread (BAA-AAA) is among the predictors that fail out-of-sample against the historical mean. This scopes our claim rather than blocking it: we are not predicting the mean, and [[CLAUDE]] §4 forbids that object anyway |
| **established** | VIX-conditioned equity quantiles have been studied directly, and the risk-return relation differs by quantile — negative at the lower tail, insignificant at the median. The incumbent's own quantile behaviour is documented, so it must be treated as a real incumbent and not a straw one |
| **established** | Mechanism sources: He, Kelly & Manela, JFE 2017 (intermediary equity capital ratio, priced across many asset classes); Brunnermeier & Pedersen 2009 (funding-liquidity spirals); He & Krishnamurthy 2013; Adrian & Shin 2010. Gilchrist & Zakrajsek, AER 2012, for the credit-spread and excess-bond-premium construction |
| **unresolved, as far as four searches can tell** | The specific encompassing test: does a credit/funding variable add to **VIX** in the conditional **lower quantile of forward equity index returns**, point-in-time, out-of-sample, on **standardized** returns? The macro analogue exists; the equity-quantile-versus-VIX literature exists; the intersection is what I could not find |
| **speculation, labelled** | That the effect, if any, is an asymmetry effect rather than a scale effect |

**If a proper search finds this settled, we stop and cite it.** [[docs/RESEARCH-PROTOCOL]] §0 field 2 is
explicit: a confidently predictable result carries no information and does not run.

## 4. What remains unresolved

1. Whether `C_t` adds anything to `VIX_t` about the forward lower quantile **at all** (§9 Screen 0).
2. Whether any such addition is **scale** or **shape** (§5.2). Only shape is a new fact about risk.
3. Whether it survives **point-in-time** construction — where the published macro versions are weakest
   (§7) and where this repository's discipline is strongest.
4. Whether it survives honest inference given **overlapping windows and a thin tail** (§8).

## 5. Candidate mechanisms

### 5.1 The mechanism, and why non-nesting is even plausible

**Risk-bearing capacity, not volatility.** When dealer and intermediary balance sheets are impaired, the
*price* of risk rises, and the compensation demanded for holding left-tail exposure rises with it.
Funding-liquidity spirals (Brunnermeier-Pedersen) and intermediary capital constraints (He-Krishnamurthy,
He-Kelly-Manela) predict that the **asymmetry** of the return distribution responds to balance-sheet
state, not merely its width.

**The fingerprint is horizon separation, and that is what makes the comparison non-trivial.** VIX is a
fast-moving, option-implied second moment with a ~30-day horizon; it reprices in hours. Intermediary
capital and credit conditions are slow state variables that adjust over quarters. If the mechanism is
balance-sheet capacity, its observable signature should appear:

- **at horizon** `h >= 4` weeks, growing to `h = 13`, and not at `h = 1`;
- **in the functional** `Q_tau` of the *standardized* return at low `tau`, and in conditional skew — not
  in conditional variance.

[[docs/RESEARCH-PROTOCOL]] §0 field 4 requires both clauses. Invisible at the proposed horizon or in the
proposed functional, and the comparison is void. Stated in advance: **if the effect appears only in
conditional variance, the answer is "nested in VIX" and the family closes.**

### 5.2 The distinction the whole assessment rests on

Write the forward return as scale times a standardized law:

```
    R_{t->t+h}  =  mu_t  +  sigma_t * Z ,       Z standardized, its law possibly depending on X_t

    Q_tau( R | X_t )  =  mu_t  +  sigma_t * q_tau( Z | X_t )
```

A lower quantile can move for two entirely different reasons, and only one of them is news:

| what moves | what it means | verdict |
|---|---|---|
| `sigma_t` | volatility is higher, so the tail sits further out | **VIX already says this.** Not a finding |
| `q_tau(Z)` | the *standardized* tail is deeper — more left-skewed at the same volatility | a claim about risk **shape**, which volatility does not carry |

So the test is run on standardized returns, `Rs = R_{t->t+h} / sigma_hat_t`, with `sigma_hat_t` a
point-in-time conditional-scale estimate, and the object is whether `C_t` enters `Q_tau( Rs | X_t )`.

This is [[CHARTER]] §2's rule in a new setting — *a difference is only a finding relative to what it is a
difference from* — and it is the same discipline as the closed programme's levels-versus-dynamics split.
**A result on unstandardized quantiles is not reportable as a shape claim at any sample size.**

## 6. What public data can observe

**Design decision, and it comes out of [[docs/POINT-IN-TIME-DISCIPLINE]] rather than out of convenience:
prefer prices to constructed indices.**

| candidate | frequency, span | PIT status | admitted? |
|---|---|---|---|
| **Moody's BAA-10Y and BAA-AAA spreads** (FRED `BAA10Y`, `BAA`, `AAA`) | daily, 1962/1986- | **clean** — yields are prices, never revised, no publication lag | **yes, primary** |
| **Term spread** (10Y minus 3M) | daily, 1962- | clean | yes, secondary |
| VIX (`^VIX` 1990-, VXO to 1986) | daily | clean | **incumbent, not a candidate** |
| Chicago Fed **NFCI** | weekly, 1971- | **revised** — the whole history is re-estimated on each release, plus a publication lag | only via ALFRED vintages, and not in Screen 0 |
| Gilchrist-Zakrajsek **excess bond premium** | monthly, 1973- | **full-sample fitted residual**, plus publication lag — §7 row 15 | descriptive only |
| He-Kelly-Manela **intermediary capital ratio** | quarterly | lag, and quarterly is too coarse for `h = 4` weeks | no |
| breadth, absorption ratio, cross-sectional dependence | — | — | **excluded — [[PARKED]] §2**, and the absorption ratio's percentile trigger already failed here (fired 76.9% of weeks in 2004-06, 4.0% in 2018-26) |
| positioning (CFTC CoT, ETF flows) | weekly, lagged | reporting lag, definitional churn | no, not in a first screen |

**The primary input is therefore a credit price, not a credit index.** That one choice removes three leak
channels before they exist.

## 7. Point-in-time — the channels this would create

New rows for [[docs/POINT-IN-TIME-DISCIPLINE]], written now rather than when they bite, per that file's
own instruction.

| # | channel | status | fix |
|---|---|---|---|
| 14 | **Index revision.** NFCI's entire history is re-estimated on each release, so today's vintage embeds the future | **LATENT** — becomes OPEN the moment NFCI enters | ALFRED vintages only, or exclude. Excluded from Screen 0 |
| 15 | **Constructed-regressor look-ahead.** The published excess bond premium is a residual from a spread model fitted over the whole sample: this is leak row 2 (parameter look-ahead) wearing a macro hat | **LATENT** | reconstruct with vintage parameters, or label as an in-sample description and never quote it as point-in-time |
| 16 | **Quantile-regression coefficients fitted on the full sample.** A `beta_tau` estimated on 1962-2026 and used to describe 1987 is the same defect | **LATENT, and the one that will actually bite** | walk-forward refit with vintage parameters, expanding window, refit cadence declared in the stub — or the number is labelled an in-sample description |
| 17 | **Publication lag.** Market prices are known same-day; macro constructs are not | **LATENT** | prices only in the screens; anything else enters with its release calendar |
| 18 | **`tau` and `h` chosen after seeing the result.** Many `(tau, h)` cells, one realized path | **OPEN by construction** | the whole quantile **curve** is reported, never one `tau` — the precedent is leak row 11's CDaR rule. `h` and the primary `tau` are declared in the stub |

## 8. Effective sample size, per coordinate — stated before any run

Weekly frequency, `h = 4` and `h = 13`, over 1962-2026 gives roughly 3,300 weekly observations. **That
number is not the sample.**

```
    independent h-week blocks      ~  T / h         ->  ~825 at h=4,  ~250 at h=13
    blocks informing tau = 0.05    ~  tau * T / h   ->  ~41  at h=4,  ~12  at h=13
```

**At `h = 13` and `tau = 0.05` the tail coordinate has effective n ~ 12, which is the same wall the closed
programmes hit, reached from a different direction** ([[README]] §4). Consequences, all declared in
advance:

- **primary coordinates are `tau in {0.10, 0.25}` at `h = 4`**, where effective n is ~80 and ~200;
- `tau = 0.05` and `tau = 0.01` are reported as **curve endpoints, not estimates**, and no magnitude is
  asserted there — [[docs/RESEARCH-PROTOCOL]] §0.1 firewall 3;
- inference uses **non-overlapping blocks or the stationary bootstrap** (Politis-Romano 1994). Overlap is
  permitted for description and never for inference (Reporting rule 3). Newey-West/Hodrick as a
  cross-check only;
- the point at which the quantile curve destabilises is **an output**, not a choice.

## 9. The cheapest first experiment

**Screen 0 — the programme-killer, and it runs first.** Cost: a few hours, two public series, no model.

1. `corr( C_t , VIX_t )` at weekly frequency, full sample and by decade, plus the lead-lag
   cross-correlation.
2. Partial association of `C_t` with the forward standardized downside of `Rs` at `h = 4`, controlling for
   `VIX_t`, with block-bootstrap standard errors.

**Preregistered reading:** if `C_t` is very highly correlated with `VIX_t` and the partial association is
indistinguishable from zero under honest standard errors, **the family closes and no charter is argued.**
That is a result, it is reportable inside this repository as a closure, and it costs one day.

**Screen 1 — only if Screen 0 survives.** Walk-forward quantile regression on standardized returns,
`VIX` alone versus `VIX + C`, compared by out-of-sample **tick (check) loss**:

```
    rho_tau(u)  =  u * ( tau - 1{u < 0} )          Koenker-Bassett 1978 check loss

    beta_tau    =  argmin over beta  of  SUM_t  rho_tau( Rs_{t->t+h} - X_t' beta )
```

with a Giacomini-White / Diebold-Mariano test on the loss differential. `X_t` is the design row
`[1, VIX_t, C_t]`; the coefficient on `C_t` at low `tau` is the object; the loss differential is the
verdict.

**Firewall, restated because it applies directly:** statistical loss never licenses an economic claim
([[docs/RESEARCH-PROTOCOL]] §0.1). The verdict vocabulary is "adds information at `(tau, h)`" or "does
not" — never "is worth acting on".

## 10. Does it deserve a charter?

**Not yet, and proposing one now would be the defect this repository names.** P13 says the cheapest
falsification runs first, and Screen 0 can end the whole line for a day's work. The correct next artefact
is **one preregistered stub for Screen 0**, not a charter.

A charter becomes arguable only if Screen 0 and Screen 1 both survive, and it would then have to be argued
from the question, with its own admissible space and its own gate.

## 11. Clearance against what is already closed or parked

Checked explicitly, because "it is not in PARKED" is not the same as "it is available".

| boundary | why this is outside it |
|---|---|
| **[[PARKED]] §4 — prediction of forward risk from public return-volatility estimators (F1, F2), permanently closed** | the inputs here are **credit and term prices**, which are not return-volatility estimators, and VIX enters as the **incumbent** rather than the challenger. The closure's own scope statement ([[README]] §3) names credit and funding as untested |
| **[[PARKED]] §4 — all trigger rules (F9), permanently closed** | the output is a conditional quantile curve. No threshold, no tier, no state label, no rule. **If the only way to express a surviving result is "so change the posture when `C` is high", it is F9 and it stops there** |
| **[[PARKED]] §0 — the mandate, parked as motivation** | there is no intervention, no instrument and no exposure decision anywhere in this document. `C2` is not referenced, because nothing here buys anything |
| **[[PARKED]] §2 — breadth, absorption ratio, cross-sectional dependence** | excluded from this proposal entirely (§6) |
| **[[PARKED]] §3b — a stochastic-volatility null** | not used. The conditional-scale estimator here is a nuisance standardizer declared in the stub, not a new null family introduced after seeing an obstruction |

**The strongest objection to this proposal, stated rather than hidden.** [[PARKED]] §1 warns that
"conditioning on decline shape is the closed prediction programme wearing a different hat", and a sceptical
reader should ask whether return-at-risk is the same trick. The differences: VIX is the incumbent rather
than the target, the input family is outside the closed one, the object is distributional shape rather than
a forecast feeding a posture, and there is no decision layer to feed. **That reasoning could be motivated,
so the test that keeps it honest is the F9 row above** — a result that can only be stated as an action is
not a result this repository accepts.

## 12. Predicted outcome, before any code

Required by [[docs/RESEARCH-PROTOCOL]] §0 field 2, and recorded so the run cannot be reinterpreted after
the fact.

- **Unstandardized lower quantiles: nests inside VIX.** High confidence, and largely derivable — credit
  spreads and VIX co-move strongly in stress. **That version therefore carries little information, and it
  is not the test.**
- **Standardized (shape) version: genuinely uncertain, and my prior is against it** — roughly 60/40 that
  no coordinate survives honest block-bootstrap inference at `h = 4`. It is not derivable from any paper I
  could find, which is what makes it worth one day.
- **What would surprise me:** `C_t` moving `q_tau(Z)` at `tau = 0.10-0.25` and `h = 4-13` with the
  conditional median unmoved — the ABG asymmetry pattern appearing in equity returns *after* VIX. That
  would establish a risk-shape fact volatility does not carry.
- **What it would change:** the standing claim that public volatility information is sufficient for
  forward equity downside description — which the closed prediction programme established for its own
  input family only.

## Related

- [[CLAUDE]] §4 (the object), §6 (standing requirements) · [[README]] §3 (the closure's scope), §6 (what
  counts as a result)
- [[docs/RESEARCH-PROTOCOL]] §0 (the gate), P11, P13 · [[docs/POINT-IN-TIME-DISCIPLINE]] (rows 14-18 above)
- [[PARKED]] §0, §1, §2, §4 (clearance) · [[docs/PROBLEM-MAP]] (the evidence the closures produced)
