# Integrated finite-resource compartment, version 1.1

Frozen local protocol before official execution, 15 October 2026. This is an engineered, dimensionless agent construction, not a molecular simulation or an origin-of-life result. The seed interval is new to this study; independence from every historical repository RNG stream has not been exhaustively proven. The source/config hashes in the run receipt identify the actual executed version.

## Question and interfaces

Can one supplied compartment maintain itself, acquire a changing cue/resource relation, and pass functional state through at least three actual resource-funded partitions? Maintenance uses `maintenance.model` without duplicating its resource rules. Division uses `heredity.lab.partition_counts` on two integer carrier populations. This integrates mechanisms previously examined separately. It tests a candidate architecture's requirements, not whether those mechanisms exist in compatible chemistry.

The inherited variable is a learned compositional state. It is not a nucleotide sequence, organism, new species or proof of Darwinian evolution. No population selection or autonomous origin is modeled. No parameter is calibrated from the online dataset. Arbitrary work units cannot be converted into ATP, joules, molar concentrations or hours.

## State and supplied mechanisms

Finite activated substrate produces structure and a work store with explicitly assigned yields. Structure decays into retained waste; energy leaks into a dissipation ledger. All sensing, action, state switching and division charge the shared work store. Resource is consumed from a finite external stock. No-feed and no-renewal are causal controls.

Integer carriers are labeled portions of structure, with count equal to its floor; its fractional remainder has no carrier label. Their two types encode the two possible cue/action mappings. The surviving carrier count is fixed by actual surviving structure, and its identities are sampled without replacement. Only the count added by actual structural renewal receives labels sampled from the previous composition with a 1% copying error. This is a supplied templating law, not measured functional heredity. Structural founder/new labels are tracked separately from the inherited functional labels.

Cues are balanced only in expectation (fair independent bits). The environmental mapping alternates every 96 episodes from a random initial bit. The controller receives the cue, then experiences a delay before choosing between two resource sites. A supplied two-state memory analogue retains the cue with probability exp(-0.08 * delay); failed retrieval returns a random bit. This is a phenomenological relaxation channel, not simulated chemistry. The delay is varied without changing the episode's maintenance interval, isolating information retention rather than total elapsed physical time; it is not a prediction of survival after a longer physical interval.

The majority carrier type predicts the mapping. After an action, the only learning signal is the observed amount of obtained resource, compared with the known low-yield ceiling. Feedback is unavailable when no resource is obtained or the remaining stock could cap a high yield. Given the remembered cue, a supplied local feedback rule converts up to one quarter of incorrect carrier labels, limited by affordable switching work. It has no access to hidden correctness or mapping. Feed magnitude jitter is identical across paired arms; the mapping, true cue and future reward are unavailable to the policy. The oracle sees the target and is explicitly a privileged upper reference.

At structure >=80, division costs one work unit and conservatively partitions actual carrier counts. The model follows one daughter; the sister's structure, fuel, energy and waste are retained in an external discarded-branch ledger. Every extensive maintenance ledger is allocated by the daughter fraction, which preserves balances but does not simulate spatial cell division. The tracked daughter inherits carrier composition and continues learning. Offspring-shuffle randomizes carrier labels with paid switching work while preserving total structure; this intervention breaks mapping identity rather than implementing a physically known randomizing reagent.

## Comparators and fixed histories

Ten arms, 12 seeds and three scenarios produce 360 trajectories. All histories are generated before the arm loop. Adaptive, erased-cue, no-update, no-renewal, no-feed and irrelevant-erasure arms share available structural/learning mechanisms except their named intervention. Irrelevant erasure resets an unused scratch variable and consumes no additional work; exact equality is expected and is only a software negative control. Reactive chooses directly from the current cue before delay; random chooses a pre-generated random action; neither learns and each avoids the memory sensing cost. Oracle sees the true target, avoids memory cost, and is an upper reference, not a fair baseline. Cost differences are reported.

After death, missed episodes count as wrong in horizon-based accuracy. Alive-only accuracy is also retained so mortality cannot silently select favorable trials. Evaluation excludes the first 32 episodes of each 96-episode phase, declared before execution. All episodes, including adaptation windows, consume resources and appear in raw trajectories.

## Predeclared evaluation

Primary conditional integration passes only if **every seed** has adaptive survival through the horizon, >=3 descendant partitions, final founder fraction <=0.05, and evaluation accuracy at least 0.10 above both reactive and random. Causal delayed-memory contribution requires adaptive accuracy at least 0.10 above erased-cue for every seed. Irrelevant erasure must reproduce the adaptive outcome exactly. No-feed/no-renewal outcomes and the offspring-shuffle difference are reported independently; no learning or inheritance advantage is inferred from positive means alone. Three scenarios are reported separately; no success is selected from them after execution.

Record per-seed margins, means and paired bootstrap intervals (2,000 resamples, seed 2026101599). Intervals describe variability over these simulated histories, not uncertainty about physical chemistry. Any failure remains a failure of this construction/criterion. Model pass does not pass physical gates G0-G6.

## Verification and stop

Before campaign: test finite resource accounting, delay-memory endpoints, conservative copying/partition, no privileged policy inputs and paid switching; test invalid configurations. After campaign: fresh-process replay must match raw and summary hashes. Never overwrite an existing output directory. No outcome-driven parameter search or rescue version is planned. Store any implementation correction separately from scientific outcomes.
