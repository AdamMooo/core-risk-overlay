# Literature

Last updated: 2026-08-13

Acquisition worklist for the `RESEARCH-PROTOCOL.md` §11 reading list. §11 carries the *status marks*
and the reason each paper matters; this file carries *metadata and whether we have it*.

Under protocol §0.3 an `[UNREAD]` paper whose question is about to be investigated empirically
**blocks that experiment.** This file exists so "I couldn't find it" is never the reason a finding
gets rediscovered instead of read.

## Metadata is UNVERIFIED

Every citation below was written from memory in one pass and **volume, issue and page numbers are
not yet checked against the sources.** Do not quote any of it in README.md, the hub, or the protocol
until the row is verified and its `meta` column flipped to `ok`. Rows flagged `verify!` are ones I am
actively unsure about, not merely unchecked.

This warning is itself an application of §0 — the repo just spent a run on a result that was already
in a cited paper, and the correction cannot be a second layer of unverified assertions.

## Acquisition status

`have`: PDF present in this directory. `paywall`: needs institutional access. `open`: freely
available preprint or author copy exists.

| # | citation | venue | meta | have |
|---|---|---|---|---|
| 1 | Rydén, Teräsvirta & Åsbrink (1998), "Stylized Facts of Daily Return Series and the Hidden Markov Model" | J. Applied Econometrics 13(3), 217-244 | unchecked | paywall |
| 2 | **Timmermann (2000), "Moments of Markov switching models"** | J. Econometrics 96(1), 75-111 | venue/vol/pages **ok** | **HAVE and READ** — open author copy, LSE FMG DP 323 (May 1999), `Timmermann-1999-Moments-of-MS-Models-LSE-FMG-DP323.pdf` |
| 3 | Cont (2001), "Empirical properties of asset returns: stylized facts and statistical issues" | Quantitative Finance 1(2), 223-236 | unchecked | open |
| 4 | Hamilton (1989), "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle" | Econometrica 57(2), 357-384 | unchecked | paywall |
| 5 | Hamilton & Susmel (1994), "Autoregressive conditional heteroskedasticity and changes in regime" | J. Econometrics 64(1-2), 307-333 | unchecked | paywall |
| 6 | Gray (1996), "Modeling the conditional distribution of interest rates as a regime-switching process" | J. Financial Economics 42(1), 27-62 | unchecked | paywall |
| 7 | Haas, Mittnik & Paolella (2004), "A New Approach to Markov-Switching GARCH Models" | J. Financial Econometrics 2(4), 493-530 | unchecked | paywall |
| 8 | Klaassen (2002), "Improving GARCH volatility forecasts with regime-switching GARCH" | Empirical Economics 27(2), 363-394 | unchecked | open |
| 9 | Ang & Bekaert (2002), "International Asset Allocation With Regime Shifts" | Review of Financial Studies 15(4), 1137-1187 | unchecked | paywall |
| 10 | Guidolin & Timmermann (2007), "Asset allocation under multivariate regime switching" | **verify!** believed J. Economic Dynamics and Control 31(11) | **verify!** | paywall |
| 11 | Magdon-Ismail, Atiya, Pratap & Abu-Mostafa (2004), "On the maximum drawdown of a Brownian motion" | **verify!** believed J. Applied Probability 41(1), 147-161 | **verify!** | paywall |
| 12 | Berkowitz (2001), "Testing Density Forecasts, With Applications to Risk Management" | J. Business & Economic Statistics 19(4), 465-474 | unchecked | paywall |
| 13 | Christoffersen (1998), "Evaluating Interval Forecasts" | International Economic Review 39(4), 841-862 | unchecked | paywall |
| 14 | Engle & Manganelli (2004), "CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles" | J. Business & Economic Statistics 22(4), 367-381 | unchecked | open |
| 15 | Kupiec (1995), "Techniques for verifying the accuracy of risk measurement models" | **verify!** believed J. Derivatives 3(2), 73-84 | **verify!** | paywall |
| 16 | Diebold & Mariano (1995), "Comparing Predictive Accuracy" | J. Business & Economic Statistics 13(3), 253-263 | unchecked | paywall |
| 17 | Giacomini & White (2006), "Tests of Conditional Predictive Ability" | Econometrica 74(6), 1545-1578 | unchecked | paywall |
| 18 | Diebold, Gunther & Tay (1998), "Evaluating Density Forecasts with Applications to Financial Risk Management" | International Economic Review 39(4), 863-883 | unchecked | open |
| 19 | Andersen & Bollerslev (1998), "Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts" | International Economic Review 39(4), 885-905 | unchecked | paywall |
| 20 | Fissler & Ziegel (2016), "Higher order elicitability and Osband's principle" | **verify!** believed Annals of Statistics 44(4), 1680-1707 | **verify!** | open |
| 21 | Frühwirth-Schnatter (2006), *Finite Mixture and Markov Switching Models* | Springer | unchecked | paywall |
| 22 | Christoffersen & Pelletier (2004), "Backtesting Value-at-Risk: A Duration-Based Approach" | **verify!** believed J. Financial Econometrics 2(1) | **verify!** | paywall |
| 23 | **Marcucci (2005), "Forecasting Stock Market Volatility with Regime-Switching GARCH Models"** | Studies in Nonlinear Dynamics & Econometrics 9(4), DOI 10.2202/1558-3708.1145 | venue+DOI **ok** (checked 2026-08-14) | paywall; an encrypted PDF exists at greta.it that this environment cannot render |
| 24 | **Patton (2011), "Volatility forecast comparison using imperfect volatility proxies"** | J. Econometrics | unchecked | paywall |
| 25 | **Kandji & Misko (2024), "Markov-Switching Normal-Mixture GARCH"** | Nexialog Consulting working paper, Paris, 30 May 2024 | title/authors/date **ok** — read from the PDF itself | **have** (`Markov-Switching-Normal-Mixture-GARCH-Nexialog.pdf`, gitignored) |

