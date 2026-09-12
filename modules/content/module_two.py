"""Module 2, Recognising Cyber Threats: understand it, then apply it.

  Lesson 1  UNDERSTAND IT  — a teaching lesson. Four reading panels, each with a
            real visual: what malware is and its family, how it gets into a small
            business, what ransomware does and how to beat it, and data breaches
            plus the Notifiable Data Breaches scheme, using the real 2022 Optus
            and Medibank incidents. One light comprehension check.
  Lesson 2  APPLY IT       — a practical lesson. Five hands-on tasks that make the
            learner use it: sort malware behaviours, triage a mixed inbox,
            diagnose ransomware/breach/glitch, read a fake-update pop-up, and work
            a ransomware incident.

Voice: warm, plain Australian English, no em-dashes, no emoji. The real cases
(Optus and Medibank, both 2022) are presented as widely reported factual
scenarios, framed evenly and without blame.

Sources (current as cited, framed as general information):
- ACSC / cyber.gov.au guidance on malware and ransomware (do not pay; keep
  offline, tested backups; the 3-2-1 rule).
- OAIC Notifiable Data Breaches Report, July to December 2024: 595 breaches in
  the half and 1,113 across 2024 (a record); 69% from malicious or criminal
  attack; phishing the leading cause of cyber-incident breaches; the health
  sector the most-breached (about 20%). Under the Privacy Act 1988, an
  organisation must assess a suspected eligible breach within 30 days and, if
  serious harm is likely, notify the OAIC and the affected individuals.
- The 2022 Optus (about 9.8 million people) and Medibank (about 9.7 million
  people) incidents.
Points sum to 10 per lesson and bank at lesson end.
"""

