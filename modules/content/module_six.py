"""Module 6, Incident Response: two deep lessons built as a tabletop exercise.

The most narratively ambitious module on the platform. Professional teams train
incident response through tabletop exercises: a structured, escalating scenario
worked stage by stage, with realistic stakes at every step. Module 6 is built
around exactly that, using the new TABLETOP activity and its live "situation
board". One continuing incident, a ransomware attack on a Geelong dental
practice, runs as the spine across both lessons: detect and contain in Lesson 1,
eradicate, recover and review (including the legal duty) in Lesson 2. The board,
tracking systems, patient data, the clock and notification, moves toward green on
sound calls and into the red on poor ones, but the exercise always continues and
teaches.

  Lesson 1  When the alert fires: detect and contain
  Lesson 2  Clean up, come back, and the law: eradicate, recover, review

Voice: warm, plain Australian English, no em-dashes, no emoji. Each lesson is
four interactive activities plus one picture-question CHECK (task 3); points sum
to 10 per lesson. The quiz is exactly ten, split five and five across the two
lessons, every question tracing to the lesson that teaches it. The Privacy Act
1988 and its Notifiable Data Breaches scheme are described as general information.
"""

# The six-phase incident response lifecycle, as one plain-English scenario runs
# through it. Preparation happens in the calm before; the other five phases are
# the tabletop itself.

