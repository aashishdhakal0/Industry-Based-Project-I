"""Module 2, Recognising Cyber Threats: understand it, then apply it.

  Lesson 1  UNDERSTAND IT, a teaching lesson. Four reading panels, each with a
            real visual: what malware is and its family, how it gets into a small
            business, what ransomware does and how to beat it, and data breaches
            plus the Notifiable Data Breaches scheme, using the real 2022 Optus
            and Medibank incidents. One light comprehension check.
  Lesson 2  APPLY IT, hands-on interactive artefacts distinct from Lesson 1's
            reading: name a detection from the shop's own protection history
            (SORT), triage a real Gmail inbox (MAILSORT), order the ransomware
            response in front of a real lock screen (SEQUENCE), assess a breach
            in a real incident register (CLASSIFY), and work a ransom note from
            the first move to recovery (BRANCH).

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
                "rare: the <a href=\"https://www.oaic.gov.au/\">OAIC</a> was notified of <strong>1,113 data "
                "breaches across 2024, a record</strong>, and the "
                "<strong>health sector reported the "
                "most</strong> of any. Australia's two landmark cases, both in 2022, "
                "show how it happens:</p>"
                "<ul>"
                "<li><strong>Optus.</strong> "
                "Information on roughly 9.8 million "
                "current and former customers was exposed through an access point to "
                "customer data that was reachable over the internet without a login. "
                "For some people it included identity document numbers like passport "
                "and licence numbers, the raw material for identity theft.</li>"
                "<li><strong>Medibank.</strong> "
                "Attackers got in using a stolen login "
                "that reached the network through a remote-access connection that did "
                "not require a second factor. They took sensitive health data on "
                "about 9.7 million people. Medibank chose not to pay the ransom, and "
                "the attackers published the stolen data. A stark reminder that once "
                "sensitive data is taken there are no good options left, and that "
                "multi-factor authentication on remote access is not optional.</li>"
                "</ul>"
                "<div class=\"cy-source\">Source: Optus and Medibank 2022 data "
                "breaches, as reported to the "
                "<a href=\"https://www.oaic.gov.au/\">OAIC</a>.</div>"
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
                "<div class=\"cy-source\">Source: OAIC Notifiable Data Breaches "
                "Report, January to December 2024.</div>",
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
        "wholesaler and counter shop, run by owner Rick Halloran with office admin "
        "Tanya Pillai, bookkeeper Dolores Fenn and counter and workshop hand Josh "
        "Tran. Name a threat from how it behaves, triage the real counter inbox, "
        "order the ransomware response, assess a breach under the law, and work a "
        "ransom note from the first move to recovery.",
        "tasks": [
            {
                "key": "name-the-threat",
                "kind": "sort",
                "points": 2,
                "title": "Name the threat",
                "body": "<p>Lesson 1 introduced the malware family. Now prove you "
                "can tell them apart by behaviour, which is what matters, because "
                "each is stopped by different defences. Below is Ballarat Auto "
                "Spares' own protection history, six recent detections. Read each "
                "and sort it to the member that fits.</p>"
                "<div class=\"cy-callout\">The tell is in HOW it behaves: does it "
                "spread itself, wait for a click, wear a disguise, hide and watch, "
                "or lock and demand?</div>",
                "payload": {
                    "prompt": "Tap a detection, then tap the malware type it belongs to. Sort all six to finish.",
                    "frame": {
                        "tab": "Windows Security · Protection history", "fav": "W", "favbg": "#0067b8",
                        "url_prefix": "https://", "url": "windowsdefender.microsoft.com", "url_bold": "/history",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "heading": "Protection history",
                    "buckets": [
                        {"id": "virus", "label": "Virus"},
                        {"id": "worm", "label": "Worm"},
                        {"id": "trojan", "label": "Trojan"},
                        {"id": "spyware", "label": "Spyware"},
                        {"id": "ransomware", "label": "Ransomware"},
                    ],
                    "items": [
                        {"text": "Thursday lunchtime, Tanya opens a 'brake pad compatibility chart' a customer emailed her, and only once she opens it does a script start silently renaming files in her Downloads folder.", "bucket": "virus",
                         "why": "That is a virus. It rode inside a normal-looking attachment and only ran because a person opened it. No open, no infection."},
                        {"text": "Overnight, the moment the network printer's firmware update reaches the counter subnet, it copies itself onto every PC connected there with nobody touching a keyboard.", "bucket": "worm",
                         "why": "That is a worm. Spreading itself across machines with no human action is exactly what lets it take out a whole subnet overnight."},
                        {"text": "Rick installs a free 'invoice reminder' tool he found online because it looks handy; it does remind him about invoices, but it also quietly opens a way in for someone outside the shop.", "bucket": "trojan",
                         "why": "That is a trojan. You install it yourself because it looks useful, then it does its real, hidden job."},
                        {"text": "For three weeks something has sat unseen on the trade-account PC, logging every password typed on the supplier login page, until Dolores spots a login from Perth on an account nobody in Ballarat made.", "bucket": "spyware",
                         "why": "That is spyware. It hid and quietly stole information rather than announcing itself, which is exactly why it took three weeks to notice."},
                        {"text": "At 7am Tuesday, every booking and quote in progress is renamed to end .locked, and a countdown demands payment in Monero within 48 hours.", "bucket": "ransomware",
                         "why": "That is ransomware. Locking your files in place and demanding payment to release them is its signature."},
                        {"text": "The moment Josh maps the parts-lookup network drive from the workshop PC, a copy of the same script appears on that PC's own shared folder, with no file ever opened.", "bucket": "worm",
                         "why": "Still a worm. Copying itself onto other machines the instant they connect, with no click needed, is the worm's calling card."},
                    ],
                },
            },
            {
                "key": "triage-counter-inbox",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the parts-counter inbox",
                "body": "<p>The commonest way malware reaches a small business is the "
                "inbox. Here is a mixed morning's mail at the counter. Read the "
                "sender, the subject and the preview, then mark each Genuine or "
                "Phishing.</p>"
                "<div class=\"cy-callout\">The tells to weigh: is it expected, who "
                "is it really from, is it rushing you, and is it pushing an "
                "attachment, a link or an Enable content prompt?</div>",
                "payload": {
                    "prompt": "Mark each message Genuine or Phishing. Sort all five to finish.",
                    "gmail": True,
                    "frame": {
                        "tab": "Inbox · Ballarat Auto Spares", "fav": "M", "favbg": "#ea4335",
                        "url_prefix": "https://", "url": "mail.google.com", "url_bold": "/mail/u/0",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "emails": [
                        {"from": "Tanya Pillai", "addr": "tanya@ballaratautospares.com.au", "time": "6:12 AM", "unread": True,
                         "subject": "Friday stocktake, start 6am",
                         "preview": "Early start Friday for the quarterly stocktake. Coffee's on me. No reply needed.",
                         "phish": False,
                         "why": "An expected note from a colleague on the shop's own domain, asking nothing of you and pushing no link or attachment."},
                        {"from": "Burson Auto Parts", "addr": "accounts@burson-tradehub.net", "time": "6:47 AM", "unread": True,
                         "subject": "Trade account suspended, verify within 12 hours",
                         "preview": "Unusual activity detected. Open Account_Verification.zip and confirm your details to restore access.",
                         "phish": True,
                         "why": "A lookalike domain (burson-tradehub.net, not the real Burson domain), a short deadline and a .zip attachment. Opening it can install malware; call the supplier on a number you already have instead."},
                        {"from": "Toll Group", "addr": "tracking@toll-parcel-au.com", "time": "7:03 AM", "unread": True,
                         "subject": "Your parts delivery needs a customs fee",
                         "preview": "A small customs fee of $2.40 is owed before delivery. Pay through the secure link to release your parcel.",
                         "phish": True,
                         "why": "A lookalike delivery domain and a tiny fee designed to grab card details through a link. Genuine carriers don't ask for a surprise payment by link like this."},
                        {"from": "Rick Halloran", "addr": "rick@ballaratautospares.com.au", "time": "7:20 AM", "unread": False,
                         "subject": "New EFTPOS machine arriving Monday",
                         "preview": "Bank's dropping off the replacement terminal Monday arvo. Just needs someone at the counter to sign for it.",
                         "phish": False,
                         "why": "A plain, expected update from the owner on the shop's real domain, with nothing to click and no pressure."},
                        {"from": "Xero Support", "addr": "billing@xero-account-center.com", "time": "7:41 AM", "unread": True,
                         "subject": "Action required: enable content to view your subscription invoice",
                         "preview": "Open the attached statement and click Enable Content to keep your Xero subscription active.",
                         "phish": True,
                         "why": "The Enable Content trick again, this time impersonating Xero from a lookalike domain. Enabling content can run macros that install malware. Log in to Xero directly instead."},
                    ],
                },
            },
            {
                "key": "order-the-response",
                "kind": "sequence",
                "points": 2,
                "title": "Order the ransomware response",
                "diagram": "ransom-lock-full",
                "body": "<p>First, the sight nobody wants: a ransom-lock screen, "
                "exactly like the one that could appear on any PC in the shop. "
                "Lesson 1 covered how a business beats ransomware. Now put the "
                "response in the right order, the sequence that turns a bad morning "
                "into a contained one.</p>"
                "<div class=\"cy-callout\">Each step depends on the one before it. "
                "Get the order right and nothing has to be undone.</div>",
                "payload": {
                    "prompt": "Tap the steps in the order you would actually do them. Place all five to finish.",
                    "steps": [
                        {"label": "Disconnect the infected machine from the network immediately.", "order": 1,
                         "detail": "Stops it reaching shared drives and other PCs before anything else happens."},
                        {"label": "Report the incident so every machine gets checked, not just the one in front of you.", "order": 2,
                         "detail": "Gets the whole shop looked at properly, instead of guessing under pressure."},
                        {"label": "Confirm which backup is clean and unaffected before touching anything.", "order": 3,
                         "detail": "You need to know your way back exists before you start undoing damage."},
                        {"label": "Wipe the infected machine and restore the files from that clean backup.", "order": 4,
                         "detail": "That is what takes away the attacker's leverage entirely. No payment needed."},
                        {"label": "Review how it got in and close that door so it can't happen again.", "order": 5,
                         "detail": "Restoring the files doesn't fix the opening it used. Find it and close it."},
                    ],
                },
            },
            {
                "key": "assess-the-breach",
                "kind": "classify",
                "points": 2,
                "title": "Assess the breach",
                "body": "<p>Lesson 1 covered the Notifiable Data Breaches scheme: "
                "when a breach is likely to cause serious harm, the law requires an "
                "assessment within 30 days and, if it meets the threshold, telling "
                "the OAIC and the people affected. Here are six real-feeling "
                "moments from around the shop. Sort each to how it should be "
                "handled.</p>"
                "<div class=\"cy-callout\">Ask: is serious harm likely, is it too "
                "soon to tell, or is there really no personal information at "
                "risk?</div>",
                "payload": {
                    "prompt": "Read each situation and tap how it should be handled. Assess all six to finish.",
                    "frame": {
                        "tab": "Incident register · Ballarat Auto Spares", "fav": "I", "favbg": "#8430ce",
                        "url_prefix": "https://", "url": "console.ballaratautospares.com.au", "url_bold": "/incidents",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "categories": [
                        {"id": "notify", "label": "Must notify"},
                        {"id": "assess", "label": "Assess further"},
                        {"id": "not", "label": "Not notifiable"},
                    ],
                    "events": [
                        {"text": "A parts supplier's leaked customer list, including Ballarat Auto Spares' trade-account details and past order history, turns up for sale online.",
                         "category": "notify",
                         "why": "Must notify. Trade-account and order details being exposed and actively for sale is exactly the serious harm the Notifiable Data Breaches scheme exists for. Assess within 30 days and notify the OAIC and affected people if it meets the threshold."},
                        {"text": "Tanya emails a single customer's invoice to the wrong customer by mistake, then recalls it within two minutes before it is opened.",
                         "category": "assess",
                         "why": "Assess further. A quick, contained mistake with no evidence it was read still needs a proper look to confirm no real harm is likely."},
                        {"text": "The eftpos terminal reboots itself mid-transaction and the sale has to be re-run; no card or customer data is affected.",
                         "category": "not",
                         "why": "Not notifiable. Nothing personal was exposed. This is ordinary equipment trouble, not a privacy incident."},
                        {"text": "A staff spreadsheet with everyone's home addresses and pay rates is left visible on a shared drive every counter PC can open, for six months.",
                         "category": "notify",
                         "why": "Must notify. Sensitive personal and financial details exposed to more people than should have had access, for a long period, is likely to cause serious harm."},
                        {"text": "A supplier calls to say their own systems were breached, and the shop's trade-account login with them might be exposed, though no misuse has been seen yet.",
                         "category": "assess",
                         "why": "Assess further. It's the supplier's breach, but your account there may be exposed. Check whether that password is reused elsewhere while it's assessed."},
                        {"text": "A customer's phone number is read aloud by accident over the counter within earshot of the next customer in the queue.",
                         "category": "not",
                         "why": "Not notifiable. A single, minor slip with no realistic path to serious harm, though worth a quiet word with staff."},
                    ],
                },
            },
            {
                "key": "the-ransom-note",
                "kind": "branch",
                "points": 2,
                "title": "The ransom note",
                "hero": "infection-spread",
                "body": "<p>First, watch it happen. The animation above is why your "
                "first move matters so much: on a flat network the infection "
                "reaches every machine, while segmentation seals it into one zone. "
                "Now the real test: what you do in the moment. Draw on everything "
                "Lesson 1 taught about ransomware.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> contain it, "
                "report it, restore from backup, then close the door. Never lead "
                "with the ransom.</div>",
                "payload": {
                    "prompt": "The incident unfolds. Make each call and see how it plays out.",
                    "start": "note",
                    "nodes": {
                        "note": {
                            "text": "6:50am Wednesday, before opening. Rick unlocks the shop and finds the booking-and-eftpos PC frozen behind a red screen: 'Your files are encrypted. Pay $4,150 in Monero within 48 hours.' The shop opens at 7:30 and three trade customers are already waiting outside. What is Rick's first move?",
                            "choices": [
                                {"label": "Unplug the network cable from that PC right now.", "outcome": "good",
                                 "feedback": "Right. Cutting it off the network first stops it reaching the shop's other systems while you work out what's next.", "to": "contain"},
                                {"label": "Try a few things himself to unlock it before opening, the customers can wait.", "outcome": "bad",
                                 "feedback": "Every minute it stays connected is a minute it can keep spreading. The first move is always to get it off the network, not to start troubleshooting.", "to": "fiddle_bad"},
                                {"label": "Pay the $4,150 straight away so the shop can open on time.", "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds crime, and the door it came through is still open. Never lead with the ransom.", "to": "pay_bad"},
                            ],
                        },
                        "fiddle_bad": {
                            "text": "While Rick pokes around, the infection reaches the shared parts-lookup drive. Every minute connected is more damage. The first move is always to disconnect.",
                            "choices": [],
                        },
                        "pay_bad": {
                            "text": "He pays, but the countdown resets and the files stay locked. Paying is unreliable and marks the shop as a soft target. Disconnect first, never lead with the ransom.",
                            "choices": [],
                        },
                        "contain": {
                            "text": "Good, it's off the network. The red screen is still up, and the trade customers are waiting. What next?",
                            "choices": [
                                {"label": "Open with pen, paper and the backup eftpos terminal, and report the incident properly.", "outcome": "good",
                                 "feedback": "Right. The shop can trade on paper for a morning; reporting gets the whole system checked instead of guessed at under pressure.", "to": "report"},
                                {"label": "Quietly try to remove the ransomware himself before telling anyone.", "outcome": "bad",
                                 "feedback": "Cleaning it alone risks destroying evidence and missing another infected machine. Report it so the full picture gets checked.", "to": "clean_bad"},
                                {"label": "Turn the trade customers away and spend the morning on the PC instead.", "outcome": "bad",
                                 "feedback": "Turning customers away isn't necessary. Paper and the backup terminal keep the shop trading while it's dealt with properly.", "to": "clean_bad"},
                            ],
                        },
                        "clean_bad": {
                            "text": "Cleaning it alone, or closing the shop instead of reporting it, wastes the morning and still leaves the real problem unchecked. Report it, keep trading on paper, and let the full picture get looked at.",
                            "choices": [],
                        },
                        "report": {
                            "text": "Reported. IT confirms last night's backup is clean and untouched. How does Rick get back to normal?",
                            "choices": [
                                {"label": "Wipe the machine, restore from the clean backup, then review how it got in.", "outcome": "good",
                                 "feedback": "That is the whole point of a backup: it takes away the attacker's leverage entirely, and reviewing the entry point stops a repeat.", "to": "win"},
                                {"label": "Pay anyway, to save the hassle of restoring.", "outcome": "bad",
                                 "feedback": "With a clean backup in hand, paying makes no sense at all. Restore, do not pay.", "to": "reconnect_bad"},
                                {"label": "Reconnect the infected machine to see if the files have come back on their own.", "outcome": "bad",
                                 "feedback": "Reconnecting an infected machine risks spreading it again. Keep it isolated, wipe it, and restore from the clean backup.", "to": "reconnect_bad"},
                            ],
                        },
                        "reconnect_bad": {
                            "text": "Reconnecting an infected machine, or paying with a clean backup in hand, undoes your good work. Keep it isolated, wipe it, and restore from the clean backup instead.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Contained, reported, restored from backup, and the entry point reviewed, with nothing paid. That is exactly how a business beats ransomware: the backup, not the wallet, is what saves you.",
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
