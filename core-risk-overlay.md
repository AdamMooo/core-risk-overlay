---
type: project
---

# Core-Risk-Overlay

Last updated: 2026-08-27

**NO ACTIVE RESEARCH PROGRAMME.** Three have run and all three are closed — see [[README]]. This file
is the chronological status log, newest first. **The repository name is historical.** It names a
program that no longer runs.

## Map

**Authority — read in this order:**

- [[CLAUDE]] — repository purpose, repository gravity, agent behaviour
- [[README]] — what is established, and what counts as a result
- [[docs/RESEARCH-PROTOCOL]] — the gate every experiment passes
- [[docs/POINT-IN-TIME-DISCIPLINE]] — time basis and leak register
- [[PARKED]] — deliberately excluded, each with its unparking condition

**Closed 2026-08-27 — the SJM reproduction (Thread A; a reproduction, not a programme):**

- [[docs/REPRO-SJM2024-FINDINGS]] — findings, fidelity audit, and the completed inference run with
  its Z0–Z5 verdicts. Code archived at `closed-research/reproduction-sjm2024/` (35+28 frozen checks)
- [[docs/MATH-AUDIT-JUMPMODEL]] — what the estimator is, exactly, and what lambda means
- [[docs/MATH-REFERENCE]] — live conventions: the drawdown process and the CDaR family

**Proposals — STATUS: PROPOSAL, nothing authorised:**

- [[docs/ASSESSMENT-PRESENT-STATE-RISK]] — Thread B, present-state risk description; Screen 0 ran,
  Screen 1 withdrawn (filtration, not states), the level-conditional decay profile is the named object
- [[docs/ASSESSMENT-RETURN-AT-RISK]] — untouched since 2026-08-20

**The three closed programmes — self-contained, reproducible archives:**

- [[closed-research/README]] — prediction/regime (closed 2026-08-17: nested inside VIX on levels and
  dynamics)
- [[closed-research/intervention/README]] — rolled-put/tenor (closed 2026-08-18: the drawdown
  reduction was mark, not cash)
- [[closed-research/return-states/README]] — return states (closed 2026-08-19: INDETERMINATE at a
  synthetic identification gate) · its charter and termination: [[CHARTER]] §11
- [[docs/PROBLEM-MAP]] — the frozen evidence and lessons of all three
- [[closed-research/HUB-RECORD]] — this file's pre-closure working record 2026-08-12 → 2026-08-18,
  moved verbatim 2026-08-27

## Status — 2026-08-27, twelfth entry: THREAD A CLOSES — Z3 INSIDE ON ALL NINE, Z4 WIDE — NO POWER EVEN WITH REGIMES REAL, THE REPRODUCTION IS ARCHIVED

> **N2 completed on its fourth launch** (detached 13:28 → 15:40; 200 paths, 7,735s on 12
> workers), the CSV at 200/200/200 with the two stale rows replaced by the resume-safe writer as
> designed. Integrity ran on two independent routes before anything was read: the N1 table
> reproduced from the raw rows, seed sets exact, observed gaps byte-identical to `inference.log`,
> null fits unchanged.
>
> **Z3 CONFIRMED as preregistered.** All nine band × statistic comparisons inside N1's 95%
> intervals; the IUT never armed (max percentile 40.5%); the (85,65) family quoted only as the
> 10pp-exposure comparison the Z0 amendment requires. The licensed sentence, and only it: the
> observed deep-tail gaps are *indistinguishable from what two rules of these exposures do to each
> other on a clustered path*, on 34 years of daily ^GSPC at these functionals.
>
> **Z4, read under the pre-read amendment** (commit 5cd0abf, written and committed while N2 still
> ran: width not zero-crossing, the scoped power sentence not the universal, the N2 verdict column
> declared unread): under the fitted regime-true world the deep-tail gap distributions are 39–45pp wide — the same width clustering alone produces under N1 (38–43pp) — so the comparison has no power to detect a regime-driven edge at this sample length even when the jump model's premise is true by construction. The scoped sentence, not the preregistration's universal; no magnitude quoted.
>
> **D8 stays retired** — Z5's episode-stability for the two tight bands is recorded as the
> descriptive fact it is, not an identification; the unpicking condition (a real residual under N1)
> did not arrive. D2, HMM and D7 stay retired with it. **Thread A is closed.** The code is archived
> at `closed-research/reproduction-sjm2024/` on the three-precedent convention (own README, 35
> frozen checks + 28 package cross-checks, frozen copies of the shared modules); root `checks.py`
> drops to 37; eight dead run logs deleted and the manifest regenerated. The findings doc carries
> the run section, the final summary line, and four conceded audit notes. Thread B
> ([[docs/ASSESSMENT-PRESENT-STATE-RISK]]) is untouched and is the only live proposal.

## Status — 2026-08-27, eleventh entry: THE DEEP CLEAN — ONE ARCHIVE PER PROGRAMME, THE HUB IS A HUB AGAIN, AND N2 IS ON ITS FOURTH LAUNCH

