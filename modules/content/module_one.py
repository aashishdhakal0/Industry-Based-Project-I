"""Module 1, Network Security Fundamentals: the gold-standard reference content.

This is the module every other module copies, so the shape matters as much as the
words. Kept as plain data (not schema) so it reads like teaching material and the
seed stays re-runnable.

Room format (TryHackMe-style): a lesson is 4 to 8 collapsible task PANELS. Each
panel is a meaty chunk of learning: substantial reading (paragraphs, a diagram,
an optional callout box) THEN one inline interactive at the bottom, either a
check (a question with instant feedback and a hint) or a hands-on activity. The
panels' points sum to 10 and bank at lesson end.

House voice for here and Modules 2 to 6: warm, confident, human. Plain Australian
English for non-technical readers. Every idea ties to why it matters to you and
what to do. Concrete local scenarios. No em-dashes, no filler.
"""

# --------------------------------------------------------------------------
# Lessons. Each task is a panel: title + rich `body` (reading, may include a
# `<div class="cy-callout">` box) + one interactive. Check option tuples are
# (text, is_correct, explanation); each check carries a `hint`. Activity config
# lives in `payload`. Points per lesson sum to 10.
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network is, and what you protect",
        "reading_time_minutes": 6,
        "intro": "Meet the thing you are protecting, see how your information "
        "moves, and learn the three questions security keeps coming back to.",
        "tasks": [
            {
                "key": "net-basics",
                "kind": "check",
                "points": 3,
                "title": "What a network actually is",
                "diagram": "data-travels",
                "body": "<p>A network is just devices talking to each other. Your "
                "laptop, the front desk printer, the eftpos machine: they all pass "
                "information back and forth through your router and out to the "
                "internet.</p>"
                "<p>Most of that information does not sit still. It is <em>in "
                "transit</em>, moving from one place to another, which is exactly "
                "when it can be intercepted if it is not looked after. Some is <em>"
                "at rest</em>, saved on a device or a server, and some is <em>in "
                "use</em>, open on a screen in front of someone. Good security "
                "looks after all three.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "you do not need to run the network to help keep it safe. Knowing "
                "your information is constantly on the move is the first step to "
                "protecting it.</div>",
                "question": "Which of these is actually a network?",
                "hint": "Look for the option that means devices are joined together to share.",
                "options": [
                    ("A few devices connected so they can share information", True,
                     "Spot on. From two machines to the whole internet, a network is devices connected to share information."),
                    ("One powerful computer sitting on its own", False,
                     "Not quite. On its own it is just a computer. What makes a network is the connection between devices."),
                    ("The antivirus app on your laptop", False,
                     "That is a tool that protects a single device. It is not the network itself."),
                    ("Your office Wi-Fi password", False,
                     "That is how you join the network, not the network itself."),
                ],
            },
            {
                "key": "cia-triad",
                "kind": "sort",
                "points": 3,
                "title": "The three questions security asks",
                "diagram": "cia-triad",
                "body": "<p>Almost every security decision comes back to three "
                "simple questions, known as the CIA triad. Nothing to do with "
                "spies. Confidentiality asks whether only the right people can see "
                "the information. Integrity asks whether it is still accurate and "
                "has not been tampered with. Availability asks whether it is there "
                "when you need it.</p>"
                "<p>Picture a small dental clinic on a Monday. A patient list "
                "emailed to the wrong address is a confidentiality slip. An invoice "
                "with the bank details swapped is an integrity problem. Files "
                "locked by ransomware before the day even starts is an availability "
                "disaster. Same office, three very different bad days.</p>"
                "<div class=\"cy-callout\">Every control in this module protects one "
                "of these three. When you are unsure about a risk, ask which pillar "
                "it threatens and the sensible response usually becomes obvious.</div>",
                "payload": {
                    "prompt": "Tap a situation, then tap the pillar it puts at "
                    "risk. Get all eight and you have got the idea.",
                    "buckets": [
                        {"id": "c", "label": "Confidentiality"},
                        {"id": "i", "label": "Integrity"},
                        {"id": "a", "label": "Availability"},
                    ],
                    "items": [
                        {"id": "list", "text": "A customer list is emailed to the wrong person",
                         "bucket": "c", "why": "A stranger can now read it. That is confidentiality."},
                        {"id": "invoice", "text": "An invoice's bank details are secretly changed",
                         "bucket": "i", "why": "The details were altered behind your back. That is integrity."},
                        {"id": "ransom", "text": "Ransomware locks all your files",
                         "bucket": "a", "why": "You cannot get to your own files. That is availability."},
                        {"id": "sticky", "text": "A password is left on a sticky note on the monitor",
                         "bucket": "c", "why": "Anyone walking past can see it. That is confidentiality."},
                        {"id": "backup", "text": "A tested backup lets you restore after a crash",
                         "bucket": "a", "why": "You can get your work back, so it stays available."},
                        {"id": "totals", "text": "A tampered spreadsheet shows the wrong totals",
                         "bucket": "i", "why": "The numbers were quietly changed. That is integrity."},
                        {"id": "shoulder", "text": "A stranger reads your screen over your shoulder",
                         "bucket": "c", "why": "Someone sees what they should not. That is confidentiality."},
                        {"id": "outage", "text": "The website is knocked offline during a sale",
                         "bucket": "a", "why": "Customers cannot reach you. That is availability."},
                    ],
                },
            },
            {
                "key": "pillar-fails",
                "kind": "check",
                "points": 2,
                "title": "When a pillar fails",
                "body": "<p>The three pillars are easiest to understand through "
                "what goes wrong. Confidentiality fails when information reaches the "
                "wrong eyes: a misdirected email, a password on a sticky note, a "
                "stranger reading your screen. Integrity fails when information is "
                "changed without permission: altered invoice details, a tampered "
                "spreadsheet. Availability fails when you cannot reach your own "
                "information: a ransomware lockout, a website knocked offline.</p>"
                "<p>Notice that a single event can look fine on the surface while a "
                "pillar has quietly failed. A tampered invoice still opens "
                "perfectly. That is what makes integrity attacks so effective, and "
                "why verifying important changes matters so much.</p>",
                "question": "Ransomware locks your files on the morning of a big deadline. Which pillar took the hit?",
                "hint": "Ask yourself: can the right people still get to the information when they need it?",
                "options": [
                    ("Availability", True,
                     "Yes. The files still exist, you just cannot reach them, and that is exactly what availability protects."),
                    ("Confidentiality", False,
                     "Not this time. Nobody has necessarily seen the files. The problem is that you cannot get to them."),
                    ("Integrity", False,
                     "Close, but the files were not altered, they were locked away. That is availability."),
                    ("None of them", False,
                     "It is very much a security problem. Being locked out of your own work is an availability failure."),
                ],
            },
            {
                "key": "cia-recap",
                "kind": "check",
                "points": 2,
                "title": "Bringing it together",
                "body": "<p>You now have the foundation: a network is connected "
                "devices sharing information, that information is usually on the "
                "move, and security is about protecting its confidentiality, "
                "integrity and availability. Everything in the rest of this module "
                "is a practical way to defend one of those three.</p>"
                "<p>Keep the triad in your back pocket. It turns vague worry into a "
                "clear question, and a clear question is halfway to the right "
                "answer.</p>",
                "question": "A backup you have tested and can actually restore mainly protects which pillar?",
                "hint": "A backup does not hide your files or prove they are unchanged. What does it guarantee you can still do?",
                "options": [
                    ("Availability", True,
                     "Yes. A backup means an attack or a mistake does not cost you access to your work."),
                    ("Confidentiality", False,
                     "No. A backup does not hide anything. It makes sure you can get your data back."),
                    ("Integrity", False,
                     "Not the main point. Backups are chiefly about restoring access, which is availability."),
                    ("It is not a security control", False,
                     "It is a core one. It protects availability against ransomware and honest mistakes alike."),
                ],
            },
        ],
    },
    {
        "title": "How attacks actually happen",
        "reading_time_minutes": 7,
        "intro": "The real ways in are fewer than you would think. Learn them, "
        "then inspect a scam yourself and tell a genuine message from a fake.",
        "tasks": [
            {
                "key": "vectors",
                "kind": "check",
                "points": 2,
                "title": "The common ways in",
                "body": "<p>Attackers are rarely magicians. They walk through doors "
                "people leave open. The common ways in are few and well understood: "
                "a convincing fake message (phishing), a weak or reused password, "
                "software that has not been updated, and harmful software called "
                "malware, of which ransomware is the one that ruins weeks.</p>"
                "<p>What ties them together is that almost all of them need a person "
                "to have a busy moment. That is good news, because it means the fix "
                "is usually a small human habit rather than an expensive gadget.</p>",
                "question": "What is phishing, in plain terms?",
                "hint": "The word sounds like fishing. Think about what they are fishing for, and how.",
                "options": [
                    ("A message that pretends to be someone you trust, to trick you into clicking or sharing details", True,
                     "Exactly. It leans on trust, and it is the most common way Australian organisations get caught out."),
                    ("A faster way to connect to the internet", False,
                     "No, that is nothing to do with it. Phishing is a con, not a connection."),
                    ("A program that backs up your files", False,
                     "That is a backup. Phishing is a trick message designed to fool you."),
                    ("A setting you switch on in your router", False,
                     "No, phishing arrives as a message. It is not a router setting."),
                ],
            },
            {
                "key": "phishing-inbox",
                "kind": "inbox",
                "points": 3,
                "title": "Anatomy of a phishing email",
                "diagram": "phishing-email",
                "body": "<p>Good news: scam emails almost always give themselves "
                "away in the same three places. The sender's address is a lookalike, "
                "close to the real thing but not quite. There is a made up deadline, "
                "because urgency stops you thinking. And there is a link that does "
                "not go where it claims.</p>"
                "<p>Once you know where to look, you can check an email in seconds "
                "without being technical at all. Here is one annotated, then you "
                "will find the tells yourself.</p>",
                "payload": {
                    "prompt": "This just landed in the shared inbox. Tap every part "
                    "that looks off. Find them all to finish.",
                    "avatar": "AP",
                    "parts": [
                        {"id": "from", "zone": "From",
                         "text": "AusPost Delivery <service@auspost-delivery.info>",
                         "bad": True,
                         "why": "A lookalike address. The real Australia Post is auspost.com.au, not auspost-delivery.info."},
                        {"id": "subject", "zone": "Subject",
                         "text": "Parcel on hold, pay a $2.99 release fee within 24 hours",
                         "bad": True,
                         "why": "A tiny fee plus a tight deadline is a classic nudge to make you act without thinking."},
                        {"id": "greeting", "zone": "Body",
                         "text": "Dear Valued Customer,",
                         "bad": True,
                         "why": "A generic greeting. A sender who really knows you usually uses your name."},
                        {"id": "b1", "zone": "Body",
                         "text": "We attempted delivery but a small customs fee is outstanding.",
                         "bad": False,
                         "why": "On its own this is just filler. The real tells are the sender, the deadline and the link."},
                        {"id": "b2", "zone": "Body",
                         "text": "Pay now at http://auspost-delivery.info/pay or your parcel is returned.",
                         "bad": True,
                         "why": "An emailed payment link on a lookalike site. Never click it. Go to the real website yourself."},
                    ],
                },
            },
            {
                "key": "human-error",
                "kind": "check",
                "points": 2,
                "title": "Why a rushed human is the biggest risk",
                "body": "<p>If you take one thing from this module, take this: the "
                "biggest risk is not a machine, it is a good person having a rushed "
                "day. Study after study, in Australia and overseas, lands on the "
                "same finding. Most incidents involve an ordinary human action: a "
                "click, a reused password, a payment approved because the email "
                "seemed urgent.</p>"
                "<p>That is not a reason for guilt, and it is not a reason to "
                "distrust your team. It is simply where the leverage is. A firewall "
                "cannot stop you typing your password into a convincing fake page, "
                "but you can pause when something feels rushed, and that single "
                "habit prevents more harm than any product.</p>"
                "<div class=\"cy-callout\">Attackers rely on urgency on purpose. A "
                "tight deadline exists to stop you thinking. Slowing down for ten "
                "seconds is a genuine security control.</div>",
                "question": "Across the organisations that get hit, what is the single biggest risk?",
                "hint": "Think about what nearly every incident has in common. It is not a particular device.",
                "options": [
                    ("Everyday human error, like clicking a link or reusing a password", True,
                     "Right. Most incidents involve an ordinary human action, which is why calm habits beat any gadget."),
                    ("Old printers", False,
                     "Any device can be a weak point, but the biggest risk overall is human error."),
                    ("Having too many backups", False,
                     "Backups are a good thing. They are never the risk."),
                    ("Using the internet at all", False,
                     "The internet is not the problem. A rushed human is the more common way in."),
                ],
            },
            {
                "key": "sms-spot",
                "kind": "spot",
                "points": 2,
                "title": "Spotting a scam text",
                "body": "<p>Phishing is not just email. The same tricks arrive by "
                "text message, often about a parcel you may or may not be expecting. "
                "The tells are identical: a lookalike web address, a small fee, and "
                "a push to act now.</p>"
                "<p>Have a look at these two, then tap the one you should not "
                "trust.</p>",
                "payload": {
                    "prompt": "Two texts about a parcel land on your phone. Tap the fake.",
                    "left": {
                        "sender": "AusPost",
                        "text": "Your parcel S12 3456 will arrive today 9am to 1pm. "
                        "Track at auspost.com.au/track",
                    },
                    "right": {
                        "sender": "+61 4xx xxx",
                        "text": "AUSPOST: your parcel is held. Pay the $1.99 redelivery "
                        "fee now at aus-post-redelivery.co/pay",
                    },
                    "fake": "right",
                    "why": "The fake uses a lookalike link (aus-post-redelivery.co, not "
                    "auspost.com.au), asks for a fee, and pushes you to hurry. The genuine "
                    "one just gives a delivery window and the proper address.",
                },
            },
            {
                "key": "when-off",
                "kind": "check",
                "points": 1,
                "title": "When something feels off",
                "body": "<p>The thread running through all of this is simple: when a "
                "message pressures you, slow down and verify on a channel you "
                "already trust. Do not use the phone number or link in the "
                "suspicious message itself, because a scammer supplies their own. "
                "Ring the number you already have, or type the real web address "
                "yourself.</p>",
                "question": "An email says an overdue invoice must be paid in the next hour, to a new bank account. Safest first move?",
                "hint": "Ask who benefits if you act fast, then find a way to check that does not rely on the email.",
                "options": [
                    ("Ring the supplier on a number you already have and check", True,
                     "Yes. A sudden change of bank details plus a deadline is the classic invoice scam. Verify on a number you already trust."),
                    ("Pay it quickly so nothing gets cut off", False,
                     "That is exactly what the scammer is counting on. The deadline is there to rush you."),
                    ("Reply to the email and ask if it is genuine", False,
                     "Risky. If it is a scam, you are just asking the scammer, and they will say yes."),
                    ("Click the link to view the invoice first", False,
                     "Best not to. An unexpected link is often where the trouble starts. Check before you click."),
                ],
            },
        ],
    },
    {
        "title": "Locking your front door",
        "reading_time_minutes": 7,
        "intro": "The practical protections: a strong password, a second key, and "
        "Wi-Fi set up so the front door actually shuts.",
        "tasks": [
            {
                "key": "router",
                "kind": "check",
                "points": 2,
                "title": "Your router is the front door",
                "body": "<p>If your workplace were a building, the router would be "
                "the front door. It is the box, sometimes called a modem or gateway, "
                "that connects everything you do to the internet. Almost all of your "
                "information passes through it, which makes it one of the most "
                "important things to set up properly and one of the most commonly "
                "neglected.</p>"
                "<p>A router has two passwords and people mix them up. The Wi-Fi "
                "password is the one everyone types to get online. The admin "
                "password changes the router's own settings, and it is the quiet, "
                "dangerous one, because its factory default is printed online for "
                "anyone to find.</p>",
                "question": "Which password is genuinely dangerous to leave on the factory setting?",
                "hint": "One password just lets people onto the Wi-Fi. The other lets them change everything.",
                "options": [
                    ("The admin password that changes the router's settings", True,
                     "Yes. Factory admin passwords are printed online, so anyone who reaches the router can take it over."),
                    ("The guest Wi-Fi password", False,
                     "Worth changing too, but the admin password is the one people forget even exists."),
                    ("Your email password", False,
                     "Your email password is not set on the router. The risky default here is the router's admin one."),
                    ("Neither, if the box is brand new", False,
                     "Brand new is exactly when it is on a known default, so change it straight away."),
                ],
            },
            {
                "key": "password-builder",
                "kind": "password",
                "points": 3,
                "title": "A password worth trusting",
                "body": "<p>Passwords do not need to be a misery. The single most "
                "important thing is length. A long password made of a few unrelated "
                "words is both very strong and easy to remember, far better than a "
                "short one with a couple of symbols swapped in. And whatever you "
                "choose, never reuse a password that guards anything else, because "
                "one leaked website then hands over the lot.</p>"
                "<p>Try it below. Type a password for the office router and watch "
                "the meter explain itself as you go.</p>",
                "payload": {
                    "prompt": "Type a password for the office router. Watch the "
                    "meter explain itself, and reach Strong to finish.",
                    "target": "strong",
                    "common": ["password", "password1", "123456", "12345678", "qwerty",
                               "admin", "letmein", "welcome", "monkey", "iloveyou"],
                    "tips": [
                        "Length beats complexity. Aim for twelve characters or more.",
                        "A few unrelated words are strong and easy to recall.",
                        "Never reuse a password that guards anything else.",
                    ],
                },
            },
            {
                "key": "twofa",
                "kind": "check",
                "points": 2,
                "title": "A second key: two-factor",
                "diagram": "two-factor",
                "body": "<p>Even a strong password can be stolen. Two-factor "
                "authentication is the answer: a second key, usually a code on your "
                "phone, so that a stolen password on its own is no longer enough to "
                "get in. It takes a couple of minutes to switch on and it is one of "
                "the most powerful things you can do.</p>"
                "<p>If you turn it on in only one place, make it your email, because "
                "email is the master key that can reset the passwords of most of "
                "your other accounts.</p>",
                "question": "What does turning on two-factor authentication actually do for you?",
                "hint": "It adds something, it does not replace anything. What does an attacker still not have?",
                "options": [
                    ("A stolen password on its own is no longer enough to get in", True,
                     "Exactly. The second step means a leaked password by itself will not open the door."),
                    ("It makes your password impossible to steal", False,
                     "It does not stop a password being stolen. It makes a stolen one useless on its own."),
                    ("It replaces your password", False,
                     "It works alongside your password, adding a second step rather than swapping it out."),
                    ("It backs up your account", False,
                     "That is a backup. Two-factor is about proving it is really you."),
                ],
            },
            {
                "key": "wifi-sort",
                "kind": "sort",
                "points": 2,
                "title": "Securing the Wi-Fi",
                "body": "<p>Three quick wins finish off the Wi-Fi. Use modern "
                "encryption, WPA3 or WPA2, and never the ancient WEP, which has been "
                "broken for years. Turn on a separate guest network so visitors' "
                "phones stay away from your work devices. And let the router and "
                "everything on it install updates automatically, because those "
                "updates close security holes before attackers can use them.</p>"
                "<p>Sort the habits below into Safe and Risky to lock it in.</p>",
                "payload": {
                    "prompt": "Sort each habit into Safe or Risky. All six right to finish.",
                    "buckets": [
                        {"id": "safe", "label": "Safe"},
                        {"id": "risky", "label": "Risky"},
                    ],
                    "items": [
                        {"id": "wpa", "text": "Using WPA3 or WPA2 encryption", "bucket": "safe",
                         "why": "Modern encryption protects everyone on the network."},
                        {"id": "default", "text": "Leaving the router admin password on default",
                         "bucket": "risky", "why": "Those defaults are published online for anyone to find."},
                        {"id": "guest", "text": "A separate guest network for visitors", "bucket": "safe",
                         "why": "It keeps visitors' devices away from your work ones."},
                        {"id": "cafe", "text": "Doing the banking on open cafe Wi-Fi", "bucket": "risky",
                         "why": "You cannot trust a network you do not control."},
                        {"id": "updates", "text": "Letting updates install automatically", "bucket": "safe",
                         "why": "Updates close holes before attackers can use them."},
                        {"id": "wep", "text": "Sticking with old WEP encryption", "bucket": "risky",
                         "why": "WEP has been broken for years and offers little protection."},
                    ],
                },
            },
            {
                "key": "login-spot",
                "kind": "spot",
                "points": 1,
                "title": "Real page or fake?",
                "body": "<p>One last skill for the front door: telling a real login "
                "page from a fake one. Scammers build convincing copies of bank and "
                "email logins, then send you to them. The padlock in the address "
                "bar does not help, because scam sites can have one too. The tell is "
                "the web address itself.</p>",
                "payload": {
                    "prompt": "Your bank's login page, or a fake? Tap the one you should not trust.",
                    "variant": "login",
                    "left": {"url": "https://coastline.com.au/login", "brand": "Coastline Bank"},
                    "right": {"url": "https://coastline-bank-verify.com/login", "brand": "Coastline Bank"},
                    "fake": "right",
                    "why": "The padlock is on both, so it proves nothing. The tell is the "
                    "address. The real bank is coastline.com.au. The fake is "
                    "coastline-bank-verify.com, a different site borrowing the name.",
                },
            },
        ],
    },
    {
        "title": "Putting it all together",
        "reading_time_minutes": 6,
        "intro": "Layer your habits, make the calls a real workplace faces, and "
        "walk away with a five point checklist you will actually use.",
        "tasks": [
            {
                "key": "defence",
                "kind": "check",
                "points": 3,
                "title": "Why you layer your defences",
                "diagram": "defence-in-depth",
                "body": "<p>No single lock is perfect, and that is fine, because you "
                "do not rely on one. You layer a few simple habits so that if one is "
                "missed, the next still protects you. If a scam email slips past you, "
                "two-factor still blocks the stolen password. If ransomware gets in, "
                "a good backup brings you back without paying anyone.</p>"
                "<p>That last one is worth dwelling on. Ransomware works by holding "
                "your only copy hostage. A recent backup that you have tested and "
                "can actually restore takes away all their leverage. You restore, "
                "and carry on.</p>",
                "question": "How do good backups help against ransomware?",
                "hint": "Ransomware holds your files hostage. What takes away their leverage?",
                "options": [
                    ("You can restore your files and carry on, instead of paying the criminals", True,
                     "Exactly. A tested backup turns a crisis into an afternoon of restoring."),
                    ("They stop the ransomware from arriving", False,
                     "They do not block it, but they mean it cannot hold your only copy hostage."),
                    ("They make the computer faster", False,
                     "Speed is not the point here. Being able to recover is."),
                    ("They hide your files from the attacker", False,
                     "They do not hide anything. They give you a clean copy to come back to."),
                ],
            },
            {
                "key": "reporting",
                "kind": "check",
                "points": 2,
                "title": "Reporting without blame",
                "body": "<p>People make mistakes, and the workplaces that handle "
                "security well are the ones where a person can say 'I think I "
                "clicked something' without fear. Fast, blame free reporting turns a "
                "near miss into a non-event, because the account can be secured "
                "before any harm is done. Staying quiet out of embarrassment is what "
                "lets a small problem grow into an expensive one.</p>"
                "<p>If you ever think you have slipped up, the most useful thing you "
                "can do is say so quickly.</p>",
                "question": "You realise you typed your password into a page that looked a bit off. What now?",
                "hint": "The goal is to get the account secured before anything bad happens. Who can do that?",
                "options": [
                    ("Tell whoever looks after your IT straight away", True,
                     "Yes. Quick reporting means the account can be secured before harm is done. There is never trouble for owning up."),
                    ("Say nothing and hope for the best", False,
                     "Silence just gives the problem room to grow. Speak up early."),
                    ("Delete the page from your history", False,
                     "That does not undo an entered password. It needs reporting so the account can be secured."),
                    ("Wait a week and see if anything happens", False,
                     "Waiting only hands the attacker time. Report it now."),
                ],
            },
            {
                "key": "capstone-branch",
                "kind": "branch",
                "points": 3,
                "title": "A week at Docklands Dental",
                "body": "<p>Time to put it all together. You are on the front desk "
                "at a small dental practice for a week, and a few situations come up "
                "that every Australian small business meets. Make the call you would "
                "really make. There are no trick questions, and you can always see "
                "the better path.</p>",
                "payload": {
                    "prompt": "Choose what you would really do. You can always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "Monday. An email from 'accounts@your-supplier-au.info' says an "
                            "invoice is overdue and the bank account has changed. Pay within the hour "
                            "or the service stops.",
                            "choices": [
                                {"label": "Pay it quickly so nothing gets cut off", "to": "n1bad",
                                 "outcome": "bad",
                                 "feedback": "Urgency plus a changed bank account is the classic invoice scam. The money is gone."},
                                {"label": "Ring the supplier on a number you already have", "to": "n2",
                                 "outcome": "good",
                                 "feedback": "Exactly. Verify a change of details on a channel you already trust."},
                            ],
                        },
                        "n1bad": {
                            "text": "You paid. An hour later the real supplier phones, confused about a "
                            "payment they never received.",
                            "choices": [{"label": "See what would have worked", "to": "n2"}],
                        },
                        "n2": {
                            "text": "Wednesday. A colleague clicks a link in a 'your password expires "
                            "today' email, types their password, then feels uneasy about it.",
                            "choices": [
                                {"label": "Tell them to keep quiet so nobody is in trouble", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "Staying quiet lets a small problem grow. Fast reporting is what limits the damage."},
                                {"label": "Report it to IT now and reset the password", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Right. Quick reporting turns a near miss into a non-event."},
                            ],
                        },
                        "n2bad": {
                            "text": "Two days later the mailbox is quietly sending scams to all your patients.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "Thursday. Setting up a new laptop, you are offered two-factor "
                            "authentication on the practice email. It is a couple of extra minutes.",
                            "choices": [
                                {"label": "Skip it, everyone is busy", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "Skipping it leaves a stolen password as the only lock on the door."},
                                {"label": "Turn it on now", "to": "n4",
                                 "outcome": "good",
                                 "feedback": "Good. A stolen password on its own will not be enough now."},
                            ],
                        },
                        "n3bad": {
                            "text": "A month later a reused password leaks from another site, and it opens "
                            "the practice email too.",
                            "choices": [{"label": "See the better path", "to": "n4"}],
                        },
                        "n4": {
                            "text": "Friday. Looking back on the week, which single habit would have "
                            "prevented the most harm?",
                            "choices": [
                                {"label": "Two-factor authentication on email", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes. A stolen password on its own would not have been enough to get in."},
                                {"label": "A faster internet plan", "to": "n4",
                                 "outcome": "bad",
                                 "feedback": "Speed is not security. Have another go."},
                            ],
                        },
                        "end": {
                            "text": "That is a real week handled. Verify before you pay, report fast, and "
                            "turn on two-factor. That is network security in practice, and none of it needed "
                            "jargon.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "five-habits",
                "kind": "check",
                "points": 2,
                "title": "Your five habits",
                "body": "<p>That is the whole module in five habits. Pause before "
                "you act on anything urgent. Use long, unique passwords and turn on "
                "two-factor. Keep everything updated. Back up what you cannot lose. "
                "And report anything odd, quickly and without blame. None of it "
                "needs you to be technical, and together they stop the great "
                "majority of problems.</p>",
                "question": "Which single habit most directly stops a stolen password from becoming a break-in?",
                "hint": "Which habit adds a second check that the attacker cannot provide?",
                "options": [
                    ("Turning on two-factor authentication", True,
                     "Yes. Two-factor adds a second key, so a stolen password on its own will not get anyone in."),
                    ("Backing up your files", False,
                     "Backups are vital for recovering from ransomware, but they do not stop a stolen password being used."),
                    ("Installing updates promptly", False,
                     "Updates close software holes, which matters, but they do not add a second check at login."),
                    ("Pausing before urgent requests", False,
                     "A great habit against scams, but two-factor is what specifically blocks a stolen password."),
                ],
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. A bank of 28 (draw 10 at random), seven per lesson. Four options each,
# exactly one correct, and every option carries an explanation that teaches (why
# right, why wrong). This is the fuel for the Adaptive Feedback Engine. Same
# house voice as the lessons: warm, plain, no em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: networks and the CIA triad ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "In plain terms, what is a computer network?",
            "options": [
                ("Two or more devices connected so they can share information", True,
                 "Yes. From two machines to the whole internet, a network is just devices connected to share information."),
                ("A single computer with a fast processor", False,
                 "Not quite. One computer on its own is not a network. It is the connection between devices that makes one."),
                ("A type of antivirus program", False,
                 "No. Antivirus protects a single device. It is not what a network is."),
                ("The password you use to log in", False,
                 "No. A password controls who gets access, but it is not the network itself."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Your information is 'in transit' when it is:",
            "options": [
                ("Moving across the network, like an email on its way to someone", True,
                 "That is it. In transit means the information is travelling, which is when it can be intercepted if it is not protected."),
                ("Saved on a hard drive that is switched off", False,
                 "That is 'at rest', sitting in storage rather than moving."),
                ("Printed out and filed in a drawer", False,
                 "That is a paper copy at rest, not data moving across a network."),
                ("Deleted from your computer", False,
                 "Deleted data is not in transit. In transit means actively moving from one place to another."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What do the letters in the CIA triad stand for?",
            "options": [
                ("Confidentiality, Integrity and Availability", True,
                 "Correct. These are the three things security protects, and most decisions come back to one of them."),
                ("Computers, Internet and Applications", False,
                 "No. The triad is about what you protect, not a list of equipment."),
                ("Control, Inspection and Access", False,
                 "These sound plausible but they are not it. The triad is Confidentiality, Integrity and Availability."),
                ("Confidential Intelligence Agency", False,
                 "Despite the initials, the CIA triad has nothing to do with any spy agency."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Putting a password on a spreadsheet of customer details mainly protects:",
            "options": [
                ("Confidentiality, keeping it from people who should not see it", True,
                 "Yes. Limiting who can open the file is a confidentiality control."),
                ("Availability, keeping it online", False,
                 "No. A password does not keep a file available. It limits who can read it."),
                ("Integrity, proving it was not changed", False,
                 "Not the main point. A password limits access, which is confidentiality."),
                ("Nothing, because spreadsheets cannot be protected", False,
                 "They can. A password is a simple but real confidentiality control."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "An invoice's bank details are secretly changed so a payment goes to a stranger. Which pillar failed?",
            "options": [
                ("Integrity, the information was altered without permission", True,
                 "Right. The file still opens, but its accuracy is gone. That is an integrity failure, and a common way money goes missing."),
                ("Availability, the file cannot be opened", False,
                 "No. Availability is about whether you can reach something. Here the file opens fine, it was just tampered with."),
                ("Confidentiality, someone saw what they should not", False,
                 "Not quite. The problem is not who saw it, it is that the details were changed. That is integrity."),
                ("None of them, this is not a security issue", False,
                 "It very much is. Altering financial details without permission is a failure of integrity."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Keeping a restorable backup of your files mainly protects which pillar?",
            "options": [
                ("Availability, you can still get your information when you need it", True,
                 "Yes. A backup means an attack or a mistake does not cost you access to your work."),
                ("Confidentiality, it hides the files", False,
                 "No. A backup does not hide anything. It makes sure you can get your data back."),
                ("Integrity, it proves nothing changed", False,
                 "Not the main point. Backups are chiefly about restoring access, which is availability."),
                ("Backups are not really a security control", False,
                 "They are a core one. They protect availability against ransomware and honest mistakes alike."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Which of these is NOT one of the three things the CIA triad protects?",
            "options": [
                ("Speed", True,
                 "Correct, speed is not part of it. The three are Confidentiality, Integrity and Availability."),
                ("Confidentiality", False,
                 "That is one of the three, keeping information from the wrong eyes."),
                ("Integrity", False,
                 "That is one of the three, information not being tampered with."),
                ("Availability", False,
                 "That is one of the three, information being there when you need it."),
            ],
        },
        # ---- Lesson 2: attacks, phishing, human error ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is phishing?",
            "options": [
                ("A message pretending to be someone you trust, to trick you into clicking or sharing details", True,
                 "Yes. It leans on trust, and it is the most common way organisations get caught out."),
                ("A way of speeding up your internet connection", False,
                 "No. Phishing has nothing to do with speed. It is a con."),
                ("A tool that backs up your files", False,
                 "No. That is a backup. Phishing is a trick message."),
                ("A setting on your router", False,
                 "No. Phishing arrives as a message. It is not a router setting."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Across the organisations that get attacked, what is the single biggest risk?",
            "options": [
                ("Human error, the everyday slips like clicking a link or reusing a password", True,
                 "Right. Most incidents involve an ordinary human action, which is why calm habits matter more than any product."),
                ("Old printers", False,
                 "Any device can be a weak point, but the biggest risk overall is human error."),
                ("Having too many backups", False,
                 "Backups are a good thing. They are never the risk."),
                ("Using a router at all", False,
                 "Routers are essential. The biggest risk is everyday human error, not the equipment."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why do scam messages so often push a tight deadline?",
            "options": [
                ("Urgency rushes you, so you act before you have time to think or check", True,
                 "Exactly. The pressure is the point. Slowing down for a moment is one of your best defences."),
                ("Deadlines are required by law on invoices", False,
                 "No. The deadline is a pressure tactic, not a legal requirement."),
                ("It makes the email arrive faster", False,
                 "No. A deadline in the text does nothing to delivery. It is there to hurry you."),
                ("Genuine senders always demand immediate payment", False,
                 "They usually do not. A sudden 'pay now or else' is a warning sign, not normal business."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "An email from 'service@auspost-delivery.info' claims to be Australia Post. What is the clearest tell?",
            "options": [
                ("The domain is not auspost.com.au, it is a lookalike", True,
                 "Yes. The sender's domain is the real giveaway, a lookalike built to pass a quick glance."),
                ("It mentions a parcel", False,
                 "Plenty of genuine messages mention parcels. That alone is not a tell."),
                ("It is written in English", False,
                 "Language is not the tell. The lookalike domain is."),
                ("It arrived in the morning", False,
                 "Timing tells you nothing about whether a message is genuine."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Ransomware is a type of:",
            "options": [
                ("Malware that locks up your files and demands payment to unlock them", True,
                 "Yes, and a tested backup is what lets you recover without paying."),
                ("Strong password", False,
                 "No. Ransomware is harmful software, not a password."),
                ("Wi-Fi encryption setting", False,
                 "No. That is unrelated. Ransomware is malware that holds files hostage."),
                ("Backup tool", False,
                 "The opposite. Backups are your defence against ransomware."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why do attackers target small businesses, councils and schools?",
            "options": [
                ("Automated tools look for any unlocked door, and smaller places often have lighter defences", True,
                 "Right. Attacks are largely automated and opportunistic. Being small does not mean being safe."),
                ("They are too small to be worth attacking", False,
                 "This is the dangerous myth. Smaller organisations are targeted precisely because defences are often lighter."),
                ("They never hold anything valuable", False,
                 "They hold plenty, from customer details to payment information."),
                ("Attackers hand pick each victim by name", False,
                 "Most attacks are automated and untargeted, knocking on thousands of doors at once."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "An email says pay an overdue invoice within the hour to a new account. Safest first step?",
            "options": [
                ("Pause, and check by phoning a number you already have", True,
                 "Yes. Urgency plus a change of bank details is the classic invoice scam. Confirm on a channel you already trust."),
                ("Pay immediately so the account is not closed", False,
                 "No. Acting fast is exactly what the scammer wants. The deadline is there to stop you thinking."),
                ("Reply to the email and ask if it is genuine", False,
                 "Risky. If it is a scam you are asking the scammer, who will happily say yes."),
                ("Click the link to view the invoice", False,
                 "No. An unexpected link is often where the trouble starts. Verify before you click."),
            ],
        },
        # ---- Lesson 3: passwords, 2FA, Wi-Fi, updates ----
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "On a new router, which password is dangerous to leave on the factory setting?",
            "options": [
                ("The admin password that changes the router's settings", True,
                 "Yes. Factory admin passwords are published online, so leaving it unchanged lets anyone take the router over."),
                ("The Wi-Fi password guests use to connect", False,
                 "Change that too, but the admin password is the critical one people forget exists."),
                ("Your email password", False,
                 "Your email password is not set on the router. The risky default here is the router's admin one."),
                ("Neither needs changing if the box is new", False,
                 "New is exactly when it is on a known default, so both should be changed, the admin one especially."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "What makes a password strongest?",
            "options": [
                ("Length, a dozen or more characters, such as a few unrelated words", True,
                 "Yes. Length beats complexity. A long passphrase is both strong and easy to remember."),
                ("Swapping a couple of letters in a short word for symbols", False,
                 "No. Something like 'P@ss1' is short and guessable. Substitutions do not rescue a short password."),
                ("Using the same strong password everywhere", False,
                 "No. Reuse means one leak unlocks everything, however strong the password is."),
                ("Your pet's name, so you will not forget it", False,
                 "No. Personal details are exactly what an attacker guesses first."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What does turning on two-factor authentication achieve?",
            "options": [
                ("A stolen password on its own is no longer enough to get in", True,
                 "Yes. The second check means a leaked password by itself will not open the door."),
                ("It makes your password impossible to steal", False,
                 "No. It does not stop a password being stolen. It makes a stolen one useless on its own."),
                ("It removes the need for a password", False,
                 "No. It works alongside your password, adding a second step rather than replacing it."),
                ("It backs up your account", False,
                 "No. Two-factor is about proving it is really you. It is not a backup."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "You notice your Wi-Fi is set to 'WEP'. What should you do?",
            "options": [
                ("Switch to WPA3 or WPA2, because WEP has been broken for years", True,
                 "Yes. WEP is easily cracked. Move to the newest option your gear supports."),
                ("Leave it, WEP is the most secure", False,
                 "No. WEP is the oldest and broken. It is the least secure of the three."),
                ("Turn encryption off to keep things simple", False,
                 "No. An open network lets anyone nearby read your traffic."),
                ("Nothing, encryption does not matter on Wi-Fi", False,
                 "It matters a lot. Unencrypted Wi-Fi exposes everything on it."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What is the main benefit of a separate guest Wi-Fi network?",
            "options": [
                ("It keeps visitors' and personal devices apart from your work devices", True,
                 "Yes. If a visitor's phone is infected, a guest network keeps that problem away from your business systems."),
                ("It makes your internet twice as fast", False,
                 "No. A guest network is about separation and safety, not speed."),
                ("It removes the need for any password", False,
                 "No. A guest network still uses a password. It simply keeps guests separate."),
                ("It automatically backs up guest files", False,
                 "No. It does not back anything up. Its job is to keep guest devices separate."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why is it worth installing software updates promptly?",
            "options": [
                ("They often fix security holes that attackers are already using", True,
                 "Yes. An update usually closes a known hole, and the gap before you install it is exactly what attackers aim for."),
                ("They always make the device faster", False,
                 "Speed is not the point. The security fixes are."),
                ("They change how the screen looks", False,
                 "Appearance is incidental. The security fixes are why prompt updates matter."),
                ("They are not needed if you have antivirus", False,
                 "No. Antivirus does not patch the holes updates fix. You want both."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "You need to log in to a work system on free cafe Wi-Fi. Safest choice?",
            "options": [
                ("Use your phone's mobile data or a trusted VPN instead", True,
                 "Yes. On a network you do not control, use mobile data or a trusted VPN for anything sensitive."),
                ("Go ahead, cafe Wi-Fi is always safe", False,
                 "No. You cannot be sure who else is on public Wi-Fi or what they can see. Treat it as a public space."),
                ("Just make sure the cafe is busy", False,
                 "How many customers are in tells you nothing about whether the network is safe."),
                ("Turn your screen brightness down so no one can see", False,
                 "The risk is the network carrying your data, not someone reading your screen."),
            ],
        },
        # ---- Lesson 4: habits and response ----
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "A supplier emails that their bank account has changed. Safest way to verify?",
            "options": [
                ("Phone them on a number you already have on file", True,
                 "Yes. Confirm a change of details on a channel you already trust, not one taken from the email."),
                ("Reply to the email and ask them to confirm", False,
                 "Risky. If the email is a scam, you are just asking the attacker."),
                ("Use the phone number printed in the email", False,
                 "No. A scammer supplies their own number. Use details you already hold."),
                ("Just pay it, suppliers do not lie about bank details", False,
                 "A changed bank account is the single most common invoice scam. Always verify."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "A colleague admits they clicked a phishing link. Best response?",
            "options": [
                ("Thank them for speaking up and report it so the account can be secured", True,
                 "Yes. A calm, fast report is what limits the damage. Punishing it just drives the next mistake into hiding."),
                ("Tell them off so they are more careful next time", False,
                 "No. Blame makes people hide mistakes, which is far more dangerous."),
                ("Tell them to keep it quiet", False,
                 "No. Silence lets a small problem grow into a big one."),
                ("Do nothing unless something obviously breaks", False,
                 "By the time damage shows, the attacker has had free rein. Report it early."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What lets a business recover from ransomware without paying?",
            "options": [
                ("Recent backups that have been tested and can actually be restored", True,
                 "Yes. A good backup means you can restore and carry on rather than negotiate."),
                ("A faster internet connection", False,
                 "No. Speed does nothing against ransomware."),
                ("Paying quickly for a discount", False,
                 "No. Paying is no guarantee of recovery, and it marks you as willing to pay again."),
                ("Turning the computer off and on again", False,
                 "No. That will not undo the encryption ransomware applies."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "If you could protect only one account with two-factor first, which should it be?",
            "options": [
                ("Your email, because it can reset the passwords of most other accounts", True,
                 "Yes. Email is the master key, so protecting it protects everything it can reset."),
                ("A rarely used shopping site", False,
                 "Lower value. Start with the account that unlocks the others."),
                ("A news site you have no login for", False,
                 "There is little to protect there. Email matters far more."),
                ("Whichever you use least", False,
                 "The opposite. Protect your highest-value account, your email, first."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "A password manager mainly helps by:",
            "options": [
                ("Letting you use a different strong password everywhere without memorising them", True,
                 "Yes. It remembers unique strong passwords for you, so one leaked site cannot unlock the rest."),
                ("Making your internet faster", False,
                 "No. It has nothing to do with speed."),
                ("Sharing your passwords with colleagues", False,
                 "No. That would undermine security, not help it."),
                ("Removing the need for any password", False,
                 "No. It manages your passwords, it does not abolish them."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What is the idea behind 'defence in depth'?",
            "options": [
                ("Layer several simple habits so that if one is missed, the next still protects you", True,
                 "Yes. No single control is perfect, so overlapping ones mean a single slip is not a disaster."),
                ("Buy one very expensive security product", False,
                 "No. It is about layering simple habits, not a single silver bullet."),
                ("Only the IT team needs to do anything", False,
                 "No. Everyone's small habits are part of the layers."),
                ("Turn off the internet whenever possible", False,
                 "No. It is about sensible overlapping protections, not going offline."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "You realise you may have entered your password into a suspicious page. Best thing to do?",
            "options": [
                ("Report it straight away to whoever looks after your IT", True,
                 "Yes. Fast reporting means the account can be secured before harm is done. There is never trouble for owning up."),
                ("Say nothing and hope nothing happens", False,
                 "No. Staying quiet lets a small problem grow. Quick reporting is what limits the damage."),
                ("Delete the email and carry on", False,
                 "No. Deleting the message does not undo an entered password. It needs reporting."),
                ("Wait a week to see if anything goes wrong", False,
                 "No. Waiting just gives an attacker time. Report it now."),
            ],
        },
    ],
}