## Reading order, and why

Rows 1-3 first, and nothing else runs until they are read. Between them they contain both of this
repo's headline empirical "findings":

- **Row 1** — an HMM fails on the slow decay of squared-return autocorrelation. That is the ARCH-LM
  rejection at 55.6 ($p = 2.4\times10^{-11}$), published 1998.
- **Row 2** — closed-form MS moments, which give the $h=1$ near-equivalence with an EWMA
  analytically, without running anything.
- **Row 3** — daily returns are materially more leptokurtic than weekly, which is the specification
  cost of the §1.3 frequency decision.

Rows 9-11 next: they are the only entries that address the model at the horizon the mandate names.
Row 11 is the one paper here about a *path* functional rather than a marginal.

Rows 5-8 are S3 and S4 and should be read before either is implemented, not after.

**Row 5 is additionally the live blocker on `../STUB-GARCH-ENCOMPASSING.md` (2026-08-14).** Hamilton
& Susmel is on **U.S. weekly stock returns** — the only exact frequency match in this table — and
its out-of-sample forecast comparison could not be obtained at any access level short of
institutional. Row 23 (Marcucci) was adjudicated **INFORMS, not SETTLED** from its abstract, on
four documented axis mismatches; that adjudication is recorded in the stub §14.2 and does not need
repeating. **Row 5 does.**

Note both row 5 and row 23 put ARCH *inside* the regimes — SWARCH and MRS-GARCH respectively. Both
are therefore evidence about **S3**, not about the plain switching-variance model this repo fits.
That distinction is easy to lose and has already been lost once.

## Row 5 — Hamilton & Susmel (1994): acquisition attempted 2026-08-14, FAILED

Recorded so the search is not repeated. **The paper is NOT read. Nothing about its findings is
recorded anywhere in this repo, and no secondary source may be substituted** — the standing
instruction is that abstracts, citations, search snippets and papers-that-cite-it do not count.

