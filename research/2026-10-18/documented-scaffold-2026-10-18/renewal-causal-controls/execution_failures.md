# Access and execution history

No failed source route is overwritten by the later successful RSC main acquisition.

| Attempt | Observed result | Subsequent state |
|---|---|---|
| Web reader, original RSC HTML route | HTTP403 | Normal Chrome later displayed full public article |
| Direct migrated RSC main PDF | HTTP403,5542 bytes | Body retained; not a valid acquired PDF |
| Direct RSC SI | HTTP403,5548 bytes | Body retained; SI unacquired |
| Direct eScholarship Stevens main | HTTP403,919 bytes | Body retained; no native main acquired locally |
| Direct CNR Cimino main | HTTP403,5743 bytes | Body retained; no native main acquired locally |
| Initial Chrome state check after navigation | CDP snapshot observation timeout | Screenshot and fresh state showed completed publisher navigation; timeout was not treated as terminal access failure |
| Browser PDF download helper |30s tool timeout and kernel reset | Re-inventory showed a live native PDF page; no successful local file return was claimed |
| Browser page rebind | Chrome reported automation blocked by another extension UI | No extension setting changed; no user-control bypass; SI browsing left uncompleted |
| Browser-observed public CDN main request | HTTP200,1,069,448 bytes | Separately saved native PDF and receipt; original403 bodies unchanged |
| Cimino primary reader | A child agent transiently received parsed primary PDF text; later same-URL and same-reference requests returned403 | Native bytes not saved; methods/control reading retained as an unacquired lead, not an integrity-verified source |

The source-unit discrepancy is a scientific source limit, not a tool extraction success that resolves the correct unit. Both native readings are retained; no corrected response was selected. There was no numerical chemical model or empirical holdout in this iteration.
