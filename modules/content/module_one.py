"""Module 1, Network Security Fundamentals: the gold-standard reference content.

  Lesson 1  UNDERSTAND IT (a teaching lesson). Four deep reading panels, each
            anchored by a device-framed recreation (own-origin, CSP-safe): what a
            network is and why small business is targeted (net-topology); how data
            travels and what encryption does (data-hops); the CIA triad mapped to
            real Australian incidents plus the Privacy Act NDB duty (cia-triad);
            and the weak points framed against the ASD Essential Eight
            (router-admin). One comprehension check on a lookalike sign-in page.
  Lesson 2  APPLY IT (a hands-on lesson, distinct in character from Lesson 1).
            Where Lesson 1 explains and the learner reads, Lesson 2 hands the
            learner a real artefact to work: the router's live device list
            (netmap), two sign-in pages to tell apart (spot), a trust-account
            inbox to triage (mailsort), an account's security settings to fix
            (harden), and a live incident board when the rent money goes missing
            (tabletop). Same agency, same cast, one day under pressure.

Cast (Yarraville Real Estate, yarravillere.com.au): Dean Whitlock (principal),
Priya Anand (senior property manager), Marion Fisk (trust accountant), Cody
Nguyen (office administrator).

Voice: warm, confident, plain Australian English for non-technical readers. No
em-dashes, no emoji, no filler.

Sources (facts current as cited, framed as general information):
- Australian Signals Directorate, Annual Cyber Threat Report 2024-25
  (cyber.gov.au): over 84,700 cybercrime reports, about one every 6 minutes;
  average self-reported cost of cybercrime per report for small business $56,600.
- ACSC Small Business Cyber Security Guide and the ASD Essential Eight
  (cyber.gov.au).
- OAIC (oaic.gov.au): the Optus (2022) and Medibank (2022) breaches; the
  Notifiable Data Breaches Report, July to December 2024.
Points per lesson sum to 10 and bank at lesson end.
"""

