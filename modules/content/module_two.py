"""Module 2, Recognising Cyber Threats: two DEEP lessons.

Deliberately two lessons, not four, each carrying the weight of the old pairs so
the learner goes deeper rather than wider:

  Lesson 1  Know the threats: malware, and how it gets in
            (the malware family: virus, worm, trojan, spyware, ransomware; and
            the everyday routes it uses to reach a small business)
  Lesson 2  When it goes wrong: ransomware, breaches, and reacting
            (ransomware across a whole business, the real Australian breaches
            Optus and Medibank, and how to recognise and react calmly)

Same shape and standard as Module 1 (see modules/content/module_one.py and
docs/module-authoring.md). Every lesson is a scrollable room of five PANELS in
the house pattern:

  1 Core content        CHECK    reading + callout + a mid-panel and end check
  2 Real-world scenario RESPOND  a workplace narrative with a decision to make
  3 Picture-question    CHECK    a realistic mock visual, read the tell from it
  4 Question set        QUIZSET  mixed mcq / true-false / fill / match
  5 Applied wrap-up     CHECK    one applied situation to prove it landed

Points sum to 10 per lesson (2 each) and bank at lesson end. Voice: warm,
confident, human, plain Australian English. No em-dashes, no emoji, no filler.
The real cases (Optus and Medibank, both 2022) are presented as widely-reported
factual scenarios for teaching, framed evenly and without blame.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
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
                "kind": "check",
                "points": 2,
                "title": "The malware family, member by member",
                "diagram": "malware-family",
                "body": "<p><strong>Malware</strong> simply means malicious "
                "software: any program built to do harm. People often say virus "
                "for all of it, but a virus is only one member of a whole "
                "family, and each member behaves differently. Knowing them apart "
                "matters, because what stops one does little against another.</p>"
                "<p>A <strong>virus</strong> hides inside a file and needs a "
                "person to open it before it can spread. A <strong>worm</strong> "
                "is the self-spreading one: it copies itself from machine to "
                "machine across a network with no help at all, which is why it "
                "can move so fast. A <strong>trojan</strong> is disguised as "
                "something you want, a handy tool or a free download, so you "
                "install it yourself. <strong>Spyware</strong> hides and quietly "
                "records what you do, like the passwords you type. And "
                "<strong>ransomware</strong>, which the next lesson covers in "
                "full, locks your files and demands payment.</p>"
                "<div class=\"cy-callout\">One family, very different habits. A "
                "worm spreads itself; a virus waits for a click; a trojan wears "
                "a disguise; spyware stays hidden. The defence changes with the "
                "member.</div>",
                "inline_check": {
                    "question": "Which member spreads across a network by itself, with no person needed?",
                    "hint": "Think about which one does not wait for a click.",
                    "options": [
                        ("A worm", True,
                         "Yes. A worm copies itself from machine to machine on its own, which is why it can reach a whole network so quickly."),
                        ("A virus", False,
                         "A virus needs a person to open the infected file first. The self-spreading one is the worm."),
                        ("A trojan", False,
                         "A trojan waits for you to install it, fooled by its disguise. The self-spreader is the worm."),
                        ("Spyware", False,
                         "Spyware hides and watches rather than spreading itself. The self-spreader is the worm."),
                    ],
                },
                "question": "What is the defining trait of a trojan?",
                "hint": "Its power is a disguise, not speed or stealth.",
                "options": [
                    ("It looks like something you want, so you install or run it yourself", True,
                     "Right. A trojan gets in because it appears legitimate, a free tool or a cracked program, and you let it in. Then it does its real work."),
                    ("It spreads across the network on its own", False,
                     "That is a worm. A trojan relies on you choosing to run it, fooled by the disguise."),
                    ("It floods a website with traffic", False,
                     "That is a denial-of-service attack. A trojan is disguised software you run yourself."),
                    ("It is harmless once installed", False,
                     "A trojan is very much harmful. The disguise is exactly what makes it dangerous."),
                ],
            },
            {
                "key": "delivery-respond",
                "kind": "respond",
                "points": 2,
                "title": "How it tries to get in",
                "body": "<p>Malware almost never appears on its own. Something "
                "has to let it in, and that something is usually a person acting "
                "in a busy moment. The good news is that the same few routes come "
                "up again and again, so a trained eye closes most of them. Three "
                "of those routes land in front of you this week. For each, choose "
                "the safer move and see how it plays out.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> before you "
                "open, download or run anything you did not expect, pause and "
                "ask where it really came from.</div>",
                "payload": {
                    "prompt": "Choose the safer move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "popup",
                            "text": "On a streaming site, a pop-up warns your video player is out of date and you must download an update now to keep watching.",
                            "options": [
                                {"text": "Close the pop-up and update software only from the maker or an app store", "outcome": "good",
                                 "feedback": "Right. Real updates come from the software itself or an official store, never from a scary pop-up on an unrelated website. This one is bait."},
                                {"text": "Click Download Update so you do not lose the video", "outcome": "bad",
                                 "feedback": "That download is the trap. A pop-up on a streaming site is a classic way to deliver a trojan."},
                                {"text": "Pay the small fee it asks for to keep watching", "outcome": "bad",
                                 "feedback": "Never pay or download from a pop-up like this. Close the tab and carry on."},
                            ],
                        },
                        {
                            "id": "macro",
                            "text": "An unexpected invoice arrives by email. When you open it, the document asks you to Enable content or Enable macros to see it properly.",
                            "options": [
                                {"text": "Do not enable it, and check with the sender through a number you already have", "outcome": "good",
                                 "feedback": "Yes. Macros are little programs inside a document, and that Enable prompt is how attackers run malware. When unsure, do not enable it."},
                                {"text": "Enable content so the invoice displays", "outcome": "bad",
                                 "feedback": "Enabling macros can run hidden code that installs malware. A genuine invoice does not need you to switch that on."},
                                {"text": "Forward it to a colleague to open instead", "outcome": "risky",
                                 "feedback": "That just moves the risk to someone else. Do not enable it, and verify the invoice through a trusted contact."},
                            ],
                        },
                        {
                            "id": "usb",
                            "text": "You find a USB stick in the car park with a sticker that reads Staff Bonuses 2026.",
                            "options": [
                                {"text": "Do not plug it in, and hand it to IT or your manager", "outcome": "good",
                                 "feedback": "Yes. A tempting label on a dropped USB is classic bait. Plugging it in can install malware in seconds."},
                                {"text": "Plug it in to find out whose it is so you can return it", "outcome": "bad",
                                 "feedback": "That is exactly what the attacker hopes for. The stick can infect your machine the moment it connects."},
                                {"text": "Try it on a spare computer at reception", "outcome": "bad",
                                 "feedback": "Same trap, different machine. Do not connect an unknown USB to any computer."},
                            ],
                        },
                    ],
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
                "kind": "quizset",
                "points": 2,
                "title": "Name the malware, name the route",
                "body": "<p>Four quick questions to lock in the family and the "
                "ways it travels. Each one leans on a single clear idea from this "
                "lesson, so read carefully and pick the tell. Answer all four to "
                "finish, and a wrong answer simply lets you try again.</p>",
                "payload": {
                    "prompt": "Answer all four to complete the task. A wrong answer just lets you try again.",
                    "questions": [
                        {"type": "mcq",
                         "q": "A program spreads from computer to computer across the office network on its own, with nobody opening anything. What is it?",
                         "hint": "Self-spreading, no human needed.",
                         "options": [
                             ["A worm", True, "Yes. Spreading by itself across a network with no human action is the defining mark of a worm."],
                             ["A virus", False, "A virus needs a person to open the infected file. This one spreads on its own, so it is a worm."],
                             ["A trojan", False, "A trojan waits to be installed by you. The self-spreader is the worm."],
                             ["Spyware", False, "Spyware hides and watches. The self-spreading one is the worm."]
                         ]},
                        {"type": "truefalse",
                         "q": "True or false: keeping your operating system and apps updated helps stop malware, because updates patch the known holes it uses to get in.",
                         "answer": True,
                         "hint": "What does an update actually fix?",
                         "why": "True. Many attacks rely on flaws the maker has already fixed. Installing updates closes those doors before malware can use them."},
                        {"type": "fill",
                         "q": "The umbrella word for all harmful software, of which a virus is just one member, is ___ . (one word)",
                         "answer": "malware",
                         "accept": ["malicious software"],
                         "hint": "Malicious plus software, shortened.",
                         "why": "Correct. Malware is the whole family: viruses, worms, trojans, spyware and ransomware are all members of it."},
                        {"type": "match",
                         "q": "Match each member of the family to what it does.",
                         "hint": "One spreads itself, one hides, one disguises, one locks.",
                         "why": "That is the family: a worm self-spreads, spyware hides and watches, a trojan wears a disguise, and ransomware locks your files.",
                         "pairs": [
                             ["Worm", "Spreads across a network by itself"],
                             ["Spyware", "Hides and records what you type"],
                             ["Trojan", "Disguised as something you want"],
                             ["Ransomware", "Locks your files for payment"]
                         ]}
                    ]
                },
            },
            {
                "key": "malware-applied",
                "kind": "check",
                "points": 2,
                "title": "Prove you have got it",
                "body": "<p>One applied situation to finish. Read it carefully, "
                "then choose the response that shows you understand both the "
                "malware family and the routes it uses. There is one clean "
                "answer, and the reasoning is what matters.</p>"
                "<div class=\"cy-callout\">A staff member downloads a free copy "
                "of an expensive design program from a site they found through a "
                "search. It installs fine and even seems to work, but a week "
                "later their saved passwords start being used from overseas.</div>",
                "question": "What most likely happened, and what is the lesson?",
                "hint": "A disguised free download that quietly steals: which members fit?",
                "options": [
                    ("The free program was a trojan carrying spyware, so downloads should come only from official sources", True,
                     "Right. Cracked or free copies of paid software are a favourite hiding place for a trojan, often bundled with spyware that steals passwords. Install only from the maker or an official store."),
                    ("A worm spread the moment the program opened, so nothing could be done", False,
                     "A worm spreads by itself without being installed. Here a person chose to install a disguised download, which is a trojan, and something could absolutely have been done: use official sources."),
                    ("It was a data breach at the design company", False,
                     "The passwords leaked from this person's own machine after installing an unofficial download, not from the software maker being breached."),
                    ("It was a denial-of-service attack", False,
                     "A denial-of-service attack floods a service with traffic. It does not install a disguised program that steals your passwords."),
                ],
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
                "kind": "check",
                "points": 2,
                "title": "Ransomware, and the breaches that made the news",
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
                "breach leaks what you hold. One is about getting your access "
                "back, the other about the fact that private data is now out in "
                "the world.</div>",
                "inline_check": {
                    "question": "Ransomware mainly attacks which of the three security pillars?",
                    "hint": "The files are unchanged, you just cannot reach them.",
                    "options": [
                        ("Availability", True,
                         "Yes. The files are still there and unchanged, you simply cannot get to them, so the pillar lost is availability."),
                        ("Confidentiality", False,
                         "Confidentiality is what a data breach attacks, by exposing private data. Classic ransomware locks files rather than publishing them."),
                        ("Integrity", False,
                         "Integrity is about data being secretly altered. Ransomware scrambles files wholesale and locks them, which is an availability hit."),
                        ("None, ransomware is harmless", False,
                         "It is among the most damaging attacks a business can face. The pillar it hits hardest is availability."),
                    ],
                },
                "question": "What is the key difference between ransomware and a data breach?",
                "hint": "One is about reaching your files; the other about who can see them.",
                "options": [
                    ("Ransomware locks your files (availability); a breach exposes private data to the wrong people (confidentiality)", True,
                     "Right. Ransomware stops you reaching files that are still yours; a breach means private information has leaked out and cannot be recalled. Different failures, different responses."),
                    ("They are two words for exactly the same attack", False,
                     "No. They fail in opposite ways: ransomware locks access, a breach exposes data. Telling them apart shapes how you respond."),
                    ("Both simply make the computer run slowly", False,
                     "Neither is about speed. Ransomware locks your files; a breach leaks your data."),
                    ("A breach locks files and ransomware exposes data", False,
                     "That is backwards. Ransomware locks files; a breach exposes data."),
                ],
            },
            {
                "key": "react-respond",
                "kind": "respond",
                "points": 2,
                "title": "The morning it goes wrong",
                "body": "<p>When something big hits, your first move decides how "
                "far it spreads and how well you recover. None of these needs you "
                "to be technical. Each needs a calm head and the right instinct. "
                "Three things go wrong across one rough week. For each, choose "
                "your first move and see how it plays out.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> contain it, "
                "then report it. Fast and calm beats clever, and reporting early "
                "is never the thing that gets you in trouble.</div>",
                "payload": {
                    "prompt": "Choose the soundest first move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "ransom",
                            "text": "Monday. Files on your PC are being renamed one after another, and a red screen appears demanding payment to unlock them.",
                            "options": [
                                {"text": "Disconnect the computer from the network, then report it straight away", "outcome": "good",
                                 "feedback": "Exactly. Getting it off the network first stops the ransomware reaching shared drives and other machines. Then report it so the right people act."},
                                {"text": "Pay the ransom quickly to get the files back", "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds crime, and marks you as a payer. Contain it first, then recover from backup."},
                                {"text": "Keep working and hope it stops on its own", "outcome": "bad",
                                 "feedback": "Every second it stays connected, more files and machines are locked. Disconnect first."},
                            ],
                        },
                        {
                            "id": "breach-notice",
                            "text": "Wednesday. A company you have an account with emails to say your details were in a data breach.",
                            "options": [
                                {"text": "Change that password, and anywhere you reused it, and turn on two-factor", "outcome": "good",
                                 "feedback": "Yes. You cannot recall leaked data, but you can lock down the accounts so it is far harder to misuse."},
                                {"text": "Do nothing, since the data is already out there", "outcome": "bad",
                                 "feedback": "There is plenty you can still do. Changing reused passwords and turning on two-factor sharply reduces the risk."},
                                {"text": "Pay the fee the follow-up text message asks for to secure your account", "outcome": "bad",
                                 "feedback": "That follow-up is the scam. Messages quoting your breached details are usually the next attack, not a fix."},
                            ],
                        },
                        {
                            "id": "strange-login",
                            "text": "Friday. Colleagues mention they have had odd emails from you that you never sent, and you get an alert about a login from overseas.",
                            "options": [
                                {"text": "Change your password, turn on two-factor, and report it", "outcome": "good",
                                 "feedback": "Right. Strange emails from you plus an overseas login strongly suggest your account is compromised. Lock it down and report it."},
                                {"text": "Ignore it, since your own screen looks completely normal", "outcome": "bad",
                                 "feedback": "A compromise is often invisible on your own screen while obvious to the people getting messages from you. Act on it."},
                                {"text": "Reply to the odd emails asking recipients to disregard them", "outcome": "risky",
                                 "feedback": "Warning people is worth doing, but not instead of the real fix: change the password, turn on two-factor, and report it."},
                            ],
                        },
                    ],
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
                "kind": "quizset",
                "points": 2,
                "title": "Recognise it, react to it",
                "body": "<p>Four questions to lock in the real cases and the calm "
                "response. Each one comes straight from this lesson, so think "
                "about what actually failed and what the right first move is. "
                "Answer all four to finish, and a wrong answer simply lets you "
                "try again.</p>",
                "payload": {
                    "prompt": "Answer all four to complete the task. A wrong answer just lets you try again.",
                    "questions": [
                        {"type": "mcq",
                         "q": "Files on a machine are suddenly renamed one after another, and a payment demand appears on screen. This is a hallmark of what?",
                         "hint": "Mass renaming plus a demand for money.",
                         "options": [
                             ["Ransomware", True, "Yes. Mass renaming as files are encrypted, with a ransom demand on screen, is the classic ransomware signature."],
                             ["A slow internet connection", False, "A slow connection would not rename your files or demand payment. This is ransomware."],
                             ["A data breach", False, "A breach exposes data quietly; it does not lock your files and demand money. This is ransomware."],
                             ["A normal software update", False, "Updates do not scramble and rename your files or demand payment. This is ransomware."]
                         ]},
                        {"type": "truefalse",
                         "q": "True or false: keeping recent, tested backups lets a business recover from ransomware without paying the attackers.",
                         "answer": True,
                         "hint": "What takes away the attacker's leverage?",
                         "why": "True. A clean copy you can restore removes the attacker's leverage entirely, which is why backups are the real answer to ransomware."},
                        {"type": "fill",
                         "q": "A data breach is mainly a failure of one security pillar: private data reaching the wrong people is a loss of ___ . (one word)",
                         "answer": "confidentiality",
                         "accept": [],
                         "hint": "The pillar about who is allowed to see the data.",
                         "why": "Correct. A breach is a confidentiality failure: the systems may keep running, but private information has reached people who should not have it."},
                        {"type": "match",
                         "q": "Match each 2022 case or attack to what actually happened.",
                         "hint": "One exposed an open door, one used a stolen login, one locks files.",
                         "why": "That is the pattern: Optus exposed an access point with no login, Medibank was entered with a stolen credential, and ransomware locks files for payment.",
                         "pairs": [
                             ["Optus breach", "Access point exposed with no login"],
                             ["Medibank breach", "Entered using a stolen login"],
                             ["Ransomware", "Files locked, payment demanded"]
                         ]}
                    ]
                },
            },
            {
                "key": "react-applied",
                "kind": "check",
                "points": 2,
                "title": "Prove you have got it",
                "body": "<p>One last applied situation. Read it, then choose the "
                "response that shows you can tell a real incident from ordinary "
                "trouble and react the calm, correct way. The reasoning is what "
                "counts.</p>"
                "<div class=\"cy-callout\">A staff member notices the office "
                "computer is slow. They check, and the hard drive is almost "
                "completely full. Nothing is renamed, there is no demand on "
                "screen, and colleagues have not mentioned anything odd.</div>",
                "question": "What is the right read on this, and why?",
                "hint": "Weigh the signs. Is this an attack, or an everyday cause?",
                "options": [
                    ("Most likely an ordinary glitch, a full drive, so notice it and fix it calmly rather than assuming an attack", True,
                     "Right. A full drive is a common, harmless cause of slowness. No renaming, no demand, no strange emails means the signs of an attack are absent. Notice, check, then fix, without crying wolf."),
                    ("Definitely ransomware, so pay a ransom at once", False,
                     "Ransomware locks files and demands payment, none of which is happening here. Treating every glitch as an attack burns out your alertness and wastes effort."),
                    ("Definitely a data breach, so tell customers their data has leaked", False,
                     "A breach is about exposed data, not a slow computer with a full drive. There is no sign of exposure here."),
                    ("Definitely a worm spreading, so shut down the whole office", False,
                     "There is no sign of anything spreading. A full drive explains the slowness. Overreacting to every hiccup causes its own harm."),
                ],
            },
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ================================================================
        # Lesson 1: the malware family, and how it gets in
        # ================================================================
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does the term 'malware' mean?",
            "options": [
                ("Malicious software: the umbrella term for viruses, worms, trojans, spyware and more", True,
                 "Yes. Malware is the whole family of harmful software, and a virus is only one member of it."),
                ("A specific brand of antivirus", False,
                 "No. Malware is the threat, not the protection against it."),
                ("Faulty hardware", False,
                 "No. Malware is harmful software, not broken equipment."),
                ("A strong password", False,
                 "No. That is a defence. Malware is the harmful software it helps protect against."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is the key difference between a virus and a worm?",
            "options": [
                ("A virus needs a person to open the infected file; a worm spreads across the network by itself", True,
                 "Exactly. That is why a worm can move so fast, and why the two are stopped by different defences."),
                ("A virus spreads by itself; a worm needs a person to run it", False,
                 "That is backwards. The worm is the self-spreading one; the virus needs a person to open the file."),
                ("They are two words for exactly the same thing", False,
                 "No. The difference in how they spread is real and useful for defending against each."),
                ("A virus only affects phones and a worm only affects computers", False,
                 "No. Both can affect computers. The real difference is whether it spreads on its own."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A worm is especially dangerous on a network because it:",
            "options": [
                ("Copies itself from machine to machine on its own, with no human action", True,
                 "Yes. Needing no help means it can reach every machine on a network very quickly."),
                ("Can only spread if each person opens an attachment", False,
                 "That describes a virus. A worm does not wait for anyone."),
                ("Encrypts files and demands a ransom", False,
                 "That is ransomware. A worm's defining trait is self-spreading."),
                ("Disguises itself as a program you want", False,
                 "That is a trojan. A worm spreads itself rather than relying on a disguise."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is the defining feature of a trojan?",
            "options": [
                ("It disguises itself as something you want, so you install or run it yourself", True,
                 "Yes. You let it in because it looks legitimate, and then it does its real work."),
                ("It spreads across the network without any help", False,
                 "That is a worm. A trojan relies on you choosing to run it."),
                ("It floods a website with traffic", False,
                 "That is a denial-of-service attack. A trojan is disguised software you run yourself."),
                ("It is completely harmless", False,
                 "No. A trojan is harmful; the disguise is exactly what makes it dangerous."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Downloading cracked or free copies of paid software is risky mainly because:",
            "options": [
                ("It is one of the most common ways to end up with a trojan", True,
                 "Yes. Those downloads are a favourite hiding place for disguised malware."),
                ("It uses too much internet data", False,
                 "Data use is not the real risk. The danger is the malware often hidden inside."),
                ("It makes your screen brighter", False,
                 "That is unrelated. The real risk is a hidden trojan."),
                ("It is always completely safe", False,
                 "The opposite. Unofficial software downloads are a classic source of trojans."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does spyware such as a keylogger do?",
            "options": [
                ("Secretly records what you do, like the passwords you type, and sends it to an attacker", True,
                 "Yes. Spyware works by staying hidden and quietly stealing information."),
                ("Locks your files and demands payment", False,
                 "That is ransomware, which wants to be noticed. Spyware stays hidden."),
                ("Makes your computer run faster", False,
                 "No. If anything it slows a device as it works in the background."),
                ("Backs up your files safely", False,
                 "No. Spyware steals your information; it does not protect it."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why does spyware often go unnoticed for a long time?",
            "options": [
                ("It is designed to stay hidden and make no obvious changes while it steals", True,
                 "Yes. Unlike ransomware it does not announce itself, so it can watch quietly for weeks."),
                ("It immediately locks you out of your computer", False,
                 "That is ransomware. Spyware does the opposite and hides."),
                ("It always shows a large warning on the screen", False,
                 "No. Announcing itself would defeat its purpose. Spyware stays quiet."),
                ("It only runs for one second and then deletes itself", False,
                 "No. It tends to sit and watch for as long as it can."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "An infected USB stick spreads malware only to people who open the file on it. This behaviour describes a:",
            "options": [
                ("Virus", True,
                 "Yes. It still needs a person to open the file, which is the mark of a virus rather than a self-spreading worm."),
                ("Worm", False,
                 "A worm would spread by itself without anyone opening anything. This one waits for a person."),
                ("Denial-of-service attack", False,
                 "A denial-of-service attack is a flood of traffic against a service, not an infected file on a USB stick."),
                ("Data breach", False,
                 "A breach is information being exposed. This is malware spreading through an opened file, a virus."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Most malware gets its first foothold by:",
            "options": [
                ("Someone opening an attachment, running a download, or clicking a bad link", True,
                 "Yes. Many entry points involve a person acting, which is why care at that moment stops so much malware."),
                ("Appearing on a computer with no cause at all", False,
                 "Malware needs a way in. It does not simply materialise from nothing."),
                ("The computer being too new", False,
                 "Age is not how malware arrives. It comes through downloads, attachments and links."),
                ("Having antivirus installed", False,
                 "Antivirus helps stop malware; it does not invite it in."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Which statement is true about the malware family?",
            "options": [
                ("A virus is one type of malware, alongside worms, trojans and spyware", True,
                 "Yes. Malware is the family; virus is a single member people often use as a catch-all by mistake."),
                ("Virus and malware mean exactly the same thing", False,
                 "No. A virus is one kind of malware, not the whole category."),
                ("Trojans spread by themselves like worms", False,
                 "No. Trojans wait to be run; worms self-spread."),
                ("Spyware always announces itself loudly", False,
                 "No. Spyware's whole point is to stay hidden."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Before malware can do any harm, it almost always needs:",
            "options": [
                ("A way in, usually a person opening, downloading or clicking something", True,
                 "Yes. Malware does not appear on its own. Something has to let it in, and that something is usually a person in a rushed moment."),
                ("A brand new computer", False,
                 "Age has nothing to do with it. Malware arrives through downloads, attachments and links."),
                ("A slow internet connection", False,
                 "Connection speed does not invite malware. A person opening or running something usually does."),
                ("Antivirus software installed", False,
                 "Antivirus helps keep malware out; it does not let it in."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "A very common way malware reaches a small business is through:",
            "options": [
                ("An email attachment or link that someone opens", True,
                 "Yes. A convincing email with a booby-trapped attachment or link is one of the most common delivery routes."),
                ("Leaving an office window open overnight", False,
                 "Physical windows are not how malware travels. It comes through files, links and downloads."),
                ("Using a wired keyboard", False,
                 "The kind of keyboard makes no difference to malware."),
                ("Turning the monitor brightness up", False,
                 "That has no effect on security at all."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A pop-up on a random website says your video player is out of date and you must download an update now. The safest move is to:",
            "options": [
                ("Ignore it and update software only from the maker or your app store", True,
                 "Right. Real updates come from the software itself or an official store, never from a scary pop-up on an unrelated website."),
                ("Click Download Update straight away", False,
                 "That download is the trap. A pop-up on an unrelated site is a classic way to deliver malware."),
                ("Pay the small fee it asks for", False,
                 "Never pay or download from a pop-up like this. Close the tab and move on."),
                ("Forward the pop-up to a friend to check", False,
                 "There is nothing to check. It is a fake designed to make you download malware. Just close it."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "An emailed document asks you to 'Enable content' or 'Enable macros' to view it. This is risky because:",
            "options": [
                ("Enabling macros can run hidden code that installs malware", True,
                 "Yes. Macros are little programs inside a document, and that Enable prompt is how attackers run malware. If unsure, do not enable it."),
                ("Macros change the colour of the text", False,
                 "This is not about appearance. Enabling macros can run code that infects your computer."),
                ("It uses extra printer ink", False,
                 "Ink has nothing to do with it. The risk is hidden code running when you enable macros."),
                ("Documents can never carry malware", False,
                 "They can. A booby-trapped document that asks you to enable content is a common delivery method."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Keeping your operating system and apps updated helps against malware because:",
            "options": [
                ("Updates patch the known holes that malware uses to get in", True,
                 "Yes. Many attacks rely on flaws the maker has already fixed. Installing updates closes those doors."),
                ("Updates make the screen bigger", False,
                 "That is not what updates do for security. They fix the flaws malware exploits."),
                ("Updates delete all your files", False,
                 "Updates do not wipe your files. They patch security holes."),
                ("Old software is always safer", False,
                 "The opposite. Out-of-date software still has open holes that malware can walk through."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "You find a USB stick in the car park labelled 'Staff Bonuses 2026'. The safe thing to do is:",
            "options": [
                ("Do not plug it in, and hand it to IT or your manager", True,
                 "Yes. A tempting label on a dropped USB is bait. Plugging it in can install malware in seconds."),
                ("Plug it in to find the owner", False,
                 "That is exactly what the attacker hopes. It can infect your machine the moment it connects."),
                ("Plug it into a customer's computer", False,
                 "Never connect an unknown USB to any machine, least of all a customer's."),
                ("Take it home and open it there", False,
                 "Same trap, different computer. Do not connect an unknown USB anywhere."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why is being careful at the moment you click or download so powerful against malware?",
            "options": [
                ("Because most malware needs that human action to get its first foothold", True,
                 "Yes. If the door is never opened, most malware never gets in. Your care at that moment stops a great deal."),
                ("Because clicking carefully makes the computer faster", False,
                 "Speed is not the point. Careful clicking denies malware the way in it depends on."),
                ("Because antivirus then stops being needed", False,
                 "Careful habits and antivirus work together. Neither replaces the other."),
                ("Because malware cannot exist if you are careful", False,
                 "Malware still exists. Careful habits stop most of it reaching you, which is the win."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Antivirus software is useful, but on its own it will not:",
            "options": [
                ("Stop a person being talked into installing or enabling something harmful", True,
                 "Right. Antivirus scans files and software. It cannot stop someone being persuaded to run malware themselves. Careful habits fill that gap."),
                ("Ever detect any malware at all", False,
                 "Antivirus does detect a lot of known malware. Its limit is the human decisions it cannot make for you."),
                ("Run on a computer", False,
                 "Antivirus runs perfectly well on a computer. The point is that it is not the whole answer."),
                ("Receive any updates", False,
                 "Good antivirus updates constantly. The gap it cannot cover is a person choosing to run something harmful."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "A text message says a parcel is held and rushes you to 'confirm your address' on a site that looks like a courier. Clicking it could:",
            "options": [
                ("Lead to a fake page that steals details, or a download that installs malware", True,
                 "Yes. A rushed message with a link is a classic delivery route, for both stolen details and malware."),
                ("Never cause any harm", False,
                 "It can. Fake courier messages are a very common way to deliver scams and malware."),
                ("Speed up your parcel", False,
                 "There is no parcel. The message exists to make you click a harmful link."),
                ("Automatically block all malware", False,
                 "It does the opposite. The link is the delivery method, not a defence."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "The single habit that shuts the most malware out at the door is:",
            "options": [
                ("Pausing before you open, download or run anything you did not expect", True,
                 "Yes. That short pause, checking who it is really from and whether you expected it, stops the majority of malware getting its foothold."),
                ("Buying a faster computer", False,
                 "Speed does not keep malware out. A moment's care at the point of clicking does."),
                ("Keeping the screen brightness low", False,
                 "That has no bearing on malware. The habit that matters is pausing before you open something."),
                ("Never turning the computer off", False,
                 "Leaving it on does nothing to keep malware out. Careful clicking does."),
            ],
        },
        # ================================================================
        # Lesson 2: ransomware, breaches, and reacting
        # ================================================================
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What does ransomware do?",
            "options": [
                ("Encrypts your files and demands a payment to unlock them", True,
                 "Yes, and a tested backup is what lets you recover without paying."),
                ("Floods a website with traffic", False,
                 "That is a denial-of-service attack. Ransomware locks your files and demands money."),
                ("Quietly records your passwords", False,
                 "That is spyware. Ransomware makes itself very much known."),
                ("Speeds up your computer", False,
                 "No. Ransomware locks you out of your own files."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Ransomware mainly attacks which security pillar?",
            "options": [
                ("Availability, because you cannot reach your own files", True,
                 "Yes. The files are still there and unchanged, you just cannot get to them."),
                ("Confidentiality, because the files are shown to the public", False,
                 "Classic ransomware locks files rather than publishing them. The core hit is to availability."),
                ("Integrity, because it edits your files to mislead you", False,
                 "It scrambles files wholesale rather than quietly editing them. The pillar lost is availability."),
                ("None, ransomware is harmless", False,
                 "It is among the most damaging attacks a business can face."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Why do authorities generally advise against paying a ransom?",
            "options": [
                ("It does not guarantee recovery, funds more crime, and marks you as a business that pays", True,
                 "Right. Payment is unreliable and it bankrolls the next attack, sometimes on you again."),
                ("Paying instantly removes the malware for good", False,
                 "It does not. Paying deals with the demand, not the infection or the open door."),
                ("The files unlock themselves after a week anyway", False,
                 "There is no such guarantee. Without a backup or a working key, encrypted files stay locked."),
                ("Backups are more expensive than a ransom", False,
                 "Backups are far cheaper and, unlike a payment, they actually work."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is the best defence that lets a business recover from ransomware without paying?",
            "options": [
                ("Recent backups that have been tested and can actually be restored", True,
                 "Yes. A clean copy to restore takes away the attacker's leverage entirely."),
                ("A faster internet connection", False,
                 "Speed does nothing against ransomware."),
                ("Paying quickly for a discount", False,
                 "Paying is unreliable and funds crime. A tested backup is the real answer."),
                ("Turning the computer off and on again", False,
                 "That will not undo the encryption ransomware applies."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Which of these is an attack on the whole business at once, rather than a single device?",
            "options": [
                ("Ransomware locking every file on the shared drive", True,
                 "Yes. When the shared drive is locked for everyone, the whole business is affected and it needs a coordinated response."),
                ("A keylogger on one reception computer", False,
                 "Serious, but it sits on one device that can be isolated and cleaned."),
                ("A virus in an attachment one person opened", False,
                 "That starts on a single machine, even if it can spread when forwarded."),
                ("A trojan on one staff member's laptop", False,
                 "That affects the one laptop, not the whole organisation at once."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You realise ransomware is encrypting files on your PC. Sensible first move?",
            "options": [
                ("Disconnect the computer from the network to stop it spreading", True,
                 "Yes. Getting it off the network first limits the spread to shared drives and other machines."),
                ("Keep working and hope it stops", False,
                 "Carrying on just gives it time to encrypt more and reach others. Disconnect first."),
                ("Pay the ransom immediately", False,
                 "Not the first move, and often not needed at all. Contain it, then report and get advice."),
                ("Email the ransom note to all staff to warn them", False,
                 "Warning people matters, but the urgent first action is to disconnect and contain the spread."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "After disconnecting an infected machine, the next best step is to:",
            "options": [
                ("Report it to whoever looks after IT straight away", True,
                 "Yes. Fast reporting gets the right people acting while the damage is small, and there is no trouble for raising it early."),
                ("Say nothing in case you get blamed", False,
                 "Staying quiet lets the problem grow. Early, blame-free reporting is what limits the damage."),
                ("Reconnect it to see if the problem fixed itself", False,
                 "Reconnecting risks spreading the infection again. Keep it isolated and report it."),
                ("Wait a week to see what happens", False,
                 "Waiting only gives an attacker time. Report it now."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is a data breach?",
            "options": [
                ("Personal information being taken or exposed to people who should not have it", True,
                 "Yes. A breach is a failure of confidentiality: private data ends up in the wrong hands."),
                ("Your files being encrypted for ransom", False,
                 "That is ransomware. A breach is about data being exposed, not locked."),
                ("A website being flooded with traffic", False,
                 "That is a denial-of-service attack. A breach is about information leaking, not availability."),
                ("A computer running slowly", False,
                 "That is a performance issue, not a data breach."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A data breach is mainly a failure of which pillar?",
            "options": [
                ("Confidentiality, because private data reaches the wrong people", True,
                 "Yes. The systems may keep running; the harm is who can now see the information."),
                ("Availability, because you cannot reach your files", False,
                 "That is ransomware or a denial-of-service attack. In a breach the data is often still accessible to you; it has just also leaked."),
                ("Integrity, because the data is secretly altered", False,
                 "A breach is usually about exposure, not quiet alteration. The pillar lost is confidentiality."),
                ("Speed, because the network slows down", False,
                 "Speed is not one of the three pillars. A breach is a confidentiality failure."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Roughly how many people were affected by the 2022 Optus breach?",
            "options": [
                ("In the order of 9.8 million current and former customers", True,
                 "Yes, a striking share of the Australian population caught in one incident."),
                ("About 500 people", False,
                 "It was vastly larger, reported to be around 9.8 million people."),
                ("Nobody was actually affected", False,
                 "A very large number were affected, reported to be around 9.8 million."),
                ("Exactly 100", False,
                 "The reported figure was far higher, in the order of 9.8 million."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "What was the widely reported cause of the Optus breach?",
            "options": [
                ("An access point to customer data was reachable over the internet without a login", True,
                 "Yes. On public reporting, a door that should have required a login did not, a failure of the basics."),
                ("A worm spread through the whole network", False,
                 "That is not what was reported. The issue was an exposed access point needing no login."),
                ("Every customer was individually phished", False,
                 "The breach was on the company's side, an exposed system, not customers being phished one by one."),
                ("The building's power was cut", False,
                 "A power cut is not a data breach. The reported cause was an exposed access point."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why was the data exposed in the Optus breach especially serious?",
            "options": [
                ("It included identity document numbers, which can be used to attempt identity theft", True,
                 "Yes. Names, birth dates and document numbers together are the ingredients for impersonating someone."),
                ("It was only marketing preferences", False,
                 "It went far beyond that, reaching identity document numbers for some of those affected."),
                ("The data was encrypted and unreadable", False,
                 "This was a breach, not ransomware. The exposed data was readable, which is the problem."),
                ("Nothing sensitive was involved", False,
                 "A great deal was, including identity document numbers for a portion of people affected."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What made the Medibank breach particularly sensitive?",
            "options": [
                ("It exposed health claims information, some of the most private data there is", True,
                 "Yes. Health records can cause real distress if exposed, quite apart from any financial fraud."),
                ("It only exposed public phone book listings", False,
                 "It went well beyond public information, into private health claims data."),
                ("No personal information was involved", False,
                 "A great deal of personal and health information was involved."),
                ("It was a traffic flood that stole nothing", False,
                 "It was a data breach, and sensitive health data was taken."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "On public reporting, how did attackers get into Medibank's systems?",
            "options": [
                ("Using a stolen login credential, appearing to be a genuine user", True,
                 "Yes. A stolen username and password opened the door, which is why unique passwords and two-factor matter so much."),
                ("By flooding the site with traffic", False,
                 "That is a denial-of-service attack. Medibank was a data breach via a stolen login."),
                ("By leaving a database open with no password", False,
                 "That was closer to the Optus account. Medibank reportedly involved a stolen credential."),
                ("By infecting customers with a virus", False,
                 "The reported entry point was a stolen login, not a virus spread among customers."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Medibank chose not to pay the ransom. What did the attackers then do?",
            "options": [
                ("Published the stolen data, showing that not paying carries a heavy cost too", True,
                 "Yes. It was a stark example that once sensitive data is taken, there are no good options left."),
                ("Quietly deleted all the stolen data", False,
                 "They did the opposite and published it. Attackers cannot be trusted to delete anything."),
                ("Returned the data and apologised", False,
                 "Criminals do not do that. They published the data when the ransom was refused."),
                ("Restored the company's files for free", False,
                 "This was a breach, not ransomware on Medibank's files. The attackers published the stolen data."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You are told your details were in a company's data breach. A sensible first step is to:",
            "options": [
                ("Change that account's password and anywhere you reused it, and turn on two-factor", True,
                 "Yes. You cannot recall leaked data, but you can lock down the accounts so it is harder to misuse."),
                ("Do nothing, since the data is already out", False,
                 "There is plenty you can still do to reduce the risk to your accounts."),
                ("Pay any fee the follow-up message asks for", False,
                 "The opposite. Messages quoting your breached details are usually the follow-on scam."),
                ("Post your new password publicly so it is on record", False,
                 "Never share a password. Keep it private and unique."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why do phishing scams often spike right after a big breach?",
            "options": [
                ("Scammers use the leaked real details to make their messages far more convincing", True,
                 "Yes. A message that quotes your real name or provider is much harder to doubt, so breaches fuel the next round of phishing."),
                ("Breaches make everyone's spam filter stop working", False,
                 "Filters keep working. The spike comes from scammers exploiting the leaked details."),
                ("Companies send more genuine emails after a breach", False,
                 "The surge is scam messages exploiting the breach, not a rise in genuine mail."),
                ("Phishing has nothing to do with breaches", False,
                 "They are closely linked. Breached data is raw material for more convincing phishing."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Files on a machine suddenly being renamed with odd new extensions is a hallmark of:",
            "options": [
                ("Ransomware", True,
                 "Yes. Mass renaming as files are encrypted, often with a new extension, is a classic ransomware sign."),
                ("A denial-of-service attack", False,
                 "That floods a service with traffic; it does not rename your local files."),
                ("A slow internet connection", False,
                 "That would not rename files. Mass renaming points to ransomware."),
                ("A normal software update", False,
                 "Updates do not scramble your files and rename them. That pattern is ransomware."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Which of these is a classic warning sign worth reporting?",
            "options": [
                ("Colleagues receiving strange emails 'from you' that you never sent", True,
                 "Yes. That strongly suggests your account or device is compromised, and it is worth reporting straight away."),
                ("Your computer working exactly as normal", False,
                 "That is reassuring, not a warning sign."),
                ("An expected email from a known colleague", False,
                 "That is normal activity, not a warning sign."),
                ("A website loading slowly once, then fine", False,
                 "A single slow load is usually nothing. Watch for persistent or unexplained changes instead."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "The calm approach to a possible threat is best summed up as:",
            "options": [
                ("Notice the change, then check, rather than panicking or ignoring it", True,
                 "Yes. Calm attention beats both alarm and denial, and a quick check with IT usually settles it."),
                ("Assume the worst and shut everything down immediately", False,
                 "Over-reacting to every hiccup causes its own harm and burns out your alertness."),
                ("Ignore everything unless the whole office stops working", False,
                 "By then a threat has had free rein. Early noticing and checking is far better."),
                ("Only worry if a message tells you to worry", False,
                 "Scam messages often tell you to act. Your own calm judgement matters more than their prompts."),
            ],
        },
    ],
}