LESSONS = [
    {
        "title": "Know the threats: malware, ransomware, and breaches",
        "reading_time_minutes": 9,
        "intro": "Meet the threats a small business actually faces. What malware "
        "is and how it gets in, what ransomware does, and what a data breach means, "
        "using the real Australian incidents. By the end you will be able to name "
        "the threat and know how to keep it out.",
        "tasks": [
            {
                "key": "malware-family",
                "kind": "concept",
                "points": 2,
                "title": "Malware is a family, not one thing",
                "diagram": "malware-family",
                "body": "<p><strong>Malware</strong> means malicious software: any "
                "program built to do harm. It is the engine behind most serious "
                "incidents, and understanding it matters because malicious or "
                "criminal attacks were behind <strong>69% of the data breaches "
                "reported to the OAIC</strong> in the second half of 2024. People "
                "say virus for all of it, but a virus is only one member of a whole "
                "family, and each behaves differently, so what stops one does little "
                "against another. The tell is always in the <em>behaviour</em>, "
                "which is really a program doing one specific job:</p>"
                "<ul>"
                "<li><strong>Virus</strong>: hides its code inside a normal file "
                "and only runs, and spreads, when a person opens that file. It needs "
                "a human to act first.</li>"
                "<li><strong>Worm</strong>: copies itself from machine to machine "
                "across the network on its own, with no clicks needed, by exploiting "
                "a weakness. That self-spreading is why a worm can take out a whole "
                "office in minutes.</li>"
                "<li><strong>Trojan</strong>: disguised as something you want, a "
                "free copy of paid software, a handy tool, so you install it "
                "yourself. Once running, it does its real, hidden job.</li>"
                "<li><strong>Spyware</strong>: hides and quietly watches, recording "
                "the passwords and card numbers you type and sending them to an "
                "attacker. You often never notice it is there.</li>"
                "<li><strong>Ransomware</strong>: encrypts your files and demands "
                "payment to unlock them. It is the most disruptive kind for a small "
                "business, and it gets its own panel next.</li>"
                "</ul>"
                "<div class=\"cy-callout\">Name it by what it does: does it wait for "
                "a click, spread itself, wear a disguise, hide and watch, or lock "
                "and demand? The behaviour tells you which defence stops it.</div>",
            },
            {
                "key": "how-it-gets-in",
                "kind": "concept",
                "points": 2,
                "title": "How it gets in, and why one click spreads",
                "diagram": "malware-vectors",
                "body": "<p>Malware almost never appears on its own. Someone has to "
                "let it in, usually a person tricked in a busy moment, which is "
                "exactly why <strong>phishing is the single leading cause</strong> "
                "of the cyber-incident breaches reported to the OAIC. What makes one "
                "click so serious is what happens next: on a flat network, where "
                "every machine shares one space, a single opened attachment can "
                "spread from computer to computer until the whole office is hit. "
                "Splitting the network into zones, called segmentation, is what stops "
                "it at the first machine. A dropped USB like the one above is one of "
                "the everyday ways it arrives.</p>"
                "<p>The everyday routes in are few, and once you know them you can "
                "see them coming:</p>"
                "<ul>"
                "<li><strong>A dodgy attachment.</strong> An email attachment can look "
                "like an invoice, but read the file name to the very end: "
                "<strong>Invoice_4471.pdf.exe</strong>. A file name can carry more "
                "than one extension, and only the <em>last</em> one decides what it "
                "really is. Here that is <strong>.exe</strong>, a program that runs "
                "code the moment you open it. The .pdf in the middle is pure "
                "disguise.</li>"
                "<li><strong>A fake update or download.</strong> A pop-up on an "
                "unrelated website rushes you to download an update. Real updates "
                "come from the software itself or an app store, never a pop-up on a "
                "random page.</li>"
                "<li><strong>The Enable content trap.</strong> A document asks you "
                "to enable macros or content to view it. Macros are small programs "
                "inside the document, and enabling them can run hidden malware. This "
                "is common enough that the ASD Essential Eight lists disabling "
                "untrusted macros as a core control.</li>"
                "<li><strong>An infected USB.</strong> A dropped stick with a "
                "tempting label like Payroll 2026 is bait, left to be found and "
                "plugged in, not a lost item.</li>"
                "<li><strong>Unpatched software.</strong> Out-of-date programs have "
                "known holes that are freely documented, and attackers scan for "
                "them constantly. This is exactly the gap automatic updates "
                "close.</li>"
                "</ul>"
                "<div class=\"cy-callout\">Before you act on anything unexpected, "
                "pause and ask where it really came from. Verify first, share "
                "nothing, plug in nothing.</div>",
            },
            {
                "key": "ransomware",
                "kind": "concept",
                "points": 2,
                "title": "Ransomware, and how a business beats it",
                "diagram": "ransom-screen",
                "body": "<p><strong>Ransomware</strong> is the one that hits a whole "
                "business at once. It works by <strong>encryption</strong>, the same "
                "maths that protects a banking website, turned against you: it "
                "scrambles your files with a key only the attacker holds, renames "
                "them (often with an ending like <strong>.locked</strong>), and "
                "leaves a note demanding payment for the key, usually with a "
                "countdown to rush you.</p>"
                "<p>It attacks <strong>availability</strong>: the files are still "
                "there, byte for byte, you simply cannot read them without the key. "
                "If it reaches a shared drive, everyone is stopped at once. Modern "
                "attacks add a second squeeze, called <strong>double "
                "extortion</strong>: before locking the files, the attacker copies "
                "them out, then threatens to publish your customer data unless you "
                "pay. That is the tactic used against Medibank, and it means a "
                "backup alone no longer makes the threat disappear.</p>"
                "<p>Even so, a business beats ransomware not with the wallet, but "
                "with the plan:</p>"
                "<ul>"
                "<li><strong>Back up, the 3-2-1 way</strong>: three copies, on two "
                "kinds of storage, with one kept offline or offsite so the "
                "ransomware cannot reach it. A clean, tested backup is what lets you "
                "restore without ever paying for the key.</li>"
                "<li><strong>Do not pay.</strong> The ACSC advises against it: "
                "payment does not guarantee you get a working key, it funds the next "
                "attack, it marks you as someone who pays, and it leaves the way in "
                "still open.</li>"
                "<li><strong>Contain, then report.</strong> The first move when it "
                "strikes is to disconnect the machine from the network so it cannot "
                "spread, then report it, including to the ACSC via ReportCyber.</li>"
                "</ul>"
                "<div class=\"cy-callout\">The countdown is pressure, not a deadline "
                "you must meet. A tested, offline backup, not the ransom, is what "
                "gets you working again.</div>",
            },
            {
                "key": "breaches-law",
                "kind": "concept",
                "points": 2,
                "title": "Data breaches, and the law that follows",
                "diagram": "data-breach",
                "body": "<p>A <strong>data breach</strong> is the opposite failure "
                "to ransomware. Nothing is locked, but private information is copied "
                "and exposed to people who should not have it, a failure of "
                "<strong>confidentiality</strong>. Once data is out, it cannot be "
                "recalled, which is what makes a breach so serious. This is not "
                "rare: the OAIC was notified of <strong>1,113 data breaches across "
                "2024, a record</strong><span class=\"cy-cite\">1</span>, and the "
                "<strong>health sector reported the "
                "most</strong> of any. Australia's two landmark cases, both in 2022, "
                "show how it happens:</p>"
                "<ul>"
                "<li><strong>Optus.</strong><span class=\"cy-cite\">2</span> "
                "Information on roughly 9.8 million "
                "current and former customers was exposed through an access point to "
                "customer data that was reachable over the internet without a login. "
                "For some people it included identity document numbers like passport "
                "and licence numbers, the raw material for identity theft.</li>"
                "<li><strong>Medibank.</strong><span class=\"cy-cite\">3</span> "
                "Attackers got in using a stolen login "
                "that reached the network through a remote-access connection that did "
                "not require a second factor. They took sensitive health data on "
                "about 9.7 million people. Medibank chose not to pay the ransom, and "
                "the attackers published the stolen data. A stark reminder that once "
                "sensitive data is taken there are no good options left, and that "
                "multi-factor authentication on remote access is not optional.</li>"
                "</ul>"
                "<p>The law here is the <strong>Notifiable Data Breaches "
                "scheme</strong> under the Privacy Act 1988. If personal information "
                "is exposed in a way "
                "<strong>likely to result in serious harm</strong>, the organisation "
                "must <strong>assess it within 30 days</strong> and, where the bar is "
                "met, notify both the regulator (the OAIC) and the affected people, "
                "telling those people what steps to take to protect themselves. The "
                "point of notifying is practical: it gives people the chance to "
                "change a password or watch their accounts before the harm "
                "lands.</p>"
                "<div class=\"cy-callout\">Ransomware locks what you have; a breach "
                "leaks what you hold. Both are serious, and a breach of personal data "
                "can carry a legal duty, on a 30-day clock, to tell people.</div>"
                "<div class=\"cy-sources\"><div class=\"cy-sources__h\">Sources</div>"
                "<ol>"
                "<li><span class=\"cy-sources__n\">1</span> OAIC Notifiable Data "
                "Breaches Report, January to December 2024 (oaic.gov.au).</li>"
                "<li><span class=\"cy-sources__n\">2</span> Optus 2022 data breach, "
                "as reported to the OAIC (oaic.gov.au).</li>"
                "<li><span class=\"cy-sources__n\">3</span> Medibank 2022 data breach, "
                "OAIC investigation (oaic.gov.au).</li>"
                "</ol></div>",
            },
            {
                "key": "enable-content",
                "kind": "check",
                "points": 2,
                "title": "Quick check: the Enable Content banner",
                "diagram": "enable-macros",
                "body": "<p>One quick check to finish, on the Enable content trap you "
                "just read about. Tanya opens a spreadsheet attached to an email, "
                "'Statement_Feb.xlsm', and the yellow security bar above appears "
                "across the top. The sheet looks blank until she clicks the button. "
                "Read the bar, then answer.</p>"
                "<div class=\"cy-callout\">Macros are small programs inside a "
                "document. A file that only works once you enable them is a warning, "
                "not an instruction.</div>",
                "question": "The document shows a 'Security Warning: macros disabled' bar with an Enable Content button, and is blank until you click it. What should Tanya do?",
                "hint": "What does Enable Content actually turn on, and why would a genuine statement need it?",
                "options": [
                    ("Not click Enable Content. A statement that is blank until you enable macros is a classic malware trap; close it and reach the sender a way she already trusts", True,
                     "Right. Enable Content switches on macros, which are programs inside the file that can run hidden malware. A real statement does not need macros to be readable. The blank sheet is bait to make her click. Disabling untrusted macros is a core ASD Essential Eight control."),
                    ("Click Enable Content, since the document clearly needs it to display", False,
                     "No. That is exactly the trap. The document is blank on purpose so you enable the macros, which can then run malware. A real statement does not need macros to be read."),
                    ("Click Enable Content but only if the sender's name looks familiar", False,
                     "No. A name is easy to fake, and a compromised mailbox sends from a real address. Never enable macros to view a document; verify the file another way."),
                    ("Save the file and open it later when there is more time", False,
                     "No. Saving it changes nothing; enabling macros later is the same risk. Do not enable content on an unexpected document at all."),
                ],
            },
        ],
    },
    {
        "title": "Put it to work: name it, triage it, react to it",
        "reading_time_minutes": 9,
        "intro": "Now use it. You are at Ballarat Auto Spares, a busy parts "
        "wholesaler and counter shop, on a Monday with the trade rush on. Owner Rick "
        "Halloran, office admin Tanya Pillai and bookkeeper Dolores Fenn keep it "
        "running. Sort malware by how it behaves, triage the real morning inbox, "
        "diagnose what kind of trouble you are looking at, read a fake security "
        "alert, and work a ransomware incident from the first move to recovery.",
        "tasks": [
            {
                "key": "sort-malware",
                "kind": "sort",
                "points": 2,
                "title": "Sort the behaviour to its malware type",
                "body": "<p>Lesson 1 introduced the malware family. Now prove you "
                "can tell them apart by behaviour, which is what matters, because "
                "each is stopped by different defences. Read each behaviour and "
                "sort it to the member that fits.</p>"
                "<div class=\"cy-callout\">The tell is in HOW it behaves: does it "
                "spread itself, wait for a click, wear a disguise, hide and watch, "
                "or lock and demand?</div>",
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
                        {"text": "A supplier's price-list spreadsheet runs a hidden script the moment Dolores opens it, and not before", "bucket": "virus",
                         "why": "That is a virus. It rides inside a normal-looking file and only runs when a person opens it. No open, no infection."},
                        {"text": "Overnight, one infected counter PC copies the malware to every other machine on the shop network by itself, no clicks", "bucket": "worm",
                         "why": "That is a worm. Spreading machine to machine on its own, with no human action, is exactly what lets it take out a whole office fast."},
                        {"text": "A 'free' invoicing tool Josh downloads to save time installs fine, then quietly opens a back door for the attacker", "bucket": "trojan",
                         "why": "That is a trojan. You install it yourself because it looks useful, and then it does its real, hidden job."},
                        {"text": "A program sits unseen on the office PC, logging the bank passwords Rick types and sending them out", "bucket": "spyware",
                         "why": "That is spyware. It hides and steals information quietly rather than announcing itself."},
                        {"text": "Every file in the Accounts folder is renamed to end .locked and a screen demands payment to unlock them", "bucket": "ransomware",
                         "why": "That is ransomware. Locking your files in place and demanding money to release them is its signature."},
                        {"text": "The malware jumps onto the workshop's USB stock-take stick and rides it to the next PC it is plugged into", "bucket": "worm",
                         "why": "Still a worm. Self-copying onto other drives and machines with no help is the worm's calling card."},
                    ],
                },
            },
            {
                "key": "triage-inbox",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the morning inbox",
                "body": "<p>The commonest way malware reaches a small business is the "
                "inbox. Here is a mixed morning's mail: some genuine, some carrying "
                "malware or trying to trick you into installing it. Read the sender, "
                "the subject and the preview, then mark each Genuine or Phishing. "
                "The verdict and the tell are revealed as you go.</p>"
                "<div class=\"cy-callout\">The tells to weigh: is it expected, who "
                "is it really from, is it rushing you, and is it pushing an "
                "attachment, a link or an Enable content prompt?</div>",
                "payload": {
                    "prompt": "Mark each message Genuine or Phishing. Sort all five to finish.",
                    "emails": [
                        {"from": "Rick Halloran <rick@ballaratautospares.com.au>",
                         "subject": "Roster for the Show Day long weekend",
                         "preview": "Counter cover sorted for Saturday. Shout if the times don't suit. No action needed.",
                         "phish": False,
                         "why": "An expected note from the owner on the shop's own domain, asking nothing of you and pushing no link or attachment."},
                        {"from": "Repco Trade <accounts@repco-tradeportal.net>",
                         "subject": "OVERDUE: pay invoice INV-88231 today to avoid account hold",
                         "preview": "Your trade account is about to be suspended. Open the attached Statement.zip and pay within 24 hours.",
                         "phish": True,
                         "why": "A real supplier's account team does not chase you from a lookalike domain with a .zip and a countdown. The pressure and the zip attachment are the tells: opening it can install malware."},
                        {"from": "Australia Post <track@auspost-delivery-au.com>",
                         "subject": "Your parts delivery is held, pay a small redelivery fee",
                         "preview": "We could not deliver your order. Confirm your address and pay $1.99 through the link to release it.",
                         "phish": True,
                         "why": "A lookalike Australia Post domain, a tiny fee and a link to grab your card. Track a parcel through the official app or website, never a link like this."},
                        {"from": "Dolores Fenn <dolores@ballaratautospares.com.au>",
                         "subject": "Feb BAS figures ready for your check",
                         "preview": "Numbers are in the shared Accounts folder when you get a sec. Nothing urgent.",
                         "phish": False,
                         "why": "A normal, expected message from the bookkeeper you know, on the shop domain, with no link, no attachment and no pressure."},
                        {"from": "MYOB Billing <billing@myob-secure-login.com>",
                         "subject": "Action required: update payment details, enable content to view",
                         "preview": "Open the attached statement and click Enable Content to keep your subscription active.",
                         "phish": True,
                         "why": "The Enable content trick from a lookalike of a tool you really use. Enabling content runs macros that can install malware. Log in to MYOB directly instead."},
                    ],
                },
            },
            {
                "key": "diagnose",
                "kind": "classify",
                "points": 2,
                "title": "Diagnose the trouble",
                "body": "<p>When something goes wrong, the first skill is naming it: "
                "is this <strong>ransomware</strong> (files locked, payment "
                "demanded), a <strong>data breach</strong> (private data exposed), "
                "or just an ordinary <strong>glitch</strong>? Not every problem is "
                "an attack. Read each situation and diagnose it.</p>"
                "<div class=\"cy-callout\">Ransomware locks what you have; a breach "
                "leaks what you hold; a glitch is everyday equipment trouble.</div>",
                "payload": {
                    "prompt": "Read each situation and tap the kind of trouble it is. Diagnose all six to finish.",
                    "categories": [
                        {"id": "ransomware", "label": "Ransomware"},
                        {"id": "breach", "label": "Data breach"},
                        {"id": "glitch", "label": "Ordinary glitch"},
                    ],
                    "events": [
                        {"text": "Every file in the shop's Accounts folder is renamed to end .locked, and a red screen demands Bitcoin to unlock them.",
                         "category": "ransomware",
                         "why": "Ransomware. Files locked in place plus a payment demand is its signature. Your data is still there, you just cannot reach it."},
                        {"text": "A customer rings: the card they used on the shop's online order form has been used for fraud, and others say the same.",
                         "category": "breach",
                         "why": "A data breach. Customer details have been exposed to people who should not have them, a failure of confidentiality that must be assessed."},
                        {"text": "The counter eftpos terminal freezes about 3pm most days and needs a quick reboot to come good.",
                         "category": "glitch",
                         "why": "An ordinary glitch. Routine equipment trouble with a mundane cause, not a security incident."},
                        {"text": "A parts supplier emails to say they were hacked, and the trade-account login the shop saved with them may be exposed.",
                         "category": "breach",
                         "why": "A data breach, on their side. Your login is exposed, so change that password anywhere it was reused and turn on two-factor."},
                        {"text": "The stock-lookup database is slow to load all morning. You check the server and its disk is 98% full.",
                         "category": "glitch",
                         "why": "An ordinary glitch. A nearly full disk is a common, harmless cause of slowness. Not every problem is an attack."},
                        {"text": "A workshop PC is stuck behind a full-screen countdown demanding payment to release the job files.",
                         "category": "ransomware",
                         "why": "Ransomware. The lock plus the countdown pressure to pay is the tell. Disconnect it, do not pay, report it."},
                    ],
                },
            },
            {
                "key": "read-scareware",
                "kind": "check",
                "points": 2,
                "title": "Read the security alert like an investigator",
                "diagram": "scareware-popup",
                "body": "<p>A picture-question. While Josh was looking up a part, the "
                "full-screen alert above took over the browser: a flashing 'Windows "
                "Defender' warning that the PC is infected, with a phone number to "
                "call now and a siren. Read it the way an investigator would, then "
                "answer.</p>"
                "<div class=\"cy-callout\">Real security software does not take over "
                "your browser, blast a siren, or ask you to phone a number. That is a "
                "scareware scam.</div>",
                "question": "Looking at this alert, what is the strongest sign it is a scam, not a real virus warning?",
                "hint": "Where did it appear, and what is it pressuring Josh to do?",
                "options": [
                    ("It appears inside the web browser and pushes him to phone a support number, which no real security tool ever does", True,
                     "Right. It is a web page pretending to be Windows, using a siren and a phone number to panic you into calling a fake 'support' line that will ask for remote access or payment. Real security software never cold-calls you or asks you to phone it. Close the tab; if it will not close, close the browser."),
                    ("It uses the Windows Defender name", False,
                     "The borrowed name is not the tell. The giveaway is that a web page is impersonating Windows and telling you to phone a number, which real security never does."),
                    ("It says the PC is infected", False,
                     "A claim of infection is easy to print on a page. The real sign is that it appeared in the browser and wants you to call a number, not that it names a threat."),
                    ("It has a red background", False,
                     "The colour means nothing. The real signs are that it hijacked the browser and is pushing Josh to phone a 'support' number."),
                ],
            },
            {
                "key": "ransomware-morning",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: a ransom note takes over your screen",
                "hero": "infection-spread",
                "body": "<p>First, watch it happen. The animation above is why your "
                "first move matters so much: on a flat network the infection reaches "
                "every machine, while segmentation seals it into one zone. Now the "
                "drill.</p>"
                "<p>The real test is what you do in the moment. The incident "
                "unfolds below: you choose your move and see the consequence before "
                "the next decision. Your first move decides how far it spreads and "
                "whether you recover cleanly. Draw on everything Lesson 1 taught "
                "about ransomware.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> contain it, "
                "report it, and restore from backup. Never lead with the ransom.</div>",
                "payload": {
                    "prompt": "The incident unfolds. Make each call and see how it plays out.",
                    "start": "note",
                    "nodes": {
                        "note": {
                            "text": "It is 4pm on a Monday, mid trade rush. Dolores is reconciling supplier invoices when files across her screen start renaming one after another, and a red screen takes over: your files are encrypted, pay 0.05 Bitcoin (about $3,400) within 72 hours. The shop's Accounts folder is on the shared drive. What is your first move?",
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
                                 "feedback": "Even contained, paying is the wrong call. With the spread stopped, the answer is report, then restore from backup.", "to": "clean_bad"},
                            ],
                        },
                        "clean_bad": {
                            "text": "Cleaning it alone or paying destroys your position: it can wipe evidence, miss a second infected machine, or reward the attacker. Report it so the right people check the whole picture, then restore from backup.",
                            "choices": [],
                        },
                        "restore": {
                            "text": "Reported. IT confirms last night's backup is clean and tested. How do you get back to work?",
                            "choices": [
                                {"label": "Wipe the machine, then restore the files from the clean backup.", "outcome": "good",
                                 "feedback": "That is the whole point of a backup: it takes away the attacker's leverage entirely. No payment needed.", "to": "win"},
                                {"label": "Pay the ransom to save the hassle of restoring.", "outcome": "bad",
                                 "feedback": "With a clean backup in hand, paying makes no sense at all. Restore, do not pay.", "to": "reconnect_bad"},
                                {"label": "Reconnect the infected machine to check if the files came back.", "outcome": "bad",
                                 "feedback": "Reconnecting an infected machine risks spreading it again. Keep it isolated, wipe it, and restore from the clean backup.", "to": "reconnect_bad"},
                            ],
                        },
                        "reconnect_bad": {
                            "text": "Reconnecting an infected machine, or paying with a clean backup in hand, undoes your good work. Keep it isolated, wipe it, and restore from the clean backup instead.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Contained, reported, and restored from backup with nothing paid. That is exactly how a business beats ransomware: the backup, not the wallet, is what saves you.",
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
        # ---- Lesson 1: understand it (the threats) ----
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
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "In the 2022 Optus and Medibank incidents, private customer data was exposed. Which security pillar does a data breach mainly fail, and what law can apply?",
            "options": [
                ("Confidentiality, and the Notifiable Data Breaches scheme can require telling the OAIC and the affected people", True,
                 "Yes. A breach exposes private data (confidentiality), and if serious harm is likely, the Privacy Act requires notifying the regulator and those affected."),
                ("Availability, because customers could not reach the files", False,
                 "No. That is ransomware. A breach is about data being exposed, not access being blocked."),
                ("Integrity, because the data was secretly altered", False,
                 "No. A breach is usually about exposure, not quiet alteration. The pillar lost is confidentiality."),
                ("None, because a breach is not really a security problem", False,
                 "No. A breach of private data is a serious confidentiality failure, and it can carry a legal duty to notify."),
            ],
        },
        # ---- Lesson 2: apply it (name, triage, react) ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A full-screen 'Windows Defender' alert appears inside your web browser saying the PC is infected and to phone a support number now. What is the safe move?",
            "options": [
                ("Close the tab or the whole browser; real security software never takes over your browser or asks you to phone a number", True,
                 "Yes. It is a web page impersonating Windows, using panic to get you to call a fake support line that will ask for remote access or payment. Close it and move on."),
                ("Phone the number so a technician can remove the virus", False,
                 "No. That number reaches the scammers. They will ask to remote in or for payment. Real security never cold-calls or asks you to phone it."),
                ("Click the alert to run the recommended scan", False,
                 "No. Clicking is what they want; it can install the very malware it claims to find. Close the tab instead."),
                ("Pay the fee it asks for to clean the PC", False,
                 "No. Never pay a browser pop-up. It is a scam. Close it and, if it will not close, close the browser."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "A spreadsheet attached to an email is blank until you click a yellow 'Enable Content' bar at the top. What should you do?",
            "options": [
                ("Do not enable content; a document that is blank until you enable macros is a trap, so verify it a way you already trust", True,
                 "Yes. Enable Content turns on macros, small programs inside the file that can run malware. A genuine statement does not need macros to be read. The blank sheet is bait."),
                ("Enable content, since the file clearly needs it to display", False,
                 "No. That is exactly the trap. The file is blank on purpose so you switch on the macros, which then run. A real document does not need them."),
                ("Enable content only if the sender's name looks right", False,
                 "No. A name is easy to fake, and a hacked mailbox sends from a real address. Never enable macros to view a document."),
                ("Print the document instead of opening it", False,
                 "No. It is blank without the macros, so printing shows nothing, and the risk is enabling them at all. Verify the file another way."),
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
