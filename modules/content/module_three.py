"""Module 3, Phishing & Social Engineering: understand it, then apply it.

  Lesson 1  UNDERSTAND IT, a teaching lesson. Four reading panels, each with a
            real visual: what social engineering is and the human levers it pulls;
            the phishing family (mass phishing, spear phishing, whaling) and the
            four red flags that read any message; the attacks that leave the inbox
            (smishing, vishing, and AI voice clones); and business email
            compromise, the quiet, costly one. One light comprehension check on
            caller ID spoofing.
  Lesson 2  APPLY IT, hands-on and almost entirely phone-framed, distinct from
            Modules 1 and 2's desktop consoles: name the lever a lock-screen
            notification is pulling (CLASSIFY), tell two SMS threads apart
            (SPOT), hunt for forged lines in a raw email header (NETMAP), hold
            your nerve through a live cloned-voice call with a scrolling
            transcript (BRANCH), and triage a voicemail inbox (MAILSORT).

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
                "targets you. This is not a fringe problem. The "
                "<a href=\"https://www.oaic.gov.au/\">OAIC</a> reports that "
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
                "among the costliest scams for Australian organisations, and the "
                "<a href=\"https://www.cyber.gov.au/\">ASD</a> names it a key way cybercrime is "
                "committed. Yet it rarely looks "
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
                "key": "read-the-sender",
                "kind": "check",
                "points": 2,
                "title": "Quick check: read the real sender",
                "diagram": "phish-headers",
                "body": "<p>One quick check to finish, using the four red flags you "
                "just read. The email above landed in the office inbox. It looks like "
                "a Microsoft security notice and it is pushing you to act. The name "
                "at the top reads 'Microsoft 365 Security'. Now look past the display "
                "name at the real sender address, and the request, then answer.</p>"
                "<div class=\"cy-callout\">The friendly name on an email is free to "
                "type. The real address, after the @, and what it asks you to do are "
                "what give a phish away.</div>",
                "question": "The email shows the name 'Microsoft 365 Security'. What is the strongest sign it is phishing?",
                "hint": "Read the actual address after the @, and compare it to a real Microsoft domain.",
                "options": [
                    ("The real sender address is a lookalike, security@m365-account-verify.co, not a Microsoft domain, and it rushes you to a link to 'keep your mailbox'", True,
                     "Right. The display name 'Microsoft 365 Security' is free to type, but the real address after the @ is a lookalike domain, not microsoft.com. That plus the urgency and the login link is a classic phish. Reach the service the way you normally do, never through the link."),
                    ("It mentions Microsoft, which real emails never do", False,
                     "No. Genuine Microsoft emails do mention Microsoft. The tell is that the real sender address is a lookalike domain, and it is rushing you to a link."),
                    ("It contains a link, which always means phishing", False,
                     "Not on its own; plenty of genuine emails contain links. Here the giveaway is the lookalike sender address combined with the urgent 'verify or lose access' push."),
                    ("It was sent to the whole office, not one person", False,
                     "Being sent widely is not the strongest tell. The real sign is the lookalike sender address and the urgent link to sign in."),
                ],
            },
        ],
    },
    {
        "title": "Read it like an analyst: spot, verify, report",
        "reading_time_minutes": 9,
        "intro": "Now put the checklist to work at Sunbury Plumbing & Gas, a busy "
        "family trades business north of Melbourne. Owner Wayne Castellano is out on "
        "jobs, office manager Bianca Okafor runs the phones and the invoices, "
        "bookkeeper Rhonda Steel handles the books, and apprentice Liam Dorsett is "
        "on the tools. Name the lever a message is pulling, tell two texts apart, "
        "hunt for a forged header, hold your nerve through a live cloned-voice call, "
        "and triage a voicemail inbox.",
        "tasks": [
            {
                "key": "name-the-lever",
                "kind": "classify",
                "points": 2,
                "title": "Which lever is it pulling?",
                "body": "<p>Lesson 1 named the five human levers: authority, "
                "urgency, fear, curiosity, greed. Below is a real lock screen with "
                "the kind of notification stack that lands on a busy tradie's phone "
                "in a single morning. Read each one and tap the lever it is "
                "pulling.</p>"
                "<div class=\"cy-callout\">Ignore what channel it arrived on for "
                "this one. Ask only: what feeling is it trying to create in you "
                "right now?</div>",
                "payload": {
                    "prompt": "Tap a notification, then tap the lever it is pulling. Name all five to finish.",
                    "phone": True,
                    "time": "7:52",
                    "date": "Tuesday, 12 February",
                    "categories": [
                        {"id": "authority", "label": "Authority"},
                        {"id": "urgency", "label": "Urgency"},
                        {"id": "fear", "label": "Fear"},
                        {"id": "curiosity", "label": "Curiosity"},
                        {"id": "greed", "label": "Greed"},
                    ],
                    "events": [
                        {"app": "Phone", "iconBg": "#34c759", "from": "Voicemail: Unknown",
                         "time": "7:41 am", "preview": "\"This is Constable Reeves. You're required to call this number back immediately regarding an outstanding warrant.\"",
                         "category": "authority",
                         "why": "Authority. It borrows the weight of the police to make you comply without question. Real police do not chase debts or warrants by voicemail."},
                        {"app": "Messages", "iconBg": "#30d158", "from": "Auspost",
                         "time": "7:44 am", "preview": "Your parcel redelivery fee of $2.20 must be paid within 3 hours or it will be returned to sender.",
                         "category": "urgency",
                         "why": "Urgency. The tight three-hour window is there to stop you pausing to check whether the fee is even real."},
                        {"app": "Mail", "iconBg": "#0a84ff", "from": "ABN Compliance",
                         "time": "7:46 am", "preview": "Final notice: your business ABN will be suspended today unless you verify your details now.",
                         "category": "fear",
                         "why": "Fear. The threat of losing your ABN is designed to make you act before you think it through."},
                        {"app": "Messages", "iconBg": "#30d158", "from": "+61 400 118 762",
                         "time": "7:49 am", "preview": "Wayne, is this you in this video from Saturday night? Thought you'd want to see before it's taken down: bit.ly/3xk9Lm",
                         "category": "curiosity",
                         "why": "Curiosity. A mysterious, slightly alarming link about yourself is almost impossible not to want to click."},
                        {"app": "Mail", "iconBg": "#0a84ff", "from": "Bunnings Trade",
                         "time": "7:51 am", "preview": "Congratulations, Sunbury Plumbing & Gas has been selected for a $500 trade account bonus. Claim before midnight.",
                         "category": "greed",
                         "why": "Greed. A surprise reward with a deadline is built to cloud your judgement before you ask why a supplier is suddenly this generous."},
                    ],
                },
            },
            {
                "key": "two-texts",
                "kind": "spot",
                "points": 2,
                "title": "Two texts, one is the trap",
                "body": "<p>Two SMS threads, side by side. Both are about the "
                "same thing, a toll bill. One is the real monthly notice, one is "
                "smishing. Use the checklist: who it is really from, and whether "
                "it pushes a link.</p>"
                "<div class=\"cy-callout\">A saved contact name versus a bare "
                "number, and a link versus no link, are usually what separate the "
                "two.</div>",
                "payload": {
                    "prompt": "One of these texts is the scam. Tap it.",
                    "variant": "sms",
                    "fake": "right",
                    "why": "The right-hand text comes from an unknown number, not the saved Linkt contact, uses a lookalike domain (linkt-toll-payau.info, not linkt.com.au), and threatens legal action to rush you into paying through the link. The left-hand text is the real monthly notice: from the saved contact, no link, no threat.",
                    "left": {"contact": "Linkt", "time": "8:03 am",
                             "bubbles": ["Your monthly statement is ready. View it in the Linkt app. No action needed."]},
                    "right": {"number": "+61 400 823 156", "time": "8:07 am", "link": "linkt-toll-payau.info/pay",
                              "bubbles": ["Your Linkt account has unpaid tolls of $34.50. Pay now to avoid legal action: linkt-toll-payau.info/pay"]},
                },
            },
            {
                "key": "forged-headers",
                "kind": "netmap",
                "points": 2,
                "title": "Find the forged header lines",
                "body": "<p>Lesson 1 taught you to read past the display name to "
                "the real sender address. Here is the deeper version: the raw "
                "headers behind an invoice email, the ones your inbox normally "
                "hides. Three of the six lines below have been forged. Tap each "
                "one you find.</p>"
                "<div class=\"cy-callout\">The name at the top can look perfect. "
                "Reply-To, Return-Path and Received are where a forwarded reply, "
                "or the message itself, actually goes.</div>",
                "payload": {
                    "prompt": "Tap every forged header line. Find all three to finish.",
                    "heading": "Original message",
                    "lede": "The raw headers behind this email, exactly as sent.",
                    "frame": {
                        "tab": "Show original · Gmail", "fav": "M", "favbg": "#ea4335",
                        "url_prefix": "https://", "url": "mail.google.com", "url_bold": "/mail/u/0/original",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "nodes": [
                        {"label": "From: \"Xero Billing\" <billing@xero.com>", "detail": "the display name and address shown to you", "weak": False,
                         "why": "This looks right: a real Xero domain. But check where a reply would actually go."},
                        {"label": "Reply-To: support@xero-invoice-secure.net", "detail": "where a reply is actually sent", "weak": True,
                         "why": "Forged. Genuine Xero mail replies to xero.com, not this lookalike domain. Any reply, or a click within the message, actually goes here."},
                        {"label": "Return-Path: bounce@xero-invoice-secure.net", "detail": "where a bounced message goes back to", "weak": True,
                         "why": "Forged. The return path matches the same lookalike domain as the Reply-To, not the real Xero one. This is where the message actually originated."},
                        {"label": "Received: from mail.xero-invoice-secure.net (203.0.113.44)", "detail": "the mail server that actually sent it", "weak": True,
                         "why": "Forged. The originating server is the lookalike domain again, not a genuine Xero mail server."},
                        {"label": "Subject: Your February invoice is ready", "detail": "the message subject line", "weak": False,
                         "why": "Ordinary, unremarkable subject line. Nothing suspicious here on its own."},
                        {"label": "Date: Thu, 12 Feb 2026 09:14:11 +1100", "detail": "the message timestamp", "weak": False,
                         "why": "A normal timestamp. Dates are trivial to fake either way, so this alone tells you nothing."},
                    ],
                },
            },
            {
                "key": "the-clone-call",
                "kind": "branch",
                "points": 2,
                "title": "The call that sounds like Wayne",
                "body": "<p>Lesson 1 covered AI voice cloning and caller ID "
                "spoofing: a familiar voice is no longer proof of who is really "
                "calling. Here is that call, live. Answer it, and make each call "
                "as it unfolds.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> a familiar "
                "voice and a matching caller ID are no longer proof. Verify any "
                "urgent money request on a number you already have.</div>",
                "payload": {
                    "prompt": "The call comes in. Make each call and see the consequence.",
                    "variant": "call",
                    "caller": "Wayne Castellano",
                    "subtitle": "mobile · Friday 3:45 pm",
                    "start": "call",
                    "nodes": {
                        "call": {
                            "text": "It's Rhonda, I'm flat out on the Gilmore St site and the reception's ordinary. I need you to wire $9,400 to a new supplier today so we don't lose our delivery slot before the weekend. Don't mention it to Bianca yet, I haven't had a chance to fill her in.",
                            "choices": [
                                {"label": "Say you'll sort it, hang up, and call Wayne back on the mobile number you already have", "outcome": "good",
                                 "feedback": "Right. Verifying on a number you already trust is the one move a voice clone cannot beat.", "to": "verify"},
                                {"label": "Make the transfer, it's clearly his voice and he's the boss", "outcome": "bad",
                                 "feedback": "That is exactly what the scam needs. A familiar voice can be cloned, and the secrecy is there to stop you checking.", "to": "paid_bad"},
                                {"label": "Ask him a personal question only Wayne would know, to be sure", "outcome": "risky",
                                 "feedback": "Risky. A well-prepared attacker may know the answer, and a clone can respond smoothly. Hang up and call back instead.", "to": "verify"},
                            ],
                        },
                        "paid_bad": {
                            "text": "The money lands in a criminal's account and is gone within minutes. The voice was an AI clone built from a recording of Wayne. A callback to his real number would have stopped it cold.",
                            "choices": [],
                        },
                        "verify": {
                            "text": "You call Wayne's real mobile. He's confused: he's on the tools, made no such call, and knows nothing about any new supplier or a $9,400 deposit. The voice was a clone.",
                            "choices": [
                                {"label": "Tell Wayne and Bianca straight away so everyone is warned, and confirm no payment went out", "outcome": "good",
                                 "feedback": "Exactly. Warning the team turns your near miss into everyone's defence against the next call.", "to": "win"},
                                {"label": "Say nothing, since no money was actually lost", "outcome": "bad",
                                 "feedback": "Staying quiet leaves colleagues exposed to the same call. Report it so the whole team is ready.", "to": "quiet_bad"},
                            ],
                        },
                        "quiet_bad": {
                            "text": "The following week the same clone calls Bianca, who has heard nothing about it, and a payment goes out. A quick warning would have prevented it.",
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
                "key": "triage-voicemail",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the voicemail inbox",
                "body": "<p>Last one, and it pulls both halves of business email "
                "compromise from Lesson 1 together: the CEO-style call you just "
                "hung up on, and its quieter cousin, invoice or bank-change fraud. "
                "Five voicemails are waiting. Listen to each and mark it Genuine "
                "or Scam.</p>"
                "<div class=\"cy-callout\">A changed bank account, or an urgent "
                "request to move money, by voicemail: neither is proof of who left "
                "it. Verify on a number you already have before anything moves.</div>",
                "payload": {
                    "prompt": "Sort every voicemail. Mark each Genuine or Scam to finish.",
                    "variant": "voicemail",
                    "voicemails": [
                        {"from": "Reece Plumbing Supplies", "number": "03 9876 5432", "time": "8:12 am", "duration": "0:14",
                         "transcript": "Hi it's Dave from Reece, your order's ready for pickup whenever, no rush, cheers.",
                         "phish": False,
                         "why": "A known supplier, an order you actually placed, nothing asked of you. Genuine."},
                        {"from": "Unknown", "number": "+61 400 111 222", "time": "9:30 am", "duration": "0:32",
                         "transcript": "This is Constable Reeves from Victoria Police regarding an outstanding warrant. Call this number back immediately or a warrant will be issued for your arrest.",
                         "phish": True,
                         "why": "Police do not chase warrants by voicemail or demand a callback like this. The authority and fear are the whole trick."},
                        {"from": "Rhonda Steel", "number": "0412 555 019", "time": "11:04 am", "duration": "0:09",
                         "transcript": "Hey it's Rhonda, BAS is done, sitting in the shared folder, no reply needed.",
                         "phish": False,
                         "why": "A normal, expected update from the bookkeeper, asking nothing and pushing nothing. Genuine."},
                        {"from": "Reece Accounts", "number": "Unknown number", "time": "1:47 pm", "duration": "0:26",
                         "transcript": "Hi it's Steve from Reece Accounts, just letting you know we've changed our bank details, please use the new BSB and account for this month's invoice, thanks.",
                         "phish": True,
                         "why": "A changed bank account by voicemail is exactly the invoice or bank-change fraud from Lesson 1. Ring Reece on a number you already have before paying anything different."},
                        {"from": "Liam Dorsett", "number": "0455 233 810", "time": "3:58 pm", "duration": "0:11",
                         "transcript": "It's Liam, running late to the Gilmore St job, stuck in traffic, tell the customer sorry.",
                         "phish": False,
                         "why": "An ordinary heads-up from the apprentice about a real job. Genuine."},
                    ],
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
