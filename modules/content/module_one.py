"""Module 1, Network Security Fundamentals: the gold-standard reference content.

  Lesson 1  UNDERSTAND IT  — a teaching lesson. Four deep reading panels, each
            with a real, device-framed visual: what a network actually is and why
            small business is targeted; how data travels and what encryption does
            (with the animated "watch your data travel" hero); the CIA triad
            mapped to real Australian incidents; and where the weak points are,
            framed against the ASD Essential Eight. One comprehension check.
  Lesson 2  APPLY IT       — a practical lesson. Five hands-on, scenario-based
            tasks (classify, a stranger-on-the-Wi-Fi branch, a HARDEN drill to
            secure the clinic, a router-screen picture check, and a
            three-mornings respond) that put Lesson 1 to work.

Voice: warm, confident, plain Australian English for non-technical readers. No
em-dashes, no emoji, no filler.

Sources (facts are current as cited, framed as general information):
- Australian Signals Directorate, Annual Cyber Threat Report 2024-25
  (cyber.gov.au): over 84,700 cybercrime reports, about one every 6 minutes;
  average self-reported cost of cybercrime per report for small business $56,600.
- ACSC Small Business Cyber Security Guide and the ASD Essential Eight
  (cyber.gov.au): change default passwords, secure Wi-Fi with WPA2/WPA3, turn on
  automatic updates, use multi-factor authentication, keep regular backups.
- The 2022 Optus (about 9.8 million people, including passport and licence
  numbers) and Medibank (about 9.7 million people; remote access without
  multi-factor authentication) incidents, used to make the CIA triad concrete.
Points per lesson sum to 10 and bank at lesson end.
"""

