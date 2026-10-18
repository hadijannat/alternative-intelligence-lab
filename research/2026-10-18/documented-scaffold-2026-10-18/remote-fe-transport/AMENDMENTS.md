# Extraction metadata and conservative handling

After the frozen protocol and before root received current-response results, the extraction worker reported clock coverage and candidate row counts. These facts are retained explicitly; they do not justify changing the split or choosing a more favorable prediction.

- All three candidate retention blocks have only two training observations at cycles<=40 and six later observations. The protocol requires at least three training points, so no candidate model is fitted. Do not move the cutoff or introduce an exception.
- The AEM and CEM CA traces end at299.83333 and299.91667min, respectively. A strict screen requiring full support through300min is left null. Observed samples inside the unchanged295–300min window may be summarized descriptively, with counts, actual first/last times and support flags. Those descriptions do not become a complete held-out endpoint test.
- SC has a final native row at300min after preceding data extend beyond301min. Preserve the original row/cell provenance. Sorting for coordinate operations must not erase that appended record or manufacture another specimen.

No missing point is filled, no endpoint is shifted, no model is retuned and no empirical pass is claimed from the strict null screen. The paired refreshed-single-cell CV assay and the synthetic mechanism comparison remain executable under their original rules. Root's clarification used clock metadata, not the current amplitudes; all analysis remains retrospective and source-informed.
