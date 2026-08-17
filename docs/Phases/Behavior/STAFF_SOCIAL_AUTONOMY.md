# Staff Social Autonomy

GotoTalk chooses one random staff ID. It requires a non-self target, compatible flags, a sitting target in STATE_WORK, and a usable standing/use cell. It sets reserved/invited talk flags, colleague IDs, STATE_MOVE, and MOVE_MODE_TO_STAFF. InviteStaffToTalk can select an installed pass-chip talk goal and notifies the colleague. Talk emits timing events at frames 20, 70, and 110 and completes at frame 130 or later by clearing flags and returning toward the desk.

The selected StaffData records 0-4 point to JobData 4 and SkillData 1. Skill 1 is `Loving Meetings`, type 10, effect index 8 value 150, passive flag 1. OnEndTyping reads that effect through the selected skill path; the random gauge distribution is not promoted.

Full meeting process-step dispatch, queue/fairness, and exact invite cadence remain source-limited.
