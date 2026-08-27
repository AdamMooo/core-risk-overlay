---
type: project
---

# Core-Risk-Overlay

Last updated: 2026-08-26

**NO ACTIVE RESEARCH PROGRAMME.** Three have run and all three are closed — see [[README]]. This file
is the chronological record. **Repository purpose and agent behaviour are [[CLAUDE]].** **The last
programme's termination is [[CHARTER]] §11.** Process in [[docs/RESEARCH-PROTOCOL]]. Time-basis rules
in [[docs/POINT-IN-TIME-DISCIPLINE]]. Frozen evidence in [[docs/PROBLEM-MAP]]. Excluded, including the
hedging mandate, in [[PARKED]].

**The repository name is historical.** It names a program that no longer runs.

## Status — 2026-08-26, ninth entry: THE SHALLOW HALF IS SCORED — Z1 HOLDS, Z2 FAILS, Z5 TRIGGERS ITS FAILURE BRANCH; N1/N2 RUNNING AT CLOSE

> **The four Ledoit–Wolf contracts are written and all 55 checks pass** (commit d1865a8). An
> independent adversarial audit against the paper and the preregistration returned **zero defects on
> the mathematics** and four findings on the harness — the Z2 pain margin was written on the wrong
> side (a lower-is-better functional given the Sharpe test's geometry), the shallow path functionals
> ran on the excess curve where the margins were calibrated on the net curve, M was 999 not 4999 for
> the percentile half, and leave-one-episode-out omitted the deep functionals so Z5 had nothing to be
> read from. **All four were amended deductively, in the Z0-amendment format, before any interval was
> read** (commit 52fa60e); the first execution's output is renamed unread
> (`data/inference.superseded.log`) and the corrected run reproduces the frozen tables exactly.
>
> **Z1 HELD.** The Sharpe difference is not distinguishable anywhere: headline max-p 0.67 / 0.62 /
> 0.55 for (75,55) / (80,60) / (85,65); no cell below 0.53. (The Z1 basis's "0.44 vs 0.44" cited the
> paper-35 row; the declared benchmark paper-25 sits at 0.398 against the band's 0.444 — delta +0.045,
> verdict unaffected.)
>
> **Z2 FAILED, on both functionals, for every band.** The Sharpe intervals are ±~0.21 wide against a
> ±0.10 margin — the margin sits inside one standard error — and the pain intervals reach past +1.0pp
> everywhere. Per the preregistration's own failure clause, **Y1 weakens from "matches or beats" to
> "not shown to be worse."** The equivalence question is the effective-sample-size wall again, now
> visible on the shallow half: 34 years cannot resolve ±0.10 Sharpe.
>
> **Z5 triggered its failure branch for the two tight bands.** The (80,60) and (75,55) deep-tail gaps
> are stable to dropping the dot-com, the GFC, or both (−1.4/−1.6/−2.0pp essentially unchanged) — the
> preregistered "one descriptive result that would make the residual worth attributing", and it
> **raises D8's priority** exactly as written. The (85,65) gap collapses without the two episodes
> (−14pp → −0.7pp, MaxDD flips sign), the exposure confound behaving as pre-recorded.
>
> **The machinery's measured size, from a known-truth simulation at the market's fitted persistence
> (0.9932):** the 6-block max-p rule's true size is ~7% at T≈8,560 (individual cells 7.5–9.5%),
> invariant to pair correlation (checked at rho 0.70 and 0.80; measured JM-band correlations are
> 0.73–0.80), sourced in the HAC estimate, not the block bootstrap. Direction of the caveat:
> strengthens Z1's non-rejection (the test over-rejects and still did not), and Z2's failure is robust
> (the true intervals are wider than the printed ones, which already failed).
>
> **N1 and N2 were resumed 21:43 (commit 6d7d897 made the writers resume-safe) and were still running
> at session close.** Each null persists to `data/deeptail_mc.csv` on completion. **Z3 and Z4 are the
> only open verdicts; Thread A does not close until they are scored.** Next session: score them from
> the CSV (observed-vs-null percentiles per band × statistic, the intersection–union reading for Y2),
> write the run section in [[docs/REPRO-SJM2024-FINDINGS]] once and whole, regenerate the manifest
> (`deeptail_mc.csv` plus run logs are the expected mismatches), and record the three cosmetic audit
> notes there (eigenvalue-not-singular-value shrink on a dead branch; "one-day lag" naming a shift(2)
> shared identically by both halves; per-grid-row seed reuse, marginally harmless).

## Status — 2026-08-26, eighth entry: THE INFERENCE RUN IS PREREGISTERED AND HALF-EXECUTED — Z0 PASSES, N1 AND N2 ARE STILL OWED

> **Thread A's closing item is committed and running.** The preregistration is
> [[docs/REPRO-SJM2024-FINDINGS]] §"Preregistered for the inference run" — the nine-field §0 gate, Z0–Z5,
> and an explicit *what may be said afterwards*, all written before any inference code. Three departures
> from the 2026-08-25 plan were taken and argued in place: **intersection–union instead of Bonferroni**
> (Y2 claims the JM beats *every* band, so the null is a union, the statistic is the max p-value, and the
> level is exactly alpha with no correction); the block size is a **declared grid** {5,10,21,42,63,126}
> with max-p as the headline rather than Ledoit–Wolf's calibration algorithm, which targets T=120 monthly
> and would be a larger simulation than the test it serves at T≈8,560 daily; and Y1 gets an **equivalence
> margin** (0.10 Sharpe, 1.0pp pain), because failing to reject licenses nothing.
>
> **Z0 was mis-specified and was amended before the scoring run, on a deductive argument.** It required
> N3's gap distribution to centre on zero, which presumes the two rules are exposure-matched. They are
> not — the volatility-threshold table in the same document already said so — so the control now tests
> that each gap's **sign agrees with its exposure difference**, and a non-zero centre is expected.
> Exposure-matching became **open item 7** rather than a mid-run redesign: changing a comparison after
> its preregistration is committed is the exact defect the preregistration exists to prevent.
>
> **Z0 PASSES, and it is the only thing scored.** All 200 N3 paths produced finite gaps, and on all
> three bands the jump model holds the market less and shows the shallower deep tail — sign agreement on
> the centre of all nine band × statistic distributions, 72–81% path by path at a correlation of only
> +0.17. The pipeline does not manufacture a difference.
>
> **The run then stopped before N1 produced a path.** N3 finished 12:42; the process was gone by 13:08
> with no N1 or N2 rows. Cause undiagnosed. Both null *fits* had already succeeded and are cached, so a
> resume re-fits nothing. **Z3 and Z4 are unscored, and Thread A does not close until they are.**
>
> **What the control exposed in passing:** the jump model's exposure deficit is **30–42pp** under i.i.d.
> returns against **2.4–12.0pp** observed. Stripped of clustering the fitted state carries nothing and
> the rule collapses to holding cash. Not a Z0 failure — N3 is a machinery check — but it means N3's gap
> magnitudes (−7 to −11pp) are **not** a calibration for the observed ones (−0.70pp) and must not be read
> as one. N1 is the null that self-calibrates the exposure confound, and N1 is the run still owed.
>
> **Also: [[docs/MATH-REFERENCE]] was split.** §1, §6, §7 and two §5 definitions moved verbatim to the
> closed intervention's own reference; §2–§5 stay and now justify themselves by what currently runs.
> §3 turned out to govern more than it was written for — "max drawdown is an extreme-value functional
> with effective n = 1" was written about one path, and a *difference* of two of them inherits the
> defect. That is the whole argument for sending the deep half to explicit simulation rather than to a
> block bootstrap whose answer would be a property of the block length.
>
> **Next, in order:** resume `deeptail_mc.py --null N1 --null N2`; write the four contracts left
> unimplemented in `src/ledoitwolf.py` (delta-method gradient, block-structure Psi, circular resampler,
> studentized test) so the shallow half can run; then score Z1–Z4 and write the run section. Thread B is
> untouched and still has one decision open before code.

## Status — 2026-08-25, seventh entry: THE LEDGER GETS KILL CONDITIONS, AND THREAD A'S SCOPE IS CUT FROM FOUR ITEMS TO ONE

> **No code ran. Two decisions, both scope-reducing, and the goal restated because the question was
> asked directly.** The operating goal is [[CLAUDE]] §4/§9 as written — determine what is true about
> systematic risk from public data; a **closure is a delivery**; no result here carries a usability or
> profitability requirement. Progress is measured in closures, not commits.
>
> **The live-thread ledger is now explicit, and every thread carries a written kill condition and a
> decision point.** A thread with no kill condition is closed by default. The cap is two, and no third
> thread opens until one closes. Thread A — the SJM reproduction (does the jump model's state carry risk
> information a volatility threshold does not). Thread B — present-state risk description (is current
> elevated risk staying or leaving).
>
> **Thread A's open list is cut from four items to one, on this repository's own §4.** D2 (`^SP500TR`),
> D7/D8 (3-sigma clipping, warm-started refits) and the HMM benchmark all exist to close *the paper's
> Sharpe margin*. That is scoring on direction, which §4 states is not this repository's object — and it
> is unbounded besides, because there is always one more fidelity deviation. The question the reproduction
> actually opened is the diagnostic one (state-vs-RV AUC 0.85–0.95), and exactly one open item can close
> it: **item 6, inference.** The three retired items are recorded in
> [[docs/REPRO-SJM2024-FINDINGS]] as *not required by the question*, unpickable if inference leaves the
> Y2 residual standing.
>
> **Thread B's redesign is corrected before it was preregistered.** Yesterday's named object — the
> unconditional local-projection decay profile — was checked and is, with a single regressor,
> `b_h = rho(h)`: the log-vol autocorrelation function, whose hyperbolic shape and `d ~ 0.4` are already
> published (Andersen, Bollerslev, Diebold & Ebens 2001). **Its informational content about markets is
> near zero.** It is demoted to a *calibration check* — does our daily-OHLC range measurement recover a
> known result — and the informative object becomes the **level-conditional** profile: decay as a
> function of the starting rank. A single slope assumes decay is the same from a high level as from a low
> one, which is the question itself, assumed away; the VIX term structure inverting at high spot is the
> options market pricing that assumption false. **Kill condition, preregisterable in one sitting: the
> profile is flat in starting level, or it adds nothing over the VIX/VIX3M slope.**
>
> **Next: Thread A's inference — preregistered, then run.** Ledoit-Wolf 2008 on the Sharpe difference,
> block machinery for the shallow half only, parametric MC under 2–3 nulls for the deep tail, Bonferroni
> over the three preregistered bands. Both outcomes close the reproduction.

## Status — 2026-08-25, sixth entry: COMMITTED CLEAN, SCREEN 1 WITHDRAWN SAME-DAY, THE TWO MAPS ARE DRAWN

> **Everything through Screen 0 is committed** (7 logical commits on `repro-sjm2024`, tree clean).
> D7 (3-sigma clip-then-scale) and D8 (warm-started refits) are declared from the authors' own
> package source — implementation choices absent from the paper's text. SJM and Lunde-Timmermann
> PDFs are local in `docs/literature/`; Xie (SSRN 2517868) is recorded unobtainable.
>
> **Screen 1 (duration/hazard) was preregistered and withdrawn the same day, before any code** — it
> hazarded a *binarized* band's exit, violating the filtration-not-states directive
> (`_daily/2026-08-24`). Kept-and-struck per [[CHARTER]] §9.3 precedent. The continuous redesign
> object is named: **the local-projection decay profile** (log range-vol at t+h on log range-vol at
> t, h = 1…120 — no model, no state; the curve's shape adjudicates model families first). Needs its
> own preregistration before any code.
>
> **Two literature surveys distilled to vault notes** ([[knowledge/backtest-inference]],
> [[knowledge/volatility-persistence-continuous]]). Load-bearing corrections caught before any run:
> block bootstrap has **no validity for deep-drawdown statistics** (never quote a bootstrap CI on
> MaxDD — the matched plan is Ledoit-Wolf for Sharpe, blocks for the shallow half only, parametric
> MC under 2–3 nulls or descriptive-only for the deep tail, Bonferroni over the 3 bands); and
> HAR-CJ jump decomposition is **ruled out on daily-only data**. Next session: learning first
> (range estimators, local projections), then the Screen 1 redesign preregistration; the SJM
> inference step follows and decides whether that thread closes.

## Status — 2026-08-24, fifth entry: SCREEN 0 RAN — THE SIX COORDINATES ARE NOT ONE AXIS

> **A new assessment exists and its first screen has run** — [[docs/ASSESSMENT-PRESENT-STATE-RISK]]
> (STATUS: PROPOSAL), grown out of the SJM reproduction's "the state is a vol threshold" ending and an
> outward literature pass (Moreira-Muir and its Cederburg refutation, the variance risk premium, the
> VIX term structure, Kritzman turbulence, and the OFR FSI as the free external incumbent).
>
> **Screen 0 (`screen0.py`, preregistered §7b) did not close the family.** On 15.7 years: the largest
> elevated-state Jaccard is RV-vs-VIX at 0.54, everything else 0.06-0.36, and the matrix is stable
> across halves. The VRP is the most independent axis (35-47 solo episodes against everything); the
> VIX/VIX3M slope is a rare subset flag, not an axis; the coordinates differ in clock as much as
> content (median spells 102/12/9/5/2 days). **The practitioner backwardation claim ("21 of 22") is
> refuted as stated on primary data**: 63 episodes, 21% hit rate against a 15.4% base; an exploratory
> >=5-day cut (42% on n=24) is recorded as post-hoc only.
>
> **Nothing is authorised beyond this.** The next question — do disagreement states carry distinct,
> well-sampled outcome base rates — needs its own preregistered screen, and F9 still forbids any
> threshold-to-action output. New data files are manifest-registered (26 files); 51 checks pass.

## Status — 2026-08-24, fourth entry: D6 CLOSED, AND THE VOL BAND MATCHES THE JUMP MODEL'S SHALLOW HALF

> Two preregistered runs, both scored — [[docs/REPRO-SJM2024-FINDINGS]].
>
> **D6 is closed as immaterial.** The CV rerun under the paper's own naming rule (`d1_cv.py --naming
> cumret`) reproduces every conclusion: Sharpe 0.50 unchanged, lambda-hat median still 150, only the
> fixed paper-70/150 rows move by hundredths — and in the direction the mechanism predicted (the paper's
> rule is slightly *hurt* by calling the melt-up state bull into the dot-com top). The CV row is now
> quotable as the paper's procedure.
>
> **The falsifier bit.** A two-parameter trailing-RV band with hysteresis — preregistered, three variants,
> none selected — **matches or beats the jump model on the shallow half of the drawdown distribution**:
> the (75,55) band's pain index is 4.2% against the JM's 4.6/4.4, same Sharpe as the JM's best fixed run
> at half the turnover. The JM's distinguishable residual is confined to the deepest 1–25% of drawdown
> days, is **under 1pp of CDaR**, and rests on two episodes — a point estimate until the block bootstrap.
> Y3 failed: the band family is parameter-fragile (exit at p85 instead of p75 doubles the pain index), so
> the JM's honest surviving claim is dial-robustness near its sweet spot, not a new observable.
>
> **The reproduction's summary line as it stands:** the paper's strategy is, to within episode-level
> noise, a persistence-regularised volatility threshold; its return claim replicates directionally under
> the CV procedure at the cost of crash depth; and its margin over a two-parameter band is unproven.
> Remaining: block bootstrap, `^SP500TR`, the HMM benchmark. No charter, no programme, no live path.

## Status — 2026-08-24, third entry: D1 RAN, THE RETURN CLAIM REPLICATES, AND IT COSTS CRASH DEPTH

> **The D1/D6 run (`d1_cv.py`) is preregistered, run, and scored — [[docs/REPRO-SJM2024-FINDINGS]].**
> X2, X3, X4 confirmed; X1 failed narrowly and informatively.
>
> **The return claim replicates directionally.** The paper's monthly CV selector, implemented exactly as
> extracted, earns CAGR 8.4% against buy-and-hold's 7.9% on the paper window — a win on price-only data
> before the ~0.45pp/yr relative dividend penalty, so roughly par on TR against the paper's +1.0pp. The
> dividend-adjusted Sharpe residual shrinks from 0.17 to ~0.07. Finding 2's return-cost half belongs to
> the fixed-lambda configuration, not the procedure; **its durable half is the trade the CV makes: it
> buys the return back by surrendering crash depth (MaxDD −34.0% against the fixed-lambda −20.3%),
> because Sharpe-selected lambda drifts to the persistent end (median lambda-hat 150 paper units, 58% of
> months at the top of the grid) where the state rides into crashes before exiting.** Sharpe cannot see
> that surrender, and the paper never runs the fixed-lambda column that would show it.
>
> **D6 is not innocent.** The two naming rules disagree on 4 of 540 fits — none at paper-lambda <= 35,
> all at 70/150, sitting at the 1987 crash and the dot-com top: at high persistence the melt-up's
> high-vol high-return days can land in the high-downside-deviation state, so "bear = high DD" and
> "bear = low cumret" diverge exactly where the money is. No quoted table is touched, but a rule-B CV
> rerun is now gating before the CV row may be called "the paper's procedure."
>
> **Also:** the full-grid sweep is not monotone in lambda (Sharpe dips at paper-70; so does the
> state-vs-RV AUC) — the earlier "monotone rise" was a truncation artifact of the half-strength grid.
> The lambda-hat series the paper never published is written to `figures/sjm2024_lambda_hat.csv`.
> Next: rule-B rerun, then the persistence-matched vol-threshold incumbent (the cheapest falsification
> left), then `^SP500TR`, block bootstrap, the HMM benchmark. Still a reproduction — no charter, no
> programme, no live path; the 0/1 rule stays F9-parked.

## Status — 2026-08-24, second entry: THE PAPER IS READ DIRECTLY, AND THE AUDIT NARROWS FINDING 2

> **No new runs.** arXiv 2402.05272v3 was read against the reproduction line by line —
> [[docs/REPRO-SJM2024-FINDINGS]] now carries a fidelity audit, a critical read of the paper's own
> weaknesses, and a fully specified open list. Three things came out of it.
>
> **Finding 2's scope is narrowed.** "It is not a return result" is a fact about *this configuration*
> (fixed half-strength lambda, price index) — the paper's own Table 4 reports JM CAGR **11.2% against
> buy-and-hold's 10.2%** on total-return data with monthly CV lambda, a return win at **44%/yr
> turnover** against our 179%. Dividends favour buy-and-hold, so D2 cannot produce their direction of
> the gap; D1 is what separates the two claims, and the turnover fingerprint (0.44 switches/yr — beyond
> our most persistent sweep point) says their CV lives at or past the top of the grid we ran. D1+D2
> decide whether their return claim replicates.
>
> **The audit confirms and declares.** Confirmed at the source: the paper's §3.4 loss is
> `0.5*||x-theta||^2`, so D5 stands on the text, not only the package; features, training window, refit
> cadence, costs and execution timing all match exactly. Newly declared: **D6** — the paper names bull
> as the higher-cumulative-return state, this repro names it by the downside-deviation centroid; almost
> surely coincident at K=2, to be verified on the fitted blocks, not assumed. The paper's grid in our
> units is {0, 10, 30, 70, 140, 300}; the HMM benchmark is now fully specified from the text.
>
> **What the paper itself gets wrong, kept as lessons rather than inherited:** no statistical inference
> anywhere (confirmed); the hyperparameter selected on the metric being reported, with the lambda-hat
> path never shown (when D1 runs here, that series is a required output); Sharpe as the headline for a
> downside claim, max drawdown as an n=1 statistic, no subperiods; no reactive incumbent in the
> comparison set; and anticipation language for what our diagnostic shows is a persistence-regularised
> trailing-volatility threshold. What it gets right is also recorded: total-return data, delay
> robustness, honest online inference.

## Status — 2026-08-24, first entry: D4 IS DISCHARGED, AND IT SURFACED THE LAMBDA CONVENTION

> **The reproduction's findings are now evidence.** Three verification legs, all passing:
> the dynamic programme against brute-force enumeration of every state path (exact); known-state
> recovery on synthetic regimes, in feature space (0.991) and end-to-end through the feature pipeline
> (0.979 away from switches); and exact equivalence with the authors' `jumpmodels` package — identical
> paths and online states at every matched penalty, free-fit label agreement 1.0000 on synthetic
> features and on a real cached `^GSPC` window. `checks.py` is now 51 checks covering the reproduction
> modules; `d4_crosscheck.py` (28 checks) holds the package leg. Details: [[docs/REPRO-SJM2024-FINDINGS]].
>
> **The correction D4 surfaced — D5, the lambda convention.** The authors' package computes the loss as
> `0.5*||x-theta||^2`; `src/jumpmodel.py` uses the unscaled square, so **a lambda here is worth half its
> face value in paper units — the headline "lambda=50" run reproduces the paper's lambda=25**, and the
> sweep's grid is really paper-lambda {0, 2.5, 7.5, 17.5, 25, 35, 75}. No outputs change, no finding
> reverses; the labels reinterpret, and D1 (the fixed penalty) sharpens as the suspect for the residual
> 0.17 Sharpe gap since performance was still rising at the top of the half-strength grid.
>
> **Also recorded from the verification work:** at lambda=30 (ours) on synthetic data with 18% true bear
> days, coordinate descent lands in a local optimum calling **73%** of days bear, 10 restarts
> notwithstanding — the penalty changes *which* fit is found, not just its persistence. And the EWM
> feature set cannot resolve regimes shorter than its own 60-day Sortino memory, a bound on the paper's
> features, not on the optimizer.
>
> **Next per the findings doc:** rerun headline and sweep at paper-unit lambdas (cheap, same code), then
> D1 (monthly CV selection), D2 removal (`^SP500TR`), block-bootstrap inference, the HMM benchmark.
> Still a reproduction under [[CLAUDE]] §1 — no charter, no programme, no live path.

## Status — 2026-08-20, second entry: A REPRODUCTION IS RUNNING, AND IT IS NOT A PROGRAMME

> **Resume here: [[docs/REPRO-SJM2024-FINDINGS]]. The first job is D4, and nothing is evidence until it
> is discharged.**
>
> **What is running.** A reproduction of Shu, Yu & Mulvey (2024), *Downside Risk Reduction Using
> Regime-Switching Signals: A Statistical Jump Model Approach*, J. Asset Management 25(5) — with the two
> reactive incumbents the paper's comparison set omits. This is a **reproduction** under [[CLAUDE]] §1
> and standing requirement 5, not a fourth programme: no charter, no queue, no new question adopted. The
> paper's 0/1 exposure rule is **F9** ([[PARKED]] §4) and is reconstructed only because reproducing the
> claim requires reproducing the rule. The output is a verification result and there is no live path.
>
> **What reproduced.** Path dominance, against benchmarks the paper never ran. Lowest CDaR at every alpha
> from the worst 1% to the pain index — 4.6% against 7.1% for a 200-day moving average, 5.8% for a capped
> volatility target and 10.8% naked. Reported as the whole curve per leak row 11, so unlike max drawdown
> the high-alpha end is not an n=1 statistic.
>
> **What did not.** The paper's margin. It is **not a return result**: CAGR 6.3% against buy-and-hold's
> 7.9%, so 1.6pp/yr is paid for the path, and Sharpe ties at 0.40 vs 0.37 because Sharpe divides by total
> volatility and cannot see path shape. **The advantage is one decade** — +8.3pp/yr in the 2000s, negative
> in every other, -9.3pp/yr in the 1990s — so effective n on what generates it is two episodes, dot-com
> and the GFC. QQQ 2011-2026 confirms it from the other side: no systemic episode, 3.5 and 8.8pp/yr given
> up, episode depth still halved.
>
> **The finding worth keeping.** Sweeping the paper's own jump-penalty grid, the AUC for separating the
> fitted state using nothing but trailing 60-day realized volatility climbs monotonically with the
> penalty: 0.762 at lambda=0 to **0.947** at lambda=150, and 0.955 on QQQ. **The better it performs, the
> more exactly the state is a slow volatility threshold.** [[docs/PROBLEM-MAP]] §0.9 firing as written:
> the jump penalty adds persistence, not information, and persistence is what makes a noisy volatility
> classifier tradeable (Sharpe 0.04 at 1503% turnover becomes 0.44 at 144%).
>
> **Also written, and also not a programme:** [[docs/ASSESSMENT-RETURN-AT-RISK]], the 10-point assessment
> for a possible fourth question. STATUS: PROPOSAL. Nothing authorised, literature field marked
> PROVISIONAL.
>
> Branch `repro-sjm2024`. Code `src/jumpmodel.py`, `src/sjm_features.py`, `repro_sjm2024.py`. 37 checks
> still pass; **the new modules have no checks yet, which is part of D4.**

## Status — 2026-08-20: THIS REPOSITORY STANDS ALONE, AND THE RECORD IS ON `main`

> **No research change.** Three closures stand, no programme reopens, no charter is drafted, no code is
> touched, 37 active checks still pass. One rule is added and two pieces of drift are fixed.
>
> **The rule — cross-repository gravity.** Relating this repository to another one is now named as the
> same defect as repository gravity, pointed sideways: [[CLAUDE]] §3 (with the four sentences that give
> it away), [[CLAUDE]] §6 requirement 16, [[CLAUDE]] §7 (**no document outside this repository has
> authority over it** — the charter in `regime-detection/governance/` governs three other repositories
> and not this one), [[README]] §3 as a fourth "what this is not", and
> [[docs/RESEARCH-PROTOCOL]] P12. This repository has no upstream, no downstream, no sibling to
> reconcile with and no governing document outside its own tree; it shares a directory with three
> governed repositories and is not one of them; it is **neither an extension nor a successor** of
> `regime-detection`.
>
> **The corollary that matters in practice.** A dataset held in another repository is a fact about the
> world, not a research question — an acquisition option for a question already argued on its own terms.
> [[docs/PROBLEM-MAP]] §4's U1 remedy column had drifted into reading as an action item pointing at
> another repository's option archive; its header now says explicitly that the row is historical, and the
> evidence itself is untouched.
>
> **Drift 1 — the record was not on the default branch.** `origin/main` pointed at a merge of an *early*
> state of `cleanup-and-retarget`, and 58 commits — every run, every closure, the governance reset —
> existed only on the feature branch. The branch is merged and `main` now carries the record.
>
> **Drift 2 — the repository was registered nowhere.** It appeared in neither `C:\dev\INDEX.md` nor the
> repo table in `C:\dev\CLAUDE.md`. Both now list it, in both cases marked **standalone and outside the
> governed stack**. The vault manual also claims a `systematic-investing-research/README.md` that does
> not exist; that is the vault's drift, not this repository's, and it is left alone.

## Status — 2026-08-19, second entry: PHILOSOPHY ALIGNMENT, NO RESEARCH CHANGE

> **The repository's declared identity changes from "a record" to "a research laboratory that currently
> has no active programme."** Nothing about the three closures changes, no programme reopens, no model
> is built, and no charter is drafted. This is a documentation correction.
>
> **What it corrects.** The repository had accumulated working machinery and three closed programmes,
> and nothing in the documentation stopped a reader from inferring that the machinery defined the
> agenda. That inference now has a name — **repository gravity** — and a rule against it
> ([[docs/RESEARCH-PROTOCOL]] P12, [[CLAUDE]] §3). The containment runs one way: the research universe
> contains the literature, which contains candidate mechanisms, which contain publicly measurable
> phenomena, which contain the experiments in this repository. **Existing code is evidence of what has
> been attempted, never evidence of what to attempt.**
>
> **What was added.** [[CLAUDE]], which did not exist — repository purpose, the order of work
> (question → literature → mechanism → data → formulation → test → falsification → extension →
> implementation), the risk-intelligence-is-not-alpha split, the public-data constraint stated as a
> research frame rather than an apology, and fifteen standing requirements. [[README]] §6 now states
> what counts as a result, with profitability absent from the list. Protocol gains **P11** (outward
> before inward), **P12** (repository gravity) and **P13** (cheapest falsification first), and its
> header is rescoped from "the active program" to every programme including future ones.
>
> **The one substantive intellectual addition** is [[docs/PROBLEM-MAP]] §0.9, and it is labelled
> interpretation rather than measurement: the closed prediction programme's containment result is what
> unsupervised compression of volatility-dominated return features *predicts*, not a surprise. Its
> reusable form is that the response to a negative result is to question the object and the
> representation, not to substitute another model. It carries a free check for anyone who recovers that
> machinery — the fitted labels should be nearly monotone in trailing realized volatility.
>
> **Not changed, deliberately:** [[CHARTER]] and `closed-research/` are historical and stay as written.
> History is not tidied to make the past look like the present.



## Status — 2026-08-19: THE RETURN-STATE PROGRAMME IS TERMINATED

> **S0b returned VOID and the programme terminates as INDETERMINATE.** Two synthetic identification
> gates ran. **No market data was ever touched.** No S0c is authorised and no Q1 was ever licensed.
>
> **The sequence.** S0 found one surviving functional and [[docs/DECISION-Q1-CLAIM]] then showed by
> exact algebra that its separation was reducible to variance-process dispersion, which S0's matching
> left free (**R1**). S0b closed that degree of freedom with a GARCH-t null matching unconditional
> variance, the squared-return ACF at every lag, and `Var(sigma^2)` — all exact to 3.4e-14. **Its
> control failed anyway**, `d' = 7.42` against a threshold of 2.
>
> **And (M3) was holding.** The observable is the problem, not the matching:
>
> ```
>     RV_B = SUM sigma2_t z2_t
> ```
>
> The observed block-variance distribution depends on both the latent variance distribution and the
> innovation distribution, and `E[z^4]` was the instrument used to match the former. **The mechanism
> that removed the difference under test also contaminated the measurement of it** (**R2**). The
> control fails hardest exactly where the instrument bites hardest — `d' = 7.42` at `kappa = 2.0`
> where `Var(sigma^2) = 0.096`, and `d' = 0.02` at `kappa = 6.5` where it is 1.158.
>
> **What survives:** R1 and R2; the elimination of aggregate kurtosis; and the elimination of path
> geometry as a state-existence coordinate, measured where the states exist by construction. **The
> `T7` pattern does not survive as evidence** and is preserved as observed-and-uninterpretable.
>
> **Why it was not repaired.** A stochastic-volatility null would leave the RV noise matched — and
> introducing it after seeing the obstruction is a new identification programme, not a repair. The
> final-gate scope condition was committed before S0b ran and is honoured. [[PARKED]] §3b.

## Status — 2026-08-18, second entry: THE RETURN-STATE TRANSITION

> **The rolled-put / tenor intervention program is CLOSED**, preserved and reproducible at
> [[closed-research/intervention/README]] with its own charter, its four preregistrations, its code
> and its 17 checks. **The active program is [[CHARTER]] — return states.**
>
> **Why it closed, and it is not fatigue.** E0 removed 82–85% of the measured drawdown reduction as
> unrealised mark. E1 showed the remainder is smaller than the spread an arbitrary roll-calendar
> offset produces, and that in cash the *sign* flips with the calendar. E2 repaired the estimand and
> no tenor ordering survived anywhere on the drawdown path in cash. E4 took the last surviving
> structural claim from unconditional to conditional — M1 is a deductible-count effect that wins
> grinds and loses V-shapes — **and the condition is a forecast the prediction program had already
> closed.** The two programs closed each other.
>
> **What the new program studies.** The conditional law of the forward return path,
> `F_{s,h} = law of R_{t:t+h} given S_t = s`. Four questions in order: existence, characterisation,
> transition, identification. **It terminates at identification.** No allocation, no instrument, no
> trigger, no exposure — those need a new charter, not an amendment ([[CHARTER]] §3, §7).
>
> **Two decisions were fixed before the first experiment so neither can be selected on a result
> later.** The null is **N1**, a smoothly-reverting continuous-scale process — the honest opponent,
> and never built in this repository. The frequency is **daily** — E8 established weekly cannot
> resolve the memory any persistence claim depends on.
>
> **S0 RAN THE SAME DAY, and Q1 now exists.** Of four candidate functionals, one discriminates the
> classes after matching that is exact on the unconditional variance and on the squared-return ACF at
> every lag: **the dispersion of log realized variance over 21-day blocks**, `d'` up to 10.2. Two are
> eliminated — aggregate kurtosis sits below its own mismatch floor everywhere, and **path geometry
> reaches `d' = 0.15` on synthetic data where the states exist by construction**, which forecloses
> drawdown geometry as a state-existence coordinate. **One preregistered deduction was wrong**, and
> the correction constrains every future matching argument here: matching the autocovariance function
> of squared returns is not matching the distribution of the latent variance process. Section below;
> full result in [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]].

## Status - 2026-08-18 — first entry, E0


> **E0 RAN 2026-08-18 AND IT IS THE LARGEST CORRECTION IN THE REPO.** The measured drawdown
> reduction is **mostly an unrealised mark**: 82% of the 52-week figure on the full sample, 85% on
> 2003-. **+16.8pp and +19.9pp both become +3.0pp in cash**, the cash reduction is flat from 26w to
> 52w, and at 4w/13w it is *negative* -- the program deepens the worst drawdown. In the well-sampled
> `CDaR_alpha` coordinate the full-sample cash reduction at 52w is zero to slightly negative at every
> alpha. E10's tenor ordering survives in **sign** and not in **magnitude**. Section below;
> preregistration and full result in [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]].
> **PROGRAM TRANSITION 2026-08-17. The prediction/regime program is CLOSED.** It is preserved,
> self-contained and reproducible, at [[closed-research/README]] -- completed research, not obsolete
> code, and not an active branch. The active program is **drawdown intervention design**: [[CHARTER]],
> which is the only research question and the only experiment queue in this repository.
>
> **Why.** The model's forward-downside information is nested inside VIX on levels (D3) and dynamics
> (F2); the clairvoyant ceiling bounds any timing rule near +3pp/yr where it has been measured; and
> the variable that dominated outcomes -- option tenor -- had been fixed by assumption while the
> variable that did not got the research. *The old program's failure was in what it held constant,
> never in how carefully it measured.* Full amendment, including the precise scope of the closure and
> what is prohibited from reopening: [[docs/PROBLEM-MAP]] Part I.
>
> **The closure is scoped, not universal.** It covers public return-volatility estimators, for
> decision purposes, on SPY, against VIX, at h=4 and h=13. Credit, funding, breadth and positioning
> were never tested -- out of scope, not refuted. And the EVPI ceiling exists only at 4w/13w, the
> tenors the structure map says are dominated; [[CHARTER]] E3 closes that corner or shows it
> undecidable.
>
> **The founding arithmetic is withdrawn.** [[README]] §2 held that premium drag would be smaller than
> the drawdown avoided. E9 measured it: 0 of 40 structures beat the naked book on CAGR, both samples.
> The overlay is a **purchase** of a different outcome path at a cost in compound return. That is
> price discovery, and it moves preference explicitly downstream of research.

