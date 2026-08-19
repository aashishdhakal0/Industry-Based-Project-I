"""Module 2, Recognising Cyber Threats: two DEEP lessons.

Deliberately two lessons, not four, each carrying the weight of the old pairs so
the learner goes deeper rather than wider:

  Lesson 1  Know the threats: malware, and how it gets in
            (the malware family: virus, worm, trojan, spyware, ransomware; and
            the everyday routes it uses to reach a small business)
  Lesson 2  When it goes wrong: ransomware, breaches, and reacting
            (ransomware across a whole business, the real Australian breaches
            Optus and Medibank, and how to recognise and react calmly)

Same standard as Module 1, but HANDS-ON throughout: every panel is a practical
exercise, not reading-then-MCQ. Each lesson is a scrollable room of five PANELS,
and the teaching happens THROUGH the interaction (per-item feedback), not before
it. Task 3 stays a picture-question CHECK; the rest are drills:

  Lesson 1 (malware, and how it gets in)
    1 Learn by doing   SORT      sort real behaviours to their malware type
    2 Decision drill   BRANCH    a connected "what do you do next" scenario
    3 Picture-question CHECK     read the fake-update pop-up (unchanged)
    4 Simulated inbox  MAILSORT  triage a mixed inbox, genuine vs malicious
    5 Tabletop         BRANCH    a mini-incident, 2 to 3 connected decisions
  Lesson 2 (ransomware, breaches, reacting)
    1 Learn by doing   CLASSIFY  diagnose each scenario: ransomware/breach/glitch
    2 Decision drill   BRANCH    a ransom-note-on-screen scenario
    3 Picture-question CHECK     read the ransom screen (unchanged)
    4 Order the steps  SEQUENCE  put the incident-response steps in order
    5 Tabletop         BRANCH    a breach mini-incident to resolve

Points sum to 10 per lesson (2 each) and bank at lesson end. Voice: warm,
confident, human, plain Australian English. No em-dashes, no emoji, no filler.
The real cases (Optus and Medibank, both 2022) are presented as widely-reported
factual scenarios for teaching, framed evenly and without blame.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Activity payload contracts
(mirroring static/js/activities.js): SORT {prompt, buckets:[{id,label}],
items:[{text,bucket,why}]}; CLASSIFY {prompt, categories:[{id,label}],
events:[{text,category,why}]}; BRANCH {prompt, start, nodes:{id:{text,
choices:[{label,outcome,feedback,to}]}}} (an ending node has no choices);
SEQUENCE {prompt, steps:[{label,detail,order}]}; MAILSORT {prompt,
emails:[{from,subject,preview,phish,why}]}. Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "Know the threats: malware, and how it gets in",
        "reading_time_minutes": 9,
        "intro": "Malware is not one thing, it is a family. Meet each member, "
        "learn what makes it dangerous, and train your eye on the everyday ways "
        "it slips into a small business.",
        "tasks": [
            {
                "key": "malware-family",
                "kind": "sort",
                "points": 2,
                "title": "Sort the behaviour to its malware type",
                "diagram": "malware-family",
                "body": "<p><strong>Malware</strong> means malicious software: any "
                "program built to do harm. People say virus for all of it, but a "
                "virus is only one member of a whole family, and each member "
                "behaves differently. Knowing them apart matters, because what "
                "stops one does little against another. The fastest way to learn "
                "the family is to sort real behaviours to the member that fits.</p>"
                "<div class=\"cy-callout\">Read each behaviour, then tap it and tap "
                "the malware type it belongs to. The tell is in HOW it behaves: "
                "does it spread itself, wait for a click, wear a disguise, hide and "
                "watch, or lock and demand?</div>",
                "payload": {
                    "prompt": "Tap a behaviour, then tap the malware type it belongs to. Sort all six to finish.",
                    "buckets": [
                        {"id": "virus", "label": "Virus"},
                        {"id": "worm", "label": "Worm"},
                        {"id": "trojan", "label": "Trojan"},
                        {"id": "spyware", "label": "Spyware"},
                        {"id": "ransomware", "label": "Ransomware"},
                    ],
                    "items": [
                        {"text": "Hides inside a file and only spreads when a person opens it", "bucket": "virus",
                         "why": "That is a virus. It needs a human to open the infected file before it can do anything or spread."},
                        {"text": "Copies itself from machine to machine across the network, no clicks needed", "bucket": "worm",
                         "why": "That is a worm. Spreading by itself with no human action is exactly what lets it move so fast."},
                        {"text": "Disguised as a free copy of paid software you install yourself", "bucket": "trojan",
                         "why": "That is a trojan. You let it in because it looks legitimate, and then it does its real work."},
                        {"text": "Quietly records the passwords you type and sends them to an attacker", "bucket": "spyware",
                         "why": "That is spyware. It stays hidden and steals information rather than announcing itself."},
                        {"text": "Locks every file and shows a demand for payment to unlock them", "bucket": "ransomware",
                         "why": "That is ransomware. It makes itself very much known, holding your files hostage for money."},
                        {"text": "Spreads to every USB stick and shared drive on its own", "bucket": "worm",
                         "why": "Still a worm. Self-copying to other drives and machines with no help is the worm's signature."},
                    ],
                },
            },
            {
                "key": "delivery-respond",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: the call, then the car park",
                "diagram": "download-trap",
                "body": "<p>Malware almost never appears on its own. Someone has to "
                "let it in, usually a person tricked in a busy moment. One of the "
                "commonest tricks is the fake download above: a page dresses up an "
                "advertisement as a big Download button, hoping you tap it instead "
                "of the real link. Read the page first, then work through the "
                "decision drill below, choosing your move and seeing the "
                "consequence each time.</p>"
                "<div class=\"cy-callout\"><strong>The habit to build:</strong> "
                "before you act on anything unexpected, pause and ask where it "
                "really came from. Verify first, share nothing, plug in nothing.</div>",
                "inline_check": {
                    "question": "Looking at the download page above, which is the real download, and how can you tell?",
                    "hint": "One is an advertisement dressed up as a button. Which one names the actual file?",
                    "options": [
                        ("The small plain text link report_2026.pdf, because it names the actual file you asked for", True,
                         "Right. The real download is the modest link that matches the file name. The giant green button is tagged Ad and Recommended, which is how ads disguise themselves as downloads."),
                        ("The big green Download Now button, because it is the most obvious one", False,
                         "That is the trap. Being big and green is exactly the disguise. It is tagged Ad, and tapping it downloads something you did not ask for."),
                        ("Both are the same, so either is fine", False,
                         "They are not the same. One is the file you wanted; the other is an advertisement that can deliver malware. Use the plain link."),
                        ("Neither, you should never download anything", False,
                         "Downloading the file you actually came for, from the real link, is fine. The skill is telling the real link from the ad."),
                    ],
                },
                "payload": {
                    "prompt": "Read each moment, choose what you do, and see how it plays out.",
                    "start": "call",
                    "nodes": {
                        "call": {
                            "text": "It is a busy Tuesday. The phone rings. A calm voice says they are from IT support, there is an urgent problem with your account, and they just need your password to fix it before it locks.",
                            "choices": [
                                {"label": "Do not give it out. Hang up and call your real IT contact on a number you already have.", "outcome": "good",
                                 "feedback": "Right. Real IT never needs your password. Verifying on a number you already trust shuts the trick down cold.", "to": "carpark"},
                                {"label": "Read out your password so the urgent problem gets fixed.", "outcome": "bad",
                                 "feedback": "That hands your account straight to an attacker. No genuine IT process ever asks you to read out your password.", "to": "call_bad"},
                                {"label": "Give them a slightly different password, just to be safe.", "outcome": "bad",
                                 "feedback": "Any password you share is a password you have lost. There is no safe version of handing one over.", "to": "call_bad"},
                            ],
                        },
                        "call_bad": {
                            "text": "Within the hour, logins from overseas appear on your account and colleagues receive odd emails 'from you'. The password was the only key the caller needed. The lesson: verify first, share nothing.",
                            "choices": [],
                        },
                        "carpark": {
                            "text": "Later that afternoon, you find a USB stick in the car park. The sticker reads Payroll 2026.",
                            "choices": [
                                {"label": "Do not plug it in. Hand it to IT or your manager.", "outcome": "good",
                                 "feedback": "Yes. A tempting label on a dropped USB is bait, not a lost item. Handing it in is exactly right.", "to": "win"},
                                {"label": "Plug it in to see whose it is so you can return it.", "outcome": "bad",
                                 "feedback": "That is what the attacker is counting on. It can infect your machine the moment it connects.", "to": "carpark_bad"},
                                {"label": "Take it home and check it on your own laptop.", "outcome": "bad",
                                 "feedback": "Same trap, different computer. Do not connect an unknown USB to any machine.", "to": "carpark_bad"},
                            ],
                        },
                        "carpark_bad": {
                            "text": "The moment it connects, it quietly installs malware in the background. A dropped USB with a tempting label is a classic delivery trick. Hand unknown USBs to IT, and never plug them in.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Two classic tricks, both stopped: you verified the caller and refused the bait. That instinct, pause and check before you act, is what keeps malware out in the real world.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "fake-update-check",
                "kind": "check",
                "points": 2,
                "title": "Read the pop-up like an investigator",
                "diagram": "fake-update",
                "body": "<p>Here is one of the most common delivery routes, up "
                "close. The pop-up above appeared while browsing a random "
                "streaming site. It looks official and it is in a hurry. Read it "
                "the way an investigator would, starting with where it actually "
                "came from and what it is really asking you to do.</p>"
                "<div class=\"cy-callout\">Two things give it away every time: a "
                "genuine update never arrives as a pop-up on an unrelated "
                "website, and real software does not put a countdown on your "
                "safety to rush you into downloading.</div>",
                "question": "Looking at this pop-up, what is the strongest sign it is malware, not a real update?",
                "hint": "Where did it come from, and how is it pressuring you?",
                "options": [
                    ("It appears on a random streaming site and rushes you to download, which is not how real updates work", True,
                     "Right. The address is free-hd-movies-stream.info, nothing to do with any software maker, and it uses a countdown to rush you. Genuine updates come from the software itself or an app store, calmly."),
                    ("It mentions Flash Player", False,
                     "The name it borrows is not the tell. The giveaway is that it appears on an unrelated website and pressures you to download now."),
                    ("It has a Not now option", False,
                     "An option to dismiss it is not what makes it fake. The tell is the unrelated site and the rushed download."),
                    ("It is written in English", False,
                     "The language means nothing. The real signs are the unrelated website and the countdown pushing you to download."),
                ],
            },
            {
                "key": "malware-quizset",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the inbox",
                "diagram": "attachment-exe",
                "body": "<p>Before you triage the whole inbox, look closely at the "
                "one email above and its attachment. The file name hides the real "
                "trick. Answer the quick check on it, then sort the mixed morning "
                "inbox below: some messages are genuine, and some are carrying "
                "malware or trying to trick you into installing it. Read the "
                "sender, the subject and the preview, then mark each Genuine or "
                "Phishing. The verdict and the tell are revealed as you go.</p>"
                "<div class=\"cy-callout\">The tells to weigh: is it expected, who "
                "is it really from, is it rushing you, and is it pushing an "
                "attachment, a link or an Enable content prompt?</div>",
                "inline_check": {
                    "question": "Look at the attachment on the email above. What is wrong with it?",
                    "hint": "Read the file name to the very end. How many extensions does it have?",
                    "options": [
                        ("It has a double extension, .pdf.exe, so it is actually a program pretending to be a PDF", True,
                         "Right. The real type is the last extension: .exe means a program that runs code. The .pdf in the middle is padding to make it look like a harmless document. Do not open it."),
                        ("Nothing, it is a normal PDF invoice", False,
                         "Look again at the very end of the name: .pdf.exe. The final .exe makes it a program, not a PDF. That is the disguise."),
                        ("The file is too small to be real", False,
                         "Size is not the tell. The problem is the double extension: .pdf.exe is a program dressed up as a document."),
                        ("It should have been sent as a link instead", False,
                         "The delivery method is not the issue. The issue is that .pdf.exe is an executable disguised as a PDF."),
                    ],
                },
                "payload": {
                    "prompt": "Mark each message Genuine or Phishing. Sort all five to finish.",
                    "emails": [
                        {"from": "IT Helpdesk <help@yourclinic.com.au>",
                         "subject": "Planned maintenance this Saturday, 7am",
                         "preview": "The email system will be briefly offline for updates. No action needed from you.",
                         "phish": False,
                         "why": "An expected notice from your real internal helpdesk, on your own domain, asking nothing of you."},
                        {"from": "Accounts <billing@invoices-au-secure.net>",
                         "subject": "OVERDUE invoice, open attached to avoid late fees",
                         "preview": "Your payment is overdue. Open the attached Invoice.zip within 24 hours or fees apply.",
                         "phish": True,
                         "why": "An unexpected, urgent demand with a .zip attachment from a lookalike sender. Opening it can install malware."},
                        {"from": "Microsoft 365 <no-reply@m365-mailcheck.com>",
                         "subject": "Your mailbox is full, log in to keep access",
                         "preview": "Verify your account through the link below or lose access within the hour.",
                         "phish": True,
                         "why": "A manufactured deadline pushing you to a login link. Reach the service the way you normally do, never through the link."},
                        {"from": "Priya (Reception)",
                         "subject": "Team lunch Friday, who is in?",
                         "preview": "Booking a table at the cafe on the corner. Reply if you can make it.",
                         "phish": False,
                         "why": "A normal, expected message from a colleague you know, with no link, no attachment and no pressure."},
                        {"from": "Payroll <hr@yourclinic-payroll.com>",
                         "subject": "Update your bank details, enable macros to view",
                         "preview": "Open the attached form and click Enable content to update where your pay goes.",
                         "phish": True,
                         "why": "The Enable macros trick from a lookalike payroll domain. Enabling content can run hidden malware."},
                    ],
                },
            },
            {
                "key": "malware-applied",
                "kind": "branch",
                "points": 2,
                "title": "Tabletop: a bad Monday morning",
                "body": "<p>Now put it all together. This is a tabletop exercise, "
                "the kind real teams run: a situation unfolds, and you make a few "
                "connected decisions to steer it to a good outcome. There is no "
                "reading first, you learn by handling it. Work through to the end "
                "and see how your calls play out.</p>"
                "<div class=\"cy-callout\">Everything you need is from this lesson: "
                "spot the trick, do not feed it, and when someone has already been "
                "caught, contain it and report it fast.</div>",
                "payload": {
                    "prompt": "Handle the morning as it unfolds. Make each call and see the consequence.",
                    "start": "morning",
                    "nodes": {
                        "morning": {
                            "text": "It is 9am. Three staff have each forwarded you the same email: a courier 'missed delivery' notice with a link to reschedule. None of them was expecting a parcel. What is your first move?",
                            "choices": [
                                {"label": "Warn everyone not to click it, and report it to whoever looks after IT.", "outcome": "good",
                                 "feedback": "Right. A quick, calm warning plus a report stops it spreading while it is still small.", "to": "clicked"},
                                {"label": "Delete your own copy and assume the others will sort themselves out.", "outcome": "bad",
                                 "feedback": "Deleting your copy changes nothing for everyone else. Silence lets the trick keep working.", "to": "ignored_bad"},
                                {"label": "Click the link yourself to see where it goes.", "outcome": "bad",
                                 "feedback": "Probing a suspicious link just risks one more infected machine. Report it, do not test it.", "to": "clicked_self_bad"},
                            ],
                        },
                        "ignored_bad": {
                            "text": "By lunchtime two more staff have clicked the link and entered their logins on a fake page. A quick warning and a report would have stopped it. Speaking up early is the whole game.",
                            "choices": [],
                        },
                        "clicked_self_bad": {
                            "text": "The link loads a convincing fake page and a quiet background download. Testing a suspicious link yourself just adds one more infected machine to the problem. Report it, do not probe it.",
                            "choices": [],
                        },
                        "clicked": {
                            "text": "Good: staff are warned and IT is looped in. Then one colleague admits they already clicked the link and typed their password before your warning went out. What now?",
                            "choices": [
                                {"label": "Have them disconnect that machine, change the password, turn on two-factor, and report which account.", "outcome": "good",
                                 "feedback": "Exactly. Contain the one machine, lock the account down, and report it so the right people can watch for misuse.", "to": "win"},
                                {"label": "Tell them to keep quiet so nobody gets in trouble.", "outcome": "bad",
                                 "feedback": "Staying quiet lets the attacker use that password freely. Early, blame-free reporting is what limits the damage.", "to": "quiet_bad"},
                                {"label": "Tell them it is probably fine since the office looks normal.", "outcome": "bad",
                                 "feedback": "A compromise is often invisible on your own screen while an attacker is already busy. Do not wait and see.", "to": "quiet_bad"},
                            ],
                        },
                        "quiet_bad": {
                            "text": "Overnight the stolen password is used, and odd emails 'from your colleague' go out to clients, spreading the trick further. Early, blame-free reporting would have contained it in minutes.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Handled: warned early, reported fast, and contained the one click before it spread. That calm, contain-then-report response is exactly how a small business rides out a bad morning.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
    {
        "title": "When it goes wrong: ransomware, breaches, and reacting",
        "reading_time_minutes": 9,
        "intro": "Some attacks hit the whole business at once. See how ransomware "
        "and the real Australian breaches played out, then learn the calm, "
        "practical way to recognise trouble and react.",
        "tasks": [
            {
                "key": "ransomware-and-breaches",
                "kind": "classify",
                "points": 2,
                "title": "Diagnose the trouble: ransomware, breach, or glitch",
                "diagram": "data-breach",
                "body": "<p>Two kinds of trouble can strike a whole organisation "
                "at once, and they fail in opposite ways. <strong>Ransomware</strong> "
                "encrypts your files and demands payment to unlock them. It "
                "attacks <strong>availability</strong>: your files are still "
                "there, unchanged, you just cannot reach them, and if it locks a "
                "shared drive, every person in the business is stopped at once. A "
                "<strong>data breach</strong> is the opposite failure. Nothing is "
                "locked, but private information is copied and exposed to people "
                "who should not have it, which is a failure of "
                "<strong>confidentiality</strong>. Once data is out, it cannot be "
                "recalled.</p>"
                "<p>Australia saw both in 2022. In the <strong>Optus</strong> "
                "breach, information on roughly 9.8 million current and former "
                "customers was exposed, reportedly through an access point to "
                "customer data that was reachable over the internet without a "
                "login. For some people it included identity document numbers, "
                "the raw material for identity theft. In the "
                "<strong>Medibank</strong> breach, attackers got in using a "
                "stolen login and took sensitive health claims data. Medibank "
                "chose not to pay the ransom, and the attackers published the "
                "stolen data, a stark reminder that once sensitive data is taken "
                "there are no good options left.</p>"
                "<div class=\"cy-callout\">Ransomware locks what you have; a "
                "breach leaks what you hold; and plenty of everyday trouble is "
                "just a glitch. Telling them apart is the whole skill. Read each "
                "situation below and diagnose it.</div>",
                "payload": {
                    "prompt": "Read each situation and tap the kind of trouble it is. Diagnose all six to finish.",
                    "categories": [
                        {"id": "ransomware", "label": "Ransomware"},
                        {"id": "breach", "label": "Data breach"},
                        {"id": "glitch", "label": "Ordinary glitch"},
                    ],
                    "events": [
                        {"text": "Every file on the shared drive is renamed with a .locked ending, and a note on screen demands Bitcoin to unlock them.",
                         "category": "ransomware",
                         "why": "Ransomware. Files locked in place plus a payment demand is its signature. Your data is still there, you just cannot reach it."},
                        {"text": "A customer says the personal details they gave you have turned up for sale on a leak site.",
                         "category": "breach",
                         "why": "A data breach. Private information has been exposed to people who should not have it, a failure of confidentiality."},
                        {"text": "The office laptop is running slowly. You check, and the hard drive is almost completely full.",
                         "category": "glitch",
                         "why": "An ordinary glitch. A full drive is a common, harmless cause of slowness, with an everyday fix. Not every problem is an attack."},
                        {"text": "A supplier emails to say their systems were breached, and the login you saved with them may be exposed.",
                         "category": "breach",
                         "why": "A data breach, on their side. Your details are exposed, so change that password anywhere you reused it and turn on two-factor."},
                        {"text": "The office printer keeps dropping off the network and needs a restart most mornings.",
                         "category": "glitch",
                         "why": "An ordinary glitch. Routine equipment trouble with a mundane cause, not a security incident."},
                        {"text": "A staff PC is locked behind a red countdown screen demanding payment to release the files.",
                         "category": "ransomware",
                         "why": "Ransomware. The lock plus the countdown pressure to pay is the tell. Disconnect it, do not pay, report it."},
                    ],
                },
            },
            {
                "key": "react-respond",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: a ransom note takes over your screen",
                "diagram": "locked-files",
                "body": "<p>Reading about ransomware is one thing. The test is what "
                "you do in the moment it happens. First, read the file explorer "
                "above and work out what it is telling you. Then run the decision "
                "drill below: the situation unfolds, you choose your move, and you "
                "see the consequence before the next decision. Your first move "
                "decides how far it spreads and whether you recover cleanly.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> contain it, "
                "report it, and restore from backup. Never lead with the ransom.</div>",
                "inline_check": {
                    "question": "Reading the file explorer above, what has happened here?",
                    "hint": "Look at what has been added to the end of every file name, and the extra file left behind.",
                    "options": [
                        ("Ransomware has encrypted the files: every one is renamed with a .locked ending and a read-me demands payment", True,
                         "Right. A whole folder renamed with the same new ending, plus a READ_ME_TO_UNLOCK file, is the classic ransomware signature. The files are locked in place, not deleted."),
                        ("The files were simply deleted", False,
                         "They are not deleted, they are still listed, just renamed with a .locked ending. That points to ransomware encryption, not deletion."),
                        ("The hard drive is full, so the files were renamed", False,
                         "A full drive does not rename files or leave a ransom read-me. This pattern is ransomware."),
                        ("It is a normal Windows update in progress", False,
                         "Updates do not rename all your documents with a .locked ending or leave an unlock demand. This is ransomware."),
                    ],
                },
                "payload": {
                    "prompt": "The incident unfolds. Make each call and see how it plays out.",
                    "start": "note",
                    "nodes": {
                        "note": {
                            "text": "You are working when your files start renaming one after another, and a red screen takes over: your files are encrypted, pay 0.05 Bitcoin within 72 hours. What is your first move?",
                            "choices": [
                                {"label": "Disconnect the machine from the network straight away.", "outcome": "good",
                                 "feedback": "Exactly. Getting it off the network first stops the ransomware reaching shared drives and other machines.", "to": "contain"},
                                {"label": "Pay the 0.05 Bitcoin quickly so you can get back to work.", "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds crime, and does nothing about the open door. Never lead with the ransom.", "to": "pay_bad"},
                                {"label": "Keep working on what you can and hope it stops.", "outcome": "bad",
                                 "feedback": "Every second it stays connected, more files and machines are locked. The first move is to disconnect.", "to": "work_bad"},
                            ],
                        },
                        "pay_bad": {
                            "text": "You pay, but the files stay locked and the door it came through is still open. Payment is unreliable, funds crime, and marks you as someone who pays. Contain first, never lead with the ransom.",
                            "choices": [],
                        },
                        "work_bad": {
                            "text": "While you carry on, the ransomware reaches the shared drive and two more machines. Every second connected is more damage. The first move is always to disconnect.",
                            "choices": [],
                        },
                        "contain": {
                            "text": "Good: the machine is off the network and the spread is stopped. The screen still demands payment. What next?",
                            "choices": [
                                {"label": "Report it to whoever looks after IT and leave the machine for them.", "outcome": "good",
                                 "feedback": "Right. Reporting gets the right people checking every affected machine, not just the one in front of you.", "to": "restore"},
                                {"label": "Delete the ransom note and quietly try to clean it up yourself.", "outcome": "bad",
                                 "feedback": "Cleaning it alone can destroy evidence and miss other affected machines. Report it so the whole picture gets checked.", "to": "clean_bad"},
                                {"label": "Pay after all, now that it is contained.", "outcome": "bad",
                                 "feedback": "Even contained, paying is the wrong call. With the spread stopped, the answer is report, then restore from backup.", "to": "pay2_bad"},
                            ],
                        },
                        "clean_bad": {
                            "text": "Cleaning it alone destroys useful evidence and misses a second machine that was also hit. Report it so the right people can check the whole picture, not just the one screen.",
                            "choices": [],
                        },
                        "pay2_bad": {
                            "text": "Paying rewards the attacker and still leaves the cause unfixed. With the spread already stopped, the clean answer was to report it and restore from a tested backup.",
                            "choices": [],
                        },
                        "restore": {
                            "text": "Reported. IT confirms last night's backup is clean and tested. How do you get back to work?",
                            "choices": [
                                {"label": "Wipe the machine, then restore the files from the clean backup.", "outcome": "good",
                                 "feedback": "That is the whole point of a backup: it takes away the attacker's leverage entirely. No payment needed.", "to": "win"},
                                {"label": "Pay the ransom to save the hassle of restoring.", "outcome": "bad",
                                 "feedback": "With a clean backup in hand, paying makes no sense at all. Restore, do not pay.", "to": "pay2_bad"},
                                {"label": "Reconnect the infected machine to check if the files came back.", "outcome": "bad",
                                 "feedback": "Reconnecting an infected machine risks spreading it again. Keep it isolated, wipe it, and restore from the clean backup.", "to": "reconnect_bad"},
                            ],
                        },
                        "reconnect_bad": {
                            "text": "Reconnecting the infected machine risks spreading the ransomware all over again. Keep it isolated, wipe it, and restore from the clean backup instead.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Contained, reported, and restored from backup with nothing paid. That is exactly how a business beats ransomware: the backup, not the wallet, is what saves you.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "ransom-screen-check",
                "kind": "check",
                "points": 2,
                "title": "Read the ransom screen",
                "diagram": "ransom-screen",
                "body": "<p>This is what ransomware looks like when it lands. The "
                "screen above took over a staff computer, with every document on "
                "it locked. It is designed to frighten you into paying fast. Read "
                "it calmly and work out what it is really telling you, and what "
                "the sound first move is.</p>"
                "<div class=\"cy-callout\">Notice the countdown. That pressure is "
                "the whole tactic. Your files are locked in place, not stolen, "
                "and a tested backup is what lets you recover without ever "
                "dealing with these people.</div>",
                "question": "Faced with this screen, what is the soundest first move?",
                "hint": "The countdown wants you to rush. What limits the damage right now?",
                "options": [
                    ("Disconnect the machine from the network, then report it so it can be recovered from backup", True,
                     "Right. Getting it off the network first stops the ransomware reaching shared drives and other machines. Then report it, and restore from a clean backup rather than paying."),
                    ("Pay the 0.05 Bitcoin quickly before the countdown ends", False,
                     "That is what the countdown is engineered to make you do. Paying is unreliable, funds crime, and does nothing to close the door it came through."),
                    ("Keep using the computer so you do not lose your work", False,
                     "Carrying on gives it time to lock more files and reach other machines. Disconnect first."),
                    ("Restart the computer and hope the files come back", False,
                     "A restart will not undo the encryption. Disconnect, report, and recover from backup."),
                ],
            },
            {
                "key": "react-quizset",
                "kind": "sequence",
                "points": 2,
                "title": "Put the response in order",
                "body": "<p>Knowing the steps is not enough; the order is what "
                "limits the damage. This is the real incident-response sequence a "
                "small business follows when ransomware hits. The steps below are "
                "shuffled. Tap them into the correct order, one at a time, and the "
                "reasoning for each falls into place as you go.</p>"
                "<div class=\"cy-callout\">Think it through: what has to happen "
                "first to stop the spread, and what can only come once the machine "
                "is safe to trust again?</div>",
                "payload": {
                    "prompt": "Tap the step that comes next, one at a time, until the whole response is in order.",
                    "steps": [
                        {"label": "Disconnect the machine from the network",
                         "detail": "Isolate it first, so the ransomware cannot reach shared drives or other computers.",
                         "order": 1},
                        {"label": "Report it to whoever looks after IT",
                         "detail": "Raise the alarm early and blame-free, so the right people can act while the damage is small.",
                         "order": 2},
                        {"label": "Preserve the evidence, and do not pay",
                         "detail": "Leave the machine and the ransom note for investigation. Paying is unreliable and funds crime.",
                         "order": 3},
                        {"label": "Wipe or rebuild the affected machine",
                         "detail": "Clean the infection off completely rather than trusting a machine that was compromised.",
                         "order": 4},
                        {"label": "Restore the files from a clean backup",
                         "detail": "Bring your work back from a recent, tested backup: the step that beats ransomware without paying.",
                         "order": 5},
                        {"label": "Review what let it in, and close the gap",
                         "detail": "Afterwards, work out how it got in and fix that, so the same door is not open next time.",
                         "order": 6},
                    ],
                },
            },
            {
                "key": "react-applied",
                "kind": "branch",
                "points": 2,
                "title": "Tabletop: your data is on a leak site",
                "diagram": "breach-email",
                "body": "<p>The final exercise brings the whole lesson together. "
                "First, put yourself in a customer's shoes: read the breach "
                "notification above and decide the first thing they should do. "
                "Then take the other side of the desk and run the tabletop "
                "mini-incident below, where the breach lands on your business and "
                "you make a few connected decisions to handle it well.</p>"
                "<div class=\"cy-callout\">Draw on all of it: you cannot recall "
                "leaked data, so verify, report, refuse the follow-up demand, and "
                "help the people affected protect themselves.</div>",
                "inline_check": {
                    "question": "Looking at the breach notice above, what should the customer do first?",
                    "hint": "The notice itself recommends it. What protects the account now that the password may be out?",
                    "options": [
                        ("Reset that password, change it anywhere it was reused, and turn on two-factor authentication", True,
                         "Right. The exposed password is the risk, so change it everywhere it was used and add two-factor, exactly as the notice recommends. That locks the account down even though the data cannot be recalled."),
                        ("Reply to the email with the current password so they can secure it", False,
                         "Never send a password by email. A genuine notice will not ask for it, and this one explicitly says it never will."),
                        ("Pay a fee to have the data removed", False,
                         "A legitimate breach notice does not ask for payment. Any message demanding a fee to remove your data is a follow-on scam."),
                        ("Ignore it, since there is nothing that can be done", False,
                         "There is plenty to do. Changing the reused password and turning on two-factor sharply reduces how the leaked details can be misused."),
                    ],
                },
                "payload": {
                    "prompt": "Handle the breach as it unfolds. Make each call and see the consequence.",
                    "start": "call",
                    "nodes": {
                        "call": {
                            "text": "A journalist emails your business: a sample of your customers' personal details has appeared on a leak site. Minutes later a text arrives, quoting one of those details and demanding a fee to 'remove' the data. What is your first move?",
                            "choices": [
                                {"label": "Do not pay the text. Verify the claim, and report it to your manager and the relevant authority for advice.", "outcome": "good",
                                 "feedback": "Right. Verify and report through proper channels. The demand is a follow-on attack, not a solution.", "to": "customers"},
                                {"label": "Pay the fee in the text so the data disappears.", "outcome": "bad",
                                 "feedback": "The data is already copied and shared, so nothing is removed. Paying just marks you as a target.", "to": "pay_bad"},
                                {"label": "Ignore both messages and hope it blows over.", "outcome": "bad",
                                 "feedback": "The data is out and customers are exposed. Silence makes it worse when it surfaces. This needs action.", "to": "ignore_bad"},
                            ],
                        },
                        "pay_bad": {
                            "text": "You pay, but the data is already copied and circulating, and nothing is removed. Paying a follow-up demand only marks you as a target for the next one. Verify and report instead, never pay the message.",
                            "choices": [],
                        },
                        "ignore_bad": {
                            "text": "Ignoring it does not make it go away. The data is out, customers are exposed, and staying silent makes the eventual fallout worse. A breach needs verifying and reporting, not hoping.",
                            "choices": [],
                        },
                        "customers": {
                            "text": "Good: you are verifying and getting advice rather than paying. Now, what do you do for the affected customers?",
                            "choices": [
                                {"label": "Tell them plainly what was exposed, and that they should change reused passwords and turn on two-factor.", "outcome": "good",
                                 "feedback": "Exactly. Honest, plain guidance lets people protect themselves, and it is what keeps their trust.", "to": "win"},
                                {"label": "Say nothing, to avoid worrying them.", "outcome": "bad",
                                 "feedback": "Kept in the dark, customers cannot protect themselves, and the trust cost is far worse when it comes out.", "to": "silent_bad"},
                                {"label": "Tell them everything is completely fine and no action is needed.", "outcome": "bad",
                                 "feedback": "That is false reassurance. Their details are exposed, and they need real steps to protect themselves.", "to": "silent_bad"},
                            ],
                        },
                        "silent_bad": {
                            "text": "Kept in the dark, customers cannot protect themselves, and the trust cost is far worse when it surfaces later. Honest, plain guidance is both the right thing and the safer path for the business.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Verified, reported, nothing paid, and customers given clear steps to protect themselves. You cannot recall leaked data, but a calm, honest response limits the harm and keeps trust intact.",
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
        # ---- Lesson 1: Know the threats: malware, and how it gets in ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does the word 'malware' mean?",
            "options": [
                ("The umbrella term for harmful software: viruses, worms, trojans, spyware and ransomware", True,
                 "Yes. Malware is the whole family of harmful software. A virus is only one member of it."),
                ("A specific brand of antivirus", False,
                 "No. Malware is the threat, not the protection against it."),
                ("Faulty or broken hardware", False,
                 "No. Malware is harmful software, not broken equipment."),
                ("A strong, unique password", False,
                 "No. That is a defence. Malware is the harmful software it helps protect against."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is the key difference between a virus and a worm?",
            "options": [
                ("A virus needs a person to open the infected file; a worm spreads across the network by itself", True,
                 "Yes. That is why a worm can move so fast, and why the two are stopped by different defences."),
                ("A virus spreads by itself; a worm needs a person to run it", False,
                 "No. That is backwards. The worm is the self-spreading one; the virus waits for a click."),
                ("They are two words for exactly the same thing", False,
                 "No. The difference in how they spread is real and useful for defending against each."),
                ("A virus only affects phones and a worm only affects computers", False,
                 "No. Both can affect computers. The real difference is whether it spreads on its own."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is the defining feature of a trojan?",
            "options": [
                ("It is disguised as something you want, so you install or run it yourself", True,
                 "Yes. You let it in because it looks legitimate, and then it does its real work."),
                ("It spreads across the network without any help", False,
                 "No. That is a worm. A trojan relies on you choosing to run it."),
                ("It floods a website with traffic", False,
                 "No. That is a denial-of-service attack. A trojan is disguised software you run yourself."),
                ("It is completely harmless", False,
                 "No. A trojan is harmful; the disguise is exactly what makes it dangerous."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "While browsing a streaming site, a pop-up warns that your video player is out of date and you must download an update now. What is the safe move?",
            "options": [
                ("Ignore it and update software only from the maker or your app store", True,
                 "Yes. Real updates come from the software itself or an official store, never from a pop-up on an unrelated website. This one is bait."),
                ("Click Download Update straight away so you can keep watching", False,
                 "No. That download is the trap. A pop-up on a streaming site is a classic way to deliver malware."),
                ("Pay the small fee it asks for", False,
                 "No. Never pay or download from a pop-up like this. Close the tab and move on."),
                ("Forward the pop-up to a friend to check", False,
                 "No. There is nothing to check. It is a fake designed to make you download malware."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "An email attachment is named Invoice_4471.pdf.exe. What does that tell you?",
            "options": [
                ("The double extension means it is really a program (.exe) disguised as a PDF, so do not open it and report it", True,
                 "Yes. The real type is the last extension: .exe runs code. The .pdf in the middle is padding to look harmless."),
                ("It is a normal PDF invoice, safe to open", False,
                 "No. Look at the very end: .pdf.exe. The final .exe makes it a program, not a document."),
                ("The file is simply too big to open", False,
                 "No. Size is not the issue. The double extension is the disguise."),
                ("It should have been sent as a link instead", False,
                 "No. The delivery method is not the point. A .pdf.exe is an executable dressed up as a PDF."),
            ],
        },
        # ---- Lesson 2: When it goes wrong: ransomware, breaches, and reacting ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What does ransomware do, and which security pillar does it mainly attack?",
            "options": [
                ("It encrypts your files and demands payment, attacking Availability because you cannot reach your own files", True,
                 "Yes. The files are still there, unchanged, you just cannot get to them, which is a loss of availability."),
                ("It quietly copies your files and publishes them, attacking Availability", False,
                 "No. That describes exposure of data. Ransomware locks your files, which is an availability failure."),
                ("It slows the computer down, attacking Integrity", False,
                 "No. Ransomware locks files and demands money. The pillar it hits is availability, not integrity."),
                ("It does no real harm to a business", False,
                 "No. It is among the most damaging attacks a business can face, taking away access to its own files."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You realise ransomware is encrypting the files on your PC. What is the soundest first move?",
            "options": [
                ("Disconnect the computer from the network, then report it", True,
                 "Yes. Getting it off the network first stops the ransomware spreading to shared drives and other machines."),
                ("Pay the ransom quickly to get the files back", False,
                 "No. Paying is unreliable and funds crime. Contain it first, then recover from backup."),
                ("Keep working and hope it stops", False,
                 "No. Every second it stays connected, more files and machines are locked. Disconnect first."),
                ("Turn the computer off and on again", False,
                 "No. A restart will not undo the encryption. Disconnect it from the network and report it."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Why do authorities generally advise against paying a ransom?",
            "options": [
                ("It does not guarantee recovery, it funds more crime, and it leaves the way in still open; a tested backup is the real answer", True,
                 "Yes. Payment is unreliable and bankrolls the next attack, while a clean backup restores your files without paying anyone."),
                ("Paying instantly removes the malware for good", False,
                 "No. Paying deals with the demand, not the infection or the open door it came through."),
                ("The files always unlock themselves after a week", False,
                 "No. There is no such guarantee. Without a backup or a working key, encrypted files stay locked."),
                ("Backups cost more than the ransom", False,
                 "No. Backups are far cheaper and, unlike a payment, they actually work."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "In the 2022 Optus and Medibank incidents, private customer data was exposed. Which security pillar does a data breach mainly fail?",
            "options": [
                ("Confidentiality, because private information reached people who should not have it", True,
                 "Yes. The systems may keep running; the harm is that private data has leaked out and cannot be recalled."),
                ("Availability, because customers could not reach the files", False,
                 "No. That is ransomware. A breach is about data being exposed, not access being blocked."),
                ("Integrity, because the data was secretly altered", False,
                 "No. A breach is usually about exposure, not quiet alteration. The pillar lost is confidentiality."),
                ("None, because a breach is not really a security problem", False,
                 "No. A breach of private data is a serious confidentiality failure with real consequences for people."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "A company you have an account with emails to say your details were in a data breach. A sensible first step is to:",
            "options": [
                ("Change that account's password, and anywhere you reused it, and turn on two-factor authentication", True,
                 "Yes. You cannot recall leaked data, but you can lock down the accounts so it is far harder to misuse."),
                ("Do nothing, since the data is already out there", False,
                 "No. There is plenty you can still do to reduce the risk to your accounts."),
                ("Pay any fee a follow-up message asks for to secure your account", False,
                 "No. Messages quoting your breached details are usually the follow-on scam. Never pay them."),
                ("Post your new password somewhere so you do not forget it", False,
                 "No. Never write a password out in the open. Keep it private and unique."),
            ],
        },
    ],
}
