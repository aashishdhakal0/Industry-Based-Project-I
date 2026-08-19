"""Module 3, Phishing & Social Engineering: the con behind the click, the email
family (phishing, spear phishing, whaling), the attacks that leave the inbox
(smishing, vishing, pretexting, baiting), and the investigator's habits.

Same shape and standard as Modules 1 and 2 (see modules/content/module_one.py and
docs/module-authoring.md): a lesson is a scrollable room of collapsible task
PANELS. Each panel is a full, deep task: several teaching paragraphs (what it is,
a concrete Australian example, why it matters, what to do), a diagram where it
helps, a callout box with a specific scenario, sometimes a mid-panel check, then
the end interactive. Points sum to 10 per lesson and bank at lesson end.

Voice: warm, confident, human. Plain Australian English. No em-dashes, no filler,
no repetition, and nothing recycled from earlier modules.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "The con, and the channels it comes through",
        "reading_time_minutes": 8,
        "intro": "Social engineering does not attack your computer. It attacks "
        "you, through whatever channel reaches you fastest: your inbox, your "
        "phone, a text. Meet the con, and the four channels it rides in on.",
        "tasks": [
            {
                "key": "channels",
                "kind": "classify",
                "points": 2,
                "title": "Which channel is this?",
                "body": "<p><strong>Social engineering</strong> is the art of "
                "manipulating a person into helping the attacker: clicking, paying, "
                "or handing over a password. It works by pulling human levers, "
                "<strong>authority</strong>, <strong>urgency</strong>, "
                "<strong>fear</strong>, <strong>curiosity</strong> and "
                "<strong>greed</strong>, and it arrives through four main channels. "
                "<strong>Email phishing</strong> is the classic. "
                "<strong>Smishing</strong> is the same con by text message. "
                "<strong>Vishing</strong> is by phone, now supercharged by AI voice "
                "cloning that can fake a familiar voice. And "
                "<strong>business email compromise</strong> impersonates a boss or "
                "supplier to redirect a real payment.</p>"
                "<div class=\"cy-callout\">Read each message below and tap the "
                "channel it uses. Naming the channel is the first step to seeing "
                "through the con.</div>",
                "inline_check": {
                    "question": "An email that appears to be from your CEO and says 'do this in the next 10 minutes' is mainly pulling which two levers?",
                    "hint": "Who it claims to be from, and the deadline.",
                    "options": [
                        ("Authority and urgency", True,
                         "Yes. It borrows the weight of a senior figure and adds a deadline so you act before you think."),
                        ("Curiosity and greed", False,
                         "No. A rushed order from the boss leans on authority and urgency, not a tempting offer."),
                        ("Fear and sympathy", False,
                         "No. The pressure here is who it claims to be plus the deadline: authority and urgency."),
                        ("Boredom and habit", False,
                         "No. The two levers being pulled are authority (the CEO) and urgency (10 minutes)."),
                    ],
                },
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
                        {"text": "A supplier emails that their bank account has changed, please pay the new account from now on.",
                         "category": "bec",
                         "why": "Business email compromise: a spoofed or hacked supplier redirecting real invoice payments to a stranger."},
                    ],
                },
            },
            {
                "key": "ceo-call",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: the CEO calls",
                "diagram": "scene-vish",
                "body": "<p>Vishing is a phone con, and it has a frightening new "
                "tool: <strong>AI voice cloning</strong>. From a few seconds of a "
                "person speaking, in a podcast, a video, a voicemail greeting, an "
                "attacker can generate a fake voice that sounds just like them. The "
                "worker above is living it: a caller who sounds exactly like the CEO "
                "is urgently demanding a transfer. Read the scene, then work through "
                "the drill and see how it plays out.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> a familiar "
                "voice and a matching caller ID are no longer proof. Verify any "
                "urgent money request on a number you already have.</div>",
                "inline_check": {
                    "question": "Look at the worker in the scene above. A caller who sounds exactly like the CEO is urgently demanding a $48,500 transfer, and to keep it quiet. What should they do right now?",
                    "hint": "A familiar voice can be cloned, and secrecy is there to stop them checking.",
                    "options": [
                        ("Do not act on the call: hang up and call the CEO back on a number they already have", True,
                         "Right. Verifying on a number you already trust is the one move a cloned voice cannot beat. Do not let the pressure or the secrecy rush you."),
                        ("Make the transfer, since the voice clearly sounds like the CEO", False,
                         "No. A familiar voice can now be cloned from public recordings. Never move money on a voice alone."),
                        ("Ask the caller a personal question to prove it is really her", False,
                         "No. A well-prepared attacker may know the answer, and a clone can respond smoothly. Hang up and call back instead."),
                        ("Reply to the request in the company chat to confirm the account", False,
                         "No. That does not verify the caller. Confirm a money request on a phone number you already trust."),
                    ],
                },
                "payload": {
                    "prompt": "The call comes in. Make each call and see the consequence.",
                    "start": "call",
                    "nodes": {
                        "call": {
                            "text": "Your phone rings: the caller ID shows your CEO, Sarah, and the voice sounds exactly like her. She says she is stuck in back-to-back meetings and needs you to transfer $48,500 to a new supplier before 4pm today, and to keep it quiet for now. What do you do?",
                            "choices": [
                                {"label": "Say you will handle it, hang up, and call her back on the number you already have", "outcome": "good",
                                 "feedback": "Right. Verifying on a number you already trust is the one move a voice clone cannot beat.", "to": "verify"},
                                {"label": "Make the transfer, it is clearly her voice and she is the boss", "outcome": "bad",
                                 "feedback": "That is exactly what the scam needs. A familiar voice can be cloned, and the secrecy is there to stop you checking.", "to": "paid_bad"},
                                {"label": "Ask her a personal question to prove it is really her", "outcome": "risky",
                                 "feedback": "Risky. A well-prepared attacker may know the answer, and a clone can respond smoothly. Hang up and call back instead.", "to": "verify"},
                            ],
                        },
                        "paid_bad": {
                            "text": "The money lands in a criminal's account and is gone within minutes. The voice was an AI clone built from Sarah's public talks. A callback to her real number would have stopped it cold.",
                            "choices": [],
                        },
                        "verify": {
                            "text": "You call Sarah's real mobile. She is bewildered: she made no such call, and knows nothing about any supplier. The voice was a clone. What now?",
                            "choices": [
                                {"label": "Tell finance and IT straight away so everyone is warned, and confirm no payment went out", "outcome": "good",
                                 "feedback": "Exactly. Warning the team turns your near miss into everyone's defence against the next call.", "to": "win"},
                                {"label": "Say nothing, since no money was actually lost", "outcome": "bad",
                                 "feedback": "Staying quiet leaves colleagues exposed to the same call. Report it so the whole team is ready.", "to": "quiet_bad"},
                            ],
                        },
                        "quiet_bad": {
                            "text": "The following week the same clone calls a colleague in accounts, who has heard nothing about it, and a payment goes out. A quick warning would have prevented it.",
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
                "key": "read-sms",
                "kind": "check",
                "points": 2,
                "title": "Read the text like an investigator",
                "diagram": "sms-phish",
                "body": "<p>Smishing lands on the device you trust most, your phone, "
                "where links are hard to inspect and you are often distracted. The "
                "message above looks urgent and official. Read it the way an "
                "investigator would, starting with whether you expected it and where "
                "the link really goes.</p>"
                "<div class=\"cy-callout\">The tells travel together: an unexpected "
                "message, a small fee, a tight deadline, and a link that is almost, "
                "but not quite, the real address.</div>",
                "question": "Looking at the text above, what most clearly marks it as a scam?",
                "hint": "Was it expected, and where does that link actually point?",
                "options": [
                    ("It is unexpected, pressures you with a fee and a deadline, and links to a lookalike site, aus-post-redelivery.info, not the real Australia Post", True,
                     "Right. Australia Post does not chase small redelivery fees by text link, and the address is a lookalike. Unexpected plus urgency plus a near-miss link is smishing."),
                    ("It was sent to a mobile phone", False,
                     "No. Plenty of genuine messages arrive by text. The tells are the unexpected fee, the deadline, and the lookalike link."),
                    ("It mentions a parcel", False,
                     "No. Real delivery updates mention parcels too. The giveaway is the fee, the pressure, and the fake address."),
                    ("It is short", False,
                     "No. Length proves nothing. The scam is in the unexpected fee, the deadline, and the lookalike link."),
                ],
            },
            {
                "key": "inbox-triage",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the morning inbox",
                "body": "<p>Now the everyday skill: an inbox with a mix of genuine "
                "mail and phishing. Read the sender, the subject and the preview, "
                "then mark each one. The verdict and the tell are revealed as you "
                "go.</p>"
                "<div class=\"cy-callout\">Weigh the same things each time: did you "
                "expect it, who is it really from, is it rushing you, and is it "
                "pushing a link or an attachment?</div>",
                "payload": {
                    "prompt": "Mark each message Genuine or Phishing. Sort all five to finish.",
                    "emails": [
                        {"from": "Payroll <payroll@yourcompany.com.au>",
                         "subject": "Your July payslip is ready",
                         "preview": "Your payslip is available in the usual staff portal. No action needed.",
                         "phish": False,
                         "why": "Expected, from your own company domain, and it points you to the portal you already use, not a link."},
                        {"from": "IT Security <security@company-verify.net>",
                         "subject": "Your password expires in 2 hours, act now",
                         "preview": "Confirm your current password here to avoid being locked out.",
                         "phish": True,
                         "why": "A lookalike domain and a rushed link asking you to confirm a password. Real IT never asks for that."},
                        {"from": "Linda Poulos (Reception)",
                         "subject": "Parcel at the front desk for you",
                         "preview": "A parcel arrived this morning, pop down when you get a chance.",
                         "phish": False,
                         "why": "A normal, expected note from a colleague you know, with no link, attachment or pressure."},
                        {"from": "DocuSign <no-reply@docusign-portal-au.com>",
                         "subject": "You have a document to sign, opens in 24 hours",
                         "preview": "Review and sign the attached contract before it expires.",
                         "phish": True,
                         "why": "A lookalike DocuSign domain with a manufactured deadline. Reach signing services the way you normally do, never through the link."},
                        {"from": "The Bean Room Cafe",
                         "subject": "Your coffee loyalty: one free coffee waiting",
                         "preview": "Show this email in store to claim. See you soon!",
                         "phish": False,
                         "why": "A genuine marketing email you signed up for, asking nothing risky and pushing no link to log in."},
                    ],
                },
            },
            {
                "key": "multichannel-tabletop",
                "kind": "branch",
                "points": 2,
                "title": "Tabletop: an attack on every channel",
                "body": "<p>Real attacks often come through more than one channel at "
                "once, to wear down your doubt. This is a tabletop drill: the "
                "situation unfolds, you make a few connected calls, and you see how "
                "it plays out.</p>"
                "<div class=\"cy-callout\">The same instinct works whatever the "
                "channel: do not act on the message in front of you, verify through "
                "one you already trust, and report it.</div>",
                "payload": {
                    "prompt": "Handle the morning as it unfolds. Make each call and see the consequence.",
                    "start": "email",
                    "nodes": {
                        "email": {
                            "text": "9am. An email 'from IT' tells everyone to re-verify their password via a link, today. It looks a bit off. What is your first move?",
                            "choices": [
                                {"label": "Do not click. Check with IT the normal way and warn colleagues to hold off", "outcome": "good",
                                 "feedback": "Right. You go to IT the way you always do, not through the email's link, and you slow everyone down.", "to": "text"},
                                {"label": "Click the link and re-enter your password so you are not locked out", "outcome": "bad",
                                 "feedback": "That hands your password to the attacker. Real IT does not make you confirm it through an email link.", "to": "clicked_bad"},
                            ],
                        },
                        "clicked_bad": {
                            "text": "Your password is captured and used within the hour to send more phishing from your account. A quick check with IT, instead of clicking, would have stopped it.",
                            "choices": [],
                        },
                        "text": {
                            "text": "Minutes later, a text arrives on your phone with the very same link. Then your desk phone rings: a friendly 'help desk' caller offers to walk you through the verification. What now?",
                            "choices": [
                                {"label": "Decline the caller, do not use the link, and report all three to IT as one coordinated scam", "outcome": "good",
                                 "feedback": "Exactly. Three channels pushing the same link is a strong sign of a coordinated attack. Reporting it protects the whole office.", "to": "win"},
                                {"label": "Let the caller guide you, since they clearly know about the email", "outcome": "bad",
                                 "feedback": "Knowing about the email is part of the act. The caller is the scam, using the email and text to seem legitimate.", "to": "caller_bad"},
                            ],
                        },
                        "caller_bad": {
                            "text": "The caller talks you through 'verifying', and you hand over your login. The multi-channel act worked because each part made the others look real. Never let an unexpected caller drive.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Three channels, one scam, and you stopped all of it: no click, no call, and a report that warned everyone. Verify through a channel you trust, whatever the message claims.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
    {
        "title": "Read it like an analyst: spot, verify, report",
        "reading_time_minutes": 8,
        "intro": "You do not need to be technical to read a message like a security "
        "analyst. You need a short checklist and the discipline to use it: check "
        "the sender, distrust the link, verify on a separate channel, and report "
        "what you find.",
        "tasks": [
            {
                "key": "red-flags",
                "kind": "classify",
                "points": 2,
                "title": "Name the red flag",
                "body": "<p>An analyst does not need a gut feeling; they run a "
                "checklist. Most attacks trip at least one of four wires: a "
                "<strong>fake sender</strong> (a lookalike address), a "
                "<strong>dodgy link</strong> (the text says one thing, the address "
                "goes elsewhere), <strong>pressure or secrecy</strong> (act now, "
                "tell no one), or an <strong>unexpected attachment</strong>. Read "
                "each observation below and name the red flag it shows.</p>"
                "<div class=\"cy-callout\">One red flag is enough to slow down. Two "
                "or more, and you should assume it is an attack until you have "
                "verified otherwise.</div>",
                "payload": {
                    "prompt": "Read each observation and tap the red flag it shows. Name all six to finish.",
                    "categories": [
                        {"id": "sender", "label": "Fake sender"},
                        {"id": "link", "label": "Dodgy link"},
                        {"id": "pressure", "label": "Pressure or secrecy"},
                        {"id": "attach", "label": "Unexpected attachment"},
                    ],
                    "events": [
                        {"text": "The name shows your bank, but the address is service@secure-bank-alerts.info.",
                         "category": "sender",
                         "why": "A fake sender: the friendly name is easy to set, but the real domain after the @ is a lookalike, not the bank."},
                        {"text": "The link text reads bankofmelbourne.com, but hovering shows it goes to bankofmelb-login.co.",
                         "category": "link",
                         "why": "A dodgy link: the visible text and the real destination do not match. Always trust the destination, not the text."},
                        {"text": "'Act within 30 minutes or your account will be permanently closed.'",
                         "category": "pressure",
                         "why": "Pressure: a manufactured deadline exists to stop you thinking and checking. Genuine services give you time."},
                        {"text": "'Please keep this request between us and do not mention it to the team.'",
                         "category": "pressure",
                         "why": "Secrecy: asking you to bypass your normal checks and colleagues is a hallmark of a scam, not a real instruction."},
                        {"text": "An invoice you were not expecting, sent as a .zip file to open.",
                         "category": "attach",
                         "why": "An unexpected attachment: a surprise file, especially a .zip, is a common way to deliver malware. Verify before opening."},
                        {"text": "The email is from ceo-office-mail.com, which is not your company's domain.",
                         "category": "sender",
                         "why": "A fake sender: an outside lookalike domain impersonating your CEO. Check the domain, not just the display name."},
                    ],
                },
            },
            {
                "key": "vendor-bank-change",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: the vendor's bank details changed",
                "body": "<p>Business email compromise costs Australian organisations "
                "dearly, and it rarely looks dramatic. It looks like a routine email "
                "from a supplier you know, quietly asking you to send the next "
                "payment to a new account. Work through it.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> a change of "
                "bank account is always worth a phone call, on a number you already "
                "have, before a cent moves.</div>",
                "payload": {
                    "prompt": "The email arrives. Make each call and see the consequence.",
                    "start": "email",
                    "nodes": {
                        "email": {
                            "text": "A long-standing supplier emails: their bank account has changed, so please pay this month's invoice, which really is due, to the new account below. The email looks entirely normal. What do you do?",
                            "choices": [
                                {"label": "Ring the supplier on the number you already have and confirm the change first", "outcome": "good",
                                 "feedback": "Right. Verifying a bank-account change on a trusted number is the one habit that defeats this scam.", "to": "verify"},
                                {"label": "Update the details and pay, so the invoice is not late", "outcome": "bad",
                                 "feedback": "That sends the money to a criminal. A changed account plus any urgency always deserves a phone call first.", "to": "paid_bad"},
                                {"label": "Reply to the email to confirm the new account is genuine", "outcome": "bad",
                                 "feedback": "If the email is compromised, you are asking the attacker, who will happily confirm. Verify a different way.", "to": "reply_bad"},
                            ],
                        },
                        "paid_bad": {
                            "text": "The payment lands in a stranger's account and is gone. The supplier's email had been spoofed. One phone call to the number on last month's statement would have caught it.",
                            "choices": [],
                        },
                        "reply_bad": {
                            "text": "Your reply goes to the attacker, who cheerfully confirms the new account. Replying can never verify a suspicious message. Reach the sender a way you already trust.",
                            "choices": [],
                        },
                        "verify": {
                            "text": "You call the supplier on their known number. They are alarmed: they never changed their account, and their email was compromised. What now?",
                            "choices": [
                                {"label": "Hold the payment, warn your accounts team, and report the compromised supplier email", "outcome": "good",
                                 "feedback": "Exactly. You stop the payment, protect colleagues who might get the same email, and flag the real problem.", "to": "win"},
                                {"label": "Just pay the old account and move on quietly", "outcome": "bad",
                                 "feedback": "Paying the old account is right, but staying quiet leaves your team and the supplier's other customers exposed. Report it.", "to": "quiet_bad"},
                            ],
                        },
                        "quiet_bad": {
                            "text": "A colleague gets the same email next week, hears nothing from you, and pays the new account. A quick warning would have stopped a second loss.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Nothing lost, the team warned, the compromise reported. A bank-change email met the one check it cannot survive: a call to a number you already trust.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "read-exec-email",
                "kind": "check",
                "points": 2,
                "title": "Read the executive's email",
                "diagram": "exec-email",
                "body": "<p>Here is business email compromise up close, with the red "
                "flags called out. It impersonates a leader to push an unusual "
                "payment through fast and quietly. Read it like an analyst: start "
                "with the real sender address, then the pressure, then the "
                "request.</p>"
                "<div class=\"cy-callout\">The pattern is always the same: someone "
                "important, in a hurry, asking for money or secrecy, from an address "
                "that is not quite right.</div>",
                "question": "Reading the email above, what most clearly marks it as business email compromise?",
                "hint": "Weigh the sender address, the tone, and the request together.",
                "options": [
                    ("It comes from a lookalike domain (ceo-office-mail.com), pressures you with urgency and secrecy, and requests an unusual payment that skips the normal checks", True,
                     "Right. A not-quite-right sender, plus pressure and secrecy, plus a request that avoids the usual process, is the signature of business email compromise."),
                    ("It is addressed to you by name", False,
                     "No. Genuine emails use your name too. The tells are the lookalike domain, the pressure and secrecy, and the unusual payment."),
                    ("It mentions a meeting", False,
                     "No. 'I am in meetings' is just the excuse for why you cannot call to check. The real tells are the domain, the pressure and the payment."),
                    ("It is signed with a first name", False,
                     "No. A signature proves nothing. The giveaways are the fake domain, the urgency and secrecy, and the out-of-process payment."),
                ],
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
                    "why": "The right-hand one is from a lookalike domain (company-verify.net) and pushes you to confirm your password through a link, which real IT never does. The left-hand one is from your real domain and asks nothing of you.",
                    "left": {
                        "sender": "IT Service Desk <helpdesk@yourcompany.com.au>",
                        "text": "Scheduled maintenance this Saturday 7am to 8am. Email may be briefly unavailable. No action needed from you.",
                    },
                    "right": {
                        "sender": "IT Security <security@company-verify.net>",
                        "text": "Your password expires today. Confirm your current password here within 2 hours to avoid being locked out.",
                    },
                },
            },
            {
                "key": "report-tabletop",
                "kind": "branch",
                "points": 2,
                "title": "Tabletop: you spotted it, now what?",
                "body": "<p>Spotting a phishing email is only half the job. What you "
                "do next decides whether it stops with you or catches a colleague. "
                "Work through this final drill.</p>"
                "<div class=\"cy-callout\">Reporting beats deleting every time: "
                "deleting protects only you, reporting lets the people who can block "
                "it protect everyone.</div>",
                "payload": {
                    "prompt": "You have spotted a convincing phish. Make each call and see the consequence.",
                    "start": "spotted",
                    "nodes": {
                        "spotted": {
                            "text": "A convincing phishing email is sitting in your inbox, and two colleagues mention getting the same one. What do you do?",
                            "choices": [
                                {"label": "Report it using the report button or by telling IT, so it can be blocked and others warned", "outcome": "good",
                                 "feedback": "Right. Reporting gets it in front of the people who can block it and alert everyone who received it.", "to": "then"},
                                {"label": "Just delete it and get on with your day", "outcome": "bad",
                                 "feedback": "Deleting protects only you. Your colleagues still have it in their inboxes, one click from trouble.", "to": "delete_bad"},
                                {"label": "Forward it to the whole team to warn them", "outcome": "bad",
                                 "feedback": "That spreads the dangerous link and invites a mis-click. Report it through the proper channel instead.", "to": "forward_bad"},
                            ],
                        },
                        "delete_bad": {
                            "text": "You are safe, but an hour later a colleague clicks the same email and enters their login. A quick report would have had it blocked for everyone.",
                            "choices": [],
                        },
                        "forward_bad": {
                            "text": "Forwarding it puts the live link in more inboxes, and someone clicks it by reflex. Warn people, yes, but by reporting it, not by passing the attack around.",
                            "choices": [],
                        },
                        "then": {
                            "text": "IT confirms it is a phishing campaign and blocks the sender. A colleague admits they already clicked the link and entered their password. What now?",
                            "choices": [
                                {"label": "Have them change that password, turn on two-factor, and tell IT which account", "outcome": "good",
                                 "feedback": "Exactly. Fast, blame-free action locks the account down before the stolen password can be used.", "to": "win"},
                                {"label": "Tell them to keep quiet so they do not get in trouble", "outcome": "bad",
                                 "feedback": "Silence lets the attacker use the password freely. Early, blame-free reporting is what limits the damage.", "to": "quiet_bad"},
                            ],
                        },
                        "quiet_bad": {
                            "text": "Overnight the stolen login is used to send more phishing from inside the company. Owning up early, without blame, would have contained it in minutes.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Reported, blocked, and the one click contained. That is the whole analyst's job for a non-technical person: spot it, verify it, and report it fast.",
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
        # ---- Lesson 1: The con behind the click ----
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
            "lesson": 1, "difficulty": "EASY",
            "text": "What is baiting?",
            "options": [
                ("Luring you with something tempting, like a found USB stick or a free prize, to make you act", True,
                 "Yes. Baiting dangles something you want so your curiosity or greed overrides your caution."),
                ("Sending the same scam to millions of people at once", False,
                 "No. That is mass phishing. Baiting lures you with a tempting offer or object."),
                ("Pretending to be your bank on the phone", False,
                 "No. That is vishing. Baiting uses a tempting lure, like a dropped USB or a prize."),
                ("Encrypting your files for a ransom", False,
                 "No. That is ransomware. Baiting is a social-engineering lure."),
            ],
        },
        # ---- Lesson 2: Phishing and its sharper cousins ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "How does ordinary phishing differ from a targeted attack?",
            "options": [
                ("It is sent generically to huge numbers of people, not tailored to any one person", True,
                 "Yes. Mass phishing is a wide net: the same generic message to a giant list, hoping a few bite."),
                ("It is always sent by text message, never email", False,
                 "No. Ordinary phishing is usually email. The point is that it is generic and sent widely."),
                ("It is aimed carefully at one named person", False,
                 "No. That describes spear phishing. Ordinary phishing is generic and mass-sent."),
                ("It can only be sent by someone who knows you", False,
                 "No. Mass phishing needs no knowledge of you; it is sent blindly to huge lists."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
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
            "text": "An urgent, unusual payment request appears to come from your CEO. What is the safest defence against this kind of CEO fraud or whaling?",
            "options": [
                ("Verify the request on a separate channel you already trust, whoever it seems to be from", True,
                 "Yes. A quick call or message on a known number defeats CEO fraud, because the attacker cannot answer it."),
                ("Pay it quickly because it is from the boss", False,
                 "No. That is exactly what the scam relies on. Verify any unusual urgent payment first."),
                ("Reply to the email and ask if it is genuine", False,
                 "No. If it is a scam, you are asking the scammer. Verify on a separate trusted channel."),
                ("Check whether the email has a company logo", False,
                 "No. Logos are trivial to copy. Verify the request itself on a channel you already trust."),
            ],
        },
        # ---- Lesson 3: Beyond the inbox ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
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
        {
            "lesson": 1, "difficulty": "EASY",
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
        # ---- Lesson 4: Reading an email like an investigator ----
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
    ],
}
