"""Module 4, Secure Communication Practices: two hands-on lessons.

Two lessons, built around a "before you hit send" frame:

  Lesson 1  Before you hit send: what 'secure' really means
            (encryption in plain English, the padlock, end-to-end, verifying a
            sender, and matching the care to how sensitive the message is)
  Lesson 2  Sharing safely: files, links, and Wi-Fi
            (secure links vs attachments, sending the key separately, public
            Wi-Fi and evil twins, and when a VPN or sealed channel is worth it)

Same 5-task room as Modules 1 and 2, with its own character: a checklist that
runs through real workplace send/share decisions, and figures that PROVE the
point (an encrypted-vs-open message compare, a real-vs-risky share link, a cafe
Wi-Fi picker with an evil twin). Voice: warm, plain Australian English, no
em-dashes, no emoji. Points sum to 10 per lesson and bank at lesson end.
"""

LESSONS = [
    {
        "title": "Before you hit send: what 'secure' really means",
        "reading_time_minutes": 8,
        "intro": "Most days you send information without a second thought. This "
        "lesson adds a short pause before you hit send: is this private, and is "
        "the way I am sending it actually sealed, or wide open?",
        "tasks": [
            {
                "key": "encrypted-or-open",
                "kind": "sort",
                "points": 2,
                "title": "Encrypted, or out in the open?",
                "body": "<p>To <strong>encrypt</strong> information is to scramble "
                "it with a key, so only someone with the key can read it. It is the "
                "difference between a sealed envelope and a postcard. Some of the "
                "ways we communicate are sealed; others are wide open, readable by "
                "anyone who can see the traffic along the way. Sorting them is the "
                "quickest way to build the instinct.</p>"
                "<div class=\"cy-callout\">Tap each item, then tap whether it is "
                "encrypted (only the right person can read it) or out in the open "
                "(others along the way could).</div>",
                "inline_check": {
                    "question": "A phishing website shows the padlock and https in the address bar. What does that prove?",
                    "hint": "The padlock is about the connection, not the owner.",
                    "options": [
                        ("Only that the connection is encrypted, not that the site is genuine", True,
                         "Yes. The padlock means the link to the site is encrypted. Scam sites can show it too, so it is not proof of trust."),
                        ("That the website is safe and genuine", False,
                         "No. The padlock says nothing about who runs the site. Phishing sites can show it as well."),
                        ("That your antivirus has checked the site", False,
                         "No. The padlock is unrelated to antivirus. It only means the connection is encrypted."),
                        ("That the site cannot collect your password", False,
                         "No. A fake page can still collect whatever you type. The padlock only encrypts the connection."),
                    ],
                },
                "payload": {
                    "prompt": "Tap an item, then tap whether it is Encrypted or Out in the open. Sort all six to finish.",
                    "buckets": [
                        {"id": "enc", "label": "Encrypted"},
                        {"id": "open", "label": "Out in the open"},
                    ],
                    "items": [
                        {"text": "A message sent through an end-to-end encrypted app", "bucket": "enc",
                         "why": "Encrypted. Only you and the recipient can read it, not even the service carrying it."},
                        {"text": "A normal email carrying sensitive client details", "bucket": "open",
                         "why": "Out in the open. Standard email is like a postcard: it passes through servers and can be read or misdirected."},
                        {"text": "A web page showing the padlock and https", "bucket": "enc",
                         "why": "Encrypted in transit. The padlock means the connection is scrambled, so an eavesdropper cannot read it."},
                        {"text": "What you type over open cafe Wi-Fi with no VPN", "bucket": "open",
                         "why": "Out in the open. On an unsecured network a stranger nearby may capture what you send."},
                        {"text": "A password-protected file, with the password sent a separate way", "bucket": "enc",
                         "why": "Encrypted. The file is scrambled, and because the password travels separately, seeing one is not enough."},
                        {"text": "An ordinary SMS text message", "bucket": "open",
                         "why": "Out in the open. Standard texts are not end-to-end encrypted, so they are a poor choice for private information."},
                    ],
                },
            },
            {
                "key": "sending-the-form",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: sending the client's form",
                "diagram": "scene-send",
                "body": "<p>Here is the everyday decision this module is really "
                "about, and it is playing out in the scene above: a client's file, "
                "about to go out as a plain email, and a colleague who has spotted "
                "it. You have a document full of a client's private details, and it "
                "needs to reach a colleague. How you send it is the whole question. "
                "Read the scene, then work through the drill.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> match the "
                "care to the sensitivity. Private information needs a sealed "
                "channel, not whatever is quickest.</div>",
                "inline_check": {
                    "question": "Look at the scene above: the worker is about to email a client's medical form as a plain attachment, to a personal address. What should they do?",
                    "hint": "Weigh how sensitive the file is against how exposed plain email is.",
                    "options": [
                        ("Stop, and send it through a secure channel, or a password-protected file with the password sent separately", True,
                         "Right. A medical form is exactly the kind of private data that needs a sealed channel, so only the intended person can open it."),
                        ("Send it, plain email is quicker and the colleague is waiting", False,
                         "No. Plain email is a postcard, and one wrong address is a breach. Speed does not change how sensitive the file is."),
                        ("Send it, but CC a manager so someone else has a copy", False,
                         "No. That just exposes the private file to more inboxes. Use a sealed, access-controlled channel instead."),
                        ("Paste the details into the body of the email instead of attaching them", False,
                         "No. The email body is just as exposed as an attachment. The fix is a sealed channel, not a different part of the email."),
                    ],
                },
                "payload": {
                    "prompt": "The form needs sending. Make each call and see the consequence.",
                    "start": "send",
                    "nodes": {
                        "send": {
                            "text": "A client's medical intake form, full of personal and health details, needs to go to a colleague across town. What do you do?",
                            "choices": [
                                {"label": "Share it through a secure, access-controlled channel, or a password-protected file with the password sent separately", "outcome": "good",
                                 "feedback": "Right. Sensitive health data deserves a sealed channel, so only the intended person can open it.", "to": "arrives"},
                                {"label": "Just attach it to a normal email, it is quicker", "outcome": "bad",
                                 "feedback": "Plain email is a postcard. Health information sent that way is exposed in transit and one wrong address from a breach.", "to": "email_bad"},
                                {"label": "Paste the details into a text message", "outcome": "bad",
                                 "feedback": "SMS is not encrypted end to end and is easy to misaddress. It is a poor channel for private details.", "to": "sms_bad"},
                            ],
                        },
                        "email_bad": {
                            "text": "The email autocompletes to the wrong contact, and a stranger now has a client's health record. Once it is sent, it cannot be recalled. A sealed channel would have kept it to the intended reader.",
                            "choices": [],
                        },
                        "sms_bad": {
                            "text": "The text goes through fine, but it also sits unencrypted on servers and could be read if the phone is lost or the number mistyped. Private details deserve better than SMS.",
                            "choices": [],
                        },
                        "arrives": {
                            "text": "Your colleague opens the form securely with the key you sent separately. Then they ask you to email them the password too, to save time. What do you say?",
                            "choices": [
                                {"label": "No, keep the password on a separate channel, like a quick phone call", "outcome": "good",
                                 "feedback": "Exactly. If the lock and the key travel together, anyone who sees that message has both. Keep them apart.", "to": "win"},
                                {"label": "Sure, reply to the same email with the password", "outcome": "bad",
                                 "feedback": "That defeats the point. The whole value of a password-protected file is that the password comes a different way.", "to": "key_bad"},
                            ],
                        },
                        "key_bad": {
                            "text": "Now the file and its password sit in the same thread. Anyone who reaches that email has the lock and the key together. Send the key a separate way, always.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Sent securely, opened by the right person, and the key kept separate. That is the whole discipline: match the care to the sensitivity, and never send the lock and the key together.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "read-encryption",
                "kind": "check",
                "points": 2,
                "title": "Read the message in transit",
                "diagram": "msg-encrypted",
                "body": "<p>Here is the same message, sent two ways, as it looks "
                "travelling across the network. One is readable by anyone who can "
                "see the traffic; the other is scrambled, useless without the key. "
                "This is what 'encrypted' actually buys you.</p>"
                "<div class=\"cy-callout\">Encryption does not hide that a message "
                "was sent. It makes the contents unreadable to everyone except the "
                "person holding the key.</div>",
                "question": "Looking at the two messages above, why is the encrypted one safer to send?",
                "hint": "Think about what a stranger watching the network would actually see.",
                "options": [
                    ("Its contents are scrambled with a key, so anyone watching the network sees only useless characters", True,
                     "Right. The plain message is readable in transit, like a postcard. The encrypted one is scrambled, so only the intended reader, who has the key, can open it."),
                    ("It is shorter, so less can leak", False,
                     "No. Length is not the point. The encrypted message is safer because its contents are scrambled and unreadable without the key."),
                    ("It was sent faster", False,
                     "No. Speed has nothing to do with it. Encryption protects the contents by scrambling them."),
                    ("It cannot be intercepted at all", False,
                     "No. It can still be intercepted, but the interceptor sees only scrambled characters, which is the whole point."),
                ],
            },
            {
                "key": "match-the-care",
                "kind": "classify",
                "points": 2,
                "title": "Match the care to the message",
                "body": "<p>Not everything needs a sealed channel. The skill is "
                "telling the everyday chatter from the genuinely private, so you "
                "spend your care where it matters. Read each thing you might send "
                "and decide: fine to send any normal way, or does it need a sealed "
                "channel?</p>"
                "<div class=\"cy-callout\">Ask one question: if a stranger read "
                "this, would it harm anyone? If yes, seal it.</div>",
                "payload": {
                    "prompt": "Read each item and tap whether it is fine any way, or needs a sealed channel. Sort all six to finish.",
                    "categories": [
                        {"id": "fine", "label": "Fine to send any way"},
                        {"id": "sealed", "label": "Needs a sealed channel"},
                    ],
                    "events": [
                        {"text": "An invitation to Friday's team lunch.",
                         "category": "fine",
                         "why": "Fine any way. Nothing here would harm anyone if a stranger saw it."},
                        {"text": "A client's full name, date of birth and Medicare number.",
                         "category": "sealed",
                         "why": "Needs a sealed channel. Identity details like these are the raw material for fraud if exposed."},
                        {"text": "The time and place of the next public webinar.",
                         "category": "fine",
                         "why": "Fine any way. It is meant to be public, so a normal channel is perfectly appropriate."},
                        {"text": "A spreadsheet of staff bank account details.",
                         "category": "sealed",
                         "why": "Needs a sealed channel. Bank details in the wrong hands lead directly to fraud."},
                        {"text": "A link to the company's published newsletter.",
                         "category": "fine",
                         "why": "Fine any way. Public content carries no risk if others see it."},
                        {"text": "A scan of a passport for a new-hire's paperwork.",
                         "category": "sealed",
                         "why": "Needs a sealed channel. A passport is a prime identity-theft target and must be sent securely."},
                    ],
                },
            },
            {
                "key": "send-tabletop",
                "kind": "branch",
                "points": 2,
                "title": "Tabletop: the rushed request",
                "body": "<p>Pressure is where good habits get dropped. This drill "
                "puts the send checklist under a bit of stress: a busy afternoon and "
                "a request that wants to skip the careful path. Work it through.</p>"
                "<div class=\"cy-callout\">The send checklist does not change under "
                "pressure: is it private, is the channel sealed, and is the key kept "
                "separate?</div>",
                "payload": {
                    "prompt": "The request lands late in the day. Make each call and see the consequence.",
                    "start": "ask",
                    "nodes": {
                        "ask": {
                            "text": "At 4:55pm a manager messages: 'Quickly email me the full staff contact and payroll list, I need it for a meeting in five minutes.' What do you do?",
                            "choices": [
                                {"label": "Send it through the secure system you normally use, and let them know where to find it", "outcome": "good",
                                 "feedback": "Right. Urgency does not change the rules. The sensitive list goes through the sealed channel, as always.", "to": "then"},
                                {"label": "Paste the whole list into a plain email to save time", "outcome": "bad",
                                 "feedback": "A payroll list in plain email is exactly the kind of exposure that becomes a breach. Sensitive data still needs a sealed channel.", "to": "plain_bad"},
                            ],
                        },
                        "plain_bad": {
                            "text": "The email is fine until it is forwarded to the wrong person a week later, and a full payroll list is now loose. Under pressure or not, sensitive data belongs in a sealed channel.",
                            "choices": [],
                        },
                        "then": {
                            "text": "Done securely. A moment later a second message arrives: 'Also text me the shared drive password so I can get in from my phone.' What now?",
                            "choices": [
                                {"label": "Do not text the password; point them to the password manager or reset the access properly", "outcome": "good",
                                 "feedback": "Exactly. A password texted in the clear is a password exposed. Keep credentials out of plain messages.", "to": "win"},
                                {"label": "Text the password, they are in a hurry", "outcome": "bad",
                                 "feedback": "A texted password sits unencrypted and can be read if the phone is seen or lost. Never send credentials in the clear.", "to": "pw_bad"},
                            ],
                        },
                        "pw_bad": {
                            "text": "The password now lives in a text message on a phone that could be lost or shoulder-surfed. Credentials never belong in plain messages, however urgent the ask.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Both requests handled without dropping the rules: the sensitive list sealed, the password kept out of plain text. That steadiness under pressure is what secure communication really is.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
    {
        "title": "Sharing safely: files, links, and Wi-Fi",
        "reading_time_minutes": 8,
        "intro": "Sharing a file feels harmless, but a careless link or an open "
        "network can leak it just as surely as a lost laptop. This lesson is about "
        "sharing on your terms: control who gets in, and stay private on the move.",
        "tasks": [
            {
                "key": "safe-share-or-leak",
                "kind": "classify",
                "points": 2,
                "title": "Safe share, or a leak?",
                "body": "<p>Modern tools make sharing a file a one-tap job, which is "
                "exactly the problem: the quick option is often the leaky one. A "
                "<strong>permissioned link</strong>, restricted to named people and "
                "revocable, keeps you in control. A public 'anyone with the link' "
                "share, or a copy emailed around, does not. Read each share below "
                "and decide.</p>"
                "<div class=\"cy-callout\">The safe question is always the same: who "
                "can open this, and can I take that access back later?</div>",
                "payload": {
                    "prompt": "Read each share and tap whether it is a safe share or a leak. Sort all six to finish.",
                    "categories": [
                        {"id": "safe", "label": "Safe share"},
                        {"id": "leak", "label": "A leak"},
                    ],
                    "events": [
                        {"text": "A link restricted to specific people, that expires and can be revoked.",
                         "category": "safe",
                         "why": "Safe share. You control exactly who gets in, and you can withdraw access later."},
                        {"text": "A public 'anyone with the link can view' share, posted in a group chat.",
                         "category": "leak",
                         "why": "A leak. Anyone who ever sees or forwards that link can open the file, and you cannot take it back."},
                        {"text": "A password-protected file, with the password sent by a separate phone call.",
                         "category": "safe",
                         "why": "Safe share. The lock and the key travel separately, so intercepting one is not enough."},
                        {"text": "Emailing the whole spreadsheet as an attachment to a mailing list.",
                         "category": "leak",
                         "why": "A leak. You lose all control of the copy, and it can be forwarded anywhere from there."},
                        {"text": "Granting a colleague view-only access to just the folder they need.",
                         "category": "safe",
                         "why": "Safe share. Least access: they get only what they need, and nothing more."},
                        {"text": "Sharing a file, and putting its password in the very same message.",
                         "category": "leak",
                         "why": "A leak. Sending the lock and the key together means anyone who sees the message has both."},
                    ],
                },
            },
            {
                "key": "link-or-attachment",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: secure link, or email attachment?",
                "body": "<p>A real sharing decision, start to finish. A colleague at "
                "another office needs a client's file. The choice you make about "
                "how to share it decides who can reach it, and whether you can ever "
                "take it back. Work through it.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> share a "
                "permissioned link, not a loose copy. Control who can open it, and "
                "keep the power to revoke.</div>",
                "payload": {
                    "prompt": "The file needs sharing. Make each call and see the consequence.",
                    "start": "share",
                    "nodes": {
                        "share": {
                            "text": "A colleague across town needs a client's file. How do you get it to them?",
                            "choices": [
                                {"label": "Share a link restricted to them, that you can expire or revoke later", "outcome": "good",
                                 "feedback": "Right. A permissioned link keeps you in control of who can open it, and lets you take access back.", "to": "perms"},
                                {"label": "Email the file as an attachment", "outcome": "bad",
                                 "feedback": "Now there is a loose copy you cannot control. It can be forwarded anywhere, and you can never recall it.", "to": "attach_bad"},
                                {"label": "Post a public 'anyone with the link' share in the team chat", "outcome": "bad",
                                 "feedback": "Anyone who sees or forwards that link can open a client's file. A public link is a leak waiting to happen.", "to": "public_bad"},
                            ],
                        },
                        "attach_bad": {
                            "text": "Weeks later the attachment is forwarded to the wrong person, and a client's file is loose with no way to pull it back. A permissioned link would have kept you in control.",
                            "choices": [],
                        },
                        "public_bad": {
                            "text": "The public link gets forwarded beyond the team, and now strangers can open the file. Anyone-with-the-link means exactly that.",
                            "choices": [],
                        },
                        "perms": {
                            "text": "The link is set to the right person. Before you send it, what access do you give them?",
                            "choices": [
                                {"label": "View-only, the least they need, with an expiry date", "outcome": "good",
                                 "feedback": "Exactly. Least access plus an expiry means the share does only what it must, for only as long as it must.", "to": "win"},
                                {"label": "Full edit access, forever, just in case", "outcome": "bad",
                                 "feedback": "That hands over more power than needed, indefinitely. Give the least access required, and set it to expire.", "to": "edit_bad"},
                            ],
                        },
                        "edit_bad": {
                            "text": "The open-ended edit access lingers long after it was needed, a standing risk if that account is ever compromised. Least access, with an expiry, is the safer default.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Shared as a restricted, view-only, expiring link. You controlled who got in, gave only what was needed, and kept the power to revoke. That is sharing on your terms.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "read-share-link",
                "kind": "check",
                "points": 2,
                "title": "Read the share settings",
                "diagram": "secure-share",
                "body": "<p>The same file can be shared two ways, and the settings "
                "screen tells you which is safe. One link lets anyone in and never "
                "expires; the other is restricted, password protected and "
                "revocable. Read the two and decide which keeps you in control.</p>"
                "<div class=\"cy-callout\">A safe share answers three questions: who "
                "can open it, does it expire, and can you take access back?</div>",
                "question": "Looking at the two link settings above, which is the safe one, and why?",
                "hint": "Which one lets you control who gets in, and take it back?",
                "options": [
                    ("The restricted link: only specific people, password protected, and it expires and can be revoked", True,
                     "Right. It limits who can open the file and lets you withdraw access. The 'anyone with the link, never expires' option loses control the moment it is forwarded."),
                    ("The 'anyone with the link' one, because it is easier for people to open", False,
                     "No. Easy for anyone means easy for the wrong person too. Once forwarded, you cannot take it back."),
                    ("They are equally safe, it is the same file", False,
                     "No. The file is the same, but the access is not. Control over who gets in is the whole point."),
                    ("Neither, you should never share files", False,
                     "No. Sharing is fine when you control it. The restricted, expiring, revocable link is the safe way."),
                ],
            },
            {
                "key": "harden-workspace",
                "kind": "harden",
                "points": 2,
                "title": "Secure the workspace before you leave",
                "diagram": "wifi-evil-twin",
                "body": "<p>Working from a cafe or an airport is normal now, and so "
                "are the risks that come with it: open networks, lookalike hotspots, "
                "and an unlocked screen in a public place. The Wi-Fi picker above "
                "shows a classic trap, two near-identical open networks, one of "
                "which may be an <strong>evil twin</strong> set up to watch your "
                "traffic. Secure each part of your mobile setup.</p>"
                "<div class=\"cy-callout\">For each item, choose the option that "
                "closes the gap and watch it flip to Secured.</div>",
                "payload": {
                    "prompt": "Secure each part of your on-the-move setup. Lock down all four to finish.",
                    "steps": [
                        {
                            "label": "Doing sensitive work on open cafe Wi-Fi",
                            "risk": "An open network, or an evil twin, can let a stranger watch what you send.",
                            "options": [
                                {"text": "Use your phone's mobile hotspot or a trusted VPN instead", "correct": True,
                                 "why": "A hotspot keeps you off the untrusted network; a VPN wraps your traffic in encryption so an eavesdropper sees only scrambled data."},
                                {"text": "Pick whichever cafe network has the strongest signal", "correct": False,
                                 "why": "Signal strength says nothing about safety, and the strongest one could be the evil twin. Use a hotspot or VPN."},
                                {"text": "Just avoid websites with a padlock", "correct": False,
                                 "why": "Backwards. The padlock is good. The real fix on open Wi-Fi is a hotspot or a VPN."},
                            ],
                        },
                        {
                            "label": "Your laptop screen when you step away",
                            "risk": "An unlocked screen in a public place is an open door to your accounts and files.",
                            "options": [
                                {"text": "Lock the screen every time you leave it, even for a minute", "correct": True,
                                 "why": "A locked screen means a moment away does not become someone else's access to everything."},
                                {"text": "Turn the brightness down so it is harder to read", "correct": False,
                                 "why": "Dimming does nothing to stop someone using it. Lock the screen."},
                                {"text": "Trust that a cafe is a safe place", "correct": False,
                                 "why": "Public places are exactly where devices get grabbed or snooped. Lock it."},
                            ],
                        },
                        {
                            "label": "Software updates on your laptop and phone",
                            "risk": "Out-of-date software leaves known holes open for attackers to walk through.",
                            "options": [
                                {"text": "Turn on automatic updates so patches apply promptly", "correct": True,
                                 "why": "Automatic updates close known holes fast, before attackers can use them, without you having to remember."},
                                {"text": "Update only once a year to avoid disruption", "correct": False,
                                 "why": "That leaves known holes open for months. Patch promptly, ideally automatically."},
                                {"text": "Skip updates while travelling", "correct": False,
                                 "why": "Travelling is when you are on riskier networks. Keep updates on."},
                            ],
                        },
                        {
                            "label": "A file link you shared publicly last week",
                            "risk": "A leftover public link keeps a file open to anyone, long after it was needed.",
                            "options": [
                                {"text": "Revoke the public link and re-share it to just the people who need it", "correct": True,
                                 "why": "Revoking closes the open door; a restricted re-share gives access only to the right people."},
                                {"text": "Leave it, since nothing has gone wrong yet", "correct": False,
                                 "why": "An open link is a standing risk. Close it once it is no longer needed."},
                                {"text": "Rename the file so the link is harder to guess", "correct": False,
                                 "why": "The existing link still works. Revoke it and re-share with proper permissions."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "anywhere-tabletop",
                "kind": "branch",
                "points": 2,
                "title": "Tabletop: working from the airport",
                "body": "<p>One last drill, on the move. You are between flights, you "
                "have work to finish, and the environment is working against you. "
                "Apply everything: sealed channels, controlled sharing, and staying "
                "private on an untrusted network.</p>"
                "<div class=\"cy-callout\">Away from the office, assume the network "
                "is watching. Use your own connection or a VPN, and keep sensitive "
                "sharing controlled.</div>",
                "payload": {
                    "prompt": "You have work to finish at the airport. Make each call and see the consequence.",
                    "start": "wifi",
                    "nodes": {
                        "wifi": {
                            "text": "The airport lounge lists two open networks with almost the same name. You need to log in to a work system. What do you do?",
                            "choices": [
                                {"label": "Skip both and use your phone's mobile data or a trusted VPN", "outcome": "good",
                                 "feedback": "Right. One of those lookalikes could be an evil twin. Your own connection or a VPN keeps the session private.", "to": "share"},
                                {"label": "Join the one with the friendlier name and log straight in", "outcome": "bad",
                                 "feedback": "A friendly name is easy to fake. If it is the evil twin, your login just went through the attacker.", "to": "wifi_bad"},
                            ],
                        },
                        "wifi_bad": {
                            "text": "The network was a lookalike set up to capture logins, and yours was one of them. On open Wi-Fi, always use your own connection or a VPN.",
                            "choices": [],
                        },
                        "share": {
                            "text": "Connected safely. Now a colleague asks you to send them a sensitive report right away. How do you share it?",
                            "choices": [
                                {"label": "Share a restricted, expiring link through the secure system", "outcome": "good",
                                 "feedback": "Exactly. Even in a hurry, a controlled link keeps a sensitive report to the right person and revocable.", "to": "win"},
                                {"label": "Quickly email it as an attachment from the lounge", "outcome": "bad",
                                 "feedback": "A loose copy of a sensitive report, sent from an untrusted place, is a leak waiting to be forwarded. Use a controlled link.", "to": "share_bad"},
                            ],
                        },
                        "share_bad": {
                            "text": "The attachment is out of your hands the moment it sends, one forward from exposure. A restricted, revocable link would have kept it under control.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Private connection, controlled share, nothing loose. You carried the whole module out of the office and into the wild: seal the channel, control the share, and assume the network is watching.",
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
        # ---- Lesson 1: Before you hit send: what 'secure' really means ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does it mean to encrypt information?",
            "options": [
                ("Scramble it with a key so only someone with the key can read it", True,
                 "Yes. Encryption turns readable data into scrambled data that only the right key can unlock."),
                ("Delete it so no one can ever see it", False,
                 "No. Encryption does not delete data; it scrambles it so only a key holder can read it."),
                ("Hide it in a folder with a long name", False,
                 "No. Hiding a file is not encryption. Encryption mathematically scrambles the contents."),
                ("Back it up to a second drive", False,
                 "No. That is a backup, which protects against loss. Encryption protects against reading."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A phishing website shows the padlock and https in the address bar. What does that prove?",
            "options": [
                ("Only that the connection is encrypted, not that the site is genuine", True,
                 "Yes. The padlock means the link to the site is encrypted. Scam sites can get a padlock too, so it is not proof of trust."),
                ("That the website is safe and genuine", False,
                 "No. The padlock says nothing about who runs the site. Phishing sites can show it as well."),
                ("That your antivirus has checked the site", False,
                 "No. The padlock is unrelated to antivirus. It only means the connection is encrypted."),
                ("That the site cannot collect your password", False,
                 "No. A fake page can still collect whatever you type. The padlock only encrypts the connection."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is special about end-to-end encryption?",
            "options": [
                ("Only the sender and the recipient can read the message, not even the service carrying it", True,
                 "Yes. The message is scrambled on your device and only unscrambled on theirs, so the provider in the middle cannot read it."),
                ("It makes messages send faster", False,
                 "No. It is about privacy, not speed. Only the two ends can read the content."),
                ("It lets the service scan your messages for spam", False,
                 "No. The point is the opposite: the service cannot read the content at all."),
                ("It backs your messages up automatically", False,
                 "No. That is unrelated. End-to-end encryption means only the sender and recipient can read them."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "An unexpected email asks you to pay an invoice or share a document urgently. What is the most reliable way to check it before acting?",
            "options": [
                ("Confirm the request through a separate channel you already trust, such as a known phone number", True,
                 "Yes. Verifying on a channel the message did not provide is the one check an attacker cannot answer for you."),
                ("Reply to the email and ask if it is genuine", False,
                 "No. If it is a scam, you are asking the scammer. Verify a different way."),
                ("Check whether the email has the company logo", False,
                 "No. Logos are trivial to copy. Confirm the request on a separate trusted channel."),
                ("Act quickly, since it says it is urgent", False,
                 "No. Manufactured urgency is the trick. Slow down and verify on a channel you already trust."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "You need to send genuinely private information to a colleague. What is the safest habit?",
            "options": [
                ("Use a sealed channel, such as an encrypted message or a password-protected file with the password sent separately", True,
                 "Yes. Private information belongs in a sealed channel, so only the intended person can read it and the key travels separately."),
                ("Send it in a normal email, it is faster", False,
                 "No. Standard email is like a postcard. Private information deserves a sealed channel."),
                ("Put it in a text message", False,
                 "No. Ordinary SMS is not end-to-end encrypted and is easy to misaddress. Use a sealed channel."),
                ("Post it in a group chat so it is easy to find later", False,
                 "No. That widens who can see it. Private information should go through a sealed, controlled channel."),
            ],
        },
        # ---- Lesson 2: Sharing safely: files, links, and Wi-Fi ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why is standard email a poor choice for genuinely sensitive information?",
            "options": [
                ("It is more like a postcard: it passes through servers, sits in mailboxes, and is easily sent to the wrong person", True,
                 "Yes. Ordinary email is not a sealed vault. It is copied along the way, and one wrong click sends it to the wrong address."),
                ("It always deletes attachments after sending", False,
                 "No. Email does not delete your attachments. The problem is that it is exposed, like a postcard."),
                ("It cannot carry files at all", False,
                 "No. Email carries files fine. The issue is that it is not private or sealed."),
                ("It encrypts everything end to end by default", False,
                 "No. Standard email does not. That is exactly why it is a poor vault for sensitive data."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "You must email a password-protected sensitive file. How should you send the password?",
            "options": [
                ("By a separate channel, such as a phone call or text, not in the same email", True,
                 "Yes. If the password travels in the same email as the file, anyone who sees that email has both. Split them across channels."),
                ("In the same email, right under the attachment", False,
                 "No. Then the lock and the key travel together, which defeats the point."),
                ("In the email subject line", False,
                 "No. That is still the same message. Send the password a different way entirely."),
                ("You do not need to protect the password at all", False,
                 "No. The password is the key to the file. Send it separately, on another channel."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "On public Wi-Fi, what is an 'evil twin'?",
            "options": [
                ("A fake hotspot set up with a familiar name, so your traffic routes through the attacker", True,
                 "Yes. It mimics a trusted network's name. Connect to it and everything you send passes through the attacker."),
                ("A second phone that copies yours", False,
                 "No. An evil twin is a rogue Wi-Fi hotspot with a familiar name, not a cloned phone."),
                ("A virus that duplicates your files", False,
                 "No. That is not it. An evil twin is a fake Wi-Fi network used to intercept traffic."),
                ("A backup copy of a website", False,
                 "No. An evil twin is a rogue hotspot impersonating a trusted network."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You need to do some online banking while waiting at a cafe. What is the safest choice?",
            "options": [
                ("Use your phone's mobile data or a trusted VPN instead of the cafe Wi-Fi", True,
                 "Yes. Your own mobile data, or a VPN's encrypted tunnel, keeps the session private even on an untrusted network."),
                ("Use the open cafe Wi-Fi because it is quicker", False,
                 "No. An eavesdropper or an evil twin on open Wi-Fi could capture the session. Use mobile data or a VPN."),
                ("Wait until several people are also using the Wi-Fi", False,
                 "No. More users does not make an open network safe. Use mobile data or a trusted VPN."),
                ("Turn the screen brightness down so no one can read it", False,
                 "No. That does nothing about the network. Use your mobile data or a trusted VPN."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What does a VPN do for you on public Wi-Fi?",
            "options": [
                ("It wraps your traffic in encryption, so an eavesdropper on the network sees only scrambled data", True,
                 "Yes. A VPN builds an encrypted tunnel, so even on an untrusted network your traffic is unreadable to anyone watching."),
                ("It makes the Wi-Fi faster", False,
                 "No. A VPN is about privacy, not speed. It encrypts your traffic across the network."),
                ("It removes the need for any passwords", False,
                 "No. You still sign in to your accounts. A VPN encrypts the connection you use to reach them."),
                ("It blocks all viruses automatically", False,
                 "No. A VPN is not antivirus. It encrypts your traffic so it cannot be read in transit."),
            ],
        },
    ],
}
