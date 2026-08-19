"""Module 1, Network Security Fundamentals: the gold-standard reference content.

This is the module every other module copies, so the shape matters as much as the
words. Kept as plain data (not schema) so it reads like teaching material and the
seed stays re-runnable.

Room format (TryHackMe-style), rebalanced toward DOING: a lesson is a scrollable
room of collapsible task PANELS, and the interactive is the CENTRE of each panel,
not an afterthought. Each panel is a tight setup (a couple of sentences) then a
hands-on task: a sort/classify triage, an inbox to inspect, a spot-the-fake, a
password build, a workspace to harden, a respond-to-the-situation exercise, or a
branching scenario. A few short "apply it" checks remain, framed as real
decisions rather than definitions. The panels' points sum to 10 and bank at
lesson end.

House voice for here and Modules 2 to 6: warm, confident, human. Plain Australian
English for non-technical readers. Reading is kept tight so the doing teaches.
Concrete local scenarios. No em-dashes, no filler.
"""

# --------------------------------------------------------------------------
# Lessons. Each task is a panel: a short `body` (the setup, may include a
# `<div class="cy-callout">` box) then one interactive that carries the learning.
# `check` panels are apply-it decisions (question + hint + four options, tuples of
# (text, is_correct, explanation)); activity panels put the config in `payload`.
# Optional `inline_check` adds a mid-panel apply-it question; `body2` adds a short
# line before the end activity. Points per lesson sum to 10.
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network is, and what you protect",
        "reading_time_minutes": 7,
        "intro": "Meet the thing you are protecting, walk the path your "
        "information takes, and lock in the three questions security keeps asking.",
        "tasks": [
            {
                "key": "net-basics",
                "kind": "check",
                "points": 2,
                "title": "What a network actually is",
                "hero": "net-scene",
                "diagram": "router-admin",
                "body": "<p>A network is just devices connected so they can share "
                "information: the front-desk computer, the printer, the eftpos "
                "machine, all talking through the router and out to the internet. The "
                "router is the heart of it, and its own settings page decides how safe "
                "the whole network is. You do not need to be technical to read it: "
                "above is a real router's admin page.</p>"
                "<div class=\"cy-callout\">Read the four rows above. Three are set up "
                "well. One is a wide-open door that anyone could walk through.</div>",
                "inline_check": {
                    "question": "Reading the router's settings, which row is set up WELL?",
                    "hint": "WPA2 and up-to-date firmware are good signs. A default password is not.",
                    "options": [
                        ("Wi-Fi encryption is set to WPA2", True,
                         "Yes. WPA2 encryption scrambles your Wi-Fi so a stranger nearby cannot read it. That is a good setting."),
                        ("The admin password is 'admin'", False,
                         "That is the weak spot, not a good habit. 'admin' is the factory default, printed online for anyone to look up."),
                        ("The guest network is open with no password", False,
                         "An open guest network is a mild risk, not a good habit. Anyone in range can hop onto it."),
                        ("Nothing here is set up well", False,
                         "Look again: WPA2 is on and the firmware is up to date. Two good settings, one clear problem."),
                    ],
                },
                "question": "What is the security problem shown on this router page?",
                "hint": "One row shows a value that every installer and every website already knows.",
                "options": [
                    ("The admin password is still the default, 'admin'", True,
                     "Right. Default router passwords like 'admin' are printed in manuals and listed online, so anyone can look yours up and change your settings. Changing it is the single most important fix."),
                    ("The firmware is up to date", False,
                     "That is a good thing, not a problem. Up-to-date firmware means known security holes are already patched."),
                    ("Wi-Fi is using WPA2 encryption", False,
                     "That is a good thing. WPA2 keeps your wireless traffic scrambled from anyone nearby."),
                    ("The router has an IP address", False,
                     "Every router has an address so you can reach its settings. That is normal, not a security problem."),
                ],
            },
            {
                "key": "clinic-mornings",
                "kind": "respond",
                "points": 2,
                "title": "Your clinic, three bad mornings",
                "body": "<p>Picture a small Australian clinic: one busy front desk, a "
                "shared drive, and the same everyday tools you just met. Over one "
                "rough week, three things go wrong. Knowing what a network is was the "
                "first step. The real skill is what you do in the moment, because your "
                "first move decides how far a problem spreads. For each morning, choose "
                "your first move and see how it plays out.</p>"
                "<div class=\"cy-callout\"><strong>The habit to build:</strong> fast "
                "and calm beats clever. Contain the problem, then report it.</div>",
                "payload": {
                    "prompt": "Choose the soundest first move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "misfire",
                            "text": "Monday. A staff member realises they just emailed the day's patient list to the wrong address.",
                            "options": [
                                {"text": "Tell your manager and IT straight away so it can be handled", "outcome": "good",
                                 "feedback": "Right. A privacy slip is far cheaper to handle in the first hour. Owning up fast is the whole game."},
                                {"text": "Delete your sent copy and hope nobody noticed", "outcome": "bad",
                                 "feedback": "Deleting your copy changes nothing at the other end, and the delay only makes it worse. Report it."},
                                {"text": "Email the stranger asking them to delete it, then move on", "outcome": "risky",
                                 "feedback": "Worth asking, but not instead of reporting it. Your manager and IT need to know so it is handled properly."},
                            ],
                        },
                        {
                            "id": "locked",
                            "text": "Wednesday. Every file on the shared drive is suddenly renamed, and a note on screen demands payment.",
                            "options": [
                                {"text": "Disconnect the computer from the network and report it", "outcome": "good",
                                 "feedback": "Exactly. Getting it off the network first stops the ransomware spreading to other machines and the shared drive."},
                                {"text": "Pay quickly to get the files back", "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds crime, and marks you as a payer. Contain it first, then recover from backup."},
                                {"text": "Keep working and hope it stops", "outcome": "bad",
                                 "feedback": "Every second it stays connected, more files and machines are locked. Disconnect first."},
                            ],
                        },
                        {
                            "id": "changed",
                            "text": "Friday. An invoice you are about to pay has a bank account that looks different from last month.",
                            "options": [
                                {"text": "Ring the supplier on a number you already have and check", "outcome": "good",
                                 "feedback": "Yes. A changed account plus any pressure to pay is the classic invoice scam. Verify on a channel you already trust."},
                                {"text": "Pay it, the invoice looks genuine", "outcome": "bad",
                                 "feedback": "A tampered invoice looks perfectly genuine. That is the point. Verify the changed details first."},
                                {"text": "Email back to ask if the account really changed", "outcome": "risky",
                                 "feedback": "If the email is a scam, you are asking the scammer. Use a number you already have, not the one in the email."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "secure-login",
                "kind": "check",
                "points": 2,
                "title": "Is this connection secure?",
                "diagram": "secure-bars",
                "body": "<p>Your information does not sit still. It travels from your "
                "device, through your router, across the shared public internet, and "
                "onto a server somewhere else. On that public stretch, anyone in the "
                "middle could try to read it, which is why the last habit matters most "
                "when you log in.</p>"
                "<p>Before you type a password, your browser quietly tells you whether "
                "the connection is protected. Two signs matter: the address starts "
                "with <strong>https</strong> (the s is for secure) and a small "
                "<strong>padlock</strong> sits beside it. Together they mean your "
                "password is encrypted on the way, so it cannot be read.</p>"
                "<div class=\"cy-callout\">Read the two browser windows above. They are "
                "for the same clinic login, but only one is safe. Look at what comes "
                "before the address, whether a padlock is there, and the address "
                "itself.</div>",
                "question": "Both windows open a login page for the same clinic. Which one is safe to type your password into, and how can you tell?",
                "hint": "Look for a padlock, and the letters right after http. One window is missing both.",
                "options": [
                    ("The bottom window, because it shows a padlock and its address starts with https", True,
                     "Right. The padlock and the s in https mean the connection is encrypted, so your password cannot be read as it travels. The top window is marked Not secure and uses plain http."),
                    ("The top window, because its address is shorter and simpler", False,
                     "Length is not safety. The top window is marked Not secure and uses http, so anything you type could be read in transit. It even uses a different address, .info instead of .com.au."),
                    ("Either one, they are the same clinic", False,
                     "They look alike on purpose. Only the bottom window, with the padlock and https, protects what you type. Notice the top address ends in .info, not the real .com.au."),
                    ("Neither, a login page can never be trusted", False,
                     "You can trust this one: the bottom window shows https, the padlock, and the correct .com.au address. Those three together are the green light."),
                ],
            },
            {
                "key": "l1-quizset",
                "kind": "quizset",
                "points": 2,
                "title": "Pull it together",
                "diagram": "cia-triad",
                "body": "<p>Time to bring it together. The board above shows the three "
                "pillars security keeps coming back to (who can see it, is it "
                "unchanged, can you reach it) and an incident to apply them to. Four "
                "quick questions now mix what a network is, how information travels, "
                "and those three pillars. Answer each one to finish.</p>",
                "payload": {
                    "prompt": "Answer all four to complete the task. A wrong answer just lets you try again.",
                    "questions": [
                        {"type": "mcq",
                         "q": "Read the incident on the board above (the invoice with its bank account quietly changed, that still opens fine). Which pillar has failed?",
                         "hint": "The file is not hidden and not locked. Something about it was changed.",
                         "options": [
                             ["Integrity, the information was altered without permission", True, "Yes. It still opens and nobody is locked out, but the details were changed behind your back. That is integrity, and exactly how invoice scams work."],
                             ["Confidentiality, someone saw it", False, "The problem is not who saw it, it is that it was changed. That is integrity."],
                             ["Availability, you cannot open it", False, "It opens perfectly. The problem is the contents were altered, which is integrity."],
                             ["None of them, the invoice looks fine", False, "A quietly changed bank account is a classic integrity attack, and it matters a great deal."]
                         ]},
                        {"type": "truefalse",
                         "q": "True or false: once your data reaches the public internet, only the sender and receiver can see it.",
                         "answer": False,
                         "hint": "Think about who else shares that middle stretch.",
                         "why": "False. The public internet is shared ground. That middle stretch is exactly why we use encryption, the padlock in the address bar."},
                        {"type": "fill",
                         "q": "The three questions security keeps coming back to are known as the ___ triad. (three letters)",
                         "answer": "CIA",
                         "accept": ["c.i.a", "cia triad", "confidentiality integrity availability"],
                         "hint": "Confidentiality, Integrity, Availability.",
                         "why": "Correct. CIA: Confidentiality, Integrity, Availability. Nothing to do with spies."},
                        {"type": "match",
                         "q": "Match each pillar to the question it asks.",
                         "hint": "Who can see it, is it unchanged, and can you get to it.",
                         "why": "That is the triad. Every security habit in this course defends one of these three.",
                         "pairs": [
                             ["Confidentiality", "Can only the right people see it?"],
                             ["Integrity", "Is it still accurate and unaltered?"],
                             ["Availability", "Is it there when you need it?"]
                         ]}
                    ]
                },
            },
            {
                "key": "spot-scam",
                "kind": "check",
                "points": 2,
                "title": "Spot the scam email",
                "diagram": "scam-email",
                "body": "<p>The same careful eye that reads a router page or an address "
                "bar reads an inbox. Most attacks on a small business do not break in, "
                "they are invited in by a convincing email. The message above looks "
                "like a delivery notice. Read it closely, then answer. This is the "
                "gate before the next lesson.</p>"
                "<div class=\"cy-callout\">Check three things on any email like this: "
                "who it is really from (the address, not just the name), whether it "
                "rushes you, and where the link actually goes.</div>",
                "question": "Looking at this email, what is the strongest sign it is a scam?",
                "hint": "Ignore the friendly name. Read the actual address it was sent from.",
                "options": [
                    ("The sender is a lookalike address, auspost-au-secure.info, not the real auspost.com.au", True,
                     "Right. The display name says AusPost, but the real address is a lookalike .info domain. Australia Post would never email from auspost-au-secure.info. The rushed 24-hour fee and the matching link seal it."),
                    ("It was sent at 9:14 in the morning", False,
                     "The time of day tells you nothing. Real and fake emails both arrive in the morning."),
                    ("It mentions a parcel", False,
                     "Plenty of genuine emails mention parcels. On its own that is not a warning sign. The giveaway is the fake sender address."),
                    ("It uses the colour blue", False,
                     "A blue button is just styling. Scammers copy real branding on purpose. Judge the sender address and the link, not the colours."),
                ],
            },
        ],
    },
    {
        "title": "How attacks actually happen",
        "reading_time_minutes": 7,
        "intro": "Most attacks do not break in. They are invited in. Learn how "
        "they really start, and train your eye to see one coming.",
        "tasks": [
            {
                "key": "how-attacks",
                "kind": "check",
                "points": 2,
                "title": "How attacks actually begin",
                "body": "<p>Forget the hooded genius in a dark room. Almost every "
                "attack on a small business starts with a person being gently tricked "
                "into opening a door: a convincing email, a phone call, a fake login "
                "page. The trade name for this is <strong>social engineering</strong>, "
                "and it works because it targets trust and time pressure, not "
                "code.</p>"
                "<div class=\"cy-callout\">The attacker's easiest path is nearly "
                "always a busy human, not a clever exploit. Most real breaches come "
                "down to simple human error, a person tricked in a rushed moment. That "
                "is good news: it means a careful eye stops most of it.</div>",
                "question": "Which of these is how most attacks on a small business actually begin?",
                "hint": "Think about the easiest door, not the cleverest lock.",
                "options": [
                    ("Someone is tricked into clicking, paying, or sharing a password", True,
                     "Yes. Social engineering, tricking a person, is behind the great majority of real attacks. It is cheaper and easier than defeating technology."),
                    ("A genius cracks the firewall with clever code", False,
                     "That is the movie version. It is rare and expensive. Attackers go for the busy human first."),
                    ("A virus simply appears out of nowhere", False,
                     "Malware still needs a way in, usually a person clicking or installing something. It does not appear by magic."),
                    ("The internet is just unsafe and nothing can be done", False,
                     "Not so. Most attacks rely on one careless moment, which a trained eye and a few habits prevent."),
                ],
            },
            {
                "key": "attack-respond",
                "kind": "respond",
                "points": 2,
                "title": "When someone tries it on you",
                "body": "<p>Social engineering happens in the moment, on a normal busy "
                "day. Three approaches land at your desk this week. For each, choose "
                "your response and see how it plays out.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> anyone who "
                "creates urgency and asks you to skip your normal checks is worth a "
                "second, slower look.</div>",
                "payload": {
                    "prompt": "Choose the soundest response for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "itcall",
                            "text": "A caller says they are from IT support, there is an urgent problem with your account, and they just need your password to fix it.",
                            "options": [
                                {"text": "Do not give it out, hang up, and check with your real IT contact", "outcome": "good",
                                 "feedback": "Right. Real IT never needs your password. Verify on a number you already have, not one the caller gave you."},
                                {"text": "Give the password so the problem gets fixed quickly", "outcome": "bad",
                                 "feedback": "That hands your account straight to an attacker. No genuine IT process asks for your password."},
                                {"text": "Give a slightly different password to be safe", "outcome": "bad",
                                 "feedback": "Any password you share is a password you have lost. Do not share any of them."},
                            ],
                        },
                        {
                            "id": "mailbox",
                            "text": "An email warns your mailbox is full and you must log in through the link within an hour or lose access.",
                            "options": [
                                {"text": "Ignore the link and check your mailbox the normal way you always do", "outcome": "good",
                                 "feedback": "Exactly. The urgency and the link are the tell. Go to the service the way you normally reach it, never through a scary email's link."},
                                {"text": "Click the link and log in to keep your access", "outcome": "bad",
                                 "feedback": "That login page is the trap, built to capture your password. The mailbox warning is fake."},
                                {"text": "Reply to ask if the email is genuine", "outcome": "risky",
                                 "feedback": "If it is a scam, you are asking the scammer. Check the service directly instead."},
                            ],
                        },
                        {
                            "id": "usb",
                            "text": "You find a USB stick in the clinic carpark with a sticker that reads Payroll 2026.",
                            "options": [
                                {"text": "Do not plug it in, and hand it to IT or your manager", "outcome": "good",
                                 "feedback": "Yes. A tempting label on a dropped USB is classic bait. Plugging it in can install malware in seconds."},
                                {"text": "Plug it in to see whose it is so you can return it", "outcome": "bad",
                                 "feedback": "That is exactly what the attacker hopes for. The stick can infect your machine the moment it connects."},
                                {"text": "Take it home and check it on your own laptop", "outcome": "bad",
                                 "feedback": "Same trap, different computer. Do not connect an unknown USB to any machine."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "invoice-scam",
                "kind": "check",
                "points": 2,
                "title": "Read the email like an investigator",
                "diagram": "email-invoice",
                "body": "<p>Here is the attack that quietly costs Australian businesses "
                "the most: a supplier's invoice that is not quite what it seems. The "
                "message above looks routine. Read it the way an investigator would, "
                "starting with who it is really from.</p>"
                "<div class=\"cy-callout\">Two things matter most on any payment "
                "email: the real sender address (not just the friendly name), and "
                "whether it is quietly asking you to change where the money goes.</div>",
                "question": "Looking at this email, what is the strongest sign it is an attack?",
                "hint": "Read the sender address, and what it is asking you to change.",
                "options": [
                    ("The sender is a lookalike domain and it quietly changes the bank account", True,
                     "Right. The address is bunya-supplies-billing.com, a lookalike, and it asks you to pay a new account by Friday. A changed account plus urgency is the classic invoice scam. Verify by phone on a number you already have."),
                    ("It has an attachment", False,
                     "Genuine invoices have attachments too. On its own that is not the tell. The giveaway is the lookalike sender and the changed bank details."),
                    ("It was sent on a Thursday", False,
                     "The day means nothing. Real and fake invoices both arrive on weekdays."),
                    ("It is addressed to the accounts inbox", False,
                     "Emailing the accounts inbox is normal. The problem is the fake sender and the quietly changed account number."),
                ],
            },
            {
                "key": "attack-quizset",
                "kind": "quizset",
                "points": 2,
                "title": "Name the trick",
                "body": "<p>Four quick questions to lock in how attacks get in and what "
                "each one leans on. Every one of them aims at a person, not a machine, "
                "so read each carefully and pick out the human tell. Answer all four to "
                "finish.</p>",
                "payload": {
                    "prompt": "Answer all four to complete the task. A wrong answer just lets you try again.",
                    "questions": [
                        {"type": "mcq",
                         "q": "A text message pretends to be from a delivery company and rushes you to pay a small fee. What kind of attack is this?",
                         "hint": "It targets a person, through a message, with urgency.",
                         "options": [
                             ["Phishing (social engineering by message)", True, "Yes. A fake message that rushes you into acting is phishing, a form of social engineering."],
                             ["A firewall failure", False, "Firewalls filter network traffic. This is a message aimed at a person."],
                             ["A power cut", False, "Not a security attack at all."],
                             ["A software bug", False, "No software flaw is involved. It is a trick aimed at you."]
                         ]},
                        {"type": "truefalse",
                         "q": "True or false: good antivirus on its own will stop a staff member being talked into sharing their password.",
                         "answer": False,
                         "hint": "What does antivirus actually watch?",
                         "why": "False. Antivirus scans files and software. It cannot stop a person being persuaded to hand over a password. That takes a careful human."},
                        {"type": "fill",
                         "q": "Tricking a person into acting against their own interest is called social ___ . (one word)",
                         "answer": "engineering",
                         "accept": ["social engineering"],
                         "hint": "It rhymes with steering.",
                         "why": "Correct. Social engineering: the human side of an attack, where trust and urgency are the weapons."},
                        {"type": "match",
                         "q": "Match each attack to what it really targets.",
                         "hint": "Each one leans on a human moment, not a machine.",
                         "why": "That is the pattern: attacks aim at trust, urgency and a quick click, not at clever code.",
                         "pairs": [
                             ["Phishing email", "Your inbox and a quick click"],
                             ["Fake IT phone call", "Your trust in authority"],
                             ["Dropped USB stick", "Your curiosity"]
                         ]}
                    ]
                },
            },
            {
                "key": "attack-applied",
                "kind": "check",
                "points": 2,
                "title": "Prove you have got it",
                "body": "<p>One applied situation to finish. Read it, then choose the "
                "response that shows you understand how attacks really work.</p>"
                "<div class=\"cy-callout\">A staff member gets a call: the bank's fraud "
                "team, very polite, says there is suspicious activity and reads out "
                "the first few digits of the company card to prove they are genuine. "
                "They ask for the rest of the number to block the fraud.</div>",
                "question": "What is the safe response, and why?",
                "hint": "Knowing a few digits is not proof. Who called whom?",
                "options": [
                    ("Hang up and ring the bank on the number from your own records", True,
                     "Right. A caller reading a few known digits is a trick to earn trust. A real bank never needs you to read out the full card. Verify by calling the bank yourself on a number you already trust."),
                    ("Read out the rest of the number so the fraud gets blocked", False,
                     "That hands the whole card to the attacker. The urgency and the partial digits are the con."),
                    ("Give the number but only if they sound professional", False,
                     "Sounding professional is the whole act. Politeness is not proof. Call the bank back yourself."),
                    ("Put them on hold and ask a colleague what to do", False,
                     "Better than complying, but the clean answer is simple: hang up and call the bank on a trusted number. Do not stay on the attacker's call."),
                ],
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. A bank of 40 (draw 10 at random), ten per lesson. Four options each,
# exactly one correct, and every option carries an explanation that teaches (why
# right, why wrong). This is the fuel for the Adaptive Feedback Engine. Same
# house voice as the lessons: warm, plain, no em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: What a network is, and what you protect ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "In plain terms, what is a computer network?",
            "options": [
                ("Devices connected so they can share information, like the front desk PC, the printer and the eftpos machine talking through the router", True,
                 "Yes. A network is just devices linked together to share information, usually through a router and out to the internet."),
                ("A single powerful computer that runs the whole business", False,
                 "No. A network is many devices connected together, not one big machine."),
                ("The antivirus software installed on a computer", False,
                 "No. That is a defence on one device. A network is the devices linked together."),
                ("The password you use to log in each morning", False,
                 "No. A password protects an account. A network is the connected devices themselves."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What do the three letters in the CIA triad stand for?",
            "options": [
                ("Confidentiality, Integrity, Availability", True,
                 "Yes. The three things security protects: keeping data private, keeping it correct, and keeping it reachable when you need it."),
                ("Control, Internet, Access", False,
                 "No. The CIA triad is Confidentiality, Integrity and Availability."),
                ("Computers, Internet, Applications", False,
                 "No. Those are just parts of a system. The triad is Confidentiality, Integrity, Availability."),
                ("Certificates, Identity, Authentication", False,
                 "No. Useful terms, but not the triad. It is Confidentiality, Integrity, Availability."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A staff member accidentally emails the day's patient list to the wrong outside address. Which pillar of the CIA triad has failed?",
            "options": [
                ("Confidentiality, because private information reached someone who should not have it", True,
                 "Yes. The data was neither lost nor changed, but it was exposed to the wrong person, which is a confidentiality failure."),
                ("Availability, because the files can no longer be opened", False,
                 "No. The files are still available. The problem is that private data was exposed, a confidentiality failure."),
                ("Integrity, because the data was secretly altered", False,
                 "No. Nothing was changed. Private data simply reached the wrong person, which is a confidentiality failure."),
                ("None, because sending an email is always safe", False,
                 "No. Sending sensitive data to the wrong address is a real confidentiality breach."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A work login page shows the padlock and https in the address bar. What does that actually tell you?",
            "options": [
                ("The connection is encrypted, so someone on the same network cannot read what you type, though it is not proof the site itself is genuine", True,
                 "Yes. The padlock means the link is encrypted in transit. It does not, on its own, prove the website is who it claims to be."),
                ("The website has been checked and is guaranteed safe and genuine", False,
                 "No. The padlock only means the connection is encrypted. Scam sites can show a padlock too."),
                ("Your password can never be stolen on this site", False,
                 "No. Encryption protects the connection, not against you typing your password into a fake page."),
                ("The site has no viruses on it", False,
                 "No. The padlock says nothing about malware. It only means the connection is encrypted."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "You open the router's settings page and see the admin password is still 'admin'. What is the problem, and the fix?",
            "options": [
                ("Default passwords like 'admin' are published online for anyone to look up, so change it to something strong straight away", True,
                 "Yes. Factory-default passwords are public knowledge, so anyone can log in and change your settings. Changing it is the single most important fix."),
                ("Nothing is wrong; 'admin' is a strong, secure password", False,
                 "No. 'admin' is the factory default, listed online for anyone to find. It must be changed."),
                ("The router is broken and needs replacing", False,
                 "No. The router is fine. The default password just needs changing to something strong."),
                ("You should turn the router off to stay safe", False,
                 "No. That takes the whole network offline. The fix is to change the default password."),
            ],
        },
        # ---- Lesson 2: How attacks actually happen ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is social engineering?",
            "options": [
                ("Tricking a person into clicking, paying or sharing something, rather than defeating the technology", True,
                 "Yes. Social engineering targets a busy, trusting human. It is cheaper and easier for attackers than breaking the technology."),
                ("A way of building stronger computer networks", False,
                 "No. It is an attack technique aimed at people, not a way of building networks."),
                ("A type of antivirus software", False,
                 "No. It is not a defence. It is the human-focused trick attackers use."),
                ("Fixing social media privacy settings", False,
                 "No. It is an attack on people, not a privacy setting."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A caller says they are from IT support, there is an urgent problem with your account, and they just need your password to fix it. What should you do?",
            "options": [
                ("Do not give it out, hang up, and check with your real IT contact on a number you already have", True,
                 "Yes. Genuine IT never needs your password. Verify on a number you already trust, not one the caller gave you."),
                ("Read out your password so the urgent problem gets fixed", False,
                 "No. That hands your account to an attacker. No real IT process asks for your password."),
                ("Give a slightly different password to be safe", False,
                 "No. Any password you share is a password you have lost. Do not share any of them."),
                ("Ask the caller to prove who they are, then share it if they sound professional", False,
                 "No. Sounding professional is the whole act. Never share a password, however convincing the caller is."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "An email from a regular supplier says their bank account has changed and this month's invoice must go to a new account today. What is the safe response?",
            "options": [
                ("Ring the supplier on a number you already have and confirm the change before paying anything", True,
                 "Yes. A changed bank account plus time pressure is the classic invoice scam. Verify through a channel you already trust, never through the email."),
                ("Pay the new account quickly so the invoice is not late", False,
                 "No. That sends the money to a stranger. A changed account always deserves a phone call to a known number first."),
                ("Reply to the email to ask whether the new account is genuine", False,
                 "No. If it is a scam, you are asking the scammer, who will say yes. Verify a different way."),
                ("Forward it to a colleague and let them decide", False,
                 "No. That just moves the risk. Verify the change on a number you already have before any payment."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "A caller claims to be your bank's fraud team, reads out the first few digits of your company card to prove it, and asks you to confirm the rest. What should you do?",
            "options": [
                ("Hang up and call the bank back on the number from your card or statement", True,
                 "Yes. Knowing a few digits is a trick to earn trust. A real bank never needs you to read out the full number. Verify by calling them yourself."),
                ("Read out the rest of the number so the fraud can be blocked", False,
                 "No. That hands the whole card to the attacker. The partial digits and urgency are the con."),
                ("Give the number because they clearly already have your details", False,
                 "No. A few digits is not proof they are genuine. Hang up and call the bank on a trusted number."),
                ("Stay on the line and ask them to email you instead", False,
                 "No. Do not keep engaging. Hang up and call the bank yourself on a number you already trust."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Which of these best describes how most attacks on a small business actually begin?",
            "options": [
                ("Someone is tricked, in a busy moment, into clicking, paying or sharing a password", True,
                 "Yes. The great majority of real attacks start with human error, because it is cheaper and easier than defeating the technology."),
                ("A genius cracks the firewall with clever code", False,
                 "No. That is the movie version. Attackers go for the busy human first."),
                ("A virus simply appears out of nowhere", False,
                 "No. Malware still needs a way in, usually a person clicking or installing something."),
                ("The internet is inherently unsafe and nothing can be done", False,
                 "No. Most attacks rely on one careless moment, which a trained eye and a few habits prevent."),
            ],
        },
    ],
}
