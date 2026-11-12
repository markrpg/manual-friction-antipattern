# Worked example: small-repo

The calibration run. Use it to check you cut steps and events the same way. Scorecard: [small-repo.json](small-repo.json).

**Journey:** launch → add a new folder → first task running, in Qwobolt (an agent workbench) installed build `ef594d8`, with Claude Code already signed in. The steps were reconstructed from the run notes, so the step count may be off by one or two; every event is recorded.

**Necessary steps (4):** open folder; choose the folder; write the task; start it, approving folder access.

**Steps taken (about 16):**

| # | Step | Test | Event |
|---|---|---|---|
| — | First attempt with a folder inside the Qwobolt project fails with generic provider troubleshooting | friction | Way forward |
| 1 | Search | friction | Search (Open folder is missing from All projects) |
| 2 | Projects | friction | |
| 3 | Open folder | necessary | |
| 4 | Cmd+Shift+G does nothing in the picker | friction | Attention (broken shortcut) |
| 5 | Drag the folder in from Finder | necessary | (this is "choose the folder") |
| 6 | Continue project, which does nothing | friction | Progress (restart to open a new project) |
| 7 | Quit Qwobolt | friction | |
| 8 | Reopen Qwobolt | friction | |
| 9 | Open small-repo | friction | (repeat of the step before the restart) |
| 10 | Composer sends them to Settings | friction | Place (detour) |
| 11 | Providers | friction | |
| 12 | Check connection | friction | Attention (manual check) |
| 13 | Use in this project | friction | Search (provider asked again inside the account's reach) |
| 14 | Close Settings, back to the composer | friction | (part of the detour) |
| 15 | Write the task | necessary | |
| 16 | Start, approving access | necessary | |

**Score:**

| Event | Loss | Weight |
|---|---|---|
| Nested folder: generic error pointing at the provider | Way forward | 10 |
| Restart to open the new project | Progress | 8 |
| Detour from the composer to Settings | Place | 5 |
| Open folder only through Search → Projects | Search | 3 |
| Signed-in provider set up again for this project | Search | 3 |
| Check connection needed before models show | Attention | 2 |
| Cmd+Shift+G missing in the picker | Attention | 2 |
| **Total** (band: broken) | | **33** |

Friction ratio about 4.0 against a budget of 1.5; score 33 against a budget of 5. Five fixes cover 31 of the 33 points: a specific overlap error (10), opening without a restart (8), reusing the signed-in provider (detour 5 plus asked again 3), Open folder on All projects (3), and Go to Folder in the picker (2). The remaining 2 is Check connection.

Only 5 of the 33 points were visible on a screen (hidden Open folder 3, Check connection 2). The other 28 showed only in behaviour, which is why the installed-app walk decides whether a change passes.
