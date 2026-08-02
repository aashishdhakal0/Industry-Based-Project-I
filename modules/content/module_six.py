"""Module 6, Incident Response: the six-phase lifecycle (Preparation,
Identification, Containment, Eradication, Recovery, Lessons Learned), the legal
duty to notify a data breach under the Privacy Act 1988, and a branching
ransomware morning that puts the whole response together.

Same shape and standard as Modules 1 to 5 (see docs/module-authoring.md): a
lesson is a scrollable room of collapsible task PANELS. Each panel is a full,
deep task: several teaching paragraphs (what it is, a concrete Australian
example, why it matters, what to do), a diagram where it helps, a callout box
with a specific scenario, sometimes a mid-panel check, then the end interactive.
Points sum to 10 per lesson and bank at lesson end.

Voice: warm, confident, human. Plain Australian English. No em-dashes, no filler,
no repetition. The Privacy Act material is general information, not legal advice,
and is framed that way in the content.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "Why a plan beats panic",
        "reading_time_minutes": 10,
        "intro": "When something goes wrong, the difference between a bad afternoon "
        "and a disaster is usually a plan made in calm. Meet incident response, its "
        "six phases, and the preparation that makes all the rest possible.",
        "tasks": [
            {
                "key": "what-ir",
                "kind": "check",
                "points": 2,
                "title": "What incident response actually is",
                "body": "<p>Everything in this course so far has been about stopping "
                "bad things from happening. This final module is about what you do "
                "when, despite your best efforts, one happens anyway. That is incident "
                "response: the organised way you react to a security incident so that "
                "you limit the damage and get back to normal as quickly and calmly as "
                "possible.</p>"
                "<p>The key word is organised. In the moment an incident hits, "
                "ransomware locking the files, an account clearly compromised, a "
                "laptop of client data lost, people feel a jolt of panic, and panic "
                "leads to exactly the wrong moves: hiding it, guessing, wiping things, "
                "paying too fast. Incident response replaces that panic with a set of "
                "steps decided in advance, so that under pressure you are following a "
                "plan rather than inventing one.</p>"
                "<p>You do not need to be the technical expert who fixes the problem. "
                "The most valuable thing a non-technical person brings to an incident "
                "is a calm head and a known set of first moves: recognise it, contain "
                "it, report it, and let the plan take over. Some of the worst outcomes "
                "in Australian businesses came not from the attack itself but from a "
                "panicked, disorganised response to it.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "incidents are not a maybe, they are a when, for organisations of "
                "every size. The businesses that come through them well are not the "
                "ones that were never hit, they are the ones that knew what to do in "
                "the first hour. This module gives you that first hour.</div>",
                "question": "What is incident response?",
                "hint": "Think about what you do after something has gone wrong, and how.",
                "options": [
                    ("The organised way you react to a security incident to limit damage and recover", True,
                     "Yes. It replaces panic with a set of steps decided in advance, so you follow a plan rather than invent one under pressure."),
                    ("A tool that prevents all incidents from happening", False,
                     "No. Prevention is the rest of the course. Incident response is what you do when something happens anyway."),
                    ("A type of firewall", False,
                     "No. A firewall is a preventive control. Incident response is your reaction after an incident occurs."),
                    ("Ignoring a problem until it goes away", False,
                     "The opposite. Incident response is a calm, organised reaction, not avoidance."),
                ],
            },
            {
                "key": "lifecycle",
                "kind": "check",
                "points": 2,
                "title": "The six phases, at a glance",
                "diagram": "ir-lifecycle",
                "body": "<p>Incident response is usually described as a lifecycle of "
                "six phases, and knowing their names and order gives you a map for the "
                "whole module. They flow in sequence, and the last one loops back to "
                "improve the first, which is why it is drawn as a cycle rather than a "
                "line.</p>"
                "<p>The six are: <strong>Preparation</strong>, the work you do before "
                "anything happens; <strong>Identification</strong>, recognising that "
                "an incident is under way; <strong>Containment</strong>, stopping it "
                "spreading; <strong>Eradication</strong>, removing the threat and "
                "closing the hole it came through; <strong>Recovery</strong>, "
                "restoring normal operations safely; and <strong>Lessons Learned</strong>, "
                "reviewing what happened so you are better prepared next time.</p>"
                "<p>You do not need to memorise a textbook, but this shape is genuinely "
                "useful, because it tells you what question you are answering at each "
                "moment. Am I ready? Is something happening? How do I stop it "
                "spreading? How do I get rid of it? How do I get back to normal? And "
                "what do I change so it does not happen again? Each phase is one of "
                "those questions, in order.</p>"
                "<div class=\"cy-callout\"><strong>The loop is the point.</strong> "
                "Notice that the cycle ends where it began, at Preparation. Every "
                "incident, handled well, leaves you better prepared for the next one. "
                "A response that skips the final review throws that lesson away and "
                "invites the same incident back.</div>",
                "inline_check": {
                    "question": "Which phase comes first, before any incident has even happened?",
                    "hint": "Which one is the work you do in advance, in calm?",
                    "options": [
                        ("Preparation", True,
                         "Yes. Preparation is the work done before anything happens, and it is what makes every other phase possible."),
                        ("Recovery", False,
                         "Recovery comes late, after you have contained and removed the threat. The first phase is Preparation."),
                        ("Eradication", False,
                         "Eradication is a middle phase, removing the threat. The very first phase is Preparation."),
                        ("Lessons Learned", False,
                         "Lessons Learned is the last phase, though it loops back to improve Preparation. The first is Preparation itself."),
                    ],
                },
                "body2": "<p>Over this module you will walk each phase in turn: "
                "Preparation in this lesson, Identification and Containment in the "
                "next, then Eradication, Recovery and Lessons Learned, and finally the "
                "legal duty to notify a serious breach. Hold the six-phase shape in "
                "your head and the rest hangs neatly off it.</p>",
                "question": "How many phases are in the incident response lifecycle, and what does the last one do?",
                "hint": "Count the phases, and think about what happens after Recovery.",
                "options": [
                    ("Six, and the last, Lessons Learned, loops back to improve Preparation", True,
                     "Yes. The six phases flow in order, and reviewing what happened makes you better prepared for next time."),
                    ("Three, and the last one is to pay the attacker", False,
                     "No. There are six phases, and paying an attacker is never one of them."),
                    ("Six, and the last one is to delete all your files", False,
                     "The six phases are right, but the last is Lessons Learned, a review, not deleting anything."),
                    ("Ten, and they never repeat", False,
                     "No. There are six, and they form a cycle, with the last looping back to improve preparation."),
                ],
            },
            {
                "key": "preparation",
                "kind": "check",
                "points": 2,
                "title": "Preparation: the phase that happens in calm",
                "body": "<p>The first phase is the one that happens when nothing is "
                "wrong, and it is the most important, because everything else depends "
                "on it. Preparation is all the work you do in advance so that when an "
                "incident hits, you are ready to respond well instead of scrambling.</p>"
                "<p>Preparation is not mysterious. It is the sum of habits you have "
                "already met, gathered into readiness. Tested backups, so you can "
                "recover without paying anyone. A simple written plan, so people know "
                "the first moves. A contact list, so nobody wastes precious minutes "
                "hunting for who to call: your IT support, your manager, and where to "
                "report. Clear roles, so it is understood who decides what. And ideally "
                "a quick practice or two, so the plan is not read for the first time "
                "during a real emergency.</p>"
                "<p>The reason preparation matters so much is that an incident is the "
                "worst possible time to be making these things up. The clock is "
                "running, people are stressed, and every decision is harder. A "
                "business that prepared in calm simply follows its plan; a business "
                "that did not is inventing one while the fire spreads.</p>"
                "<div class=\"cy-callout\"><strong>The plan on the fridge.</strong> A "
                "small accounting firm keeps a single laminated page by the office "
                "kitchen: if you think something is wrong, disconnect the device, "
                "phone this number, and do not delete anything. It cost nothing to "
                "make. When a staff member hit ransomware one morning, she did not "
                "have to think, she just read the three steps and followed them. That "
                "page was preparation, and it worked.</div>",
                "question": "What is 'Preparation' in incident response?",
                "hint": "When does this phase happen, and what does it involve?",
                "options": [
                    ("The work done in advance, in calm: backups, a plan, contacts, roles and practice", True,
                     "Yes. Preparation is getting ready before anything happens, so you follow a plan under pressure instead of scrambling."),
                    ("Cleaning up after the incident is over", False,
                     "That is closer to Recovery and Lessons Learned. Preparation is the work done beforehand."),
                    ("Paying the attacker in advance", False,
                     "No. Paying attackers is never part of a good plan. Preparation is readiness like backups and a plan."),
                    ("Something only large companies can do", False,
                     "Not at all. A single laminated page of first steps is preparation, and any business can do it."),
                ],
            },
            {
                "key": "why-plan",
                "kind": "check",
                "points": 1,
                "title": "Why the plan beats the panic",
                "body": "<p>It is worth being clear about why a plan matters so much, "
                "because it is not obvious until you have felt the moment. When an "
                "incident hits, your brain floods with stress, and stress is terrible "
                "for careful thinking. Under that pressure people reach for whatever "
                "feels like it will make the bad feeling stop: pay the ransom, hide "
                "the mistake, wipe the machine, tell no one.</p>"
                "<p>A plan removes the need to make those decisions in that state, "
                "because the decisions were already made, calmly, in advance. You are "
                "not deciding whether to disconnect the machine while your heart is "
                "pounding; you are following step one, which says disconnect the "
                "machine. That is the whole gift of preparation: it lets a stressed "
                "person act like a calm one, by borrowing the calm they had "
                "earlier.</p>",
                "question": "Why does having a plan help so much during an incident?",
                "hint": "Think about how well people make decisions under sudden stress.",
                "options": [
                    ("It lets a stressed person follow calm decisions that were made in advance", True,
                     "Yes. Stress ruins careful thinking, so a plan means the hard choices were already made, calmly, before the pressure hit."),
                    ("It makes the incident less likely to happen", False,
                     "Prevention does that. A response plan helps once an incident is already under way."),
                    ("It guarantees nothing will ever go wrong", False,
                     "Nothing guarantees that. A plan makes your response to what goes wrong far better."),
                    ("It means you never have to tell anyone", False,
                     "The opposite. A good plan usually includes telling the right people quickly."),
                ],
            },
            {
                "key": "sequence",
                "kind": "sequence",
                "points": 3,
                "title": "Put the lifecycle in order",
                "body": "<p>The six phases only work as a map if you know their order, "
                "so let us lock it in. Remember the questions each one answers: am I "
                "ready, is something happening, how do I stop it spreading, how do I "
                "remove it, how do I get back to normal, and what do I change for next "
                "time.</p>"
                "<p>The six phases are shuffled below. Tap them in the correct order, "
                "from the first phase to the last. Get all six in sequence to "
                "finish.</p>",
                "payload": {
                    "prompt": "Tap the six phases in order, from first to last. All six in sequence to finish.",
                    "steps": [
                        {"id": "prep", "label": "Preparation", "order": 1,
                         "detail": "The work done before anything happens"},
                        {"id": "ident", "label": "Identification", "order": 2,
                         "detail": "Recognising an incident is under way"},
                        {"id": "cont", "label": "Containment", "order": 3,
                         "detail": "Stopping the incident spreading"},
                        {"id": "erad", "label": "Eradication", "order": 4,
                         "detail": "Removing the threat and closing the hole"},
                        {"id": "rec", "label": "Recovery", "order": 5,
                         "detail": "Restoring normal operations safely"},
                        {"id": "learn", "label": "Lessons Learned", "order": 6,
                         "detail": "Reviewing what happened, to improve"},
                    ],
                },
            },
        ],
    },
    {
        "title": "Spot it and stop it",
        "reading_time_minutes": 10,
        "intro": "The first two phases in the heat of the moment: recognising that an "
        "incident is happening, working out how bad it is, and stopping it spreading "
        "before it can do more harm.",
        "tasks": [
            {
                "key": "identification",
                "kind": "check",
                "points": 2,
                "title": "Identification: noticing an incident",
                "body": "<p>You cannot respond to what you have not noticed, so the "
                "second phase, Identification, is simply recognising that a security "
                "incident is actually happening. It draws on the warning signs you met "
                "back in Module 2, but it adds a decision: this is not just an odd "
                "glitch, this is an incident, and it is time to act.</p>"
                "<p>The signs are the ones you already know. Files suddenly renamed or "
                "locked with a ransom note. Colleagues getting strange messages from "
                "your account. A login alert or an approval prompt for something you "
                "did not do. A device behaving very oddly, or an antivirus warning you "
                "cannot explain. Any of these might be the start of an incident, and "
                "the skill is not perfect certainty, it is noticing the change and "
                "taking it seriously enough to raise it.</p>"
                "<p>The single most important thing Identification asks of you is to "
                "say something quickly. An incident caught in its first minutes, while "
                "it is still one locked laptop or one dodgy login, is a manageable "
                "problem. The same incident noticed a week later, after it has spread "
                "and settled in, is a crisis. Early identification is what keeps a "
                "problem small, so a suspected incident always goes to the right "
                "people straight away.</p>"
                "<div class=\"cy-callout\"><strong>Better a false alarm than a missed "
                "one.</strong> People hesitate to report because they worry it might "
                "be nothing. In incident response, a false alarm costs a few minutes; "
                "a missed incident can cost the business. Raise it. Nobody worth "
                "working for will mind you flagging something that turned out to be "
                "fine.</div>",
                "question": "What does the 'Identification' phase involve?",
                "hint": "It is about noticing. What are you recognising, and what do you then do?",
                "options": [
                    ("Recognising that a security incident is happening, and raising it quickly", True,
                     "Yes. It is noticing the warning signs, deciding this is an incident, and reporting it straight away while it is still small."),
                    ("Removing the malware from every machine", False,
                     "That is Eradication, a later phase. Identification is about noticing the incident in the first place."),
                    ("Writing the incident response plan", False,
                     "That is Preparation, done in advance. Identification is recognising an incident as it happens."),
                    ("Restoring files from a backup", False,
                     "That is Recovery. Identification comes first: noticing that something is wrong."),
                ],
            },
            {
                "key": "triage-severity",
                "kind": "check",
                "points": 2,
                "title": "How bad is it? Sizing up the incident",
                "body": "<p>Once you know an incident is real, the next question is how "
                "serious it is, because that shapes everything you do next. This "
                "sizing-up is sometimes called triage, borrowed from the way a "
                "hospital sorts patients by how urgent their needs are. Not every "
                "incident is a five-alarm fire, and not every incident is minor.</p>"
                "<p>A few plain questions do the work. What exactly is affected, one "
                "laptop or the whole shared drive? What kind of information is "
                "involved, a menu and some photos, or customer records and "
                "identities? Is it still spreading right now, or has it stopped? And "
                "is anything critical to the business down? You are not aiming for a "
                "precise score, you are getting a rough sense of scale, so the "
                "response matches the problem. A single quarantined file is not the "
                "same as ransomware across every machine, and treating them the same "
                "wastes effort on one and under-reacts to the other.</p>"
                "<div class=\"cy-callout\"><strong>The question that changes "
                "everything.</strong> Of all the triage questions, one matters most "
                "for what comes next: was personal information about people exposed? "
                "If customer or patient data may have been taken, the incident is not "
                "just a technical clean-up, it may carry a legal duty to notify, which "
                "is the whole of this module's final lesson. Always ask, early, "
                "whether people's information was involved.</div>",
                "inline_check": {
                    "question": "During triage, which question matters most for deciding whether you may have a legal duty later?",
                    "hint": "Think about what turns a technical clean-up into something the law cares about.",
                    "options": [
                        ("Was personal information about people exposed?", True,
                         "Yes. If people's data may have been taken, the incident can carry a legal duty to notify, which shapes the whole response."),
                        ("What time of day did it start?", False,
                         "The timing is minor. What matters for later duties is whether personal information was exposed."),
                        ("Which brand of computer was affected?", False,
                         "The make of device is not the point. Whether personal data was exposed is what carries legal weight."),
                        ("How fast is the office internet?", False,
                         "Speed is irrelevant here. The key question is whether personal information was exposed."),
                    ],
                },
                "body2": "<p>Sizing up an incident is not about panicking over how bad "
                "it might be, it is about matching your response to reality. A quick, "
                "honest read of what is affected and whether people's data is involved "
                "tells everyone how hard to push and who else needs to know. With that "
                "picture, the next move, containment, becomes clear.</p>",
                "question": "What is the point of sizing up, or triaging, an incident?",
                "hint": "Why do you assess how bad it is before diving into fixing it?",
                "options": [
                    ("To match your response to the real scale of the problem, and see who else needs to know", True,
                     "Yes. A rough sense of what is affected and whether data was exposed tells you how hard to push and who to involve."),
                    ("To decide who to blame for it", False,
                     "Blame is not the goal, and rarely helpful. Triage is about understanding the scale, not fault."),
                    ("To make the incident look smaller than it is", False,
                     "Honesty is the point. Triage gives an accurate read, not a comforting one."),
                    ("To delay doing anything about it", False,
                     "The opposite. A quick size-up speeds up the right response, it does not delay it."),
                ],
            },
            {
                "key": "containment",
                "kind": "check",
                "points": 2,
                "title": "Containment: stop the bleeding",
                "body": "<p>Containment is the phase where you stop the incident "
                "spreading, and it is often the most urgent thing you will do. The "
                "goal is simple: limit the damage to what has already happened, and "
                "prevent it reaching anything else. In a fast-moving incident like "
                "ransomware or a spreading worm, minutes matter.</p>"
                "<p>For most people, containment means one decisive action: get the "
                "affected device off the network. Unplug the network cable, or turn "
                "off its Wi-Fi. That single step stops malware spreading to shared "
                "drives and other machines, and cuts off an attacker who is working "
                "through a compromised account. It is the digital equivalent of "
                "closing the fire doors. You are not fixing anything yet, you are "
                "stopping it getting worse.</p>"
                "<p>There is an important balance in containment: act fast to stop the "
                "spread, but do not destroy the evidence. Disconnecting a machine is "
                "good, because it isolates it. Wiping it clean immediately is usually "
                "bad, because it erases the traces that help work out what happened, "
                "how far it went, and whether data was taken. Isolate, do not "
                "obliterate, and leave the deeper clean-up to the plan and the "
                "experts.</p>"
                "<div class=\"cy-callout\"><strong>Pull the plug, keep the "
                "evidence.</strong> When ransomware began encrypting a firm's files, "
                "the staff member did exactly the right thing: she pulled the network "
                "cable to contain it, and then left the machine alone rather than "
                "trying to wipe or fix it. Isolating it stopped the spread; leaving it "
                "intact let the responders see how it got in and confirm what was "
                "affected.</div>",
                "question": "For most people, what is the key containment action when a device is compromised?",
                "hint": "What single step stops the problem spreading to other machines?",
                "options": [
                    ("Disconnect the device from the network, by cable or Wi-Fi", True,
                     "Yes. Getting it off the network stops malware spreading and cuts off an attacker, without destroying evidence."),
                    ("Immediately wipe and reinstall the device yourself", False,
                     "That destroys the evidence of what happened and may miss other affected machines. Isolate it, do not obliterate it."),
                    ("Keep using it so you do not lose your work", False,
                     "That lets the incident spread and do more damage. Disconnect first."),
                    ("Turn the whole office internet off for a week", False,
                     "That is heavy-handed and rarely needed. Isolating the affected device is the targeted containment move."),
                ],
            },
            {
                "key": "dont-panic-delete",
                "kind": "check",
                "points": 1,
                "title": "Do not clean up in a panic",
                "body": "<p>One instinct is worth naming and resisting, because it "
                "does real harm: the urge to quietly clean up the mess yourself before "
                "anyone sees it. It comes from a good place, wanting to fix things and "
                "avoid embarrassment, but in an incident it is one of the most "
                "damaging things you can do.</p>"
                "<p>Deleting the ransom note, wiping the machine, or 'sorting it out' "
                "alone causes two problems. It destroys the evidence that responders "
                "need to understand the incident, including whether personal data was "
                "taken, which you may be legally required to know. And it often misses "
                "the real extent of the problem, leaving a second infected machine or "
                "a compromised account still active while you think you have handled "
                "it. Contain the incident, report it, and let the plan run. The "
                "clean-up is a later phase, done properly, not a panicked solo "
                "effort.</p>",
                "question": "Why should you not quietly wipe or clean up a compromised machine yourself?",
                "hint": "Think about evidence, and about what a solo clean-up might miss.",
                "options": [
                    ("It destroys evidence and often misses the full extent, like a second infected machine", True,
                     "Yes. A panicked clean-up erases what responders need and can leave the real problem still active. Contain, report, and follow the plan."),
                    ("It uses too much electricity", False,
                     "Power use is not the issue. The harm is lost evidence and a missed, still-active problem."),
                    ("There is no reason, cleaning up alone is fine", False,
                     "It is not fine. It destroys evidence and often leaves part of the incident unresolved."),
                    ("It makes the machine run faster", False,
                     "Speed is irrelevant. The point is preserving evidence and not missing the full extent."),
                ],
            },
            {
                "key": "contain-classify",
                "kind": "classify",
                "points": 3,
                "title": "Sound response, or making it worse?",
                "body": "<p>The first minutes of an incident are full of choices, and "
                "under pressure the wrong ones can feel just as natural as the right "
                "ones. Sorting good moves from harmful ones now makes them automatic "
                "when it counts.</p>"
                "<p>Below are things a person might do in the first minutes of an "
                "incident. For each one, decide whether it is a sound response or "
                "makes things worse. Lean on the lesson: isolate fast, preserve "
                "evidence, report early, and do not go it alone.</p>",
                "payload": {
                    "prompt": "For each action, choose Sound response or Makes it worse. Get all six to finish.",
                    "categories": [
                        {"id": "good", "label": "Sound response"},
                        {"id": "bad", "label": "Makes it worse"},
                    ],
                    "events": [
                        {"id": "disconnect", "category": "good",
                         "text": "Disconnect the affected computer from the network.",
                         "why": "This contains the incident by stopping it spreading. A sound first move."},
                        {"id": "keep-working", "category": "bad",
                         "text": "Keep using the computer so you do not lose your work.",
                         "why": "That lets the incident spread and do more damage. Disconnect first."},
                        {"id": "report", "category": "good",
                         "text": "Report it to your manager or IT straight away.",
                         "why": "Fast reporting gets the right people acting while the problem is small. A sound move."},
                        {"id": "wipe", "category": "bad",
                         "text": "Immediately wipe the machine to clean it, before anyone looks.",
                         "why": "That destroys evidence and may miss other affected machines. Isolate, do not obliterate."},
                        {"id": "note", "category": "good",
                         "text": "Note what you saw: the time, the message on screen, what is affected.",
                         "why": "A quick record helps responders understand the incident. A genuinely useful, sound move."},
                        {"id": "quiet-pay", "category": "bad",
                         "text": "Quietly pay the ransom and tell no one.",
                         "why": "Paying is unreliable and funds crime, and hiding it robs everyone of the chance to respond properly. It makes things worse."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Clean up and come back",
        "reading_time_minutes": 10,
        "intro": "With the incident contained, the last three phases bring you back "
        "to normal: remove the threat for good, restore what was lost, and turn the "
        "whole painful episode into a lesson that makes you stronger.",
        "tasks": [
            {
                "key": "eradication",
                "kind": "check",
                "points": 2,
                "title": "Eradication: remove it, and close the hole",
                "body": "<p>Containment stopped the incident spreading. Eradication is "
                "the phase where you actually get rid of the threat: remove the "
                "malware from every affected machine, delete the attacker's foothold, "
                "and make sure nothing of theirs remains. This is usually work for "
                "your IT support or a specialist, but there is one part of it everyone "
                "should understand, because it is so often missed.</p>"
                "<p>Removing the malware is not enough on its own. You also have to "
                "close the hole it came through, or it simply comes straight back. If "
                "ransomware got in through an unpatched system, you patch it. If an "
                "attacker used a phished password, you reset that password and turn on "
                "multi-factor authentication. If a compromised account was the way in, "
                "you lock it down. Cleaning up the malware while leaving the open door "
                "untouched is like mopping the floor without turning off the tap.</p>"
                "<div class=\"cy-callout\"><strong>The threat that came back.</strong> "
                "A business cleaned the ransomware off its machines and breathed a "
                "sigh of relief, then got hit again a week later through the very same "
                "unpatched system. The malware had been removed, but the hole it "
                "entered through was never closed. Eradication means both: remove the "
                "threat, and shut the door it used.</div>",
                "question": "Eradication means removing the threat, but what crucial second part is often missed?",
                "hint": "If you remove the malware but leave the way it got in, what happens?",
                "options": [
                    ("Closing the hole it came through, or the threat simply returns", True,
                     "Yes. Patch the flaw, reset the phished password, lock the compromised account. Otherwise the attacker walks back in the same way."),
                    ("Buying a faster computer to replace the old one", False,
                     "New hardware does not close the entry point. You must fix the flaw or account that let the threat in."),
                    ("Telling no one it happened", False,
                     "Silence is not part of eradication, and usually harmful. The missed part is closing the entry point."),
                    ("Paying the attacker to remove it for you", False,
                     "Never. You remove the threat and close the hole yourself; you do not rely on the attacker."),
                ],
            },
            {
                "key": "recovery",
                "kind": "check",
                "points": 2,
                "title": "Recovery: getting back to normal, safely",
                "body": "<p>With the threat removed and the hole closed, Recovery is "
                "the phase of restoring normal operations. It is the light at the end "
                "of the incident, the point where systems come back and people can "
                "work again. The word that matters is safely, because a rushed "
                "recovery can undo all the careful work before it.</p>"
                "<p>Recovery usually means restoring data and systems from clean, "
                "trusted backups, the ones you prepared in calm and, ideally, tested. "
                "This is why backups have come up in almost every module: they are "
                "what let you recover from ransomware without paying, and from a "
                "serious incident without starting from nothing. As systems come back, "
                "you verify they are working properly and keep a close watch for any "
                "sign the threat is returning, because reinfection during recovery is "
                "a real risk.</p>"
                "<div class=\"cy-callout\"><strong>Restore from clean, not "
                "infected.</strong> One subtlety trips people up: you must restore "
                "from a backup taken before the incident, not after. Restoring a copy "
                "that already contains the malware just brings the problem back. This "
                "is why regular, well-kept backups matter, so you always have a clean "
                "point in time to return to.</div>",
                "inline_check": {
                    "question": "When recovering from ransomware, which backup should you restore from?",
                    "hint": "Think about when the backup was taken, relative to the infection.",
                    "options": [
                        ("A clean backup taken before the infection", True,
                         "Yes. A backup from before the incident is free of the malware. Restoring a later, infected copy just brings the problem back."),
                        ("The most recent backup, even if taken after the infection", False,
                         "A backup taken after the infection may contain the malware itself. Restore from a clean, earlier point."),
                        ("Any backup, it does not matter when it was taken", False,
                         "It matters a great deal. An infected backup reintroduces the threat. Use a clean one from before."),
                        ("You should never use backups during recovery", False,
                         "Backups are exactly what recovery relies on. The key is choosing a clean one from before the incident."),
                    ],
                },
                "body2": "<p>A good recovery is patient. It is tempting to declare "
                "victory the moment the main system is back, but the incident is not "
                "truly over until systems are verified, watched for a while, and "
                "confirmed clean. Rushing to normal is how a half-finished response "
                "becomes a second incident.</p>",
                "question": "What does the Recovery phase mainly involve?",
                "hint": "How do you get systems and data back, and what do you use to do it?",
                "options": [
                    ("Restoring systems and data from clean backups, then verifying and watching them", True,
                     "Yes. Recovery brings you back to normal safely, using trusted backups and keeping watch for any return of the threat."),
                    ("Removing the malware from the machines", False,
                     "That is Eradication, the phase before. Recovery is about restoring normal operations after the threat is gone."),
                    ("Deciding whether an incident is happening", False,
                     "That is Identification, an earlier phase. Recovery is restoring systems once the threat is removed."),
                    ("Paying to get your files back", False,
                     "No. Recovery uses your own clean backups, which is exactly how you avoid paying anyone."),
                ],
            },
            {
                "key": "reset-credentials",
                "kind": "check",
                "points": 1,
                "title": "Change the locks",
                "body": "<p>One recovery step deserves a spotlight, because it is easy "
                "to forget in the rush to get systems back: change the locks. If there "
                "is any chance an attacker got hold of passwords during the incident, "
                "those passwords have to be reset, and multi-factor authentication "
                "turned on where it is not already.</p>"
                "<p>Think of it like a break-in at a physical building. You would not "
                "just repair the broken window and carry on; you would change the "
                "locks, because the intruder may have copied a key. The digital "
                "version is the same. Reset the passwords for any accounts that may "
                "have been exposed, especially the important ones like email, and add "
                "a second factor so that even a password the attacker still holds is "
                "no longer enough to get back in.</p>",
                "question": "After an incident where passwords may have been exposed, you should:",
                "hint": "What is the digital equivalent of changing the locks after a break-in?",
                "options": [
                    ("Reset the affected passwords and turn on multi-factor authentication", True,
                     "Yes. Any password an attacker may hold must be changed, and a second factor added, so a stolen password is no longer enough."),
                    ("Keep the same passwords to avoid confusion", False,
                     "That leaves the attacker's copied keys working. Reset anything that may have been exposed."),
                    ("Only change passwords if you are completely certain they were stolen", False,
                     "If there is any real chance they were exposed, reset them. Waiting for certainty leaves the door open."),
                    ("Write the new passwords on a shared note so nobody forgets", False,
                     "Never do that. Use a password manager, and keep the new passwords private."),
                ],
            },
            {
                "key": "lessons-learned",
                "kind": "check",
                "points": 2,
                "title": "Lessons Learned: get stronger from it",
                "body": "<p>The final phase is the one most often skipped, and skipping "
                "it is a genuine mistake. Once the dust settles and everything is back "
                "to normal, Lessons Learned is a calm review of what happened, so that "
                "the whole painful episode makes you stronger instead of leaving you "
                "exactly as exposed as before.</p>"
                "<p>A good review asks plain questions without pointing fingers. What "
                "happened, and how did it get in? What did we do well in the response, "
                "and what was slow or confusing? What can we change so this specific "
                "thing cannot happen again, and so we respond even better next time? "
                "The answers feed straight back into Preparation, which is why the "
                "lifecycle is a loop. Maybe you need a patch applied, a backup tested, "
                "a plan written down, some training booked.</p>"
                "<p>The tone of this review matters enormously. It must be blameless. "
                "The moment a review becomes about punishing the person who clicked "
                "the link, people stop being honest, and you lose the very information "
                "that would prevent the next incident. The goal is a better system, "
                "not a scapegoat. The person who made the mistake is usually the one "
                "with the most useful lesson to share.</p>"
                "<div class=\"cy-callout\"><strong>The review that paid off.</strong> "
                "After a phishing incident, a council held a short, blameless review "
                "and found the real problem was not one careless click, it was that "
                "MFA had never been switched on. They turned it on across the "
                "organisation that month. The next phishing attempt, and there was "
                "one, went nowhere. That is a lesson learned turned into a lesson "
                "used.</div>",
                "question": "What makes a 'Lessons Learned' review effective?",
                "hint": "Think about the tone, and where the findings should go.",
                "options": [
                    ("A blameless look at what happened, feeding concrete improvements back into preparation", True,
                     "Yes. Without blame, people stay honest, and the findings become real changes that prevent the next incident."),
                    ("Identifying who to punish for the incident", False,
                     "Blame makes people hide the truth, and you lose the lessons. The goal is a better system, not a scapegoat."),
                    ("Agreeing never to speak of it again", False,
                     "Silence throws away the lesson. A review exists precisely to learn from what happened."),
                    ("Deciding the incident was nobody's concern", False,
                     "The point is to improve. A good review turns the episode into concrete changes that make you stronger."),
                ],
            },
            {
                "key": "recovery-sort",
                "kind": "sort",
                "points": 3,
                "title": "Which phase does it belong to?",
                "body": "<p>The last three phases can blur together, so let us make "
                "them sharp. <strong>Eradication</strong> removes the threat and closes "
                "the hole. <strong>Recovery</strong> restores normal operations safely. "
                "<strong>Lessons Learned</strong> reviews the episode to improve for "
                "next time.</p>"
                "<p>Sort each action into the phase it belongs to. Get all six right to "
                "finish.</p>",
                "payload": {
                    "prompt": "Tap an action, then tap the phase it belongs to. All six to finish.",
                    "buckets": [
                        {"id": "erad", "label": "Eradication"},
                        {"id": "rec", "label": "Recovery"},
                        {"id": "learn", "label": "Lessons Learned"},
                    ],
                    "items": [
                        {"id": "remove", "text": "Remove the malware from every affected machine",
                         "bucket": "erad", "why": "Getting rid of the threat itself is Eradication."},
                        {"id": "patch", "text": "Patch the unpatched system the attacker used to get in",
                         "bucket": "erad", "why": "Closing the hole the threat came through is part of Eradication."},
                        {"id": "restore", "text": "Restore files from a clean backup taken before the incident",
                         "bucket": "rec", "why": "Bringing systems and data back safely is Recovery."},
                        {"id": "verify", "text": "Verify systems are working and watch for reinfection",
                         "bucket": "rec", "why": "Confirming a safe return to normal is Recovery."},
                        {"id": "review", "text": "Hold a blameless review of what happened",
                         "bucket": "learn", "why": "Reviewing the episode to understand it is Lessons Learned."},
                        {"id": "improve", "text": "Update the plan so the same gap cannot be used again",
                         "bucket": "learn", "why": "Turning findings into improvements is Lessons Learned, looping back to Preparation."},
                    ],
                },
            },
        ],
    },
    {
        "title": "The law, and the whole response",
        "reading_time_minutes": 9,
        "intro": "An incident involving people's data is not only a technical matter, "
        "it can be a legal one. Learn the Australian duty to notify a serious breach, "
        "then bring the whole lifecycle together in a real ransomware morning.",
        "tasks": [
            {
                "key": "privacy-act",
                "kind": "check",
                "points": 2,
                "title": "The Privacy Act and notifiable breaches",
                "diagram": "breach-notify",
                "body": "<p>When an incident involves people's personal information, "
                "responding well is not only good practice, it can be the law. In "
                "Australia, the Privacy Act 1988 and its Notifiable Data Breaches "
                "scheme set out an obligation to tell people when their information "
                "has been caught up in a serious breach. This is general information "
                "to make you aware of the duty, not legal advice, and the exact "
                "obligations are worth checking for your own organisation.</p>"
                "<p>The core idea is fairness. If an organisation loses control of your "
                "personal information in a way that could seriously harm you, you have "
                "a right to know, so you can protect yourself, and the regulator has a "
                "right to know, so it can oversee the response. The scheme turns that "
                "fairness into a concrete duty, rather than leaving it to whether a "
                "business feels like owning up.</p>"
                "<p>This matters to you because the trigger for that duty is decided "
                "during an incident, in the phases you have just learned. When you "
                "size up an incident and ask whether personal information was exposed, "
                "you are not only guiding the technical response, you are starting the "
                "clock on a possible legal obligation. Knowing the duty exists is what "
                "makes you ask the question early.</p>"
                "<div class=\"cy-callout\"><strong>Why the law is on your side "
                "here.</strong> The notification duty can feel like a burden in the "
                "middle of a hard week, but it points the same way good response "
                "already does: be honest, be quick, and help the people affected. A "
                "business that hides a serious breach fails its customers twice, once "
                "by losing the data and once by leaving them in the dark.</div>",
                "question": "What does the Notifiable Data Breaches scheme, under the Privacy Act, require?",
                "hint": "Think about who has a right to know when personal information is seriously exposed.",
                "options": [
                    ("Telling affected people, and the regulator, when a breach is likely to cause serious harm", True,
                     "Yes. The scheme turns fairness into a duty: notify those affected and the OAIC when a breach could seriously harm people."),
                    ("Paying a fine for every incident, no matter how small", False,
                     "No. The scheme is about notifying serious breaches, not automatic fines for every incident."),
                    ("Keeping all breaches secret to avoid alarm", False,
                     "The opposite. The whole point is that people have a right to be told about serious breaches."),
                    ("Reporting only if the breach reaches the news", False,
                     "The trigger is likely serious harm, not media attention. Many breaches that never make the news are notifiable."),
                ],
            },
            {
                "key": "notify-when",
                "kind": "check",
                "points": 2,
                "title": "When you have to tell someone",
                "body": "<p>Discovering a breach is not only a technical problem, it "
                "can be a legal obligation, and getting this part wrong causes its own "
                "harm. In Australia, the Privacy Act 1988 and its Notifiable Data "
                "Breaches scheme set out when an organisation must tell people that "
                "their information has been exposed. This is general information "
                "rather than legal advice, but every non-technical person should know "
                "the shape of it.</p>"
                "<p>The trigger is what the scheme calls an eligible data breach. "
                "Personal information is lost, or accessed or disclosed without "
                "authorisation, and that exposure is likely to result in serious harm "
                "to someone, such as identity theft, financial loss or serious "
                "distress. Not every minor slip clears that bar. A single internal "
                "email sent to the wrong colleague and deleted straight away is "
                "probably not it. A database of customers' identity documents taken by "
                "an attacker very much is.</p>"
                "<p>When a breach is eligible, two groups must be told: the affected "
                "individuals, so they can protect themselves, and the Office of the "
                "Australian Information Commissioner, the OAIC, which is the regulator. "
                "The timing is as soon as practicable after you become aware. If you "
                "are genuinely unsure whether a breach is serious enough to notify, "
                "you are generally allowed up to thirty days to assess it, but treat "
                "that as a limit, not a target. You move as fast as you reasonably "
                "can.</p>"
                "<div class=\"cy-callout\"><strong>Small does not mean exempt.</strong> "
                "A common and dangerous assumption is that these rules are only for "
                "big companies. Many small organisations are covered too, and health "
                "service providers of any size are covered regardless of turnover, "
                "because health information is so sensitive. A small clinic that loses "
                "patient records has the same duty to notify as a large hospital. If "
                "you are unsure whether your organisation is covered, that is exactly "
                "the question to raise with your manager before an incident, not "
                "during one.</div>",
                "inline_check": {
                    "question": "What makes a data breach 'notifiable' under the scheme?",
                    "hint": "It is not about size or fame. What is the harm test?",
                    "options": [
                        ("It is likely to result in serious harm to the affected individuals", True,
                         "Yes. The trigger is likely serious harm, such as identity theft or financial loss, not whether the breach is big or public."),
                        ("Any breach at all, however minor, must always be notified", False,
                         "Not every minor slip clears the bar. The test is whether the breach is likely to cause serious harm."),
                        ("Only breaches that make the news", False,
                         "Media attention is irrelevant. The test is likely serious harm to people, whether or not it is reported."),
                        ("Only breaches at government agencies", False,
                         "Many businesses are covered too, including small health providers. The test is likely serious harm."),
                    ],
                },
                "body2": "<p>Two practical points follow. First, notification is a "
                "reason to prepare, not to hide. Knowing you may have to tell people "
                "is all the more reason to have a plan and to act quickly and "
                "honestly. Second, this sits inside the response lifecycle you have "
                "learned: you identify and contain the incident, you assess whether it "
                "is notifiable, and if it is, notifying becomes part of your recovery. "
                "It is not a separate world, it is one more phase of doing the right "
                "thing. Separately, you can also report cybercrime to ReportCyber, run "
                "by the Australian Cyber Security Centre.</p>",
                "question": "Under the Notifiable Data Breaches scheme, who must be told about an eligible data breach?",
                "hint": "Two groups: the people at risk, and an official body.",
                "options": [
                    ("The affected individuals and the OAIC", True,
                     "Yes. Those whose data was exposed, so they can protect themselves, and the Office of the Australian Information Commissioner, the regulator."),
                    ("Only your own staff", False,
                     "Telling staff is not enough. The affected individuals and the OAIC must be notified."),
                    ("Nobody, as long as you fix it quietly", False,
                     "Hiding an eligible breach is exactly what the scheme forbids. The affected people and the OAIC must be told."),
                    ("Only your bank", False,
                     "Your bank is not the requirement. Notify the affected individuals and the OAIC."),
                ],
            },
            {
                "key": "ransomware-morning",
                "kind": "branch",
                "points": 4,
                "title": "A ransomware morning",
                "body": "<p>This is the whole module in one scenario. It is Monday "
                "morning at a small clinic, you are the first person at the front "
                "desk, and something is very wrong with the computers. Every decision "
                "you make changes how this goes.</p>"
                "<p>Walk it through using everything you have learned: identify, "
                "contain, report, recover from backups rather than pay, decide about "
                "notifying, and finish with a lesson. There are no trick questions, "
                "and if a choice goes wrong you will see why and get another go.</p>",
                "payload": {
                    "prompt": "Choose what you would really do. You can always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "It is 8:15am. Files on the reception PC are turning to gibberish before your eyes, "
                            "and a message demands payment in cryptocurrency to unlock them. What is your first move?",
                            "choices": [
                                {"label": "Keep clicking to try to save the open files", "to": "n1bad",
                                 "outcome": "bad",
                                 "feedback": "Every second it stays connected, the ransomware spreads further, including to the shared drive. Containment comes first."},
                                {"label": "Disconnect the PC from the network straight away", "to": "n2",
                                 "outcome": "good",
                                 "feedback": "Exactly. Pulling it off the network contains the ransomware before it can reach the shared drive and other machines."},
                            ],
                        },
                        "n1bad": {
                            "text": "While you try to save files, the ransomware reaches the shared drive and a second computer.",
                            "choices": [{"label": "See the better first move", "to": "n2"}],
                        },
                        "n2": {
                            "text": "The PC is off the network. You have a moment. What now?",
                            "choices": [
                                {"label": "Quietly wipe the PC and reinstall it before anyone notices", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "Wiping it destroys the evidence of what happened and whether data was taken, and you may miss other affected machines. Report it instead."},
                                {"label": "Report it to the practice manager and IT, and note what you saw", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Right. Reporting starts the plan, and your notes on the time and the message help the responders."},
                            ],
                        },
                        "n2bad": {
                            "text": "With the machine wiped, no one can tell how the attacker got in, or whether patient data was taken.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "IT confirms it is ransomware. There is a clean nightly backup from before this morning, and it "
                            "has been tested. The ransom note demands payment within 48 hours. What do you advise?",
                            "choices": [
                                {"label": "Pay the ransom to be safe and save time", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds crime, and marks you as a payer. With a clean, tested backup there is no need to even consider it."},
                                {"label": "Restore from the clean backup and do not pay", "to": "n4",
                                 "outcome": "good",
                                 "feedback": "Yes. A clean backup from before the incident lets you recover without funding criminals or gambling on a key."},
                            ],
                        },
                        "n3bad": {
                            "text": "You reconsider: a clean, tested backup is sitting right there, and paying would risk everything for nothing.",
                            "choices": [{"label": "Take the better path", "to": "n4"}],
                        },
                        "n4": {
                            "text": "During the clean-up, IT finds the attacker reached a file of patients' names, dates of birth and "
                            "Medicare numbers. That is personal information, likely to cause serious harm. What now?",
                            "choices": [
                                {"label": "Say nothing, since the files are restored and it is fixed", "to": "n4bad",
                                 "outcome": "bad",
                                 "feedback": "Restoring the files does not undo the exposure. A breach likely to cause serious harm must be notified to the affected people and the OAIC."},
                                {"label": "Begin notifying: the affected patients and the OAIC, as soon as practicable", "to": "n5",
                                 "outcome": "good",
                                 "feedback": "Right. Sensitive personal data was exposed, so under the Notifiable Data Breaches scheme the patients and the OAIC must be told."},
                            ],
                        },
                        "n4bad": {
                            "text": "Weeks later, patients discover their details were exposed and were never told. The harm, and the breach of duty, are now much worse.",
                            "choices": [{"label": "See the better path", "to": "n5"}],
                        },
                        "n5": {
                            "text": "The systems are restored, passwords are reset, MFA is on, and the patients and the OAIC have been "
                            "notified. A week later, what completes a good response?",
                            "choices": [
                                {"label": "Put it behind you and never mention it again", "to": "n5bad",
                                 "outcome": "bad",
                                 "feedback": "Skipping the review throws away the lesson and invites the same incident back. The final phase is Lessons Learned."},
                                {"label": "Hold a blameless review of what happened and what to change", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes. A blameless review turns the episode into concrete improvements, looping back to better preparation."},
                            ],
                        },
                        "n5bad": {
                            "text": "You reconsider: without a review, the gap that let this in stays open for next time.",
                            "choices": [{"label": "Take the better path", "to": "end"}],
                        },
                        "end": {
                            "text": "That is a whole incident handled well: you identified it, contained it, reported it, recovered from a "
                            "clean backup instead of paying, notified the breach as the law requires, and reviewed it to get stronger. That is "
                            "the entire lifecycle, and none of it needed you to be the technical expert. It needed a calm head and a plan.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "ir-recap",
                "kind": "check",
                "points": 2,
                "title": "Your incident response habits",
                "body": "<p>That is incident response, and that is the whole course. "
                "When something goes wrong, you now have a map: recognise the incident "
                "and raise it quickly, contain it by disconnecting the affected device, "
                "report it and follow the plan rather than going it alone, recover "
                "from clean backups instead of paying, notify a serious breach as the "
                "law requires, and review it afterwards, without blame, to get "
                "stronger.</p>"
                "<p>Notice that not one of those steps asked you to be a technical "
                "expert. The most valuable person in an incident is often the calm, "
                "prepared non-technical one who knows the first moves and makes them "
                "without panic. Across six modules you have become that person: someone "
                "who understands the threats, communicates securely, recognises an "
                "attack, and knows exactly what to do when one lands. That is what "
                "keeps an organisation safe.</p>",
                "question": "What is the most valuable thing a non-technical person brings to an incident?",
                "hint": "It is not technical skill. Think about the first hour.",
                "options": [
                    ("A calm head and a known set of first moves: recognise, contain, report, follow the plan", True,
                     "Yes. Preparation and calm let a non-technical person do the most important work of an incident, before the experts even arrive."),
                    ("The ability to personally remove all the malware", False,
                     "That is specialist work, and not what is needed first. The vital contribution is calm, prepared first moves."),
                    ("Paying the ransom quickly", False,
                     "Paying is never the goal. The valuable contribution is a calm, correct response and following the plan."),
                    ("Keeping the incident secret", False,
                     "Silence harms the response. The valuable thing is recognising, containing and reporting, calmly and quickly."),
                ],
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. A bank of 40 (draw 10 at random), ten per lesson. Four options each,
# exactly one correct, every option carries an explanation that teaches. Fuel for
# the Adaptive Feedback Engine. House voice: warm, plain, no em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: preparation and the lifecycle ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is incident response?",
            "options": [
                ("The organised way you react to a security incident to limit damage and recover", True,
                 "Yes. It replaces panic with steps decided in advance, so you follow a plan rather than invent one under pressure."),
                ("A tool that prevents all incidents", False,
                 "No. Prevention is the rest of the course. Incident response is what you do when something happens anyway."),
                ("A type of antivirus", False,
                 "No. Antivirus is preventive. Incident response is your reaction after an incident occurs."),
                ("Ignoring problems until they pass", False,
                 "The opposite. It is a calm, organised reaction, not avoidance."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "How many phases are in the incident response lifecycle used in this module?",
            "options": [
                ("Six: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned", True,
                 "Yes. They flow in order, and the last loops back to improve the first."),
                ("Three, ending with paying the attacker", False,
                 "No. There are six phases, and paying an attacker is never one of them."),
                ("Ten, and they never repeat", False,
                 "No. There are six, and they form a repeating cycle."),
                ("Two: break and fix", False,
                 "It is more structured than that. Six phases guide a good response."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Which phase comes first, before any incident has happened?",
            "options": [
                ("Preparation", True,
                 "Yes. It is the work done in advance, and it makes every other phase possible."),
                ("Recovery", False,
                 "Recovery comes late, after containing and removing the threat. The first phase is Preparation."),
                ("Containment", False,
                 "Containment happens during an incident. The first phase is Preparation."),
                ("Lessons Learned", False,
                 "That is the last phase, though it loops back to Preparation. The first is Preparation itself."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What does 'Preparation' involve?",
            "options": [
                ("Work done in advance: backups, a plan, contacts, roles and practice", True,
                 "Yes. Getting ready in calm so you follow a plan under pressure instead of scrambling."),
                ("Cleaning up after the incident is over", False,
                 "That is closer to Recovery and Lessons Learned. Preparation is beforehand."),
                ("Paying the attacker in advance", False,
                 "No. Paying is never part of a good plan. Preparation is readiness like backups and a plan."),
                ("Something only large companies can do", False,
                 "Any business can do it. Even a single page of first steps is preparation."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why does having a plan help so much during an incident?",
            "options": [
                ("It lets a stressed person follow calm decisions made in advance", True,
                 "Yes. Stress ruins careful thinking, so a plan means the hard choices were already made before the pressure hit."),
                ("It makes the incident less likely to happen", False,
                 "Prevention does that. A response plan helps once an incident is under way."),
                ("It guarantees nothing will go wrong", False,
                 "Nothing guarantees that. A plan makes your response far better."),
                ("It means you never have to tell anyone", False,
                 "The opposite. A good plan usually includes telling the right people quickly."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "Why is the incident response lifecycle drawn as a loop rather than a straight line?",
            "options": [
                ("The last phase, Lessons Learned, feeds back to improve Preparation for next time", True,
                 "Yes. Every incident handled well leaves you better prepared, so the cycle returns to where it began."),
                ("Because incidents never really end", False,
                 "Incidents do end. The loop is about learning from each one to prepare better."),
                ("Because you repeat every phase endlessly during one incident", False,
                 "You do not loop within one incident. The loop is that lessons improve future preparation."),
                ("It is drawn as a line, not a loop", False,
                 "It is drawn as a loop precisely because the final review improves the first phase."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "The most valuable thing a non-technical person brings to an incident is:",
            "options": [
                ("A calm head and a known set of first moves", True,
                 "Yes. Recognise, contain, report and follow the plan. That calm, prepared response is the vital first contribution."),
                ("The ability to personally rewrite the software", False,
                 "That is not needed, and not the point. Calm, correct first moves matter most."),
                ("A willingness to pay the ransom fast", False,
                 "Paying is never the goal. Calm, prepared action is the valuable contribution."),
                ("Keeping quiet about what happened", False,
                 "Silence harms the response. Recognising, containing and reporting is what helps."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Under sudden stress, people tend to:",
            "options": [
                ("Make poor decisions, which is exactly why a pre-made plan helps", True,
                 "Yes. Stress harms careful thinking, so following steps decided in calm leads to far better outcomes."),
                ("Think more clearly than usual", False,
                 "Stress usually harms clear thinking, which is why a plan made in calm is so valuable."),
                ("Automatically know the right thing to do", False,
                 "Rarely. Without a plan, people reach for whatever feels like relief, often the wrong move."),
                ("Become immune to mistakes", False,
                 "The opposite. Stress makes mistakes more likely, so a plan matters."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A laminated page by the office kitchen listing 'disconnect, phone this number, delete nothing' is an example of:",
            "options": [
                ("Preparation, the first phase of the lifecycle", True,
                 "Yes. Simple, in-advance readiness like this is exactly what Preparation means, and it works under pressure."),
                ("Recovery", False,
                 "Recovery is restoring systems after the threat is gone. This page is Preparation, made in advance."),
                ("Eradication", False,
                 "Eradication removes the threat. A first-steps page prepared beforehand is Preparation."),
                ("A waste of time", False,
                 "Far from it. A simple plan people can follow under stress is one of the most useful things a business can have."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Incidents, for organisations of every size, are best thought of as:",
            "options": [
                ("A 'when', not an 'if', so being ready matters", True,
                 "Yes. Because incidents happen to everyone eventually, the businesses that cope are the ones that prepared."),
                ("An 'if' that only happens to big companies", False,
                 "Attacks are largely automated and hit organisations of every size. Being small is not being safe."),
                ("Impossible, if you have a firewall", False,
                 "No single control prevents every incident. Preparation for when one happens still matters."),
                ("Not worth preparing for", False,
                 "Preparation is what separates a bad afternoon from a disaster. It is very much worth it."),
            ],
        },
        # ---- Lesson 2: identification and containment ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What does the 'Identification' phase involve?",
            "options": [
                ("Recognising that a security incident is happening, and raising it quickly", True,
                 "Yes. Noticing the warning signs, deciding it is an incident, and reporting it while it is still small."),
                ("Removing the malware from every machine", False,
                 "That is Eradication, a later phase. Identification is noticing the incident."),
                ("Writing the response plan", False,
                 "That is Preparation, done in advance. Identification is recognising an incident as it happens."),
                ("Restoring files from a backup", False,
                 "That is Recovery. Identification comes first: noticing something is wrong."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Why report a suspected incident quickly, even if you are not certain?",
            "options": [
                ("An incident caught early, while small, is far easier to handle than one left to spread", True,
                 "Yes. A false alarm costs minutes; a missed incident can cost the business. Raise it early."),
                ("So someone else can be blamed", False,
                 "Blame is not the goal. Early reporting is about limiting the damage."),
                ("Because reporting is required by law for every glitch", False,
                 "Not every glitch. You report because early action keeps a real incident small."),
                ("There is no reason to report early", False,
                 "There is a strong reason. Early reporting keeps a problem manageable."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "During triage, which question matters most for possible legal duties later?",
            "options": [
                ("Was personal information about people exposed?", True,
                 "Yes. If people's data may have been taken, the incident can carry a legal duty to notify."),
                ("What time did it start?", False,
                 "Timing is minor. Whether personal information was exposed is what carries legal weight."),
                ("Which brand of computer was affected?", False,
                 "The make of device is not the point. Exposure of personal data is."),
                ("How fast is the internet?", False,
                 "Speed is irrelevant. The key question is whether personal information was exposed."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "The purpose of sizing up, or triaging, an incident is to:",
            "options": [
                ("Match your response to the real scale, and see who else needs to know", True,
                 "Yes. A rough read of what is affected and whether data was exposed guides how hard to push and who to involve."),
                ("Decide who to blame", False,
                 "Blame is not the goal. Triage is about scale, not fault."),
                ("Make the incident look smaller", False,
                 "Honesty is the point. Triage gives an accurate read, not a comforting one."),
                ("Delay taking action", False,
                 "The opposite. A quick size-up speeds the right response."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "For most people, the key containment action when a device is compromised is to:",
            "options": [
                ("Disconnect it from the network, by cable or Wi-Fi", True,
                 "Yes. That stops malware spreading and cuts off an attacker, without destroying evidence."),
                ("Immediately wipe and reinstall it yourself", False,
                 "That destroys evidence and may miss other machines. Isolate, do not obliterate."),
                ("Keep using it so you do not lose work", False,
                 "That lets the incident spread. Disconnect first."),
                ("Turn off the whole office internet for a week", False,
                 "Heavy-handed and rarely needed. Isolating the affected device is the targeted move."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Why isolate a compromised machine but not immediately wipe it?",
            "options": [
                ("Wiping destroys evidence of what happened, including whether data was taken, and may miss other machines", True,
                 "Yes. Isolate to stop the spread, but preserve the machine so responders can understand the incident."),
                ("Wiping is too slow to be worth it", False,
                 "Speed is not the issue. Wiping destroys the evidence you need, so isolate instead."),
                ("There is no difference between the two", False,
                 "There is a big difference. Disconnecting contains safely; wiping erases crucial evidence."),
                ("Wiping makes the incident spread faster", False,
                 "The problem with wiping is lost evidence, not spread. Disconnecting is what contains the spread."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why should you not quietly clean up a compromised machine by yourself?",
            "options": [
                ("It destroys evidence and often misses the full extent, like a second infected machine", True,
                 "Yes. A panicked solo clean-up erases what responders need and can leave the real problem active."),
                ("It uses too much electricity", False,
                 "Power use is not the concern. Lost evidence and a missed problem are."),
                ("Cleaning up alone is perfectly fine", False,
                 "It is not. It destroys evidence and often leaves part of the incident unresolved."),
                ("It voids the computer's warranty", False,
                 "That is not the issue. The harm is lost evidence and an incompletely resolved incident."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Which is a sound first-minutes response to an incident?",
            "options": [
                ("Disconnect the device, report it, and note what you saw", True,
                 "Yes. Contain the spread, get the right people involved, and preserve useful detail."),
                ("Keep working and tell no one", False,
                 "That lets it spread and delays the response. Disconnect and report."),
                ("Wipe the machine before anyone looks", False,
                 "That destroys evidence. Isolate and report instead."),
                ("Pay the ransom quietly", False,
                 "Paying is unreliable, funds crime, and hiding it prevents a proper response."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Containment in incident response is best summed up as:",
            "options": [
                ("Stopping the incident from spreading any further", True,
                 "Yes. It limits the damage to what has already happened, most often by isolating the affected device."),
                ("Removing the threat completely", False,
                 "That is Eradication, a later phase. Containment stops the spread first."),
                ("Restoring everything to normal", False,
                 "That is Recovery. Containment comes earlier, halting the spread."),
                ("Writing a report for the regulator", False,
                 "Notification is separate. Containment is the urgent act of stopping the spread."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Which of these is a warning sign that an incident may be under way?",
            "options": [
                ("Colleagues receiving strange messages from your account that you never sent", True,
                 "Yes. That strongly suggests your account or device is compromised, and it should be raised straight away."),
                ("Your computer working exactly as it always does", False,
                 "That is reassuring, not a warning sign. Identification is about noticing unexpected changes."),
                ("Receiving an expected email from a known colleague", False,
                 "That is normal activity, not a sign of an incident."),
                ("The office being quiet on a public holiday", False,
                 "That has nothing to do with a security incident. Watch for unexplained changes like spam sent in your name."),
            ],
        },
        # ---- Lesson 3: eradication, recovery, lessons learned ----
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Eradication removes the threat, but which crucial second part is often missed?",
            "options": [
                ("Closing the hole it came through, or the threat simply returns", True,
                 "Yes. Patch the flaw, reset the phished password, lock the account. Otherwise the attacker returns the same way."),
                ("Buying a faster computer", False,
                 "New hardware does not close the entry point. You must fix the flaw or account that let it in."),
                ("Telling no one it happened", False,
                 "Silence is not eradication, and usually harmful. The missed part is closing the entry point."),
                ("Paying the attacker to remove it", False,
                 "Never. You remove the threat and close the hole yourself."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What does the Recovery phase mainly involve?",
            "options": [
                ("Restoring systems and data from clean backups, then verifying and watching them", True,
                 "Yes. Recovery brings you back to normal safely, using trusted backups and watching for the threat's return."),
                ("Removing the malware from machines", False,
                 "That is Eradication, the phase before. Recovery restores normal operations after the threat is gone."),
                ("Deciding whether an incident is happening", False,
                 "That is Identification. Recovery restores systems once the threat is removed."),
                ("Paying to get files back", False,
                 "No. Recovery uses your own clean backups, which is how you avoid paying."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "When recovering from ransomware, which backup should you restore from?",
            "options": [
                ("A clean backup taken before the infection", True,
                 "Yes. A backup from before the incident is free of the malware. A later, infected copy just brings it back."),
                ("The most recent backup, even if taken after the infection", False,
                 "A backup taken after infection may contain the malware. Restore from a clean, earlier point."),
                ("Any backup, timing does not matter", False,
                 "Timing matters a great deal. An infected backup reintroduces the threat."),
                ("No backup, recovery never uses them", False,
                 "Backups are exactly what recovery relies on, choosing a clean one from before the incident."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why should recovery be patient rather than rushed?",
            "options": [
                ("The incident is not over until systems are verified, watched, and confirmed clean", True,
                 "Yes. Declaring victory too early can turn a half-finished response into a second incident."),
                ("Rushing uses more electricity", False,
                 "Power is not the issue. The risk is an unverified, possibly still-infected recovery."),
                ("There is no reason, faster is always better", False,
                 "Faster is not always better here. A rushed recovery can reintroduce the threat."),
                ("Because backups take days to load", False,
                 "The point is verification and watchfulness, not load times."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "After an incident where passwords may have been exposed, you should:",
            "options": [
                ("Reset the affected passwords and turn on multi-factor authentication", True,
                 "Yes. Change any password an attacker may hold, and add a second factor so a stolen one is no longer enough."),
                ("Keep the same passwords to avoid confusion", False,
                 "That leaves the attacker's copied keys working. Reset anything that may have been exposed."),
                ("Only change them if you are completely certain they were stolen", False,
                 "If there is any real chance, reset them. Waiting for certainty leaves the door open."),
                ("Write the new passwords on a shared note", False,
                 "Never. Use a password manager and keep them private."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "What makes a 'Lessons Learned' review effective?",
            "options": [
                ("A blameless look at what happened, feeding concrete improvements back into preparation", True,
                 "Yes. Without blame, people stay honest, and the findings become real changes that prevent the next incident."),
                ("Identifying who to punish", False,
                 "Blame makes people hide the truth, losing the lessons. The goal is a better system, not a scapegoat."),
                ("Agreeing never to speak of it again", False,
                 "Silence throws away the lesson. A review exists to learn from what happened."),
                ("Deciding it was nobody's concern", False,
                 "The point is to improve, turning the episode into concrete changes."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "Why must a post-incident review be blameless?",
            "options": [
                ("If it is about punishment, people hide the truth and you lose the information that prevents the next incident", True,
                 "Yes. Honesty is what makes a review useful, and blame destroys honesty."),
                ("Because blame is against the law", False,
                 "It is not a legal rule. It is that blame makes people conceal the facts you need."),
                ("So the review can be kept secret", False,
                 "The point is not secrecy. It is that a blameless tone keeps people honest."),
                ("Because reviews never find anything useful", False,
                 "Reviews find plenty, when people feel safe to be honest. That is why they must be blameless."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "'Restore files from a clean backup, then verify systems and watch for reinfection' belongs to which phase?",
            "options": [
                ("Recovery", True,
                 "Yes. Bringing systems back safely, verified and watched, is Recovery."),
                ("Eradication", False,
                 "Eradication removes the threat and closes the hole. Restoring from backup is Recovery."),
                ("Identification", False,
                 "Identification is noticing the incident. Restoring systems is Recovery."),
                ("Preparation", False,
                 "Preparation is the work done in advance. Restoring after an incident is Recovery."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "'Update the plan so the same gap cannot be used again' belongs to which phase?",
            "options": [
                ("Lessons Learned", True,
                 "Yes. Turning findings into improvements is Lessons Learned, which loops back to Preparation."),
                ("Containment", False,
                 "Containment stops the spread during the incident. Improving the plan afterward is Lessons Learned."),
                ("Recovery", False,
                 "Recovery restores systems. Updating the plan to prevent recurrence is Lessons Learned."),
                ("Identification", False,
                 "Identification is noticing the incident. Improving from it afterward is Lessons Learned."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "The findings of a Lessons Learned review feed back into which phase, completing the loop?",
            "options": [
                ("Preparation, so you are better ready for next time", True,
                 "Yes. That is why the lifecycle is a cycle: what you learn improves how prepared you are for the next incident."),
                ("Containment, so the current incident stops", False,
                 "Containment happens during the incident. The review's findings improve future Preparation."),
                ("Identification, so you notice faster", False,
                 "Better preparation can help you notice faster, but the findings feed back into Preparation, which the loop returns to."),
                ("Nowhere, the review is just a formality", False,
                 "It is far from a formality. Its findings become real improvements to your preparation."),
            ],
        },
        # ---- Lesson 4: the law and the whole response ----
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What does the Notifiable Data Breaches scheme, under the Privacy Act, require?",
            "options": [
                ("Telling affected people and the regulator when a breach is likely to cause serious harm", True,
                 "Yes. It turns fairness into a duty: notify those affected and the OAIC when a breach could seriously harm people."),
                ("Paying a fine for every incident", False,
                 "No. The scheme is about notifying serious breaches, not automatic fines."),
                ("Keeping all breaches secret", False,
                 "The opposite. People have a right to be told about serious breaches."),
                ("Reporting only if the breach makes the news", False,
                 "The trigger is likely serious harm, not media attention."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What makes a data breach 'notifiable' under the scheme?",
            "options": [
                ("It is likely to result in serious harm to the affected individuals", True,
                 "Yes. The trigger is likely serious harm, such as identity theft or financial loss, not the size or fame of the breach."),
                ("Any breach at all, however minor", False,
                 "Not every minor slip clears the bar. The test is likely serious harm."),
                ("Only breaches that make the news", False,
                 "Media attention is irrelevant. The test is likely serious harm to people."),
                ("Only breaches at government agencies", False,
                 "Many businesses are covered too, including small health providers. The test is likely serious harm."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Under the scheme, who must be told about an eligible data breach?",
            "options": [
                ("The affected individuals and the OAIC", True,
                 "Yes. Those whose data was exposed, and the Office of the Australian Information Commissioner, the regulator."),
                ("Only your own staff", False,
                 "Not enough. The affected individuals and the OAIC must be notified."),
                ("Nobody, as long as you fix it quietly", False,
                 "Hiding an eligible breach is exactly what the scheme forbids."),
                ("Only your bank", False,
                 "Your bank is not the requirement. Notify the affected individuals and the OAIC."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "How quickly must an eligible data breach be notified?",
            "options": [
                ("As soon as practicable, with up to 30 days to assess if you are genuinely unsure", True,
                 "Yes. You move as fast as you reasonably can; the 30 days to assess is a limit, not a target."),
                ("Within exactly one year, no sooner", False,
                 "Far too slow. It must be as soon as practicable after you become aware."),
                ("Only if the affected people ask you", False,
                 "The duty does not wait to be asked. You must notify as soon as practicable."),
                ("There is no time requirement at all", False,
                 "There is: as soon as practicable, with a limited assessment period if unsure."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Which of these is most likely a notifiable, eligible data breach?",
            "options": [
                ("An attacker takes a database of customers' identity documents", True,
                 "Yes. That exposure is likely to cause serious harm, such as identity theft, so it is very likely notifiable."),
                ("An internal email sent to the wrong colleague and deleted straight away", False,
                 "That is probably not notifiable, as it is unlikely to cause serious harm. The identity-document theft is."),
                ("A staff member forgetting their own password", False,
                 "That is not a breach of others' data at all. The identity-document theft is the notifiable one."),
                ("The office printer running out of ink", False,
                 "That is not a data breach. The theft of identity documents is the notifiable event."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Are small businesses ever covered by the breach notification duty?",
            "options": [
                ("Yes, many are, and health service providers of any size are covered regardless of turnover", True,
                 "Yes. The 'we are too small' assumption is dangerous. Small health providers in particular are covered."),
                ("No, only companies with thousands of staff", False,
                 "Many smaller organisations are covered, and small health providers are covered regardless of size."),
                ("No, the scheme does not exist for businesses", False,
                 "It very much applies to businesses, including many small ones."),
                ("Only overseas businesses are covered", False,
                 "It applies to Australian organisations, including many small ones."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "In the ransomware morning, what is the correct first move when files start locking?",
            "options": [
                ("Disconnect the PC from the network to contain the spread", True,
                 "Yes. Containment first: get it off the network before the ransomware reaches shared drives and other machines."),
                ("Keep clicking to try to save open files", False,
                 "That lets it spread further. Disconnect first to contain it."),
                ("Pay the ransom immediately", False,
                 "Not the first move, and often unnecessary. Contain, then report and recover from backup."),
                ("Wipe the machine straight away", False,
                 "That destroys evidence. Disconnect to contain, and preserve the machine."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "In the scenario, the clinic has a clean, tested backup and the attacker demands payment. The right call is to:",
            "options": [
                ("Restore from the clean backup and not pay", True,
                 "Yes. A clean backup lets you recover without funding criminals or gambling on a decryption key."),
                ("Pay the ransom to save time", False,
                 "Paying is unreliable and funds crime. With a tested backup there is no need to consider it."),
                ("Do nothing and hope it resolves", False,
                 "Inaction leaves you locked out. Recover from the clean backup."),
                ("Delete the backup to be safe", False,
                 "Never delete a clean backup. It is exactly what lets you recover."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "During recovery, the clinic finds patient records were taken. Restoring the files means:",
            "options": [
                ("The data exposure still happened, so an eligible breach must still be notified", True,
                 "Yes. Restoring files does not undo the exposure. A breach likely to cause serious harm must be notified."),
                ("Nothing more to do, since the files are back", False,
                 "Restoring the files does not undo that the data was exposed. Notification is still required."),
                ("Notification is no longer needed", False,
                 "Recovery of files does not remove the duty. The exposure of personal data still triggers it."),
                ("The breach can be kept secret", False,
                 "An eligible breach must be notified. Restoring the files does not change that."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "Across all six modules, the throughline of incident response is that:",
            "options": [
                ("A calm, prepared response, following a plan, beats panic every time", True,
                 "Yes. You do not need to be the technical expert. Recognise, contain, report, recover, notify and review, calmly."),
                ("Only technical experts can do anything useful", False,
                 "The most valuable first response often comes from a calm, prepared non-technical person."),
                ("Paying attackers is the simplest solution", False,
                 "Paying is unreliable and funds crime. A prepared response and clean backups are the answer."),
                ("Incidents should be kept secret", False,
                 "Good response is honest and prompt, including notifying serious breaches as the law requires."),
            ],
        },
    ],
}
