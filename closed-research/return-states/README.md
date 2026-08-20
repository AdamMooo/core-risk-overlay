# CLOSED — the return-state programme

**Terminated 2026-08-19 as INDETERMINATE.** Preserved for provenance and replication. **Not an active
branch, not a backlog, and not a source of next experiments.**

**No market data was ever touched by this programme.** It ran two synthetic identification gates and
stopped at a structural obstruction. That is the whole of its history.

---

## The question it asked

> Are there empirically distinguishable states in which the distribution of future equity returns is
> sufficiently different from the ordinary state that the statistical character of the risk being held
> has materially changed?

Formally, whether the conditional law `F_{s,h} = law of R_{t:t+h} given S_t = s` differs across a
partition `{s}` — against a **stated null** (`N1`, a continuous smoothly-reverting conditional-scale
process) and on a functional and horizon declared in advance. The programme terminated at its first
question, **(A) existence**, and never reached characterisation, transition or identification.

## What it established

### R1 — T3's separation was reducible to variance-process dispersion

**S0 (2026-08-18)** matched the unconditional variance and the whole squared-return ACF between a
two-state switching process and a Gaussian-innovation GARCH(1,1), and found one surviving functional:
`T3`, the dispersion of log realized variance over 21-day blocks, `d'` up to 10.22.

**The survivor carried no information about discreteness.** For any `r = sigma z` with `z ~ iid N(0,1)`
and `E[sigma^2] = 1`, kurtosis `K = 3 E[sigma^4]`, so

```
    Var(sigma^2) = K/3 - 1        exactly, for both classes
```

S0's matching fixed the variance process's autocorrelation **in shape but not in scale**, and the
scale is `Var(sigma^2)` — which *is* the residual kurtosis mismatch S0 declared. T3 measures that
dispersion. So the surviving functional and the declared mismatch were two estimators of one quantity,
and T3 won on efficiency rather than on content.

**S0 also eliminated two candidates, and those eliminations stand:**

- **Aggregate kurtosis at `h > 1`**: max `d' = 1.59` against a mismatch floor reaching 6.80. Below its
  own floor in every cell.
- **Path geometry** (max drawdown, CDaR): `d' = 0.15` and `0.14`; mean max drawdown **0.645 against
  0.647**; **6.1 excursions past 10% per simulated 33-year history.** Measured where the states exist
  *by construction*, which makes it a foreclosure no market measurement could have delivered.

### R2 — the observable cannot isolate the latent shape dimension under this design

**S0b (2026-08-19)** closed the free parameter. A four-parameter GARCH-t null matched unconditional
variance, the squared-return ACF at every lag **and** `Var(sigma^2)`, leaving only the *shape* of the
variance distribution free — two mass points against a continuum. All 18 cells feasible; all three
constraints exact to `3.4e-14`.

**The control failed.** `T3` was in the functional list precisely so a broken match would announce
itself, with the preregistered instruction that a non-zero `d'` there means the matching is broken
rather than that a difference was found. **Max `d'` on T3: 7.416**, against a threshold of 2.

**(M3) was holding.** What failed was the control's premise, and the reason is structural:

```
    RV_B = SUM sigma2_t z2_t
```

The observed block-variance distribution depends on **both** the latent `sigma^2` distribution **and**
the distribution of `z^2`. S0b used `E[z^4]` as the instrument for matching `Var(sigma^2)` — so **the
mechanism that removes the latent dispersion difference simultaneously changes the observation noise
in RV.** And `sd(log RV)` was never a function of `Var(sigma^2)` alone, since the variance of a log
depends on the whole distribution of the level.

The obstruction is monotone and visible in the run: at `kappa = 2.0`, where `Var(sigma^2) = 0.096` and
the required innovation kurtosis reaches 9.91, T3's `d'` is **7.42**; at `kappa = 6.5, pi2 = 0.15`,
where `Var(sigma^2) = 1.158`, it is **0.02**. The control fails exactly where the instrument bites
hardest.

> **R2. The T3 failure is not evidence that the models differ in variance-process dispersion after
> matching. It tells us that the proposed observable cannot cleanly isolate the latent shape dimension
> under this design.**

**Therefore the remaining functionals cannot be interpreted as tests of discreteness**, and none of
them is promoted to evidence.

## The observed but uninterpretable pattern, preserved as such

`T7` — Sarle's bimodality coefficient of log block variance — produced large separations (up to
`d' = 11.74`) and was the only column that satisfied the preregistered `lambda`-direction prediction
cleanly at `B = 63` (5 rises, 0 falls) while also strengthening with aggregation in most cells. **That
is what a genuine shape signal was predicted to look like.**

**It is not evidence and is not promoted.** The control voided the run, and the pattern may equally be
an artifact of the noise channel R2 identifies. It is recorded so that it is neither lost nor promoted,
and it is **not** a reason to reopen anything.

## Why it terminated rather than being repaired

The natural repair is a null whose variance dispersion is a free parameter *of the variance process*
rather than of the innovation law — a lognormal stochastic-volatility null with Gaussian innovations
would leave the RV estimation noise matched. **That is a different null family, introduced after
seeing the obstruction**, and S0b's own header declared it the final synthetic gate.

> **A stochastic-volatility null may be scientifically interesting, but it is a new identification
> programme, not a repair to this committed experiment.** It is recorded in `../../PARKED.md` on those
> terms.

**No S0c is authorised. No Q1 was ever licensed.**

## Contents

| file | what it established |
|---|---|
| `s0_discriminating_functional.py` | **S0** — the four-functional identification study, and **R1** |
| `s0b_discreteness_gate.py` | **S0b** — the discreteness gate, and **R2**. VOID by its own control |
| `checks.py` | 140 checks: the matching algebra of both gates, Sarle's coefficient against its exact known values, and the (M3) constraint asserted to 1e-10 |
| `data_loader.py`, `pathfunctionals.py` | frozen copies — see below |

Preregistrations, unaltered: `../../docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE.md`,
`../../docs/STUB-S0B-DISCRETENESS-GATE.md`. Identification analysis:
`../../docs/IDENTIFICATION-UNDER-N1.md`. Why Q1 was never licensed:
`../../docs/DECISION-Q1-CLAIM.md`. The charter: `../../CHARTER.md`.

## Reproducing

```
.venv\Scripts\python.exe closed-research/return-states/s0_discriminating_functional.py
.venv\Scripts\python.exe closed-research/return-states/s0b_discreteness_gate.py
.venv\Scripts\python.exe closed-research/return-states/checks.py
```

Neither script reads market data. S0b was verified to reproduce after the archive move on 2026-08-19
— control `d' = 7.416`, unchanged.

## The frozen copies, deliberately

`data_loader.py` and `pathfunctionals.py` are duplicated here rather than imported from `../../src/`,
on the same precedent as the other two archives: importing across the boundary would let a later
change silently alter an archived result. **Nothing in this directory imports from outside it.**