| route | outcome |
|---|---|
| Hamilton's own page, `econweb.ucsd.edu/~jhamilto/` | paper listed; **no PDF**. Hosts `SWARCH.ZIP` — replication *data and software only*. Code cannot establish horizons or conclusions and was not used. |
| Susmel's own page, `bauer.uh.edu/rsusmel/Academic/pub.htm` | paper listed among publications; **no PDF link**, unlike 11 of his other papers which do have one. |
| ScienceDirect, PII `0304407694900671` | abstract only; full text paywalled. |
| general search | secondary sources only — papers citing it, textbook summaries. Excluded by the standing instruction. |

**Environment limitation, updated 2026-08-14 after row 25 was read successfully.** PDF *rendering*
is unavailable (`pdftoppm`/poppler not installed), but raw text-stream extraction works on
**unencrypted, born-digital** PDFs — row 25 was read that way in full.

| PDF kind | readable here? |
|---|---|
| unencrypted, born-digital (LaTeX/Word origin) | **yes** — row 25 proved it |
| encrypted (typical publisher DRM) | no — the Marcucci PDF failed on this |
| scanned page images | no — would need OCR, unavailable |

**So a PDF of Hamilton & Susmel may work, and is worth trying before transcribing anything.** A
1994 Elsevier scan probably will not. If extraction fails, pasted text or a `.txt`/`.md` file in
this directory is the fallback.

### To be filled when the primary text is available — NOT before

| | |
|---|---|
| **What the paper establishes** | *(empty — paper unread)* |
| **What it does NOT establish for the plain-MS vs GARCH density experiment** | *(empty — paper unread)* |

Then apply the existing `../STUB-GARCH-ENCOMPASSING.md` §14.1 adjudication — SETTLED / INFORMS /
ORTHOGONAL. **No new gate is to be invented.**

## Row 2 — Timmermann: READ IN FULL 2026-08-14. Now the live literature gate.

Source: **LSE Financial Markets Group DP 323 (May 1999)**, the author's institutional working-paper
copy of what became *J. Econometrics* 96(1), 75-111. Freely available, downloaded, text extracted
in full. **Version caveat: working paper, not the published article.**

**Why it displaced Hamilton & Susmel as the blocker.** A fact changed, not a preference. Kandji &
Misko (row 25) established that **SWARCH is MS-*ARCH*** — rung 4 — while Timmermann's model (1),
`y_t = mu[S_t] + sigma[S_t] eps_t`, iid innovations, no within-regime dynamics, **is exactly this
repo's specification**. Row 5 stays open at lower priority; it was not dismissed.

**What the paper establishes**

- Closed-form unconditional variance, skewness and excess kurtosis for the two-state Gaussian MS
  model (**Corollary 1**), and the autocovariance function of levels and squares (**Propositions
  4-5**).
- **Skewness requires the state MEANS to differ.** Variance switching alone cannot generate
  skewness, at any transition matrix. His footnote pairs this with Bollerslev (1986): standard
  GARCH without leverage has **zero** skewness.
- MS on data with small means in every state "may have trouble replicating successfully the
  skewness found in these data."
- Squared-value autocovariance decays through `vec(P^n)`, i.e. geometrically at
  `lam = p11 + p22 - 1`, positive iff the chain is persistent (`p11 + p22 > 1`).

**What it does NOT establish for this experiment**

- **No forecast comparison of any kind, and no GARCH benchmark** beyond the skewness footnote.
- **Unconditional** moments and ACF only — never a *conditional* h-step predictive density, which
  is our functional. The `2^h`-regime-path mixture conditional on `xi[t]` is untouched.
- Nothing about horizons, out-of-sample evaluation, encompassing, or power.

**Verdict under `../STUB-GARCH-ENCOMPASSING.md` §14.1: INFORMS.** Sharpens the design materially
(stub §14.3), does not settle the question, does not kill the run.

