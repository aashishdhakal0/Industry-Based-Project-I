"""Module 4, Secure Communication Practices: understand it, then apply it.

  Lesson 1  UNDERSTAND IT, a teaching lesson. Four reading panels, each with a
            real visual: what encryption means (sealed envelope vs postcard); the
            padlock and https, and what they do and do not prove, plus end-to-end
            encryption; sharing safely with permissioned links and keeping the key
            separate; and staying private on the move (open Wi-Fi, evil twins, and
            VPNs). One light comprehension check on an insecure send.
  Lesson 2  APPLY IT, hands-on artefacts drawn from settings panels, toggles and
            modal overlays, distinct from Modules 1-2's desktop consoles and
            Module 3's phone apps: sort a week's real activity log (SORT), read
            a browser's connection-details panel and find what a padlock does
            not prove (NETMAP), fix a leaky share on a floating Drive-style
            dialog (HARDEN), order your moves past an evil-twin Wi-Fi picker
            (SEQUENCE), and work a live privacy-law incident when a stale share
            link is found by a search engine (TABLETOP).

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
                "diagram": "encryption",
                "title": "Encryption: a sealed envelope, not a postcard",
                "body": "<p>To <strong>encrypt</strong> information is to scramble it "
                "using a <strong>key</strong>, so that only someone with the matching "
                "key can turn it back into something readable. The readable version "
                "is called <em>plaintext</em>; the scrambled version is "
                "<em>ciphertext</em>. To anyone without the key, the ciphertext is "
                "just noise, and modern encryption is strong enough that guessing the "
                "key is not realistically possible. The same message can be sent two "
                "ways.</p>"
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
                "diagram": "msg-encrypted",
                "body": "<p>The padlock and <strong>https</strong> in the address "
                "bar mean the connection between your browser and that website is "
                "encrypted, using a technology called TLS. When you connect, your "
                "browser and the site agree on a shared key and scramble everything "
                "that passes between them, so someone watching the network sees only "
                "ciphertext. In the address bar you see the difference: plain "
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
                "diagram": "secure-share",
                "title": "Sharing safely: keep control, keep the key separate",
                "body": "<p>Sending a file is easy; keeping control of it is the "
                "skill. Once a loose copy leaves your hands, in a plain attachment or "
                "a public link, you can never pull it back. There are two ends of the "
                "spectrum.</p>"
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
                "diagram": "wifi-evil-twin",
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
                "<strong>VPN</strong>. A VPN builds an "
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
                "key": "read-the-compose",
                "kind": "check",
                "points": 2,
                "title": "Quick check: about to hit send",
                "diagram": "compose-send",
                "body": "<p>One quick check to finish. The compose window above is "
                "ready to go: a client's passport scan, attached as a plain file, "
                "addressed to a personal Gmail account, with Send one click away. You "
                "now know what 'sealed' means and what plain email is. Read the "
                "window, then answer.</p>"
                "<div class=\"cy-callout\">Match the care to the sensitivity: a "
                "passport scan needs a sealed channel, not whatever is quickest.</div>",
                "question": "Looking at this compose window, what should happen before Send is clicked?",
                "hint": "Weigh how sensitive the attachment is against how exposed a plain email to a personal address really is.",
                "options": [
                    ("Stop, and send it through a secure channel, or as a password-protected file with the password sent separately, to the client's verified address", True,
                     "Right. A passport scan is exactly the kind of private data that needs a sealed channel, so only the intended person can open it, and one wrong address is not a breach. The personal Gmail address is a second warning sign."),
                    ("Just click Send, plain email is quicker and everyone uses it", False,
                     "No. Plain email is a postcard, and one wrong address is a breach. Speed does not change how sensitive the file is."),
                    ("Click Send, but CC the principal so someone else has a copy", False,
                     "No. That just exposes the private file to more inboxes. Use a sealed, access-controlled channel instead."),
                    ("Paste the passport details into the body of the email instead of attaching the file", False,
                     "No. The email body is just as exposed as an attachment. The fix is a sealed channel, not a different part of the email."),
                ],
            },
        ],
    },
    {
        "title": "Put it to work: sharing safely, files, links, and Wi-Fi",
        "reading_time_minutes": 9,
        "intro": "Now use it at Coburg Migration & Legal, a small practice that "
        "handles passports, visa applications and police checks all day. Principal "
        "Farah Haddad, paralegal Owen Tran and admin Steph Corrigan send sensitive "
        "client documents between the office and the road constantly. Sort what is "
        "sealed from what is open, read what a padlock actually proves, fix a leaky "
        "share, order your moves at a departure gate, and work a live privacy "
        "incident.",
        "tasks": [
            {
                "key": "sealed-or-postcard",
                "kind": "sort",
                "points": 2,
                "title": "Sealed, or a postcard?",
                "body": "<p>Lesson 1 drew the line between a sealed envelope and a "
                "postcard. Below is this week's activity log at the practice, six "
                "things that actually went out. Read each and sort it: encrypted "
                "(only the right person can read it) or out in the open (others "
                "along the way could).</p>"
                "<div class=\"cy-callout\">Ask of each one: if a stranger watched "
                "the traffic, would they see the contents, or only scrambled "
                "characters?</div>",
                "payload": {
                    "prompt": "Tap an item, then tap whether it is Encrypted or Out in the open. Sort all six to finish.",
                    "heading": "Sent & shared this week",
                    "frame": {
                        "tab": "Activity log · Coburg Migration & Legal", "fav": "C", "favbg": "#5f6368",
                        "url_prefix": "https://", "url": "portal.coburgmigrationlegal.com.au", "url_bold": "/activity",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "buckets": [
                        {"id": "enc", "label": "Encrypted"},
                        {"id": "open", "label": "Out in the open"},
                    ],
                    "items": [
                        {"text": "Owen texts a boarding pass QR code via standard SMS to a partner picking someone up from the airport", "bucket": "open",
                         "why": "Out in the open. Standard SMS is not end-to-end encrypted, a poor choice even for something this ordinary."},
                        {"text": "Steph photographs a new starter's tax file number and sends it as an MMS to the bookkeeper", "bucket": "open",
                         "why": "Out in the open. MMS travels the same way as SMS: not end-to-end encrypted."},
                        {"text": "Farah video-calls a client through Signal to talk through their visa application", "bucket": "enc",
                         "why": "Encrypted. Signal calls are end-to-end encrypted between the two devices."},
                        {"text": "Steph emails the weekly staff roster as a plain PDF to everyone's personal address", "bucket": "open",
                         "why": "Out in the open. Standard email is a postcard, whatever the content. It passes through servers along the way."},
                        {"text": "A signed court order is uploaded to the firm's cloud drive over the office's WPA3 Wi-Fi, padlock showing", "bucket": "enc",
                         "why": "Encrypted at the Wi-Fi layer and in transit to the site. Two layers, not one."},
                        {"text": "A client's appointment reference is confirmed over an encrypted VoIP call on the firm's Teams line", "bucket": "enc",
                         "why": "Encrypted. The call itself is encrypted in transit, unlike a plain phone line or a text."},
                    ],
                },
            },
            {
                "key": "read-connection-panel",
                "kind": "netmap",
                "points": 2,
                "title": "Read the connection panel",
                "body": "<p>Lesson 1 warned you: the padlock proves the connection "
                "is private, not that the person on the other end is honest. Owen "
                "followed a link from an email and landed here to sign in, padlock "
                "showing. Here is that real browser's connection details panel. "
                "Two of the five fields below are the actual problem. Find them.</p>"
                "<div class=\"cy-callout\">Encrypted, and a valid certificate, are "
                "both genuinely true here. Neither one tells you who you are "
                "actually dealing with.</div>",
                "payload": {
                    "prompt": "Tap every field that is a genuine red flag. Find both to finish.",
                    "heading": "Connection details",
                    "lede": "Everything this browser can tell you about the page you're on.",
                    "frame": {
                        "tab": "Sign in · Coburg Migration & Legal", "fav": "C", "favbg": "#1a73e8",
                        "url_prefix": "https://", "url": "migration-legal-secure-check.com", "url_bold": "/portal",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "nodes": [
                        {"label": "Connection: Encrypted (TLS 1.3)", "detail": "the technical link between you and this page", "weak": False,
                         "why": "Genuine: the traffic between your browser and this site is scrambled. But encrypted does not mean honest."},
                        {"label": "Certificate: Valid, issued by Let's Encrypt", "detail": "proof someone controls this domain", "weak": False,
                         "why": "A valid certificate just proves someone controls this domain, for a moment. Anyone, including a scammer, can get one free in minutes."},
                        {"label": "Address: migration-legal-secure-check.com", "detail": "the domain you are actually on", "weak": True,
                         "why": "Not the firm's real domain (coburgmigrationlegal.com.au). A valid padlock on a lookalike address is exactly how a phishing page earns its trust badge."},
                        {"label": "Site identity: Not verified as an organisation", "detail": "whether a real business has been confirmed", "weak": True,
                         "why": "No one has confirmed which real business runs this site. The padlock alone never tells you that."},
                        {"label": "Cookies and site data: 3 trackers active", "detail": "ordinary site tracking", "weak": False,
                         "why": "Ordinary, and unrelated to whether the site is trustworthy. Trackers exist on plenty of legitimate sites too."},
                    ],
                },
            },
            {
                "key": "fix-share-settings",
                "kind": "harden",
                "points": 2,
                "title": "Fix the share settings",
                "body": "<p>Lesson 1 covered permissioned links, least access, and "
                "keeping the password separate from the file. Owen set up this "
                "share for a client's visa documents in a hurry, four settings "
                "wrong. Fix each one and watch it flip to Fixed.</p>"
                "<div class=\"cy-callout\">Pick the option that actually closes the "
                "gap, not the one that is merely more convenient.</div>",
                "payload": {
                    "prompt": "Fix each setting on this share. Lock down all four to finish.",
                    "variant": "sharemodal",
                    "heading": "Share \"Nguyen_visa_docs.pdf\"",
                    "file": "Nguyen_visa_docs.pdf · 4.2 MB",
                    "steps": [
                        {"label": "General access", "value": "Anyone with the link",
                         "risk": "Anyone who ever sees this link, forwarded or not, can open it.",
                         "options": [
                            {"text": "Change to Restricted, and add only the named client", "correct": True,
                             "why": "Right. Restricted access means only the person you named can open it, and you keep control of who that is."},
                            {"text": "Leave it as Anyone with the link, but set it to view-only", "correct": False,
                             "why": "Still leaky. Anyone with the link can still open it, whatever their role. Restrict who can reach it at all."},
                            {"text": "Leave it, it's just a link, unlikely anyone finds it", "correct": False,
                             "why": "A link is not a secret. Once shared once, you cannot control where it travels. Restrict it properly."},
                         ]},
                        {"label": "Role", "value": "Editor",
                         "risk": "An editor can change or delete the file, not just read it.",
                         "options": [
                            {"text": "Change the role to Viewer", "correct": True,
                             "why": "Right. A client reviewing their own documents needs to read them, not change them. Give the least access that does the job."},
                            {"text": "Leave it as Editor, they might need to fill in a field", "correct": False,
                             "why": "Give access based on what the job actually needs, not what might possibly help. Viewer is enough here."},
                            {"text": "Change it to Commenter instead", "correct": False,
                             "why": "Better than Editor, but still more than a client reviewing their own file needs. Viewer is the least-access choice."},
                         ]},
                        {"label": "Link expiry", "value": "Never expires",
                         "risk": "A link with no expiry is a standing risk that outlives the reason it was created.",
                         "options": [
                            {"text": "Set the link to expire in 7 days", "correct": True,
                             "why": "Right. A short, deliberate expiry means the share does its job and then closes itself, no cleanup required later."},
                            {"text": "Leave it as Never expires, easier to remember", "correct": False,
                             "why": "Convenient for you, but it leaves the door open indefinitely. Set a real expiry."},
                            {"text": "Set it to expire in 1 year", "correct": False,
                             "why": "Still far longer than this share needs to exist. Match the expiry to the actual task, a matter of days."},
                         ]},
                        {"label": "Note to recipient", "value": "Password: Nguyen2024!",
                         "risk": "The lock and the key are travelling in the same message. Anyone who sees this share has both.",
                         "options": [
                            {"text": "Remove the password from the note and send it by phone instead", "correct": True,
                             "why": "Right. Sending the password on a separate channel means intercepting or forwarding this message alone is not enough to open the file."},
                            {"text": "Leave the password in the note, it's convenient", "correct": False,
                             "why": "Convenient for whoever intercepts it too. Split the file and the password across two channels."},
                            {"text": "Just make the password longer", "correct": False,
                             "why": "A longer password sitting right next to the file does not fix the real problem: they are travelling together."},
                         ]},
                    ],
                },
            },
            {
                "key": "departure-gate",
                "kind": "sequence",
                "points": 2,
                "title": "Order your move at the departure gate",
                "diagram": "wifi-picker-evil-twin",
                "body": "<p>Lesson 1 covered open networks, evil twins, VPNs and "
                "locking your screen. Steph is at the departure gate on the way "
                "to a conference. The Wi-Fi picker above shows the classic trap: "
                "two near-identical network names, sitting side by side. Put the "
                "right response in order.</p>"
                "<div class=\"cy-callout\">Each step depends on the one before it. "
                "Get the order right and nothing is left exposed.</div>",
                "payload": {
                    "prompt": "Tap the steps in the order you would actually take them. Place all five to finish.",
                    "steps": [
                        {"label": "Notice the two near-identical Wi-Fi names and don't join either yet.", "order": 1,
                         "detail": "A near-identical name, both open, is exactly how an evil twin hides in plain sight."},
                        {"label": "Switch to your phone's hotspot, or turn on the firm's VPN.", "order": 2,
                         "detail": "Off the untrusted network entirely, or wrapped in an encrypted tunnel if you must use it."},
                        {"label": "Only start the sensitive work once you're on a connection you trust.", "order": 3,
                         "detail": "Sensitive work waits for a trustworthy connection, not the other way around."},
                        {"label": "Lock the screen the moment you step away to board.", "order": 4,
                         "detail": "An unlocked laptop at a gate is an open door to every account you're signed into."},
                        {"label": "Report the lookalike network name once you're safely on board.", "order": 5,
                         "detail": "A quick report helps the next traveller avoid the same trap."},
                    ],
                },
            },
            {
                "key": "the-leaked-file",
                "kind": "tabletop",
                "points": 2,
                "title": "The leaked file",
                "body": "<p>Last one, and it pulls sharing and the law together. "
                "Work the incident live. The board tracks the state of the "
                "practice as you act.</p>"
                "<div class=\"cy-callout\">Contain it, find out who actually saw "
                "it, then meet your obligations. In that order.</div>",
                "payload": {
                    "prompt": "Work the incident phase by phase. The board updates with each call.",
                    "scenario": "Farah discovers that a batch of client passport scans, shared by Steph months ago as 'anyone with the link' and never revoked, has been indexed by a search engine and is now publicly findable by anyone who searches the right terms.",
                    "board": [
                        {"id": "link", "label": "Link status", "state": "bad", "value": "Public & indexed"},
                        {"id": "clients", "label": "Client trust", "state": "warn", "value": "Not yet told"},
                        {"id": "duty", "label": "Privacy duty", "state": "warn", "value": "Not yet assessed"},
                    ],
                    "stages": [
                        {"phase": "Contain", "title": "The link is still live",
                         "prompt": "The scans are still publicly reachable right now. What is the first move?",
                         "options": [
                            {"label": "Revoke the link immediately and request the pages be removed from the search index", "outcome": "good",
                             "consequence": "Right. Revoking stops any new access, and a removal request clears the cached, indexed copy so it stops turning up in search.", "board": {"link": {"state": "ok", "value": "Revoked, removal requested"}}},
                            {"label": "Just delete the shared folder", "outcome": "bad",
                             "consequence": "Deleting the folder does not clear the search engine's own cached copy. The scans can still turn up in results.", "board": {"link": {"state": "bad", "value": "Still indexed"}}},
                            {"label": "Wait and see if anyone actually finds it", "outcome": "bad",
                             "consequence": "Every day it stays indexed is another day it can be found. Contain it now, do not wait.", "board": {"link": {"state": "bad", "value": "Still public"}}},
                         ]},
                        {"phase": "Assess", "title": "Who actually saw it",
                         "prompt": "The link is down. Before anything else, what do you need to know?",
                         "options": [
                            {"label": "Check the access logs to see who actually viewed the files while the link was public", "outcome": "good",
                             "consequence": "Right. The logs tell you the real scope, not a guess, which is exactly what a proper assessment needs.", "board": {"clients": {"state": "warn", "value": "Scope confirmed"}}},
                            {"label": "Assume no one saw it since nobody has complained", "outcome": "bad",
                             "consequence": "No complaint is not the same as no access. Check the logs before you assume anything.", "board": {"clients": {"state": "bad", "value": "Unknown scope"}}},
                         ]},
                        {"phase": "Notify", "title": "Meeting the obligation",
                         "prompt": "The logs show the files were viewed a number of times by unknown visitors. What now?",
                         "options": [
                            {"label": "Assess it under the Privacy Act's Notifiable Data Breaches scheme, and tell the affected clients and the OAIC if serious harm is likely", "outcome": "good",
                             "consequence": "Right. Passport scans exposed to unknown viewers is exactly the kind of serious harm the scheme exists for. A proper assessment and honest notification is the law, and it rebuilds trust.", "board": {"duty": {"state": "ok", "value": "Assessed & notified"}, "clients": {"state": "ok", "value": "Told directly"}}},
                            {"label": "Stay quiet now that the link is fixed", "outcome": "bad",
                             "consequence": "The exposure already happened. Staying quiet can itself breach the law, and clients find out anyway, just later and worse.", "board": {"duty": {"state": "bad", "value": "Unreported"}}},
                            {"label": "Mention it quietly to the principal partner only, no formal assessment", "outcome": "bad",
                             "consequence": "A private word is not an assessment, and it leaves the actual legal obligation unmet.", "board": {"duty": {"state": "bad", "value": "Not assessed"}}},
                         ]},
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
