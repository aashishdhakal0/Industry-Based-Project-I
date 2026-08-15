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
    {
        "title": "Locking your front door",
        "reading_time_minutes": 7,
        "intro": "You do not need to be technical to be hard to attack. Meet the "
        "handful of everyday locks that close the doors attackers rely on.",
        "tasks": [
            {
                "key": "the-four-locks",
                "kind": "check",
                "points": 2,
                "title": "The four locks that stop most attacks",
                "body": "<p>Being hard to attack comes down to four plain habits, none "
                "of them clever. <strong>Keep things updated</strong> so known holes "
                "are patched. <strong>Use strong, unique passwords</strong> (a "
                "password manager remembers them for you). <strong>Turn on two-factor "
                "authentication</strong> so a stolen password alone is not enough. And "
                "<strong>keep a tested backup</strong> so an attack or mistake never "
                "costs you your work.</p>"
                "<div class=\"cy-callout\">Each lock is simple. Together they shut the "
                "doors that nearly every attack walks through.</div>",
                "question": "Which habit does the most to stop a stolen password from becoming a break-in?",
                "hint": "What still stands in the way even after a password leaks?",
                "options": [
                    ("Two-factor authentication", True,
                     "Yes. With two-factor on, a thief with your password still cannot get in without the second code from your phone. It is the single best defence against leaked passwords."),
                    ("Changing your desktop wallpaper", False,
                     "Pleasant, but it does nothing for security. Two-factor is the real lock here."),
                    ("Using a shorter password so you remember it", False,
                     "Shorter is weaker, and easier to guess or crack. Length and a second factor are what help."),
                    ("Turning the computer off at night", False,
                     "Sensible for power bills, but it does not stop a leaked password being used from anywhere. Two-factor does."),
                ],
            },
            {
                "key": "protect-respond",
                "kind": "respond",
                "points": 2,
                "title": "Everyday choices that keep you safe",
                "body": "<p>Protection is not one big project. It is a series of small "
                "choices you make on ordinary days. Here are three. Pick the safer "
                "option each time.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> when a quick, "
                "slightly annoying safe option sits next to an easy risky one, take "
                "the annoying one. It is almost always worth it.</div>",
                "payload": {
                    "prompt": "Choose the safer option for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "password",
                            "text": "You are setting up a new work account and need a password.",
                            "options": [
                                {"text": "Use a long unique passphrase, saved in a password manager", "outcome": "good",
                                 "feedback": "Right. A long, unique passphrase is hard to crack, and the manager means you never have to remember or reuse it."},
                                {"text": "Reuse the same password you use for everything else", "outcome": "bad",
                                 "feedback": "One leak then unlocks all your accounts at once. Reused passwords are how a single breach becomes many."},
                                {"text": "Use a short simple one and change it often", "outcome": "risky",
                                 "feedback": "Short passwords are weak however often you change them, and frequent forced changes usually make people pick worse ones. Go long and unique instead."},
                            ],
                        },
                        {
                            "id": "twofactor",
                            "text": "An account offers to turn on two-factor authentication with a code to your phone.",
                            "options": [
                                {"text": "Turn it on now", "outcome": "good",
                                 "feedback": "Yes. It takes two minutes and means a stolen password alone can never log in. This is the highest-value habit here."},
                                {"text": "Skip it, it sounds like a hassle every login", "outcome": "bad",
                                 "feedback": "The tiny hassle is the point: it is the same hassle for a thief, and they do not have your phone. Turn it on."},
                                {"text": "Turn it on only for the email account", "outcome": "risky",
                                 "feedback": "Email first is a good start (it can reset your other passwords), but turn it on everywhere it is offered."},
                            ],
                        },
                        {
                            "id": "update",
                            "text": "A notice says a security update is ready and asks to restart.",
                            "options": [
                                {"text": "Install it soon, or let updates install automatically", "outcome": "good",
                                 "feedback": "Right. Updates patch the exact holes attackers use. Automatic updates mean you never have to remember."},
                                {"text": "Click 'remind me later' every time", "outcome": "bad",
                                 "feedback": "Forever-later leaves a known, published hole open on your machine. Install security updates promptly."},
                                {"text": "Ignore it, if it still works it is fine", "outcome": "bad",
                                 "feedback": "Working and safe are different. An unpatched machine is a favourite target. Keep it updated."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "settings-check",
                "kind": "check",
                "points": 2,
                "title": "Read the security settings",
                "diagram": "security-settings",
                "body": "<p>Most accounts have a security page that tells you, at a "
                "glance, how well protected you are. You do not need to be technical to "
                "read it. Above is a staff member's account. Read each row and find the "
                "weakest link.</p>"
                "<div class=\"cy-callout\">When you check a security page, the first "
                "thing to look for is whether two-factor authentication is on. It is "
                "the lock that matters most.</div>",
                "question": "Looking at these settings, what is the most important thing to fix first?",
                "hint": "Which single setting, if switched on, best protects a leaked password?",
                "options": [
                    ("Turn on two-factor authentication, which is currently Off", True,
                     "Right. With two-factor Off, a leaked password is a straight way in. Turning it on is the single biggest improvement here, ahead of the ageing password."),
                    ("Turn off login alerts", False,
                     "Login alerts are a good thing: they warn you of a strange sign-in. Leave them on. The real gap is two-factor being Off."),
                    ("Nothing, these settings are fine", False,
                     "Two-factor is Off and the password is three years old. There is real work to do, starting with two-factor."),
                    ("Delete the recovery email", False,
                     "A recovery email is useful; a personal Gmail is not ideal but not the priority. Turning on two-factor comes first."),
                ],
            },
            {
                "key": "protect-quizset",
                "kind": "quizset",
                "points": 2,
                "title": "Lock it in",
                "body": "<p>Four quick questions on the everyday habits that keep your "
                "front door shut: strong passwords, two-factor, updates and backups. "
                "None of them is clever, and together they do most of the heavy "
                "lifting. Answer all four to finish.</p>",
                "payload": {
                    "prompt": "Answer all four to complete the task. A wrong answer just lets you try again.",
                    "questions": [
                        {"type": "mcq",
                         "q": "Which makes the strongest password?",
                         "hint": "Length beats complexity for a password you must also be able to use.",
                         "options": [
                             ["A long passphrase like 'brave-otter-canoe-lantern'", True, "Yes. Length is what makes a password hard to crack, and a few random words are both strong and usable."],
                             ["A short one with symbols like 'P@ss1'", False, "Short passwords are quick to crack even with symbols. Length matters more."],
                             ["Your business name and the year", False, "Guessable in seconds. Anything about you is a weak choice."],
                             ["The word 'password' spelt backwards", False, "Attackers try every obvious trick like this first."]
                         ]},
                        {"type": "truefalse",
                         "q": "True or false: once two-factor is on, the password itself no longer matters.",
                         "answer": False,
                         "hint": "Two-factor is a second lock, not a replacement for the first.",
                         "why": "False. Two-factor is a powerful second lock, but a weak or reused password still puts you at risk. Use both: a strong password and two-factor."},
                        {"type": "fill",
                         "q": "A tested ___ is what lets you recover your files after ransomware or a mistake. (one word)",
                         "answer": "backup",
                         "accept": ["backups"],
                         "hint": "A spare copy you can restore from.",
                         "why": "Correct. A tested backup means an attack or accident never costs you your work: you restore and carry on."},
                        {"type": "match",
                         "q": "Match each habit to the danger it defends against.",
                         "hint": "Each lock is aimed at a different threat.",
                         "why": "That is the set: updates, two-factor and backups each shut a different door.",
                         "pairs": [
                             ["Installing updates", "Known holes attackers exploit"],
                             ["Two-factor authentication", "A stolen or leaked password"],
                             ["A tested backup", "Ransomware and lost files"]
                         ]}
                    ]
                },
            },
            {
                "key": "protect-applied",
                "kind": "check",
                "points": 2,
                "title": "Prove you have got it",
                "body": "<p>One applied decision to finish. Read the setup, then pick the "
                "change that protects the most.</p>"
                "<div class=\"cy-callout\">A cafe owner uses the same password for "
                "email, banking and the booking system, and has never turned on "
                "two-factor. They are short on time and can make exactly one change "
                "this week.</div>",
                "question": "Which single change protects them most if that shared password ever leaks?",
                "hint": "What stops a known password from being enough on its own?",
                "options": [
                    ("Turn on two-factor authentication on the important accounts", True,
                     "Right. If the password leaks, two-factor means it is still not enough to log in without the code on their phone. It buys the most safety for one change. Unique passwords should follow."),
                    ("Change the shared password to a new shared password", False,
                     "Still one password for everything, so one future leak still opens all of it. Two-factor helps far more, and unique passwords next."),
                    ("Write the password on a note by the till", False,
                     "That adds a new way to lose it, to anyone at the counter. The opposite of protection."),
                    ("Do nothing until they have more time", False,
                     "Two-factor takes minutes and is the highest-value move. Waiting leaves every account one leak away from a break-in."),
                ],
            },
        ],
    },
    {
        "title": "Putting it all together",
        "reading_time_minutes": 7,
        "intro": "A week at Docklands Dental, where everything you have learned gets "
        "used. Layer the habits, read the signs, and handle the bad Friday.",
        "tasks": [
            {
                "key": "layered-defence",
                "kind": "check",
                "points": 2,
                "title": "Why layers beat one big lock",
                "body": "<p>Docklands Dental is a small clinic: a busy front desk, a "
                "shared drive, patient records that must stay private, accurate and "
                "available. They do not have an IT department. What keeps them safe is "
                "not one clever measure, it is several plain habits stacked together: "
                "locked screens, strong passwords, two-factor, tested backups, and a "
                "careful eye on email.</p>"
                "<div class=\"cy-callout\">This is called defence in depth. No single "
                "lock is perfect, so you layer a few simple ones. One slip is then a "
                "nuisance, not a disaster.</div>",
                "question": "Why does layering several simple habits beat relying on one strong measure?",
                "hint": "What happens when the one measure is the thing that fails or is missed?",
                "options": [
                    ("If one habit is missed, the next still protects what matters", True,
                     "Yes. Defence in depth means a single mistake, a reused password, a missed update, is caught by another layer. One slip does not open everything."),
                    ("Because more locks look more impressive to customers", False,
                     "It is about real protection, not appearances. Layers catch the mistakes that a single measure would miss."),
                    ("Because you can then ignore all the other habits", False,
                     "The opposite. The strength comes from the habits working together, not from dropping them."),
                    ("Because one perfect lock is impossible to buy", False,
                     "True that no lock is perfect, but the point is that layers cover each other's gaps, not that you gave up on a perfect one."),
                ],
            },
            {
                "key": "week-respond",
                "kind": "respond",
                "points": 2,
                "title": "Three moments in the week",
                "body": "<p>Over one ordinary week at Docklands Dental, three little "
                "moments decide whether a small problem stays small. You are on the "
                "front desk. Choose your move each time.</p>"
                "<div class=\"cy-callout\"><strong>Remember:</strong> your first move "
                "decides how far a problem spreads. Contain and verify beat speed and "
                "trust every time.</div>",
                "payload": {
                    "prompt": "Choose the soundest move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "bankchange",
                            "text": "An email, apparently from a supplier, urgently asks you to change their bank details before you pay this month's invoice.",
                            "options": [
                                {"text": "Ring the supplier on a number you already have and confirm", "outcome": "good",
                                 "feedback": "Right. A changed bank account plus urgency is the classic invoice scam. Verify on a channel you already trust, not the email."},
                                {"text": "Update the details and pay, the email looks genuine", "outcome": "bad",
                                 "feedback": "A convincing look is the whole trick. Never change payment details on the say-so of an email alone."},
                                {"text": "Reply to the email to double-check", "outcome": "risky",
                                 "feedback": "If the email is fake, you are asking the scammer. Phone the supplier on a known number instead."},
                            ],
                        },
                        {
                            "id": "unlocked",
                            "text": "You notice the reception laptop has been left unlocked and unattended, with a patient record on screen, facing the waiting room.",
                            "options": [
                                {"text": "Lock it straight away and remind the team to lock screens", "outcome": "good",
                                 "feedback": "Yes. An unlocked screen in a public space is a confidentiality leak anyone can read. Locking screens is a two-second habit worth building."},
                                {"text": "Leave it, you will be back in a minute", "outcome": "bad",
                                 "feedback": "A minute is long enough for a waiting patient to read or photograph private records. Lock it now."},
                                {"text": "Turn the screen brightness down", "outcome": "bad",
                                 "feedback": "It is still readable, and still logged in. Lock the screen instead."},
                            ],
                        },
                        {
                            "id": "overseas",
                            "text": "A staff member's account shows a login alert from another country overnight, when nobody was working.",
                            "options": [
                                {"text": "Treat it as a likely break-in: change the password, check two-factor, and report it", "outcome": "good",
                                 "feedback": "Right. An unexpected overseas login is a red flag. Lock the account down fast and report it, before the intruder does more."},
                                {"text": "Assume it is a glitch and carry on", "outcome": "bad",
                                 "feedback": "Login alerts exist precisely so you act on them. Assuming it is nothing is how a foothold becomes a full breach."},
                                {"text": "Wait to see if it happens again", "outcome": "bad",
                                 "feedback": "Waiting gives an intruder more time. Change the password and check two-factor now."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "device-gap",
                "kind": "check",
                "points": 2,
                "title": "Find the gap on the laptop",
                "diagram": "device-checklist",
                "body": "<p>Before the clinic closes on Friday, you run a quick security "
                "check on the reception laptop. Most of it is in good shape. Read the "
                "four rows above and find the one that still needs attention.</p>"
                "<div class=\"cy-callout\">A tick is a lock that is on. A cross is a "
                "door left open. On a laptop that leaves the building, the open door "
                "matters most.</div>",
                "question": "Looking at the reception laptop's check, what is the remaining gap?",
                "hint": "Three rows are ticked. One is not.",
                "options": [
                    ("Disk encryption is Off", True,
                     "Right. Without disk encryption, if the laptop is lost or stolen its files can be read straight off the drive, patient records and all. Turning it on means a thief gets a useless brick."),
                    ("Screen lock is On", False,
                     "That is a good thing, not a gap. A locked screen stops a passer-by reading it."),
                    ("Automatic updates are On", False,
                     "Also good. Updates patch known holes. The gap is disk encryption being Off."),
                    ("Backup is On", False,
                     "Good again. A backup means you can recover. The one thing not done is disk encryption."),
                ],
            },
            {
                "key": "capstone-quizset",
                "kind": "quizset",
                "points": 2,
                "title": "The whole module, in four",
                "body": "<p>Four questions that pull the whole of Module 1 together: "
                "what you are protecting, how attacks actually come at you, and the "
                "plain habits that stop them. Take your time and answer each one to "
                "finish.</p>",
                "payload": {
                    "prompt": "Answer all four to complete the task. A wrong answer just lets you try again.",
                    "questions": [
                        {"type": "mcq",
                         "q": "A tested backup protects mainly which of the three pillars, Confidentiality, Integrity or Availability?",
                         "hint": "A backup gives you your files back after they are locked or lost.",
                         "options": [
                             ["Availability", True, "Yes. A backup restores access after ransomware or a crash, so your data stays available when you need it."],
                             ["Confidentiality", False, "Confidentiality is about who can see the data. A backup does not control that; it restores access."],
                             ["Integrity", False, "Integrity is about data being unaltered. A backup mainly protects your ability to get the data back, which is availability."],
                             ["None of them", False, "A backup squarely protects availability, and it matters a great deal."]
                         ]},
                        {"type": "truefalse",
                         "q": "True or false: locking your screen when you step away protects the confidentiality of what is on it.",
                         "answer": True,
                         "hint": "Who can see the screen once it is locked?",
                         "why": "True. A locked screen stops anyone nearby reading private information. That is confidentiality: only the right people can see it."},
                        {"type": "fill",
                         "q": "Tricking a person into acting against their own interest is called social ___ . (one word)",
                         "answer": "engineering",
                         "accept": ["social engineering"],
                         "hint": "The same word from Lesson 2.",
                         "why": "Correct. Social engineering is the human side of most attacks, and a careful eye is its best defence."},
                        {"type": "match",
                         "q": "Match each habit to the main threat it defends against.",
                         "hint": "Each habit shuts a different door.",
                         "why": "That is the layered defence of Module 1: several plain habits, each covering a different risk.",
                         "pairs": [
                             ["Two-factor authentication", "A stolen password"],
                             ["A tested backup", "Ransomware"],
                             ["A careful eye on email", "Phishing and scams"]
                         ]}
                    ]
                },
            },
            {
                "key": "capstone-applied",
                "kind": "check",
                "points": 2,
                "title": "The bad Friday",
                "body": "<p>The gate before the quiz. It is a bad Friday at Docklands "
                "Dental, and everything you have learned is on the line. Read it, then "
                "choose the right first move.</p>"
                "<div class=\"cy-callout\">Late Friday, a staff member opens the shared "
                "drive to find every file renamed and a note on screen demanding "
                "payment in cryptocurrency to unlock them. The clinic has tested "
                "backups from last night.</div>",
                "question": "What is the right first move?",
                "hint": "Before recovering anything, what stops the problem spreading to other machines?",
                "options": [
                    ("Disconnect the affected computer from the network, then report it", True,
                     "Right. Getting it off the network first stops the ransomware spreading to other machines and the shared drive. Then you report it and recover from last night's backup. Containment comes before recovery."),
                    ("Pay the ransom quickly to get the files back", False,
                     "Paying is unreliable, funds crime, and marks you as a payer. With tested backups you never need to. Contain first, then restore."),
                    ("Keep working on other files and deal with it Monday", False,
                     "Every minute it stays connected, more machines and files are locked. Disconnect and act now."),
                    ("Delete the ransom note and hope it clears", False,
                     "The note is not the problem; the encryption is, and it is still spreading. Disconnect the machine and recover from backup."),
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
        # ---- Lesson 1: networks and the CIA triad ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "In plain terms, what is a computer network?",
            "options": [
                ("Two or more devices connected so they can share information", True,
                 "Yes. From two machines to the whole internet, a network is just devices connected to share information."),
                ("A single computer with a fast processor", False,
                 "Not quite. One computer on its own is not a network. It is the connection between devices that makes one."),
                ("A type of antivirus program", False,
                 "No. Antivirus protects a single device. It is not what a network is."),
                ("The password you use to log in", False,
                 "No. A password controls who gets access, but it is not the network itself."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Your information is 'in transit' when it is:",
            "options": [
                ("Moving across the network, like an email on its way to someone", True,
                 "That is it. In transit means the information is travelling, which is when it can be intercepted if it is not protected."),
                ("Saved on a hard drive that is switched off", False,
                 "That is 'at rest', sitting in storage rather than moving."),
                ("Printed out and filed in a drawer", False,
                 "That is a paper copy at rest, not data moving across a network."),
                ("Deleted from your computer", False,
                 "Deleted data is not in transit. In transit means actively moving from one place to another."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What do the letters in the CIA triad stand for?",
            "options": [
                ("Confidentiality, Integrity and Availability", True,
                 "Correct. These are the three things security protects, and most decisions come back to one of them."),
                ("Computers, Internet and Applications", False,
                 "No. The triad is about what you protect, not a list of equipment."),
                ("Control, Inspection and Access", False,
                 "These sound plausible but they are not it. The triad is Confidentiality, Integrity and Availability."),
                ("Confidential Intelligence Agency", False,
                 "Despite the initials, the CIA triad has nothing to do with any spy agency."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Putting a password on a spreadsheet of customer details mainly protects:",
            "options": [
                ("Confidentiality, keeping it from people who should not see it", True,
                 "Yes. Limiting who can open the file is a confidentiality control."),
                ("Availability, keeping it online", False,
                 "No. A password does not keep a file available. It limits who can read it."),
                ("Integrity, proving it was not changed", False,
                 "Not the main point. A password limits access, which is confidentiality."),
                ("Nothing, because spreadsheets cannot be protected", False,
                 "They can. A password is a simple but real confidentiality control."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "An invoice's bank details are secretly changed so a payment goes to a stranger. Which pillar failed?",
            "options": [
                ("Integrity, the information was altered without permission", True,
                 "Right. The file still opens, but its accuracy is gone. That is an integrity failure, and a common way money goes missing."),
                ("Availability, the file cannot be opened", False,
                 "No. Availability is about whether you can reach something. Here the file opens fine, it was just tampered with."),
                ("Confidentiality, someone saw what they should not", False,
                 "Not quite. The problem is not who saw it, it is that the details were changed. That is integrity."),
                ("None of them, this is not a security issue", False,
                 "It very much is. Altering financial details without permission is a failure of integrity."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Keeping a restorable backup of your files mainly protects which pillar?",
            "options": [
                ("Availability, you can still get your information when you need it", True,
                 "Yes. A backup means an attack or a mistake does not cost you access to your work."),
                ("Confidentiality, it hides the files", False,
                 "No. A backup does not hide anything. It makes sure you can get your data back."),
                ("Integrity, it proves nothing changed", False,
                 "Not the main point. Backups are chiefly about restoring access, which is availability."),
                ("Backups are not really a security control", False,
                 "They are a core one. They protect availability against ransomware and honest mistakes alike."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Which of these is NOT one of the three things the CIA triad protects?",
            "options": [
                ("Speed", True,
                 "Correct, speed is not part of it. The three are Confidentiality, Integrity and Availability."),
                ("Confidentiality", False,
                 "That is one of the three, keeping information from the wrong eyes."),
                ("Integrity", False,
                 "That is one of the three, information not being tampered with."),
                ("Availability", False,
                 "That is one of the three, information being there when you need it."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Which part of a workplace network connects your devices to the internet and passes messages between them?",
            "options": [
                ("The router", True,
                 "Yes. The router is the box that links your devices to each other and out to the internet. Almost everything passes through it."),
                ("The printer", False,
                 "A printer is just one device on the network. It does not connect the office to the internet."),
                ("The antivirus program", False,
                 "Antivirus protects a single device. It is not what connects the network to the internet."),
                ("The spreadsheet software", False,
                 "That is an application you run. It has nothing to do with connecting the network."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A file is perfectly safe on a locked laptop, then a staff member emails it to a supplier. What has changed about the risk?",
            "options": [
                ("The information is now in transit, so it needs different protection than when it sat at rest", True,
                 "Exactly. Moving it across the network changes its state to in transit, which is the moment it can be intercepted or misdirected."),
                ("Nothing, a safe file stays safe wherever it goes", False,
                 "Not so. Once it leaves the laptop it is in transit, a different situation with different risks, like being sent to the wrong person."),
                ("It is now permanently deleted from the laptop", False,
                 "Emailing a copy does not delete the original. The change is that the copy is now moving across the network."),
                ("It becomes impossible to read", False,
                 "It is still perfectly readable. The point is that it is now travelling, which is when in-transit risks apply."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "A stranger reads confidential figures over an employee's shoulder at a shared front desk. Which state was the information in, and which pillar failed?",
            "options": [
                ("In use, and confidentiality failed", True,
                 "Yes. Open on a screen means the data was in use, and someone who should not see it did, which is a confidentiality failure."),
                ("At rest, and availability failed", False,
                 "It was on screen, so it was in use, not at rest, and nobody lost access, so availability did not fail."),
                ("In transit, and integrity failed", False,
                 "It was not moving across the network, and nothing was altered. It was in use, and confidentiality failed."),
                ("In use, and availability failed", False,
                 "The state is right, but nobody was locked out. The problem is that someone saw it, which is confidentiality."),
            ],
        },
        # ---- Lesson 2: attacks, phishing, human error ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is phishing?",
            "options": [
                ("A message pretending to be someone you trust, to trick you into clicking or sharing details", True,
                 "Yes. It leans on trust, and it is the most common way organisations get caught out."),
                ("A way of speeding up your internet connection", False,
                 "No. Phishing has nothing to do with speed. It is a con."),
                ("A tool that backs up your files", False,
                 "No. That is a backup. Phishing is a trick message."),
                ("A setting on your router", False,
                 "No. Phishing arrives as a message. It is not a router setting."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Across the organisations that get attacked, what is the single biggest risk?",
            "options": [
                ("Human error, the everyday slips like clicking a link or reusing a password", True,
                 "Right. Most incidents involve an ordinary human action, which is why calm habits matter more than any product."),
                ("Old printers", False,
                 "Any device can be a weak point, but the biggest risk overall is human error."),
                ("Having too many backups", False,
                 "Backups are a good thing. They are never the risk."),
                ("Using a router at all", False,
                 "Routers are essential. The biggest risk is everyday human error, not the equipment."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why do scam messages so often push a tight deadline?",
            "options": [
                ("Urgency rushes you, so you act before you have time to think or check", True,
                 "Exactly. The pressure is the point. Slowing down for a moment is one of your best defences."),
                ("Deadlines are required by law on invoices", False,
                 "No. The deadline is a pressure tactic, not a legal requirement."),
                ("It makes the email arrive faster", False,
                 "No. A deadline in the text does nothing to delivery. It is there to hurry you."),
                ("Genuine senders always demand immediate payment", False,
                 "They usually do not. A sudden 'pay now or else' is a warning sign, not normal business."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "An email from 'service@auspost-delivery.info' claims to be Australia Post. What is the clearest tell?",
            "options": [
                ("The domain is not auspost.com.au, it is a lookalike", True,
                 "Yes. The sender's domain is the real giveaway, a lookalike built to pass a quick glance."),
                ("It mentions a parcel", False,
                 "Plenty of genuine messages mention parcels. That alone is not a tell."),
                ("It is written in English", False,
                 "Language is not the tell. The lookalike domain is."),
                ("It arrived in the morning", False,
                 "Timing tells you nothing about whether a message is genuine."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Ransomware is a type of:",
            "options": [
                ("Malware that locks up your files and demands payment to unlock them", True,
                 "Yes, and a tested backup is what lets you recover without paying."),
                ("Strong password", False,
                 "No. Ransomware is harmful software, not a password."),
                ("Wi-Fi encryption setting", False,
                 "No. That is unrelated. Ransomware is malware that holds files hostage."),
                ("Backup tool", False,
                 "The opposite. Backups are your defence against ransomware."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why do attackers target small businesses, councils and schools?",
            "options": [
                ("Automated tools look for any unlocked door, and smaller places often have lighter defences", True,
                 "Right. Attacks are largely automated and opportunistic. Being small does not mean being safe."),
                ("They are too small to be worth attacking", False,
                 "This is the dangerous myth. Smaller organisations are targeted precisely because defences are often lighter."),
                ("They never hold anything valuable", False,
                 "They hold plenty, from customer details to payment information."),
                ("Attackers hand pick each victim by name", False,
                 "Most attacks are automated and untargeted, knocking on thousands of doors at once."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "An email says pay an overdue invoice within the hour to a new account. Safest first step?",
            "options": [
                ("Pause, and check by phoning a number you already have", True,
                 "Yes. Urgency plus a change of bank details is the classic invoice scam. Confirm on a channel you already trust."),
                ("Pay immediately so the account is not closed", False,
                 "No. Acting fast is exactly what the scammer wants. The deadline is there to stop you thinking."),
                ("Reply to the email and ask if it is genuine", False,
                 "Risky. If it is a scam you are asking the scammer, who will happily say yes."),
                ("Click the link to view the invoice", False,
                 "No. An unexpected link is often where the trouble starts. Verify before you click."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A scam is sent by text message rather than email. What is this called, and are the warning signs different?",
            "options": [
                ("Smishing, and the tells are the same: a lookalike link, a small fee or threat, and pressure to act now", True,
                 "Yes. SMS phishing is called smishing, and although it feels more personal, the giveaways are exactly the same as in a scam email."),
                ("It is harmless, because texts cannot contain scams", False,
                 "Texts absolutely carry scams. A message on your phone can be just as fake as an email."),
                ("Smishing, and you should always tap the link to check where it goes", False,
                 "The name is right, but never tap the link to check. Open the real website yourself instead."),
                ("Vishing, and it only ever happens over the phone", False,
                 "A scam text is smishing. Vishing is a voice-call scam, which is a different channel."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Why is it risky to click the link inside an unexpected 'parcel on hold' message?",
            "options": [
                ("The link usually leads to a lookalike site built to capture your details or payment", True,
                 "Right. The link is the hook. It sends you to a fake page. Go to the carrier's real website yourself instead."),
                ("Clicking links uses up your mobile data allowance", False,
                 "Data use is not the danger. The danger is where the link takes you and what it asks for."),
                ("Parcel companies never send text messages", False,
                 "Some genuinely do, which is why scammers copy them. The safe move is to check on the real website, not to tap the link."),
                ("It will always install a virus instantly", False,
                 "It does not always install anything. More often it leads to a fake page after your login or card details."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "An email has a perfect company logo but comes from 'no-reply@trust-portal-au.com' and warns access ends in two hours. What is the safest read?",
            "options": [
                ("Treat it as a likely scam: the logo is easy to copy, but the odd domain and the deadline are two classic tells", True,
                 "Yes. A perfect logo proves nothing, while a lookalike domain and an invented deadline are two of the three tells. Verify before acting."),
                ("Trust it, because the logo is exactly right", False,
                 "A logo is trivial to copy, so a perfect one is no reassurance at all. Judge it on the domain and the pressure."),
                ("Trust it, because it has a specific deadline", False,
                 "A tight deadline is a pressure tactic, not a sign of authenticity. It is one of the warning signs, not a green light."),
                ("Reply and ask whether it is genuine", False,
                 "If it is a scam, that just asks the scammer, who will say yes. Verify through a channel you already trust."),
            ],
        },
        # ---- Lesson 3: passwords, 2FA, Wi-Fi, updates ----
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "On a new router, which password is dangerous to leave on the factory setting?",
            "options": [
                ("The admin password that changes the router's settings", True,
                 "Yes. Factory admin passwords are published online, so leaving it unchanged lets anyone take the router over."),
                ("The Wi-Fi password guests use to connect", False,
                 "Change that too, but the admin password is the critical one people forget exists."),
                ("Your email password", False,
                 "Your email password is not set on the router. The risky default here is the router's admin one."),
                ("Neither needs changing if the box is new", False,
                 "New is exactly when it is on a known default, so both should be changed, the admin one especially."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "What makes a password strongest?",
            "options": [
                ("Length, a dozen or more characters, such as a few unrelated words", True,
                 "Yes. Length beats complexity. A long passphrase is both strong and easy to remember."),
                ("Swapping a couple of letters in a short word for symbols", False,
                 "No. Something like 'P@ss1' is short and guessable. Substitutions do not rescue a short password."),
                ("Using the same strong password everywhere", False,
                 "No. Reuse means one leak unlocks everything, however strong the password is."),
                ("Your pet's name, so you will not forget it", False,
                 "No. Personal details are exactly what an attacker guesses first."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What does turning on two-factor authentication achieve?",
            "options": [
                ("A stolen password on its own is no longer enough to get in", True,
                 "Yes. The second check means a leaked password by itself will not open the door."),
                ("It makes your password impossible to steal", False,
                 "No. It does not stop a password being stolen. It makes a stolen one useless on its own."),
                ("It removes the need for a password", False,
                 "No. It works alongside your password, adding a second step rather than replacing it."),
                ("It backs up your account", False,
                 "No. Two-factor is about proving it is really you. It is not a backup."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "You notice your Wi-Fi is set to 'WEP'. What should you do?",
            "options": [
                ("Switch to WPA3 or WPA2, because WEP has been broken for years", True,
                 "Yes. WEP is easily cracked. Move to the newest option your gear supports."),
                ("Leave it, WEP is the most secure", False,
                 "No. WEP is the oldest and broken. It is the least secure of the three."),
                ("Turn encryption off to keep things simple", False,
                 "No. An open network lets anyone nearby read your traffic."),
                ("Nothing, encryption does not matter on Wi-Fi", False,
                 "It matters a lot. Unencrypted Wi-Fi exposes everything on it."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What is the main benefit of a separate guest Wi-Fi network?",
            "options": [
                ("It keeps visitors' and personal devices apart from your work devices", True,
                 "Yes. If a visitor's phone is infected, a guest network keeps that problem away from your business systems."),
                ("It makes your internet twice as fast", False,
                 "No. A guest network is about separation and safety, not speed."),
                ("It removes the need for any password", False,
                 "No. A guest network still uses a password. It simply keeps guests separate."),
                ("It automatically backs up guest files", False,
                 "No. It does not back anything up. Its job is to keep guest devices separate."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why is it worth installing software updates promptly?",
            "options": [
                ("They often fix security holes that attackers are already using", True,
                 "Yes. An update usually closes a known hole, and the gap before you install it is exactly what attackers aim for."),
                ("They always make the device faster", False,
                 "Speed is not the point. The security fixes are."),
                ("They change how the screen looks", False,
                 "Appearance is incidental. The security fixes are why prompt updates matter."),
                ("They are not needed if you have antivirus", False,
                 "No. Antivirus does not patch the holes updates fix. You want both."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "You need to log in to a work system on free cafe Wi-Fi. Safest choice?",
            "options": [
                ("Use your phone's mobile data or a trusted VPN instead", True,
                 "Yes. On a network you do not control, use mobile data or a trusted VPN for anything sensitive."),
                ("Go ahead, cafe Wi-Fi is always safe", False,
                 "No. You cannot be sure who else is on public Wi-Fi or what they can see. Treat it as a public space."),
                ("Just make sure the cafe is busy", False,
                 "How many customers are in tells you nothing about whether the network is safe."),
                ("Turn your screen brightness down so no one can see", False,
                 "The risk is the network carrying your data, not someone reading your screen."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "You have dozens of accounts and cannot remember a unique long password for each. What is the sensible fix?",
            "options": [
                ("Use a password manager, which invents and remembers a unique strong password for every account", True,
                 "Yes. You memorise one strong master password, and the manager handles the rest, so one leaked site cannot unlock the others."),
                ("Use one very strong password for everything so there is less to remember", False,
                 "Reuse is the trap. However strong it is, one breached site then hands over every account at once."),
                ("Write them all on a sticky note by the screen", False,
                 "A sticky note in plain view is a confidentiality failure waiting to happen. A password manager keeps them locked away."),
                ("Keep them short so they are easy to recall", False,
                 "Short passwords are exactly the ones a computer guesses fastest. Length is what makes them strong."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "If you turn on two-factor authentication for only one account first, which should it be?",
            "options": [
                ("Your email, because it can reset the passwords of most of your other accounts", True,
                 "Yes. Email is the master key. Whoever controls it can reset your other logins, so protect it first."),
                ("A shopping site you use once a year", False,
                 "Low value. Start with the account that unlocks the others, which is your email."),
                ("Whichever account you care about least", False,
                 "The opposite. Protect your highest-value account first, and that is usually email."),
                ("It does not matter, they are all the same", False,
                 "They are not equal. Email is special because it can reset so many other accounts."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "A visitor's phone is infected with malware and joins your Wi-Fi. What keeps that problem away from your work computers?",
            "options": [
                ("A separate guest network, which walls visitors' devices off from your work devices", True,
                 "Right. A guest network lets visitors online while keeping their devices, infected or not, separate from your business systems."),
                ("A faster internet plan", False,
                 "Speed does nothing to separate devices. A guest network is what keeps them apart."),
                ("Turning the Wi-Fi password off", False,
                 "An open network is worse, not better. You want a separate, password-protected guest network."),
                ("Nothing can be done once a device is on the Wi-Fi", False,
                 "Plenty can. A guest network is designed for exactly this, keeping guest devices away from your own."),
            ],
        },
        # ---- Lesson 4: habits and response ----
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "A supplier emails that their bank account has changed. Safest way to verify?",
            "options": [
                ("Phone them on a number you already have on file", True,
                 "Yes. Confirm a change of details on a channel you already trust, not one taken from the email."),
                ("Reply to the email and ask them to confirm", False,
                 "Risky. If the email is a scam, you are just asking the attacker."),
                ("Use the phone number printed in the email", False,
                 "No. A scammer supplies their own number. Use details you already hold."),
                ("Just pay it, suppliers do not lie about bank details", False,
                 "A changed bank account is the single most common invoice scam. Always verify."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "A colleague admits they clicked a phishing link. Best response?",
            "options": [
                ("Thank them for speaking up and report it so the account can be secured", True,
                 "Yes. A calm, fast report is what limits the damage. Punishing it just drives the next mistake into hiding."),
                ("Tell them off so they are more careful next time", False,
                 "No. Blame makes people hide mistakes, which is far more dangerous."),
                ("Tell them to keep it quiet", False,
                 "No. Silence lets a small problem grow into a big one."),
                ("Do nothing unless something obviously breaks", False,
                 "By the time damage shows, the attacker has had free rein. Report it early."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What lets a business recover from ransomware without paying?",
            "options": [
                ("Recent backups that have been tested and can actually be restored", True,
                 "Yes. A good backup means you can restore and carry on rather than negotiate."),
                ("A faster internet connection", False,
                 "No. Speed does nothing against ransomware."),
                ("Paying quickly for a discount", False,
                 "No. Paying is no guarantee of recovery, and it marks you as willing to pay again."),
                ("Turning the computer off and on again", False,
                 "No. That will not undo the encryption ransomware applies."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "If you could protect only one account with two-factor first, which should it be?",
            "options": [
                ("Your email, because it can reset the passwords of most other accounts", True,
                 "Yes. Email is the master key, so protecting it protects everything it can reset."),
                ("A rarely used shopping site", False,
                 "Lower value. Start with the account that unlocks the others."),
                ("A news site you have no login for", False,
                 "There is little to protect there. Email matters far more."),
                ("Whichever you use least", False,
                 "The opposite. Protect your highest-value account, your email, first."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "A password manager mainly helps by:",
            "options": [
                ("Letting you use a different strong password everywhere without memorising them", True,
                 "Yes. It remembers unique strong passwords for you, so one leaked site cannot unlock the rest."),
                ("Making your internet faster", False,
                 "No. It has nothing to do with speed."),
                ("Sharing your passwords with colleagues", False,
                 "No. That would undermine security, not help it."),
                ("Removing the need for any password", False,
                 "No. It manages your passwords, it does not abolish them."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What is the idea behind 'defence in depth'?",
            "options": [
                ("Layer several simple habits so that if one is missed, the next still protects you", True,
                 "Yes. No single control is perfect, so overlapping ones mean a single slip is not a disaster."),
                ("Buy one very expensive security product", False,
                 "No. It is about layering simple habits, not a single silver bullet."),
                ("Only the IT team needs to do anything", False,
                 "No. Everyone's small habits are part of the layers."),
                ("Turn off the internet whenever possible", False,
                 "No. It is about sensible overlapping protections, not going offline."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "You realise you may have entered your password into a suspicious page. Best thing to do?",
            "options": [
                ("Report it straight away to whoever looks after your IT", True,
                 "Yes. Fast reporting means the account can be secured before harm is done. There is never trouble for owning up."),
                ("Say nothing and hope nothing happens", False,
                 "No. Staying quiet lets a small problem grow. Quick reporting is what limits the damage."),
                ("Delete the email and carry on", False,
                 "No. Deleting the message does not undo an entered password. It needs reporting."),
                ("Wait a week to see if anything goes wrong", False,
                 "No. Waiting just gives an attacker time. Report it now."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "With defence in depth in place, a staff member is tricked into giving away their password. What is most likely to stop it becoming a break-in?",
            "options": [
                ("Two-factor authentication, because the attacker still lacks the second key", True,
                 "Yes. That is the value of layering. The click got through, but the next layer, two-factor, still blocks the login."),
                ("Nothing, once a password is handed over the account is lost", False,
                 "Not with layers. Two-factor sits behind the password for exactly this moment."),
                ("A recent backup of the files", False,
                 "Backups help you recover from ransomware, but they do not stop someone logging in with a stolen password. Two-factor does."),
                ("A faster internet connection", False,
                 "Speed is irrelevant here. The layer that saves you is the second factor at login."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "Why does a blame-free culture make a workplace more secure, not less?",
            "options": [
                ("People report mistakes quickly, so accounts can be secured before harm is done", True,
                 "Exactly. Fast, honest reporting turns a slip into a near miss. Blame just teaches people to hide the next one."),
                ("It means nobody has to follow the security habits", False,
                 "Blame-free does not mean rule-free. It means mistakes get reported early rather than hidden."),
                ("It removes the need for two-factor and backups", False,
                 "It works alongside those, not instead of them. Reporting is the layer that limits damage when something slips through."),
                ("Attackers avoid friendly workplaces", False,
                 "Attackers do not care how friendly you are. The benefit is that staff report problems fast so they can be fixed."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Why does testing that you can actually restore a backup matter as much as having one?",
            "options": [
                ("A backup nobody has ever restored may have silently stopped working, and you find out on the worst day", True,
                 "Right. Backups can quietly fail for months. Restoring a file now and then is how you know it will be there when ransomware strikes."),
                ("Testing makes the backup run faster", False,
                 "Speed is not the point. Testing proves the backup actually works so you can rely on it in a crisis."),
                ("A tested backup can never be affected by ransomware", False,
                 "Testing does not make it immune. It confirms the backup is real and restorable, which is what you need."),
                ("You only need to test it once, when you buy it", False,
                 "Backups can fail at any time, so an occasional restore check is worth repeating, not a one-off."),
            ],
        },
    ],
}