**It also triggered a §0 rule 3 process failure** — `memory_diagnostic.py`'s 2026-08-13 "deductive
result" is Timmermann's Proposition 5, published 1999, sitting `[UNREAD]` as row 2 of this very
list, with the reading-order note already flagging what it contained. Logged in
`../RESEARCH-PROTOCOL.md` §Amendments. The repo's version also omits the mean terms and overstates
the autocovariance by **1.00%** at the fitted parameters.

## Row 25 — Kandji & Misko (2024): READ, adjudicated 2026-08-14

**Read in full from the primary text**, not from an abstract. Supplied 2026-08-14. **It is not
Hamilton & Susmel and does not clear that gate** — it cites H&S exactly once, in its introduction,
as the originator of MS-GARCH. That is a secondary citation and the standing instruction excludes it.

**Verdict under `../STUB-GARCH-ENCOMPASSING.md` §14.1: ORTHOGONAL, shading to INFORMS.**

| axis | Kandji & Misko (2024) | our experiment | match |
|---|---|---|---|
| frequency | **daily** | weekly | no |
| asset | **CAC 40** | SPY / QQQ | no |
| horizon | **1 day, 1 week** | 4 / 13 / 26 weeks | no |
| regime model | **MS-NM-GARCH** — GARCH inside regimes *and* normal-mixture innovations | plain MS | no (above rung 4) |
| opponent | GARCH(1,1), NM-GARCH | GARCH(1,1) | partial |
| functional | conditional volatility; conditional density percentiles | h-step predictive density | partial |
| evaluation | log-likelihood, fitted parameter tables, forecast plots | walk-forward, encompassing, Giacomini-White | no |

**What the paper establishes:** stationarity conditions for MS-NM-GARCH, and — claimed as a first
for the MS-GARCH class — **strong consistency of the MLE**, plus an EM/Hamilton-filter estimation
algorithm. Applied to daily CAC 40, it reports better density percentile estimation than GARCH(1,1)
and NM-GARCH.

**What it does NOT establish for our experiment:** anything. It never fits a plain MS model, never
tests weekly US equity data, and its longest horizon is one week against our shortest of four.

**Two things in it that genuinely INFORM our design, and are the reason this row is not simply
discarded:**

1. **Why SWARCH is MS-*ARCH* rather than MS-GARCH — a constraint, not a preference.** The paper
   states that MS-GARCH inference is *"very difficult due to the path dependence of the likelihood
   on the latent factor. In practice, only MS-ARCH models are considered to avoid this dependence,
   leading to a persistence loss."* Haas et al. (2004b) later gave a path-dependence-free variant.
   **Consequence for us:** the S3 rung is harder than the ladder makes it look, and Hamilton &
   Susmel's choice of ARCH was likely forced. This is context for reading H&S — **it is not a
   substitute for reading it.**
2. **An identification warning that lands squarely on our parameters.** The paper notes that where
   regimes are **persistent** — *"low probabilities of state change, such as in stock markets"* —
   an MS-GARCH may struggle *"to arbitrate between capturing the non-normality of the innovations
   and effectively filtering states."* **Our $\lambda = 0.9126$ is exactly that case.** So fat tails
   and regime switching may be weakly separately identified here. This bears on the stub's §12
   Gaussian-vs-Student-$t$ sensitivity — which assumes the tail assumption and the variance dynamics
   can be told apart — and more heavily on S3 if it is ever run. **Recorded as a caveat to inherit,
   not acted on: the design is frozen and this does not motivate a new control.**

## PDFs

Nothing is stored here yet. Most rows are paywalled journal articles, so acquisition is a manual
step through institutional access — not something to automate or route around. Rows marked `open`
have legitimate author copies or preprints.

`.gitignore` should exclude `*.pdf` in this directory before any are added, so paywalled files never
enter git history.
