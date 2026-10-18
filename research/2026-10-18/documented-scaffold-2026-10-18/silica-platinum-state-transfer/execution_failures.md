# Execution record

The first native verifier run failed one authored sheet-name assertion: it expected `Fig3h` after whitespace removal, while the workbook actually names the sheet `Figure 3h`. Ten other source checks passed. The assertion was corrected to the exact observed sheet name, retaining the source identity requirement. This was an implementation error, not a failed physical result or a changed scientific acceptance criterion. No source payload or numerical outcome was altered. The rerun is recorded in `checks.md` and `sources/verification.json`.

The independent scout encountered an identity-authorization redirect on the Nature main page and a browser check on the PMC reader. These are scout observations without persistent response bodies. Root used the openly responding EuropePMC XML and supplementary archive endpoints; both native requests returned HTTP200 and have byte/hash receipts. No purchase, author contact or access-control bypass occurred.
