"""Module 6, Incident Response: understand it, then apply it.

The most narratively ambitious module. Lesson 1 TEACHES the whole discipline:
what incident response is and why the first hours decide everything, the
six-phase lifecycle, how to detect and contain without making it worse, and how
you clean up, recover, and meet the legal duty when personal information is
breached. Lesson 2 APPLIES it through the signature TABLETOP exercises, run on a
live "situation board", following one continuing incident (a ransomware attack on
a Geelong dental practice) from detect and contain through eradicate, recover, and
review.

  Lesson 1  UNDERSTAND IT  — four teaching panels, each with a real visual (two
            of them animated heroes), plus one comprehension check on the order of
            the phases.
  Lesson 2  APPLY IT       — two staged TABLETOP exercises with a live board,
            plus a first-move CLASSIFY, a picture CHECK, and ordering the phases.

Voice: warm, plain Australian English, no em-dashes, no emoji. The Privacy Act
1988 and its Notifiable Data Breaches scheme (OAIC) are described as general
information, grounded in cyber.gov.au and OAIC guidance. Points sum to 10 per
lesson and bank at lesson end.
"""

LESSONS = [
    {
        "title": "The shape of a response: detect, contain, recover, and the law",
        "reading_time_minutes": 10,
        "intro": "When something goes wrong, panic is optional but a plan is not. "
        "This lesson gives you the whole shape of a professional response: why the "
        "first hours matter most, the six phases every team follows, how to contain "
        "trouble without destroying what you need, and the legal duty that follows "
        "a breach of personal information.",
        "tasks": [
            {
                "key": "first-hours",
                "kind": "concept",
                "points": 2,
                "title": "Incident response, and why the first hours decide everything",
                "hero": "incident-escalation",
                "body": "<p><strong>Incident response</strong> is the calm, "
                "rehearsed way a team handles a security incident: not improvising in "
                "a panic, but following a plan from the moment something is noticed "
                "to the lessons drawn afterwards. You do not need to be technical to "
                "play your part; you need to know the shape of it.</p>"
                "<p>Watch the two timelines above. It is the same attack, handled two "
                "ways. Left alone, treated as a glitch, the impact climbs to a "
                "disaster. Caught early and contained, it stays a scare. The "
                "difference is almost entirely about the first hours: how fast "
                "someone names it as an incident and starts the plan.</p>"
                "<p>This is not a rare event to prepare for once and forget. The "
                "Australian Signals Directorate received <strong>over 84,700 "
                "cybercrime reports in 2024-25, about one every six minutes</strong>, "
                "and the average incident cost a small business <strong>$56,600</strong>. "
                "For a business that size, how the first hour is handled often decides "
                "whether that number is the whole story or just the beginning.</p>"
                "<p>That is why <strong>preparation</strong>, done in the calm before, "
                "matters so much: a written plan, known contacts, and tested backups "
                "mean that when the alert fires, everyone knows their first move "
                "instead of freezing.</p>"
                "<div class=\"cy-callout\">Time is the one thing you cannot get back "
                "in an incident. Naming it early and starting the plan is what keeps "
                "a scare from becoming a disaster.</div>",
            },
            {
                "key": "the-lifecycle",
                "kind": "concept",
                "points": 2,
                "title": "The six phases, and why the order matters",
                "diagram": "ir-lifecycle",
                "body": "<p>Every professional response follows the same shape, shown "
                "above. It is worth knowing by name, because each phase depends on "
                "the one before it.</p>"
                "<ul>"
                "<li><strong>Preparation</strong>: have a plan, backups and contacts "
                "ready, in the calm before anything happens.</li>"
                "<li><strong>Identification</strong>: notice and confirm that this is "
                "a real security incident, not a glitch.</li>"
                "<li><strong>Containment</strong>: stop the spread, so the trouble "
                "cannot reach more systems.</li>"
                "<li><strong>Eradication</strong>: remove the cause and close the way "
                "it got in.</li>"
                "<li><strong>Recovery</strong>: restore from clean backups and return "
                "to normal, safely.</li>"
                "<li><strong>Lessons Learned</strong>: review what happened and get "
                "stronger, so next time is easier.</li>"
                "</ul>"
                "<p>The order is not decoration. You cannot recover cleanly until you "
                "have eradicated the cause, and you cannot eradicate until you have "
                "contained the spread. Skip ahead, and the attack simply reaches the "
                "machines you have just cleaned or restored.</p>"
                "<div class=\"cy-callout\">Contain, then eradicate, then recover. Do "
                "them out of order and the work undoes itself.</div>",
            },
            {
                "key": "detect-contain",
                "kind": "concept",
                "points": 2,
                "title": "Detect and contain, without making it worse",
                "diagram": "ransom-screen",
                "body": "<p>The first hours are where good instincts matter most, and "
                "where the wrong instinct does the damage. Picture the screen above "
                "on a Monday morning: files that will not open, and a demand for "
                "payment. Here is how a level head handles it.</p>"
                "<ul>"
                "<li><strong>Name it fast.</strong> Treat it as a security incident "
                "straight away, rather than clicking and rebooting as though it were "
                "a glitch. Every minute of doubt is a minute it keeps spreading.</li>"
                "<li><strong>Isolate, do not yank the power.</strong> Disconnect the "
                "affected machines from the network to stop the spread, but avoid a "
                "blind power-off at the wall, which can destroy useful evidence and "
                "may not stop it anyway.</li>"
                "<li><strong>Protect the backups.</strong> Keep your clean backups "
                "well clear of infected machines. Plugging a backup drive into an "
                "infected computer can encrypt the backup too, destroying your way "
                "back.</li>"
                "<li><strong>Write it down, and tell the right people.</strong> A "
                "simple timeline of what you saw and when is invaluable later, and "
                "the people who can help (the owner, your IT support) cannot help if "
                "they do not know.</li>"
                "</ul>"
                "<div class=\"cy-callout\">The calm, by-the-plan move is almost "
                "always right. Speed without a plan, rebooting, wiping, paying, is "
                "what causes the damage.</div>",
            },
            {
                "key": "recover-and-law",
                "kind": "concept",
                "points": 2,
                "title": "Coming back, and the law that follows",
                "hero": "recovery-board",
                "body": "<p>Once the spread is stopped, the incident is far from "
                "over. <strong>Eradication</strong> means removing the attack for "
                "good, wiping and rebuilding affected machines, and closing the way "
                "in (an unpatched remote login, an exposed service). "
                "<strong>Recovery</strong> means coming back deliberately: restoring "
                "from clean, verified backups and bringing systems online one at a "
                "time, as the board above shows, never all at once in a scramble.</p>"
                "<p>Then comes the part many businesses forget. If the incident "
                "exposed personal information, the <strong>Notifiable Data Breaches "
                "scheme</strong>, under the Privacy Act 1988, may require you to act, "
                "and it runs on a clock. Once you have grounds to suspect an eligible "
                "breach, you must <strong>assess it within 30 days</strong>, and if a "
                "breach of personal information is likely to cause <strong>serious "
                "harm</strong>, you must notify both the regulator (the "
                "<strong>OAIC</strong>) and the affected people as soon as "
                "practicable. This is common and rising: the OAIC recorded "
                "<strong>1,113 data breaches across 2024, a record</strong>, with the "
                "<strong>health sector the most affected</strong>. Anything involving "
                "sensitive data, like health or identity details, is very likely to "
                "meet the serious-harm bar. Telling people promptly is not just the "
                "law; it is what lets them protect themselves, by changing passwords "
                "or watching their accounts, before the harm lands.</p>"
                "<p>Finally, the <strong>Lessons Learned</strong> review: a calm, "
                "blame-free look at what happened and what to change, with each fix "
                "given an owner and a date. A lesson noted but not acted on is not "
                "learned.</p>"
                "<div class=\"cy-callout\">Eradicate the cause, recover from clean "
                "backups, notify honestly if personal data was breached, then fix "
                "what let it happen.</div>",
            },
            {
                "key": "order-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check: why contain before you clean up?",
                "diagram": "ir-lifecycle",
                "body": "<p>One quick check to finish. The lifecycle above runs "
                "prepare, identify, contain, eradicate, recover, learn. You just saw "
                "why that order is not up for grabs. Put the key reason into your own "
                "words.</p>"
                "<div class=\"cy-callout\">You cannot recover cleanly until you have "
                "eradicated the cause, and you cannot eradicate until you have "
                "contained the spread.</div>",
                "question": "Looking at the lifecycle above, why must containment come before eradication and recovery?",
                "hint": "Think about what happens if the trouble is still spreading while you clean up.",
                "options": [
                    ("If you have not stopped the spread first, cleaning up and restoring just gets undone as it keeps moving", True,
                     "Right. Containment stops the bleeding. Trying to eradicate or recover while the attack is still spreading means it reaches the machines you have just cleaned or restored."),
                    ("The order does not really matter; you can do them in any sequence", False,
                     "No. The order is the point. Each phase depends on the one before, which is why containment comes before eradication and recovery."),
                    ("Recovery is the first thing you should ever do", False,
                     "No. Recovering while the cause is still active just reinfects what you restore. You contain, then eradicate, then recover."),
                    ("Eradication means paying the ransom", False,
                     "No. Eradication means removing the malware and closing the way it got in. It has nothing to do with paying."),
                ],
            },
        ],
    },
    {
        "title": "Work the incident: a tabletop from alert to review",
        "reading_time_minutes": 10,
        "intro": "Now run it for real. Riverside Dental in Geelong has been hit by "
        "ransomware. Work the incident as a tabletop exercise, one decision at a "
        "time, and watch the situation board respond: detect and contain first, "
        "then eradicate, recover, and face the law.",
        "tasks": [
            {
                "key": "tt-detect-contain",
                "kind": "tabletop",
                "points": 2,
                "title": "Tabletop: the Monday the files stopped opening",
                "hero": "incident-escalation",
                "body": "<p>This is a <strong>tabletop exercise</strong>: a real "
                "incident, worked one decision at a time, the way professional teams "
                "rehearse. Everything Lesson 1 taught about the first hours applies "
                "here. Make each call and watch the situation board change, tracking "
                "systems, patient data, the clock, and your response.</p>"
                "<div class=\"cy-callout\"><strong>The first hours decide "
                "everything.</strong> Name it, understand it, and contain it, in "
                "that order, without destroying what you will need later.</div>",
                "payload": {
                    "prompt": "Work the incident one decision at a time. Watch the board respond.",
                    "scenario": "Riverside Dental, Geelong. Six staff, no in-house IT. 8:05am Monday: the receptionist cannot open any files, and a message on screen is demanding payment to unlock them.",
                    "board": [
                        {"id": "systems", "label": "Systems", "state": "warn", "value": "Acting up"},
                        {"id": "data", "label": "Patient data", "state": "ok", "value": "Intact?"},
                        {"id": "clock", "label": "Clock", "state": "ok", "value": "8:05 am"},
                        {"id": "notify", "label": "Response", "state": "ok", "value": "Not started"},
                    ],
                    "stages": [
                        {
                            "phase": "Detect",
                            "title": "Is this an incident?",
                            "prompt": "None of the files will open, and a message is demanding payment to unlock them. What is your first move?",
                            "options": [
                                {"label": "Treat it as a security incident straight away: stop using the machines and start the response plan", "outcome": "good",
                                 "consequence": "Naming it early is the whole game. The plan kicks in, the right people are called, and the clock is still on your side.",
                                 "board": {"systems": {"state": "bad", "value": "Ransomware"}, "clock": {"state": "warn", "value": "8:15 am"}, "notify": {"state": "warn", "value": "Plan running"}}},
                                {"label": "Assume it is a computer glitch and keep clicking and rebooting to fix it", "outcome": "bad",
                                 "consequence": "Treating an attack as a glitch costs the one thing you cannot get back: time. While you reboot, it keeps encrypting more files.",
                                 "board": {"systems": {"state": "bad", "value": "Spreading"}, "data": {"state": "warn", "value": "At risk"}, "clock": {"state": "warn", "value": "9:10 am"}}},
                                {"label": "Pull every machine's power at the wall immediately, noting nothing", "outcome": "bad",
                                 "consequence": "A blind shutdown can wipe useful evidence and may not stop it anyway. Isolating machines from the network is better than yanking the power.",
                                 "board": {"systems": {"state": "bad", "value": "Dark"}, "data": {"state": "warn", "value": "Unknown"}}},
                            ],
                        },
                        {
                            "phase": "Assess",
                            "title": "How bad is it?",
                            "prompt": "The plan is running and help is on the way. Before touching anything else, what do you need to know?",
                            "options": [
                                {"label": "Which machines are affected, and whether patient records are among them", "outcome": "good",
                                 "consequence": "Knowing the scope, especially whether patient data is caught up in it, shapes every decision that follows, including the legal ones later.",
                                 "board": {"data": {"state": "warn", "value": "Scoping"}}},
                                {"label": "Nothing; just pay the ransom now so the practice can open", "outcome": "bad",
                                 "consequence": "Paying is a gamble with no guarantee you get the files back, it funds the next attack, and it skips the questions the law will later ask. Understand the scope first.",
                                 "board": {"notify": {"state": "warn", "value": "Paid?"}, "clock": {"state": "warn", "value": "Rushed"}}},
                                {"label": "Announce on the practice's social media that you have been hacked", "outcome": "bad",
                                 "consequence": "Going public before you understand the incident, or your obligations, spreads panic and can breach the very rules you must follow. Assess privately first.",
                                 "board": {"notify": {"state": "bad", "value": "Public"}}},
                            ],
                        },
                        {
                            "phase": "Contain",
                            "title": "Stop the spread",
                            "prompt": "You have found it on three machines, including the one holding patient records. How do you stop it spreading further?",
                            "options": [
                                {"label": "Disconnect the affected machines from the network, and check the backups are safe and untouched", "outcome": "good",
                                 "consequence": "Isolating the affected machines stops the spread, and protecting the backups protects your way back. This is containment done right.",
                                 "board": {"systems": {"state": "warn", "value": "Contained"}, "data": {"state": "warn", "value": "Backups safe"}}},
                                {"label": "Leave everything connected and hope the antivirus catches up", "outcome": "bad",
                                 "consequence": "While it stays on the network it keeps reaching new machines, and your backups. Hope is not containment. Disconnect the affected machines.",
                                 "board": {"systems": {"state": "bad", "value": "Spreading"}, "data": {"state": "bad", "value": "Encrypting"}}},
                                {"label": "Plug a backup drive into the infected machine to grab the files quickly", "outcome": "bad",
                                 "consequence": "Connecting your clean backup to an infected machine can encrypt the backup too, destroying your safety net. Keep backups well clear until it is clean.",
                                 "board": {"data": {"state": "bad", "value": "Backup hit"}}},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "sound-or-worse",
                "kind": "classify",
                "points": 2,
                "title": "Sound first move, or making it worse?",
                "body": "<p>In the first minutes of an incident, instinct often "
                "points the wrong way. The urge to fix it quietly, to try one more "
                "reboot, to make it disappear, is exactly what lets it spread or "
                "destroys the evidence you will need. Read each first reaction and "
                "decide: is it a sound move, or one that makes things worse?</p>"
                "<div class=\"cy-callout\">The calm, boring, by-the-plan move is "
                "almost always the right one. Speed without a plan is what causes "
                "the damage.</div>",
                "payload": {
                    "prompt": "Read each first reaction to an incident and tap whether it is a sound move or makes it worse. Sort all six to finish.",
                    "categories": [
                        {"id": "sound", "label": "Sound first move"},
                        {"id": "worse", "label": "Makes it worse"},
                    ],
                    "events": [
                        {"text": "Start the incident response plan and call the people it names.",
                         "category": "sound",
                         "why": "Sound. The plan exists for this moment. Following it is how a scare stays a scare."},
                        {"text": "Keep working on the affected computer to finish the morning's bookings.",
                         "category": "worse",
                         "why": "Makes it worse. Every minute it stays in use, the attack spreads further and does more damage."},
                        {"text": "Disconnect the affected machine from the network.",
                         "category": "sound",
                         "why": "Sound. Isolating it stops the spread while keeping the evidence intact, unlike a blind shutdown."},
                        {"text": "Delete the ransom message and pretend it did not happen.",
                         "category": "worse",
                         "why": "Makes it worse. Hiding it removes evidence and delays the real response, while the attack carries on underneath."},
                        {"text": "Write down what you saw and when, as the incident unfolds.",
                         "category": "sound",
                         "why": "Sound. A simple timeline is invaluable later, for recovery, for the review, and for any notification you must make."},
                        {"text": "Pay the ransom straight away to make it stop.",
                         "category": "worse",
                         "why": "Makes it worse. Paying is no guarantee, funds more attacks, and skips the assessment the law will later require."},
                    ],
                },
            },
            {
                "key": "breach-notify-map",
                "kind": "check",
                "points": 2,
                "title": "Read the notification duty",
                "diagram": "breach-notify",
                "body": "<p>A picture-question, straight from Lesson 1. Here is the "
                "legal duty as a simple picture: when a breach is likely to cause "
                "serious harm, the path leads to notifying both the regulator and the "
                "people affected. Read the diagram, then answer. This is not just "
                "paperwork; prompt, honest notification is what lets affected people "
                "protect themselves.</p>"
                "<div class=\"cy-callout\">The whole point of notifying is to give "
                "people the chance to act, change a password, watch their accounts, "
                "before the harm lands.</div>",
                "question": "Looking at the notification path above, why does the law require you to tell the affected people, not just the regulator?",
                "hint": "Think about what those people can do once they know.",
                "options": [
                    ("So they can protect themselves in time, by changing passwords, watching their accounts, or being alert to fraud", True,
                     "Right. Telling people promptly is what gives them the chance to act before the harm reaches them. That is the human purpose behind the rule."),
                    ("Only so the business avoids a fine, with no benefit to anyone else", False,
                     "No. Avoiding penalties is a side effect. The real reason is to let affected people protect themselves in time."),
                    ("So the affected people can pay the ransom on the business's behalf", False,
                     "No. Notification has nothing to do with paying a ransom. It is about warning people so they can protect themselves."),
                    ("Because the affected people caused the breach", False,
                     "No. Notifying is not about blame. It is about giving people the information they need to guard against harm."),
                ],
            },
            {
                "key": "order-the-phases",
                "kind": "sequence",
                "points": 2,
                "title": "Put the lifecycle in order",
                "body": "<p>Prove you have the shape of it. Below are the phases of "
                "incident response, shuffled. Put them back into the order a real "
                "response follows, from the calm preparation before, through to the "
                "lessons learned after. Getting the order right is getting the whole "
                "discipline right.</p>"
                "<div class=\"cy-callout\">Tap the phases in order, starting with "
                "what you do before anything ever goes wrong.</div>",
                "payload": {
                    "prompt": "Tap the six phases in the order a real incident response follows.",
                    "steps": [
                        {"label": "Preparation", "detail": "Have a plan, backups and contacts ready, in the calm before anything happens.", "order": 1},
                        {"label": "Identification", "detail": "Notice and confirm that this is a real security incident.", "order": 2},
                        {"label": "Containment", "detail": "Stop the spread, so the trouble cannot reach more systems.", "order": 3},
                        {"label": "Eradication", "detail": "Remove the cause and close the way it got in.", "order": 4},
                        {"label": "Recovery", "detail": "Restore from clean backups and return to normal, safely.", "order": 5},
                        {"label": "Lessons Learned", "detail": "Review what happened and get stronger, so next time is easier.", "order": 6},
                    ],
                },
            },
            {
                "key": "tt-eradicate-review",
                "kind": "tabletop",
                "points": 2,
                "title": "Tabletop: cleaning up, coming back, and the law",
                "hero": "recovery-board",
                "body": "<p>The same incident, continued. The spread is contained; now "
                "comes the careful part. Watch the recovery board above: systems come "
                "back one at a time, from down, to restoring, to online, never all at "
                "once in a scramble. Work the final phases: remove the attack for "
                "good, recover cleanly, and meet your obligations under the law.</p>"
                "<div class=\"cy-callout\"><strong>Coming back is deliberate.</strong> "
                "Eradicate the cause, close the hole, restore from clean backups, and "
                "then face the law honestly.</div>",
                "payload": {
                    "prompt": "Finish the incident. Work the last three phases and watch the board.",
                    "scenario": "Riverside Dental, later the same week. The attack is contained, the affected machines are isolated, and the backups are safe. The way in has been traced to one office computer with a remote-login left open and unpatched.",
                    "board": [
                        {"id": "systems", "label": "Systems", "state": "warn", "value": "Contained"},
                        {"id": "data", "label": "Patient data", "state": "warn", "value": "Backups safe"},
                        {"id": "clock", "label": "Clock", "state": "warn", "value": "Day 1"},
                        {"id": "notify", "label": "The law", "state": "ok", "value": "To assess"},
                    ],
                    "stages": [
                        {
                            "phase": "Eradicate",
                            "title": "Remove it for good",
                            "prompt": "The spread is stopped. How do you make sure the attack is truly gone from the affected machines?",
                            "options": [
                                {"label": "Wipe and rebuild the affected machines from clean sources, and reset the passwords that may have been exposed", "outcome": "good",
                                 "consequence": "A full wipe and rebuild is the only way to be sure it is gone, and resetting exposed passwords closes the door it came through.",
                                 "board": {"systems": {"state": "warn", "value": "Rebuilding"}}},
                                {"label": "Just delete the ransom note and the one obvious bad file, then carry on", "outcome": "bad",
                                 "consequence": "Malware hides far more than the one file you can see. Deleting the note leaves the rest behind, and it comes straight back.",
                                 "board": {"systems": {"state": "bad", "value": "Reinfected"}}},
                                {"label": "Skip working out how it got in; it does not matter now that it is contained", "outcome": "bad",
                                 "consequence": "If you leave the unpatched remote login open, it will simply be used again. Eradication has to include closing the entry point.",
                                 "board": {"systems": {"state": "bad", "value": "Hole open"}}},
                            ],
                        },
                        {
                            "phase": "Recover",
                            "title": "Come back cleanly",
                            "prompt": "The machines are clean and the entry point is closed. How do you get the practice running again?",
                            "options": [
                                {"label": "Restore from the clean backups, verify each system, and bring them back one at a time", "outcome": "good",
                                 "consequence": "Careful, verified recovery from clean backups is how you come back without dragging the problem back with you.",
                                 "board": {"systems": {"state": "ok", "value": "Online"}, "data": {"state": "ok", "value": "Restored"}, "clock": {"state": "warn", "value": "Day 3"}}},
                                {"label": "Rush everything back online at once to open on time, without checking", "outcome": "bad",
                                 "consequence": "Rushing risks restoring infected files or missing a still-open hole, and you end up back where you started. Recovery is deliberate, not a scramble.",
                                 "board": {"systems": {"state": "bad", "value": "Unstable"}}},
                                {"label": "Reopen using the encrypted files and hope they still work", "outcome": "bad",
                                 "consequence": "The encrypted files are locked, that is the whole attack. Recovery means restoring from clean backups, not trying to use the damaged data.",
                                 "board": {"data": {"state": "bad", "value": "Still locked"}}},
                            ],
                        },
                        {
                            "phase": "Review and the law",
                            "title": "Face it honestly",
                            "prompt": "The practice is back. Patient records, names, dates of birth and health details, were on an affected machine. What now?",
                            "options": [
                                {"label": "Assess it under the Notifiable Data Breaches scheme, and if serious harm is likely, notify the OAIC and the affected patients", "outcome": "good",
                                 "consequence": "Health information is sensitive, so a breach like this is very likely notifiable. Telling the regulator and the affected people is both the law and the decent thing.",
                                 "board": {"notify": {"state": "ok", "value": "Notified"}, "clock": {"state": "ok", "value": "Handled"}}},
                                {"label": "Say nothing and hope no one ever finds out", "outcome": "bad",
                                 "consequence": "Hiding an eligible breach of health data breaks the law under the Privacy Act, and the harm to patients, and to trust, is far worse when it comes out later.",
                                 "board": {"notify": {"state": "bad", "value": "Hidden"}}},
                                {"label": "Delete the logs so there is no record of what happened", "outcome": "bad",
                                 "consequence": "Destroying the evidence is the worst move of all: it obstructs the response, breaches your obligations, and leaves you unable to learn what went wrong.",
                                 "board": {"notify": {"state": "bad", "value": "Cover-up"}}},
                            ],
                        },
                    ],
                },
            },
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: understand it (the whole response) ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is incident response?",
            "options": [
                ("A planned, step-by-step way of handling a security incident, from noticing it to learning from it", True,
                 "Yes. It is the calm, rehearsed process teams follow so a security incident is handled well instead of in a panic."),
                ("A type of antivirus software", False,
                 "No. It is not a product. It is the process a team follows when something goes wrong."),
                ("Paying a ransom as quickly as possible", False,
                 "No. Paying is not a plan, and it is discouraged. Incident response is the structured way of handling the whole event."),
                ("A yearly security newsletter", False,
                 "No. It is the process for responding when an incident actually happens, not a newsletter."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "You see a ransom message and files that will not open. What is the best first move?",
            "options": [
                ("Treat it as a security incident and start the response plan straight away", True,
                 "Yes. Naming it early and starting the plan is what keeps a scare from becoming a disaster. Time is everything in the first hours."),
                ("Keep clicking and rebooting to try to fix the glitch", False,
                 "No. Treating an attack as a glitch wastes the most valuable thing you have, time, while it keeps spreading."),
                ("Pay the ransom immediately", False,
                 "No. Paying is a gamble that funds more attacks and skips the assessment you need to do. Start the plan instead."),
                ("Post about it on social media", False,
                 "No. Going public before you understand it causes panic and can breach your obligations. Start the response plan first."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What does 'containment' mean in an incident?",
            "options": [
                ("Stopping the trouble spreading further, for example by disconnecting affected machines from the network", True,
                 "Yes. Containment is stopping the bleeding, so the attack cannot reach more systems while you deal with it."),
                ("Deleting all the affected files at once", False,
                 "No. That is not containment, and it can destroy what you need. Containment stops the spread, often by isolating machines."),
                ("Paying to make the attack stop", False,
                 "No. Paying is not containment. Containment is halting the spread, such as by disconnecting affected machines."),
                ("Turning the whole business off for a week", False,
                 "No. Containment is targeted, isolating what is affected, not shutting everything down indefinitely."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why is it usually better to disconnect an infected machine from the network than to yank its power out?",
            "options": [
                ("Disconnecting stops the spread while preserving evidence that a sudden power-off can destroy", True,
                 "Yes. Network isolation halts the spread and keeps the useful evidence intact, which a blind shutdown can wipe."),
                ("Because power-offs damage the screen", False,
                 "No. The concern is not the hardware. It is that a sudden power-off can lose evidence you will need."),
                ("Because a disconnected machine runs faster", False,
                 "No. Speed is not the point. Disconnecting contains the spread and preserves evidence."),
                ("There is no difference between the two", False,
                 "No. There is a real difference. Disconnecting preserves evidence and stops the spread; a blind power-off can lose evidence."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "In the six-phase lifecycle, why does containment come before eradication and recovery?",
            "options": [
                ("Because cleaning up or restoring while the attack is still spreading just gets undone", True,
                 "Yes. If you have not stopped the spread, the attack reaches the machines you have just cleaned or restored. Contain first."),
                ("Because eradication is not really necessary", False,
                 "No. Eradication is essential. Containment simply has to come first so the cleanup is not undone."),
                ("Because recovery is always the very first step", False,
                 "No. Recovering first, while the cause is active, just reinfects what you restore. You contain, then eradicate, then recover."),
                ("The phases can be done in any order", False,
                 "No. The order matters. Each phase depends on the one before, starting with containing the spread."),
            ],
        },
        # ---- Lesson 2: apply it (eradicate, recover, review, and the law) ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What does 'eradication' involve after an incident?",
            "options": [
                ("Removing the attack completely and closing the way it got in, such as wiping machines and patching the hole", True,
                 "Yes. Eradication is making sure it is truly gone and that the entry point is shut, so it cannot simply return."),
                ("Restoring the files from backup", False,
                 "No. That is recovery. Eradication comes first: remove the threat and close the entry point."),
                ("Telling the affected customers", False,
                 "No. That is part of the review and notification. Eradication is removing the attack and closing the hole."),
                ("Deleting only the ransom message you can see", False,
                 "No. Malware hides more than the visible file. Eradication means a thorough removal and closing the way in."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is the safe way to recover after the attack has been removed?",
            "options": [
                ("Restore from clean, verified backups and bring systems back one at a time", True,
                 "Yes. Deliberate, verified recovery from clean backups is how you return to normal without dragging the problem back."),
                ("Rush everything back online at once to save time", False,
                 "No. Rushing risks restoring infected files or missing an open hole, and you end up back where you started."),
                ("Keep using the encrypted files and hope they work", False,
                 "No. The encrypted files are locked by the attack. Recovery means restoring from clean backups, not using the damaged data."),
                ("Skip backups and rebuild everything by hand from memory", False,
                 "No. Clean backups are exactly what recovery relies on. That is why keeping good, tested backups matters so much."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Under the Notifiable Data Breaches scheme, when personal information is breached in a way likely to cause serious harm, who must be told?",
            "options": [
                ("Both the regulator (the OAIC) and the people whose information was affected", True,
                 "Yes. An eligible breach must be reported to the OAIC and notified to the affected individuals so they can protect themselves."),
                ("Only the business's own staff", False,
                 "No. Keeping it internal is what the scheme prevents. Both the OAIC and the affected people must be told."),
                ("Only the business's bank", False,
                 "No. The duty is to notify the OAIC and the affected individuals, not the bank."),
                ("No one, as long as it is fixed quickly", False,
                 "No. Fixing it does not remove the duty. An eligible breach must be notified to the OAIC and those affected."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why does the law require telling the affected people, not just the regulator?",
            "options": [
                ("So they can protect themselves in time, such as changing passwords or watching their accounts", True,
                 "Yes. Prompt, honest notification gives people the chance to act before the harm reaches them. That is its human purpose."),
                ("So the affected people can pay any fines", False,
                 "No. Notification is not about passing on penalties. It is about warning people so they can protect themselves."),
                ("So the business looks good in the media", False,
                 "No. It is not a public-relations exercise. It is to give affected people a real chance to guard against harm."),
                ("Because the affected people must fix the breach themselves", False,
                 "No. They are not responsible for the fix. They are told so they can protect themselves from the fallout."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What makes the final 'lessons learned' phase actually worthwhile?",
            "options": [
                ("Turning the review into specific fixes, each with an owner and a date, and checking they are done", True,
                 "Yes. A lesson is only learned when the changes are made. Owners, dates and follow-up are what turn a review into real improvement."),
                ("Writing a neat report and filing it away", False,
                 "No. A filed report changes nothing. The weaknesses stay open unless the fixes are actually made and checked."),
                ("Finding one person to blame for the incident", False,
                 "No. Blame makes people hide mistakes and hides the real gaps. Review the process, not the person."),
                ("Never mentioning the incident again", False,
                 "No. Skipping the review wastes the hardest lesson you will get, and leaves the same doors open."),
            ],
        },
    ],
}
