"""Module 1, Network Security Fundamentals: the gold-standard reference content.

This is the module every other module copies, so the shape matters as much as the
words. Kept as plain data (not schema) so it reads like teaching material and the
seed stays re-runnable.

Room format (TryHackMe-style): a lesson is a scrollable room of collapsible task
PANELS. Each panel is a full, deep task, not a quick read: a diagram, several
substantial teaching paragraphs (what it is, a concrete Australian example, why it
matters, what to do), a callout box with a specific scenario, sometimes a
mid-panel check to test understanding partway through, THEN the end interactive (a
question or a hands-on activity). The panels' points sum to 10 and bank at lesson
end.

House voice for here and Modules 2 to 6: warm, confident, human. Plain Australian
English for non-technical readers. Every paragraph earns its place: it teaches
something new, grounds it locally, or tells you what to do. No em-dashes, no
filler, no repetition.
"""

# --------------------------------------------------------------------------
# Lessons. Each task is a panel: title, an optional `diagram`, a rich multi
# paragraph `body` (may include a `<div class="cy-callout">` box), an optional
# mid-panel `inline_check` {question, hint, options}, an optional `body2` (more
# reading after the mid-check), then the end interactive: a `check`/`scenario`
# (question + hint + options) or a hands-on activity (`payload`). Check option
# tuples are (text, is_correct, explanation). Points per lesson sum to 10.
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network is, and what you protect",
        "reading_time_minutes": 9,
        "intro": "Meet the thing you are protecting, follow your information as it "
        "moves through it, and learn the three questions that sit underneath every "
        "security decision you will ever make.",
        "tasks": [
            {
                "key": "net-basics",
                "kind": "check",
                "points": 2,
                "title": "What a network actually is",
                "diagram": "data-travels",
                "body": "<p>Before you can protect a network it helps to know, in "
                "plain terms, what one actually is. A network is simply two or more "
                "devices connected so they can share information. The laptop that "
                "sends a file to the front desk printer, the phone that picks up "
                "email over Wi-Fi, the eftpos terminal that reaches the bank to "
                "approve a payment: each of those is a small conversation between "
                "devices, and the network is what carries the conversation.</p>"
                "<p>Your workplace network has a few familiar parts. There are the "
                "<strong>devices</strong> people use, like computers, phones and "
                "printers. There is a <strong>router</strong>, the box that "
                "connects your workplace to the internet and passes messages between "
                "your devices. And there is the <strong>internet</strong> itself, a "
                "vast shared network of other networks that your information travels "
                "across to reach a supplier, a customer or the tax office.</p>"
                "<p>The diagram above traces a single click. When you open a "
                "supplier's website, your request leaves your device, passes through "
                "your router, crosses the internet to the supplier's server, and the "
                "answer comes all the way back. It happens in a fraction of a "
                "second, and at every step your information is somewhere it could, in "
                "principle, be seen or interfered with. That is the whole reason "
                "security exists.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "you do not need to run the network to help keep it safe. Most real "
                "trouble starts with an everyday choice at one of these devices, not "
                "with some clever attack on the wires in between. Knowing the shape "
                "of it is the first step, and by the end of this module you will "
                "recognise where every habit you learn fits on that picture.</div>",
                "question": "Which of these best describes a network?",
                "hint": "Look for the option that is about devices being joined together to share.",
                "options": [
                    ("Two or more devices connected so they can share information", True,
                     "Spot on. From two machines in one room to the whole internet, a network is devices connected to share information."),
                    ("One powerful computer sitting on its own", False,
                     "Not quite. On its own it is just a computer. What makes a network is the connection between devices."),
                    ("The antivirus program on your laptop", False,
                     "That is a tool that protects a single device. It is not the network itself."),
                    ("The password you type to get on the Wi-Fi", False,
                     "That is how you join the network. It is not the network itself."),
                ],
            },
            {
                "key": "data-states",
                "kind": "check",
                "points": 2,
                "title": "Where your information lives",
                "body": "<p>Here is an idea that quietly makes sense of a great deal "
                "of security. At any moment, a piece of your information is in one of "
                "three states. It is <strong>at rest</strong>, saved on a device or a "
                "server. It is <strong>in transit</strong>, moving across the network "
                "from one place to another. Or it is <strong>in use</strong>, open "
                "on a screen in front of someone.</p>"
                "<p>Each state needs looking after in a different way, and it is easy "
                "to protect one and forget the others. Think of a Bendigo accounting "
                "firm with a spreadsheet of clients' tax file numbers. Locking the "
                "office at night protects that file at rest. But the moment a staff "
                "member attaches it to an email, the very same information is in "
                "transit across the internet, and the lock on the door does nothing "
                "for it. And when the file is open on a screen at a shared front "
                "desk, it is in use, where anyone walking past can read it.</p>"
                "<p>The lesson is not to panic about all three at once. It is simply "
                "to notice which state your information is in before you decide it is "
                "safe. A file can be perfectly secure on a locked laptop and "
                "completely exposed thirty seconds later as an email attachment. The "
                "state changed, so the protection it needs changed too.</p>"
                "<div class=\"cy-callout\"><strong>In practice:</strong> the single "
                "most common way sensitive information leaks is not a hacker breaking "
                "in. It is ordinary information in transit, sent to the wrong person "
                "by email. That is why email comes up again and again in this "
                "course, and why a two second glance at the address line saves so "
                "much grief.</div>",
                "question": "Your information is 'in transit' when it is doing what?",
                "hint": "The word transit is about movement. Which option describes information on the move?",
                "options": [
                    ("Moving across the network, like a file attached to an email on its way to someone", True,
                     "Yes. In transit means the information is travelling, which is exactly when it can be intercepted if it is not protected."),
                    ("Saved on a hard drive that is switched off", False,
                     "That is at rest, sitting in storage rather than moving."),
                    ("Printed out and filed in a drawer", False,
                     "That is a paper copy at rest, not data moving across a network."),
                    ("Deleted and gone from your computer", False,
                     "Deleted data is not in transit. In transit means actively moving from one place to another."),
                ],
            },
            {
                "key": "cia-triad",
                "kind": "sort",
                "points": 3,
                "title": "The three questions security asks",
                "diagram": "cia-triad",
                "body": "<p>Every security decision you will ever make comes back to "
                "three simple questions. Security people call them the CIA triad, and "
                "despite the name it has nothing to do with spies. The three are "
                "Confidentiality, Integrity and Availability, and once you can name "
                "them, most security choices stop feeling like guesswork.</p>"
                "<p><strong>Confidentiality</strong> asks a simple thing: can only "
                "the right people see this? A patient's medical history, a list of "
                "donors, an employee's tax file number. When you put a password on a "
                "spreadsheet or lock a filing cabinet, you are protecting "
                "confidentiality.</p>"
                "<p><strong>Integrity</strong> asks whether the information is still "
                "accurate and has not been quietly changed. This one is easy to miss, "
                "because a tampered file usually looks perfectly normal. If someone "
                "edits the bank account number on an invoice, the document still "
                "opens and still looks right, but its integrity is gone, and that is "
                "how a surprising amount of money quietly disappears.</p>"
                "<p><strong>Availability</strong> asks whether the information and the "
                "systems are actually there when you need them. A backup you can "
                "restore protects availability. So does keeping the lights on rather "
                "than being knocked offline by an attack or a failed hard drive.</p>"
                "<div class=\"cy-callout\"><strong>One office, three bad days.</strong> "
                "Picture the front desk at a small Geelong dental practice. On Monday "
                "a staff member emails the day's patient list to the wrong address: a "
                "confidentiality failure, private records sitting in a stranger's "
                "inbox. On Tuesday a scammer changes the bank details on a supplier "
                "invoice and the payment vanishes: an integrity failure, the numbers "
                "altered without anyone noticing. On Wednesday ransomware locks every "
                "file an hour before the first appointment: an availability failure, "
                "the records still there but nobody able to open them. Same office, "
                "same week, three very different disasters, one for each pillar.</div>",
                "inline_check": {
                    "question": "A supplier's invoice arrives with the bank account number quietly changed. Which pillar has failed?",
                    "hint": "The file opens fine and nobody has been locked out. What has actually changed about the information?",
                    "options": [
                        ("Integrity, the information was altered without permission", True,
                         "Yes. The invoice still opens and still looks right, but the details were changed behind your back. That is an integrity failure, and it is exactly how invoice scams work."),
                        ("Availability, you cannot open the file", False,
                         "Not this time. The file opens perfectly. The problem is that its contents were changed, which is integrity."),
                        ("Confidentiality, someone saw it who should not have", False,
                         "The issue is not who saw it, it is that the numbers were altered. That is integrity."),
                        ("Nothing failed, invoices change all the time", False,
                         "A quietly changed bank account is a classic integrity attack, and it matters a great deal."),
                    ],
                },
                "body2": "<p>Here is why the triad is worth carrying around in your "
                "head. When something feels risky but you cannot say why, ask which "
                "of the three it threatens. Would this expose information to the "
                "wrong people? That is confidentiality. Could this change important "
                "information without anyone noticing? That is integrity. Could this "
                "stop us reaching what we need? That is availability. Naming the "
                "pillar usually points straight at what to do next.</p>"
                "<p>Now try it yourself. Below are eight everyday situations. Tap "
                "each one, then tap the pillar it puts at risk.</p>",
                "payload": {
                    "prompt": "Tap a situation, then tap the pillar it puts at risk. Get all eight to finish.",
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
                "body": "<p>The three pillars are easiest to understand through what "
                "goes wrong, so let us look a little closer at each failure and what "
                "it feels like from the front desk.</p>"
                "<p>A <strong>confidentiality</strong> failure is information reaching "
                "the wrong eyes, and it is rarely dramatic. It is a misdirected "
                "email, a shared spreadsheet with the wrong permissions, a password "
                "on a sticky note, a laptop left on a train. Nobody has to break in. "
                "The information simply ends up where it should not be.</p>"
                "<p>An <strong>integrity</strong> failure is information changed "
                "without permission, and it is the sneakiest of the three because "
                "nothing looks broken. The classic case is a scammer altering the "
                "bank details on an invoice. The document opens, the logo is right, "
                "the amount is right, and the money goes to a stranger. This is why "
                "we make such a point later of verifying a change of bank details "
                "before you pay a cent.</p>"
                "<p>An <strong>availability</strong> failure is being locked out of "
                "your own information. Ransomware is the obvious example, but so is a "
                "failed hard drive with no backup, or a website knocked offline "
                "during your busiest hour. The information may be perfectly intact "
                "and perfectly private, and still useless to you because you cannot "
                "reach it.</p>"
                "<div class=\"cy-callout\"><strong>Watch for this:</strong> a single "
                "event can look completely normal while a pillar has quietly failed. "
                "A tampered invoice still opens. That is what makes integrity attacks "
                "so effective, and why a moment of verification is worth so much.</div>",
                "question": "Ransomware locks all your files on the morning of a big deadline. Which pillar took the hit?",
                "hint": "Ask yourself: can the right people still get to the information when they need it?",
                "options": [
                    ("Availability", True,
                     "Yes. The files still exist and have not been changed, you just cannot reach them, and that is exactly what availability protects."),
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
                "points": 1,
                "title": "Bringing it together",
                "body": "<p>You now have the foundation the whole module is built on. "
                "A network is connected devices sharing information. That information "
                "spends much of its life on the move. And security is the practice of "
                "protecting its confidentiality, integrity and availability, "
                "whichever one a given risk happens to threaten.</p>"
                "<p>Everything that follows is a practical, non-technical way to "
                "defend one of those three. Strong passwords and two-factor protect "
                "confidentiality. Verifying a change of bank details protects "
                "integrity. Backups protect availability. When you can see why a "
                "habit matters, it is far easier to keep, and far harder to talk "
                "yourself out of on a busy day.</p>",
                "question": "A backup you have tested and can actually restore mainly protects which pillar?",
                "hint": "A backup does not hide your files or prove they are unchanged. What does it guarantee you can still do?",
                "options": [
                    ("Availability", True,
                     "Yes. A backup means an attack or a mistake does not cost you access to your work. You restore and carry on."),
                    ("Confidentiality", False,
                     "No. A backup does not hide anything. It makes sure you can get your data back."),
                    ("Integrity", False,
                     "Not the main point. Backups are chiefly about restoring access, which is availability."),
                    ("It is not really a security control", False,
                     "It is a core one. It protects availability against ransomware and honest mistakes alike."),
                ],
            },
        ],
    },
    {
        "title": "How attacks actually happen",
        "reading_time_minutes": 10,
        "intro": "The real ways in are fewer than you would think. Learn them, take "
        "a phishing message apart yourself, and practise telling a genuine one from "
        "a fake before it ever reaches your inbox.",
        "tasks": [
            {
                "key": "vectors",
                "kind": "check",
                "points": 2,
                "title": "The common ways in",
                "body": "<p>Attackers are rarely magicians. They walk through doors "
                "people leave open, and the doors are fewer and better understood "
                "than the movies suggest. Almost every incident starts with one of "
                "four things: a convincing fake message, known as <strong>phishing"
                "</strong>; a <strong>weak or reused password</strong>; <strong>"
                "software that has not been updated</strong>, which leaves a known "
                "hole open; or <strong>malware</strong>, harmful software, of which "
                "ransomware is the variety that ruins weeks.</p>"
                "<p>What ties all four together is that they almost always need a "
                "person to have a busy moment. A phishing email only works if someone "
                "clicks. A reused password only hurts if someone reuses it. That is "
                "genuinely good news, because it means the fix is usually a small "
                "human habit rather than an expensive piece of equipment.</p>"
                "<p>It also explains who gets hit. Most attacks are automated. "
                "Software knocks on thousands of doors an hour looking for any one "
                "that is unlocked, which is why a Brunswick bakery with a single "
                "laptop is targeted by the same wave of scam emails as a large "
                "company. Being small is not the same as being safe. It usually just "
                "means lighter defences behind the same unlocked door.</p>"
                "<div class=\"cy-callout\"><strong>What to do with this:</strong> you "
                "do not need to memorise a hundred attack types. Learn the handful of "
                "doors above and the single habit that guards most of them, which is "
                "to slow down when a message pressures you. The rest of this lesson "
                "is about spotting the most common door of all, the fake message.</div>",
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
                "body": "<p>Here is the reassuring truth about scam emails: they "
                "almost always give themselves away in the same few places. Once you "
                "know where to look, you can check a suspicious message in seconds, "
                "without being technical at all.</p>"
                "<p>The first place is the <strong>sender's address</strong>. Scammers "
                "cannot use the real organisation's address, so they use a lookalike, "
                "something close enough to pass a quick glance. The real Australia "
                "Post is auspost.com.au, but a scam might come from "
                "auspost-delivery.info or auspost.secure-parcel.com. The brand name "
                "is in there, but the actual domain, the part right before the first "
                "single slash, is not the real one.</p>"
                "<p>The second is <strong>manufactured urgency</strong>. A made up "
                "deadline, a threat that something will be lost or cut off, a small "
                "fee to pay right now. Urgency is not an accident. It is there on "
                "purpose, to push you into acting before the thinking part of your "
                "brain catches up. The third is a <strong>link that does not go "
                "where it claims</strong>, usually to that same lookalike site, ready "
                "to catch your login or your card.</p>"
                "<div class=\"cy-callout\"><strong>A real Tuesday at a Ballarat real "
                "estate agency.</strong> An email lands looking exactly like the one "
                "the agency's trust account software really sends. The logo is "
                "perfect. But the sender is 'no-reply@trust-portal-au.com' rather "
                "than the usual address, and it warns that access will be suspended "
                "in two hours unless the login is 'reverified'. Perfect logo, wrong "
                "domain, invented deadline. Two of the three tells, in one glance.</div>",
                "inline_check": {
                    "question": "Of the three tells, which is the most reliable single thing to check first?",
                    "hint": "Two of the tells rely on your judgement of tone. One is a plain fact you can read straight off the message.",
                    "options": [
                        ("The sender's actual domain, the part right before the first single slash", True,
                         "Yes. Tone and urgency take judgement, but the real domain is a fact sitting right there. If it is not the organisation's genuine address, that is your answer."),
                        ("Whether the email mentions money", False,
                         "Plenty of genuine emails mention money. On its own that proves nothing."),
                        ("Whether the logo looks correct", False,
                         "A logo is trivial to copy, so a perfect one is no comfort at all. Check the domain."),
                        ("How politely it is written", False,
                         "Scammers can be perfectly polite. Politeness is not a safety signal."),
                    ],
                },
                "body2": "<p>Now put it into practice. Below is a message that just "
                "landed in a shared inbox. Read it the way you now know how, and tap "
                "every part that looks off. Find them all and the panel is yours.</p>",
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
                "body": "<p>If you take one idea from this entire module, take this: "
                "the biggest risk is not a machine, it is a good person having a "
                "rushed day. Study after study, in Australia and overseas, lands on "
                "the same finding. The large majority of incidents involve an "
                "ordinary human action: a click on the wrong link, a password reused "
                "from another site, a payment approved because the email seemed "
                "urgent and the day was busy.</p>"
                "<p>That is not a reason for guilt, and it is certainly not a reason "
                "to distrust your team. It is simply where the leverage is. A "
                "firewall cannot stop you typing your password into a convincing fake "
                "page, but you can pause when something feels rushed, and that single "
                "habit prevents more harm than any product you could buy.</p>"
                "<p>The reason it works is that attackers depend on you not pausing. "
                "Every manufactured deadline, every 'urgent' in a subject line, every "
                "threat that an account will be closed, exists to keep you moving "
                "fast. The moment you stop and check on a channel you already trust, "
                "the whole trick falls apart, because it was only ever going to work "
                "at speed.</p>"
                "<div class=\"cy-callout\"><strong>Make it a rule, not a mood:</strong> "
                "when a message pressures you to act right now, that pressure is "
                "itself the warning sign. Ten seconds of slowing down is a genuine "
                "security control, and it is one nobody can take away from you.</div>",
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
                "body": "<p>Phishing is not only an email problem. The exact same "
                "tricks arrive by text message, and the shorthand for it is smishing, "
                "SMS phishing. Text feels more trustworthy than email to a lot of "
                "people, which is precisely why scammers like it. A message on your "
                "phone feels personal and immediate, and there is less room on the "
                "screen for the details that would give it away.</p>"
                "<p>The tells are identical to email, just squeezed smaller. A "
                "lookalike web address instead of the real one. A small fee or a "
                "threat that a parcel will be returned. And a push to act now, "
                "usually within a few hours. The parcel theme is popular because at "
                "any given moment half the country is expecting something in the "
                "post, so a message about a held delivery lands on a lot of people "
                "who genuinely are waiting on one.</p>"
                "<p>The safe move is the same as always: do not tap the link in the "
                "message. If you think you might really have a parcel held, open the "
                "carrier's proper website yourself, or use the tracking number from "
                "the actual order confirmation. The scammer's whole plan depends on "
                "you taking the shortcut they provided.</p>"
                "<div class=\"cy-callout\"><strong>Have a look:</strong> below are two "
                "texts about a parcel, side by side. One is genuine and one is a "
                "scam. Read the addresses closely, then tap the one you should not "
                "trust.</div>",
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
                "body": "<p>The thread running through this whole lesson is simple, "
                "and it is worth saying in one sentence you can keep. When a message "
                "pressures you, slow down and verify on a channel you already "
                "trust.</p>"
                "<p>The important words there are 'already trust'. Do not use the "
                "phone number or the link in the suspicious message itself, because a "
                "scammer supplies their own, and it leads straight back to them. Ring "
                "the number you have had for years, or the one printed on a past "
                "invoice, or type the real web address in yourself. You are not being "
                "rude or paranoid by checking. You are doing exactly what a careful "
                "professional does.</p>",
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
        "reading_time_minutes": 10,
        "intro": "The practical protections, one at a time: set the router up "
        "properly, build a password worth trusting, add a second key, and make sure "
        "the Wi-Fi and the login page in front of you are the real thing.",
        "tasks": [
            {
                "key": "router",
                "kind": "check",
                "points": 2,
                "title": "Your router is the front door",
                "body": "<p>If your workplace were a building, the router would be the "
                "front door. It is the box, sometimes called a modem or a gateway, "
                "that connects everything you do to the internet. Almost all of your "
                "information passes through it, which makes it one of the most "
                "important things to set up properly, and, unfortunately, one of the "
                "most commonly ignored. Plenty of small offices plug it in on day one "
                "and never touch it again.</p>"
                "<p>Here is the part that trips people up. A router has <strong>two "
                "passwords</strong>, and they do very different jobs. The <strong>"
                "Wi-Fi password</strong> is the one everyone types to get online, the "
                "one written on the whiteboard for visitors. The <strong>admin "
                "password</strong> is different. It logs in to the router's own "
                "settings, the control panel that decides how the whole network "
                "behaves, and most people do not even know it exists.</p>"
                "<p>That second one is the quiet, dangerous default. Routers ship with "
                "a standard admin password like 'admin' or 'password', and those "
                "defaults are printed in manuals that anyone can find online in "
                "seconds. Leave it unchanged and a stranger who reaches your router "
                "can change your settings, redirect your traffic, or lock you out of "
                "your own network. Changing it, once, is one of the highest value "
                "five minute jobs in this entire course.</p>"
                "<div class=\"cy-callout\"><strong>A Toowoomba cafe learns the hard "
                "way:</strong> a cafe never changed the admin password on the router "
                "the installer left. A guest with a little know how opened the "
                "settings from a corner table, changed them, and started quietly "
                "intercepting what other customers typed. Nothing looked wrong from "
                "the counter. The fix would have taken five minutes on the first "
                "day.</div>",
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
                "body": "<p>Passwords do not have to be a misery, and most of what "
                "people believe about them is out of date. For years we were told to "
                "make them short and cryptic, full of symbols and swapped letters. It "
                "turns out that advice was backwards.</p>"
                "<p>The single most important thing is <strong>length</strong>. The "
                "way passwords get broken is a computer guessing, at enormous speed, "
                "and every extra character multiplies the number of guesses it has to "
                "make. A short password bristling with symbols, like 'P@ss1!', falls "
                "quickly because it is short. A long password made of a few unrelated "
                "words, like 'copper-lantern-river-desk', is both far stronger and far "
                "easier to remember, because you can picture it. Length beats "
                "cleverness, every time.</p>"
                "<p>The second rule matters just as much: <strong>never reuse a "
                "password</strong> that guards anything you care about. When a website "
                "you signed up to years ago gets breached, and websites are breached "
                "constantly, the leaked passwords are fed into automated tools that "
                "try them everywhere else. One reused password is all it takes to "
                "turn someone else's leak into your problem. A different password for "
                "every important account means one leak stays one leak.</p>"
                "<div class=\"cy-callout\"><strong>You cannot remember dozens of "
                "these, and you are not meant to.</strong> That is what a password "
                "manager is for. It invents a long, unique password for every account "
                "and remembers them all behind one strong master password, so the "
                "only thing you memorise is that one. It is the rare security step "
                "that makes your day easier, not harder.</div>",
                "inline_check": {
                    "question": "Which of these is the strongest office password?",
                    "hint": "Ignore how clever it looks. Count the characters, and ask whether it could be reused or guessed from personal details.",
                    "options": [
                        ("brave-oyster-ladder-comet", True,
                         "Yes. Four unrelated words make it long, which is what actually matters, and it is easy to picture and recall."),
                        ("P@ssw0rd!", False,
                         "It looks tricky but it is short and built on a common word. A computer clears it quickly."),
                        ("Rex2019", False,
                         "A pet's name and a year is short and personal, exactly the kind of thing an attacker guesses first."),
                        ("The same strong password you use for everything", False,
                         "However strong it is, reuse means one leaked website hands over every account at once."),
                    ],
                },
                "body2": "<p>Enough theory. Build one yourself below. Type a password "
                "for the office router and watch the meter explain, as you go, what "
                "is making it weak or strong. Reach Strong to finish the task.</p>",
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
                "body": "<p>Even a long, unique password can be stolen. It can be "
                "phished on a fake page, caught in a website breach, or simply "
                "guessed on an account where someone got lazy. So the sensible "
                "assumption is not 'my password is safe', it is 'what happens the day "
                "my password is not?' That is the question two-factor authentication "
                "answers.</p>"
                "<p>Two-factor, sometimes shown as 2FA, adds a <strong>second key</strong> "
                "on top of your password, usually a short code from an app on your "
                "phone or a prompt you approve. The password is something you know. "
                "The second key is something you have. An attacker on the other side "
                "of the world might steal what you know, but they do not have your "
                "phone in their hand, so the stolen password alone gets them "
                "nowhere.</p>"
                "<p>You do not have to turn it on everywhere at once, and if you only "
                "protect one account, make it your <strong>email</strong>. Email is "
                "the master key of your digital life, because almost every other "
                "account has a 'reset my password, send a link to my email' button. "
                "Someone who controls your inbox can walk into your other accounts one "
                "by one. Lock the inbox with two-factor and you have protected far "
                "more than the inbox.</p>"
                "<div class=\"cy-callout\"><strong>Worth knowing:</strong> a code from "
                "an authenticator app is a bit stronger than one sent by text, "
                "because a text can, in rare cases, be redirected. But any second "
                "factor is a huge step up from a password on its own. Do not let the "
                "choice between them stop you turning something on today.</div>",
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
                "body": "<p>With the router's admin password sorted and a strong "
                "Wi-Fi password in place, three more habits finish the job, and none "
                "of them takes long.</p>"
                "<p>First, use <strong>modern encryption</strong>. In your router's "
                "settings the Wi-Fi security will be listed as WPA3, WPA2 or WEP. "
                "WPA3 and WPA2 are current and fine. WEP is ancient and has been "
                "broken for well over a decade, so if you see it, change it. Second, "
                "turn on a <strong>separate guest network</strong>. It is a second "
                "Wi-Fi name for visitors, and it keeps their phones and laptops walled "
                "off from your work devices, so a stranger's infected phone cannot "
                "reach your systems. Third, let the router and everything on it "
                "<strong>install updates automatically</strong>, because those "
                "updates quietly close security holes before anyone can use them.</p>"
                "<p>One more habit belongs here, because it comes up every day: be "
                "careful on Wi-Fi you do not control. Free Wi-Fi at a cafe or airport "
                "is fine for reading the news, but for anything sensitive, like "
                "banking or logging in to work, use your phone's mobile data or a "
                "trusted connection instead. You cannot see who else is on a public "
                "network or what they can watch.</p>"
                "<div class=\"cy-callout\"><strong>Try it:</strong> a community sports "
                "club is tidying up its Wi-Fi. Sort each habit below into Safe or "
                "Risky. Get all six right and the panel is done.</div>",
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
                "body": "<p>One last skill for the front door, and it is the one that "
                "catches the most people: telling a real login page from a fake copy. "
                "This is where phishing usually ends up. The email or text is just the "
                "bait. The hook is a page that looks exactly like your bank or your "
                "email provider, built to catch your username and password the moment "
                "you type them.</p>"
                "<p>These fakes can be pixel perfect, so do not trust how the page "
                "looks. And here is the myth worth killing: the little <strong>padlock"
                "</strong> in the address bar does not tell you a site is genuine. All "
                "it means is that the connection is encrypted, and scammers encrypt "
                "their fake sites too. A padlock on a scam page is still a scam "
                "page.</p>"
                "<p>The one thing that does not lie is the <strong>web address itself"
                "</strong>. Read it carefully, from the start to the first single "
                "slash. Is it really your bank's address, or a lookalike with the name "
                "buried in the middle of something else? When in doubt, do not use the "
                "link that brought you there. Open a new tab and type the address you "
                "know, or use your own saved bookmark.</p>"
                "<div class=\"cy-callout\"><strong>Test yourself:</strong> below are "
                "two login pages for the same bank, side by side. The padlock is on "
                "both, so ignore it. Read the addresses, then tap the one you should "
                "not trust.</div>",
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
        "reading_time_minutes": 9,
        "intro": "Layer the habits so a single slip is never a disaster, build a "
        "workplace where mistakes get reported instead of hidden, then make the real "
        "calls a small Australian business faces across one week.",
        "tasks": [
            {
                "key": "defence",
                "kind": "check",
                "points": 3,
                "title": "Why you layer your defences",
                "diagram": "defence-in-depth",
                "body": "<p>Here is the idea that pulls the whole module together, and "
                "it has a name worth knowing: <strong>defence in depth</strong>. No "
                "single lock is perfect, and that is completely fine, because you are "
                "not relying on one. You layer several simple habits so that if one is "
                "missed, the next one still protects you.</p>"
                "<p>Watch how the layers cover for each other. A scam email slips past "
                "your attention, but your unique password means it cannot unlock "
                "anything else. The password is phished anyway, but two-factor blocks "
                "the login because the attacker does not have your phone. Somehow "
                "malware still gets a foothold, but automatic updates had already "
                "closed the hole it was aiming for. Each layer is ordinary on its "
                "own. Together they are very hard to get through.</p>"
                "<p>The last and most forgiving layer is <strong>backups</strong>, and "
                "it deserves special attention because it is what saves you when every "
                "other layer has failed. Ransomware works by holding your only copy of "
                "your files hostage and demanding payment. A recent backup that you "
                "have actually tested, and can genuinely restore, removes all their "
                "leverage in an instant. You do not negotiate. You wipe the machine, "
                "restore your files, and carry on with your afternoon.</p>"
                "<div class=\"cy-callout\"><strong>The word 'tested' is doing real "
                "work there.</strong> A backup nobody has ever restored is a hope, not "
                "a plan. Plenty of businesses discover on the worst possible day that "
                "their backup had silently stopped running months ago. Once in a while, "
                "actually restore a file from it, just to be sure it works.</div>",
                "inline_check": {
                    "question": "A convincing scam email gets one of your staff to click and hand over a password. With defence in depth in place, what stops it becoming a break-in?",
                    "hint": "The password is already gone. Which layer sits behind the password and asks for something the attacker does not have?",
                    "options": [
                        ("Two-factor authentication, because the attacker still does not have the second key", True,
                         "Yes. That is the point of layering. One habit failed, the click, but the next one behind it, two-factor, still holds the door."),
                        ("Nothing, once a password is given away the account is lost", False,
                         "Not with layers in place. Two-factor sits behind the password precisely for this moment."),
                        ("The antivirus, which deletes the email", False,
                         "The email already did its job when the password was typed. What protects you now is the second factor at login."),
                        ("A faster internet connection", False,
                         "Speed has nothing to do with it. The layer that saves you here is two-factor."),
                    ],
                },
                "body2": "<p>That is defence in depth in a sentence: assume any single "
                "habit might fail, and make sure the next one behind it still has your "
                "back. Now, one question on the most forgiving layer of all.</p>",
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
                "body": "<p>Every layer you have learned still leaves one thing "
                "uncovered, and it is not technical at all. It is what happens in the "
                "minutes after someone makes a mistake. People will click the wrong "
                "link. They will type a password into a page that turns out to be "
                "fake. The workplaces that come through it well are not the ones "
                "where this never happens. They are the ones where a person can say "
                "'I think I clicked something' without fear.</p>"
                "<p>The reason is timing. Almost every incident is far cheaper to fix "
                "in the first hour than the first week. If a staff member reports a "
                "phished password straight away, the account can be locked and reset "
                "before the attacker does anything with it, and the whole event ends "
                "as a near miss. If they stay quiet out of embarrassment, the "
                "attacker gets days of free rein, and a small slip grows into a real "
                "loss.</p>"
                "<p>So the most valuable thing a workplace can build is not a gadget, "
                "it is a culture where owning up early is welcomed, never punished. "
                "If you are the person who slipped, the best thing you can do for "
                "everyone is say so quickly. And if you are the one being told, the "
                "best thing you can do is say thank you, and fix it together.</p>"
                "<div class=\"cy-callout\"><strong>A school office gets it right:</strong> "
                "an administrator realises the 'urgent payroll update' link they "
                "clicked was a fake, and tells the office manager within minutes. The "
                "password is reset before lunch, nothing comes of it, and nobody is "
                "made to feel small. That is exactly how it is meant to go.</div>",
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
                "body": "<p>Time to put all of it together in the place it actually "
                "lives: a normal working week. You are covering the front desk at a "
                "small dental practice, and over five days a handful of situations "
                "come up that every Australian small business meets sooner or "
                "later.</p>"
                "<p>Make the call you would really make, not the one you think sounds "
                "clever. There are no trick questions here, and if a choice goes "
                "wrong you will see exactly why and get another go at it. This is the "
                "same judgement you have been building all module, just without any "
                "labels telling you which pillar or which habit is in play.</p>",
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
                "body": "<p>That is the whole module, and it comes down to five habits "
                "you can genuinely keep. <strong>Pause</strong> before you act on "
                "anything urgent, because urgency is the scammer's favourite tool. "
                "Use <strong>long, unique passwords</strong> and turn on <strong>"
                "two-factor</strong>, especially on your email. Keep everything "
                "<strong>updated</strong>, ideally automatically. <strong>Back up"
                "</strong> what you cannot afford to lose, and test that you can "
                "restore it. And <strong>report</strong> anything odd quickly, "
                "without blame.</p>"
                "<p>Not one of those needs you to be technical, and you will notice "
                "each one maps straight back to the very first lesson. Pausing and "
                "reporting protect against the human error most attacks rely on. "
                "Passwords and two-factor protect confidentiality. Updates close the "
                "holes. Backups protect availability. The whole module was really one "
                "idea, seen from five practical angles.</p>",
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
# Quiz. A bank of 40 (draw 10 at random), ten per lesson. Four options each,
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
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Which part of a workplace network connects your devices to the internet and passes messages between them?",
            "options": [
                ("The router", True,
                 "Yes. The router is the box that links your devices to each other and out to the internet. Almost everything passes through it."),
                ("The printer", False,
                 "A printer is just one device on the network. It does not connect the office to the internet."),
                ("The antivirus program", False,
                 "Antivirus protects a single device. It is not what connects the network to the internet."),
                ("The spreadsheet software", False,
                 "That is an application you run. It has nothing to do with connecting the network."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A file is perfectly safe on a locked laptop, then a staff member emails it to a supplier. What has changed about the risk?",
            "options": [
                ("The information is now in transit, so it needs different protection than when it sat at rest", True,
                 "Exactly. Moving it across the network changes its state to in transit, which is the moment it can be intercepted or misdirected."),
                ("Nothing, a safe file stays safe wherever it goes", False,
                 "Not so. Once it leaves the laptop it is in transit, a different situation with different risks, like being sent to the wrong person."),
                ("It is now permanently deleted from the laptop", False,
                 "Emailing a copy does not delete the original. The change is that the copy is now moving across the network."),
                ("It becomes impossible to read", False,
                 "It is still perfectly readable. The point is that it is now travelling, which is when in-transit risks apply."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "A stranger reads confidential figures over an employee's shoulder at a shared front desk. Which state was the information in, and which pillar failed?",
            "options": [
                ("In use, and confidentiality failed", True,
                 "Yes. Open on a screen means the data was in use, and someone who should not see it did, which is a confidentiality failure."),
                ("At rest, and availability failed", False,
                 "It was on screen, so it was in use, not at rest, and nobody lost access, so availability did not fail."),
                ("In transit, and integrity failed", False,
                 "It was not moving across the network, and nothing was altered. It was in use, and confidentiality failed."),
                ("In use, and availability failed", False,
                 "The state is right, but nobody was locked out. The problem is that someone saw it, which is confidentiality."),
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
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A scam is sent by text message rather than email. What is this called, and are the warning signs different?",
            "options": [
                ("Smishing, and the tells are the same: a lookalike link, a small fee or threat, and pressure to act now", True,
                 "Yes. SMS phishing is called smishing, and although it feels more personal, the giveaways are exactly the same as in a scam email."),
                ("It is harmless, because texts cannot contain scams", False,
                 "Texts absolutely carry scams. A message on your phone can be just as fake as an email."),
                ("Smishing, and you should always tap the link to check where it goes", False,
                 "The name is right, but never tap the link to check. Open the real website yourself instead."),
                ("Vishing, and it only ever happens over the phone", False,
                 "A scam text is smishing. Vishing is a voice-call scam, which is a different channel."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Why is it risky to click the link inside an unexpected 'parcel on hold' message?",
            "options": [
                ("The link usually leads to a lookalike site built to capture your details or payment", True,
                 "Right. The link is the hook. It sends you to a fake page. Go to the carrier's real website yourself instead."),
                ("Clicking links uses up your mobile data allowance", False,
                 "Data use is not the danger. The danger is where the link takes you and what it asks for."),
                ("Parcel companies never send text messages", False,
                 "Some genuinely do, which is why scammers copy them. The safe move is to check on the real website, not to tap the link."),
                ("It will always install a virus instantly", False,
                 "It does not always install anything. More often it leads to a fake page after your login or card details."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "An email has a perfect company logo but comes from 'no-reply@trust-portal-au.com' and warns access ends in two hours. What is the safest read?",
            "options": [
                ("Treat it as a likely scam: the logo is easy to copy, but the odd domain and the deadline are two classic tells", True,
                 "Yes. A perfect logo proves nothing, while a lookalike domain and an invented deadline are two of the three tells. Verify before acting."),
                ("Trust it, because the logo is exactly right", False,
                 "A logo is trivial to copy, so a perfect one is no reassurance at all. Judge it on the domain and the pressure."),
                ("Trust it, because it has a specific deadline", False,
                 "A tight deadline is a pressure tactic, not a sign of authenticity. It is one of the warning signs, not a green light."),
                ("Reply and ask whether it is genuine", False,
                 "If it is a scam, that just asks the scammer, who will say yes. Verify through a channel you already trust."),
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
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "You have dozens of accounts and cannot remember a unique long password for each. What is the sensible fix?",
            "options": [
                ("Use a password manager, which invents and remembers a unique strong password for every account", True,
                 "Yes. You memorise one strong master password, and the manager handles the rest, so one leaked site cannot unlock the others."),
                ("Use one very strong password for everything so there is less to remember", False,
                 "Reuse is the trap. However strong it is, one breached site then hands over every account at once."),
                ("Write them all on a sticky note by the screen", False,
                 "A sticky note in plain view is a confidentiality failure waiting to happen. A password manager keeps them locked away."),
                ("Keep them short so they are easy to recall", False,
                 "Short passwords are exactly the ones a computer guesses fastest. Length is what makes them strong."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "If you turn on two-factor authentication for only one account first, which should it be?",
            "options": [
                ("Your email, because it can reset the passwords of most of your other accounts", True,
                 "Yes. Email is the master key. Whoever controls it can reset your other logins, so protect it first."),
                ("A shopping site you use once a year", False,
                 "Low value. Start with the account that unlocks the others, which is your email."),
                ("Whichever account you care about least", False,
                 "The opposite. Protect your highest-value account first, and that is usually email."),
                ("It does not matter, they are all the same", False,
                 "They are not equal. Email is special because it can reset so many other accounts."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "A visitor's phone is infected with malware and joins your Wi-Fi. What keeps that problem away from your work computers?",
            "options": [
                ("A separate guest network, which walls visitors' devices off from your work devices", True,
                 "Right. A guest network lets visitors online while keeping their devices, infected or not, separate from your business systems."),
                ("A faster internet plan", False,
                 "Speed does nothing to separate devices. A guest network is what keeps them apart."),
                ("Turning the Wi-Fi password off", False,
                 "An open network is worse, not better. You want a separate, password-protected guest network."),
                ("Nothing can be done once a device is on the Wi-Fi", False,
                 "Plenty can. A guest network is designed for exactly this, keeping guest devices away from your own."),
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
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "With defence in depth in place, a staff member is tricked into giving away their password. What is most likely to stop it becoming a break-in?",
            "options": [
                ("Two-factor authentication, because the attacker still lacks the second key", True,
                 "Yes. That is the value of layering. The click got through, but the next layer, two-factor, still blocks the login."),
                ("Nothing, once a password is handed over the account is lost", False,
                 "Not with layers. Two-factor sits behind the password for exactly this moment."),
                ("A recent backup of the files", False,
                 "Backups help you recover from ransomware, but they do not stop someone logging in with a stolen password. Two-factor does."),
                ("A faster internet connection", False,
                 "Speed is irrelevant here. The layer that saves you is the second factor at login."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "Why does a blame-free culture make a workplace more secure, not less?",
            "options": [
                ("People report mistakes quickly, so accounts can be secured before harm is done", True,
                 "Exactly. Fast, honest reporting turns a slip into a near miss. Blame just teaches people to hide the next one."),
                ("It means nobody has to follow the security habits", False,
                 "Blame-free does not mean rule-free. It means mistakes get reported early rather than hidden."),
                ("It removes the need for two-factor and backups", False,
                 "It works alongside those, not instead of them. Reporting is the layer that limits damage when something slips through."),
                ("Attackers avoid friendly workplaces", False,
                 "Attackers do not care how friendly you are. The benefit is that staff report problems fast so they can be fixed."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Why does testing that you can actually restore a backup matter as much as having one?",
            "options": [
                ("A backup nobody has ever restored may have silently stopped working, and you find out on the worst day", True,
                 "Right. Backups can quietly fail for months. Restoring a file now and then is how you know it will be there when ransomware strikes."),
                ("Testing makes the backup run faster", False,
                 "Speed is not the point. Testing proves the backup actually works so you can rely on it in a crisis."),
                ("A tested backup can never be affected by ransomware", False,
                 "Testing does not make it immune. It confirms the backup is real and restorable, which is what you need."),
                ("You only need to test it once, when you buy it", False,
                 "Backups can fail at any time, so an occasional restore check is worth repeating, not a one-off."),
            ],
        },
    ],
}
