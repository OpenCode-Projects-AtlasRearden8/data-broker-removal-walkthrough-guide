# Renewal Calendar: Reminders That Keep You Off

*The dirty secret of broker removal: it decays. New public records, sloppy
matching, and fresh list purchases can re-add you in 6–18 months. The fix is a
tiny recurring routine, not a heroic one.*

## The schedule that works

| When | What to do | Time |
|---|---|---|
| **+1 month** | Verify your first-round confirmations landed. Spot-check the 3 biggest sites (search your name + city, incognito) | 15 min |
| **+3 months** | Full re-search pass (Step 1 of `03-walkthrough.md`). Re-request anything new | 45–60 min |
| **+6 months** | Same pass again | 45–60 min |
| **+12 months** | Same pass + new-broker sweep (their ranks shift; new sites launch) | 60–90 min |
| **Every year after** | One pass per year, ideally the same month each year (birthday month is a memorable pick) | 60 min |

## Building the reminders (choose your tool)

### Plain calendar (Google/Outlook/Apple) — the honest default

Create 4 yearly-repeating events named *e.g.* "NY — broker re-check." Suggested
titles so you don't miss context:

- `Broker re-check: search name+city, re-request stragglers (45 min)`
- `Broker 1-year sweep: new brokers + confirm old removals (75 min)`

Set each to repeat at 3 / 6 / 12 months from your initial pass date, then annually.

### ICS snippet (import into any calendar app)

Save the below as `broker-recheck.ics` and open/import it:

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Asdale Dynamics//Broker Re-check Reminders//EN
BEGIN:VEVENT
UID:broker-recheck-3mo@asdale.local
DTSTAMP:20260101T120000Z
DTSTART;VALUE=DATE:20260115
DURATION:PT1H
RRULE:FREQ=MONTHLY;INTERVAL=3;COUNT=4
SUMMARY:Broker re-check (search name+city, re-request stragglers)
DESCRIPTION:Re-run docs/03 Walkthrough Step 1. Update tracking sheet.
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:Broker re-check tomorrow
END:VALARM
END:VEVENT
BEGIN:VEVENT
UID:broker-recheck-annual@asdale.local
DTSTAMP:20260101T120000Z
DTSTART;VALUE=DATE:20270115
DURATION:PT90M
RRULE:FREQ=YEARLY;COUNT=5
SUMMARY:Broker annual sweep (new brokers + verify old removals)
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:Broker annual sweep tomorrow
END:VALARM
END:VEVENT
END:VCALENDAR
```

*Adjust the `DTSTART` dates to a real date a few weeks after you start your first
pass (the sample above is a placeholder; edit before importing).*

### Rules that make renewals painless

1. **Use your project email.** Every confirmation lands in one folder; the annual
   sweep is "search, compare to folder, act on anything new."
2. **Keep the tracker forever.** A dated `2026-06-14 spokeo confirmed` line is the
   fastest way to see whether a site re-listed you.
3. **Two passes, not one.** send-request → click-confirm → *verify 2 weeks later*.
4. **Pair it with another yearly chore** (freeze-thaw? tax records? password
   audit) so it rides the same "once a year admin day" you may already have.

## Triggers that mean "do a pass early"

- You get a spam call/snail mail **quoting details from a listing**
- You move, change your name, register a business, or renew a license
- A public record about you exists (even a boring one — permits, notary renewals)
- Your name appeared in any news article, obit (family), or public docket
- You notice a listing under a **relatives' names** you didn't remove (they will
  pull you back in via "associated persons") — hand them this guide

## Habit anchor (ADHD-friendly version)

Do the whole annual sweep in **one 60-minute block with a timer**, music on, in
the same chair, same drink, same playlist. The sameness is the point: repetition
needs fewer decisions than cleverness does. The `site/` checklist page can be
kept open in a browser tab all year and re-checked at each pass.
