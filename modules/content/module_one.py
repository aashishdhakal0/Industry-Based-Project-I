"""Module 1, Network Security Fundamentals: the gold-standard reference content.

This is the module every other module copies, so the shape matters as much as the
words. Kept as plain data (not schema) so it reads like teaching material and the
seed stays re-runnable.

Room format (TryHackMe-style), rebalanced toward DOING: a lesson is a scrollable
room of collapsible task PANELS, and the interactive is the CENTRE of each panel,
not an afterthought. Each panel is a tight setup (a couple of sentences) then a
hands-on task: a sort/classify triage, an inbox to inspect, a spot-the-fake, a
password build, a workspace to harden, a respond-to-the-situation exercise, or a
branching scenario. A few short "apply it" checks remain, framed as real
decisions rather than definitions. The panels' points sum to 10 and bank at
lesson end.

House voice for here and Modules 2 to 6: warm, confident, human. Plain Australian
English for non-technical readers. Reading is kept tight so the doing teaches.
Concrete local scenarios. No em-dashes, no filler.
"""

# --------------------------------------------------------------------------
# Lessons. Each task is a panel: a short `body` (the setup, may include a
# `<div class="cy-callout">` box) then one interactive that carries the learning.
# `check` panels are apply-it decisions (question + hint + four options, tuples of
# (text, is_correct, explanation)); activity panels put the config in `payload`.
# Optional `inline_check` adds a mid-panel apply-it question; `body2` adds a short
# line before the end activity. Points per lesson sum to 10.
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network is, and what you protect",
        "reading_time_minutes": 7,
        "intro": "Meet the thing you are protecting, see where information is "
        "exposed, and sort the three questions security keeps coming back to.",
        "tasks": [
            {
                "key": "net-basics",
                "kind": "check",
                "points": 2,
                "title": "What a network actually is",
                "diagram": "data-travels",
                "body": "<p>A network is just devices connected so they can share "
                "information: the front-desk computer, the printer, the eftpos "
                "machine, all talking through your router and out to the internet. "
                "Most of that information does not sit still. It is on the move, which "
                "is exactly when it can be intercepted if it is not looked after.</p>"
                "<div class=\"cy-callout\">You do not need to run the network to keep "
                "it safe. Nearly all real trouble starts with an everyday choice at "
                "one of these devices, not a clever attack on the wires between "
                "them.</div>",
                "question": "A staff member does each of these. Which one puts information 'on the move' across the network?",
                "hint": "Which action sends information somewhere, rather than leaving it sitting in one place?",
                "options": [
                    ("Emailing a client's file to a supplier", True,
                     "Yes. The moment it is sent, the file is travelling across the internet, which is exactly when it needs protecting in transit."),
                    ("Saving the file to a locked laptop", False,
                     "That leaves it sitting still (at rest) on one device. It is not moving across the network."),
                    ("Printing the file and filing the paper copy", False,
                     "A paper copy in a drawer is at rest, not travelling across the network."),
                    ("Closing the laptop lid for the night", False,
                     "That just leaves the file at rest on the device. Nothing is on the move."),
                ],
            },
            {
                "key": "spot-exposure",
                "kind": "classify",
                "points": 2,
                "title": "Exposed, or protected?",
                "body": "<p>Information is safe in one moment and exposed the next, "
                "depending on where it is and who can reach it. Train your eye on a "
                "normal morning at the front desk. For each moment, decide: is the "
                "information exposed, or protected?</p>",
                "payload": {
                    "prompt": "Tap a moment, then tap Exposed or Protected. Get all six to finish.",
                    "categories": [
                        {"id": "exposed", "label": "Exposed"},
                        {"id": "protected", "label": "Protected"},
                    ],
                    "events": [
                        {"id": "email", "category": "exposed",
                         "text": "A client's file is emailed as an attachment to a supplier.",
                         "why": "On the move across the internet, and one wrong address away from a stranger's inbox. Exposed."},
                        {"id": "screen", "category": "exposed",
                         "text": "The reception screen faces the waiting room, showing a patient's record.",
                         "why": "Anyone waiting can read it over the counter. Information in use, in plain view. Exposed."},
                        {"id": "drawer", "category": "protected",
                         "text": "A laptop is locked and put away in a drawer overnight.",
                         "why": "At rest and secured, out of sight and needing a login. Protected."},
                        {"id": "sticky", "category": "exposed",
                         "text": "The Wi-Fi password is on a sticky note stuck to the monitor.",
                         "why": "In plain view of every visitor to the desk. Exposed."},
                        {"id": "drive", "category": "protected",
                         "text": "A file sits on a drive only staff can open with their login.",
                         "why": "Access is limited to the right people. Protected."},
                        {"id": "counter", "category": "exposed",
                         "text": "Card details are read out loud across a busy counter.",
                         "why": "Anyone within earshot now has them. Exposed."},
                    ],
                },
            },
            {
                "key": "cia-triad",
                "kind": "sort",
                "points": 3,
                "title": "The three questions security asks",
                "diagram": "cia-triad",
                "body": "<p>Almost every security decision comes back to three "
                "questions, known as the CIA triad. Nothing to do with spies. "
                "<strong>Confidentiality</strong>: can only the right people see it? "
                "<strong>Integrity</strong>: is it still accurate and unaltered? "
                "<strong>Availability</strong>: is it there when you need it?</p>",
                "inline_check": {
                    "question": "A supplier's invoice arrives with the bank account number quietly changed. Which pillar has failed?",
                    "hint": "The file opens fine and nobody is locked out. What has changed about it?",
                    "options": [
                        ("Integrity, the information was altered without permission", True,
                         "Yes. It still opens and looks right, but the details were changed behind your back. That is an integrity failure, and exactly how invoice scams work."),
                        ("Availability, you cannot open it", False,
                         "It opens perfectly. The problem is the contents were changed, which is integrity."),
                        ("Confidentiality, someone saw it", False,
                         "The issue is not who saw it, it is that it was altered. That is integrity."),
                        ("Nothing failed", False,
                         "A quietly changed bank account is a classic integrity attack, and it matters a great deal."),
                    ],
                },
                "body2": "<p>Now sort ten real situations by the pillar each one puts "
                "at risk. Watch the last few, they are subtler than they look.</p>",
                "payload": {
                    "prompt": "Tap a situation, then tap the pillar it puts at risk. All ten to finish.",
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
                        {"id": "contract", "text": "A signed contract is quietly edited before it is filed",
                         "bucket": "i", "why": "The agreement itself was altered without permission. That is integrity."},
                        {"id": "perms", "text": "The HR folder's permissions are set so anyone can open it",
                         "bucket": "c", "why": "People who should not see private records now can. That is confidentiality."},
                    ],
                },
            },
            {
                "key": "pillar-respond",
                "kind": "respond",
                "points": 2,
                "title": "Your clinic, three bad mornings",
                "body": "<p>Knowing the pillars is one thing, acting when one fails is "
                "another. Three things go wrong at a small clinic. For each, choose "
                "your first move and see how it plays out.</p>",
                "payload": {
                    "prompt": "Choose the soundest first move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "misfire",
                            "text": "A staff member realises they just emailed the day's patient list to the wrong address.",
                            "options": [
                                {"text": "Tell your manager and IT straight away so it can be handled", "outcome": "good",
                                 "feedback": "Right. A confidentiality slip is far cheaper to handle in the first hour. Owning up fast is the whole game."},
                                {"text": "Delete your sent copy and hope nobody noticed", "outcome": "bad",
                                 "feedback": "Deleting your copy changes nothing at the other end, and the delay only makes it worse. Report it."},
                                {"text": "Email the stranger asking them to delete it, then move on", "outcome": "risky",
                                 "feedback": "Worth asking, but not instead of reporting it. Your manager and IT need to know so it is handled properly."},
                            ],
                        },
                        {
                            "id": "locked",
                            "text": "Every file on the shared drive is suddenly renamed, and a note on screen demands payment.",
                            "options": [
                                {"text": "Disconnect the computer from the network and report it", "outcome": "good",
                                 "feedback": "Exactly. Getting it off the network first stops the ransomware spreading to other machines and the shared drive."},
                                {"text": "Pay quickly to get the files back", "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds crime, and marks you as a payer. Contain it first, then recover from backup."},
                                {"text": "Keep working and hope it stops", "outcome": "bad",
                                 "feedback": "Every second it stays connected, more files and machines are locked. Disconnect first."},
                            ],
                        },
                        {
                            "id": "changed",
                            "text": "An invoice you are about to pay has a bank account that looks different from last month.",
                            "options": [
                                {"text": "Ring the supplier on a number you already have and check", "outcome": "good",
                                 "feedback": "Yes. A changed account plus any pressure to pay is the classic invoice scam. Verify on a channel you already trust."},
                                {"text": "Pay it, the invoice looks genuine", "outcome": "bad",
                                 "feedback": "A tampered invoice looks perfectly genuine. That is the point. Verify the changed details first."},
                                {"text": "Email back to ask if the account really changed", "outcome": "risky",
                                 "feedback": "If the email is a scam, you are asking the scammer. Use a number you already have, not the one in the email."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "cia-recap",
                "kind": "check",
                "points": 1,
                "title": "Which habit protects which pillar?",
                "body": "<p>Every habit in this course defends one of the three "
                "pillars. Matching the habit to the pillar is how you know why it "
                "matters, and that makes it far easier to keep on a busy day.</p>",
                "question": "You want to make sure a ransomware attack can never cost you access to your work. Which habit does that?",
                "hint": "Ransomware locks your only copy. What gives you another one to fall back on?",
                "options": [
                    ("Keeping a tested backup you can actually restore", True,
                     "Yes. A backup protects availability: an attack or a mistake no longer costs you access, because you restore and carry on."),
                    ("Putting a password on the file", False,
                     "A password protects confidentiality (who can see it), not your ability to get it back after ransomware."),
                    ("Checking the invoice's bank details", False,
                     "That protects integrity against tampering. It does nothing about being locked out by ransomware."),
                    ("Nothing can protect against ransomware", False,
                     "A tested backup very much does. It takes away the attacker's entire advantage."),
                ],
            },
        ],
    },
    {
        "title": "How attacks actually happen",
        "reading_time_minutes": 8,
        "intro": "Inspect a real scam, sort the genuine from the fake, and practise "
        "the calls you would make when a message tries to rush you.",
        "tasks": [
            {
                "key": "phishing-inbox",
                "kind": "inbox",
                "points": 3,
                "title": "Take a phishing email apart",
                "diagram": "phishing-email",
                "body": "<p>Scam emails give themselves away in the same few places: a "
                "lookalike sender, a made-up deadline, and a link that does not go "
                "where it claims. Once you know where to look, you can check one in "
                "seconds. Here is one in the shared inbox.</p>",
                "inline_check": {
                    "question": "Of everything in a suspicious email, which single thing is the most reliable to check?",
                    "hint": "Tone and urgency take judgement. One thing is a plain fact sitting right there.",
                    "options": [
                        ("The sender's real address, the part right before the first single slash", True,
                         "Yes. Tone can be faked and logos copied, but the genuine domain is a fact. If it is not the real one, that is your answer."),
                        ("Whether it mentions money", False,
                         "Plenty of genuine emails mention money. On its own it proves nothing."),
                        ("Whether the logo looks right", False,
                         "A logo is trivial to copy, so a perfect one is no comfort. Check the domain."),
                        ("How polite it is", False,
                         "Scammers can be perfectly polite. Politeness is not a safety signal."),
                    ],
                },
                "body2": "<p>Now find every tell yourself. Tap each part that should "
                "give you pause. One of them is sneakier than the rest.</p>",
                "payload": {
                    "prompt": "Tap every part that looks off. Find all of them to finish.",
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
                         "why": "On its own this is just filler. The real tells are the sender, the deadline and the links."},
                        {"id": "track", "zone": "Body",
                         "text": "Track your parcel: auspost.com.au.parcel-track.info/xyz",
                         "bad": True,
                         "why": "The sneaky one. It starts with auspost.com.au but the real address is parcel-track.info. The domain is the part before the first single slash."},
                        {"id": "pay", "zone": "Body",
                         "text": "Pay now at http://auspost-delivery.info/pay",
                         "bad": True,
                         "why": "An emailed payment link on a lookalike site. Never click it. Go to the real website yourself."},
                    ],
                },
            },
            {
                "key": "sms-spot",
                "kind": "spot",
                "points": 2,
                "title": "Spot the scam text",
                "body": "<p>The same tricks arrive by text, and the fakes are getting "
                "closer to the real thing. Two messages about a parcel land on your "
                "phone. Read the addresses closely, then tap the one you should not "
                "trust.</p>",
                "payload": {
                    "prompt": "Two texts about a parcel. Tap the fake.",
                    "left": {
                        "sender": "AusPost",
                        "text": "Your parcel S12 3456 will arrive today 9am to 1pm. "
                        "Track at auspost.com.au/track",
                    },
                    "right": {
                        "sender": "AusPost Info",
                        "text": "Your parcel could not be delivered. Confirm your "
                        "address at auspost.info-track.com to avoid return.",
                    },
                    "fake": "right",
                    "why": "The fake uses a lookalike link (auspost.info-track.com, where the real domain is info-track.com) and pressures you to act. The genuine one gives a delivery window and the proper auspost.com.au address.",
                },
            },
            {
                "key": "scam-triage",
                "kind": "classify",
                "points": 2,
                "title": "Genuine, or a scam?",
                "body": "<p>Scams do not only arrive by email. They come by text and "
                "phone too, mixed in with plenty of genuine messages. Sort a normal "
                "day's worth. For each, decide: genuine, or a scam?</p>",
                "payload": {
                    "prompt": "Tap a message, then tap Genuine or Scam. Get all six to finish.",
                    "categories": [
                        {"id": "genuine", "label": "Genuine"},
                        {"id": "scam", "label": "Scam"},
                    ],
                    "events": [
                        {"id": "colleague", "category": "genuine",
                         "text": "An email from a colleague on your own domain, replying to a thread you started.",
                         "why": "A known sender continuing a real conversation, with no link or pressure. Genuine."},
                        {"id": "parcel", "category": "scam",
                         "text": "A text: 'AUSPOST: parcel held, pay $1.99 now at aus-post-redelivery.co'.",
                         "why": "A lookalike link, a small fee, and a push to hurry. Scam."},
                        {"id": "ato", "category": "scam",
                         "text": "A call: 'This is the ATO. Pay your debt today in gift cards or face arrest.'",
                         "why": "No real government body is ever paid in gift cards, and the threat is a scare tactic. Scam."},
                        {"id": "invoice", "category": "genuine",
                         "text": "An expected invoice from your regular supplier, same bank details as always.",
                         "why": "Expected, from a known supplier, with no change of details or urgency. Genuine."},
                        {"id": "mailbox", "category": "scam",
                         "text": "An email: 'Your mailbox is full. Verify your password here within 24 hours.'",
                         "why": "A manufactured deadline and a request for your password. No IT team asks that. Scam."},
                        {"id": "invite", "category": "genuine",
                         "text": "A calendar invite from your manager for the regular Monday team meeting.",
                         "why": "An expected, routine invite from someone you know. Genuine."},
                    ],
                },
            },
            {
                "key": "human-error",
                "kind": "check",
                "points": 1,
                "title": "Where the real risk sits",
                "body": "<p>Study after study, in Australia and overseas, lands on the "
                "same finding: the biggest risk is not a machine, it is a good person "
                "having a rushed day. Most incidents come down to everyday human "
                "error, a click or a reused password made in a hurry. That is not a "
                "reason for guilt, it is where the leverage is. A calm pause beats any "
                "gadget.</p>",
                "question": "Attackers deliberately build urgency into their messages. Why?",
                "hint": "What does a tight deadline stop you from doing?",
                "options": [
                    ("A rushed person acts before they think or check, which is exactly what the scam needs", True,
                     "Yes. Urgency exists to stop you pausing. Slowing down for ten seconds is a genuine security control, and human error is the biggest risk of all."),
                    ("Deadlines are legally required on invoices", False,
                     "No. The deadline is a pressure tactic, not a legal requirement."),
                    ("It makes the email arrive faster", False,
                     "A deadline in the text does nothing to delivery. It is there to hurry you."),
                    ("Genuine senders always demand instant payment", False,
                     "They usually do not. A sudden 'pay now or else' is a warning sign, not normal business."),
                ],
            },
            {
                "key": "pressure-respond",
                "kind": "respond",
                "points": 2,
                "title": "When a message pushes you",
                "body": "<p>The cure for a pushy message is a habit, not a fact: when "
                "something pressures you to act, slow down and check on a channel you "
                "already trust. Three just landed at the front desk. Handle each "
                "one.</p>",
                "payload": {
                    "prompt": "Choose the soundest response for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "invoice",
                            "text": "An email from your supplier says their bank account has changed, and this month's invoice is now urgent.",
                            "options": [
                                {"text": "Ring the supplier on a number you already have and check", "outcome": "good",
                                 "feedback": "Spot on. A change of bank details always gets verified on a channel you already trust, never the one in the email."},
                                {"text": "Pay it now so the service is not cut off", "outcome": "bad",
                                 "feedback": "That is exactly what the scammer is counting on. A changed account plus urgency is the classic invoice scam, and the money is gone."},
                                {"text": "Reply to the email to ask if it is genuine", "outcome": "risky",
                                 "feedback": "If it is a scam, you are asking the scammer, and they will say yes. Use a number you already have."},
                            ],
                        },
                        {
                            "id": "parcel",
                            "text": "A text says your parcel is held, and to pay a $2.99 fee at a link within 24 hours.",
                            "options": [
                                {"text": "Ignore the link and check the carrier's real app or website yourself", "outcome": "good",
                                 "feedback": "Yes. Go the front way. Real carriers do not chase small fees through a text link."},
                                {"text": "Tap the link and pay the small fee", "outcome": "bad",
                                 "feedback": "The tiny fee and the deadline are the bait. The link goes to a lookalike site built to take your card."},
                                {"text": "Reply STOP to make it go away", "outcome": "risky",
                                 "feedback": "Replying just tells them the number is live. Do not engage, check through the real app."},
                            ],
                        },
                        {
                            "id": "bankcall",
                            "text": "A caller says they are from your bank's fraud team and need you to confirm your login to 'secure your account'.",
                            "options": [
                                {"text": "Hang up and call the bank back on the number on your card", "outcome": "good",
                                 "feedback": "Exactly. You cannot verify an incoming caller, so hang up and dial a number you already trust."},
                                {"text": "Read out your login so they can help", "outcome": "bad",
                                 "feedback": "Never. A real bank will not ask you to confirm a password or code. That is the scam itself."},
                                {"text": "Ask them to prove who they are first", "outcome": "risky",
                                 "feedback": "A practised scammer will happily reel off convincing details. You still cannot verify them. Hang up and call back."},
                            ],
                        },
                    ],
                },
            },
        ],
    },
    {
        "title": "Locking your front door",
        "reading_time_minutes": 8,
        "intro": "The practical protections, done by hand: build a password worth "
        "trusting, secure a new front-desk computer top to bottom, and make the "
        "calls that keep your Wi-Fi and logins safe.",
        "tasks": [
            {
                "key": "password-builder",
                "kind": "password",
                "points": 3,
                "title": "Build a password worth trusting",
                "body": "<p>Passwords do not need to be a misery. Length beats "
                "complexity: a few unrelated words are strong and easy to remember, "
                "far better than a short jumble of symbols. And never reuse one that "
                "guards anything else, or a single leak hands over the lot.</p>",
                "inline_check": {
                    "question": "Which of these is the strongest office password?",
                    "hint": "Ignore how clever it looks. Count the characters, and ask whether it could be reused or guessed.",
                    "options": [
                        ("brave-oyster-ladder-comet", True,
                         "Yes. Four unrelated words make it long, which is what actually matters, and it is easy to picture and recall."),
                        ("P@ssw0rd!", False,
                         "It looks tricky but it is short and built on a common word. A computer clears it quickly."),
                        ("Rex2019", False,
                         "A pet's name and a year is short and personal, exactly what an attacker guesses first."),
                        ("The same strong password you use for everything", False,
                         "However strong, reuse means one leaked website hands over every account at once."),
                    ],
                },
                "body2": "<p>Build one yourself. Type a password for the office router "
                "and watch the meter explain, as you go, what makes it weak or strong. "
                "Reach Strong to finish.</p>",
                "payload": {
                    "prompt": "Type a password for the office router. Reach Strong to finish.",
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
                "key": "harden-frontdesk",
                "kind": "harden",
                "points": 3,
                "title": "Set up the front desk securely",
                "diagram": "two-factor",
                "body": "<p>A new front-desk computer has just been set up, and like "
                "most fresh setups it is a bit loose. Work down it and choose the "
                "secure fix for each part. Lock every one down to finish.</p>",
                "payload": {
                    "prompt": "Secure each part of the new front-desk setup. Fix all six to finish.",
                    "steps": [
                        {
                            "id": "email", "label": "The email account", "risk": "Protected by a password only",
                            "options": [
                                {"text": "Turn on two-factor authentication", "correct": True,
                                 "why": "Now a stolen password alone will not open the inbox, which is the master key to most other accounts."},
                                {"text": "Just make the password a little longer", "correct": False,
                                 "why": "Longer helps, but without a second factor a phished password still walks straight in."},
                            ],
                        },
                        {
                            "id": "passwords", "label": "All the passwords", "risk": "On a sticky note on the monitor",
                            "options": [
                                {"text": "Move them into a password manager", "correct": True,
                                 "why": "The manager keeps unique passwords in an encrypted vault, so no more sticky notes and no more reuse."},
                                {"text": "Reuse one memorable password everywhere", "correct": False,
                                 "why": "Reuse is the trap: one leak then unlocks everything. Use a manager."},
                            ],
                        },
                        {
                            "id": "screen", "label": "The screen", "risk": "Never locks when the desk is left",
                            "options": [
                                {"text": "Set it to auto-lock and need a login to wake", "correct": True,
                                 "why": "An unattended, logged-in screen shows everything to whoever walks up. Auto-lock closes that gap."},
                                {"text": "Leave it, the office is friendly", "correct": False,
                                 "why": "A friendly office still has visitors and busy moments. An open screen exposes whatever is on it."},
                            ],
                        },
                        {
                            "id": "router", "label": "The router", "risk": "Still on its factory admin password",
                            "options": [
                                {"text": "Change it to a strong, unique password", "correct": True,
                                 "why": "Factory admin passwords are published online. Leaving it lets anyone who reaches the router take it over."},
                                {"text": "Leave it, the router is brand new", "correct": False,
                                 "why": "Brand new is exactly when it is on a known default. Change it straight away."},
                            ],
                        },
                        {
                            "id": "guest", "label": "Visitor Wi-Fi", "risk": "Visitors use the same Wi-Fi as the work computers",
                            "options": [
                                {"text": "Turn on a separate guest network", "correct": True,
                                 "why": "A guest network keeps visitors' devices away from your work computers and files."},
                                {"text": "Keep it simple with one network for everyone", "correct": False,
                                 "why": "That puts an unknown visitor device right beside your systems. Separate them."},
                            ],
                        },
                        {
                            "id": "updates", "label": "Updates", "risk": "Set to 'remind me later', always",
                            "options": [
                                {"text": "Turn on automatic updates", "correct": True,
                                 "why": "Updates close security holes. Automatic means the machine protects itself without waiting for someone to remember."},
                                {"text": "Keep dismissing them to avoid interruptions", "correct": False,
                                 "why": "Every dismissed update leaves a known hole open. Let them install automatically."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "login-spot",
                "kind": "spot",
                "points": 2,
                "title": "Real login page, or fake?",
                "body": "<p>Phishing usually ends on a fake login page, a pixel-perfect "
                "copy of your bank or email. The padlock does not help, because scam "
                "sites have one too. The tell is the web address. Here are two for the "
                "same bank. Tap the one you should not trust.</p>",
                "payload": {
                    "prompt": "Your bank's login, or a fake? Tap the one you should not trust.",
                    "variant": "login",
                    "left": {"url": "https://coastline.com.au/login", "brand": "Coastline Bank"},
                    "right": {"url": "https://secure.coastline-bank.com/login", "brand": "Coastline Bank"},
                    "fake": "right",
                    "why": "The padlock is on both, so it proves nothing. The real bank is coastline.com.au. The fake is coastline-bank.com, a different site borrowing the name, and 'secure.' at the front does not change which domain it really is.",
                },
            },
            {
                "key": "wifi-respond",
                "kind": "respond",
                "points": 2,
                "title": "Wi-Fi calls you will actually make",
                "body": "<p>The front-desk Wi-Fi throws up the same few decisions again "
                "and again, usually a sensible option next to a tempting shortcut. "
                "Make the calls you would really make, and see how each one plays "
                "out.</p>",
                "payload": {
                    "prompt": "Choose the soundest option for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "visitor",
                            "text": "A visitor asks for the Wi-Fi password so they can get online while they wait.",
                            "options": [
                                {"text": "Give them the guest network details", "outcome": "good",
                                 "feedback": "Right. The guest network gets them online while keeping their device away from your work systems."},
                                {"text": "Give them the main office Wi-Fi password", "outcome": "bad",
                                 "feedback": "That puts an unknown device on the same network as your computers and files. Use the guest network."},
                                {"text": "Tell them visitors are not allowed on the Wi-Fi at all", "outcome": "risky",
                                 "feedback": "Unnecessary, and a bit unfriendly. A guest network is made for exactly this."},
                            ],
                        },
                        {
                            "id": "cafe",
                            "text": "You need to check the business bank account while waiting at a cafe.",
                            "options": [
                                {"text": "Use your phone's mobile data instead of the cafe Wi-Fi", "outcome": "good",
                                 "feedback": "Yes. For anything sensitive, your own mobile data beats a network you do not control."},
                                {"text": "Use the cafe Wi-Fi, just be quick about it", "outcome": "bad",
                                 "feedback": "Being quick does not make an untrusted network safe. Use mobile data for banking."},
                                {"text": "Ask the cafe whether their Wi-Fi is secure", "outcome": "risky",
                                 "feedback": "They will say yes, and it tells you nothing. You cannot trust a network you do not control. Use mobile data."},
                            ],
                        },
                        {
                            "id": "smarttv",
                            "text": "A new smart TV for the waiting room needs to go online.",
                            "options": [
                                {"text": "Put it on the guest network, away from work systems", "outcome": "good",
                                 "feedback": "Right. Smart devices have weak security, so keep them off the network with your computers and files."},
                                {"text": "Connect it to the main network with everything else", "outcome": "bad",
                                 "feedback": "A cheap smart device beside your systems is an easy way in. Put it on the guest network."},
                                {"text": "Leave its default password and connect it to the main network", "outcome": "bad",
                                 "feedback": "Default password and the main network is the worst of both. Change the password and use the guest network."},
                            ],
                        },
                    ],
                },
            },
        ],
    },
    {
        "title": "Putting it all together",
        "reading_time_minutes": 8,
        "intro": "Layer your habits, report without blame, then run a real week at a "
        "small practice where every decision changes how it goes.",
        "tasks": [
            {
                "key": "defence-respond",
                "kind": "respond",
                "points": 2,
                "title": "When one layer fails",
                "diagram": "defence-in-depth",
                "body": "<p>No single lock is perfect, so you layer a few. If one is "
                "missed, the next still protects you. Three things go wrong. Choose "
                "the move that lets the layers do their job.</p>",
                "payload": {
                    "prompt": "Choose the soundest move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "phished",
                            "text": "A convincing scam email got a staff member to type their password into a fake page.",
                            "options": [
                                {"text": "Report it now so the password is reset, trusting two-factor blocked the login", "outcome": "good",
                                 "feedback": "Right. Two-factor means the stolen password alone will not get in, and a fast report gets it reset before anything else."},
                                {"text": "Assume it is fine, the page looked real", "outcome": "bad",
                                 "feedback": "A stolen password is a real problem. Report it so it can be reset, and rely on two-factor holding the door."},
                                {"text": "Wait a week to see if anything happens", "outcome": "risky",
                                 "feedback": "Waiting only gives an attacker time. Report it now so the password is reset."},
                            ],
                        },
                        {
                            "id": "ransom",
                            "text": "Ransomware has encrypted the files, and the attacker demands payment.",
                            "options": [
                                {"text": "Restore from last night's tested backup and do not pay", "outcome": "good",
                                 "feedback": "Exactly. A clean, tested backup takes away the attacker's leverage. You restore and carry on."},
                                {"text": "Pay the ransom to be safe", "outcome": "bad",
                                 "feedback": "Paying is unreliable and funds crime. With a tested backup there is no need to even consider it."},
                                {"text": "Try to unlock the files yourself", "outcome": "risky",
                                 "feedback": "You will not crack strong encryption, and you risk making things worse. Restore from the backup."},
                            ],
                        },
                        {
                            "id": "update",
                            "text": "An update prompt appears on the office computer during a busy morning.",
                            "options": [
                                {"text": "Let it install, updates close security holes", "outcome": "good",
                                 "feedback": "Yes. Updates patch known holes before attackers can use them. A short interruption is worth it."},
                                {"text": "Dismiss it, you are too busy right now", "outcome": "bad",
                                 "feedback": "Every dismissed update leaves a known hole open. Let it install, or set updates to run automatically."},
                                {"text": "Turn off update prompts from now on", "outcome": "bad",
                                 "feedback": "That leaves the machine permanently exposed. Keep updates on, ideally automatic."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "report-respond",
                "kind": "respond",
                "points": 2,
                "title": "Reporting, without the blame",
                "body": "<p>The workplaces that handle security well are the ones where "
                "a person can say 'I think I clicked something' without fear. Fast, "
                "blame-free reporting turns a near miss into a non-event. Three "
                "moments call for it.</p>",
                "payload": {
                    "prompt": "Choose the soundest response for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "clicked",
                            "text": "You clicked a link in an email and only afterwards felt something was off.",
                            "options": [
                                {"text": "Tell IT straight away so the account can be secured", "outcome": "good",
                                 "feedback": "Right. Quick reporting means the account can be secured before any harm is done. There is never trouble for owning up."},
                                {"text": "Say nothing, hoping it was nothing", "outcome": "bad",
                                 "feedback": "Silence just gives a problem room to grow. Report it early."},
                                {"text": "Delete the email so there is no trace", "outcome": "risky",
                                 "feedback": "Deleting the email does not undo the click, and it removes useful detail. Report it instead."},
                            ],
                        },
                        {
                            "id": "colleague",
                            "text": "A colleague quietly tells you they think they fell for a scam.",
                            "options": [
                                {"text": "Thank them and help them report it fast", "outcome": "good",
                                 "feedback": "Exactly. A calm, fast report limits the damage, and treating it well means the next person owns up too."},
                                {"text": "Tell them off for being careless", "outcome": "bad",
                                 "feedback": "Blame teaches people to hide mistakes, which is far more dangerous. Help them report it."},
                                {"text": "Suggest they keep it quiet", "outcome": "bad",
                                 "feedback": "Staying quiet lets a small problem grow into a big one. It needs reporting."},
                            ],
                        },
                        {
                            "id": "popup",
                            "text": "A strange pop-up appears and you are not sure if it is a real problem.",
                            "options": [
                                {"text": "Ask IT rather than guess", "outcome": "good",
                                 "feedback": "Right. When in doubt, ask. A two-minute check settles it without risking a wrong move."},
                                {"text": "Click the pop-up to make it go away", "outcome": "bad",
                                 "feedback": "Clicking an unexpected pop-up can be exactly what it wants. Do not click, ask IT."},
                                {"text": "Ignore it and carry on", "outcome": "risky",
                                 "feedback": "It might be nothing, or a genuine warning. Better to ask than to guess."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "capstone-branch",
                "kind": "branch",
                "points": 4,
                "title": "A week at Docklands Dental",
                "body": "<p>Put it all together. You are on the front desk at a small "
                "dental practice for a week, and the situations every Australian small "
                "business meets come up one by one. Make the call you would really "
                "make. You can always see the better path.</p>",
                "payload": {
                    "prompt": "Choose what you would really do. You can always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "Monday. An email from 'accounts@your-supplier-au.info' says an invoice is overdue and "
                            "the bank account has changed. Pay within the hour or the service stops.",
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
                            "text": "You paid. An hour later the real supplier phones, confused about a payment they never received.",
                            "choices": [{"label": "See what would have worked", "to": "n2"}],
                        },
                        "n2": {
                            "text": "Tuesday. A USB stick labelled 'Staff bonuses' is sitting on the front counter. Nobody knows "
                            "whose it is.",
                            "choices": [
                                {"label": "Plug it in to find out who it belongs to", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "A tempting label on a stray USB is classic bait. Plugging it in can install malware in seconds."},
                                {"label": "Hand it to IT, and do not plug it in", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Right. A found USB goes to IT, never into a work computer. Curiosity is exactly the lever it relies on."},
                            ],
                        },
                        "n2bad": {
                            "text": "The moment it is plugged in, it quietly installs malware that starts spreading across the network.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "Wednesday. A colleague clicks a link in a 'your password expires today' email, types their "
                            "password, then feels uneasy about it.",
                            "choices": [
                                {"label": "Tell them to keep quiet so nobody is in trouble", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "Staying quiet lets a small problem grow. Fast reporting is what limits the damage."},
                                {"label": "Report it to IT now and reset the password", "to": "n4",
                                 "outcome": "good",
                                 "feedback": "Right. Quick reporting turns a near miss into a non-event."},
                            ],
                        },
                        "n3bad": {
                            "text": "Two days later the mailbox is quietly sending scams to all your patients.",
                            "choices": [{"label": "See the better path", "to": "n4"}],
                        },
                        "n4": {
                            "text": "Thursday. Setting up a new laptop, you are offered two-factor authentication on the practice "
                            "email. It is a couple of extra minutes.",
                            "choices": [
                                {"label": "Skip it, everyone is busy", "to": "n4bad",
                                 "outcome": "bad",
                                 "feedback": "Skipping it leaves a stolen password as the only lock on the door."},
                                {"label": "Turn it on now", "to": "n5",
                                 "outcome": "good",
                                 "feedback": "Good. A stolen password on its own will not be enough now."},
                            ],
                        },
                        "n4bad": {
                            "text": "A month later a reused password leaks from another site, and it opens the practice email too.",
                            "choices": [{"label": "See the better path", "to": "n5"}],
                        },
                        "n5": {
                            "text": "Friday. Looking back on the week, which single habit would have prevented the most harm?",
                            "choices": [
                                {"label": "Two-factor authentication on email", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes. A stolen password on its own would not have been enough to get in."},
                                {"label": "A faster internet plan", "to": "n5",
                                 "outcome": "bad",
                                 "feedback": "Speed is not security. Have another go."},
                            ],
                        },
                        "end": {
                            "text": "That is a real week handled. Verify before you pay, never plug in a stray USB, report fast, and "
                            "turn on two-factor. That is network security in practice, and none of it needed jargon.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "habits",
                "kind": "check",
                "points": 2,
                "title": "Which habit fits the moment?",
                "body": "<p>The whole module comes down to a few habits: pause before "
                "you act on anything urgent, use long unique passwords with two-factor, "
                "keep everything updated, back up what you cannot lose, and report "
                "anything odd, fast and without blame.</p>",
                "question": "A colleague's password was stolen by a convincing fake login page. Which habit would stop that stolen password from letting the attacker in?",
                "hint": "Which habit adds a second check the attacker cannot provide?",
                "options": [
                    ("Two-factor authentication", True,
                     "Yes. Two-factor adds a second key, so a stolen password on its own will not get anyone in."),
                    ("Keeping a backup", False,
                     "Backups are vital for recovering from ransomware, but they do not stop a stolen password being used to log in."),
                    ("Installing updates promptly", False,
                     "Updates close software holes, which matters, but they do not add a second check at login."),
                    ("Pausing before urgent requests", False,
                     "A great habit against scams, but two-factor is what specifically blocks a stolen password at login."),
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