## Governing frame — HISTORICAL, superseded by [[CHARTER]]

> **Everything from here to the "Next" section is the chronological record of two closed programs and
> stands as written.** It is not the active frame and does not govern anything. Rules 1-4 below were
> the prediction program's; rule 4 (width is not direction) survives verbatim into [[CHARTER]] §4,
> and rule 3 (check the data and the frequency first) is why the active program is daily. The rest is
> history.

Rules 1-3 have each been broken by this repo at least once. They exist because the documents kept
asserting the right principle while the practice reverted. Rule 4 is the one rule added *before* it
was broken, and it is now binding architecture rather than a preference.

**1. The model's content is `P`, not a level.** A Markov-switching model's claim is about
*persistence* — how long a state lasts, how belief decays, how the forecast reverts. Every test
run through 2026-08-13, including D3, collapsed it to a **scalar** (a VaR or ES number) and raced
that against VIX's scalar. VIX is a spot price with no memory structure, so a level-vs-level test
**structurally cannot see** what this model knows. Protocol §1.2 already said this and every
subsequent experiment scored levels anyway. Before proposing a test: *what does the model claim to
know that the comparison object does not?* If a test could be passed by a constant rescaling of
VIX, it is not testing this model.

**2. The model never decides what, where or how to trade.** It reports risk. Strikes, tenors, roll
schedules, hedge ratios, premium and P&L are not the working surface — [[README]] §5 has said so
from the start, and on 2026-08-13 three consecutive runs drifted into option mechanics anyway
before being stopped. Economic viability is the long-run goal, not the near-term reasoning surface.

