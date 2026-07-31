"""Module 4, Secure Communication Practices: what "secure" really means
(encryption and HTTPS), proving it is you (password managers and MFA), sharing
information without leaking it, and working safely anywhere, ending with a
whole-workspace hardening exercise.

Same shape and standard as Modules 1 to 3 (see docs/module-authoring.md): a
lesson is a scrollable room of collapsible task PANELS. Each panel is a full,
deep task: several teaching paragraphs (what it is, a concrete Australian
example, why it matters, what to do), a diagram where it helps, a callout box
with a specific scenario, sometimes a mid-panel check, then the end interactive.
Points sum to 10 per lesson and bank at lesson end.

Voice: warm, confident, human. Plain Australian English. No em-dashes, no filler,
no repetition. This module goes a level deeper than Module 1's "use long
passwords and 2FA": it explains the how and the why, and nothing is recycled.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "What 'secure' really means",
        "reading_time_minutes": 10,
        "intro": "Before you can communicate securely, it helps to know what secure "
        "actually means. Meet encryption, understand the padlock and its limits, and "
        "see what scrambling your data can and cannot do.",
        "tasks": [
            {
                "key": "what-encryption",
                "kind": "check",
                "points": 2,
                "title": "Encryption: a locked box only the key opens",
                "diagram": "encryption",
                "body": "<p>Almost everything in this module rests on one idea, and it "
                "is a lovely simple one: encryption. To encrypt something is to "
                "scramble it, using a secret key, so that it turns into meaningless "
                "gibberish for anyone who does not have that key. With the key, the "
                "gibberish turns back into the original. Without it, the scrambled "
                "version is useless.</p>"
                "<p>A helpful picture is a locked box. You put a message in, lock it, "
                "and send it across a crowded room. Plenty of people might handle the "
                "box on the way, but none of them can read what is inside, because "
                "only the person at the other end has a key that fits. Encryption is "
                "that box for your digital information, whether it is a message, a "
                "password, or a whole file.</p>"
                "<p>This is the quiet machinery behind most of the security you rely "
                "on without thinking. When your banking app talks to the bank, when a "
                "message app carries a private chat, when a website takes your card "
                "details, encryption is what stops the information being readable to "
                "everyone in between. You do not need to understand the mathematics, "
                "only the promise: scrambled for anyone without the key.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "the whole rest of this module is really about making sure the "
                "sensitive things you send are in a locked box, not a clear one. Once "
                "you can spot the difference between an encrypted channel and an open "
                "one, choosing the safe way to communicate becomes obvious rather than "
                "technical.</div>",
                "question": "What does it mean to encrypt information?",
                "hint": "Think about the locked box. What happens to the information, and who can read it?",
                "options": [
                    ("Scramble it with a key so only someone with the key can read it", True,
                     "Yes. Encryption turns readable information into gibberish for anyone without the key, and back again for anyone with it."),
                    ("Delete it so no one can ever see it", False,
                     "No. Encryption does not delete anything. It scrambles the information so only the right person can read it."),
                    ("Make a backup copy of it", False,
                     "That is a backup. Encryption is about scrambling information so it cannot be read without the key."),
                    ("Send it faster across the internet", False,
                     "Encryption is about privacy, not speed. It scrambles the data so eavesdroppers cannot read it."),
                ],
            },
            {
                "key": "https-padlock",
                "kind": "check",
                "points": 2,
                "title": "The padlock, and what it really means",
                "body": "<p>You have seen the little padlock in the address bar a "
                "thousand times, and you may have been told it means a site is 'safe'. "
                "That is half right, and the half that is wrong is exactly what gets "
                "people into trouble. Let us pin down what it does and does not "
                "promise.</p>"
                "<p>The padlock means the connection is using HTTPS, the secure version "
                "of a web address that begins with https rather than http. The S "
                "stands for secure, and what it secures is the journey. Everything you "
                "send to that site, and everything it sends back, is encrypted along "
                "the way, scrambled so that anyone who intercepts it on the network in "
                "between sees only gibberish.</p>"
                "<p>That protection is real, and it matters most on a shared network. "
                "When you sign in to your bank over HTTPS at a cafe, the stranger two "
                "tables over cannot pluck your password out of the air, because it "
                "left your device already scrambled. Without HTTPS the same login "
                "would travel as plain, readable text. This is why every site handling "
                "anything private uses it, and why a login page with no padlock is a "
                "genuine warning sign.</p>"
                "<div class=\"cy-callout\"><strong>Here is the trap.</strong> The "
                "padlock only promises that the connection is encrypted, not that the "
                "site on the other end is honest. A phishing site can show a padlock "
                "too, because anyone can get HTTPS for free. So the padlock tells you "
                "'no one is eavesdropping on this conversation', not 'this is really "
                "your bank'. A scammer's fake login page can be perfectly encrypted "
                "and perfectly fraudulent at the very same time.</div>",
                "inline_check": {
                    "question": "A phishing site shows the padlock in the address bar. What does that prove?",
                    "hint": "The padlock is about the connection, not about who is on the other end.",
                    "options": [
                        ("Only that the connection is encrypted, not that the site is genuine", True,
                         "Yes. Anyone can get HTTPS, so the padlock means no eavesdropping, not that the site is trustworthy."),
                        ("That the site is definitely safe to log in to", False,
                         "No. A padlock does not vouch for the site's honesty. A scam page can be encrypted and still be a scam."),
                        ("That your antivirus has checked the site", False,
                         "The padlock has nothing to do with antivirus. It only means the connection is encrypted."),
                        ("Nothing at all, the padlock is meaningless", False,
                         "It does mean something useful, that the connection is encrypted. It just does not prove the site is genuine."),
                    ],
                },
                "body2": "<p>So use the padlock for what it is worth and no more. Its "
                "absence on a page asking for a password is a red flag worth heeding. "
                "Its presence is reassurance about eavesdropping only, and you still "
                "read the web address itself to know whether you are really where you "
                "meant to be. Encryption keeps your conversation private; it cannot "
                "vouch for who you are talking to.</p>",
                "question": "What does HTTPS, shown by the padlock, actually protect?",
                "hint": "Think about the journey between you and the site. What can and cannot an eavesdropper see?",
                "options": [
                    ("It encrypts the connection so eavesdroppers on the network cannot read what you send", True,
                     "Yes. HTTPS scrambles the data travelling between you and the site, so someone intercepting it sees only gibberish."),
                    ("It guarantees the website is run by an honest company", False,
                     "No. HTTPS secures the connection, not the site's honesty. A phishing site can use HTTPS too."),
                    ("It scans the website for viruses", False,
                     "No. HTTPS is about encrypting the connection, not scanning for malware."),
                    ("It makes the website load faster", False,
                     "Speed is not the point. HTTPS encrypts the connection so it cannot be read in transit."),
                ],
            },
            {
                "key": "e2ee",
                "kind": "check",
                "points": 2,
                "title": "End-to-end encryption: only the two of you",
                "body": "<p>HTTPS protects the journey between you and a website, but "
                "there is an even stronger form of privacy worth knowing, especially "
                "for messages. It is called end-to-end encryption, and it means a "
                "message is scrambled on your device and can only be unscrambled on "
                "the recipient's device, so that nobody in between can read it. Not an "
                "eavesdropper, and not even the company running the service.</p>"
                "<p>That last part is the key difference. With ordinary email, the "
                "provider can technically read what is in your inbox, and so can anyone "
                "who gains access to it. With an end-to-end encrypted messaging app, "
                "like Signal or WhatsApp, the provider is carrying sealed envelopes it "
                "cannot open. Only the two people in the conversation hold the keys. "
                "For a genuinely private exchange, that is exactly what you want.</p>"
                "<p>The practical takeaway is to match the channel to the sensitivity. "
                "A lunch order can go anywhere. A client's personal details, a "
                "password, a confidential decision, are better shared on a channel you "
                "know is end-to-end encrypted, rather than in a standard email that "
                "sits readable in several mailboxes and servers along the way.</p>"
                "<div class=\"cy-callout\"><strong>Sealed versus readable.</strong> "
                "Picture two ways to send a note. One is a postcard: the postie, the "
                "sorting office and anyone it passes can read it. The other is a sealed "
                "letter only the recipient can open. Standard email is closer to the "
                "postcard; end-to-end encryption is the sealed letter. For anything you "
                "would not write on a postcard, choose the sealed one.</div>",
                "question": "What is special about end-to-end encryption?",
                "hint": "Think about who cannot read the message, including the company carrying it.",
                "options": [
                    ("Only the sender and recipient can read it, not even the service carrying it", True,
                     "Yes. The message is sealed on your device and opened only on theirs, so nobody in the middle, including the provider, can read it."),
                    ("The message is deleted the moment it is read", False,
                     "That is a disappearing-message feature, which is different. End-to-end encryption is about who can read it at all."),
                    ("It makes messages send faster", False,
                     "Speed is not the point. It is about privacy, keeping the content readable only to the two of you."),
                    ("The company can read it to check for spam", False,
                     "The opposite. With end-to-end encryption even the company cannot read the content."),
                ],
            },
            {
                "key": "encryption-limits",
                "kind": "check",
                "points": 2,
                "title": "What encryption cannot do",
                "body": "<p>Encryption is powerful, but it is not magic, and knowing "
                "its limits keeps you from a false sense of safety. It protects "
                "information in specific ways, and leaves other gaps that you cover "
                "with different habits.</p>"
                "<p>First, encryption in transit protects a message on its journey, "
                "but the person at the other end can obviously read it, because that is "
                "the point. Sending your password over an encrypted connection to a "
                "scammer's site still hands the scammer your password. Second, "
                "encryption does not help if your device is unlocked and in the wrong "
                "hands. A logged-in laptop left open on a train shows its contents to "
                "whoever picks it up, encrypted storage or not, because you have "
                "already provided the key by logging in. Third, encryption hides the "
                "contents of a conversation, but often not the fact that it happened, "
                "who spoke to whom and when.</p>"
                "<p>None of this makes encryption less worth having. It simply means "
                "encryption is one layer among several. You still verify who you are "
                "talking to, still lock your screen when you step away, and still think "
                "before you send. Encryption keeps the contents private; your judgement "
                "and your habits do the rest.</p>"
                "<div class=\"cy-callout\"><strong>The unlocked laptop on the "
                "train.</strong> A consultant's laptop uses full encryption, which "
                "sounds reassuring until she leaves it open and logged in on a seat at "
                "Central. Encryption protects the drive when the machine is off and "
                "locked, but she had already unlocked it, so a passer-by could read "
                "everything. A simple auto-lock would have done what encryption alone "
                "could not.</div>",
                "question": "Which of these is a real limit of encryption?",
                "hint": "Think about what encryption does not cover, such as a device you have already unlocked.",
                "options": [
                    ("It does not protect a device that is unlocked and in the wrong hands", True,
                     "Yes. Once you have logged in, you have supplied the key, so an unlocked device shows its contents regardless of encryption."),
                    ("It makes your files impossible to ever open again", False,
                     "No. With the key, encrypted information opens normally. Encryption is reversible for the right person."),
                    ("It stops you from needing any other security habits", False,
                     "The opposite. Encryption is one layer. You still verify, lock your screen, and think before you send."),
                    ("It slows your computer down too much to be useful", False,
                     "Modern encryption is fast and runs unnoticed. Its limits are about scope, not speed."),
                ],
            },
            {
                "key": "encryption-sort",
                "kind": "sort",
                "points": 2,
                "title": "Encrypted, or out in the open?",
                "body": "<p>The skill worth building is a quick instinct for when your "
                "information is travelling in a locked box and when it is out in the "
                "open. Remember the main cues: an https address and its padlock mean "
                "the web connection is encrypted, an end-to-end encrypted app means a "
                "message is sealed, while plain http, standard email content and an "
                "open channel are readable in transit.</p>"
                "<p>Sort the situations below into Encrypted or Out in the open. Get "
                "all six right to finish.</p>",
                "payload": {
                    "prompt": "Sort each situation into Encrypted or Out in the open. All six to finish.",
                    "buckets": [
                        {"id": "encrypted", "label": "Encrypted"},
                        {"id": "open", "label": "Out in the open"},
                    ],
                    "items": [
                        {"id": "https", "text": "Logging in on a site whose address starts with https",
                         "bucket": "encrypted", "why": "HTTPS encrypts the connection, so the login is scrambled in transit."},
                        {"id": "http", "text": "Entering details on a page whose address starts with http",
                         "bucket": "open", "why": "Plain http is not encrypted, so anyone on the network can read what you send."},
                        {"id": "signal", "text": "Messaging a colleague on an end-to-end encrypted app",
                         "bucket": "encrypted", "why": "End-to-end encryption seals the message so only the two of you can read it."},
                        {"id": "postcard", "text": "Sending a Medicare number in the body of a standard email",
                         "bucket": "open", "why": "Standard email is like a postcard, readable in the mailboxes and servers it passes through."},
                        {"id": "bankapp", "text": "Using your bank's official app to check your balance",
                         "bucket": "encrypted", "why": "Banking apps use encrypted connections to protect your data in transit."},
                        {"id": "opennote", "text": "Reading a password a colleague wrote on a shared whiteboard",
                         "bucket": "open", "why": "A password in plain view is as open as it gets, no encryption anywhere."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Proving it is you",
        "reading_time_minutes": 10,
        "intro": "Passwords and the second factor, done properly. Why reuse is the "
        "real danger, how a password manager fixes it, and how multi-factor "
        "authentication stops a stolen password from being enough.",
        "tasks": [
            {
                "key": "reuse-problem",
                "kind": "check",
                "points": 2,
                "title": "Why one leaked password is so dangerous",
                "body": "<p>Module 1 told you to use long, unique passwords. This "
                "lesson is about why the unique part matters so much, and the practical "
                "system that makes it possible. It starts with an attack that turns one "
                "small leak into a large disaster: credential stuffing.</p>"
                "<p>Websites are breached constantly, and when one is, the usernames "
                "and passwords often end up dumped online. Attackers gather these lists "
                "and feed them into automated tools that try each leaked email and "
                "password combination against hundreds of other services: banks, email "
                "providers, shopping sites, social media. The tool does not guess. It "
                "already has your real password from the breached site, and it is "
                "simply checking everywhere else you might have used the same one.</p>"
                "<p>If you reuse passwords, this is devastating, because a leak from a "
                "forum you forgot about in 2016 becomes the key to your email today. If "
                "every account has its own unique password, the same attack fizzles: "
                "the leaked password opens exactly one door, the one that was already "
                "breached, and nothing else. Uniqueness is what contains the "
                "damage.</p>"
                "<div class=\"cy-callout\"><strong>The forgotten forum.</strong> A "
                "Brisbane tradesperson used the same password for a fishing forum and "
                "for his email. The forum was breached years ago, and one quiet night "
                "an automated tool tried that leaked password against his email, walked "
                "straight in, and used it to reset his other accounts. He had done "
                "nothing wrong recently. The reuse from years earlier was the whole "
                "opening.</div>",
                "question": "What is credential stuffing?",
                "hint": "The attacker is not guessing. Where did they get the password, and what do they do with it?",
                "options": [
                    ("Taking passwords leaked from one breach and automatically trying them on many other sites", True,
                     "Yes. It relies on reuse: a password leaked from one place is tried everywhere else you might have used it."),
                    ("Guessing your password by trying random combinations", False,
                     "That is a different attack. Credential stuffing uses real leaked passwords, not random guesses."),
                    ("Flooding a login page with traffic", False,
                     "That is closer to a denial-of-service attack. Credential stuffing reuses leaked passwords across sites."),
                    ("Stuffing extra characters into your password to make it longer", False,
                     "No. It has nothing to do with lengthening passwords. It is about reusing leaked ones across many services."),
                ],
            },
            {
                "key": "password-manager",
                "kind": "check",
                "points": 2,
                "title": "The password manager: the system that makes it work",
                "body": "<p>Here is the honest problem with 'use a different strong "
                "password everywhere'. Nobody can remember fifty unique, random "
                "passwords. Asked to try, people fall back on reuse or on small "
                "variations that attackers expect. The realistic fix is not a better "
                "memory, it is a tool: a password manager.</p>"
                "<p>A password manager is a secure, encrypted vault for all your "
                "passwords. You remember exactly one strong master password to unlock "
                "it, and the manager does the rest. It generates a long, random, unique "
                "password for every account, stores them all safely, and fills them in "
                "for you when you log in. You get uniqueness everywhere without "
                "memorising anything, which is the combination that was impossible by "
                "hand.</p>"
                "<p>There is a quiet security bonus, too. Because the manager fills in "
                "a password only on the exact website it was saved for, it simply will "
                "not offer your bank password on a lookalike phishing site. The manager "
                "is not fooled by a convincing copy the way a hurried human can be, so "
                "it quietly protects you from phishing as well as from reuse.</p>"
                "<div class=\"cy-callout\"><strong>What to look for.</strong> Reputable "
                "password managers are widely available, some free, and many workplaces "
                "provide one. The main thing is to actually use it: let it generate new "
                "passwords as you log in to each site over the coming weeks, rather than "
                "trying to switch everything at once. Start with your most important "
                "accounts, your email and your bank.</div>",
                "inline_check": {
                    "question": "How does a password manager quietly help protect you from phishing?",
                    "hint": "Think about when it will, and will not, offer to fill in a saved password.",
                    "options": [
                        ("It only fills a password on the exact site it was saved for, so it will not offer it on a lookalike", True,
                         "Yes. A manager is not fooled by a convincing copy. If the address is not the real one, it will not autofill, which is a useful warning."),
                        ("It emails you whenever a scam is detected", False,
                         "That is not how it works. Its anti-phishing help comes from only autofilling on the genuine site."),
                        ("It reads your messages to find scams", False,
                         "No. A password manager does not read your messages. It protects you by only filling passwords on the correct site."),
                        ("It makes all your passwords the same so they are easy", False,
                         "The opposite. It gives every account a different password, which is the whole point."),
                    ],
                },
                "body2": "<p>The one thing a password manager asks of you is a strong "
                "master password, because that single password protects all the "
                "others. Make it long and memorable, guard it well, and put a second "
                "factor on the manager itself. You will build that master password in a "
                "couple of panels. First, the second factor.</p>",
                "question": "What is the main benefit of a password manager?",
                "hint": "What does it let you do that memory alone cannot?",
                "options": [
                    ("It lets you have a unique strong password for every account without memorising them", True,
                     "Yes. It generates, stores and fills unique passwords, so a leak from one site cannot unlock the others."),
                    ("It removes the need for any passwords at all", False,
                     "No. It manages your passwords, it does not abolish them. You still have a master password to unlock the vault."),
                    ("It shares your passwords with your colleagues", False,
                     "No. That would undermine security. A manager keeps your passwords private in an encrypted vault."),
                    ("It makes your internet faster", False,
                     "Speed has nothing to do with it. It is about unique, well-managed passwords."),
                ],
            },
            {
                "key": "mfa",
                "kind": "check",
                "points": 2,
                "title": "The second factor, done properly",
                "diagram": "two-factor",
                "body": "<p>Even a strong, unique password can be stolen, phished or "
                "leaked. Multi-factor authentication, often shortened to MFA or 2FA, is "
                "the answer, and it is worth understanding properly rather than just "
                "switching on. It asks for two different kinds of proof: something you "
                "know, your password, and something you have, usually your phone.</p>"
                "<p>The power of combining the two is that they fail in different ways. "
                "An attacker on the other side of the world might steal what you know, "
                "but they do not have your phone in their hand, so the stolen password "
                "on its own gets them nowhere. This one step blocks the overwhelming "
                "majority of account takeovers, because most attacks have only the "
                "password and nothing else.</p>"
                "<p>The accounts to protect first are the ones that unlock the rest. "
                "Turn MFA on for your email above all, because email can reset most "
                "other passwords, then your online banking, then your main work "
                "accounts like Microsoft 365 or Google. These all offer MFA in their "
                "security settings, and enabling it takes a couple of minutes for a "
                "protection that lasts.</p>"
                "<div class=\"cy-callout\"><strong>The stolen password that went "
                "nowhere.</strong> An accounts officer at a Darwin firm had her "
                "Microsoft 365 password phished. The attacker tried to log in from "
                "overseas and was stopped cold at the second step, a prompt on her "
                "phone that she had not approved. The password was genuinely stolen; "
                "MFA made it worthless on its own. Without that second factor, it would "
                "have been game over.</div>",
                "question": "What does multi-factor authentication actually achieve?",
                "hint": "It adds a second kind of proof. What does an attacker with only your password still lack?",
                "options": [
                    ("A stolen password on its own is no longer enough, because a second proof is still required", True,
                     "Yes. MFA asks for something you have as well as something you know, so a leaked password alone will not get in."),
                    ("It makes your password impossible to steal", False,
                     "It does not stop a password being stolen. It makes a stolen one useless without the second factor."),
                    ("It replaces your password entirely", False,
                     "It works alongside your password, adding a second step rather than removing the first."),
                    ("It backs up your account data", False,
                     "That is a backup. MFA is about proving it is really you at login."),
                ],
            },
            {
                "key": "authenticator-vs-sms",
                "kind": "check",
                "points": 1,
                "title": "Authenticator app or text message?",
                "body": "<p>When you switch on MFA, you are usually offered a choice of "
                "second factor: a code texted to your phone, or a code from an "
                "authenticator app you install. Both are a huge improvement on a "
                "password alone, so the most important thing is to turn something on. "
                "But if you have the choice, the app is the stronger option.</p>"
                "<p>The reason is a trick called SIM swapping. An attacker convinces "
                "your phone provider to move your number to a SIM they control, and "
                "from that moment your text-message codes go to them, not you. It is "
                "not common, but it happens, and it targets exactly the people worth "
                "targeting. An authenticator app sidesteps the problem entirely, "
                "because it generates its codes on your device without any text message "
                "to intercept or redirect.</p>"
                "<div class=\"cy-callout\"><strong>The short version.</strong> Any MFA "
                "beats none, so start today with whatever is offered. Where you can "
                "choose, prefer an authenticator app over text-message codes, "
                "especially for your most valuable accounts like email and "
                "banking.</div>",
                "question": "Why is an authenticator app generally a stronger second factor than a texted code?",
                "hint": "Think about a text message being intercepted or a number being taken over.",
                "options": [
                    ("A texted code can be redirected by a SIM swap, while an app generates codes on your device", True,
                     "Yes. The app needs no text message to intercept, so it avoids the SIM-swap weakness that text codes can have."),
                    ("Text-message codes never work at all", False,
                     "They do work and are far better than nothing. The app is simply stronger because it cannot be intercepted by a SIM swap."),
                    ("An app does not need your password anymore", False,
                     "You still use your password. The app is the second factor alongside it, not a replacement."),
                    ("Texts are stronger, so you should always choose them", False,
                     "It is the other way around. The authenticator app is the stronger choice where it is offered."),
                ],
            },
            {
                "key": "master-builder",
                "kind": "password",
                "points": 3,
                "title": "Build your one master password",
                "body": "<p>A password manager reduces the dozens of passwords you need "
                "to remember down to one: the master password that unlocks the vault. "
                "That makes it the single most important password you own, so it is "
                "worth building well. The good news is that the rules are the friendly "
                "ones from Module 1, applied to just this one password.</p>"
                "<p>Length beats complexity. A passphrase of a few unrelated words is "
                "both very strong and easy to remember, far better than a short jumble "
                "of symbols you will forget. It must be unique, used nowhere else, so a "
                "leak somewhere else can never expose it. Build one below, and reach "
                "Strong to finish.</p>",
                "payload": {
                    "prompt": "Type a master password for your vault. Watch the meter explain itself, and reach Strong to finish.",
                    "target": "strong",
                    "common": ["password", "password1", "123456", "12345678", "qwerty",
                               "admin", "letmein", "welcome", "monkey", "iloveyou", "master"],
                    "tips": [
                        "A few unrelated words make a strong, memorable master password.",
                        "Aim for at least twelve characters.",
                        "Use it nowhere else, ever. This one password protects all the others.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Sharing information safely",
        "reading_time_minutes": 9,
        "intro": "Most leaks are not dramatic hacks, they are ordinary information "
        "sent the wrong way. Learn why email is not a vault, how to share files with "
        "care, and how to match the channel to the sensitivity.",
        "tasks": [
            {
                "key": "email-not-a-vault",
                "kind": "check",
                "points": 2,
                "title": "Email is not a vault",
                "body": "<p>Email feels private because it arrives in your personal "
                "inbox, but that feeling is misleading. Standard email was never "
                "designed to be a secure vault, and treating it like one is behind a "
                "great many everyday data leaks. Understanding its weaknesses tells you "
                "when to reach for something better.</p>"
                "<p>An email is more like a postcard than a sealed letter. It passes "
                "through several servers on its way, it lands in a mailbox that other "
                "people or an attacker might access, and it can be forwarded on in a "
                "single click to people you never intended. Worst of all is the "
                "wrong-recipient slip: a name autocompletes to the wrong person, and a "
                "sensitive attachment is gone before you notice. Once sent, an email "
                "cannot truly be unsent.</p>"
                "<p>The practical rule is simple. Do not put genuinely sensitive things "
                "in the body of an ordinary email or attach them casually: passwords, "
                "identity documents, bank details, health information, whole customer "
                "lists. For those, use the safer methods in the next two panels. Email "
                "is wonderful for everyday conversation, and the wrong tool for your "
                "most confidential material.</p>"
                "<div class=\"cy-callout\"><strong>The autocomplete disaster.</strong> "
                "A Ballarat clinic's receptionist meant to send a patient's referral to "
                "Dr Naomi Webb, but the address bar helpfully filled in Naomi Waters, a "
                "former patient with a similar name. The referral, full of private "
                "health details, landed in a stranger's inbox. No hacker was involved. "
                "A sealed, permissioned share instead of an email attachment would have "
                "prevented it.</div>",
                "question": "Why is standard email a poor choice for genuinely sensitive information?",
                "hint": "Think about where it travels, who can access it, and the ease of a wrong-recipient slip.",
                "options": [
                    ("It is more like a postcard: it passes through servers, sits in mailboxes, and is easily sent to the wrong person", True,
                     "Yes. Standard email is not a sealed vault, so sensitive material can be exposed, forwarded, or misdirected."),
                    ("It is too slow for sensitive information", False,
                     "Speed is not the issue. The problem is that email is not private or secure enough for confidential material."),
                    ("Sensitive information cannot be typed into an email at all", False,
                     "You technically can, but you should not, because email is not a secure vault for confidential material."),
                    ("Email is always perfectly secure, so there is no concern", False,
                     "Standard email is not a secure vault. That false confidence is exactly what leads to leaks."),
                ],
            },
            {
                "key": "share-links",
                "kind": "check",
                "points": 2,
                "title": "Share a link, not a copy",
                "body": "<p>When you attach a file to an email, you scatter permanent "
                "copies into every recipient's mailbox, beyond your control forever. A "
                "better approach for anything sensitive is to keep the file in one "
                "secure place and share a link to it, with permissions you control. "
                "This is how business file services like Microsoft 365 and Google "
                "Drive are meant to be used.</p>"
                "<p>A proper share link lets you decide exactly who can open the file, "
                "usually named people rather than 'anyone with the link'. It lets you "
                "choose whether they can only view or also edit. It can be set to "
                "expire, and you can revoke access later if someone leaves or the file "
                "is no longer needed. None of that is possible once a copy has been "
                "emailed out. The guiding idea is least privilege: give each person the "
                "least access that lets them do their job, and no more.</p>"
                "<div class=\"cy-callout\"><strong>Anyone with the link is a "
                "trap.</strong> Convenience often nudges you toward 'anyone with the "
                "link can view', which feels harmless until that link is forwarded, "
                "pasted into a chat, or guessed. For anything sensitive, share to named "
                "people only. A link that works for anyone is a copy waiting to "
                "spread.</div>",
                "inline_check": {
                    "question": "What does 'least privilege' mean when sharing a file?",
                    "hint": "It is about how much access each person gets.",
                    "options": [
                        ("Give each person the least access they need to do their job, and no more", True,
                         "Yes. Least privilege limits exposure: view-only rather than edit, named people rather than anyone, access removed when no longer needed."),
                        ("Give everyone full access so nobody is held up", False,
                         "That is the opposite. Broad access spreads risk. Least privilege keeps access as narrow as the task allows."),
                        ("Only the most senior person may ever open the file", False,
                         "Not quite. It is about matching access to need, not restricting everything to the boss."),
                        ("Share the file with as many people as possible", False,
                         "No. Wider sharing means more exposure. Least privilege deliberately keeps it narrow."),
                    ],
                },
                "body2": "<p>The habit takes a moment and saves a great deal. Before "
                "you share, ask who actually needs this, for how long, and whether they "
                "need to edit or just to read. Then share to those people, with that "
                "access, for that time. It feels a little more deliberate than "
                "attaching a file, and it keeps your information under your control "
                "rather than loose in a dozen inboxes.</p>",
                "question": "Why is sharing a permissioned link usually safer than emailing an attachment?",
                "hint": "Think about control: who can open it, and whether you can change your mind later.",
                "options": [
                    ("You control who can open it, view or edit, and you can expire or revoke access later", True,
                     "Yes. A link keeps the file in one place under your control, unlike copies scattered into inboxes you can never recall."),
                    ("Links are always faster to download", False,
                     "Speed is not the point. The benefit is control over who can access the file and for how long."),
                    ("An attachment cannot contain sensitive information", False,
                     "It certainly can, which is the risk. A permissioned link gives you control that an emailed copy does not."),
                    ("Links can never be shared with the wrong person", False,
                     "They can if set to 'anyone with the link', which is why you share to named people. The control is the advantage, used properly."),
                ],
            },
            {
                "key": "password-protect",
                "kind": "check",
                "points": 2,
                "title": "Lock the file, send the key separately",
                "body": "<p>Sometimes you genuinely do need to send a file rather than "
                "share a link, perhaps to someone outside your organisation. For "
                "anything sensitive, there is a simple way to protect it: lock the file "
                "with a password, and send that password by a different channel from "
                "the file itself.</p>"
                "<p>That second part is the whole trick, and it is called out-of-band "
                "verification. If you email a password-protected file and then email "
                "the password too, anyone who can read the email has both halves, and "
                "you have gained nothing. Instead you send the file by email and the "
                "password by a separate channel: a phone call, a text message, or a "
                "quick word in person. Now an attacker would need to compromise two "
                "different channels to get both the locked file and its key, which is "
                "far harder.</p>"
                "<div class=\"cy-callout\"><strong>Two channels, not one.</strong> A "
                "conveyancer needs to send a client a document with their identity "
                "details. She password-protects the file, emails it, and then rings the "
                "client to read out the password. Even if the email were intercepted, "
                "the file stays locked, because the key travelled by phone. One channel "
                "for the box, another for the key.</div>",
                "question": "You must email a password-protected sensitive file. How should you send the password?",
                "hint": "If the password goes the same way as the file, what have you actually protected?",
                "options": [
                    ("By a separate channel, such as a phone call or text, not in the same email", True,
                     "Yes. Sending the key by a different channel means intercepting the email alone does not unlock the file."),
                    ("In the same email, just below the attachment", False,
                     "That defeats the purpose. Anyone who reads the email then has both the file and its password."),
                    ("In a reply to the same email thread", False,
                     "Still the same channel. If the mailbox is compromised, both halves are there together."),
                    ("There is no need for a password if the file is important", False,
                     "The opposite. An important, sensitive file is exactly the one worth locking, with the key sent separately."),
                ],
            },
            {
                "key": "messaging",
                "kind": "check",
                "points": 1,
                "title": "Match the channel to the message",
                "body": "<p>Pulling the lesson together, the real skill is choosing the "
                "right channel for what you are sending. Not everything needs "
                "fortress-level protection, and treating a lunch order like a state "
                "secret just wears people out. The judgement is to match the care to "
                "the sensitivity.</p>"
                "<p>For everyday chatter, ordinary email or messaging is completely "
                "fine. For genuinely private or personal information, step up: an "
                "end-to-end encrypted messaging app for a quick sensitive note, a "
                "permissioned share for a confidential file, a locked file with the key "
                "sent separately when you must send a copy. The question to ask before "
                "you hit send is simply: if this ended up in the wrong hands, would it "
                "matter? If yes, choose a sealed channel.</p>",
                "question": "What is the sensible way to decide how carefully to send something?",
                "hint": "Should every message get the same treatment, or should the care match the content?",
                "options": [
                    ("Match the care to the sensitivity: everyday chatter is fine anywhere, private information needs a sealed channel", True,
                     "Yes. Ask whether it would matter in the wrong hands. If so, choose an encrypted or permissioned channel."),
                    ("Send everything by the most locked-down method possible", False,
                     "That is exhausting and unnecessary. Reserve the strongest methods for genuinely sensitive information."),
                    ("Send everything by standard email for simplicity", False,
                     "That leaves sensitive material exposed. Standard email is fine for chatter but not for confidential content."),
                    ("It does not matter how you send anything", False,
                     "It does matter for sensitive information. Matching the channel to the content is the whole point."),
                ],
            },
            {
                "key": "share-classify",
                "kind": "classify",
                "points": 3,
                "title": "Safe share, or a leak?",
                "body": "<p>Time to put the judgement into practice. Below are several "
                "ways people share information at work. For each one, decide whether it "
                "is a safe way to handle that information or a leak waiting to "
                "happen.</p>"
                "<p>Lean on the whole lesson: sensitive material belongs in sealed, "
                "controlled channels, while confidential information sent openly or "
                "sprayed widely is a leak, even when it is done with the best of "
                "intentions.</p>",
                "payload": {
                    "prompt": "For each one, choose Safe share or Leak. Get all six to finish.",
                    "categories": [
                        {"id": "safe", "label": "Safe share"},
                        {"id": "leak", "label": "Leak"},
                    ],
                    "events": [
                        {"id": "payroll", "category": "leak",
                         "text": "Emailing the payroll spreadsheet as an attachment to the whole staff mailing list.",
                         "why": "A sensitive file scattered to everyone, beyond recall. That is a leak, however well meant."},
                        {"id": "named-link", "category": "safe",
                         "text": "Sharing a document via a link limited to the two named people who need it.",
                         "why": "Controlled access to named people is a safe, least-privilege share."},
                        {"id": "sms-medicare", "category": "leak",
                         "text": "Texting a client's Medicare number over standard SMS to a colleague.",
                         "why": "Sensitive identity data sent over an open channel. That is a leak."},
                        {"id": "locked-file", "category": "safe",
                         "text": "Sending a password-protected file and phoning the recipient with the password.",
                         "why": "The file is locked and the key travels by a separate channel. That is a safe share."},
                        {"id": "public-post", "category": "leak",
                         "text": "Posting a photo of a signed contract in a public social media group.",
                         "why": "Confidential details put in public view, impossible to recall. A clear leak."},
                        {"id": "approved-share", "category": "safe",
                         "text": "Using the company's approved file service with the link set to expire.",
                         "why": "A controlled, expiring, permissioned share is exactly the safe way to do it."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Working securely anywhere",
        "reading_time_minutes": 9,
        "intro": "The office moves with you now, to cafes, airports and home. Learn "
        "the real risks of public Wi-Fi and the tools that handle them, then secure a "
        "new starter's whole workspace from top to bottom.",
        "tasks": [
            {
                "key": "public-wifi",
                "kind": "check",
                "points": 2,
                "title": "The trouble with public Wi-Fi",
                "body": "<p>Free Wi-Fi at a cafe, an airport or a hotel is genuinely "
                "useful, and it is not the instant disaster some warnings suggest. But "
                "it carries real risks that are worth understanding plainly, so you can "
                "use it sensibly rather than either fearing it or ignoring the "
                "dangers.</p>"
                "<p>The first risk is that you are sharing a network with strangers, "
                "and on a poorly secured public network some of your traffic may be "
                "visible to others on it. Modern HTTPS protects a lot of this, since "
                "encrypted sites stay scrambled even over open Wi-Fi, which is real "
                "reassurance. The sharper risk is the evil twin: an attacker sets up a "
                "hotspot with a friendly, familiar name like 'Airport Free WiFi', and "
                "anyone who connects is routed through the attacker's equipment. You "
                "think you are on the airport's network; you are on theirs.</p>"
                "<p>A related trick is the fake login page, or captive portal, that "
                "asks for an email and password, or even card details, to 'grant "
                "access'. A genuine free network rarely needs your account password. "
                "The safe mindset on any network you do not control is to assume it "
                "might be watched or fake, and to save anything genuinely sensitive for "
                "a channel you trust, which is exactly what the next panel is "
                "about.</p>"
                "<div class=\"cy-callout\"><strong>The friendly hotspot that was "
                "not.</strong> Waiting at a regional airport, a traveller joined "
                "'Airport WiFi Free' and thought nothing of it. It was an evil twin run "
                "from a laptop two seats away, quietly positioned between her and every "
                "site she visited. HTTPS still protected her encrypted logins, but the "
                "safest move would have been not to trust the unknown network for "
                "anything sensitive in the first place.</div>",
                "question": "What is an 'evil twin' in the context of public Wi-Fi?",
                "hint": "Think about a fake network pretending to be a real, trusted one.",
                "options": [
                    ("A fake hotspot with a familiar name, set up so your traffic routes through the attacker", True,
                     "Yes. It mimics a trusted network's name, so people connect to the attacker's equipment believing it is genuine."),
                    ("A second router that speeds up the cafe's internet", False,
                     "No. An evil twin is a malicious fake network, not a performance upgrade."),
                    ("A backup network the venue provides", False,
                     "No. It is a hostile imposter set up by an attacker, not a legitimate backup."),
                    ("Two people using the same password", False,
                     "No. An evil twin is a fake Wi-Fi hotspot impersonating a trusted one."),
                ],
            },
            {
                "key": "wifi-tools",
                "kind": "check",
                "points": 2,
                "title": "The tools that keep you safe on the move",
                "body": "<p>Knowing the risks of public Wi-Fi is only useful if you "
                "know the handful of tools that handle them. The good news is that they "
                "are simple, and you often carry the best one in your pocket.</p>"
                "<p>The simplest is your phone's mobile data, used directly or shared to "
                "your laptop as a personal hotspot. It sidesteps the untrusted network "
                "entirely, because you are on your own mobile connection rather than a "
                "stranger's Wi-Fi. For anything genuinely sensitive on the move, this is "
                "often the easiest safe choice. The second tool is a VPN, a virtual "
                "private network, which wraps all of your traffic in its own layer of "
                "encryption, so that even on a hostile network an eavesdropper sees only "
                "scrambled data. Many workplaces provide one and ask you to use it "
                "outside the office. And the third is the HTTPS you already met: it "
                "keeps individual encrypted sites private even over open Wi-Fi.</p>"
                "<div class=\"cy-callout\"><strong>A simple rule for the road.</strong> "
                "For casual browsing, public Wi-Fi with HTTPS is generally fine. For "
                "anything sensitive, banking, confidential work, logging in to "
                "important accounts, switch to your mobile data or a trusted VPN. And "
                "never enter an account password into a captive portal that a network "
                "asks you to sign in through.</div>",
                "inline_check": {
                    "question": "You need to do some online banking while waiting at a cafe. What is the safest choice?",
                    "hint": "Which option keeps you off the untrusted network for the sensitive task?",
                    "options": [
                        ("Use your phone's mobile data or a trusted VPN instead of the cafe Wi-Fi", True,
                         "Yes. For anything sensitive, use your own mobile connection or a VPN rather than a network you do not control."),
                        ("Use the cafe Wi-Fi, but type quickly", False,
                         "Speed does not make an untrusted network safe. Switch to mobile data or a VPN for banking."),
                        ("Ask the cafe staff for their Wi-Fi password first", False,
                         "A password to join the cafe network does not make it trustworthy for your banking. Use mobile data or a VPN."),
                        ("Turn the screen brightness down so no one sees", False,
                         "The risk is the network carrying your data, not someone reading your screen. Use mobile data or a VPN."),
                    ],
                },
                "body2": "<p>Notice how these tools map onto the ideas from the whole "
                "module. Mobile data avoids the untrusted network, a VPN adds "
                "encryption around everything, and HTTPS encrypts each site. Together "
                "they mean you can work from anywhere without handing your information "
                "to whoever set up the Wi-Fi. The next task puts all of it into "
                "practice at once.</p>",
                "question": "What does a VPN do for you on public Wi-Fi?",
                "hint": "Think about an extra layer of scrambling around all of your traffic.",
                "options": [
                    ("It wraps all your traffic in encryption, so an eavesdropper on the network sees only scrambled data", True,
                     "Yes. A VPN encrypts everything you send, which protects you even on a hostile or untrusted network."),
                    ("It makes the public Wi-Fi faster", False,
                     "Speed is not its job. A VPN adds a protective layer of encryption around your traffic."),
                    ("It hides your screen from people nearby", False,
                     "No. A VPN protects your network traffic, not the physical view of your screen."),
                    ("It removes the need for a password on your accounts", False,
                     "No. A VPN encrypts your connection; it does not change how you log in to accounts."),
                ],
            },
            {
                "key": "harden",
                "kind": "harden",
                "points": 4,
                "title": "Secure the whole workspace",
                "body": "<p>Everything in this module comes together in one practical "
                "job: setting a person up to work securely. Jordan has just started at "
                "a small clinic, keen and capable, but their digital setup is a bit "
                "loose in the way most people's are before anyone helps them tidy "
                "it.</p>"
                "<p>Work down Jordan's workspace below and choose the secure fix for "
                "each part. You are pulling together the whole module: encryption and "
                "the right channels, unique passwords and a manager, multi-factor "
                "authentication, careful sharing, and safe habits on the move. Secure "
                "every part to finish.</p>",
                "payload": {
                    "prompt": "Jordan just started at the clinic and their setup is loose. Secure each part of the workspace. Fix all six to finish.",
                    "steps": [
                        {
                            "id": "email",
                            "label": "Work email",
                            "risk": "Protected by a password only",
                            "options": [
                                {"text": "Turn on multi-factor authentication", "correct": True,
                                 "why": "Now a stolen password alone will not open the inbox, which is the master key to most other accounts."},
                                {"text": "Just make the password a little longer", "correct": False,
                                 "why": "Longer helps, but without a second factor a phished password still walks straight in."},
                            ],
                        },
                        {
                            "id": "passwords",
                            "label": "All those passwords",
                            "risk": "Written on sticky notes under the keyboard",
                            "options": [
                                {"text": "Move them into a password manager", "correct": True,
                                 "why": "The manager stores unique passwords in an encrypted vault, so no more sticky notes and no more reuse."},
                                {"text": "Reuse one memorable password everywhere instead", "correct": False,
                                 "why": "Reuse is the credential-stuffing trap. One leak would then unlock everything. Use a manager."},
                            ],
                        },
                        {
                            "id": "banking",
                            "label": "Online banking",
                            "risk": "Uses the same password as the work email",
                            "options": [
                                {"text": "Give it its own unique password and turn on MFA", "correct": True,
                                 "why": "A unique password plus a second factor means a leak elsewhere cannot reach the bank."},
                                {"text": "Keep the shared password, it is a strong one", "correct": False,
                                 "why": "However strong, a shared password means one leak unlocks both. Make it unique and add MFA."},
                            ],
                        },
                        {
                            "id": "fileshare",
                            "label": "Sharing the client list",
                            "risk": "Emails it as an attachment to a big group",
                            "options": [
                                {"text": "Share a permissioned link with only the people who need it", "correct": True,
                                 "why": "A named, controlled share keeps the sensitive list in one place you can revoke, not scattered into inboxes."},
                                {"text": "Keep emailing it, but write 'confidential' in the subject", "correct": False,
                                 "why": "A label does not protect an attachment that has already been copied into many mailboxes. Share a controlled link instead."},
                            ],
                        },
                        {
                            "id": "wifi",
                            "label": "Working from the cafe",
                            "risk": "Does the banking on the open cafe Wi-Fi",
                            "options": [
                                {"text": "Use a phone hotspot or a trusted VPN for sensitive tasks", "correct": True,
                                 "why": "That keeps the sensitive work off the untrusted network, safe from snooping or an evil twin."},
                                {"text": "Carry on, but log out quickly afterwards", "correct": False,
                                 "why": "Logging out later does not protect what was exposed during the session. Use mobile data or a VPN."},
                            ],
                        },
                        {
                            "id": "laptop",
                            "label": "The laptop itself",
                            "risk": "No screen lock, left open on the desk",
                            "options": [
                                {"text": "Set an auto-lock and require a login to wake it", "correct": True,
                                 "why": "An auto-lock means a laptop left open, or lost, does not simply hand over everything it contains."},
                                {"text": "Leave it unlocked, the office is friendly", "correct": False,
                                 "why": "A friendly office still has visitors and busy moments. An unlocked, logged-in laptop exposes everything on it."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "secure-habits",
                "kind": "check",
                "points": 2,
                "title": "Your secure communication habits",
                "body": "<p>That is the whole module, and it comes down to a short set "
                "of habits you can actually keep. Look for the padlock and understand "
                "it protects the connection, not the site's honesty. Use a password "
                "manager for unique passwords, and turn on multi-factor authentication, "
                "especially for email and banking. Share sensitive information through "
                "sealed, controlled channels rather than open email. And on the move, "
                "use your mobile data or a VPN for anything that matters, and lock your "
                "screen.</p>"
                "<p>None of it requires you to be technical. Each habit is a small, "
                "repeatable choice, and together they mean your communication is "
                "private by default and exposed only when you decide it can be. That is "
                "what secure communication really looks like in an ordinary working "
                "day.</p>",
                "question": "Which habit most directly stops a password leaked from one website from unlocking your other accounts?",
                "hint": "Which habit ensures every account has its own different password?",
                "options": [
                    ("Using a password manager so every account has a unique password", True,
                     "Yes. Unique passwords everywhere mean a leak from one site cannot be reused to open the others."),
                    ("Looking for the padlock before you log in", False,
                     "Checking for HTTPS is a good habit, but it does not stop reuse. Unique passwords do that."),
                    ("Using a VPN on public Wi-Fi", False,
                     "A VPN protects your traffic on untrusted networks, but it does not fix password reuse across sites."),
                    ("Locking your screen when you step away", False,
                     "That protects an unattended device, but it does not stop a leaked password being reused elsewhere."),
                ],
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. A bank of 40 (draw 10 at random), ten per lesson. Four options each,
# exactly one correct, every option carries an explanation that teaches. Fuel for
# the Adaptive Feedback Engine. House voice: warm, plain, no em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: encryption and HTTPS ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does it mean to encrypt information?",
            "options": [
                ("Scramble it with a key so only someone with the key can read it", True,
                 "Yes. Encryption turns readable information into gibberish for anyone without the key."),
                ("Delete it permanently", False,
                 "No. Encryption scrambles information, it does not delete it. The right key restores it."),
                ("Make a backup of it", False,
                 "That is a backup. Encryption is about making information unreadable without the key."),
                ("Compress it to save space", False,
                 "No. That is compression. Encryption is about privacy, not file size."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What does the padlock and HTTPS in a web address tell you?",
            "options": [
                ("The connection is encrypted, so eavesdroppers cannot read what you send", True,
                 "Yes. HTTPS scrambles the data between you and the site. It does not, however, prove the site is honest."),
                ("The website is definitely run by a trustworthy company", False,
                 "No. HTTPS secures the connection, not the site's honesty. Phishing sites can use HTTPS too."),
                ("The website has been scanned for viruses", False,
                 "No. The padlock is about connection encryption, not malware scanning."),
                ("The website will load faster", False,
                 "Speed is not the point. HTTPS encrypts the connection."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "A phishing site displays the padlock. What should you conclude?",
            "options": [
                ("Only that the connection is encrypted; you still must check the address is genuine", True,
                 "Yes. Anyone can get HTTPS, so a padlock does not prove the site is real. The web address is what to verify."),
                ("It must be safe, because scammers cannot get a padlock", False,
                 "They can, and for free. A padlock does not prove a site is legitimate."),
                ("The padlock is fake and means nothing", False,
                 "The padlock is genuine and means the connection is encrypted. It just does not vouch for the site."),
                ("Your device has been infected", False,
                 "A padlock on a page says nothing about infection. It only indicates an encrypted connection."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is special about end-to-end encryption?",
            "options": [
                ("Only the sender and recipient can read the message, not even the service carrying it", True,
                 "Yes. The message is sealed on one device and opened only on the other, so nobody in the middle can read it."),
                ("The message deletes itself after sending", False,
                 "That is a disappearing-message feature. End-to-end encryption is about who can read it at all."),
                ("The provider reads it to filter spam", False,
                 "The opposite. With end-to-end encryption even the provider cannot read the content."),
                ("It only works for photos", False,
                 "No. It protects messages, calls and files, whatever the app supports."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "Compared with a sealed letter, standard email is most like a:",
            "options": [
                ("Postcard that many hands can read along the way", True,
                 "Yes. Standard email passes through servers and mailboxes and is easily forwarded, so it is not private by default."),
                ("Locked safe only you can open", False,
                 "No. Standard email is not a sealed vault. It is closer to a readable postcard."),
                ("Message that self-destructs instantly", False,
                 "No. Email lingers in mailboxes and servers, readable, until deleted."),
                ("Fully end-to-end encrypted channel", False,
                 "Standard email is not end-to-end encrypted. That is what makes it more like a postcard."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "Which is a genuine limit of encryption?",
            "options": [
                ("It does not protect a device that you have already unlocked and left open", True,
                 "Yes. Once you log in you have supplied the key, so an unlocked device exposes its contents regardless of encryption."),
                ("It makes files impossible to open ever again", False,
                 "No. With the key, encrypted data opens normally. It is reversible for the right person."),
                ("It removes the need for any other security habits", False,
                 "The opposite. Encryption is one layer; you still verify, lock your screen and think before sending."),
                ("It only works on weekdays", False,
                 "That makes no sense. Encryption works continuously; its limits are about scope, not time."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "You are about to log in on a page whose address starts with http, not https. You should:",
            "options": [
                ("Be cautious, because the connection is not encrypted and your login could be read in transit", True,
                 "Yes. Without HTTPS the data travels as readable text. A login page with no padlock is a warning sign."),
                ("Proceed, because http is the more secure version", False,
                 "It is the other way around. HTTPS is the secure, encrypted version; plain http is not."),
                ("Assume it is fine as long as the page looks professional", False,
                 "Appearance does not make an unencrypted login safe. The missing encryption is the concern."),
                ("Type faster so no one can intercept it", False,
                 "Speed does not protect unencrypted data. The connection itself is not secured."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "For a genuinely private message, the best channel is one that is:",
            "options": [
                ("End-to-end encrypted, so only you and the recipient can read it", True,
                 "Yes. That keeps the content sealed from everyone in between, including the provider."),
                ("A standard email, because it feels private", False,
                 "Standard email is not sealed. It is readable in the mailboxes and servers it passes through."),
                ("A public social media post", False,
                 "That is the opposite of private. Anyone can read a public post."),
                ("Any channel, since it makes no difference", False,
                 "It makes a real difference. For private content, choose a sealed, encrypted channel."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "HTTPS protects your data while it is:",
            "options": [
                ("Travelling between your device and the website", True,
                 "Yes. HTTPS encrypts the connection, so the data is scrambled in transit."),
                ("Sitting on your unlocked screen", False,
                 "HTTPS does not cover what is visible on your own screen. It protects the connection in transit."),
                ("Being read by the recipient", False,
                 "The recipient can of course read what you sent them. HTTPS protects the journey, not the destination."),
                ("Printed on paper", False,
                 "HTTPS is about network connections, not paper. It protects data in transit online."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Encryption keeps the contents of a conversation private, but it usually does not hide:",
            "options": [
                ("That the conversation happened, and who took part", True,
                 "Yes. Encryption protects the contents, but the fact of a conversation and who was involved may still be visible."),
                ("The words inside the message", False,
                 "The words are exactly what encryption does protect. It is the fact of the exchange that may remain visible."),
                ("Anything at all, since it is useless", False,
                 "Encryption is very useful; it protects the contents. Its limit is that it may not hide that you communicated."),
                ("The colour of your screen", False,
                 "That is not what encryption is about. It protects message contents, not screen appearance."),
            ],
        },
        # ---- Lesson 2: passwords and MFA ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is credential stuffing?",
            "options": [
                ("Taking passwords leaked from one breach and automatically trying them on many other sites", True,
                 "Yes. It relies on reuse: a password leaked from one place is tried everywhere else."),
                ("Guessing passwords by trying random combinations", False,
                 "That is a different attack. Credential stuffing uses real leaked passwords, not random guesses."),
                ("Adding characters to make a password longer", False,
                 "No. It has nothing to do with lengthening passwords. It reuses leaked ones across services."),
                ("Flooding a website with traffic", False,
                 "That is a denial-of-service attack. Credential stuffing reuses leaked credentials."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Why is reusing the same password across sites so risky?",
            "options": [
                ("A leak from any one site can then be used to open all the others", True,
                 "Yes. Reuse turns one breach into a master key for every account that shares the password."),
                ("It makes websites load more slowly", False,
                 "Speed is not the issue. The risk is that one leak unlocks everything."),
                ("It uses more storage on your device", False,
                 "Reuse is not a storage issue. It is a security one: one leak compromises many accounts."),
                ("There is no real risk to reusing passwords", False,
                 "There is a serious risk. Reuse is exactly what credential stuffing exploits."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is the main benefit of a password manager?",
            "options": [
                ("It lets you use a unique strong password for every account without memorising them", True,
                 "Yes. It generates, stores and fills unique passwords, so a leak from one site cannot unlock the rest."),
                ("It removes the need for any passwords", False,
                 "No. You still have a master password to unlock the vault; it manages the rest."),
                ("It shares your passwords with colleagues", False,
                 "No. It keeps your passwords private in an encrypted vault."),
                ("It makes your internet faster", False,
                 "Speed has nothing to do with it. It is about unique, well-managed passwords."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "How does a password manager also help protect you from phishing sites?",
            "options": [
                ("It only autofills a saved password on the exact site it belongs to, not on a lookalike", True,
                 "Yes. If the address is not the genuine one, the manager will not fill the password, which is a useful warning."),
                ("It emails you a warning about every scam", False,
                 "That is not how it helps. Its anti-phishing benefit comes from autofilling only on the real site."),
                ("It reads your emails to detect scams", False,
                 "No. It does not read your email. It fills passwords only on the correct site."),
                ("It makes every password identical for convenience", False,
                 "The opposite. It gives every account a different password."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is multi-factor authentication?",
            "options": [
                ("Requiring a second proof, like a phone code, in addition to your password", True,
                 "Yes. It combines something you know with something you have, so a stolen password alone is not enough."),
                ("Using a much longer password", False,
                 "No. A longer password is still one factor. MFA adds a second, different kind of proof."),
                ("Logging in from multiple devices at once", False,
                 "No. MFA is about proving your identity with more than one factor, not multiple devices."),
                ("Changing your password every day", False,
                 "No. That is a password policy, not MFA. MFA adds a second factor at login."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Which account should you protect with MFA first?",
            "options": [
                ("Your email, because it can reset the passwords of most other accounts", True,
                 "Yes. Email is the master key. Protecting it protects everything it can reset."),
                ("A rarely used shopping account", False,
                 "Lower value. Start with the account that unlocks the others, your email."),
                ("A news site you have no login for", False,
                 "There is little to protect there. Email matters far more."),
                ("Whichever account you use least", False,
                 "The opposite. Protect your highest-value account, your email, first."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Why is an authenticator app generally stronger than SMS codes for MFA?",
            "options": [
                ("A texted code can be redirected by a SIM swap, while an app generates codes on your device", True,
                 "Yes. The app needs no text message to intercept, avoiding the SIM-swap weakness."),
                ("SMS codes do not work at all", False,
                 "They do work and beat a password alone. The app is simply stronger against interception."),
                ("An app means you no longer need a password", False,
                 "You still use your password. The app is the second factor alongside it."),
                ("SMS is stronger, so you should prefer it", False,
                 "It is the other way around. Prefer an authenticator app where offered."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What makes a good master password for a password manager?",
            "options": [
                ("Long and memorable, such as a few unrelated words, and used nowhere else", True,
                 "Yes. Length beats complexity, and uniqueness means a leak elsewhere can never expose it."),
                ("Short but full of symbols", False,
                 "Short passwords are the easiest to crack. Length matters more than a scatter of symbols."),
                ("The same password you use for email", False,
                 "Never reuse it. The master password must be unique, as it protects everything."),
                ("Your pet's name and birth year", False,
                 "Personal details are among the first things an attacker guesses. Use a long unique passphrase."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "An attacker phishes your Microsoft 365 password but you had MFA turned on. What happens?",
            "options": [
                ("The login is blocked, because they still lack the second factor", True,
                 "Yes. MFA means a stolen password on its own cannot get in, which stops most account takeovers."),
                ("They get straight in, because MFA only protects email", False,
                 "MFA protects any account you enable it on, including Microsoft 365. The login is blocked."),
                ("Your files are automatically deleted", False,
                 "MFA does not delete anything. It blocks the login that lacks the second factor."),
                ("Nothing changes, MFA makes no difference", False,
                 "MFA makes a decisive difference here: it blocks a login that has only the stolen password."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Is it not risky to put all your passwords in one password manager, like eggs in one basket?",
            "options": [
                ("The vault is strongly encrypted and can have its own MFA, making it far safer than reuse or sticky notes", True,
                 "Yes. The realistic alternatives, reuse and sticky notes, are far riskier. A protected vault is the safer basket."),
                ("Yes, so it is better to reuse one password everywhere", False,
                 "No. Reuse is exactly the credential-stuffing trap. A protected manager is safer than reusing a password."),
                ("Yes, so passwords are best written on paper", False,
                 "Paper can be lost, seen or copied. An encrypted vault with MFA is a stronger, safer option."),
                ("Yes, so you should avoid passwords altogether", False,
                 "You still need passwords. A manager handles them safely; the concern is outweighed by strong encryption and MFA."),
            ],
        },
        # ---- Lesson 3: sharing safely ----
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why is standard email a poor vault for sensitive information?",
            "options": [
                ("It passes through servers, sits in mailboxes, and is easily sent to the wrong person", True,
                 "Yes. Email is more like a postcard than a sealed vault, so sensitive material can be exposed or misdirected."),
                ("It is too slow for large files", False,
                 "Speed is not the issue. The problem is that email is not private or secure enough for confidential material."),
                ("You cannot type sensitive details into it", False,
                 "You technically can, but you should not, because email is not a secure vault."),
                ("It is always perfectly secure", False,
                 "That false confidence is what leads to leaks. Standard email is not a secure vault."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "Which is the most common way sensitive information leaks by email?",
            "options": [
                ("Sending it to the wrong recipient by mistake", True,
                 "Yes. An autocompleted wrong address is behind a great many everyday data leaks. Once sent, it cannot be unsent."),
                ("The email travelling faster than expected", False,
                 "Speed does not cause leaks. Misdirected messages and casual attachments do."),
                ("Writing in a large font", False,
                 "Font size has nothing to do with it. The risk is exposure and misdirection."),
                ("Using a professional signature", False,
                 "A signature is harmless. The leak risk is sending sensitive material to the wrong person."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why is sharing a permissioned link usually safer than emailing an attachment?",
            "options": [
                ("You control who can open it, can limit view or edit, and can expire or revoke access", True,
                 "Yes. The file stays in one place under your control, unlike copies scattered into inboxes you cannot recall."),
                ("Links always download faster", False,
                 "Speed is not the point. The benefit is control over access."),
                ("An attachment cannot hold sensitive data", False,
                 "It certainly can, which is the risk. A permissioned link gives control an emailed copy does not."),
                ("Links can never reach the wrong person", False,
                 "They can if set to 'anyone with the link', which is why you share to named people."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "What does 'least privilege' mean when sharing files?",
            "options": [
                ("Give each person the least access they need, and no more", True,
                 "Yes. Least privilege limits exposure: view-only over edit, named people over anyone, access removed when done."),
                ("Give everyone full access to avoid hold-ups", False,
                 "That spreads risk. Least privilege deliberately keeps access as narrow as the task allows."),
                ("Only the most senior person may open anything", False,
                 "Not quite. It is about matching access to need, not restricting everything to the boss."),
                ("Share with as many people as possible", False,
                 "No. Wider sharing means more exposure. Least privilege keeps it narrow."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "You email a password-protected file. How should you send the password?",
            "options": [
                ("By a separate channel, such as a phone call or text", True,
                 "Yes. Sending the key by a different channel means intercepting the email alone will not unlock the file."),
                ("In the same email, under the attachment", False,
                 "That defeats the purpose. Anyone reading the email then has both the file and the password."),
                ("In a reply on the same thread", False,
                 "Still the same channel. A compromised mailbox would have both halves."),
                ("You do not need a password on important files", False,
                 "Important, sensitive files are exactly the ones worth locking, with the key sent separately."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "'Out-of-band' verification means:",
            "options": [
                ("Using a second, separate channel to confirm or unlock something", True,
                 "Yes. Sending a file one way and its password another is out-of-band, so one channel alone is not enough."),
                ("Sending everything through the same email", False,
                 "That is in-band, and it defeats the purpose. Out-of-band uses a separate channel."),
                ("Turning off your internet connection", False,
                 "No. Out-of-band is about using a different channel, not going offline."),
                ("Encrypting a file twice", False,
                 "No. It is about the channel you use to send the key, not double encryption."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "How should you decide how carefully to send something?",
            "options": [
                ("Match the care to the sensitivity: chatter can go anywhere, private information needs a sealed channel", True,
                 "Yes. Ask whether it would matter in the wrong hands. If so, choose an encrypted or permissioned channel."),
                ("Send everything the most locked-down way possible", False,
                 "That is exhausting and unnecessary. Reserve the strongest methods for sensitive information."),
                ("Send everything by standard email", False,
                 "That leaves sensitive material exposed. Email is fine for chatter, not for confidential content."),
                ("It never matters how you send anything", False,
                 "It matters for sensitive information. Matching channel to content is the point."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "A colleague asks you to email them a client's full identity details. A safer response is to:",
            "options": [
                ("Share it through a controlled, permissioned channel instead, or lock the file and send the password separately", True,
                 "Yes. Identity details are sensitive, so use a sealed, controlled method rather than a plain email."),
                ("Send it in the email body so it is easy to read", False,
                 "That exposes sensitive data in a channel that is not a vault. Use a controlled or locked method."),
                ("Attach it and mark the email urgent", False,
                 "Urgency does not protect an attachment. Use a permissioned share or a locked file with a separate password."),
                ("Post it in a shared team chat for convenience", False,
                 "That widens exposure. Sensitive identity data belongs in a controlled, sealed channel."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Setting a share link to 'anyone with the link can view' is risky because:",
            "options": [
                ("The link can be forwarded, pasted or guessed, spreading access beyond who you intended", True,
                 "Yes. An open link is a copy waiting to travel. For sensitive files, share to named people only."),
                ("It slows the file down", False,
                 "Speed is not the concern. The risk is uncontrolled access spreading via the link."),
                ("It encrypts the file too strongly", False,
                 "It does not over-encrypt anything. The issue is that anyone with the link can get in."),
                ("It stops the intended people from opening it", False,
                 "It actually lets too many people in, not too few. That is the problem."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "The safest place for genuinely confidential files is:",
            "options": [
                ("A controlled file service with named access and, where possible, expiry", True,
                 "Yes. Controlled, permissioned sharing keeps confidential files under your control rather than loose in inboxes."),
                ("Attached to an email to the whole team", False,
                 "That scatters uncontrolled copies. Use a controlled, permissioned share instead."),
                ("Posted in a public online group", False,
                 "That is the opposite of confidential. Anyone could see it."),
                ("On a USB stick left at reception", False,
                 "That is easily lost or taken. A controlled digital share is far safer."),
            ],
        },
        # ---- Lesson 4: working securely anywhere ----
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "What is an 'evil twin' on public Wi-Fi?",
            "options": [
                ("A fake hotspot with a familiar name, set up so your traffic routes through the attacker", True,
                 "Yes. It mimics a trusted network's name, so people connect to the attacker's equipment thinking it is genuine."),
                ("A second router that boosts the signal", False,
                 "No. An evil twin is a malicious fake network, not a signal booster."),
                ("A backup network the venue runs", False,
                 "No. It is a hostile imposter set up by an attacker."),
                ("Two devices sharing one connection", False,
                 "No. An evil twin is a fake Wi-Fi hotspot impersonating a trusted one."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "You need to do online banking while out at a cafe. The safest choice is to:",
            "options": [
                ("Use your phone's mobile data or a trusted VPN rather than the cafe Wi-Fi", True,
                 "Yes. For anything sensitive, use your own mobile connection or a VPN instead of a network you do not control."),
                ("Use the cafe Wi-Fi but type quickly", False,
                 "Speed does not make an untrusted network safe. Switch to mobile data or a VPN."),
                ("Ask staff for the Wi-Fi password first", False,
                 "A password to join the cafe network does not make it trustworthy for banking."),
                ("Just lower your screen brightness", False,
                 "The risk is the network carrying your data, not someone seeing your screen."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What does a VPN do on public Wi-Fi?",
            "options": [
                ("Wraps all your traffic in encryption, so an eavesdropper sees only scrambled data", True,
                 "Yes. A VPN protects everything you send, even on a hostile or untrusted network."),
                ("Makes the Wi-Fi faster", False,
                 "Speed is not its job. A VPN adds a protective layer of encryption."),
                ("Hides your screen from onlookers", False,
                 "No. A VPN protects your network traffic, not the physical view of your screen."),
                ("Removes the need to log in to accounts", False,
                 "No. A VPN encrypts your connection; it does not change how you log in."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "How much protection does HTTPS give you on an untrusted public network?",
            "options": [
                ("It keeps individual encrypted sites private, but you should still use mobile data or a VPN for sensitive tasks", True,
                 "Yes. HTTPS protects each encrypted site, which is real, but for anything sensitive, add a VPN or use mobile data."),
                ("None at all, so HTTPS is pointless on public Wi-Fi", False,
                 "HTTPS does protect encrypted sites even over open Wi-Fi. It is real, if not complete, protection."),
                ("Complete protection, so no other care is needed", False,
                 "It is not complete. Evil twins and fake portals remain risks, so use a VPN or mobile data for sensitive work."),
                ("It slows the network to keep you safe", False,
                 "HTTPS is not about slowing anything. It encrypts the connection to each site."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "A public network shows a login page asking for your email account password to 'grant access'. You should:",
            "options": [
                ("Not enter your account password, because a genuine free network rarely needs it", True,
                 "Yes. A captive portal asking for an account password is a red flag. Do not hand it over."),
                ("Enter it, since the network needs to verify you", False,
                 "No. A legitimate free network does not need your email password. This is a trap."),
                ("Enter a slightly different password to be safe", False,
                 "Do not enter your account password at all into a network's sign-in page."),
                ("Enter it only if the page looks official", False,
                 "A polished look is easy to fake. Never give an account password to a captive portal."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "Why set your laptop to auto-lock the screen?",
            "options": [
                ("So a device left open or lost does not simply hand over everything on it", True,
                 "Yes. An auto-lock protects an unattended or lost device, which encryption alone cannot do once you are logged in."),
                ("To make the battery last longer", False,
                 "That is a side benefit at best. The security reason is to protect an unattended device."),
                ("To make the laptop faster", False,
                 "Locking the screen is about security, not speed."),
                ("It is not worth doing in a friendly office", False,
                 "Even a friendly office has visitors and busy moments. An auto-lock is a simple, worthwhile protection."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Which habit most directly stops a password leaked from one site unlocking your other accounts?",
            "options": [
                ("Using a password manager so every account has a unique password", True,
                 "Yes. Unique passwords everywhere mean a leak from one site cannot be reused to open the others."),
                ("Looking for the padlock before logging in", False,
                 "A good habit, but it does not stop reuse. Unique passwords do that."),
                ("Using a VPN on public Wi-Fi", False,
                 "A VPN protects traffic on untrusted networks, but it does not fix password reuse."),
                ("Locking your screen when you step away", False,
                 "That protects an unattended device, not against reused passwords."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "For casual browsing on public Wi-Fi, the reasonable approach is:",
            "options": [
                ("It is generally fine over HTTPS, but switch to mobile data or a VPN for anything sensitive", True,
                 "Yes. HTTPS covers casual browsing well; save the stronger tools for banking, logins and confidential work."),
                ("Never use public Wi-Fi for anything, ever", False,
                 "That is stricter than needed. Casual browsing over HTTPS is generally fine."),
                ("Do all your banking on it to save mobile data", False,
                 "No. Sensitive tasks belong on mobile data or a VPN, not an untrusted network."),
                ("Treat it exactly like your home network", False,
                 "A network you do not control deserves more caution than your own."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Which set of habits best sums up secure communication?",
            "options": [
                ("Understand the padlock, use a manager and MFA, share through sealed channels, and use mobile data or a VPN on the move", True,
                 "Yes. Together these keep your communication private by default and exposed only when you decide it can be."),
                ("Rely on a single strong password for everything", False,
                 "Reuse is the core weakness. Use unique passwords via a manager, plus MFA and careful sharing."),
                ("Trust any site that shows a padlock", False,
                 "The padlock only means the connection is encrypted, not that the site is honest. It is one habit among several."),
                ("Avoid computers entirely", False,
                 "Not practical. The workable answer is the set of everyday secure habits."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "Sharing your phone's mobile data to your laptop as a hotspot helps because:",
            "options": [
                ("You are on your own mobile connection, not a stranger's untrusted Wi-Fi", True,
                 "Yes. A personal hotspot sidesteps the untrusted network entirely, which is ideal for sensitive tasks on the move."),
                ("It is always faster than Wi-Fi", False,
                 "Speed varies. The security benefit is avoiding the untrusted public network."),
                ("It encrypts your laptop's hard drive", False,
                 "A hotspot does not encrypt your drive. It keeps you off the untrusted Wi-Fi."),
                ("It removes the need for passwords", False,
                 "It does not change your logins. It simply gives you a connection you control."),
            ],
        },
    ],
}
