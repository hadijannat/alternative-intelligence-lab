# Independent review of completed blocked C-PCM qualification

Reviewer: cpcm_memory_design, read-only. Verdict: CLEAR for PASS_IMPLEMENTATION_EQUIVALENCE_ONLY. No new SCF or parent calculation was executed by this review.

The reviewer checked both hash manifests and recomputed saved NPZ comparisons across three cases, three densities and block sizes1,7,8. Surface matrices agree exactly. Maximum q difference1.494e-15, AO potential7.217e-16, solvent energy2.776e-16Eh and normalized backward error5.297e-17. Separate solves of the reference transpose equations on initial densities agree with the averaged charge within1.442e-15. The261 main checks, three receipts and native convergence records support exactly three reference SCFs, each under90seconds. Frozen thresholds were retained.

Same surface generation, symmetric S, q_sym=-f*S^-1*v, half-charge-potential energy and negative AO contraction were verified. Cache/reset and unsupported interfaces were covered. Keep settings fixed after build; changing cavity/geometry requires reset/build. Setting frozen=True after attachment could bypass the internal guard through upstream get_veff; the qualified drivers never do this. This is a scoped interface limitation.

Parent S plus factor totals1,379,082,496bytes, AO8 tensor602,407,936bytes and the old AO400 tensor30,120,396,800bytes. Nuclear block128 is196*128*8=200,704bytes. These do not certify total RSS, runtime or conditioning. The unchanged10GiB/900second/20cycle parent controls remain required. This review admits no physical function, molecular identity, gradient or parent accuracy claim.
