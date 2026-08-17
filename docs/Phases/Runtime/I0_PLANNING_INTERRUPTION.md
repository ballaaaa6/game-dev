# I0 Planning and Interruption Cleanup

Planning is an original command boundary: Player → Room → Staff for start, update, and end. The implementation stores planning flags on canonical Staff state and does not create a dashboard task queue or product policy.

Equipment, talk, door, and desk interruptions clear their reservations and target relations at the source-backed cleanup boundary. Destroyed desks clear owner and Staff desk references; destroyed equipment releases reservations; colleague IDs and talk flags are bilateral and are cleared together.