LESSONS = [
    {
        "title": "When the alert fires: detect and contain",
        "reading_time_minutes": 9,
        "intro": "It is a Monday morning at a busy dental practice, and the files "
        "will not open. This lesson runs the first, most important hours of a real "
        "incident as a tabletop exercise: notice it, understand it, and stop it "
        "spreading, all without making it worse.",
        "tasks": [
            {
                "key": "tt-detect-contain",
                "kind": "tabletop",
                "points": 2,
                "title": "Tabletop: the Monday the files stopped opening",
                "hero": "incident-escalation",
                "body": "<p>This is a <strong>tabletop exercise</strong>: a real "
                "incident, worked one decision at a time, the way professional teams "
                "rehearse. Watch the two timelines above first. The same attack, "
                "handled two ways: left alone it climbs to a disaster; caught early "
                "and contained, it stays a scare. Your job in the first hours is to "
                "keep it on the second line. Watch the situation board change as you "
                "decide.</p>"
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
                "inline_check": {
                    "question": "In a ransomware incident, why is it a mistake to power a machine off at the wall the moment you see it?",
                    "hint": "Think about what investigators and your recovery will need afterwards.",
                    "options": [
                        ("It can destroy useful evidence, and isolating the machine from the network is a better way to stop the spread", True,
                         "Right. Disconnecting from the network halts the spread while preserving what happened, which a blind power-off can wipe."),
                        ("Powering off damages the computer's hardware", False,
                         "No. The concern is not hardware. A sudden power-off can destroy evidence, and network isolation is the better containment move."),
                        ("It is never a mistake; always pull the power first", False,
                         "No. A blind shutdown can lose evidence and may not stop it. Isolate from the network instead."),
                        ("Because the machine will then update automatically", False,
                         "No. That is unrelated. The real issue is lost evidence, and that isolation is the better way to contain it."),
                    ],
                },
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
                "key": "lifecycle-map",
                "kind": "check",
                "points": 2,
                "title": "Read the response lifecycle",
                "diagram": "ir-lifecycle",
                "body": "<p>Incident response is not improvised. It follows a known "
                "shape, the same one every professional team uses, shown in the "
                "diagram above: prepare in the calm, then identify, contain, "
                "eradicate, recover, and finally learn. Read it, then answer. The "
                "order is not decoration; each phase depends on the one before.</p>"
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
                "key": "who-to-call",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: who to tell, and when",
                "body": "<p>An incident is not only a technical event; it is a "
                "communication test. Tell the right people early and calmly and the "
                "response holds together. Tell the wrong people, or the world, too "
                "soon and you create panic and legal problems. Work through the "
                "calls.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> escalate "
                "internally and to your support first, keep a clear record, and do "
                "not go public until you understand the incident and your "
                "obligations.</div>",
                "payload": {
                    "prompt": "The incident is contained. Make each call about who to tell.",
                    "start": "internal",
                    "nodes": {
                        "internal": {
                            "text": "It is mid-morning and the incident is contained. Who should you make sure knows, right now?",
                            "choices": [
                                {"label": "The practice owner or manager, and your IT support, following the plan", "outcome": "good",
                                 "feedback": "Right. The people who can make decisions and fix the problem need to know first, calmly and clearly.", "to": "record"},
                                {"label": "No one yet; try to fix it all quietly before anyone finds out", "outcome": "bad",
                                 "feedback": "Handling it alone and in secret is how small incidents become disasters. The people who can help cannot help if they do not know.", "to": "secret_bad"},
                                {"label": "Everyone, by posting the details in the practice's public reviews and social media", "outcome": "bad",
                                 "feedback": "Announcing an incident you do not yet fully understand causes panic and can breach your obligations. Escalate internally first.", "to": "public_bad"},
                            ],
                        },
                        "secret_bad": {
                            "text": "Working alone, you miss things only IT support would catch, and the owner is blindsided later. Secrecy slows the response and erodes trust. Escalate to the right people straight away.",
                            "choices": [],
                        },
                        "public_bad": {
                            "text": "The public post, made before you understood the incident, spreads alarm and gets details wrong, and it may breach the careful process the law expects. Understand it, then communicate properly.",
                            "choices": [],
                        },
                        "record": {
                            "text": "The right people know and are helping. A patient rings, having heard a rumour, and asks if their records are safe. What do you do?",
                            "choices": [
                                {"label": "Be honest and measured: say you are aware of an issue, are dealing with it, and will update them properly once you know more", "outcome": "good",
                                 "feedback": "Exactly. Calm honesty keeps trust. You do not overshare or speculate, but you do not deny or dismiss either.", "to": "win"},
                                {"label": "Tell them everything is completely fine and nothing happened", "outcome": "bad",
                                 "feedback": "Flatly denying it is a lie you may have to retract, and if their data was affected you have a duty to tell them properly. Be honest and measured.", "to": "deny_bad"},
                            ],
                        },
                        "deny_bad": {
                            "text": "The denial unravels when the breach is confirmed and patients must be notified after all. Now they were misled as well as affected. Honest, measured communication protects trust; denial destroys it.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Escalated to the right people, kept a clear record, and answered the patient with calm honesty. That steady, truthful handling of the people side is as much a part of incident response as the technical fix.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
    {
        "title": "Clean up, come back, and the law: eradicate, recover, review",
        "reading_time_minutes": 9,
        "intro": "The spread is stopped, but the incident is far from over. This "
        "lesson finishes the job: remove the attack for good, come back cleanly "
        "from backups, and face the part many businesses forget, the legal duty to "
        "tell people when their personal information has been breached.",
        "tasks": [
            {
                "key": "tt-eradicate-review",
                "kind": "tabletop",
                "points": 2,
                "title": "Tabletop: cleaning up and coming back",
                "hero": "recovery-board",
                "body": "<p>The same incident, continued. The spread is contained; "
                "now comes the careful part. Watch the recovery board above: systems "
                "come back one at a time, from down, to restoring, to online, never "
                "all at once in a scramble. Work the final phases: remove the attack "
                "for good, recover cleanly, and meet your obligations. The board is "
                "waiting on your calls.</p>"
                "<div class=\"cy-callout\"><strong>Coming back is deliberate.</strong> "
                "Eradicate the cause, close the hole, restore from clean backups, "
                "and then face the law honestly.</div>",
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
            {
                "key": "notifiable-or-not",
                "kind": "classify",
                "points": 2,
                "title": "Does this one have to be notified?",
                "body": "<p>Under the Privacy Act 1988, the "
                "<strong>Notifiable Data Breaches</strong> scheme says that when "
                "personal information is lost or exposed in a way likely to cause "
                "serious harm, you must tell both the regulator (the OAIC) and the "
                "people affected. Not every mishap meets that bar, but many do, "
                "especially anything involving sensitive data like health or "
                "identity details. Read each case and decide.</p>"
                "<div class=\"cy-callout\">Ask two questions: is personal "
                "information involved, and is serious harm to those people likely? If "
                "both point to yes, it is very likely notifiable.</div>",
                "inline_check": {
                    "question": "Under the Notifiable Data Breaches scheme, who must be told about an eligible breach?",
                    "hint": "Think about both the regulator and the people whose data it is.",
                    "options": [
                        ("Both the OAIC (the regulator) and the individuals whose information was affected", True,
                         "Right. An eligible breach must be reported to the OAIC and notified to the affected people, so they can protect themselves."),
                        ("Only the business's own manager, kept internal", False,
                         "No. Keeping it internal is exactly what the scheme prevents. Both the OAIC and the affected individuals must be told."),
                        ("Only the police", False,
                         "No. The scheme is about notifying the OAIC and the affected people. The police are a separate matter."),
                        ("No one; notification is optional", False,
                         "No. For an eligible breach, notification is a legal duty, not a choice."),
                    ],
                },
                "payload": {
                    "prompt": "Read each case and tap whether it is very likely notifiable, or can be handled internally. Sort all six to finish.",
                    "categories": [
                        {"id": "notify", "label": "Very likely notifiable"},
                        {"id": "internal", "label": "Handle internally"},
                    ],
                    "events": [
                        {"text": "Patient health records, with names and dates of birth, exposed in a ransomware attack.",
                         "category": "notify",
                         "why": "Very likely notifiable. Health information is sensitive, and its exposure is likely to cause serious harm, so the OAIC and patients must be told."},
                        {"text": "A staff member briefly saw a colleague's leave request on a shared screen.",
                         "category": "internal",
                         "why": "Handle internally. A minor internal glimpse of low-risk information is not likely to cause serious harm, so it does not meet the bar."},
                        {"text": "A spreadsheet of customers' names, addresses and payment details emailed to the wrong company.",
                         "category": "notify",
                         "why": "Very likely notifiable. Identity and payment details in the wrong hands can cause serious harm, so this must be assessed and almost certainly notified."},
                        {"text": "An internal newsletter about a public event sent to the wrong internal list.",
                         "category": "internal",
                         "why": "Handle internally. Public, non-personal information going to the wrong colleagues is not a notifiable breach."},
                        {"text": "A laptop full of unencrypted client files stolen from a car.",
                         "category": "notify",
                         "why": "Very likely notifiable. Personal client information lost with no encryption protecting it is likely to cause serious harm, so it must be assessed and notified."},
                        {"text": "A typo in a public blog post about office opening hours.",
                         "category": "internal",
                         "why": "Handle internally. No personal information is involved and no one is harmed, so it is simply a correction to make."},
                    ],
                },
            },
            {
                "key": "breach-notify-map",
                "kind": "check",
                "points": 2,
                "title": "Read the notification duty",
                "diagram": "breach-notify",
                "body": "<p>Here is the legal duty as a simple picture: when a breach "
                "is likely to cause serious harm, the path leads to notifying both "
                "the regulator and the people affected. Read the diagram above, then "
                "answer. This is not just paperwork; prompt, honest notification is "
                "what lets affected people protect themselves.</p>"
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
                "key": "eradicate-recover",
                "kind": "sort",
                "points": 2,
                "title": "Eradication, or recovery?",
                "body": "<p>The two phases after containment are easy to blur, but "
                "they are different jobs. <strong>Eradication</strong> is removing "
                "the attack and closing the way in. <strong>Recovery</strong> is "
                "getting the business running again, safely. Do them in the wrong "
                "order and you restore straight onto a machine that is still "
                "compromised. Sort each action into the phase it belongs to.</p>"
                "<div class=\"cy-callout\">Tap an action, then tap whether it is "
                "Eradication (remove and close) or Recovery (restore and resume). "
                "Sort all six to finish.</div>",
                "payload": {
                    "prompt": "Sort each action into Eradication or Recovery.",
                    "buckets": [
                        {"id": "eradicate", "label": "Eradication"},
                        {"id": "recover", "label": "Recovery"},
                    ],
                    "items": [
                        {"text": "Wipe and rebuild the infected machines from clean sources", "bucket": "eradicate",
                         "why": "Eradication. Removing the malware entirely is how you make sure it is gone for good."},
                        {"text": "Restore the files from a clean, verified backup", "bucket": "recover",
                         "why": "Recovery. Bringing data and systems back from clean backups is the heart of recovery."},
                        {"text": "Close the unpatched remote login the attack came through", "bucket": "eradicate",
                         "why": "Eradication. Shutting the way in is part of removing the threat, so it cannot simply return."},
                        {"text": "Bring systems back online one at a time and check each works", "bucket": "recover",
                         "why": "Recovery. A careful, staged return to normal is exactly what recovery means."},
                        {"text": "Reset the passwords that may have been exposed", "bucket": "eradicate",
                         "why": "Eradication. Changing credentials the attacker may hold closes another door they came through."},
                        {"text": "Confirm the booking system is working before staff rely on it", "bucket": "recover",
                         "why": "Recovery. Verifying that restored systems actually work is the final part of coming back safely."},
                    ],
                },
            },
            {
                "key": "lessons-learned",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: getting stronger from it",
                "body": "<p>The last phase is the one most often skipped, and the "
                "most valuable. Once the crisis is over, a calm review turns a bad "
                "day into a stronger practice: what happened, what worked, and what "
                "to change so it is harder next time. Work through the review.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> review "
                "honestly and without blame, then actually change the things that "
                "let it happen. A lesson noted but not acted on is not a lesson "
                "learned.</div>",
                "payload": {
                    "prompt": "The incident is closed. Make each call about the review.",
                    "start": "review",
                    "nodes": {
                        "review": {
                            "text": "A week later, the practice is back to normal. What is the right way to close the incident out?",
                            "choices": [
                                {"label": "Hold a calm, blame-free review of what happened and what to change", "outcome": "good",
                                 "feedback": "Right. An honest review, focused on the process rather than punishing people, is how a business genuinely gets stronger.", "to": "change"},
                                {"label": "Move on quickly and never speak of it again", "outcome": "bad",
                                 "feedback": "Skipping the review wastes the hardest lesson you will ever get. The same hole stays open for next time.", "to": "skip_bad"},
                                {"label": "Find one person to blame and leave it there", "outcome": "bad",
                                 "feedback": "Blame makes people hide mistakes, so you learn less and the real weaknesses go unfixed. Review the process, not the person.", "to": "blame_bad"},
                            ],
                        },
                        "skip_bad": {
                            "text": "Because nothing was reviewed, the unpatched remote login and the shaky backup habits stay exactly as they were. The next incident finds the same open doors. The review is where the value is.",
                            "choices": [],
                        },
                        "blame_bad": {
                            "text": "With one person blamed, everyone else learns to stay quiet about mistakes, and the real process gaps are never surfaced. A blame-free review would have found and fixed them.",
                            "choices": [],
                        },
                        "change": {
                            "text": "The review lists clear fixes: close remote logins, test the backups, add staff training. What turns this into a lesson actually learned?",
                            "choices": [
                                {"label": "Assign each fix to someone, with a date, and check they are done", "outcome": "good",
                                 "feedback": "Exactly. A lesson is only learned when the changes are made. Owners and dates are what turn a list into real improvement.", "to": "win"},
                                {"label": "Write the list up neatly and file it away", "outcome": "bad",
                                 "feedback": "A filed list changes nothing. If no one owns the fixes and no one checks them, the weaknesses are still there.", "to": "file_bad"},
                            ],
                        },
                        "file_bad": {
                            "text": "The tidy report sits in a folder while the same weaknesses remain live. Documenting a fix is not making it. Give each change an owner and a date, and follow it through.",
                            "choices": [],
                        },
                        "win": {
                            "text": "A calm review, honest and blame-free, turned into real fixes with owners and dates, each one checked off. That is the final phase working as intended: the practice came out of a bad week genuinely harder to hit. That is incident response, start to finish.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: detect and contain ----
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
        # ---- Lesson 2: eradicate, recover, review, and the law ----
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
