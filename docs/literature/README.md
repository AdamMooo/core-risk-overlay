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
| 2 | Timmermann (2000), "Moments of Markov switching models" | J. Econometrics 96(1), 75-111 | unchecked | paywall |
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

## PDFs

Nothing is stored here yet. Most rows are paywalled journal articles, so acquisition is a manual
step through institutional access — not something to automate or route around. Rows marked `open`
have legitimate author copies or preprints.

`.gitignore` should exclude `*.pdf` in this directory before any are added, so paywalled files never
enter git history.