**3. Check the data and the frequency before reasoning about model shape.** The weekly series
cannot resolve volatility memory at all — at n=1750 the ACF band is ±0.0469 and the empirical
squared-return ACF is inside it by lag 8. A year of argument about regime counts and tail shapes
happened on a series that could not have settled any of it.

**4. The model measures WIDTH. Direction is a separate layer that does not exist.** Established
empirically, not assumed: volatility separates 2.4x (SPY) / 1.8x (QQQ) across probability bins and
replicates, while the drift difference **reverses sign between the two assets** and the down/up
tail ratio straddles 1.0. So `wide` never licenses `bearish`, `short`, or `to cash`. Sizing on
width is legitimate **only** as variance targeting, and the reason must be written next to the
line — identical code, different research obligation. Full contract, forbidden patterns, and the
status of every "beyond simpler measures" comparison: [[closed-research/docs/TRANSLATION-LAYER]].

The question is unchanged ([[README]] §3): *how well does a Markov-switching model provide
real-time information about Value at Risk and the tail risk of equity assets?* **Real-time**
excludes smoothed probabilities by definition.

[[docs/RESEARCH-PROTOCOL]] is preregistered. `src/evaluation.py` scores whatever it is handed and
knows nothing about which model produced it, which is what turns the specification argument into
an experiment.

## Target

> Each week: is there a real, **systemic** threat to a long global equity book, large enough that
> paying for a hedge is worth it?

The book is permanently long SPY / QQQ / international and is never sold. The hedge is a small USD
sleeve buying SPY puts, monetized in a crash and recycled into the core at lower prices. Goals:
smooth the ride, cut drawdown depth, stay invested.

Two properties this implies that the current model lacks:

- **Systemic, not single-asset.** SPY alone wobbling is noise; SPY + QQQ + international falling
  together is the event. Those correlate 0.77-0.87 weekly.
- **Continuous in principle, saturated in practice.** *Not* near-binary by construction — the
  conditional variance is continuous in the mixture weight and sweeps the whole range between the two
  regime variances. It saturates because the fitted components are far apart ($\sigma$ 1.50% vs
  3.84%, a 2.6x ratio), so one bad week moves the likelihood ratio almost all the way: the top-20
  probability weeks all sit at P ≥ 0.99999. A property of the fit, not of the model class.

## Open questions

Positions stated, not hedged. None is a tuning question.

1. **Is the target variable right?** *Probably not.* The model estimates the latent state of return
   *variance*; the mandate is about forward *drawdown* over weeks to months. These diverge badly —
   2022 was -24% over 39 weeks at unremarkable weekly volatility, while a single -8% week that
   recovers is high-variance and harmless. Subsumes most of the others. The protocol's answer is to
   score the predictive density directly rather than argue about the target.