LESSONS = [
    {
        "title": "What a network is, and what you protect",
        "reading_time_minutes": 10,
        "intro": "Start here. Meet the thing you are protecting, follow the exact "
        "path your information takes, learn the three questions security keeps "
        "asking, and see where the weak points are. By the end you will be able to "
        "look at your own network and know what keeps it safe, and why.",
        "tasks": [
            {
                "key": "net-basics",
                "kind": "concept",
                "points": 2,
                "title": "What a network actually is, and why it is a target",
                "hero": "net-scene",
                "body": "<p>A <strong>network</strong> is simply devices connected so "
                "they can share information. In a small Australian business that is "
                "the front-desk computer, the printer, the eftpos machine and "
                "everyone's phones, all talking through one <strong>router</strong> "
                "and out to the internet. The router is the gateway: every message "
                "in or out of the business passes through it, which is why so much "
                "of security comes down to that one box.</p>"
                "<p>Here is how the pieces fit. Each device gets its own "
                "<strong>IP address</strong>, a number that works like a street "
                "address so information reaches the right machine. Inside your walls, "
                "on your own Wi-Fi, traffic between devices is on home ground. The "
                "moment it leaves the router for the internet, it is travelling "
                "across equipment owned by other people, and that is where most of "
                "the risk lives.</p>"
                "<p>Why does a small clinic or cafe get targeted at all? Because "
                "attacks are automated and scale is free. The Australian Signals "
                "Directorate received <strong>over 84,700 cybercrime reports in "
                "2024-25, about one every six minutes</strong>, and the average "
                "self-reported cost to a small business was <strong>$56,600 per "
                "report</strong>. Attackers are not picking you personally; their "
                "tools scan everyone, and a small business with real customer data "
                "and light defences is an easy win.</p>"
                "<div class=\"cy-callout\">The good news: the same report shows most "
                "incidents use a handful of predictable weaknesses. A few simple "
                "habits, covered in this lesson, shut most of those doors.</div>",
            },
            {
                "key": "data-travels",
                "kind": "concept",
                "points": 2,
                "title": "How your information travels, and what encryption does",
                "hero": "data-journey",
                "body": "<p>Your information does not sit still. When you sign in to a "
                "website or send an email, what you type is broken into small "
                "<strong>packets</strong> that travel from your device, to your "
                "router, out to your internet provider, across the "
                "<strong>shared public internet</strong>, and finally to a server "
                "somewhere else. The animation above follows that journey.</p>"
                "<p>That middle stretch is the catch. The public internet is shared "
                "ground: your packets hop through equipment you do not own or "
                "control, and someone positioned in the middle could try to read "
                "them. Watch the top lane above: without protection, a login travels "
                "as plain, readable text, and a listener on the network simply reads "
                "it, password and all.</p>"
                "<p>This is what <strong>encryption</strong> fixes. It scrambles your "
                "information with a key so that, even if it is intercepted, it is "
                "useless gibberish, exactly like the bottom lane above. You already "
                "rely on this every day: before you type a password, look at the "
                "address bar. <strong>https</strong> (the s is for secure) and a "
                "small <strong>padlock</strong> mean the connection is encrypted end "
                "to end between you and that site.</p>"
                "<p>One important limit. The padlock proves the <em>connection</em> "
                "is private. It does <em>not</em> prove the website is genuine. "
                "Criminals can get a padlock for a fake site in minutes, so treat it "
                "as a green light for privacy, never as a guarantee of trust.</p>"
                "<div class=\"cy-callout\">Look for https and the padlock before you "
                "type anything sensitive. No padlock, no password. And remember: the "
                "padlock protects the pipe, not your judgement about the site.</div>",
            },
            {
                "key": "cia-triad",
                "kind": "concept",
                "points": 2,
                "title": "The three questions, and three real Australian breaches",
                "diagram": "cia-triad",
                "body": "<p>Security sounds complicated, but underneath it is three "
                "simple questions, known as the <strong>CIA triad</strong> (nothing "
                "to do with spies). Every control in this course defends one of "
                "them, and each maps to a real incident Australians have lived "
                "through.</p>"
                "<p><strong>Confidentiality</strong>: can only the right people see "
                "it? In 2022 the <strong>Optus</strong> breach exposed information on "
                "about <strong>9.8 million</strong> current and former customers, "
                "including, for some, passport and licence numbers, the raw material "
                "for identity theft. Nothing was locked or changed; private data "
                "simply reached people who should never have had it.</p>"
                "<p><strong>Integrity</strong>: is it accurate and unaltered? A "
                "supplier's invoice with its bank account quietly changed fails this. "
                "The file still opens perfectly, but the details were tampered with, "
                "which is exactly how invoice and payment-redirection scams drain "
                "real money from Australian businesses.</p>"
                "<p><strong>Availability</strong>: is it there when you need it? "
                "Ransomware that locks every file, or a booking system down all "
                "morning, fails this. In the 2022 <strong>Medibank</strong> attack, "
                "sensitive health data on about <strong>9.7 million</strong> people "
                "was stolen and later published; the same class of attack routinely "
                "locks a business out of its own systems for days.</p>"
                "<div class=\"cy-callout\">Keep information private, keep it correct, "
                "keep it reachable. Name which one a problem threatens, and you "
                "already understand half of how to respond.</div>",
            },
            {
                "key": "weak-points",
                "kind": "concept",
                "points": 2,
                "title": "Where the weak points are, and the Essential Eight",
                "diagram": "router-admin",
                "body": "<p>Most small networks share the same handful of weak "
                "points, and the same handful of fixes. The router page above, open "
                "in a browser, shows the biggest one: an admin password still set to "
                "the factory default, <strong>admin</strong>. This matters because "
                "default passwords are not secret. Manufacturers print them in "
                "manuals and publish them online, and attackers keep ready-made lists "
                "of them, so anyone can look yours up and change your settings. "
                "Changing it to something strong and unique is the single most "
                "important fix on that screen.</p>"
                "<p>For the rest, the Australian Signals Directorate publishes a "
                "baseline called the <strong>Essential Eight</strong>. You do not "
                "need all of it on day one, but these five habits from it and the "
                "ACSC Small Business Guide stop the great majority of trouble:</p>"
                "<ul>"
                "<li><strong>Turn on automatic updates (patching)</strong> for "
                "computers, phones and the router. Most attacks that use a software "
                "flaw use one the maker had already fixed; updating closes that hole "
                "before it can be used.</li>"
                "<li><strong>Turn on multi-factor authentication (MFA)</strong> for "
                "email and important accounts, so a stolen password alone is not "
                "enough to get in. The Medibank attackers reached the network through "
                "remote access that lacked MFA.</li>"
                "<li><strong>Keep regular backups</strong>, with at least one copy "
                "kept offline, so ransomware cannot take your only path back.</li>"
                "<li><strong>Change default passwords</strong> on the router and "
                "every device, straight out of the box.</li>"
                "<li><strong>Secure your Wi-Fi</strong> with WPA2 or WPA3 encryption "
                "and a long passphrase, and put visitors on a separate guest "
                "network, so an unknown phone never shares the Wi-Fi with the "
                "accounts computer.</li>"
                "</ul>"
                "<div class=\"cy-callout\">None of this is technical. It is a short "
                "list of settings, done once, that closes most of the doors an "
                "automated attack would ever try.</div>",
            },
            {
                "key": "who-is-on",
                "kind": "check",
                "points": 2,
                "title": "Quick check: who is on your Wi-Fi?",
                "diagram": "wifi-devices",
                "body": "<p>One quick check to finish, using something you can "
                "actually do today. Most routers and Wi-Fi apps let you see every "
                "device connected right now, with its name, address and when it "
                "joined. The clinic's list is above. Four are the clinic's own "
                "devices, each tagged as familiar. Read the list, then answer.</p>"
                "<div class=\"cy-callout\">Being able to see what is on your network "
                "is the first step to protecting it. A device you do not recognise "
                "is worth a second look.</div>",
                "question": "Looking at the clinic's connected-devices list, which one should make you stop and check?",
                "hint": "Four devices are tagged as the clinic's own. One is not.",
                "options": [
                    ("The unknown device that joined two hours ago", True,
                     "Right. It is the only device not recognised as the clinic's own, with an unfamiliar hardware address, and it appeared recently. That is exactly what you check: flag it, and change the Wi-Fi password so unknown devices drop off."),
                    ("The waiting room TV", False,
                     "The TV is tagged as the clinic's own device and has been on since the morning. It is expected, not a concern."),
                    ("The clinic printer that is always on", False,
                     "The printer is a known clinic device that stays connected by design. Nothing unusual there."),
                    ("Reception's iPad", False,
                     "The iPad is a familiar clinic device that joined at the start of the day. That is normal."),
                ],
            },
        ],
    },
    {
        "title": "Put it to work: protect a real network",
        "reading_time_minutes": 9,
        "intro": "Now use it. Every task here is a real workplace situation that "
        "puts Lesson 1 to work: name what is at risk, handle a stranger on the "
        "Wi-Fi, secure the clinic before it opens, read a router screen, and make "
        "the right first move when something goes wrong.",
        "tasks": [
            {
                "key": "pillar-triage",
                "kind": "classify",
                "points": 2,
                "title": "Which pillar is at risk?",
                "body": "<p>Lesson 1 gave you the three questions security asks: is "
                "it private (Confidentiality), is it correct (Integrity), is it "
                "reachable (Availability). Here are six things that could go wrong in "
                "a clinic. For each, decide which pillar it puts at risk. This is how "
                "a security-minded person sizes up any problem in seconds.</p>"
                "<div class=\"cy-callout\">Ask: was private information exposed, was "
                "something changed, or can you no longer reach what you need?</div>",
                "payload": {
                    "prompt": "Read each situation and tap the pillar it puts at risk. Sort all six to finish.",
                    "categories": [
                        {"id": "conf", "label": "Confidentiality"},
                        {"id": "integ", "label": "Integrity"},
                        {"id": "avail", "label": "Availability"},
                    ],
                    "events": [
                        {"text": "A staff member emails the day's patient list to the wrong outside address.",
                         "category": "conf",
                         "why": "Confidentiality. Nothing was lost or changed, but private information reached someone who should not have it. Like Optus, the failure is exposure."},
                        {"text": "A supplier's invoice arrives with its bank account quietly changed, but it still opens fine.",
                         "category": "integ",
                         "why": "Integrity. The file is readable and available, but its details were altered without permission, which is how invoice scams work."},
                        {"text": "Ransomware locks every file on the shared drive and demands payment.",
                         "category": "avail",
                         "why": "Availability. The files are not stolen or changed, but you cannot reach them, which halts the business."},
                        {"text": "A visitor glances at a password written on a sticky note at the front desk.",
                         "category": "conf",
                         "why": "Confidentiality. A secret that should be private has been exposed to the wrong person."},
                        {"text": "The online booking system is down all morning and patients cannot check in.",
                         "category": "avail",
                         "why": "Availability. Nothing was stolen or altered, but a system you need is not there when you need it."},
                        {"text": "Someone edits the clinic's price list without approval and no one notices.",
                         "category": "integ",
                         "why": "Integrity. The information was changed without permission, so it can no longer be trusted as accurate."},
                    ],
                },
            },
            {
                "key": "unknown-device",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: a stranger on the Wi-Fi",
                "body": "<p>You just learned you can see every device on your "
                "network. Now one of them is a stranger. This is a real decision, "
                "made in the moment, and your first move decides how it plays out. "
                "Work it through.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> an unknown "
                "device is a door you did not open. Close it, then keep visitors off "
                "the staff network for good.</div>",
                "payload": {
                    "prompt": "You spot an unknown device on the clinic Wi-Fi. Make each call and see the consequence.",
                    "start": "look",
                    "nodes": {
                        "look": {
                            "text": "You open the clinic Wi-Fi's device list and there is a device you do not recognise, connected right now. What is your first move?",
                            "choices": [
                                {"label": "Flag it to whoever manages the Wi-Fi, and change the Wi-Fi password so unknown devices are kicked off", "outcome": "good",
                                 "feedback": "Right. Changing the Wi-Fi password forces every device to reconnect with the new one, so anything you did not authorise simply drops off.", "to": "reconnect"},
                                {"label": "Ignore it, it is probably a staff member's phone", "outcome": "bad",
                                 "feedback": "Maybe it is, but you cannot assume that. An unknown device on the same network as your records is worth two minutes to rule out.", "to": "ignore_bad"},
                                {"label": "Turn the whole router off for the day to be safe", "outcome": "bad",
                                 "feedback": "That takes the entire clinic offline, staff and all, for one unknown device. Change the Wi-Fi password instead of pulling the plug.", "to": "off_bad"},
                            ],
                        },
                        "ignore_bad": {
                            "text": "Assuming it is harmless is exactly what an intruder counts on. If it was not a staff phone, it now has a quiet foothold on the network your records sit on. Rule out unknown devices, do not wave them through.",
                            "choices": [],
                        },
                        "off_bad": {
                            "text": "The clinic grinds to a halt for the afternoon, and the moment the router comes back on, the same unknown device could reconnect. A blunt shutdown is not a fix. Change the Wi-Fi password.",
                            "choices": [],
                        },
                        "reconnect": {
                            "text": "The Wi-Fi password is changed, every device reconnects with the new one, and the stranger is gone. How do you stop it happening again?",
                            "choices": [
                                {"label": "Set up a separate guest network so visitors never share the staff Wi-Fi", "outcome": "good",
                                 "feedback": "Exactly. A guest network keeps visitors' phones and devices completely apart from the computers holding your records. That is the lasting fix.", "to": "win"},
                                {"label": "Leave everything on one network, it is simpler", "outcome": "bad",
                                 "feedback": "One shared network means the next visitor's phone sits right alongside the accounts computer again. A guest network is a five-minute setting that solves it for good.", "to": "one_net_bad"},
                            ],
                        },
                        "one_net_bad": {
                            "text": "The immediate stranger is gone, but the door is still there. On one flat network, every visitor device shares the ground with your most sensitive systems. Separate them with a guest network.",
                            "choices": [],
                        },
                        "win": {
                            "text": "You spotted the unknown device, shut it out by changing the Wi-Fi password, and split visitors onto a guest network so it cannot recur. That is exactly how you look after a real network: see what is on it, close what you did not open, and keep the sensitive systems apart.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "secure-the-clinic",
                "kind": "harden",
                "points": 2,
                "title": "Secure the clinic before it opens",
                "body": "<p>It is 8am and the clinic opens in fifteen minutes. Four "
                "parts of the network are not set up safely yet. For each one, choose "
                "the fix that closes the gap, using the Essential Eight habits from "
                "Lesson 1, and watch it flip to Secured. This is the real morning "
                "checklist.</p>"
                "<div class=\"cy-callout\">For each item, pick the option that "
                "genuinely closes the door. Lock down all four to finish.</div>",
                "payload": {
                    "prompt": "Secure each part of the clinic network. Lock down all four to finish.",
                    "steps": [
                        {
                            "label": "The router still uses its default 'admin' password",
                            "risk": "Default passwords are published online, so anyone can look yours up and change your settings.",
                            "options": [
                                {"text": "Change it to a long, unique password only staff know", "correct": True,
                                 "why": "Right. A strong, unique admin password is the single most important router fix, because the factory default is public knowledge."},
                                {"text": "Hide the router in a cupboard so no one can reach it", "correct": False,
                                 "why": "Attackers reach the router over the network, not by walking up to it. Physically hiding it changes nothing. Change the password."},
                                {"text": "Leave it, since 'admin' is easy for staff to remember", "correct": False,
                                 "why": "Easy to remember means easy to guess, and this one is already published. Change it to something strong and unique."},
                            ],
                        },
                        {
                            "label": "Visitors join the same Wi-Fi as the accounts computer",
                            "risk": "A device you do not control sits on the same network as your most sensitive systems.",
                            "options": [
                                {"text": "Put visitors on a separate guest network", "correct": True,
                                 "why": "Right. A guest network keeps untrusted devices completely apart from the computers holding your records."},
                                {"text": "Ask visitors not to open anything risky", "correct": False,
                                 "why": "You cannot control what is on a visitor's phone or what it does. Separate them with a guest network instead of relying on trust."},
                                {"text": "Turn the Wi-Fi off whenever a visitor is in", "correct": False,
                                 "why": "That stops the staff working too, and is not practical. A guest network solves it permanently in one setting."},
                            ],
                        },
                        {
                            "label": "Email has only a password, no second step",
                            "risk": "If that password is guessed or stolen, an attacker walks straight into the mailbox.",
                            "options": [
                                {"text": "Turn on multi-factor authentication for email", "correct": True,
                                 "why": "Right. MFA adds a second factor, like a code on your phone, so a stolen password alone is not enough to get in."},
                                {"text": "Make everyone change the password every week", "correct": False,
                                 "why": "Constant changes lead to weaker, reused passwords written on notes. A second factor protects far better. Turn on MFA."},
                                {"text": "Use the same strong password across all accounts", "correct": False,
                                 "why": "Reusing one password means one leak unlocks everything. Use unique passwords, and add MFA on top."},
                            ],
                        },
                        {
                            "label": "Computers are set to update 'later', manually",
                            "risk": "Out-of-date software keeps known holes open for attackers to walk through.",
                            "options": [
                                {"text": "Turn on automatic updates so patches apply promptly", "correct": True,
                                 "why": "Right. Automatic updates close known holes fast, before attackers can use them, without anyone having to remember."},
                                {"text": "Update once a year during the quiet period", "correct": False,
                                 "why": "That leaves known holes open for months. Most attacks use a flaw a patch had already fixed. Update promptly, ideally automatically."},
                                {"text": "Skip updates to avoid any disruption", "correct": False,
                                 "why": "Skipping updates leaves the door open on purpose. Turn automatic updates on so it happens quietly in the background."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "read-the-router",
                "kind": "check",
                "points": 2,
                "title": "Read the router screen",
                "diagram": "router-admin",
                "body": "<p>A real router admin page, open in a browser, the kind you "
                "would check on your own network. Three of its four rows are set up "
                "well. One is a wide-open door. Read it the way you now know how, "
                "then answer.</p>"
                "<div class=\"cy-callout\">Remember the biggest weak point from "
                "Lesson 1: a setting that every installer and every website already "
                "knows.</div>",
                "question": "What is the security problem shown on this router page, and the fix?",
                "hint": "One row shows a value that is the same on thousands of routers straight from the factory.",
                "options": [
                    ("The admin password is still the default, 'admin', so change it to something strong straight away", True,
                     "Right. Default router passwords like 'admin' are printed in manuals and listed online, so anyone can look yours up and change your settings. Changing it is the single most important fix. WPA2 and up-to-date firmware are already fine."),
                    ("The firmware is up to date, which is a problem", False,
                     "That is a good thing, not a problem. Up-to-date firmware means known security holes are already patched. The real issue is the default admin password."),
                    ("Wi-Fi is using WPA2 encryption, which is unsafe", False,
                     "No, WPA2 is a good setting that keeps your wireless traffic scrambled. The problem on this page is the default admin password."),
                    ("The router has an IP address, which exposes it", False,
                     "Every router has an address so you can reach its settings. That is normal. The real weak point is the default admin password."),
                ],
            },
            {
                "key": "three-mornings",
                "kind": "respond",
                "points": 2,
                "title": "Three bad mornings",
                "body": "<p>One last drill, and the most important, because this is "
                "where it counts. A small clinic, three rough mornings, three things "
                "going wrong. Knowing what a network is was the start. The real skill "
                "is your first move, because it decides how far a problem spreads. "
                "For each morning, choose your first move and see how it plays "
                "out.</p>"
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
                                 "feedback": "Right. A privacy slip is far cheaper to handle in the first hour. Owning up fast is the whole game, and it is a confidentiality problem, so it must be reported."},
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
                                 "feedback": "Exactly. Getting it off the network first stops the ransomware spreading to other machines and the shared drive. That protects availability for everyone else."},
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
                                 "feedback": "Yes. A changed account plus any pressure to pay is the classic invoice scam, an integrity attack. Verify on a channel you already trust."},
                                {"text": "Pay it, the invoice looks genuine", "outcome": "bad",
                                 "feedback": "A tampered invoice looks perfectly genuine. That is the point. Verify the changed details first."},
                                {"text": "Email back to ask if the account really changed", "outcome": "risky",
                                 "feedback": "If the email is a scam, you are asking the scammer. Use a number you already have, not the one in the email."},
                            ],
                        },
                    ],
                },
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. Exactly ten, five per lesson: Lesson 1 checks the concepts taught, Lesson
# 2 checks applying them. Four options each, exactly one correct, every option
# carries an explanation that teaches (the Adaptive Feedback Engine's fuel). Same
# house voice: warm, plain, no em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: understand it ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "In plain terms, what is a computer network, and what is the router's role?",
            "options": [
                ("Devices connected to share information, with the router as the gateway every message passes through on its way in or out", True,
                 "Yes. A network is devices linked to share information, and the router is the single gateway between your business and the internet."),
                ("A single powerful computer that runs the whole business", False,
                 "No. A network is many devices connected together, not one big machine."),
                ("The antivirus software installed on a computer", False,
                 "No. That is a defence on one device. A network is the devices linked together, joined by the router."),
                ("The password you use to log in each morning", False,
                 "No. A password protects an account. A network is the connected devices themselves."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "The CIA triad names the three things security protects. What are they, and which did the 2022 Optus breach fail?",
            "options": [
                ("Confidentiality, Integrity, Availability, and Optus was a Confidentiality failure: private data was exposed to the wrong people", True,
                 "Yes. The triad is Confidentiality, Integrity and Availability, and exposing customers' private details is a confidentiality failure."),
                ("Control, Internet, Access, and Optus failed Availability", False,
                 "No. The triad is Confidentiality, Integrity and Availability. Optus exposed private data, a confidentiality failure."),
                ("Confidentiality, Integrity, Availability, and Optus failed Availability because files were locked", False,
                 "No on the second part. Nothing was locked at Optus; private data was exposed, which is a confidentiality failure."),
                ("Computers, Internet, Applications, and Optus failed Integrity", False,
                 "No. The triad is Confidentiality, Integrity, Availability, and Optus was a confidentiality failure."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A work login page shows the padlock and https in the address bar. What does that actually tell you?",
            "options": [
                ("The connection is encrypted, so someone on the same network cannot read what you type, though it is not proof the site itself is genuine", True,
                 "Yes. The padlock means the link is encrypted in transit. It does not, on its own, prove the website is who it claims to be, because scam sites can get a padlock too."),
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
            "text": "You open the router's settings page and see the admin password is still 'admin'. Why is that dangerous, and what is the fix?",
            "options": [
                ("Default passwords like 'admin' are published online for anyone to look up, so change it to something strong and unique straight away", True,
                 "Yes. Factory-default passwords are public knowledge and attackers keep lists of them, so anyone can log in and change your settings. Changing it is the single most important fix."),
                ("Nothing is wrong; 'admin' is a strong, secure password", False,
                 "No. 'admin' is the factory default, listed online for anyone to find. It must be changed."),
                ("The router is broken and needs replacing", False,
                 "No. The router is fine. The default password just needs changing to something strong and unique."),
                ("You should turn the router off to stay safe", False,
                 "No. That takes the whole network offline. The fix is to change the default password."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "The ASD Essential Eight includes turning on automatic updates. Why does that matter so much?",
            "options": [
                ("Most attacks that use a software flaw use one the maker has already fixed, and updates close that hole before it can be used", True,
                 "Yes. Updates apply the maker's fixes for known security holes. Applying them promptly, ideally automatically, shuts the door before an attacker reaches it."),
                ("Updates make the computer run faster", False,
                 "No. Speed is not the point. Updates matter because they close known security holes."),
                ("Updates back up your files automatically", False,
                 "No. That is a backup, a separate Essential Eight habit. Updates patch security weaknesses."),
                ("Updates are only about new features and can safely be ignored", False,
                 "No. Many updates fix security holes. Skipping them leaves known weaknesses open."),
            ],
        },
        # ---- Lesson 2: apply it ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A staff member accidentally emails the day's patient list to the wrong outside address. Which pillar of the CIA triad has failed?",
            "options": [
                ("Confidentiality, because private information reached someone who should not have it", True,
                 "Yes. The data was neither lost nor changed, but it was exposed to the wrong person, which is a confidentiality failure. It should be reported straight away."),
                ("Availability, because the files can no longer be opened", False,
                 "No. The files are still available. The problem is that private data was exposed, a confidentiality failure."),
                ("Integrity, because the data was secretly altered", False,
                 "No. Nothing was changed. Private data simply reached the wrong person, which is a confidentiality failure."),
                ("None, because sending an email is always safe", False,
                 "No. Sending sensitive data to the wrong address is a real confidentiality breach."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Every file on the shared drive is suddenly locked and a note demands payment. What is the safe first move?",
            "options": [
                ("Disconnect that computer from the network, then report it", True,
                 "Yes. Getting it off the network first stops the ransomware spreading to other machines and the shared drive. Then report it and recover from backup, do not pay."),
                ("Pay the ransom quickly to get the files back", False,
                 "No. Paying is unreliable, funds crime, and marks you as a payer. Contain it first, then recover from backup."),
                ("Keep working and hope it stops", False,
                 "No. Every second it stays connected, more files and machines are locked. Disconnect first."),
                ("Restart the computer to clear it", False,
                 "No. A restart will not remove ransomware and may make recovery harder. Disconnect from the network and report it."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "An invoice from a regular supplier arrives with a changed bank account and asks you to pay it today. Which pillar is at risk, and what should you do?",
            "options": [
                ("Integrity, so ring the supplier on a number you already have and confirm the change before paying", True,
                 "Yes. A changed account plus time pressure is the classic invoice scam, an integrity attack. Verify through a channel you already trust, never through the email."),
                ("Availability, so pay it quickly before the system goes down", False,
                 "No. Nothing is unavailable. The details were altered, which is integrity, and it needs verifying by phone first."),
                ("Confidentiality, so mark the email private and pay it", False,
                 "No. Nothing private was exposed. The account was changed, which is integrity. Verify before paying."),
                ("Nothing is at risk, so pay it because the invoice looks genuine", False,
                 "No. A tampered invoice looks genuine on purpose. A changed account always deserves a phone call to a known number first."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "You open your Wi-Fi's device list and see a device you do not recognise, connected right now. What should you do?",
            "options": [
                ("Flag it, and change the Wi-Fi password so unknown devices are forced off, then keep visitors on a separate guest network", True,
                 "Yes. Changing the Wi-Fi password drops any device you did not authorise, and a guest network stops visitors sharing the staff Wi-Fi in future."),
                ("Ignore it, it is probably a staff member's phone", False,
                 "No. You cannot assume that. An unknown device on the network with your records is worth ruling out."),
                ("Turn the router off for the day to be safe", False,
                 "No. That takes the whole business offline for one device, and it can reconnect later. Change the Wi-Fi password instead."),
                ("Nothing, you cannot see or control who joins your Wi-Fi", False,
                 "No. You can: most routers list connected devices, and changing the Wi-Fi password removes any you did not authorise."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Securing the clinic before it opens, which of these is the EXPOSED setup that needs fixing?",
            "options": [
                ("The router is still using its default 'admin' password", True,
                 "Yes. A default password is public knowledge and must be changed to something strong and unique. WPA2 Wi-Fi, automatic updates and MFA are all good, secure habits."),
                ("Wi-Fi encryption is set to WPA2", False,
                 "No, that is secure. Strong Wi-Fi encryption keeps your wireless traffic private."),
                ("Automatic updates are turned on", False,
                 "No, that is secure. Automatic updates close known holes promptly."),
                ("Multi-factor authentication is turned on for email", False,
                 "No, that is secure. MFA stops a stolen password on its own getting an attacker in."),
            ],
        },
    ],
}
