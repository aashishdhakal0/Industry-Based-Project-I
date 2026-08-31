"""Module 4, Secure Communication Practices: understand it, then apply it.

  Lesson 1  UNDERSTAND IT  — a teaching lesson. Four reading panels, each with a
            real visual: what encryption means (sealed envelope vs postcard); the
            padlock and https, and what they do and do not prove, plus end-to-end
            encryption; sharing safely with permissioned links and keeping the key
            separate; and staying private on the move (open Wi-Fi, evil twins, and
            VPNs). One light comprehension check on an insecure send.
  Lesson 2  APPLY IT       — a practical lesson. Five hands-on tasks: sort
            encrypted vs open, judge safe shares from leaks, read a share-settings
            screen, work a real share decision, and harden a mobile workspace.

Voice: warm, plain Australian English, no em-dashes, no emoji. Grounded in ACSC
(cyber.gov.au) guidance on secure communication, protecting information, and
public Wi-Fi. Points sum to 10 per lesson and bank at lesson end.
"""

LESSONS = [
    {
        "title": "What 'secure' really means",
        "reading_time_minutes": 9,
        "intro": "Most days you send information without a second thought. This "
        "lesson gives you the ideas behind a safer habit: what encryption actually "
        "does, what the padlock does and does not promise, how to share a file "
        "without losing control of it, and how to stay private on someone else's "
        "network.",
        "tasks": [
            {
                "key": "encryption",
                "kind": "concept",
                "points": 2,
                "title": "Encryption: a sealed envelope, not a postcard",
                "diagram": "msg-encrypted",
                "body": "<p>To <strong>encrypt</strong> information is to scramble it "
                "using a <strong>key</strong>, so that only someone with the matching "
                "key can turn it back into something readable. The readable version "
                "is called <em>plaintext</em>; the scrambled version is "
                "<em>ciphertext</em>. To anyone without the key, the ciphertext is "
                "just noise, and modern encryption is strong enough that guessing the "
                "key is not realistically possible. The picture above shows the same "
                "patient record sent two ways.</p>"
                "<ul>"
                "<li><strong>Out in the open</strong>: the plain version is readable "
                "by anyone who can see the traffic along the way, like a postcard a "
                "stranger can read over your shoulder. Ordinary email between servers "
                "and standard SMS often travel like this.</li>"
                "<li><strong>Encrypted</strong>: the scrambled version is useless "
                "without the key, like a sealed envelope. Someone can still see that "
                "a message was sent, and to whom, but not what it says.</li>"
                "</ul>"
                "<p>So be clear on what encryption does and does not do. It does not "
                "hide that you sent something, it does not delete or back anything up, "
                "and it does not protect a message once it is opened and sitting on a "
                "screen. It does one job, extremely well: it makes the contents "
                "unreadable to everyone except the intended reader while they are in "
                "transit or storage.</p>"
                "<div class=\"cy-callout\">The question to carry into every send: is "
                "this going as a sealed envelope, or a postcard anyone along the way "
                "can read?</div>",
            },
            {
                "key": "padlock-and-e2e",
                "kind": "concept",
                "points": 2,
                "title": "The padlock, https, and end-to-end",
                "diagram": "secure-bars",
                "body": "<p>The padlock and <strong>https</strong> in the address "
                "bar mean the connection between your browser and that website is "
                "encrypted, using a technology called TLS. When you connect, your "
                "browser and the site agree on a shared key and scramble everything "
                "that passes between them, so someone watching the network sees only "
                "ciphertext. The two address bars above show the difference: plain "
                "<strong>http</strong> with no padlock is open and readable; "
                "<strong>https</strong> with a padlock is encrypted in transit.</p>"
                "<p>But here is the catch that catches people out: the padlock says "
                "nothing about <em>who runs the site</em>. Anyone can get the "
                "certificate that turns on https, including a criminal running a "
                "convincing fake, in minutes and for free. The padlock tells you the "
                "line is private, not that the person on the other end is honest. "
                "That is why a padlock on a login page you reached from an email link "
                "is no reassurance at all.</p>"
                "<p><strong>End-to-end encryption</strong> goes one step further. On "
                "an ordinary website, the company at the far end can read your data "
                "once it arrives. In an end-to-end encrypted app (used by the "
                "well-known secure messaging apps), the message is scrambled on your "
                "device and only unscrambled on the recipient's, so not even the "
                "service carrying it can read the contents. Only the two ends hold the "
                "key.</p>"
                "<div class=\"cy-callout\">The padlock means the connection is sealed. "
                "It is not a badge of trust: still check who you are actually dealing "
                "with.</div>",
            },
            {
                "key": "sharing-safely",
                "kind": "concept",
                "points": 2,
                "title": "Sharing safely: keep control, keep the key separate",
                "diagram": "secure-share",
                "body": "<p>Sending a file is easy; keeping control of it is the "
                "skill. Once a loose copy leaves your hands, in a plain attachment or "
                "a public link, you can never pull it back. The share settings above "
                "show the two ends of the spectrum.</p>"
                "<ul>"
                "<li><strong>A public 'anyone with the link' share</strong>: no "
                "sign-in, never expires, and can be forwarded to anyone. Convenient, "
                "and completely out of your control the moment it is passed on.</li>"
                "<li><strong>A permissioned link</strong>: restricted to named "
                "people, password protected, expires, and can be revoked. You decide "
                "who gets in, and you can take access back.</li>"
                "</ul>"
                "<p>Two habits make sharing safe. Give the <strong>least access</strong> "
                "needed (view-only beats edit; one folder beats the whole drive), so "
                "a shared link can never do more than the job requires. And when you "
                "send a password-protected file, send the <strong>password by a "
                "separate channel</strong>: the file by email, the password by a text "
                "or a quick call. If the lock and the key travel together in the same "
                "message, anyone who intercepts or is forwarded that message has "
                "both, and the protection was for nothing.</p>"
                "<div class=\"cy-callout\">Before you share, ask: who can open this, "
                "and can I take that access back later? If the answer is 'anyone' and "
                "'no', it is a leak.</div>",
            },
            {
                "key": "on-the-move",
                "kind": "concept",
                "points": 2,
                "title": "Staying private on someone else's network",
                "hero": "eavesdrop",
                "diagram": "vpn-tunnel",
                "body": "<p>Working from a cafe, an airport, or a hotel is normal now, "
                "and so are the risks. Public Wi-Fi is a shared space, and two traps "
                "stand out.</p>"
                "<ul>"
                "<li><strong>Open networks</strong> carry your traffic unencrypted "
                "unless the site itself is https. A stranger on the same network, "
                "using free and legal tools, can capture what everyone around them "
                "sends. Anything not on https, and the fact of which sites you "
                "visit, is readable.</li>"
                "<li><strong>Evil twins</strong>: an attacker sets up their own "
                "hotspot with a familiar name, like 'Corner Cafe Free WiFi', so you "
                "connect to them by mistake. Now they are the network: everything you "
                "send passes through their equipment first. A friendly name and a "
                "strong signal prove nothing, because both are trivial to fake.</li>"
                "</ul>"
                "<p>The fix is to stop trusting the network at all. Use your phone's "
                "<strong>mobile data</strong>, which is encrypted and yours, or a "
                "<strong>VPN</strong>. As the animation above shows, a VPN builds an "
                "encrypted tunnel from your device to a trusted server, so even on an "
                "untrusted Wi-Fi, and even against an evil twin, an eavesdropper sees "
                "only scrambled traffic. And lock your screen whenever you step away: "
                "an unlocked laptop in a public place is an open door to every account "
                "you are signed into.</p>"
                "<div class=\"cy-callout\">Away from the office, assume the network is "
                "watching. Use your own connection or a VPN, and lock the screen when "
                "you leave it.</div>",
            },
            {
                "key": "read-the-send",
                "kind": "check",
                "points": 2,
                "title": "Quick check: about to send the form",
                "diagram": "scene-send",
                "body": "<p>One quick check to finish. In the scene above, a worker "
                "is about to email a client's medical form as a plain attachment, to "
                "a personal Gmail address, and a colleague has noticed. You now know "
                "what 'sealed' means and what plain email is. What should happen "
                "next?</p>"
                "<div class=\"cy-callout\">Match the care to the sensitivity: private "
                "health data needs a sealed channel, not whatever is quickest.</div>",
                "question": "Looking at the scene, what should the worker do before sending the client's medical form?",
                "hint": "Weigh how sensitive the file is against how exposed plain email to a personal address is.",
                "options": [
                    ("Stop, and send it through a secure channel, or a password-protected file with the password sent separately", True,
                     "Right. A medical form is exactly the kind of private data that needs a sealed channel, so only the intended person can open it, and one wrong address is not a breach."),
                    ("Send it, plain email is quicker and the colleague is waiting", False,
                     "No. Plain email is a postcard, and one wrong address is a breach. Speed does not change how sensitive the file is."),
                    ("Send it, but CC a manager so someone else has a copy", False,
                     "No. That just exposes the private file to more inboxes. Use a sealed, access-controlled channel instead."),
                    ("Paste the details into the body of the email instead of attaching them", False,
                     "No. The email body is just as exposed as an attachment. The fix is a sealed channel, not a different part of the email."),
                ],
            },
        ],
    },
    {
        "title": "Put it to work: sharing safely, files, links, and Wi-Fi",
        "reading_time_minutes": 9,
        "intro": "Now use it. Sort what is sealed from what is open, tell a safe "
        "share from a leak, read a real share-settings screen, make a live sharing "
        "decision, and harden a workspace for life on the move.",
        "tasks": [
            {
                "key": "encrypted-or-open",
                "kind": "sort",
                "points": 2,
                "title": "Encrypted, or out in the open?",
                "body": "<p>Lesson 1 drew the line between a sealed envelope and a "
                "postcard. Prove you can place any everyday channel on the right side "
                "of it. Read each item and sort it: encrypted (only the right person "
                "can read it) or out in the open (others along the way could).</p>"
                "<div class=\"cy-callout\">Ask of each one: if a stranger watched the "
                "traffic, would they see the contents, or only scrambled "
                "characters?</div>",
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
                "key": "safe-share-or-leak",
                "kind": "classify",
                "points": 2,
                "title": "Safe share, or a leak?",
                "body": "<p>The quick share option is often the leaky one. A "
                "permissioned link, restricted to named people and revocable, keeps "
                "you in control. A public share, or a copy emailed around, does not. "
                "Read each share and decide.</p>"
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
                "key": "read-share-link",
                "kind": "check",
                "points": 2,
                "title": "Read the share settings",
                "diagram": "secure-share",
                "body": "<p>A picture-question, straight from Lesson 1. The same file "
                "can be shared two ways, and the settings screen tells you which is "
                "safe. One link lets anyone in and never expires; the other is "
                "restricted, password protected and revocable. Read the two and "
                "decide which keeps you in control.</p>"
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
                "key": "link-or-attachment",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: secure link, or email attachment?",
                "body": "<p>A real sharing decision, start to finish. A colleague at "
                "another office needs a client's file. The choice you make about how "
                "to share it decides who can reach it, and whether you can ever take "
                "it back. Work through it.</p>"
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
                "key": "harden-workspace",
                "kind": "harden",
                "points": 2,
                "title": "Secure the workspace before you leave",
                "diagram": "wifi-evil-twin",
                "body": "<p>The final drill puts life on the move to work. The Wi-Fi "
                "picker above shows a classic trap: two near-identical open networks, "
                "one of which may be an <strong>evil twin</strong> set up to watch "
                "your traffic. Secure each part of your mobile setup.</p>"
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
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: understand it (what 'secure' means) ----
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
            "lesson": 1, "difficulty": "MEDIUM",
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
        # ---- Lesson 2: apply it (sharing safely) ----
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
            "text": "A colleague needs a client's file. What is the safest way to share it?",
            "options": [
                ("A link restricted to them, view-only, that expires and can be revoked", True,
                 "Yes. A permissioned link keeps you in control of who can open it and lets you take access back later."),
                ("Email the whole file as an attachment so they have their own copy", False,
                 "No. A loose copy can be forwarded anywhere and never recalled. Share a controlled link instead."),
                ("Post a public 'anyone with the link' share in the team chat", False,
                 "No. Anyone who sees or forwards that link can open the file. That is a leak."),
                ("Give them full edit access to the whole drive to save time", False,
                 "No. That hands over far more than needed. Give the least access required, with an expiry."),
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
    ],
}