2. **Is a discrete-regime model the right class?** *Not alone.* ARCH-LM on standardized residuals
   rejects at 55.6 (p = 2.4e-11) *after* regime-switching — volatility keeps moving within regimes.
   Not because MS(2) has "only two conditional variances" — it has a continuum, via the mixture
   weight. The binding limits are that the weight is driven only by returns through a saturating
   likelihood ratio, and that **the tail decay rate is fixed by the largest regime $\sigma$ alone**:
   a finite Gaussian mixture is Gaussian in the far tail for any $k$ and any weight. That is algebra,
   and it means **more regimes cannot fix a tail.** Within-regime ARCH and Student-$t$ regime
   densities are S3/S4 in the protocol; S4 is the one aimed at the measured defect. Known in the
   literature since Rydén, Teräsvirta & Åsbrink (1998) — see protocol §11.
3. **How many regimes?** Corrected AIC *and* BIC both prefer **k=3** decisively (ΔAIC 66, ΔBIC 44) on
   real data. k=2 persisted only because [[README]] said so. But k=3 does not fix question 2.
4. **Returns only?** *No.* VIX is free, forward-looking, aligns 1750/1750 weeks. It is the **price**
   side — what acting costs — not a benchmark to beat. Loaded in `data_loader.py`, used by nothing.
5. **Sign-blindness.** Not a bug to patch — it is what modelling variance *means*. Up/down probability
   ratio **1.0000** at |return| ≥ 7% with a common mean; **0.9279** with a switching mean. Follows
   from question 1, and it is why the regime is named `high_variance` rather than anything
   directional.

## Settled by evidence

- **Filtered, never smoothed.** Kim-smoothed probabilities condition on the entire sample including
  the future. Filtered and smoothed disagree at the 0.5 threshold in **9.7%** of real weeks. Guarded
  by two checks.
- **520-week (10-year) minimum history, weekly.** At 260 weeks, walk-forward fits produced degenerate
  parameters (`p[0->0]` to 0.163, `p[1->0]` pinned at 0.999999, a variance collapsing to zero), 6
  label flips across SPY and QQQ, 2-3% convergence failures. At 520: 1 flip, 0-1 failures, 7.3-7.8%
  revision, no degenerate values. **Does not transfer to daily by multiplying by 5** — must be
  re-measured.
- **Post-hoc relabelling is load-bearing.** The high-variance index flips across refits on real data —
  SPY at 2009-01-09, a genuine GFC transition. Any hardcoded index inverts the signal.
- **The data loader must resample daily onto a fixed weekly grid.** `yfinance`'s `interval="1wk"`
  anchors on each series' first observation: SPY from 1993 came back Monday-anchored, from 2010
  Friday-anchored, sharing zero bars. `start=None` silently returned a short window. Both fixed.
- **The 2006-2011 "persistence pathology"** the original constraints existed to prevent **does not
  occur.** The unconstrained high-variance regime is *less* persistent (17.2 vs 44.7 weeks). Those
  constraints were removed.
- **Mixture VaR and ES closed forms verified** against a 40M-draw Monte Carlo to ~1e-5. The
  moment-matched normal approximation errs by 11% of the VaR level at $w=[0.85,0.15]$ — it is wrong,
  not merely imprecise.
- **The primary test has a blind spot, and it is the one this project cares about.** Berkowitz's
  $\rho$ tests autocorrelation in the *level* of $z$. A stochastic-volatility series scored at
  constant volatility passes the full LR at $p=0.07$ while the Ljung-Box on $(u_t-0.5)^2$ rejects at
  $p<10^{-16}$. Unabsorbed volatility dynamics are a $z^2$ phenomenon. A passing Berkowitz is
  meaningless without the companion statistic — enforced by a check, documented in both the
  docstring and protocol §5.1.
- **The censored Berkowitz separates from the full one on exactly the case it is for.** Standardized
  $t(4)$ scored as $N(0,1)$ — zero mean, unit variance, no dependence, wrong only in the tail — gives
  full $p=0.89$, censored $p=4\times10^{-37}$. Measured, not asserted.

## Known defects

| what | where | severity |
|---|---|---|
| **No dynamics test exists** — every experiment scores levels | whole repo | **the live gap** |
| Daily minimum history still unmeasured; 520 is a weekly figure | `RELIABLE_MIN_OBSERVATIONS` | blocks any daily model fit |
| Squared daily returns are a noisy variance proxy; attenuates long-lag ACF | `memory_diagnostic.py` | blocks the shape question |
| DQ, tick loss, ES bootstrap unbuilt | `src/evaluation.py` | deprioritized — level-based (D3) |
| ~~No vintage-parameter VaR path~~ | ~~`walkforward.py`~~ | **fixed 2026-08-13**, `walkforward.py density` |
| Base specification's tail is ~2.8x too narrow at $\alpha$=0.05 | model class | the finding, not a bug — S3/S4 exist for it |
| Parameter look-ahead in the convenience path | `markov_switching.estimate_high_variance_probability` | documented in the docstring; walk-forward path is the honest one |
| ~7.5% of weeks have their state revised by later refits | model class | reliability number, protocol R4 |
| ~1-2% of refits fail to converge | `markov_switching.py` | policy fixed in protocol §4.5, not yet coded |
| Signal timing unresolved — no weekly close exists at Friday 3:30pm | operational | leak register #3 |
| Daily minimum history unmeasured | `RELIABLE_MIN_OBSERVATIONS` | blocks quoting any daily result |

## Working lesson from 2026-08-12

**Most of this repo was analysis apparatus built while the base was unsettled, and it did active harm
rather than merely wasting effort.** 2065 lines documenting a 2-regime model made k=2 feel decided
when the repo's own diagnostics said k=3. A 764-line diagnostics suite nobody had read produced
numbers that entered permanent documents as fact — including a QQ standardization bug found the first
time it was actually reviewed. That suite is deleted; the documents that cited its line numbers had to
be rewritten.

Two rules that came out of it:

- Sort findings into **deductive** (code does X, math implies Y — solid as stated) and **inductive**
  (this beat that on these episodes — needs a rule-based test bed and honest effective-n, which is
  episodes, not configuration rows). They were being quoted with equal confidence.
- **Fix the design and the kill thresholds before running.** That is now
  [[docs/RESEARCH-PROTOCOL]] §7.

A third, from the naming sweep: **a wrong name is a load-bearing defect.** `jump_model.py` implemented
a Markov-switching model while "statistical jump model" is an established name for a different method.
Every document inherited the confusion.

## Possible output: a paper

A **long-run** goal, not a near-term deliverable — but recording it disciplines the work rather than
adding to it. A paper audience will not accept metrics invented after seeing the data, hand-picked
crisis windows, or economic results without a calibration test. That is exactly the standard
[[docs/RESEARCH-PROTOCOL]] sets, and it is stricter than what this project was applying to itself.

The natural shape, if results support one: *does a conditional regime model carry information about
downside risk that is incremental to implied volatility?* Open in the literature, genuinely uncertain,
and a well-executed negative result is publishable and useful. It is also exactly the question that
decides whether this system should exist.

## First honest result — 2026-08-13

**Walk-forward, no look-ahead.** 1,230 out-of-sample weekly SPY forecasts, 2003-01-24 to 2026-08-14.
Parameters refit every 13 weeks on data through the refit point only; state from `filtered[t-1]`;
density formed before $r_t$ exists. Run: `.venv\Scripts\python.exe walkforward.py density SPY`.

**Alignment verified adversarially**, because an off-by-one would invalidate everything: shifting the
realized series so a forecast is scored against a return its own filter already absorbed collapses
coverage to $p=0.0000$. Only the true alignment and the harmless staler direction are sane.

**The body is calibrated. The tail is not, and it degrades monotonically with depth.**

| $\alpha$ | breach rate | Kupiec $p$ | independence $p$ | CC $p$ |
|---|---|---|---|---|
| 0.10 | 0.1049 | 0.571 | 0.657 | 0.772 |
| 0.05 | 0.0528 | 0.650 | 0.384 | 0.617 |
| 0.01 | **0.0179** | **0.012** | **0.006** | **0.001** |

| measure | $\alpha$=0.10 | $\alpha$=0.05 | $\alpha$=0.01 |
|---|---|---|---|
| censored Berkowitz $\sigma^2$ | 1.89 ($p<10^{-4}$) | 2.80 ($p<10^{-4}$) | — |
| ES ratio realized ÷ predicted | 1.108 | 1.171 | 1.216 |

Full Berkowitz LR 8.66, $p=0.034$ — $\mu=-0.008$, $\rho=-0.076$, $\sigma^2=1.044$. PIT uniformity
$p=0.033$. Ljung-Box on $u$ quiet at every lag count (0.06-0.42).

**Ljung-Box on $(u-0.5)^2$ is lag-dependent and must be quoted as a sweep, not a number:**

| lags | 5 | 10 | 15 | 20 | 26 | 52 |
|---|---|---|---|---|---|---|
| $p$ | 0.0004 | 0.0075 | 0.045 | 0.062 | 0.099 | 0.108 |

The dependence is concentrated at lags 1-4 and dilutes as uninformative lags are added. Unabsorbed
volatility dynamics are therefore a **short-horizon** finding, not a general one. **The protocol never
preregistered a lag count** — a real gap, recorded rather than closed by picking one after seeing the
sweep.

**Worst week, and the whole story in one line:** 2008-10-10, SPY $-22.1\%$ against a 1% VaR of
$-6.4\%$. PIT $= 6\times10^{-16}$: the density called it impossible. That is the sample's one clipped
observation, surfaced by the clip counter rather than swallowed.

### The diagnosis: thin tails INSIDE each regime, not bad regime detection

Found 2026-08-13 by looking at Figure 2 and asking why ordinary weeks were breaching.
**16 of the 22 breaches happen while the model believes it is calm**, most at $P(\text{wide}) < 0.10$:

| date | realized | its 1% VaR | $P$(wide) |
|---|---|---|---|
| 2007-03-02 | −4.67% | −3.00% | 0.005 |
| 2005-04-15 | −3.32% | −3.03% | 0.008 |
| 2004-03-12 | −3.32% | −2.93% | 0.008 |
| 2007-07-27 | −5.62% | −3.04% | 0.007 |

2004 and 2005 are not crises. The calm regime has $\sigma \approx 1.5\%$/week, so a Gaussian puts the
1% worst week at $-3.5\%$; real quiet markets deliver $-4\%$ and $-5\%$ weeks far more often.

| model state | weeks | breaches | rate | vs promised |
|---|---|---|---|---|
| believes calm | 929 | 16 | 1.72% | 1.7x |
| believes wide | 301 | 6 | 1.99% | 2.0x |

**Both states are broken by roughly the same factor** — the tell that this is the conditional
*density*, not the regime *classifier*. Three separable failures:

1. **Thin tails** — small breaches ($-3\%$ to $-5.7\%$) in genuinely quiet markets. Majority of cases.
   Also explains 2008-10-10: $P(\text{wide})=0.995$, VaR $-6.4\%$, realized $-22.1\%$. Fix: fat-tailed
   regime densities (S4).
2. **Lateness** — *large* breaches at low $P$(wide) at crisis onset, before the filter switches:
   2020-02-28 ($-11.8\%$ vs $-4.8\%$, $P=0.10$), 2025-04-04 ($-9.5\%$ vs $-6.1\%$, $P=0.16$).
   Fix: daily cadence, or a leading input (VIX).
3. **Neither is fixed by more regimes.** k=3 walk-forward threw `Invalid regime transition
   probabilities` across the run — numerically fragile, and aimed at the wrong defect anyway.

**Read.** The failure is exactly the one open question 2 predicts — ARCH-LM rejects *after*
regime-switching, and two conditional variances cannot track scale in the far tail. Three independent
measures (breach rate, censored $\sigma^2$, ES ratio) agree and all worsen with depth, which is the
signature of a tail that is too thin rather than a level that is mis-set.

**The censored test earned itself immediately.** The full Berkowitz alone reads as borderline
($p=0.034$); the censored version is $p<10^{-4}$ — body-correct, tail-wrong, on real data the same day
the discriminating case was demonstrated on simulated $t(4)$.

**The figures say two things the tables do not.**

- **The QQ panel of the PIT is asymmetric.** The *left* tail falls off the 45-degree line; the right
  tail sits on it. The density is too thin on the downside specifically, not symmetrically fat-tailed.
  That argues for a **skewed** heavy-tailed regime density, not just Student-$t$ — and it is a
  distributional-width finding, not a directional one, so it stays inside the mandate.
- **A 20-bin PIT histogram cannot resolve the failure.** The whole $\alpha=0.01$ story lives inside
  the leftmost bin. Figure 1's histogram looks unremarkable ($\chi^2 p = 0.033$) while the QQ panel
  and the censored LR show the defect plainly. Do not read the histogram as the tail check.

