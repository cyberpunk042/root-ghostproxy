---
description: Switch statusline to "full-aidlc-narrow" tier — 3-line planning variant for narrow terminals (~90 chars; drops session/thinking/vim/weekly/sescost)
---

# /statusline-full-aidlc-narrow

Activate the `full-aidlc-narrow` profile (t4-narrow planning variant for narrow terminals ~90 chars). Use case: planning mode on narrow terminal — full AIDLC visibility without overflow.

Drops vs full-aidlc: L1-model (redundant with L2-model) · L1-stage (SFIF carries phase) · L2-session-name · L2-thinking · L2-vim · L3-weeklyusage · L3-sescost.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh full-aidlc-narrow
```

Briefly confirm the new active profile to the operator.