LESSONS = [
    {
        "title": "What a network is, and what you protect",
        "reading_time_minutes": 11,
        "intro": "Start here. Meet the thing you are protecting, follow the exact "
        "path your information takes, learn the three questions security keeps "
        "asking, and see where the weak points are. By the end you will be able to "
        "look at your own network and know what keeps it safe, and why.",
        "tasks": [
            {
                "key": "net-basics",
                "kind": "concept",
                "points": 2,
                "title": "What a network actually is, and why it is a target",
                "diagram": "net-topology",
                "body": "<p>A <strong>network</strong> is simply devices connected so "
                "they can share information. At a small agency like Yarraville Real "
                "Estate that is the reception PC, the trust-account computer, the "
                "printer and everyone's phones, all talking through one "
                "<strong>router</strong> and out to the internet.</p>"
                "<p>Here is the mechanism. Every device on the office network gets a "
                "private <strong>IP address</strong> (a number like 192.168.1.24) "
                "that works like an internal street address, so information reaches "
                "the right machine. When a device needs the internet, its traffic "
                "goes to the router, which swaps the private address for the "
                "office's single public address and sends it on. That swap is why "
                "<strong>every message in or out of the business passes through the "
                "router</strong>. It is the one gateway, the single chokepoint, "
                "which is why so much of security comes down to that one box. Inside "
                "your walls the traffic is on home ground; the moment it leaves the "
                "router it is crossing equipment other people own, and that is where "
                "most of the risk lives.</p>"
                "<p>So why would anyone target a four-person agency? Because modern "
                "attacks are <strong>automated and untargeted</strong>. Criminals "
                "run tools that scan the whole internet continuously, knocking on "
                "every address to find a device with a known weakness or a default "
                "password, then hand the openings to a queue of follow-up attacks. "
                "Nobody picks Yarraville by name. The "
                "<a href=\"https://www.cyber.gov.au/\">Australian Signals Directorate</a> received "
                "<strong>over 84,700 cybercrime reports in 2024-25, about "
                "one every six minutes</strong>, and the average self-reported cost "
                "to a small business was <strong>$56,600 per report</strong>. A "
                "small business with real customer data and light defences is "
                "exactly what those tools are built to find.</p>"
                "<div class=\"cy-callout\">The good news: the same report shows most "
                "incidents use a handful of predictable weaknesses. A few simple "
                "habits, covered in this lesson, shut most of those doors.</div>",
            },
            {
                "key": "data-travels",
                "kind": "concept",
                "points": 2,
                "title": "How your information travels, and what encryption does",
                "diagram": "data-hops",
                "body": "<p>Your information does not sit still. When Cody signs in to "
                "the rent portal or emails a lease, what he types is broken into "
                "small <strong>packets</strong>. Each packet travels from his device, "
                "to the office router, out to the internet provider, across the "
                "<strong>shared public internet</strong>, and finally to a server "
                "somewhere else. Every packet is handed from one piece of equipment "
                "to the next, like a note passed along a chain of strangers, and any "
                "link in that chain can, in principle, read what it carries.</p>"
                "<p>That middle stretch is the catch. The public internet is shared "
                "ground: your packets hop through routers and cables you do not own. "
                "Closer to home, on an open cafe Wi-Fi, everyone on that network can "
                "attempt to read traffic that is not protected. Without protection, "
                "a login travels as plain, readable text, and a listener on the "
                "network simply reads it, password and all.</p>"
                "<p>This is what <strong>encryption</strong> fixes. Before your "
                "information leaves your device it is scrambled with a mathematical "
                "key, so that even if a packet is intercepted it is useless "
                "gibberish, and only the real server holds the key to unscramble it. "
                "This happens automatically on any site using <strong>https</strong>. "
                "You already rely on it every day: before you type a password, look "
                "at the address bar. Plain <strong>http</strong> with no padlock is "
                "open, and the browser now warns you it is <strong>Not secure</strong>. "
                "<strong>https</strong> (the s is for secure) with a small "
                "<strong>padlock</strong> means the connection is encrypted the whole "
                "way between you and that site.</p>"
                "<p>One limit matters more than any other. The padlock proves the "
                "<em>connection</em> is private. It does <em>not</em> prove the "
                "website is genuine. Anyone can get a padlock for a site they own in "
                "minutes, including a criminal running a convincing fake. So treat "
                "the padlock as a green light for privacy, never as a guarantee of "
                "trust. The address itself, read carefully, is what tells you where "
                "you really are.</p>"
                "<div class=\"cy-callout\">Look for https and the padlock before you "
                "type anything sensitive. No padlock, no password. And always read "
                "the address: the padlock protects the pipe, not your judgement "
                "about the site.</div>",
            },
            {
                "key": "cia-triad",
                "kind": "concept",
                "points": 2,
                "title": "The three questions, and three real Australian breaches",
                "diagram": "cia-triad",
                "body": "<p>Security sounds complicated, but underneath it is three "
                "simple questions, known as the <strong>CIA triad</strong> (nothing "
                "to do with spies). Every control in this course defends one of "
                "them, and each maps to a real incident Australians have lived "
                "through.</p>"
                "<p><strong>Confidentiality</strong>: can only the right people see "
                "it? In 2022 the <strong>Optus</strong> breach exposed information on "
                "about <strong>9.8 million</strong> "
                "current and former customers, including, for some, passport and "
                "licence numbers, the raw material for identity theft. Nothing was "
                "locked or changed; private data simply reached people who should "
                "never have had it. For an agency, the equivalent is a tenant's "
                "licence and payslips reaching the wrong inbox.</p>"
                "<div class=\"cy-source\">Source: Optus 2022 data breach, as "
                "reported to the <a href=\"https://www.oaic.gov.au/\">OAIC</a>.</div>"
                "<p><strong>Integrity</strong>: is it accurate and unaltered? A "
                "landlord's payout account, quietly changed in the rent ledger, "
                "fails this. The record still opens perfectly, but the details were "
                "tampered with, which is exactly how payment-redirection scams drain "
                "real money from Australian businesses.</p>"
                "<p><strong>Availability</strong>: is it there when you need it? "
                "Ransomware that locks every file, or a booking system down all "
                "morning, fails this. In the 2022 <strong>Medibank</strong> attack, "
                "sensitive health data on about <strong>9.7 million</strong> "
                "people was stolen and later "
                "published; the attackers reached the network through remote access "
                "that lacked a second factor. The same class of attack routinely "
                "locks a business out of its own systems for days.</p>"
                "<div class=\"cy-source\">Source: Medibank 2022 data breach, "
                "<a href=\"https://www.oaic.gov.au/\">OAIC</a> investigation.</div>"
                "<p>There is a legal side to this too. Under the "
                "<strong>Privacy Act 1988</strong> and the Notifiable Data Breaches "
                "scheme run by the "
                "<a href=\"https://www.oaic.gov.au/\">OAIC</a>, a business that suffers a breach likely "
                "to cause serious harm generally must assess it within "
                "<strong>30 days</strong> and notify both the OAIC and the people "
                "affected. In the OAIC's July to December 2024 figures, "
                "<strong>595 breaches</strong> were "
                "reported, most caused by malicious attacks, with phishing the "
                "leading cause. Getting the three questions right is not just good "
                "practice; for real data it is the law.</p>"
                "<div class=\"cy-callout\">Keep information private, keep it correct, "
                "keep it reachable. Name which one a problem threatens, and you "
                "already understand half of how to respond.</div>",
            },
            {
                "key": "weak-points",
                "kind": "concept",
                "points": 2,
                "title": "Where the weak points are, and the Essential Eight",
                "diagram": "router-admin",
                "body": "<p>Most small networks share the same handful of weak "
                "points, and the same handful of fixes. Start with the "
                "<strong>router</strong>. Its biggest weakness is usually its admin "
                "password still set to the factory default, often just "
                "<strong>admin</strong>. This matters because default passwords are "
                "not secret. Manufacturers print them in manuals and publish them "
                "online, and attackers keep ready-made lists of them, so anyone who "
                "reaches the settings page can look yours up and take over. Changing "
                "it to something strong and unique is the single most important fix "
                "you can make (and you will read a real router settings page in "
                "Lesson 2).</p>"
                "<p>For the rest, the Australian Signals Directorate publishes a "
                "baseline called the <strong>Essential Eight</strong>. You do not "
                "need all of it on day one, but these habits from it and the ACSC "
                "Small Business Guide stop the great majority of trouble, and each "
                "one has a concrete consequence if you skip it:</p>"
                "<ul>"
                "<li><strong>Patch promptly (automatic updates)</strong> on "
                "computers, phones and the router. Most attacks that use a software "
                "flaw use one the maker had already fixed; a device left unpatched "
                "is a known-open door.</li>"
                "<li><strong>Turn on multi-factor authentication (MFA)</strong> for "
                "email and anything that moves money, so a stolen password alone is "
                "not enough. The Medibank attackers reached the network through "
                "remote access that lacked MFA.</li>"
                "<li><strong>Give each person their own account</strong>, never a "
                "shared login, so actions are traceable and one leaked password does "
                "not hand over everything.</li>"
                "<li><strong>Keep regular backups</strong>, with at least one copy "
                "kept offline or off-site, so ransomware or a stolen laptop cannot "
                "take your only path back.</li>"
                "<li><strong>Change default passwords and secure your Wi-Fi</strong> "
                "with WPA2 or WPA3 and a long passphrase, and put visitors on a "
                "separate guest network, so an unknown phone never shares the Wi-Fi "
                "with the accounts computer.</li>"
                "</ul>"
                "<div class=\"cy-callout\">None of this is technical. It is a short "
                "list of settings, done once, that closes most of the doors an "
                "automated attack would ever try.</div>",
            },
            {
                "key": "read-the-address",
                "kind": "check",
                "points": 2,
                "title": "Quick check: is this login page safe?",
                "diagram": "lookalike-login",
                "body": "<p>One quick check to finish, straight from what you just "
                "read about encryption. It is 4:55pm. Cody clicks a link in an email "
                "and lands on the sign-in page above for the agency's rent portal. "
                "The address bar shows a padlock and https. Read the whole address, "
                "then answer.</p>"
                "<div class=\"cy-callout\">The padlock proves the connection is "
                "private. It does not prove the site is genuine. The address is what "
                "tells you where you really are.</div>",
                "question": "The page has a padlock and says https. Is it safe for Cody to type the agency login here?",
                "hint": "Read the web address one character at a time, and compare it to the agency's real domain.",
                "options": [
                    ("No. The padlock only proves the connection is encrypted, not that the site is genuine, and the address is a lookalike (yarravi11ere-payments.com, with number ones for the 'll', and a .com not .com.au). Close it and open the portal from a bookmark", True,
                     "Right. Anyone can get a padlock for a site they own, including a fake one. https protects the pipe, not your judgement about the destination. The tell here is the address: two number ones stand in for the letters, and it is a .com, not the agency's real .com.au."),
                    ("Yes. The padlock and https mean the connection is secure, so the login is safe to enter", False,
                     "No. https and the padlock only mean the connection is encrypted. They say nothing about whether the site is the real one. Criminals get padlocks for fake sites in minutes."),
                    ("Yes. The page loaded with no browser warning, so it is trusted", False,
                     "No. A lookalike phishing page loads perfectly normally, with no warning, because the connection itself is fine. The problem is the destination, not the connection."),
                    ("No, because a real portal would never ask for a password on screen", False,
                     "Not quite. Real portals do ask for a password, and this form looks normal. The actual problem is the lookalike address, not the presence of a login form."),
                ],
            },
        ],
    },
    {
        "title": "Put it to work: a day under pressure",
        "reading_time_minutes": 10,
        "intro": "Now you handle the real thing. Same agency, Yarraville Real "
        "Estate in Melbourne's inner west, run by principal Dean Whitlock with "
        "senior property manager Priya Anand, trust accountant Marion Fisk and "
        "administrator Cody Nguyen. But today is not a quiet day. You will name the "
        "strangers on the office network, tell the real rent portal from a trap, "
        "triage the trust-account inbox, harden an account after a scare, and run "
        "the incident when the rent money goes missing. Less reading, more doing.",
        "tasks": [
            {
                "key": "network-strangers",
                "kind": "netmap",
                "points": 2,
                "title": "Who is on the network?",
                "body": "<p>Lesson 1 showed that a network is just the devices "
                "sharing one connection, so knowing your network means knowing every "
                "device on it. It is 8:05am Monday. Cody opens the router's Attached "
                "Devices page before Yarraville Real Estate opens for the day. The "
                "list is longer than it should be. Tap every device that does not "
                "belong or is a risk.</p>"
                "<div class=\"cy-callout\">Ask of each row: do we own this, and does "
                "the way it joined make sense?</div>",
                "payload": {
                    "prompt": "Tap each device that should not be there. Find both to finish.",
                    "frame": {
                        "tab": "NetGuard R6300 · Devices", "fav": "R", "favbg": "#0f6f78",
                        "url_prefix": "http://", "url": "192.168.1.1", "url_bold": "/devices",
                        "insecure": True,
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "nodes": [
                        {"label": "Front-desk-PC", "detail": "192.168.1.24 · e4:5f:01:9c:2a:7b · Ethernet", "weak": False,
                         "why": "Fine. This is the reception PC, wired in, exactly where it should be."},
                        {"label": "EFTPOS-VX520", "detail": "192.168.1.31 · 00:1b:44:11:3a:b7 · Wi-Fi 2.4GHz", "weak": False,
                         "why": "Fine. The card terminal at the front desk. Known and expected."},
                        {"label": "UNKNOWN-2.4G", "detail": "192.168.1.88 · Guest Wi-Fi · joined 02:14 Sunday", "weak": True,
                         "why": "A stranger. Nobody at the agency was here at 2:14am Sunday, and this device joined the open guest Wi-Fi. Lock down or password the guest network and investigate before opening."},
                        {"label": "HP-LaserJet-M182", "detail": "192.168.1.40 · 3c:52:82:0e:11:9d · Wi-Fi 2.4GHz", "weak": False,
                         "why": "Fine. The office printer."},
                        {"label": "Priya-iPhone", "detail": "192.168.1.52 · a4:83:e7:2c:88:10 · Wi-Fi 5GHz", "weak": False,
                         "why": "Fine. Priya's work phone, a known device."},
                        {"label": "TL-WR841N", "detail": "192.168.1.77 · Wi-Fi repeater · unmanaged", "weak": True,
                         "why": "Nobody at the agency installed a Wi-Fi repeater. An unknown access point on your network can quietly relay or watch traffic. Unplug it and find out how it got there."},
                    ],
                },
            },
            {
                "key": "portal-or-trap",
                "kind": "spot",
                "points": 2,
                "title": "Two portals, one is a trap",
                "body": "<p>Lesson 1 showed how to read a web address and why the "
                "padlock (https) matters. It is 11:40am. Priya gets a text: "
                "\"Yarraville RE: your rent portal login needs re-verification, sign "
                "in here.\" She also has the real portal bookmarked. Two sign-in "
                "pages are open side by side. Tap the one she must not sign in to.</p>"
                "<div class=\"cy-callout\">Two things to read before you type on any "
                "login: the padlock, and the exact domain.</div>",
                "payload": {
                    "prompt": "One of these is safe and one is a trap. Tap the page Priya must not sign in to.",
                    "variant": "login",
                    "fake": "left",
                    "left": {"tab": "Rent Portal: Verify", "url": "yarravillere-tenant.com/verify", "brand": "Rent Portal", "insecure": True},
                    "right": {"tab": "Yarraville Real Estate", "url": "portal.yarravillere.com.au", "brand": "Rent Portal", "insecure": False},
                    "why": "The left page is the trap: it is plain http with no padlock, so anything typed is sent in the clear, and the domain is yarravillere-tenant.com, not the agency's real portal.yarravillere.com.au. The right page has the padlock and the exact real domain. When a login link arrives out of the blue, check the padlock and the domain before you type.",
                },
            },
            {
                "key": "triage-inbox",
                "kind": "mailsort",
                "points": 2,
                "title": "Triage the trust-account inbox",
                "body": "<p>Lesson 1 covered how records get quietly altered "
                "(integrity), and how fake messages try to hook you. It is 9:12am "
                "Tuesday. Marion Fisk, the trust accountant, opens the inbox that "
                "handles rent and landlord payouts. Five emails came in overnight. "
                "Mark each one Genuine or Phishing.</p>"
                "<div class=\"cy-callout\">The dangerous ones ask you to move money or "
                "type a password. Slow down on those.</div>",
                "payload": {
                    "prompt": "Sort every message. Mark each Genuine or Phishing to finish.",
                    "gmail": True,
                    "frame": {
                        "tab": "Inbox · Yarraville RE Mail", "fav": "M", "favbg": "#ea4335",
                        "url_prefix": "https://", "url": "mail.google.com", "url_bold": "/mail/u/0",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "emails": [
                        {"from": "Barbara Nguyen", "addr": "barb.nguyen@outlook.com", "time": "6:48 AM", "unread": True,
                         "subject": "Change my payout account",
                         "preview": "Hi Marion, please update my rent payout to a new account, BSB 083-170 Acct 55 981 402, effective this month.",
                         "phish": True,
                         "why": "A request to change bank details by email is the classic payment-redirection scam. Even when the name looks right, verify by phoning the landlord on the number you already hold, never a number in the email. Changing a payout on an email alone is how agencies lose rent."},
                        {"from": "DocuSign", "addr": "dse@docu-sign-secure.net", "time": "7:15 AM", "unread": True,
                         "subject": "Priya Anand shared a lease for signature",
                         "preview": "Review and sign: Lease_14Bishop_St. This link expires in 24 hours.",
                         "phish": True,
                         "why": "The sender domain is docu-sign-secure.net, not docusign.net. A 24-hour countdown is pressure. Open DocuSign from your own bookmark, not the link in the email."},
                        {"from": "Consumer Affairs Victoria", "addr": "noreply@consumer.vic.gov.au", "time": "8:02 AM", "unread": False,
                         "subject": "Rental bond lodgement confirmation, 14 Bishop St",
                         "preview": "Your bond lodgement has been received by the RTBA. No action is required.",
                         "phish": False,
                         "why": "A real government domain (consumer.vic.gov.au), confirming an action the office already took, and it asks for nothing. Genuine."},
                        {"from": "Microsoft account team", "addr": "account-security@microsoft-verify.co", "time": "8:29 AM", "unread": True,
                         "subject": "Your password will expire today",
                         "preview": "Sign in within 2 hours to keep your account active.",
                         "phish": True,
                         "why": "Microsoft does not send from microsoft-verify.co, and 'expire today, 2 hours' is manufactured urgency. Change a password only from the real Microsoft site, never a link like this."},
                        {"from": "Bright Office Supplies", "addr": "accounts@brightofficesupplies.com.au", "time": "8:51 AM", "unread": False,
                         "subject": "Invoice #4471, October stationery",
                         "preview": "Attached is your invoice for the October order, $186.00, payable to our usual account.",
                         "phish": False,
                         "why": "A known supplier, an order the office placed, the usual payment details, and no request to change anything. Genuine, though it never hurts to sanity-check the amount."},
                    ],
                },
            },
            {
                "key": "harden-account",
                "kind": "harden",
                "points": 2,
                "title": "Fix Priya's account after the scare",
                "body": "<p>Lesson 1 named the Essential Eight, the handful of habits "
                "that stop most attacks. After the fake-portal text, Dean asks you to "
                "review Priya's Microsoft 365 account security at 2:30pm. Four "
                "settings on this page are wrong. For each, choose the fix that "
                "genuinely closes the gap and watch it flip to Secured.</p>"
                "<div class=\"cy-callout\">Pick the option that truly closes the door, "
                "not the one that just looks busy.</div>",
                "payload": {
                    "prompt": "Secure each setting on Priya's account. Lock down all four to finish.",
                    "settings": True,
                    "frame": {
                        "tab": "Security · Microsoft 365", "fav": "365", "favbg": "#0a5ca8",
                        "url_prefix": "https://", "url": "account.microsoft.com", "url_bold": "/security",
                        "marks": [{"label": "Router", "bg": "#0f6f78"}, {"label": "Xero", "bg": "#13b5ea"}, {"label": "Gmail", "bg": "#ea4335"}],
                    },
                    "steps": [
                        {"label": "Multi-factor authentication", "value": "Off",
                         "risk": "A password on its own is one phished text away from letting an attacker in.",
                         "options": [
                            {"text": "Turn on MFA with an authenticator app or a code", "correct": True,
                             "why": "Right. MFA adds a second factor, so a stolen password alone cannot sign in. The Medibank breach began with remote access that had no MFA."},
                            {"text": "Make the password longer instead", "correct": False,
                             "why": "A long password still travels and can still be phished. A second factor is what stops a stolen password being reused. Turn on MFA."},
                            {"text": "Only sign in from the office", "correct": False,
                             "why": "That does not stop a stolen password being used elsewhere. Add MFA so the password alone is not enough."},
                         ]},
                        {"label": "Legacy authentication (IMAP / POP)", "value": "Allowed",
                         "risk": "Old mail protocols can sign in with just a password and skip MFA entirely.",
                         "options": [
                            {"text": "Block legacy authentication", "correct": True,
                             "why": "Right. Legacy protocols bypass MFA, so leaving them on undoes the second factor. Blocking them closes a common backdoor, and staff on modern Outlook are unaffected."},
                            {"text": "Leave it on, staff use Outlook anyway", "correct": False,
                             "why": "An attacker will use the old protocol precisely because it skips MFA. Block it."},
                            {"text": "Change the password monthly", "correct": False,
                             "why": "That does nothing about a protocol that skips the second factor. Block legacy authentication."},
                         ]},
                        {"label": "Automatic Office updates", "value": "Off · 3 versions behind",
                         "risk": "Known security holes stay open until the update that patches them is installed.",
                         "options": [
                            {"text": "Turn on automatic updates", "correct": True,
                             "why": "Right. Patching is Essential Eight core: automatic updates close known holes quickly, without relying on anyone remembering."},
                            {"text": "Update manually when there is time", "correct": False,
                             "why": "Manual updates slip, and the gap between a fix being released and installed is exactly when attacks land. Turn on automatic updates."},
                            {"text": "Skip updates, they cause problems", "correct": False,
                             "why": "Unpatched software is one of the most common ways in. Turn automatic updates on."},
                         ]},
                        {"label": "Account recovery email", "value": "cody.old@hotmail.com",
                         "risk": "A stale recovery address can be used to reset the account into someone else's hands.",
                         "options": [
                            {"text": "Set recovery to Priya's own verified phone and email", "correct": True,
                             "why": "Right. Recovery details are a master key. They must point to the account owner's current, verified contacts, not an old address nobody controls."},
                            {"text": "Leave the old address, it still works", "correct": False,
                             "why": "An old address you do not control is exactly how accounts get hijacked through the reset flow. Update it to Priya's own."},
                            {"text": "Remove recovery details entirely", "correct": False,
                             "why": "With no recovery, a locked-out Priya cannot get back in. The fix is current, verified recovery details, not none."},
                         ]},
                    ],
                },
            },
            {
                "key": "missing-rent",
                "kind": "tabletop",
                "points": 2,
                "title": "4:35pm Friday: the rent that vanished",
                "body": "<p>The last drill, and the real test: when it counts, your "
                "first moves decide how bad it gets. Lesson 1 covered the three "
                "questions security asks and the first move that keeps a problem "
                "small. Work this one live. The board tracks the state of the "
                "business as you act.</p>"
                "<div class=\"cy-callout\">Fast and calm beats clever. Contain the "
                "money, secure the account, preserve the evidence.</div>",
                "payload": {
                    "prompt": "Work the incident phase by phase. The board updates with each call.",
                    "scenario": "Friday 4:35pm. Marion notices the trust ledger is $2,180 short, and landlord Barbara Nguyen emails: \"I still haven't received last month's rent.\" It looks like Tuesday's emailed request to change a payout account was acted on. The money has gone to an account nobody recognises.",
                    "board": [
                        {"id": "money", "label": "Trust funds", "state": "bad", "value": "$2,180 gone"},
                        {"id": "systems", "label": "Portal & mailbox", "state": "warn", "value": "Priya's login suspect"},
                        {"id": "clients", "label": "Landlord (Barbara)", "state": "warn", "value": "Unpaid, asking"},
                        {"id": "clock", "label": "Privacy duty", "state": "warn", "value": "Not yet assessed"},
                    ],
                    "stages": [
                        {"phase": "Contain", "title": "The money is moving",
                         "prompt": "It is 4:36pm on a Friday. What is your first move?",
                         "options": [
                            {"label": "Call the bank's fraud line now to try to recall the $2,180 and freeze the account", "outcome": "good",
                             "consequence": "Right first move. Speed is everything with a redirected payment: banks can sometimes recall or hold funds if you call within the hour. The recall is lodged before the weekend.",
                             "board": {"money": {"state": "warn", "value": "Recall lodged"}}},
                            {"label": "Email Barbara back to ask what account she meant", "outcome": "bad",
                             "consequence": "That burns the crucial first hour and tells you nothing useful. The change did not come from Barbara, it came from an attacker. Phone the bank first.",
                             "board": {"money": {"state": "bad", "value": "Still gone · hour lost"}}},
                            {"label": "Wait until Monday when the office is properly staffed", "outcome": "bad",
                             "consequence": "By Monday the money is cleared and unrecoverable. A redirected payment is an emergency, not a Monday task.",
                             "board": {"money": {"state": "bad", "value": "Cleared · gone"}}},
                         ]},
                        {"phase": "Secure", "title": "Close the way in",
                         "prompt": "The bank is working the recall. The change was authorised from Priya's mailbox. What now?",
                         "options": [
                            {"label": "Reset Priya's password, sign out all her sessions, and confirm MFA is on", "outcome": "good",
                             "consequence": "Right. The attacker had her login. Resetting the password and ending every active session locks them out, and MFA stops the stolen password being reused.",
                             "board": {"systems": {"state": "ok", "value": "Locked down"}}},
                            {"label": "Change Priya's password and leave it there", "outcome": "bad",
                             "consequence": "A password change alone does not end sessions the attacker already has open. Sign out all sessions and confirm MFA too.",
                             "board": {"systems": {"state": "warn", "value": "Sessions still open"}}},
                            {"label": "Nothing yet, IT can look on Monday", "outcome": "bad",
                             "consequence": "Every hour the attacker keeps access they can send more requests. Secure the account now.",
                             "board": {"systems": {"state": "bad", "value": "Still open"}}},
                         ]},
                        {"phase": "Assess", "title": "Obligations and evidence",
                         "prompt": "Tenant and landlord personal details passed through the compromised mailbox. What is the responsible step?",
                         "options": [
                            {"label": "Preserve the emails and logs, and assess it under the Privacy Act breach scheme with Dean", "outcome": "good",
                             "consequence": "Right. Personal information was exposed, so this may be a notifiable breach. Keeping the evidence and assessing it properly is the law, and it is how you learn what to fix.",
                             "board": {"clock": {"state": "ok", "value": "Assessment started"}, "clients": {"state": "ok", "value": "Barbara informed"}}},
                            {"label": "Delete the phishing email so no one clicks it by mistake", "outcome": "bad",
                             "consequence": "That destroys the evidence you need to understand and report the incident. Keep it, and warn people separately.",
                             "board": {"clock": {"state": "bad", "value": "Evidence lost"}}},
                            {"label": "Keep it quiet to avoid embarrassing the agency", "outcome": "bad",
                             "consequence": "Hiding a breach of personal information can itself break the law and destroys trust. Assess and report it properly.",
                             "board": {"clock": {"state": "bad", "value": "Unreported"}}},
                         ]},
                    ],
                },
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. Exactly ten, five per lesson: Lesson 1 checks the concepts taught, Lesson
# 2 checks applying them at Yarraville Real Estate. Four options each, exactly one
# correct, every option carries an explanation that teaches (the Adaptive Feedback
# Engine's fuel). Same house voice: warm, plain, no em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: understand it ----
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Every device at the office reaches the internet through the router. In plain terms, why does that make the router so important to security?",
            "options": [
                ("It is the single gateway every message passes through on its way in or out, so it is the one box that guards the whole network", True,
                 "Yes. The router translates between your private network and the internet, so all traffic crosses it. That single chokepoint is why securing the router protects everything behind it."),
                ("It stores all the business's files, so losing it loses the data", False,
                 "No. The router routes traffic; it is not where your files live. Its importance is that every message in or out passes through it."),
                ("It is the fastest computer in the office", False,
                 "No. Speed is not the point. The router matters because it is the one gateway between the office and the internet."),
                ("It is the only device with a password", False,
                 "No. Every account should have a password. The router matters because all traffic in and out flows through it."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A landlord's payout bank account is quietly changed in the rent ledger, so next month's rent is set to pay a stranger. Which pillar of the CIA triad has failed?",
            "options": [
                ("Integrity, because a trusted record was altered without permission", True,
                 "Yes. The record still opens and the system still works, but the details were changed without approval, so it can no longer be relied on. That is an integrity failure, and exactly how payment-redirection fraud works."),
                ("Confidentiality, because private data was exposed", False,
                 "No. Nothing was exposed to an outsider. A trusted record was altered, which is integrity."),
                ("Availability, because the ledger cannot be opened", False,
                 "No. The ledger opens fine. The problem is that its contents were changed, which is integrity."),
                ("None, because the system is working normally", False,
                 "No. Working normally is the danger here. The altered account will send real money to a stranger. That is an integrity failure."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A sign-in page shows the padlock and https, but the address reads yarravi11ere-payments.com. Is it safe to enter the agency login?",
            "options": [
                ("No. The padlock only proves the connection is encrypted, not that the site is genuine, and the address is a lookalike of the real domain", True,
                 "Yes. Anyone can get a padlock for a site they own, including a fake one. The padlock protects the connection, not the identity of the site. The lookalike address is the tell."),
                ("Yes. The padlock and https mean the site has been checked and is genuine", False,
                 "No. The padlock only means the connection is encrypted. Scam sites can show a padlock too. Read the address instead."),
                ("Yes. It loaded with no browser warning, so it is trusted", False,
                 "No. A lookalike page loads normally with no warning, because the connection itself is fine. The destination is the problem."),
                ("There is no way to tell from the address bar", False,
                 "No. The address bar is exactly where you tell: the domain is a lookalike, with number ones for the letters and the wrong ending."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "You open the office router's settings and the admin password is still 'admin'. Why is that dangerous, and what is the fix?",
            "options": [
                ("Default passwords like 'admin' are published online for anyone to look up, so change it to something strong and unique straight away", True,
                 "Yes. Factory-default passwords are public knowledge and attackers keep lists of them, so anyone who reaches the page can log in. Changing it is the single most important router fix."),
                ("Nothing is wrong; 'admin' is a strong, secure password", False,
                 "No. 'admin' is the factory default, listed online for anyone to find. It must be changed to something strong and unique."),
                ("The router is faulty and needs replacing", False,
                 "No. The router is fine. The default password just needs changing."),
                ("You should turn the router off to be safe", False,
                 "No. That takes the whole office offline. The fix is to change the default password."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "The Essential Eight recommends multi-factor authentication (MFA). What does MFA actually protect you against?",
            "options": [
                ("A stolen or guessed password on its own, because a second factor is still needed to get in", True,
                 "Yes. MFA means a password alone is not enough; a code or approval on your phone is also required. The Medibank attackers got in through remote access that lacked exactly this."),
                ("Your computer running slowly", False,
                 "No. MFA is about access, not speed. It stops a stolen password alone getting an attacker in."),
                ("Losing your files to a hardware failure", False,
                 "No. That is what backups protect against. MFA protects your accounts when a password is stolen."),
                ("Viruses in email attachments", False,
                 "No. That is a different control. MFA stops a stolen password alone being used to log in."),
            ],
        },
        # ---- Lesson 2: apply it ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "At 4:50pm a staff member sends a rent-increase notice to 214 tenants with every address in the To field instead of Bcc. Which pillar has failed?",
            "options": [
                ("Confidentiality, because personal contact details were exposed to people who should not have them", True,
                 "Yes. Nothing was changed or lost, but every tenant can now see every other tenant's email address. That exposure is a confidentiality failure, and it can be reportable."),
                ("Availability, because the email cannot be recalled", False,
                 "No. The issue is not access to the email. Private details were exposed, which is a confidentiality failure."),
                ("Integrity, because the email was altered", False,
                 "No. Nothing was altered. Personal details were exposed to the wrong people, which is confidentiality."),
                ("None, because sending an email is always safe", False,
                 "No. Exposing 214 people's details to each other is a real confidentiality breach that should be assessed."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Priya is at a cafe on its open Wi-Fi and needs to email a lease full of a tenant's ID and bank details. What is the safest way to send it?",
            "options": [
                ("Switch to her own phone hotspot, then send over https so it is encrypted the whole way", True,
                 "Yes. The open cafe Wi-Fi is shared ground where others could watch unencrypted traffic. Her own hotspot plus https keeps the lease private end to end."),
                ("Send it on the cafe Wi-Fi; it is faster than mobile data", False,
                 "No. Anyone on the open network can try to read traffic that is not encrypted. Do not send sensitive files over a network you do not control."),
                ("Ask the cafe for their Wi-Fi password first, then send", False,
                 "No. Everyone in the cafe has that same password and shares the same network. It is still not a connection she controls."),
                ("Turn off Wi-Fi encryption on her phone to send faster", False,
                 "No. That would remove protection, not add it. Use her own hotspot and https."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "At 9pm the principal's phone keeps buzzing with sign-in approval prompts he did not start. What is the right first move?",
            "options": [
                ("Deny every prompt, change the account password now, and report it", True,
                 "Yes. Repeated prompts you did not start mean someone already has the password and is hoping for an accidental Approve. Deny them, change the password so the stolen one is useless, and report it."),
                ("Approve one so the prompts stop", False,
                 "No. One approval is exactly what the attacker needs to get in. Never approve a prompt you did not start."),
                ("Ignore it and turn the phone to silent", False,
                 "No. The attacker keeps trying, and one accidental tap lets them in. Change the password now."),
                ("Reply to the prompt asking who is trying to log in", False,
                 "No. You cannot reply to a login prompt, and it would not help. Deny them and change the password."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "The office router's Wi-Fi settings show Security set to Open, with the admin password already changed and firmware up to date. What needs fixing?",
            "options": [
                ("The Open Wi-Fi, because it has no encryption and anyone in range can join and read the traffic. Set WPA2 or WPA3 with a strong passphrase", True,
                 "Yes. Open means unencrypted, so anyone nearby can join without a password and read wireless traffic. WPA2 or WPA3 with a long passphrase closes it. The admin password and firmware are already fine."),
                ("The firmware, because being up to date is a risk", False,
                 "No. Up-to-date firmware is good; it means known holes are patched. The open Wi-Fi is the problem."),
                ("The admin password, because it was changed from the default", False,
                 "No. Changing it from the default is exactly right. The open Wi-Fi is what needs fixing."),
                ("Nothing, because the firmware is current", False,
                 "No. Current firmware is good, but the Wi-Fi is Open with no encryption, which anyone in range can join."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A USB stick labelled 'Rentals Q2 backup' is found on the office front step. What should staff do with it?",
            "options": [
                ("Not plug it into any office device, and hand it to IT to check safely", True,
                 "Yes. A 'lost' USB left where staff will find it is a known way to get malware onto a machine, and some drives run code the moment they connect. Never plug unknown media into a work device."),
                ("Plug it into the reception PC to find the owner", False,
                 "No. Opening it is the risk. Do not plug an unknown stick into a work PC. Hand it to IT."),
                ("Plug it into the spare laptop instead, to be safe", False,
                 "No. Any work machine is at risk, and it may be on the same network. Do not plug it in anywhere. Give it to IT."),
                ("Throw it in the bin without telling anyone", False,
                 "No. It could be a genuine lost drive or part of an attack worth flagging. Hand it to IT rather than binning it quietly."),
            ],
        },
    ],
}