**Figure 2 makes the causal-filter lag concrete.** Through Feb 2020 the 1% VaR sits flat near $-5\%$;
the $-11.8\%$, $-10.0\%$ and $-15.7\%$ weeks all arrive *before* it widens to $-9\%$. Same shape in
2008. This is protocol §7's recorded threat to D5, now visible rather than argued.

**Not a verdict.** D1 requires Berkowitz *and* DQ rejecting across R8 subsamples for *every* §3
specification. DQ is unbuilt, subsamples unrun, and S3 (within-regime ARCH) and S4 (Student-$t$
regime densities) — preregistered precisely for this failure — do not exist yet. **This is the base
specification only**, and it fails where the protocol said to look.

## Context rungs — one-step coverage, harness shakeout (2026-08-13)

**Claim tuple: weekly · $h=1$ · marginal quantile and density · SPY, 1,230 OOS weeks 2003-2026.**
Nothing in this section supports any claim outside that tuple (protocol §0.1).

Protocol step 3, `baselines.py`. Constant (expanding mean/sd) and EWMA
($\sigma^2_t = \lambda\sigma^2_{t-1} + (1-\lambda)r^2_{t-1}$, $\lambda$ reported as a sweep, never
tuned) scored by the identical battery on the identical 1,230-week sample.

**Ranking, mean tick loss $\times 10^4$ — lower better:**

| | 10% | 5% | 1% |
|---|---|---|---|
| MS model | **42.71** | **27.73** | **9.92** |
| EWMA 0.94 | 43.77 | 28.54 | 10.77 |
| constant | 46.38 | 30.20 | 11.10 |

The model wins at every level and **Diebold-Mariano finds none of it significant** (vs EWMA 0.94:
$p$ = 0.24, 0.30, 0.077). It beats the *constant* significantly at 10% ($p<0.001$) and 5%
($p=0.011$) — so conditioning on something helps; conditioning on *regimes* specifically is not
demonstrated.

**Density calibration — EWMA 0.97 beats the model:**

| | Berkowitz $p$ |
|---|---|
| EWMA 0.97 | **0.237** passes |
| EWMA 0.94 | 0.070 |
| MS model | 0.034 fails |
| constant | 0.027 fails |

**No verdict is available here, and none ever was.** At $h=1$ the MS model and a tuned EWMA have
near-identical conditional variances by construction, so a DM null is what theory *predicts* rather
than information about the model. RiskMetrics EWMA is IGARCH — its multi-step variance forecast is a
martingale and never reverts; MS(2) reverts toward the stationary regime mix at a rate set by the
second eigenvalue of $P$. That is the entire structural difference between the two, and it is exactly
zero one step ahead. **D2 may not be evaluated against this comparison** (protocol §0, standing
consequence).

**Recorded because the rule came from it.** This section was previously headed *"the model does not
beat a moving average"* and called the outcome *"a thin return on a Hamilton filter."* The first
exceeded the claim tuple; the second inferred an economic judgement from a loss function, when
economic value is gated on D5 and has never been measured here. The protocol already forbade all of
it — the header says "Not a horse race," §3 requires a preregistered expectation, and §11 cited the
paper that answers the specification question. Protocol §0 is the gate that now runs before code.

### The most important number on this page

**Every method breaches ~2x at $\alpha=0.01$:** MS 1.79%, constant 1.87%, EWMA 0.97 2.03%,
EWMA 0.94 2.36%. What they share is the **Gaussian assumption**. The 1% failure is therefore a
property of the *data*, not a defect of the regime model, and **no Gaussian-based estimator of any
complexity can fix it**. This is the strongest evidence yet for fat-tailed conditional densities —
and it means the fix applies to EWMA too, without a custom Hamilton filter.

### From `figures/rungs_paths_spy.png`

- The model's VaR path is **blocky** — snaps between levels and sits flat, while EWMA glides.
  Saturation of the mixture weight, visible; not a structural binary (see open question 2). This is
  also the whipsaw source: 10 of 36 elevated-risk episodes are single-week blips. Whether blocky is a
  *defect* is undetermined at $h=1$ — a model that holds a level because it believes the state
  persists is doing what a regime model is for. That question lives at horizon.
- **In 2008 and 2020 EWMA went deeper and faster** — reaching $-16\%$ at the 2008 trough against the
  model's $-10\%$.

## Earlier smoke reading — NOT a result

`src/predictive.py` landed 2026-08-12 and the full path runs. On weekly SPY (1,749 forecasts), fitted
**once on the whole sample**, so this carries parameter look-ahead and is not reportable — it is a
smoke test that the plumbing produces sane numbers:

| $\alpha$ | breach rate | Kupiec $p$ | independence $p$ |
|---|---|---|---|
| 0.10 | 0.1109 | 0.134 | 0.724 |
| 0.05 | 0.0555 | 0.303 | 0.782 |
| 0.01 | 0.0114 | 0.555 | **0.020** |

Regimes: high-variance $\sigma$ 3.84%/week, mean -0.26%, expected duration 12.9 weeks; calm $\sigma$
1.50%, mean +0.36%, 36.1 weeks.

**The pattern worth noting:** rates are right at every level, but at $\alpha=0.01$ the breaches
*cluster* — the independence test rejects while Kupiec passes comfortably. That is precisely the
failure Kupiec cannot see and the reason [[README]] §3 calls independence the discriminating test. It
is also what the ARCH-LM rejection predicts: two conditional variance values cannot track scale in
the far tail. Expect the honest walk-forward version to be worse, not better, since look-ahead
flatters.

## D3 FIRED — the model is nested inside VIX on levels (2026-08-13)

**Claim tuple: weekly · h=4 and h=13 · forward downside semivolatility · SPY 2003-2026, 1,230
walk-forward OOS forecasts.** Run: `.venv\Scripts\python.exe encompassing.py SPY`.

`RV[t,t+h] = a + b·IV[t] + c·X[t]`, with RV the forward downside semi-volatility
`sqrt(SUM min(r,0)^2)`, IV log VIX at the same information time, and X the model's own
`-ES(0.05)` from the walk-forward vintage path.

| h=4, non-overlapping n=307 | coefficient | p |
|---|---|---|
| VIX | +0.3616 | 0.0026 |
| model (−ES 0.05) | **+0.0009** | **0.9935** |

| R² | value |
|---|---|
| both together | **0.1015** |
| VIX alone | **0.1015** |
| model alone | 0.0471 |

Joint and VIX-alone are **identical to four decimal places**. h=13 agrees: c = −0.0232 (p=0.9277),
joint 0.1173 against VIX-alone 0.1172.

**Alignment verified adversarially**, because an off-by-one would invalidate it: leaky (window
starts d−1) R²=0.2488 > true (starts d) 0.1015 > stale (starts d+1) 0.0769. Monotone in the right
direction; the leak more than doubles R².

**The null arrives in its strong form.** Low power shows up as a large-but-insignificant
coefficient. c = +0.0009 with p = 0.99 is a coefficient that is actually zero. The model carries
real downside information (R²=0.047 alone) and it is **strictly nested** inside VIX's.

**Preregistered consequence (§7 D3): no capital is committed.** The result is reported.

**The load-bearing caveat.** X was a *level*. This is a level-vs-level test and it is exactly what
governing-frame rule 1 warns about. D3 closes the level-based case; it says nothing about
persistence, which remains untested.

## Memory diagnostic — and a claim of mine that it refuted (2026-08-13)

Run: `.venv\Scripts\python.exe memory_diagnostic.py SPY [--daily]`.

**Deductive result first.** For a two-state switching-variance model with regime variances `v[j]`,
stationary weights `pi`, and `lam = p00 + p11 − 1`:

```
Cov(r[t]^2, r[t+k]^2) = pi_0 * pi_1 * (v_0 - v_1)^2 * lam^k
```

The squared-return ACF decays **geometrically — for any k, any number of regimes, any parameters**.
That is algebra, not a fitted claim, and it holds at all 95 vintages (λ₂ ∈ [0.8921, 0.9929]).

**Weekly (n=1750, band ±0.0469):** median λ₂ = 0.9126, half-life 7.6 weeks. Model lag-1 ACF 0.1754
against empirical 0.2776 — the model captures **63% of the one autocorrelation weekly data can
measure reliably**. Shape test inconclusive: exponential R² 0.4094 against power-law 0.4283, both
poor, H = 0.524. Empirical ACF falls inside the noise band by lag 8, so **decay shape is not
identifiable at weekly frequency at all.**

**Daily built and cached** (`data_loader.download_daily_prices` / `load_daily_log_returns`;
`data/spy_daily.csv`). All 64 checks still pass. n = 8,441, band ±0.0213.

| | weekly | daily |
|---|---|---|
| ACF significant to | ~4-7 weeks (20-35 days) | **lag 212 (~10 months)** |
| fraction of lags significant | — | 54% of lags 1-250 |

Weekly hid ten months of memory behind its noise band. That gain alone justified the frequency
change.

**But the shape claim was refuted.** I asserted confidently that volatility has power-law memory a
Markov chain structurally cannot match, and that MSM or HAR was therefore required. At daily
frequency:

```
lags 1-250   exponential R2 = 0.7192   power law R2 = 0.6219   H = 0.423
lags 1- 63   exponential R2 = 0.8644   power law R2 = 0.7719
lags 1-126   exponential R2 = 0.8094   power law R2 = 0.8264
```

**Exponential wins**, and H = 0.423 is *below* 0.5 — anti-persistent, the opposite of long memory.
The gap is one of **duration, not shape**: the model's implied memory reaches ~138 trading days
against the data's 212, roughly 35% short.

**Three reasons the refutation is itself weak, recorded so neither claim is over-read:**

1. **It flips with the window** — exp / power / exp across 1-63, 1-126, 1-250. Under D4 a verdict
   that flips on window choice is not reportable as stated. This one flips.
2. **The ACF is non-monotone at short lags** — 0.2638 at lag 1 *rising* to 0.2858 at lag 5. Neither
   functional form fits a hump, at exactly the lags carrying the most signal.
3. **An R² race on log-ACF is not a long-memory test.** GPH log-periodogram regression or local
   Whittle estimate the fractional integration order `d` *with a standard error*. A proxy was used
   in place of the test.

**Most likely cause, and it is fixable in scope.** Squared daily returns are a single-draw estimate
of that day's variance — unbiased but very noisy — and measurement error **attenuates the ACF
toward zero at exactly the long lags where long memory would appear**. Andersen & Bollerslev (1998),
already `[skim]` in the reading list. The literature's long-memory results are mostly on realized
volatility from intraday data, which protocol §9 excludes.

## THE DYNAMICS TEST — the model class is closed on both axes (2026-08-14)

**Claim tuple: weekly · h=4 · forward downside semivolatility · SPY 2003-2026, n=307
non-overlapping. One preregistered input, no sweep.** Run:
`.venv\Scripts\python.exe dynamics_test.py SPY`.

The first experiment whose **input matches what the model claims to know**. Scale-free by
construction, so it cannot be passed by a rescaling of VIX:

```
X[t] = Var_4(t) / Var_1(t)        w_1 = xi[t]' P ,  w_h = w_1 P^(h-1)
```

X > 1 means the model expects risk to rise; X < 1 means it expects reversion. Pure `P`.

| | coefficient | p |
|---|---|---|
| VIX | +0.3473 | 0.0003 |
| model (Var₄/Var₁) | **−0.0047** | **0.6255** |

R² both 0.1019 · VIX alone 0.1015 · **X alone 0.0339**. Alignment verified adversarially
(leaky 0.2481 > true 0.1019 > stale 0.0768); c stays insignificant even in the leaky variant.

**Power was reported, not assumed — and it rules out "undetected".** X ranges 0.8019 to 1.3144,
sd 0.1422, coefficient of variation 0.131; 69.8% of weeks have X > 1. Correlation with VIX is
only **−0.5324**, the expected mean-reversion signature, so X is not VIX in disguise. A genuinely
independent, well-varying input with real standalone content that adds **0.0004 of R²**.

**Result, stated absolutely as [[README]] §3 requires.** A two-state Markov-switching model on
weekly SPY returns provides **no information about forward downside risk beyond what implied
volatility already prices — on either level (D3) or dynamics (here)**. Predicted in advance,
both times.

**Why this is a strong negative rather than a weak one:** the prediction was registered before the
run, the alignment was verified adversarially, power was demonstrated rather than assumed, the
input was scale-free by construction, and both axes were tested.

**The structural reason, and it is why more modelling cannot fix it.** `F^returns ⊆ F^market`. The
option market observes the same return path plus everything else. That containment is a property
of the information set, not of the estimator, so no filter, tail shape, regime count, memory
structure or frequency escapes it.

**What this does NOT close.** VIX is **SPY-only** implied volatility. A cross-asset measure is a
genuinely different information set — covariance structure is information a single-asset option
price cannot contain. That argument is structural and survives every result in this file. It is the
only thing that does.

**Daily would sharpen these estimates and cannot change them.** The containment argument is
frequency-invariant. Daily is worth building for the *memory* question; it is not a route back into
this one, and proposing it as one would be the goalpost-moving this repo keeps catching itself at.

## STATE CHARACTERISATION — what the states actually describe (2026-08-14)

