# Preserved execution and access limits

These failures predate the final local checkpoint. Successful later checks do not erase them.

| Action | Observed failure | Resolution or remaining limit |
|---|---|---|
| `python3 tools/verify_october18.py` in the original publication checkout | Assertion at `actual == expected`: extra untracked duplicate files, no missing expected file reported | Unrelated files preserved; verify a fresh exact remote clone |
| Six-test exporter suite in that checkout | 1 failure in `test_complete_saved_snapshot_and_tampering`, same extra-file assertion | Same six tests pass in the clean remote clone; the original checkout is not declared clean |
| Worktree under `publication/` | `fatal: mmap failed: Operation canceled`, during checkout at 1/3694 files | Failed attempt preserved in this log; not reported as a completed worktree |
| Worktree outside the research workspace | Same fatal mmap cancellation, during checkout at 3/3694 files | Fresh HTTPS clone succeeded instead |
| Wei normal Chrome access | Redirect to abstract-only route, no-access message and purchase offer | No purchase, login change or bypass; native main remains unacquired |
| Direct Nature web-reader request for Ou | Redirect to publisher identity route unavailable to that reader | Legitimate author-hosted main PDF and publisher SI acquired successfully; direct-reader failure remains a different observation |
| Ag40 source readers | PMC challenge; ACS/Europe PMC reader failures, SI not acquired | Bounded indexed-primary screen only; missing serial-founder evidence remains unverified |

The goal already existed when a create request was attempted. The goal tool rejected a duplicate unfinished goal; `get_goal` confirmed the active goal. No second goal or false completion was created.

The editorial skill's referenced `ANTI_AI_PROSE_STYLE.md` was not present at its installed path or in the scoped skill-directory search. The explicit specificity, evidence, overclaiming, uncertainty and diff-size checklist in the loaded skill was applied directly.

No chemical model was executed in this iteration, so no model failure is hidden by a later fit. Offline synthetic acquisition-failure tests are deliberate tests, not successful primary-source acquisitions.