> **N2 died a third terminal-tied death and is running again, detached.** The morning's sequence:
> the N1N2 detached run completed N1 (200 paths, 5,490s, appended 11:25) and the 12:34 reboot killed
> N2; a 12:43 relaunch was not detached and died at ~13:16 when its parent vanished (one pool-worker
> WinError 5) — and its `manifest.py` provenance line had been written **ahead of the run**, claiming
> a scored table that never existed. Corrected, and recorded here so the pattern has a name:
> provenance describes what a log *is*, never what a run is hoped to produce. Relaunched 13:28 via
> `Start-Process` — the exact pattern that carried N1 through 91 minutes — logging to
> `data/deeptail_mc.N2retry.log`; 12 workers confirmed healthy at 14:05. The CSV holds N3 200 / N1
> 200 / N2 2 stale rows the writer replaces on completion. **Nothing was scored. Z3 and Z4 remain
> the only open verdicts, and Thread A does not close until they are read from the completed CSV.**
>
> **The return-states archive is now self-contained, like the other two.** Its four supporting
> documents — both preregistration stubs, [[closed-research/return-states/IDENTIFICATION-UNDER-N1]]
> and [[closed-research/return-states/DECISION-Q1-CLAIM]] — moved verbatim from `docs/` into
> `closed-research/return-states/` (git recorded renames at 96–98% similarity), with every wikilink
> retargeted: [[CHARTER]], [[README]], this file, the documents' own cross-references, and the two
> archive scripts' pointer strings. All 180 frozen return-states checks pass after the move; the
> archive README claimed "140 checks" and now states the measured 180. The charter stays at root —
> the §7 authority table is its home.
>
> **The hub is a hub again.** This file's 1,094-line pre-closure body — the governing frame, the
> mandate's target, the open questions, the known defects, and every experiment write-up from
> 2026-08-12 to 2026-08-18 — moved verbatim to [[closed-research/HUB-RECORD]]. What remains is the
> status log plus a navigation map of every document. [[docs/MATH-REFERENCE]] and
> [[docs/MATH-AUDIT-JUMPMODEL]] join the [[CLAUDE]] §7 authority table (the daily note had flagged
> the former: it binds the CDaR convention and is cited from source code).
>
> **The learning got a vault note.** [[systemic-events-are-too-rare-to-calibrate]] now exists in
> `C:\dev\lessons\` — the n=1 benefit side, the two-episode SJM edge, and Z2's ±0.10-margin wall are
> one lesson — and the two documents that cited the phrase as prose
> ([[docs/REPRO-SJM2024-FINDINGS]], [[docs/ASSESSMENT-PRESENT-STATE-RISK]]) now link it.
>
> **Vault-side, the queued audit items are done** (VA-030/031/033/035/036/037): the INDEX's
> dismantled-stack section is replaced by the truth (this container holds one repo; check counts
> corrected 37→72, 140→180), dead project links pruned, the stale memories deleted or corrected, and
> the graph mirror reconciled. `C:\dev\CLAUDE.md`'s structure diagram and repo table now match the
> disk. **Next: read Z3/Z4 from the completed CSV, write the run section in
> [[docs/REPRO-SJM2024-FINDINGS]] once and whole, regenerate the manifest.**

## Status — 2026-08-27, tenth entry: N1/N2 RELAUNCHED DETACHED, AND THE MODEL GETS ITS MATHEMATICAL AUDIT; Z3/Z4 STILL THE ONLY OPEN VERDICTS

> **Housekeeping first: the branch sprawl is gone.** Every branch — four locals plus two remote
> copilot stubs — was verified fully contained in `repro-sjm2024` before anything was deleted;
> `main` fast-forwarded to a521c35 and pushed; everything else removed locally and on GitHub. One
> branch remains, and it is `main`.
>
> **The N1/N2 deaths have a probable cause, and the fix is procedural.** Both prior attempts were
> launched from inside a session terminal and died at or near session close (the 21:43 resume
> wrote nothing in 55 minutes; `pool.map` persists a null's rows only after all its paths finish,
> so partial progress dies with the process). Relaunched 2026-08-27 via `Start-Process` — detached
> from any terminal — logging to `data/deeptail_mc.N1N2.log`; both null fits loaded from cache and
> the pool was simulating at last check. **Nothing has been scored; Z3 and Z4 remain the only open
> verdicts, and Thread A does not close until they are read from the completed CSV.**
>
> **The jump model now has a mathematical audit: [[docs/MATH-AUDIT-JUMPMODEL]].** Method: the
> implementation translated line-by-line into the exact objective; two independent literature
> sweeps, one instructed to attack the "k-means + switching penalty" characterization; six
> computational experiments against `src/jumpmodel.py` itself. Verdict: the characterization is
> exact as algebra, but the informative exact description is Bemporad et al. (2018) Prop. 1 —
> **joint MAP of a constrained Gaussian HMM with the switching prior frozen at
> `lambda = 2 sigma^2 log((1-q)/q)`, fit by classification EM** — which is what predicts the
> failure modes (no consistency theorem exists; lambda is scale- and dimension-relative; the
> solution path skips switch counts, demonstrated analytically at a T=5 breakpoint of exactly
> 0.9). Two measured surprises: at the MAP-calibrated lambda the hard-assignment separation bias
> (+78% at k-means) nearly vanishes and the fit matches an oracle Viterbi; and under strongly
> autocorrelated noise the lambda-accuracy curve flattens rather than shifting — the i.i.d.
> lambda-to-prior mapping simply stops meaning anything, which is the honest reading of
> production lambda = 50 (implied i.i.d. switch probability 1.4e-11/day) on EWM-smoothed
> features. The adversarial sweep independently rediscovered D5 (the factor-2 lambda convention),
> D7 (the package's undocumented 3-sigma winsorization) and D1's selection critique — a
> convergence that corroborates the findings doc rather than extending it. No model change is
> proposed: the surfaced repairs address defects that do not bear on path-level comparison, and
> no live question needs them. The preregistration and findings doc are untouched.

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
> **The sequence.** S0 found one surviving functional and [[closed-research/return-states/DECISION-Q1-CLAIM]] then showed by
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
> full result in [[closed-research/return-states/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]].

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

## The pre-closure record

Everything this file carried below the status log — the governing frame, the mandate's target, the
open questions, the known defects, and the full experiment write-ups from 2026-08-12 to 2026-08-18 —
was moved verbatim to [[closed-research/HUB-RECORD]] on 2026-08-27. It is the working record of the
closed programmes and stands as written there.

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