**Claim tuple: weekly · h=1 · contemporaneous realized environment (volatility, drift, tail
asymmetry, episode duration, drawdown position) · SPY 1,230 OOS weeks 2003-2026 and QQQ 898 OOS
weeks 2009-2026, vintage parameters.** Run: `.venv\Scripts\python.exe state_character.py [SPY|QQQ]`.
Figure: `figures/state_character_<ticker>.png`.

The first description of the **state** in observable market terms. Everything prior scored the
**density**; everything known about the regimes came from fitted parameters on a single whole-sample
fit. No forward window, no regression, no VIX column, no rule.

**Q1 — can the states be told apart? Yes, on width, and it replicates.** Realized volatility is
monotone across all six probability bins on both assets.

| | realized vol ratio wide/calm | block-bootstrap 95% CI | fitted σ ratio |
|---|---|---|---|
| SPY | 2.446 | [1.823, 3.124] | 2.560 |
| QQQ | 1.791 | [1.316, 2.184] | 2.477 |

Stable across sample halves (SPY 2.559 / 2.372; QQQ 1.714 / 1.638). **The direction was entailed** —
`w_wide[t]` is driven by `r[t-1]` through the likelihood ratio and volatility clusters — and is
recorded rather than claimed. The magnitude and the monotonicity were not.

**One thing does not replicate.** On SPY the fitted ratio (2.560) nearly equals the delivered one
(2.446); on QQQ the fit overstates its own discrimination by 38% (2.477 vs 1.791). "The fit does not
exaggerate its separation" is a **SPY fact, not a model fact.**

**Q2 — what do they look like? A width axis with no direction content.** This is the sign-blindness
finding reappearing out-of-sample on the state bands rather than on the fitted parameters:

| | drift, wide − calm | Welch t | down/up at \|r\|≥3%, wide | calm |
|---|---|---|---|---|
| SPY | −0.24%/wk | −0.78 | 1.12 | 1.00 |
| QQQ | +0.46%/wk | +0.91 | 0.83 | 0.90 |

**The two assets disagree on the sign of the drift difference and the down/up ratio straddles 1.0.**
That is as clean a demonstration as this sample can give that the state is a statement about
**width, not direction.** The Welch *t* is quoted without a *p*-value on purpose — the observations
and the band assignment are both autocorrelated, so a nominal *p* would be badly oversized.

**The trap, flagged because the figure makes it inviting.** SPY's `[0.99,1.00)` bin shows −60.9%/yr
drift on **n=28 weeks**, a handful of overlapping episodes. QQQ's same bin shows **+131%/yr on n=5**.
Reading either as a directional signal is exactly the error [[README]] §4 names. The figure carries
a footnote saying so.

**Persistence — the model misdescribes its own.** The one property this model class claims that a
spot measure lacks:

| | fitted expected duration, wide | realized mean band run | median | 1-week blips |
|---|---|---|---|---|
| SPY | 12.9 weeks | 5.1 | 2 | 34.2% |
| QQQ | 26.7 weeks | 4.3 | 3 | 23.5% |

**The realized run lengths are stable across assets (5.1, 4.3) while the fitted duration parameter is
not (12.9, 26.7).** SPY's second half is worse than its first (3.2 vs 7.6 weeks). **Caveat that keeps
this from being a test:** a band crossing is not a state transition, so a threshold on a continuous
probability necessarily crosses more often than the latent state switches. Part of the gap is
mechanical and this is an order-of-magnitude reading, not a calibration result.

**Drawdown position — the cleanest replication in the run, and the most decision-relevant table.**
Depth below the running peak, past data only:

| | mean dd when wide | median | % of wide weeks at a peak | mean dd when calm |
|---|---|---|---|---|
| SPY | −15.90% | −13.08% | 10.4% | −3.04% |
| QQQ | −15.52% | −13.54% | 12.3% | −2.75% |

**By the time the model says "wide", the book is already ~13% below its peak at the median.** This
is the causal-filter lag of §"Figure 2 makes the causal-filter lag concrete" expressed for the first
time in the **mandate's own variable** — depth, not variance. Partly mechanical in direction (a wide
state follows bad returns, which put you below peak); the magnitude is not entailed, and it lands
within 0.4pp across two assets.

**A prediction of mine, refuted.** I predicted from the saturation finding that the ambiguous band
would be nearly empty and an abstain path would have nothing to fire on. **It is 17.6% of SPY weeks
and 13.8% of QQQ weeks**, with only 9.0% / 5.5% of weeks outside `[0.01, 0.99]` and median `w_wide`
0.073 / 0.030. It is a *state*, not a transit corridor — its transition diagonal is 66.7% / 65.3%,
median run 3 / 2 weeks. The saturation claim above is about the **extreme top** (top-20 weeks at
P ≥ 0.99999) and the blocky VaR path, and both stand; what does not stand is the natural reading
that the signal is effectively binary. Recorded as a correction of a plausible misreading, not of a
stated claim.

**Stated precisely, because the loose version jumps A→C** (protocol §0.2 P3): what is measured is
**occupancy** — the ambiguous band is populated and persistent rather than empty. That an abstain
branch would have something to fire on is **not** evidence that abstaining is useful, which is a
question C and untouched. An earlier phrasing here — *"the abstain path is available"* — elided the
two and is retracted.

**QQQ is a weak replication and must not be quoted as an independent one.** Its OOS window starts
2009-03-06 — the 520-week burn-in swallows the GFC entirely — and QQQ correlates 0.87 with SPY
weekly. Effective sample is far below 1,230 + 898.

**Scope.** All of the above is measurement and interpretation. Whether the description is
*incremental* to what a downstream user already observes is **not** asked here and is not answerable
from these tables; for SPY it is already answered **no** on levels (D3) and dynamics, and nothing
above reopens either. No rule, threshold, sizing or action is proposed.

## Hedge economics — measured before the strand was legitimised (2026-08-13)

Two runs happened while the measure-vs-instrument boundary still applied to everything. That boundary
was scoped to the research strand on 2026-08-14 and the scope reset of 2026-08-15 makes **this the
main strand**. The line that used to head this section — *"nothing should be built on this strand"* —
is **retracted**. It was written when the signal program still looked like the source of value.

- `hedge_economics.py` — [[README]] §2's inequality (*"premium drag smaller than the drawdown
  avoided"*) measured for the first time. Naked SPY 1993-2026: **+10.82% CAGR, −54.6% maxDD**.
- **A correction is logged inside it.** A first pass priced puts off flat VIX and reported an
  efficiency of 17.58 for 15% OTM. That was an artifact of ignoring the equity skew. With a
  strike-dependent skew (0.60 vol points per 1% OTM) it is **3.6**, and at 5-10% OTM the drawdown
  benefit turns *negative* on the full sample.
- **The robust half:** the clairvoyant ceiling (expected value of perfect information, Howard 1966)
  barely moves with pricing — +2.8 to +3.2pp/yr and +18 to +22pp of drawdown across every skew
  assumption. **Cost of always-on is highly pricing-sensitive; value of timing is not.**
- `trigger_bracket.py` — payoff per dollar of premium: always-on 0.34, best VIX rule (VIX>30) 0.44,
  clairvoyant 2.98. Real VIX rules capture **4% (full sample) to 7% (2003+)** of available selection
  skill, and **no rule beats simply not hedging** on return. Eight rules on ~5 systemic episodes:
  **power to kill, not to confirm.**

## THE STRUCTURE MAP — tenor dominates, and it reorders the project (2026-08-15)

**Claim tuple: weekly marks · full holding period · geometric return and max drawdown · SPY
1993-2026 and 2003-2026 · ALWAYS-ON, h=1.00, NO signal and NO timing anywhere in the design.**
Run: `.venv\Scripts\python.exe structure_map.py SPY`. Grid: 4 tenors × 5 strikes × outright/spread,
skew slope 0.60 primary, 5% offer spread.

**All three registered predictions resolved, and one of them was wrong in a useful direction.**

- **(a) CONFIRMED, unanimously.** **0 of 40** structures beat the naked book on CAGR, in *both*
  samples. README §2's inequality — "premium drag smaller than the drawdown avoided" — **fails on
  average at every point in this grid.** The mandate's founding arithmetic does not hold as stated.
- **(b) SPLIT.** *Long tenor* confirmed decisively. *Deep strike* **refuted** — 30% OTM at 4w and 13w
  buys **negative** drawdown, and the drawdown-bought table is dominated by *shallow* strikes at long
  tenor. "Deep OTM is where tail insurance lives" was wrong.
- **(c) CONFIRMED.** Put spreads top the efficiency table (13.90) and buy 3.3-6.8pp of drawdown
  against outright's 16.8-24.3pp. Cheap, and capped exactly in the tail the program exists for.

**The result — drawdown bought (pp) @ cost (pp/yr), outright, slope 0.60:**

| strike | sample | 4w | 13w | 26w | 52w |
|---|---|---|---|---|---|
| 10% OTM | 1993-2026 | −1.1 @ 3.28 | +1.1 @ 3.39 | **+10.8 @ 2.74** | **+16.8 @ 2.36** |
| 10% OTM | 2003-2026 | +5.1 @ 2.85 | +5.7 @ 2.98 | **+17.8 @ 2.51** | **+19.9 @ 2.49** |
| 15% OTM | 2003-2026 | +4.1 @ 0.94 | +3.3 @ 1.64 | +12.5 @ 1.42 | +16.0 @ 1.70 |

**Cost is flat to falling across the row while protection triples.** This is a dominated region of the
design space, not a trade-off — and the repo sat in it for two years without measuring it.

**Against the clairvoyant bound (2003+, slope 0.60), which is what makes it a project-level finding.**
Always-on 52w 5% OTM buys **+24.3pp @ 3.74**. The *clairvoyant* 4w 5% bound is **+24.7pp**; the
clairvoyant 13w 5% bound is **+14.5pp**. **Choosing the tenor correctly with no signal at all delivers
as much drawdown reduction as perfect foresight at the tenors previously tested.** The apparent value
of timing was substantially an artifact of holding structure at 4-13 weeks.

At matched structure (13w 5%), perfect foresight adds **+1.4pp of drawdown and +8.46pp/yr of
premium**. **A signal is a cost-reduction device, not a protection device** — the first statement of
what a signal is *for* that this repo has derived from the decision rather than from statistics.

**Two things this run refutes about its own predecessor.**

- **Efficiency is not a usable selection metric.** Its denominator goes to zero: at slope 0.00 the
  grid's best efficiency is **218.23 at a cost of 0.03pp/yr** — a structure that protects nothing.
  The script's own warning was right and its footer ("eff … is the right metric for comparing
  STRUCTURES") contradicts it. **Rank on drawdown bought at a stated cost.**
- **The whole grid is conditional on an unverified skew parameterization**, and it favours the
  conclusion. `skewed_vol` scales skew as `sqrt(4/tenor)`, so long tenors are assumed to carry far
  less skew per point of moneyness. The repo has no option chain. Best-efficiency structure swings
  from 4w to 26w and from eff 218 to 9.22 across slope 0.00→0.80. **This is the single largest
  caveat on the finding and it now has a cheap fix** — `options-quant` has archived point-in-time SPY
  chains since 2026-08-14 with 25Δ skew per expiry.

**Not covered, stated so the run is not read as complete:** recycling (`simulate` reinvests passively
at the next roll; never sized deliberately), the honest competitors (trend sleeve, long duration),
and the 26w/52w clairvoyant columns, which do not exist.

## E0 — THE DRAWDOWN REDUCTION IS MOSTLY A MARK (2026-08-18)

**Claim tuple: weekly marks · full holding period · the drawdown process D(t) and its functionals
(CDaR_alpha curve, per-excursion depths, time under water; max drawdown as a labelled diagnostic) ·
SPY 1993-2026 and 2003-2026, one path · ALWAYS-ON h=1.00, no signal, roll phase 0.**
Preregistered in [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]], committed before the code existed.
Run: `.venv\Scripts\python.exe research/m3_decomposition.py SPY`.

**The experiment is one accounting difference**, and that is the whole design. Same path, same
parameters, same contracts, same cash flows; the only change is *when the hedge is recognised as
wealth*. `W_marked` carries the put's model value continuously — which is what every drawdown number
in this repo has always been computed from. `W_cash` carries it only when it becomes a cash flow, at
expiry, which is the only moment `simulate` has ever actually transacted it.

**The precondition held exactly.** The two curves agree to `0.00e+00` at every roll boundary, at the
terminal date, and on premium and payoff, at all four tenors. Not "close" — zero. So the difference
is entirely interior, CAGR is untouched, and the result is a decomposition rather than a comparison
of two programs.

**H3 is REJECTED**, in fifteen of the sixteen cells where the ratio is reportable, in both samples and
at all three strikes. Drawdown bought, 10% OTM:

| sample | | 4w | 13w | 26w | 52w |
|---|---|---|---|---|---|
| 1993- | marked | −1.1 | +1.1 | +10.8 | **+16.8** |
| 1993- | **cash** | **−4.7** | **−4.8** | **+3.2** | **+3.0** |
| 2003- | marked | +5.1 | +5.7 | +17.8 | **+19.9** |
| 2003- | **cash** | +1.1 | −0.9 | **+4.4** | **+3.0** |

