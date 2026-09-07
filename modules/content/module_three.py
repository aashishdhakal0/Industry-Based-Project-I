"""Module 3, Phishing & Social Engineering: understand it, then apply it.

  Lesson 1  UNDERSTAND IT  — a teaching lesson. Four reading panels, each with a
            real visual: what social engineering is and the human levers it pulls;
            the phishing family (mass phishing, spear phishing, whaling) and the
            four red flags that read any message; the attacks that leave the inbox
            (smishing, vishing, and AI voice clones); and business email
            compromise, the quiet, costly one. One light comprehension check on
            caller ID spoofing.
  Lesson 2  APPLY IT       — a practical lesson. Five hands-on tasks: name the
            channel, triage a mixed inbox, read a vishing scene, work a live
            AI voice-clone call, and spot the scam of two lookalike messages.

Voice: warm, plain Australian English, no em-dashes, no emoji. Grounded in ACSC
(cyber.gov.au) phishing and scam guidance and Scamwatch reporting on business
email compromise and voice-cloning. Points sum to 10 per lesson and bank at
lesson end.
"""

LESSONS = [
    {
        "title": "Know the con: how they hack the human",
        "reading_time_minutes": 9,
        "intro": "Social engineering does not attack your computer, it attacks "
        "you. Learn the levers it pulls, the shapes phishing takes, the channels "
        "beyond your inbox, and the one move that beats all of them. By the end you "
        "will read any message the way a security analyst does.",
        "tasks": [
            {
                "key": "the-con",
                "kind": "concept",
                "points": 2,
                "title": "The con: they hack the human, not the machine",
                "diagram": "se-levers",
                "body": "<p><strong>Social engineering</strong> is the art of "
                "manipulating a person into helping the attacker: clicking a link, "
                "opening a file, moving money, or handing over a password. No "
                "firewall stops it, because it does not target the machine, it "
                "targets you. This is not a fringe problem. The OAIC reports that "
                "<strong>phishing is the leading cause</strong> of the cyber "
                "incidents behind Australia's data breaches, and that "
                "<strong>social engineering and impersonation are rising</strong> "
                "sharply.</p>"
                "<p>It works because it borrows a real psychological shortcut: under "
                "pressure, people stop analysing and fall back on habit and "
                "instinct. Attackers pull five human levers to create that pressure:</p>"
                "<ul>"
                "<li><strong>Authority</strong>: it claims to be the boss, the bank, "
                "or the tax office, because we are trained to comply with people in "
                "charge.</li>"
                "<li><strong>Urgency</strong>: a countdown or a deadline, to stop "
                "you pausing to think or check.</li>"
                "<li><strong>Fear</strong>: a threat, like your account will be "
                "closed or you will be fined, to push you into acting.</li>"
                "<li><strong>Curiosity</strong>: a tempting subject line or a "
                "mystery attachment you just want to open.</li>"
                "<li><strong>Greed</strong>: a prize, a refund, or a too-good offer "
                "that clouds your judgement.</li>"
                "</ul>"
                "<div class=\"cy-callout\">Whenever a message reaches for one of "
                "these levers, that is your cue to slow down. The pressure is the "
                "point: it is engineered to stop you checking.</div>",
            },
            {
                "key": "phishing-family",
                "kind": "concept",
                "points": 2,
                "title": "The phishing family, and how a phish actually works",
                "diagram": "phishing-email",
                "body": "<p><strong>Phishing</strong> is social engineering by "
                "message, and it comes in three sizes. Ordinary "
                "<strong>phishing</strong> is a wide net: one generic message sent "
                "to thousands, hoping a few bite. <strong>Spear phishing</strong> is "
                "aimed at one person and personalised with real details (your name, "
                "your role, a live project), which makes it far harder to doubt. "
                "<strong>Whaling</strong> targets the big fish, a senior leader, or "
                "impersonates one.</p>"
                "<p>Whatever the size, a phish is a <strong>chain</strong>: an email "
                "arrives looking legitimate, you click, a fake login page copies your "
                "password as you type it, and the attacker signs in as you. The good "
                "news is that breaking <em>any</em> link stops the whole thing, and "
                "you do not need to spot which size it is. You need a checklist.</p>"
                "<p>A lookalike supplier invoice, say, trips the four wires that "
                "catch almost every phish:</p>"
                "<ul>"
                "<li><strong>Fake sender</strong>: the friendly name is easy to set "
                "to anything, but the real address after the @ is what matters. Here "
                "it is a lookalike domain (flour-supplier-au.info), not the genuine "
                "one. Always read the part after the @.</li>"
                "<li><strong>Dodgy link</strong>: the visible text says one thing, "
                "but the address it actually points to goes somewhere else. On a "
                "computer you can hover to see the real destination before you "
                "click.</li>"
                "<li><strong>Pressure or secrecy</strong>: act now, or keep this "
                "between us, both there to bypass your normal checks and your "
                "colleagues.</li>"
                "<li><strong>Unexpected attachment</strong>: a surprise file, "
                "especially a .zip or an invoice you were not expecting.</li>"
                "</ul>"
                "<div class=\"cy-callout\">One red flag is enough to slow down. Two "
                "or more, treat it as an attack until you have verified it a "
                "different way.</div>",
            },
            {
                "key": "beyond-the-inbox",
                "kind": "concept",
                "points": 2,
                "title": "Beyond the inbox: text, voice, and cloned voices",
                "diagram": "sms-phish",
                "body": "<p>The same con does not stay in email. It follows you onto "
                "the devices you trust most, and the phone in your pocket is the "
                "softest target of all.</p>"
                "<ul>"
                "<li><strong>Smishing</strong> is phishing by text message, like the "
                "parcel-fee text. It works because a phone is built for speed, not "
                "scrutiny: links are shortened and hard to inspect, you are usually "
                "distracted, and a text feels more personal than an email. A tiny "
                "fee and a tight deadline do the rest.</li>"
                "<li><strong>Vishing</strong> is the con by phone call: a live voice "
                "using authority and fear to rush you, a fake ATO officer threatening "
                "arrest, a fake bank fraud team, a fake help desk. A real person on "
                "the line is far more persuasive than any email.</li>"
                "<li><strong>AI voice cloning</strong> is the frightening new twist. "
                "From only a few seconds of someone speaking, in a podcast, a video, "
                "or even a voicemail greeting, an attacker can now generate a voice "
                "that sounds convincingly like them, then call and ask you to move "
                "money. What used to be proof of identity, a familiar voice, no "
                "longer is.</li>"
                "</ul>"
                "<p>That leaves two things you can no longer trust. A "
                "<strong>caller ID</strong> can be <em>spoofed</em>: the number that "
                "shows on your screen is just data the caller sends, so a scammer can "
                "make it read your bank's real name. And a <strong>familiar "
                "voice</strong> can be cloned. Neither, on its own, is proof of who "
                "is really calling.</p>"
                "<div class=\"cy-callout\">The defence is the same on every channel: "
                "do not act on the message in front of you. Hang up, and call back on "
                "a number you already have, from the back of your card or your own "
                "contacts.</div>",
            },
            {
                "key": "bec",
                "kind": "concept",
                "points": 2,
                "title": "Business email compromise: the quiet, costly one",
                "diagram": "exec-email",
                "body": "<p><strong>Business email compromise</strong> (BEC) is "
                "among the costliest scams for Australian organisations, and the ASD "
                "names it a key way cybercrime is committed. Yet it rarely looks "
                "dramatic. There is no malware and no obvious threat. It looks like a "
                "routine email, from a leader or a supplier you know, quietly asking "
                "you to do one reasonable-sounding thing with money.</p>"
                "<p>Here is how the money actually moves. The attacker either "
                "<em>spoofs</em> a trusted sender (a lookalike address), or genuinely "
                "<em>takes over</em> a real mailbox by stealing its password, then "
                "watches the real email flow and steps in at the right moment to "
                "redirect a payment that was always going to happen. The classic "
                "shape is this: an email appears to be from the CEO, marked urgent "
                "and confidential, asking for an unusual payment that skips the "
                "normal checks. Two everyday versions:</p>"
                "<ul>"
                "<li><strong>CEO fraud</strong>: a message from the boss demanding a "
                "fast, secret transfer, leaning hard on authority and urgency, and "
                "usually claiming to be uncontactable so you cannot check.</li>"
                "<li><strong>Invoice or bank-change fraud</strong>: a supplier you "
                "know emails that their bank account has changed, so please pay the "
                "next real invoice to a new account. Because the invoice itself is "
                "genuine, nothing looks wrong until the money is gone.</li>"
                "</ul>"
                "<p>The one habit that defeats all of it: verify any new or changed "
                "payment on a channel you already trust, a phone call to a number you "
                "already have (not the one in the email), before a cent moves. The "
                "attacker cannot answer that call.</p>"
                "<div class=\"cy-callout\">Someone important, in a hurry, asking for "
                "money or secrecy, from an address that is not quite right. That is "
                "the signature of business email compromise.</div>",
            },
            {
                "key": "caller-id-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check: does the caller ID prove it?",
                "diagram": "caller-id",
                "body": "<p>One quick check to finish. Your phone rings and the "
                "screen shows the name and number of your CEO, Sarah, exactly as "
                "they are saved in your contacts. The voice on the line sounds like "
                "her too, and she needs a payment made right now. You just learned "
                "the two things you can no longer trust.</p>"
                "<div class=\"cy-callout\">A caller ID can be spoofed, and a voice "
                "can be cloned. Neither is proof of who is really calling.</div>",
                "question": "The caller ID shows your CEO's real name and number, and the voice sounds like her. What does that prove about who is calling?",
                "hint": "Can the number that appears, and the voice, both be faked?",
                "options": [
                    ("Very little: caller ID can be spoofed and a voice can be cloned, so verify on a number you already have before acting", True,
                     "Right. Both the number on screen and the voice can be faked. The only reliable move is to hang up and call back on a number you already trust."),
                    ("It proves the call is genuinely from your CEO", False,
                     "No. Caller ID can be spoofed to show any name or number, and a voice can be cloned. A matching display is not proof."),
                    ("It proves your phone has been hacked", False,
                     "No. A spoofed caller ID does not mean your phone is compromised. The display was simply faked from the other end."),
                    ("It proves the call is safe to act on", False,
                     "No. Because both the ID and the voice can be faked, you should still verify by calling back on a trusted number."),
                ],
            },
        ],
    },
    {
        "title": "Read it like an analyst: spot, verify, report",
        "reading_time_minutes": 9,
        "intro": "Now put the checklist to work at Brunswick Family Dental, a busy "
        "three-chair practice on Sydney Road. Practice manager Anita Rossi, "
        "receptionist Jaydn and principal dentist Dr Lam run the day between "
        "patients. Name the channel each con rides in on, triage the morning inbox, "
        "read a live vishing scene, hold your nerve through an AI voice-clone call, "
        "and pick the scam out of two lookalike messages.",
        "tasks": [
            {
                "key": "channels",
                "kind": "classify",
                "points": 2,
                "title": "Name the channel",
                "body": "<p>Naming the channel is the first step to seeing through "
                "the con. Read each message and tap the channel it uses: "
                "<strong>email phishing</strong>, <strong>smishing</strong> by text, "
                "<strong>vishing</strong> by voice, or <strong>business email "
                "compromise</strong> that redirects a real payment.</p>"
                "<div class=\"cy-callout\">The channel changes, the con does not: "
                "authority, urgency and a request that skips your normal checks.</div>",
                "payload": {
                    "prompt": "Read each message and tap the channel it uses. Sort all six to finish.",
                    "categories": [
                        {"id": "email", "label": "Email phishing"},
                        {"id": "sms", "label": "Smishing (SMS)"},
                        {"id": "voice", "label": "Vishing (voice)"},
                        {"id": "bec", "label": "Business email compromise"},
                    ],
                    "events": [
                        {"text": "A mass email pretending to be from a big bank, sent to thousands, with a link to 'verify your login'.",
                         "category": "email",
                         "why": "Email phishing: one generic message thrown wide to a huge list, hoping a few people click."},
                        {"text": "A text message about a missed parcel, with a small fee and a link to a lookalike delivery site.",
                         "category": "sms",
                         "why": "Smishing: the same con delivered by SMS, betting you will tap the link on a small screen."},
                        {"text": "A phone call from someone claiming to be the ATO, demanding an immediate payment or you will be arrested.",
                         "category": "voice",
                         "why": "Vishing: a live phone call using fear and authority to rush you. The ATO does not work this way."},
                        {"text": "A call where the voice sounds exactly like your manager, asking you to transfer money urgently.",
                         "category": "voice",
                         "why": "Vishing with AI voice cloning: a familiar voice can now be faked from public recordings. Verify on a known number."},
                        {"text": "An email from your 'CEO', from a lookalike address, asking for a confidential urgent payment.",
                         "category": "bec",
                         "why": "Business email compromise: impersonating a leader to push through an unusual payment quietly."},
                        {"text": "An email from 'Henry Schein accounts' says their bank details have changed, please pay this month's $6,200 invoice to the new account.",
                         "category": "bec",
                         "why": "Business email compromise: a spoofed or hacked supplier redirecting a real invoice payment to a stranger. Confirm any account change on a number you already have."},
                    ],
                },
            },
            {
                "key": "inbox-triage",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the morning inbox",
                "body": "<p>The everyday skill: an inbox with a mix of genuine mail "
                "and phishing. Read the sender, the subject and the preview, run the "
                "four red flags, then mark each one. The verdict and the tell are "
                "revealed as you go.</p>"
                "<div class=\"cy-callout\">Weigh the same things each time: did you "
                "expect it, who is it really from, is it rushing you, and is it "
                "pushing a link or an attachment?</div>",
                "payload": {
                    "prompt": "Mark each message Genuine or Phishing. Sort all five to finish.",
                    "emails": [
                        {"from": "Dr Lam <drlam@brunswickfamilydental.com.au>",
                         "subject": "Can you reschedule Mr Osman to Thursday?",
                         "preview": "Running behind on the crown fit. Move his 2pm to Thursday if he's happy. Thanks Jaydn.",
                         "phish": False,
                         "why": "Expected, from the principal on the practice's own domain, about a real patient, pushing no link or attachment."},
                        {"from": "IT Security <security@dental-verify.net>",
                         "subject": "Your password expires in 2 hours, act now",
                         "preview": "Confirm your current password here to avoid being locked out of the patient system.",
                         "phish": True,
                         "why": "A lookalike domain and a rushed link asking you to confirm a password. Real IT never asks for that."},
                        {"from": "Anita Rossi <anita@brunswickfamilydental.com.au>",
                         "subject": "Staff roster for the long weekend",
                         "preview": "Roster's on the noticeboard and in the shared drive. Let me know if the Saturday shift doesn't suit.",
                         "phish": False,
                         "why": "A normal, expected note from your practice manager on the practice domain, with no link, attachment or pressure."},
                        {"from": "DocuSign <no-reply@docusign-portal-au.com>",
                         "subject": "You have a document to sign, opens in 24 hours",
                         "preview": "Review and sign the attached supplier contract before it expires.",
                         "phish": True,
                         "why": "A lookalike DocuSign domain with a manufactured deadline. Reach signing services the way you normally do, never through the link."},
                        {"from": "Henry Schein <orders@henryschein.com.au>",
                         "subject": "Your March order has shipped",
                         "preview": "Your dental consumables order is on the way, tracking in your account. No action needed.",
                         "phish": False,
                         "why": "A genuine order update from a supplier you actually use, on their real domain, asking nothing risky and pushing no login link."},
                    ],
                },
            },
            {
                "key": "read-vishing-scene",
                "kind": "check",
                "points": 2,
                "title": "Read the vishing scene",
                "diagram": "scene-vish",
                "body": "<p>A picture-question, straight from Lesson 1. Jaydn on the "
                "front desk is on the phone to a caller who sounds exactly like Dr "
                "Lam, the principal, urgently demanding a $48,500 transfer to a new "
                "lab, and to keep it quiet. Read the scene the way an analyst would, "
                "then answer.</p>"
                "<div class=\"cy-callout\">A familiar voice and a matching caller ID "
                "are no longer proof. Secrecy is there to stop you checking.</div>",
                "question": "Looking at the scene, what should Jaydn do right now?",
                "hint": "A voice can be cloned, and 'keep it quiet' is there to stop them verifying.",
                "options": [
                    ("Do not act on the call: hang up and ring Dr Lam back on a number the practice already has", True,
                     "Right. Verifying on a number you already trust is the one move a cloned voice cannot beat. Do not let the pressure or the secrecy rush you."),
                    ("Make the transfer, since the voice clearly sounds like Dr Lam", False,
                     "No. A familiar voice can now be cloned from public recordings. Never move money on a voice alone."),
                    ("Ask the caller a personal question to prove it is really Dr Lam", False,
                     "No. A well-prepared attacker may know the answer, and a clone can respond smoothly. Hang up and call back instead."),
                    ("Reply in the practice chat to confirm the new account", False,
                     "No. That does not verify the caller. Confirm a money request on a phone number you already trust."),
                ],
            },
            {
                "key": "ceo-call",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: the CEO calls",
                "hero": "phish-unfold",
                "body": "<p>First, the anatomy. The animation above walks the phishing "
                "chain end to end: an email arrives, you click, your password is "
                "captured on a fake page, and the attacker signs in as you. Breaking "
                "any one link stops it. Now a live version of that con, by phone.</p>"
                "<p>The real test is what you do in the moment. A caller who "
                "sounds exactly like the CEO is urgently demanding a transfer. Work "
                "through the drill: make each call and see the consequence before the "
                "next decision.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> a familiar "
                "voice and a matching caller ID are no longer proof. Verify any "
                "urgent money request on a number you already have.</div>",
                "payload": {
                    "prompt": "The call comes in. Make each call and see the consequence.",
                    "start": "call",
                    "nodes": {
                        "call": {
                            "text": "The front desk phone rings: the caller ID shows Dr Lam, the principal, and the voice sounds exactly like her. She says she is stuck between patients and needs Jaydn to transfer $48,500 to a new dental lab before 4pm today, and to keep it quiet for now. What do you do?",
                            "choices": [
                                {"label": "Say you will handle it, hang up, and call her back on the number the practice already has", "outcome": "good",
                                 "feedback": "Right. Verifying on a number you already trust is the one move a voice clone cannot beat.", "to": "verify"},
                                {"label": "Make the transfer, it is clearly her voice and she is the principal", "outcome": "bad",
                                 "feedback": "That is exactly what the scam needs. A familiar voice can be cloned, and the secrecy is there to stop you checking.", "to": "paid_bad"},
                                {"label": "Ask her a personal question to prove it is really her", "outcome": "risky",
                                 "feedback": "Risky. A well-prepared attacker may know the answer, and a clone can respond smoothly. Hang up and call back instead.", "to": "verify"},
                            ],
                        },
                        "paid_bad": {
                            "text": "The money lands in a criminal's account and is gone within minutes. The voice was an AI clone built from a recording of Dr Lam. A callback to her real number would have stopped it cold.",
                            "choices": [],
                        },
                        "verify": {
                            "text": "Jaydn calls Dr Lam's real mobile. She is bewildered: she made no such call, and knows nothing about any lab. The voice was a clone. What now?",
                            "choices": [
                                {"label": "Tell Anita and the rest of the front desk straight away so everyone is warned, and confirm no payment went out", "outcome": "good",
                                 "feedback": "Exactly. Warning the team turns your near miss into everyone's defence against the next call.", "to": "win"},
                                {"label": "Say nothing, since no money was actually lost", "outcome": "bad",
                                 "feedback": "Staying quiet leaves colleagues exposed to the same call. Report it so the whole team is ready.", "to": "quiet_bad"},
                            ],
                        },
                        "quiet_bad": {
                            "text": "The following week the same clone calls the other receptionist, who has heard nothing about it, and a payment goes out. A quick warning would have prevented it.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Nothing paid, everyone warned. You beat a convincing AI-cloned voice with one old-fashioned habit: hang up, and call back on a number you already trust.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "spot-the-scam",
                "kind": "spot",
                "points": 2,
                "title": "Spot the scam",
                "body": "<p>Two messages, side by side. One is genuine, one is a "
                "scam. Put your checklist to work: check the sender, and whether it "
                "is pushing you to act through a link. Tap the one that is the "
                "attack.</p>"
                "<div class=\"cy-callout\">When two messages look similar, the "
                "sender address and the call to 'verify' or 'log in' through a link "
                "are usually what separate the real from the fake.</div>",
                "payload": {
                    "prompt": "One of these is a phishing message. Tap the scam.",
                    "fake": "right",
                    "why": "The right-hand one is from a lookalike domain (dental-verify.net) and pushes you to confirm your password through a link, which real IT never does. The left-hand one is from the practice's real domain and asks nothing of you.",
                    "left": {
                        "sender": "IT Service Desk <helpdesk@brunswickfamilydental.com.au>",
                        "text": "Scheduled maintenance this Saturday 7am to 8am. Email may be briefly unavailable. No action needed from you.",
                    },
                    "right": {
                        "sender": "IT Security <security@dental-verify.net>",
                        "text": "Your password expires today. Confirm your current password here within 2 hours to avoid being locked out of the patient system.",
                    },
                },
            },
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: understand it (the con and its shapes) ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is social engineering?",
            "options": [
                ("Manipulating a person into doing something that helps the attacker", True,
                 "Yes. Social engineering hacks the human, not the machine, by exploiting trust, habit and pressure."),
                ("A method for designing safer software", False,
                 "No. It is an attack on people, not a software design method."),
                ("A setting that hardens your social media account", False,
                 "No. It is the attacker's technique, not a privacy setting."),
                ("A type of firewall", False,
                 "No. It is a human-focused trick, not a piece of defensive technology."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "An email that looks like it is from your CEO and says 'do this in the next 10 minutes' is mainly pulling which two levers?",
            "options": [
                ("Authority and urgency", True,
                 "Yes. It borrows the weight of a senior figure and adds a tight deadline so you act before you think."),
                ("Curiosity and greed", False,
                 "No. Those are other levers. A rushed order from the boss leans on authority and urgency."),
                ("Fear and sympathy", False,
                 "No. The pressure here comes from who it claims to be and the deadline: authority and urgency."),
                ("Habit and boredom", False,
                 "No. The two levers being pulled are authority (the CEO) and urgency (10 minutes)."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What makes spear phishing more dangerous than ordinary mass phishing?",
            "options": [
                ("It is personalised with real details about you, so it slips past your guard", True,
                 "Yes. Using your name, role or a real project makes the message feel legitimate and much harder to doubt."),
                ("It is sent to far more people at once", False,
                 "No. Spear phishing is narrow and targeted, not mass-sent. Its danger is the personalisation."),
                ("It never contains a link or attachment", False,
                 "No. It often does. What sets it apart is the real personal detail that makes it convincing."),
                ("It can only be opened on a phone", False,
                 "No. The device is not the point. Spear phishing is dangerous because it is tailored to you."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is business email compromise?",
            "options": [
                ("A scam that impersonates a leader or supplier by email to redirect a real payment or push an unusual one", True,
                 "Yes. There is no malware, just a convincing email quietly steering money to the attacker's account."),
                ("A virus that spreads through a company's email server", False,
                 "No. Business email compromise is a social-engineering scam about money, not a piece of malware."),
                ("A rule that blocks spam before it reaches the inbox", False,
                 "No. That is a defence. Business email compromise is the attack it tries to catch."),
                ("A way to back up company email safely", False,
                 "No. It is an attack that abuses trusted email relationships, not a backup method."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A call shows your bank's real name and phone number on your screen. What does that prove?",
            "options": [
                ("Very little, because caller ID can be spoofed to show any name or number", True,
                 "Yes. Attackers can fake the number that appears, so a familiar caller ID is not proof of who is calling."),
                ("That the call is definitely from your bank", False,
                 "No. Caller ID can be faked. A matching number proves almost nothing."),
                ("That your phone has been hacked", False,
                 "No. A spoofed caller ID does not mean your phone is compromised; the display was simply faked."),
                ("That the call is safe to act on", False,
                 "No. Because caller ID can be spoofed, you should still hang up and call back on a trusted number."),
            ],
        },
        # ---- Lesson 2: apply it (spot, verify, report) ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You get an unexpected text about a held parcel, with a link to pay a small release fee. What is the best move?",
            "options": [
                ("Do not tap the link; check with the carrier through their real app or website yourself", True,
                 "Yes. An unexpected parcel text with a fee and a link is classic smishing. Reach the carrier the way you normally would."),
                ("Tap the link and pay the small fee to release the parcel", False,
                 "No. That link is the trap. Never pay through a link in an unexpected text."),
                ("Reply STOP to the text", False,
                 "No. Replying can confirm your number is live. Just check with the carrier directly."),
                ("Forward the text to friends to warn them", False,
                 "No. Do not spread the link. Check the parcel yourself through the carrier's real app or website."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is the single most reliable thing to check on any suspicious email?",
            "options": [
                ("The sender's real address, especially the domain after the @", True,
                 "Yes. The friendly name is easy to fake, but the real domain after the @ often gives a scam away."),
                ("Whether the email has a company logo", False,
                 "No. Logos are trivial to copy. The real sender address is the reliable tell."),
                ("How polite the wording is", False,
                 "No. Scam emails can be perfectly polite. Check the real sender address instead."),
                ("The colour scheme of the email", False,
                 "No. Appearance is easy to fake. The domain after the @ is what to check."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A caller sounds exactly like your manager and urgently asks you to transfer money to a new account. What is the safest action?",
            "options": [
                ("Hang up and call your manager back on a number you already have before moving any money", True,
                 "Yes. A voice can be cloned, so verifying on a trusted number is the one move the scam cannot survive."),
                ("Make the transfer, since the voice clearly sounds like them", False,
                 "No. A familiar voice can now be cloned. Never move money on a voice alone."),
                ("Ask the caller a personal question to confirm their identity", False,
                 "No. A prepared attacker may know the answer, and a clone can respond smoothly. Call back on a trusted number."),
                ("Confirm the account by replying to the caller's text", False,
                 "No. That does not verify the caller. Use a phone number you already trust."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You spot and correctly identify a phishing email at work. What is the best thing to do with it?",
            "options": [
                ("Report it, using the report button or by telling IT, so others can be protected", True,
                 "Yes. Reporting warns the people who can block it and alert colleagues who got the same message."),
                ("Just delete it and move on", False,
                 "No. Deleting protects only you. Reporting lets IT protect everyone else too."),
                ("Reply to tell the sender you are onto them", False,
                 "No. Replying confirms your address is active and engages the attacker. Report it instead."),
                ("Forward it to the whole team as a warning", False,
                 "No. That spreads the dangerous link. Report it through the proper channel."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "A supplier you know emails that their bank account has changed, so please pay this month's real invoice to the new account. What should you do first?",
            "options": [
                ("Ring the supplier on a number you already have and confirm the change before paying anything", True,
                 "Yes. A changed bank account is always worth a call to a trusted number. That one check defeats this scam."),
                ("Update the details and pay, so the invoice is not late", False,
                 "No. That can send the money to a criminal. A changed account deserves a phone call first."),
                ("Reply to the email to ask if the new account is genuine", False,
                 "No. If the email is compromised, you are asking the attacker, who will happily confirm. Verify a different way."),
                ("Pay a small test amount first to see if it goes through", False,
                 "No. Any payment to an unverified account is a loss. Confirm the change by phone before paying at all."),
            ],
        },
    ],
}
