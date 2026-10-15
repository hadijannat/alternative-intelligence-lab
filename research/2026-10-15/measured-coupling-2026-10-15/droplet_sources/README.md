# Measured droplet source package

Start with [SOURCE_AUDIT.md](SOURCE_AUDIT.md). It identifies the same nominal Figure 1 formulation for C3 production and compartment turbidity, and the limits of the retention/inheritance evidence.

Use `tables/observations.csv` or the untouched `author/` CSVs. Filter `condition_id=single_Cys_PSS` for the matched Figure 1 observations, then select `measurement=concentration` (C3, mM) or `measurement=turbidity` (OD650). Their samples are not paired. `conditions.json` records reported chemistry and source inconsistencies. `source_models.json` transcribes source equations and existing fit outputs without selecting new rates.

Reproduce:

```sh
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 acquire_sources.py
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 acquire_article_text.py
pdftotext -layout supplement.pdf supplement.txt
/USER_HOME/.pyenv/versions/3.12.3/bin/python3 normalize_sources.py
```

Acquisition downloads only public primary sources. The author data are commit-pinned; the publisher PDFs are SHA256-recorded. No downloaded code is executed. The combined 31.7 MB article/SI PDF is parsed in memory; local retained source data stay below 30 MB. `pypdf` is the only non-standard-library requirement of the article-text extractor and is already installed in the stated Python runtime.

Unknown active retention and daughter inheritance must remain explicit simulator parameters, not measured constants inferred from FRAP or substrate partitioning.