> **+16.8pp becomes +3.0pp. +19.9pp becomes +3.0pp. The best cell in the repo, +24.3pp, has never
> been quoted in cash at all.**

**What this does to E10, the largest measured effect in the repo.** The *sign* of the tenor ordering
survives — long tenor beats short, which is M1, strike anchoring, and it is arithmetic about where the
strike sits rather than anything about pricing. Everything else about the row changes. The cash
reduction is **flat from 26w to 52w**, it is *larger at 26w* on the 2003- sample, and at 4w and 13w it
is **negative on the full sample**: the program makes the worst drawdown about 5pp deeper than never
hedging, because premium is paid continuously and the payoff lands after the trough. The monotone
climb across the marked row is a mark that grows with the length of the block interior — 51
unrecognised weeks at 52w against three at 4w. **Read the marked row as the ordering and the cash row
as the size.**

**In the well-sampled coordinate the cash reduction is approximately zero.** CDaR_alpha, full sample,
52w: cash reduction is −0.5 / +0.0 / −0.2 / −0.6 / −1.0 / −0.8 across alpha 0.01 → 1.00, against a
marked +10.0 → +1.0. The 2003- subsample does show a real cash benefit concentrated at the extreme
end (+0.6 / +3.5 / +2.9 at alpha 0.01 / 0.05 / 0.10), and 26w is stronger there than 52w. This is
exactly the job CDaR was built for: the marked effect decays smoothly in alpha, the signature of a
statistic resting on the deepest part of one episode, and the cash effect has almost nothing to decay
from.

**The mark erases excursions the investor still lives through.** Full sample, excursions deeper than
10%: naked 9, 52w marked **6**, 52w cash **9** — the same nine the unhedged book has. Time under water
at 10%: naked 31.7%, 52w marked 29.1%, 52w cash **34.1%**. **In cash, the hedged book spends more time
under water than if it had never hedged**, because premium drag is continuous and the offset is not.
"Smooth the ride" is one of the mandate's three stated goals, and on this path, at this phase,
measured in cash, the 52-week program did the opposite of it.

**What it does NOT establish, and this matters as much as the rest.** Not that the marked number is
wrong — cash accounting is not the truth either, since a real investor can sell mid-life. The
realizable path under any stated rule lies *between* the two curves. What E0 establishes is that
**the accounting interval is wider than the effect inside it** — 13.9pp of gap within a 16.8pp claim —
so no point in it can be quoted. And it adds **no observation**: one path, one crisis, one unswept
roll phase, effective n = 1 on the benefit side still. The 82% is an accounting fact about this path,
not an effect size.

**Consequences, booked the same day.** E6 (`specify rho, measure kappa`) is reclassified from queued
experiment to **precondition** — no drawdown magnitude in this repository is interpretable until it
runs. E1 (roll-phase sweep) is **promoted**, because how much of a crisis falls inside a block
interior is exactly what phase sets, and that is what the size of the mark depends on. And no number
here may be quoted as a drawdown reduction without naming its accounting.

**One process note, recorded against myself.** The stub declared a denominator floor for `gap_share`
because the denominator was known to approach zero, and then predicted the *ratio* at precisely the
tenors where that floor binds. The floor did its job — those cells print INDETERMINATE instead of
531% — but the prediction should have been stated in pp of gap. F7, twice in one document, in
opposite directions.

**And a second, larger one: the literature gate was skipped.** [[docs/literature/README]] lists
Israelov (2017), *Pathetic Protection*, as **blocking on E0**, and yesterday's carry-over note said
so in as many words. E0 ran first; the paper was read afterwards, on the same day. The verdict is
mixed and worth having in full:

- **E0's design survives.** The paper never distinguishes marked from realized value — zero
  occurrences of *mark-to-market*, *unrealised* or *monetise* in the text, and every drawdown it
  reports is computed on a marked NAV. **The decomposition is not in the literature.** Honouring
  the gate would have changed nothing about the run.
- **But E10 was a rediscovery.** The paper sweeps 20 / 63 / 250 business-day maturities — our 4w /
  13w / 52w — and concludes that *"longer-dated options do a less bad job of protecting a portfolio
  against long-term drawdowns than shorter-dated options. Less bad, but not good."* That is E10's
  ordering and, in cash, roughly E0's magnitude, in a paper sitting `[UNREAD]` as **row 1** of the
  reading list while both were derived from scratch. Second §0-rule-3 failure in this repo's
  history; the first was Timmermann's Proposition 5, also row 2 of a list at the time.
- **E1 is respecified by it.** The paper's central mechanism is expiration-cycle misalignment:
  *"equity drawdowns have lives of their own that may not conveniently coincide with option
  expiration cycles."* That phase matters is therefore **citable, not testable**, and a run showing
  it carries no information. E1 now measures the quantity the paper does not supply — the **phase
  spread relative to the effect**, which is what H2 actually turns on.
- **Its remedy is inadmissible here, and that is the load-bearing difference.** The paper's
  comparison alternative throughout is static divestment — 36.5% equity, 63.5% cash, matched to
  PPUT's realized return. [[CHARTER]] §2's C2 excludes exactly that. **Its verdict does not bind
  this mandate; its mechanisms bind it completely.** The permanent-long constraint is what makes
  the paper's recommendation unavailable and its evidence entirely relevant — which is the worst
  possible combination to have skipped.


## E1 — THE TENOR MAGNITUDE IS ALIGNMENT-DEPENDENT (2026-08-18)

**Claim tuple: weekly marks · full holding period · drawdown bought versus the naked book, on max
drawdown and on `CDaR_0.05` · SPY 1993-2026 and 2003-2026, one path · ALWAYS-ON h=1.00, 10% OTM, no
signal and no conditioning of any kind.** Preregistered in [[closed-research/intervention/STUB-E1-ROLL-PHASE]], committed
before the code existed. Run: `.venv\Scripts\python.exe research/phase_sweep.py SPY`.

**E1 asked one question and answered it.** `simulate` walked blocks from index 0, so the alignment of
every roll against the 2007-09 decline was set by the sample's first date and nothing else. The sweep
moves the roll grid without moving the sample -- at phase `p` the first block is a stub of `p` weeks
-- and reports the resulting spread **relative to the tenor effect it is supposed to qualify**. Every
offset, no selection: 4 + 13 + 26 + 52 alignments per accounting per sample.

**Verdicts against the rule fixed before the run:**

| sample | acct | effect | spread at 52w | R | verdict |
|---|---|---|---|---|---|
| 1993- | marked | +18.0 | 12.7 | 0.71 | MARGINAL |
| 1993- | **cash** | +7.6 | 14.1 | **1.85** | **KILLED** |
| 2003- | marked | +14.7 | 12.5 | 0.85 | MARGINAL |
| 2003- | **cash** | +1.8 | 12.6 | **6.82** | **KILLED** |

Nothing anywhere reached the preregistered SURVIVES threshold of `R <= 1/3`. In `CDaR_0.05`, the
declared artifact check, the ratios are 0.79 / 1.41 and 1.14 / 4.10 -- **the sensitivity is not a
max-drawdown artifact**, and on the 2003- marked cell the CDaR ratio would have flipped MARGINAL to
KILLED. The rule keyed on max drawdown, so the recorded verdict stands and the CDaR number is
reported beside it.

> **In cash, the sign of the 52-week result is set by the roll calendar.** Same program, same path,
> same contracts: at one arbitrary offset it removes 7.8pp of drawdown, at another it adds 6.3pp.
> Published cell: +3.0.

**The ordering, which is the part that survives.** `separation = min_p bought(52w) - max_p
bought(4w)`: **+6.0pp** (1993-) and **+13.1pp** (2003-) in marks -- long tenor beats short at **56 of
56 alignments tested**. In cash it is **-9.0pp** and **-7.5pp**: there are alignments at which a
4-week program buys more than a 52-week one. **Combined with E0, the only claim left standing about
tenor is a marked-accounting ordering. Every magnitude, in both accountings, is gone.**

**The published number was never cherry-picked -- it was arbitrary.** On the 2003- sample `p = 0`
gives +19.9, the *second lowest of 52* alignments.

**One diagnostic that changes how the marked column should be read.** The naked book's max drawdown
is set in 2009. The hedged book's, on the full sample at 26w and 52w in marks, is set in **2003** --
in 25 of 26 and 51 of 52 phases. So `+16.8pp` never meant "the 2008 drawdown was 16.8pp shallower".
It meant the 2008 trough was pushed below the 2003 trough, after which the statistic stopped
measuring 2008 at all: **max drawdown is censored from below by the next-deepest episode.** The 2003-
subsample is the control -- it excludes the dot-com decline, its episodes match, and its marked ratio
is still 0.85. The phase sensitivity is real and is not an artifact of episode switching. The
coordinate problem itself is parked to E2, which exists to replace this coordinate.

**Predictions, scored.** `R(52w) > 1` in marks on the full sample: **REFUTED** at 0.71, and the
post-hoc reason is the censoring above -- the prediction was about the 2008 window, and the
coordinate had stopped reporting on it. `separation > 0` marked and `<= 0` cash: **CONFIRMED**, both
samples. And a claim the stub called *derivable* -- that spread grows with tenor -- is **REFUTED**:
full-sample marked spreads run 11.8 (4w), 12.6 (13w), **14.1 (26w)**, 12.7 (52w). A four-week program
has an 11.8pp spread over four alignments. Block length bounds how far an alignment can slip; it does
not determine how much the outcome moves, because that depends on whether a given window happens to
contain October 2008. Filed as an error in the stub's §2, not as a finding.

**What it does not establish.** Nothing about a second crisis: the 52 phases are 52 overlapping views
of one episode, no standard error was computed and none may be, and **effective n on the benefit side
is still 1**. Nothing about timing or signals -- the phase is swept exhaustively, never selected, and
the prediction program stays closed. And no new magnitude: E1 produces no quotable number. It removes
one.

**E1 triggered nothing automatically.** E2 and E3 stand where they were; what runs next is an open
decision, deliberately not taken inside the experiment that preceded it.


## E2 — THE ESTIMAND REPAIRED, AND THE ORDERING DOES NOT SURVIVE THE REPAIR (2026-08-18)

**Claim tuple: weekly marks · full holding period and per-episode windows within it ·
`CDaR(worst q%)` reduction as a curve, and episode-matched depth reduction · SPY 1993-2026 and
2003-2026, one path · ALWAYS-ON h=1.00, 10% OTM, no signal and no conditioning.** Preregistered in
[[closed-research/intervention/STUB-E2-DRAWDOWN-PATH]], with the identification status of each coordinate written **before**
the run. Run: `.venv\Scripts\python.exe research/path_outcomes.py SPY`.

**The gate was closed first this time.** Chekhlov, Uryasev & Zabarankin read before the run, not
after, and it found a real defect: **their `alpha` is a confidence level and ours is the fraction
averaged**, so our `CDaR_0.05` is their `0.95`-CDaR and a bare label reads as its own opposite. Also
recorded: our estimator is the *upper* CDaR with a bounded gap, and their convexity result is in the
portfolio weights and licenses nothing here. [[docs/MATH-REFERENCE]] §4.1.

**What E2 repaired.** E1 showed `max(D)` on the hedged and naked paths describing *different
episodes* — 2003 versus 2009, in 51 of 52 alignments. E2 replaced it with two coordinates that cannot
do that: `CDaR(worst q%)`, which integrates the whole path, and **episode-matched depths**, where
episodes are defined once on the **naked** book and both books are measured inside the same calendar
windows from their own peak within each. Defining the windows on the naked book is the load-bearing
choice; windows taken from the hedged path would move with the intervention.

**V1 — the ordering, phase-robust, at every `q`:**

| sample | acct | worst 1% | 5% | 10% | 25% | 50% | 100% |
|---|---|---|---|---|---|---|---|
| 1993- | marked | **+2.0** | **+0.5** | **+0.2** | **+0.2** | -0.2 | -0.1 |
| 1993- | cash | -8.0 | -7.4 | -5.6 | -3.8 | -3.4 | -2.0 |
| 2003- | marked | **+8.9** | **+4.0** | -0.2 | -3.1 | -2.7 | -1.5 |
| 2003- | cash | -9.3 | -8.7 | -7.6 | -7.2 | -5.6 | -3.1 |

**In cash the ordering survives NOWHERE, at any `q`, in either sample.** In marks it survives at
`q <= 25%` (1993-) and `q <= 5%` (2003-) — and the full-sample margins at 5%, 10% and 25% are +0.5,
+0.2 and +0.2pp, which is survival by the letter of a preregistered rule and by nothing else.

**And then the `Psi` column, which is what the whole curve was built to produce.** Distinct episodes
contributing to the worst `q%` of the process: at `q = 1%` and `5%` the marked tail rests on **one or
two episodes**; at `q >= 50%` all nine contribute.

> **The ordering survives exactly where the coordinate has collapsed onto one or two episodes, and
> fails exactly where the coordinate is well sampled.** The sample-size problem was converted into an
> output rather than argued about, which is the entire reason CDaR was specified as a curve.

**V2 / V3 — the episode-matched coordinate.** Over (episode x 52w-phase x 4w-phase) triples:

