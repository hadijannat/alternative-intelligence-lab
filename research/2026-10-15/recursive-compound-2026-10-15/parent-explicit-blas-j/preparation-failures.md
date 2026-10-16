# Preserved preparation failure

First mock-only test invocation used the aligned Python and `test_run.py` without --record. Six tests ran: one passed, one failed, four errored. The writer resolved output paths but compared them to an unresolved temporary-directory BASE on macOS (/var versus /private/var); all affected errors were `ValueError: Output outside diagnostic`. No native parent work ran. Corrected the writer to compare with BASE.resolve(); subsequent full suite rerun is captured in qualification.json. This was a preparation path-normalization failure, not a chemistry result.
