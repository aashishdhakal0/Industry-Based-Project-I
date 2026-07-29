"""Module 1 — Network Security Fundamentals: interactive lessons and the quiz.

Content, not schema: kept as plain data so it reads like the teaching material it
is, and so the seed command stays re-runnable. Written in plain Australian
English for non-technical readers — small businesses, councils, schools.

Each lesson is a sequence of short interactive TASKS (TryHackMe-style): a concept
chunk (often with a diagram), an inline check-question, or a real-world scenario.
Every task carries points; a lesson's tasks sum to 10 (POINTS_PER_LESSON), so
finishing the last task banks the whole lesson through the normal points path —
the economy is unchanged, the tasks just fill an XP bar on the way.

QUIZ is the end-of-module assessment (a 15-question bank; ten drawn per attempt).
Every option carries an explanation_text — the Adaptive Feedback Engine reads it
back to the learner, so wrong options explain the misconception, not just "no".
"""

# --------------------------------------------------------------------------
# Lessons — each a sequence of tasks whose points sum to 10.
#   concept  — a teaching chunk (optional diagram); completed by "continue"
#   check    — an inline question with instant feedback; completed when correct
#   scenario — a real-world problem to solve; completed when correct
# Option tuples are (text, is_correct, explanation).
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network actually is",
        "reading_time_minutes": 4,
        "intro": "Meet the thing we're protecting — and the three questions "
        "security always comes back to.",
        "tasks": [
            {
                "key": "what-is-a-network",
                "kind": "concept",
                "points": 2,
                "title": "What a network actually is",
                "diagram": "data-travels",
                "body": "<p>A <strong>network</strong> is simply two or more "
                "devices connected so they can share information — the laptop "
                "talking to the office printer, the phone picking up email, the "
                "eftpos terminal reaching the bank. Your workplace has "
                "<em>devices</em> (computers, phones, printers), a "
                "<em>router</em> (the box that connects you to the internet), "
                "and the <em>internet</em> itself, which your information crosses "
                "to reach a customer or supplier.</p>",
            },
            {
                "key": "network-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "Which of these best describes a network?",
                "options": [
                    ("Two or more devices connected to share information", True,
                     "Exactly — from two machines to the whole internet, a network is devices connected to share information."),
                    ("A single fast computer", False,
                     "Not quite — one computer on its own isn't a network. It's the connection between devices that makes one."),
                    ("An antivirus program", False,
                     "No — antivirus protects a device; it isn't what a network is."),
                    ("Your login password", False,
                     "No — a password controls access, but it isn't the network itself."),
                ],
            },
            {
                "key": "three-states",
                "kind": "concept",
                "points": 2,
                "title": "Where your information lives",
                "body": "<p>At any moment your information is in one of three "
                "places: <strong>at rest</strong> (saved on a device or server), "
                "<strong>in transit</strong> (moving across the network), or "
                "<strong>in use</strong> (open on a screen). Each needs looking "
                "after — a customer list is exposed just as easily by an email "
                "sent to the wrong person as by a stolen laptop.</p>",
            },
            {
                "key": "cia-triad",
                "kind": "concept",
                "points": 2,
                "title": "The three questions security asks",
                "diagram": "cia-triad",
                "body": "<p>Security comes down to the <strong>CIA triad</strong> "
                "— nothing to do with spies. "
                "<strong>Confidentiality</strong> is keeping information away from "
                "people who shouldn't see it. <strong>Integrity</strong> is making "
                "sure it hasn't been changed without permission. "
                "<strong>Availability</strong> is making sure it's there when you "
                "need it. Almost every security decision is really one of these "
                "three.</p>",
            },
            {
                "key": "cia-scenario",
                "kind": "scenario",
                "points": 2,
                "title": "Spot the failure",
                "scenario": "<p>A small Melbourne café keeps a spreadsheet of its "
                "loyalty customers' names and emails. A staff member, rushing, "
                "emails that spreadsheet to the wrong customer.</p>",
                "question": "Which part of the CIA triad has just failed?",
                "options": [
                    ("Confidentiality — the right people should have seen it, and someone else did", True,
                     "Correct — the information reached a person who shouldn't have it. That's a confidentiality failure."),
                    ("Integrity — the information was changed", False,
                     "Not this time — nothing was altered. The problem is who saw it, which is confidentiality."),
                    ("Availability — no one can open the file", False,
                     "No — the file still opens fine. The issue is that it went to the wrong person: confidentiality."),
                    ("Nothing failed — it was just a small slip", False,
                     "It matters — customer details reaching a stranger is a real confidentiality breach, however innocent the mistake."),
                ],
            },
        ],
    },
    {
        "title": "Where the weak points are",
        "reading_time_minutes": 4,
        "intro": "The handful of ways attackers actually get in — and why the "
        "biggest one isn't a machine at all.",
        "tasks": [
            {
                "key": "attack-vectors",
                "kind": "concept",
                "points": 2,
                "title": "The common ways in",
                "body": "<p>Attackers rarely break in cleverly — they walk "
                "through an open door. The common ones are few: "
                "<strong>phishing</strong> (a message pretending to be someone you "
                "trust), <strong>weak or reused passwords</strong>, "
                "<strong>out-of-date software</strong> (updates fix holes; until "
                "you install them, the hole is open), <strong>malware</strong> "
                "like ransomware, and <strong>unsafe networks</strong> such as "
                "public Wi-Fi. Nearly all of them are preventable.</p>",
            },
            {
                "key": "phishing-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "What is 'phishing'?",
                "options": [
                    ("A message pretending to be from someone you trust, to trick you into clicking or sharing details", True,
                     "Right — phishing impersonates a trusted sender, and it's the most common way organisations are attacked."),
                    ("A way to speed up your internet", False,
                     "No — phishing has nothing to do with speed; it's a form of deception."),
                    ("A tool that backs up your files", False,
                     "No — that's a backup. Phishing is a scam message designed to trick you."),
                    ("A setting on your router", False,
                     "No — phishing arrives as a message; it isn't a router setting."),
                ],
            },
            {
                "key": "human-error",
                "kind": "concept",
                "points": 2,
                "title": "The biggest weak point isn't a machine",
                "body": "<p>If you remember one thing, make it this: "
                "<strong>human error is the biggest risk of all</strong>. Most "
                "incidents involve a person doing something ordinary — clicking a "
                "link that looked genuine, reusing a password, approving a payment "
                "because an email seemed urgent. That's not a reason for guilt; "
                "it's where the leverage is. Attackers rely on <em>urgency</em> to "
                "stop you thinking, so slowing down is itself a security "
                "control.</p>",
            },
            {
                "key": "bakery-scenario",
                "kind": "scenario",
                "points": 2,
                "title": "Scenario: the urgent invoice",
                "diagram": "phishing-email",
                "scenario": "<p>You do the books for a Brunswick bakery. An email "
                "lands from what looks like your flour supplier: "
                "<em>“Our bank details have changed — please pay the overdue "
                "invoice to the new account within the hour or deliveries stop.”</em> "
                "The sender's address is billing@flour-supplier-au.info, and there's "
                "a link to 'view the invoice'.</p>",
                "question": "What's the safest first move?",
                "options": [
                    ("Pause, and ring the supplier on the number you already have to check", True,
                     "Correct — urgency plus a change of bank details is the classic scam shape. Verify through a channel you already trust."),
                    ("Pay quickly so the deliveries don't stop", False,
                     "No — the deadline exists to rush you. Paying now is exactly what the attacker wants."),
                    ("Click the link to read the invoice first", False,
                     "Risky — an unexpected link is how many attacks begin. Don't click; verify the request another way."),
                    ("Reply to the email to ask if it's genuine", False,
                     "No — if it's a scam you're just asking the attacker, who'll say yes. Confirm using details you already hold."),
                ],
            },
            {
                "key": "password-reuse-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "Why is reusing one password across many sites dangerous?",
                "options": [
                    ("If one site is breached, attackers try that password everywhere else", True,
                     "Exactly — one leak then unlocks all your accounts. Unique passwords keep a single breach contained."),
                    ("It makes websites load more slowly", False,
                     "No — reuse has no effect on speed; the danger is that one leak spreads everywhere."),
                    ("It uses up storage on your device", False,
                     "No — passwords take almost no storage. The risk is a single breach unlocking everything."),
                    ("It's fine as long as the password is long", False,
                     "No — even a long password is dangerous if reused, because one breached site exposes it everywhere."),
                ],
            },
        ],
    },
    {
        "title": "Wi-Fi, routers and the front door",
        "reading_time_minutes": 4,
        "intro": "Set up the one box every piece of your information passes "
        "through, and you close a whole category of risk.",
        "tasks": [
            {
                "key": "router-front-door",
                "kind": "concept",
                "points": 2,
                "title": "The router is your front door",
                "body": "<p>If your network were a building, the "
                "<strong>router</strong> would be the front door — the box "
                "(sometimes called a modem or gateway) that connects everything "
                "to the internet. Almost all of your information passes through "
                "it, which makes it one of the most important things to set up "
                "properly, and one of the most commonly neglected.</p>",
            },
            {
                "key": "two-passwords",
                "kind": "concept",
                "points": 2,
                "title": "Change the default passwords — both",
                "body": "<p>A new router has <strong>two</strong> passwords, and "
                "people mix them up. The <strong>Wi-Fi password</strong> is what "
                "people type to join the wireless. The <strong>admin "
                "password</strong> logs in to change the router's own settings — "
                "and it's the dangerous one to leave on the factory default, "
                "because those defaults are published online. Change both when "
                "the device is first set up.</p>",
            },
            {
                "key": "admin-password-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "Which password is the dangerous one to leave on the factory default?",
                "options": [
                    ("The admin password that changes the router's settings", True,
                     "Right — its defaults are publicly known, so leaving it unchanged lets anyone who reaches the router take it over."),
                    ("The guest Wi-Fi password", False,
                     "Change that too, but the admin password is the critical one people forget even exists."),
                    ("Your email password", False,
                     "Your email password isn't set on the router — the risky default here is the router's admin password."),
                    ("Neither, if the box is brand new", False,
                     "No — both should be changed, the admin one especially, precisely because it's new and still on a known default."),
                ],
            },
            {
                "key": "guest-and-encryption",
                "kind": "concept",
                "points": 2,
                "title": "Guest network and modern encryption",
                "body": "<p>Two quick wins. Turn on a <strong>guest network</strong> "
                "— a separate Wi-Fi name for visitors and personal phones, kept "
                "apart from your work devices, so an infected visitor's phone "
                "can't reach your business systems. And choose modern "
                "<strong>encryption</strong> (WPA3 or WPA2, the newest your gear "
                "supports); avoid the old WEP, which is long broken.</p>",
            },
            {
                "key": "public-wifi-scenario",
                "kind": "scenario",
                "points": 2,
                "title": "Scenario: the café login",
                "scenario": "<p>You're at a café and need to log in to your work "
                "system to fix something before a meeting. The café's free Wi-Fi "
                "is open and available.</p>",
                "question": "What's the safest choice?",
                "options": [
                    ("Use your phone's mobile data or a trusted VPN instead", True,
                     "Correct — on a network you don't control, use mobile data or a trusted VPN for anything sensitive."),
                    ("Go ahead on the café Wi-Fi — it's fine", False,
                     "No — you can't be sure who else is on public Wi-Fi or what they can see. Treat it as a public space."),
                    ("Check that the café is busy first", False,
                     "No — how many customers are in doesn't tell you anything about whether the network is safe."),
                    ("Just lower your screen brightness", False,
                     "No — the risk is the network carrying your data, not someone reading over your shoulder."),
                ],
            },
        ],
    },
    {
        "title": "A simple security checklist",
        "reading_time_minutes": 3,
        "intro": "Turn everything you've learned into a handful of habits — and "
        "know exactly what to do if something ever goes wrong.",
        "tasks": [
            {
                "key": "everyday-habits",
                "kind": "concept",
                "points": 3,
                "title": "The everyday habits",
                "body": "<p>A short, practical list prevents most problems:</p>"
                "<ul>"
                "<li><strong>Pause</strong> before acting on an unexpected, urgent "
                "message.</li>"
                "<li><strong>Verify</strong> money or bank-detail changes by phoning "
                "a number you already have.</li>"
                "<li>Use <strong>strong, unique passwords</strong> with a password "
                "manager, and turn on <strong>two-factor authentication</strong>, "
                "especially on email.</li>"
                "<li>Install <strong>updates</strong> promptly, and keep "
                "<strong>backups</strong> you've checked you can restore.</li>"
                "</ul>",
            },
            {
                "key": "twofactor-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "What does turning on two-factor authentication achieve?",
                "options": [
                    ("A stolen password alone is no longer enough to get in", True,
                     "Right — a second check means a leaked password by itself won't let an attacker into your account."),
                    ("It makes your password impossible to steal", False,
                     "No — it doesn't stop a password being stolen; it makes a stolen password insufficient on its own."),
                    ("It replaces your password entirely", False,
                     "No — two-factor works alongside your password, adding a second step rather than replacing it."),
                    ("It backs up your account", False,
                     "No — two-factor verifies it's really you; it isn't a backup."),
                ],
            },
            {
                "key": "map-to-cia",
                "kind": "concept",
                "points": 2,
                "title": "Why each habit matters",
                "body": "<p>Each habit protects one of the three things from the "
                "first lesson. Strong passwords and two-factor protect "
                "<strong>confidentiality</strong>. Verifying a change of bank "
                "details protects <strong>integrity</strong>. Backups protect "
                "<strong>availability</strong>. When you can see <em>why</em> a "
                "habit matters, it's far easier to keep.</p>",
            },
            {
                "key": "report-scenario",
                "kind": "scenario",
                "points": 3,
                "title": "Scenario: the slip",
                "scenario": "<p>An hour ago you entered your work password into a "
                "page that, thinking back, looked a bit off. Nothing obvious has "
                "happened since. You feel a bit embarrassed.</p>",
                "question": "What's the best thing to do?",
                "options": [
                    ("Report it straight away to whoever looks after your IT, or your manager", True,
                     "Correct — fast reporting turns a near-miss into a non-event. There's never trouble for reporting, only for hiding it."),
                    ("Say nothing and hope it's fine", False,
                     "No — staying quiet lets a small problem grow. Quick reporting is what limits the damage."),
                    ("Delete the page from your history and move on", False,
                     "No — that doesn't undo an entered password. It needs reporting so the account can be secured."),
                    ("Wait a week to see if anything goes wrong", False,
                     "No — waiting just gives an attacker time. Report it now so action can be taken."),
                ],
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz — a 15-question bank; ten drawn per attempt.
# Each question names the lesson it comes from (1-based, into LESSONS above) so
# the Adaptive Feedback Engine can trace a mistake back to the right lesson.
# Options: exactly one correct; every option carries an explanation.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "In plain terms, what is a computer network?",
            "options": [
                ("Two or more devices connected so they can share information", True,
                 "Correct — a network is just devices connected to share information, from two machines to the whole internet."),
                ("A single computer with a fast processor", False,
                 "No — one computer on its own isn't a network; a network is about devices being connected to each other."),
                ("A type of antivirus program", False,
                 "No — antivirus is software that protects a device; it isn't what a network is."),
                ("The password you use to log in", False,
                 "No — a password protects access, but it isn't the network itself."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "What do the letters in the 'CIA triad' stand for?",
            "options": [
                ("Confidentiality, Integrity and Availability", True,
                 "Correct — these are the three things security protects, and most decisions come back to one of them."),
                ("Computers, Internet and Applications", False,
                 "No — the triad is about what we protect, not a list of equipment."),
                ("Control, Inspection and Access", False,
                 "No — these sound plausible but aren't the triad; it's Confidentiality, Integrity and Availability."),
                ("Confidential Intelligence Agency", False,
                 "No — despite the initials, the CIA triad has nothing to do with spy agencies."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "An invoice's bank details are secretly changed so payment goes to a stranger. Which part of the CIA triad has failed?",
            "options": [
                ("Integrity — the information was altered without permission", True,
                 "Correct — the file still opens, but its accuracy is gone; that's an integrity failure, and a common way money is stolen."),
                ("Availability — the file can't be opened", False,
                 "No — availability is about whether you can access something; here the file opens fine, it's just been tampered with."),
                ("Confidentiality — someone saw information they shouldn't", False,
                 "Not quite — the problem isn't who saw it, it's that the details were changed. That's integrity."),
                ("None of them — this isn't a security issue", False,
                 "No — altering financial details without permission is very much a security issue: a failure of integrity."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "Keeping a restorable backup of your files mainly protects which part of the CIA triad?",
            "options": [
                ("Availability — you can still get your information when you need it", True,
                 "Correct — backups mean an attack or mistake doesn't cost you access to your information; that's availability."),
                ("Confidentiality — it hides the files from others", False,
                 "No — a backup doesn't hide anything; it ensures you can still get your data back. That's availability."),
                ("Integrity — it proves the files weren't changed", False,
                 "Not the main point — backups are chiefly about being able to restore access, which is availability."),
                ("Backups aren't related to security at all", False,
                 "No — backups are a core security control; they protect availability against ransomware and mistakes."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "EASY",
            "text": "What is 'phishing'?",
            "options": [
                ("A message pretending to be from someone you trust, to trick you into clicking or sharing details", True,
                 "Correct — phishing impersonates a trusted sender and is the most common way organisations are attacked."),
                ("A way of speeding up your internet connection", False,
                 "No — phishing has nothing to do with connection speed; it's a form of deception."),
                ("A tool that backs up your files", False,
                 "No — that's a backup; phishing is a scam message designed to trick you."),
                ("A setting on your router", False,
                 "No — phishing is a type of attack delivered by message, not a router setting."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "According to this module, what is the single biggest security risk?",
            "options": [
                ("Human error — everyday mistakes like clicking a link or reusing a password", True,
                 "Correct — most incidents involve an ordinary human action, which is why calm habits matter more than any product."),
                ("Old printers", False,
                 "No — while any device can be a weak point, the biggest risk overall is human error."),
                ("Having too many backups", False,
                 "No — backups are a good thing; they're never the risk."),
                ("Using a router at all", False,
                 "No — routers are essential; the biggest risk is everyday human error, not the equipment."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "Why is reusing the same password across many sites dangerous?",
            "options": [
                ("If one site is breached, attackers try that password everywhere else", True,
                 "Correct — a single leak then unlocks all your accounts; unique passwords contain the damage."),
                ("It makes websites load more slowly", False,
                 "No — password reuse has no effect on speed; the danger is that one leak unlocks everything."),
                ("It uses up storage on your device", False,
                 "No — passwords don't take meaningful storage; the risk is that a single breach spreads."),
                ("There's no real danger if the password is long", False,
                 "No — even a long password is dangerous if reused, because one breached site exposes it everywhere."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "HARD",
            "text": "An email says 'Pay this overdue invoice in the next hour or the account will be closed.' What's the safest first step?",
            "options": [
                ("Pause, and verify the request using contact details you already have", True,
                 "Correct — urgency is a pressure tactic. Slowing down and confirming another way is the safest move."),
                ("Pay immediately so the account isn't closed", False,
                 "No — acting fast is exactly what the attacker wants; the deadline exists to stop you thinking."),
                ("Reply to the email asking if it's genuine", False,
                 "Risky — if it's a scam, you're just asking the attacker, who will say yes. Verify through a channel you trust."),
                ("Click the link to see the invoice details", False,
                 "No — clicking an unexpected link is how many attacks begin; verify before you click anything."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "Why do attackers often target small businesses, councils and schools?",
            "options": [
                ("Automated tools look for any unlocked door, and smaller organisations often have fewer defences", True,
                 "Correct — attacks are largely automated and opportunistic; being small doesn't mean being safe."),
                ("They are too small to be worth attacking", False,
                 "No — this is the dangerous myth; smaller organisations are targeted precisely because defences are often lighter."),
                ("They never hold any valuable information", False,
                 "No — they hold plenty of valuable data, from customer details to payment information."),
                ("Attackers personally choose each victim by name", False,
                 "No — most attacks are automated and untargeted, knocking on thousands of doors at once."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "On a new router, which password is the dangerous one to leave on the factory default?",
            "options": [
                ("The admin password used to change the router's settings", True,
                 "Correct — default admin passwords are published online, so leaving it unchanged lets anyone take the router over."),
                ("The Wi-Fi password guests use to connect", False,
                 "Partly — you should change this too, but the admin password is the critical one people forget exists."),
                ("Your email password", False,
                 "No — your email password isn't set on the router; the risky default here is the router's admin password."),
                ("Neither needs changing if the box is new", False,
                 "No — both should be changed, and the admin password especially, because its defaults are publicly known."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "EASY",
            "text": "What is the main benefit of a separate 'guest' Wi-Fi network?",
            "options": [
                ("It keeps visitors' and personal devices apart from your work devices", True,
                 "Correct — if a guest device is infected, a guest network keeps that problem away from your business systems."),
                ("It makes your internet twice as fast", False,
                 "No — a guest network is about separation and safety, not speed."),
                ("It removes the need for any passwords", False,
                 "No — a guest network still uses a password; it simply separates guests from your main network."),
                ("It automatically backs up guest files", False,
                 "No — a guest network doesn't back anything up; its purpose is to keep guest devices separate."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "When setting Wi-Fi encryption, which should you choose?",
            "options": [
                ("The most recent option your equipment supports, such as WPA3 or WPA2", True,
                 "Correct — modern encryption protects everything on the network; pick the newest your gear supports."),
                ("The oldest option, WEP, for compatibility", False,
                 "No — WEP is long broken and should be avoided; choose WPA2 or WPA3 instead."),
                ("No encryption, to keep things simple", False,
                 "No — an open network lets anyone nearby read your traffic; always use modern encryption."),
                ("It doesn't matter which you choose", False,
                 "No — it matters a great deal; older schemes like WEP are insecure, so pick the newest available."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "HARD",
            "text": "You need to log in to a work system while on free café Wi-Fi. What's the safest choice?",
            "options": [
                ("Use your phone's mobile connection or a trusted VPN instead", True,
                 "Correct — on a network you don't control, use mobile data or a trusted VPN for anything sensitive."),
                ("Go ahead — café Wi-Fi is always safe", False,
                 "No — you can't be sure who else is on public Wi-Fi or what they can see; treat it as a public space."),
                ("Just make sure the café is busy", False,
                 "No — how many customers there are tells you nothing about whether the network is safe."),
                ("Turn off your screen brightness so no one can see", False,
                 "No — the risk is the network carrying your data, not someone reading your screen."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "EASY",
            "text": "What does turning on two-factor authentication achieve?",
            "options": [
                ("A stolen password alone is no longer enough to get into the account", True,
                 "Correct — two-factor adds a second check, so a leaked password by itself won't let an attacker in."),
                ("It makes your password impossible to steal", False,
                 "No — it doesn't stop a password being stolen; it makes a stolen password insufficient on its own."),
                ("It removes the need for a password entirely", False,
                 "No — two-factor works alongside your password, adding a second step rather than replacing it."),
                ("It backs up your account", False,
                 "No — two-factor is about verifying it's really you; it isn't a backup."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "MEDIUM",
            "text": "You realise you may have entered your password into a suspicious page. What's the best thing to do?",
            "options": [
                ("Report it straight away to whoever looks after your IT or your manager", True,
                 "Correct — fast reporting turns a near-miss into a non-event; there's never trouble for reporting, only for hiding it."),
                ("Say nothing and hope nothing happens", False,
                 "No — staying quiet lets a small problem grow; quick reporting is what limits the damage."),
                ("Delete the email and carry on as normal", False,
                 "No — deleting the message doesn't undo an entered password; you need to report it so the account can be secured."),
                ("Wait a week to see if anything goes wrong", False,
                 "No — waiting gives an attacker time; report it immediately so action can be taken."),
            ],
        },
    ],
}