- **marked: 52w >= 4w in 90-94%** of pairs, both thresholds, both samples. **SURVIVES** — and this is
  the strongest positive result the intervention side of this repo has produced.
- **cash: 48-61%**, MARGINAL to KILLED. And **V3 is the number that stops V2 being read as good
  news**: in cash the 52-week programme reduces episode depth in only **16.5-27.9%** of pairs, so it
  **deepens** the episode three-quarters to five-sixths of the time. The cash ordering is between two
  harms.

**The episodes, phase 0, full sample, in cash.** 2008: **+3.0pp**. Everything else: -0.0, -0.0, -2.0,
-6.1, +0.0, **-0.0**, -2.6, -0.0. **The entire cash-side benefit in thirty-three years is one
episode.** The 2020 row is E0's finding in episode form: **+24.9pp of marked protection through
February-March 2020, and -0.0pp in cash** -- the option was never sold, and the market recovered past
it.

**Predictions.** "Marked survives at small `q`, at risk at large `q`" and "cash fails at every `q`":
both **CONFIRMED**, the second with no margin close to zero. "Episode sign-consistency >= 2/3 marked,
< 1/2 cash": **SPLIT** — marked confirmed, cash came in at 48-61%, below SURVIVES everywhere but only
*at* KILLED in one of four cells. Directionally right and too strong, recorded as the rule says.

**What it does not establish.** No magnitude and no population claim: one path, episodes that are not
exchangeable, phases that are not independent. The V2/V3 fractions are counts of a deterministic
sensitivity and **no standard error or test statistic may be derived from them** — that was written
into the stub before the run. Nothing about cost, outlay or monetisation, which are E6 and E7.
Nothing that promotes `q = 1%` to a preferred coordinate: the surviving points are the *least*
identified ones on the curve, which is the finding rather than a selection criterion.

**Consequence for the one claim still standing.** [[CHARTER]] §9.1's preserved structural ordering
keeps its status but gains a qualifier it cannot be quoted without: it is an **episode-level,
marked-accounting regularity about deep episodes**, and it is absent on the well-sampled part of the
drawdown path.

**E2 triggered nothing. E3 was not started.**


## E4 — M1 IS A DEDUCTIBLE-COUNT EFFECT, AND IT IS CONDITIONAL (2026-08-18)

**Claim tuple: weekly W-FRI closes · H = 52 weeks primary, 104 robustness · the SIGN of the gross
intrinsic payoff difference, no magnitude reported anywhere · ^GSPC 1927-2026, ^N225 1965-, ^FTSE
1984-, ^GDAXI 1988- (12,601 weekly observations, 29 episodes at 20%) · every week with a complete
horizon is a start, and NO start is placed at a peak.** Preregistered in
[[closed-research/intervention/STUB-E4-STRIKE-ANCHORING]], amended once — also before any run — to record that the verdict
rule is biased toward M1. Run: `.venv\Scripts\python.exe research/anchoring.py`.

**Not a rescue attempt, and it could not have been one.** Nothing in E4 is priced and no premium is
paid anywhere in it. E9, E0, E1 and E2 stand unchanged and the economic hypothesis for rolled
outright puts remains provisionally negative.

**What M1 actually is, derived before the run and confirmed by it.** With `a_i` the decline over
sub-period `i`, at `m = 0`:

```
    P_restriking = SUM max(a_i, 0)  >=  max(SUM a_i, 0) = P_anchored
```

the positive part of a sum never exceeds the sum of positive parts — so **without a deductible the
re-striking leg weakly dominates on every path, always.** M1 is therefore not "long contracts protect
better". It is **a deductible charged once versus the same deductible charged `H/s` times**, and when
every leg finishes in the money the difference is exactly `m · (SUM of re-strike levels − S_0)`. The
`m = 0` control reproduced this to the bit: `max(anchored − restriking) = 0.00e+00` in all four
markets.

**The verdict, in the order the stub requires.**

| | |
|---|---|
| preregistered rule | **M1 SURVIVES** — 4 of 29 episodes flip = 13.8%, against a 1/3 kill line |
| diagnostic declared before the run | **CONTRADICTED** — excluding starts where both legs pay zero, **15 of 28 = 54%** flip |
| therefore | *survival on a biased rule, contradicted on the diagnostic* — **not to be quoted as M1 holding** |

The whole gap is ties: starts whose horizon sits in flat or rising prices, where both legs pay zero
and the preregistered rule scores that as a vote *for* M1. **Had the amendment not been written
before the run, 13.8% would have been the headline.**

**The deductible sweep, and it is decisive.** Flip share on the diagnostic, `H = 52` — higher is
worse for M1:

| `m` | s=4 | s=13 | s=26 |
|---|---|---|---|
| **5%** | **100%** | **100%** | 83-90% |
| 10% | 54-61% | 76-77% | 76% |
| 15% | 40-45% | 59-70% | 69-74% |

> **At a 5% deductible M1 fails in every single episode, in every market.** The effect is a property
> of large deductibles, not of long tenor, exactly as the identity says.

**The shape split is the finding.** Anchoring wins persistent grinds — S&P 1973-80 (65%), S&P 2000-07
(72%), Nikkei 1989-2024 (56%), FTSE 1999-2015 (57%) — and loses V-shaped crashes: **2020 at 0/53 in
both the S&P and the DAX**, 1987 at 5/54 and 8/62, DAX 1998 at 0/69, Nikkei 1970 at 1/94. A contract
struck in February 2020 expired in February 2021 above its strike having paid nothing, while
four-week legs collected March as it happened.

**And that routes straight into the closed programme.** The condition deciding M1 is whether the
coming decline grinds or V-bottoms — **a property not observable at the moment the contract must be
bought.** Forecasting it is the problem [[docs/PROBLEM-MAP]] Part I closed. **M1 is real, conditional,
and unusable without the one capability this programme has established it does not have.** Parked as
*unavailable* rather than queued, in [[PARKED]].

**Predictions.** "Failures concentrated in V-shapes, 2020 and 1987 against": **CONFIRMED sharply.**
"More favourable at larger `m`": **CONFIRMED**, monotonically. "More favourable at `H = 104`":
**REFUTED** — the diagnostic flip share rises to 89-98%, because the §3 reasoning counted the extra
deductibles and forgot that a two-year contract has two years in which to expire out of the money.
Half a mechanism asserted as the whole one.

**`Psi`.** 29 episodes is not 29 observations: 2000-07, 2008, 2020 and 2022 appear in three or four
markets each and are one event reported several times. Only five episodes have no cross-market
calendar overlap, and **the genuinely independent content is US 1929-1954 and Japan 1990-2003** —
perhaps 12-15 distinct events, not 29. Two mega-episodes (S&P 1929-54, Nikkei 1989-2024) carry 42% of
all starts, a known limitation of the inherited peak-to-recovery definition that was **not** re-tuned
after seeing the result. Starts overlap almost completely, so `n_starts` is not a sample size and no
standard error, test statistic or population magnitude appears anywhere in E4.

**E4 stopped where its stub said it would.** No pricing, no monetisation, no additional structures,
no progression to E5/E6/E7. The outcome is neither the clean failure that closes the rolled-put/tenor
branch nor the clean survival that triggers a reassessment, so **the branch decision is recorded as
open and was not taken inside the experiment.**


## S0 — WHAT COUNTS AS EVIDENCE, AND THREE CANDIDATES DIE (2026-08-18)

**Preregistered** in [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]], with the sweep, functionals and
matching declared in a separate commit before any code. **No market data.** 18 parameter cells, 400
replications per class per cell, seed 20260818.

**The setup.** A two-state switching process against GARCH(1,1) — the charter's null N1 — calibrated
to match so the easy differences are gone. The match turned out **exact on more than intended**: both
squared-return ACFs are geometric from lag 1 (Timmermann Prop. 5, E6 here), so fixing GARCH
persistence at the chain's second eigenvalue and solving one `alpha` for `rho(1)` matches the whole
ACF at every lag, residual 1.8e-15. The surviving mismatch is **kurtosis**, and it is large — up to
38.6%. That mismatch became the floor every separation had to clear.

**The results, against predictions written before any code:**

| | predicted | measured | |
|---|---|---|---|
| squared-return ACF | `d' ~ 0`, correctness check | 1.035 | matching confirmed; **residue is a fourth-moment effect in the estimator, not the population** |
| aggregate kurtosis, `h>1` | different but small | 1.59 vs a floor of 6.80 | **HELD.** Too small to use |
| block realized-variance dispersion | **dies at matching** | **10.22** | **PREDICTION WRONG** |
| max drawdown / CDaR(5%) | separates in expectation, unestimable at `n` | 0.15 / 0.14; 0.645 vs 0.647; 6.1 excursions per 33 years | **HELD** |

**The wrong prediction is the most useful thing here.** §5.2 argued deductively that matching the
whole squared-return ACF would kill the block-variance coordinate. It did not, because **the ACF is a
second-order object and the dispersion of block realized variance depends on the shape of the
variance process.** A two-state chain makes a 21-day block mostly-one-state; a GARCH variance drifts
through a continuum. Identical autocovariance at every lag, different distribution. **Second-order
equality is not equality.** The claim is withdrawn in the results and left standing in the
preregistration, because a stub edited after the fact is worthless.

**And the negative that closes a route.** Path geometry cannot carry a state-existence claim: `d' =
0.15`, mean max drawdown 0.645 against 0.647, 6.1 excursions past 10% per simulated 33-year history.
**Measured where the states exist by construction** — so unlike a market measurement, its silence is
informative rather than ambiguous.

**Verdict: H(S0) survives conditionally.** Q1 exists, its functional and block length are fixed and
not re-chosen, three candidates are forbidden to it, and it inherits a condition — the functional
never survives at a variance ratio of 2, so a Q1 negative is INCONCLUSIVE unless Q1 demonstrates
power against the contrast the market actually has. [[CHARTER]] §9.1.

**Governance updated, and stopped there.** No second synthetic study, no third model class, no search
for a better functional.

## Next

**Nothing. The repository is closed.** Three programmes, three closures, one preserved and
reproducible record. A fourth would require a new charter, argued from the start.

**There is no queue in this file.** [[CHARTER]] §9 is the single experiment queue, and two documents
proposing next steps is how a second research program starts.

**PROGRAM TRANSITION 2026-08-18 — the second one.** Both the prediction/regime program (closed
2026-08-17) and the rolled-put/tenor intervention program (closed 2026-08-18) are preserved,
reproducible, in `closed-research/`. The active program is **return states**: [[CHARTER]]. What is
queued is **S0 only** — the identification problem, worked before anything is measured.

**Nothing from the intervention queue carries forward.** E3, E5, E6 and E7 are closed with the
programme, not parked as future work; they were downstream of a claim that no longer stands. See
[[PARKED]] §1.

Everything above this line is the chronological record and stands as written, with one standing
caveat that attaches to the structure-map entry and to every number derived from it:

> **The benefit side has effective n = 1.** `summarize` returns `max_drawdown` as a single `.min()`,
> and on both reported samples that statistic is set by the same episode (Oct 2007 - Mar 2009). The
> **orderings** are probably robust; the **magnitudes** are one draw at one unswept roll phase and are
> not identified. [[CHARTER]] E1 and E2 test exactly this. **E0 has now run (2026-08-18) and the
> answer is that the reduction is mostly a mark** — 82% of it at 52w on the full sample — which makes
> the caveat above stronger, not weaker: the magnitudes are one draw at one phase *and* they are
> quoted in an accounting the investor cannot bank.

The four "actual next actions" previously listed here — fit the real skew surface, extend the
clairvoyant grid, decide the objective, specify recycling — were written on 2026-08-15 under the
framing this transition replaces. They are not deleted from the project: the clairvoyant extension is
[[CHARTER]] E3, the surface is E5 (reclassified as procurement, never prediction), and recycling is
E6. The objective question is answered by [[CHARTER]] §1.

## Registration

Registered 2026-08-20 in `C:\dev\INDEX.md` and in the repo table in `C:\dev\CLAUDE.md`, in both cases
**as a standalone repository that shares the `systematic-investing-research/` directory and is not part
of the governed stack.** It is not covered by the charter in `regime-detection/governance/` and is not
audited against it. Remote: `github.com/AdamMooo/core-risk-overlay`.

**`regime-detection` is not this repo's problem and is not to be raised here.** It was a learning
ground — jump models, k-means, lag experiments — it lives on `AdamMooo/regime-detection`, and it will
be revisited on its own terms. This repository is **neither an extension nor a successor** of it and owes
it no reconciliation. Raised three times on 2026-08-15 as a "migration risk"; that was wrong each time,
and it is now [[CLAUDE]] §3 cross-repository gravity, [[docs/RESEARCH-PROTOCOL]] P12, and
[[docs/PROBLEM-MAP]] standing rule 5.

## Related

- [[README]] · [[docs/RESEARCH-PROTOCOL]] · [[docs/MATH-REFERENCE]] · [[docs/POINT-IN-TIME-DISCIPLINE]]
- [[look-ahead-bias-is-self-concealing]] — vault lesson from this work
- [[INDEX|Home]]
