"""Module 1, Network Security Fundamentals: the gold-standard reference content.

  Lesson 1  UNDERSTAND IT (a teaching lesson). Four deep reading panels, each
            anchored by a device-framed recreation (own-origin, CSP-safe): what a
            network is and why small business is targeted (net-topology); how data
            travels and what encryption does (data-hops); the CIA triad mapped to
            real Australian incidents plus the Privacy Act NDB duty (cia-triad);
            and the weak points framed against the ASD Essential Eight
            (router-admin). One comprehension check on a lookalike sign-in page.
  Lesson 2  APPLY IT (a practical lesson). Five hands-on, scenario tasks set at
            Yarraville Real Estate, a small inner-west Melbourne agency: sort
            situations to the CIA pillar, a public-Wi-Fi decision drill, an
            Essential-Eight hardening pass, read an Open Wi-Fi settings screen, and
            three first-move incidents.

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
                "Nobody picks Yarraville by name. The Australian Signals Directorate "
                "received <strong>over 84,700 cybercrime reports in 2024-25, about "
                "one every six minutes</strong>, and the average self-reported cost "
                "to a small business was <strong>$56,600 per report</strong>"
                "<span class=\"cy-cite\">1</span>. A small business with real "
                "customer data and light defences is exactly what those tools are "
                "built to find.</p>"
                "<div class=\"cy-callout\">The good news: the same report shows most "
                "incidents use a handful of predictable weaknesses. A few simple "
                "habits, covered in this lesson, shut most of those doors.</div>"
                "<div class=\"cy-sources\"><div class=\"cy-sources__h\">Source</div>"
                "<ol><li><span class=\"cy-sources__n\">1</span> "
                "Australian Signals Directorate, ASD Cyber Threat Report 2024-25 "
                "(cyber.gov.au).</li></ol></div>",
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
                "about <strong>9.8 million</strong><span class=\"cy-cite\">1</span> "
                "current and former customers, including, for some, passport and "
                "licence numbers, the raw material for identity theft. Nothing was "
                "locked or changed; private data simply reached people who should "
                "never have had it. For an agency, the equivalent is a tenant's "
                "licence and payslips reaching the wrong inbox.</p>"
                "<p><strong>Integrity</strong>: is it accurate and unaltered? A "
                "landlord's payout account, quietly changed in the rent ledger, "
                "fails this. The record still opens perfectly, but the details were "
                "tampered with, which is exactly how payment-redirection scams drain "
                "real money from Australian businesses.</p>"
                "<p><strong>Availability</strong>: is it there when you need it? "
                "Ransomware that locks every file, or a booking system down all "
                "morning, fails this. In the 2022 <strong>Medibank</strong> attack, "
                "sensitive health data on about <strong>9.7 million</strong>"
                "<span class=\"cy-cite\">2</span> people was stolen and later "
                "published; the attackers reached the network through remote access "
                "that lacked a second factor. The same class of attack routinely "
                "locks a business out of its own systems for days.</p>"
                "<p>There is a legal side to this too. Under the "
                "<strong>Privacy Act 1988</strong> and the Notifiable Data Breaches "
                "scheme run by the OAIC, a business that suffers a breach likely to "
                "cause serious harm generally must assess it within "
                "<strong>30 days</strong> and notify both the OAIC and the people "
                "affected. In the OAIC's July to December 2024 figures, "
                "<strong>595 breaches</strong><span class=\"cy-cite\">3</span> were "
                "reported, most caused by malicious attacks, with phishing the "
                "leading cause. Getting the three questions right is not just good "
                "practice; for real data it is the law.</p>"
                "<div class=\"cy-callout\">Keep information private, keep it correct, "
                "keep it reachable. Name which one a problem threatens, and you "
                "already understand half of how to respond.</div>"
                "<div class=\"cy-sources\"><div class=\"cy-sources__h\">Sources</div>"
                "<ol>"
                "<li><span class=\"cy-sources__n\">1</span> Optus 2022 data breach, "
                "as reported to the OAIC (oaic.gov.au).</li>"
                "<li><span class=\"cy-sources__n\">2</span> Medibank 2022 data breach, "
                "OAIC investigation (oaic.gov.au).</li>"
                "<li><span class=\"cy-sources__n\">3</span> OAIC Notifiable Data "
                "Breaches Report, July to December 2024 (oaic.gov.au).</li>"
                "</ol></div>",
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
        "title": "Put it to work: protect a real network",
        "reading_time_minutes": 10,
        "intro": "Now use it. You are helping out at Yarraville Real Estate, a small "
        "independent agency in Melbourne's inner west. Principal Dean Whitlock runs "
        "the office with senior property manager Priya Anand, trust accountant "
        "Marion Fisk and administrator Cody Nguyen. Every task here is a real day at "
        "that agency: name what is at risk, make the right call on a cafe Wi-Fi, "
        "harden the office before it opens, read a router screen, and make the sound "
        "first move when something goes wrong.",
        "tasks": [
            {
                "key": "pillar-triage",
                "kind": "classify",
                "points": 2,
                "title": "Which pillar is at risk?",
                "body": "<p>Lesson 1 gave you the three questions security asks: is "
                "it private (Confidentiality), is it correct (Integrity), is it "
                "reachable (Availability). Here are six things that actually happen "
                "across a fortnight at Yarraville Real Estate. For each, decide which "
                "pillar it puts at risk. This is how a security-minded person sizes "
                "up any problem in seconds.</p>"
                "<div class=\"cy-callout\">Ask: was private information exposed, was "
                "something changed, or can you no longer reach what you need?</div>",
                "payload": {
                    "prompt": "Read each situation and tap the pillar it puts at risk. Sort all six to finish.",
                    "categories": [
                        {"id": "conf", "label": "Confidentiality"},
                        {"id": "integ", "label": "Integrity"},
                        {"id": "avail", "label": "Availability"},
                    ],
                    "events": [
                        {"text": "4:50pm Thursday. Marion sends the quarterly rent-increase notice to 214 tenants but puts every address in the To field instead of Bcc, so all 214 can see each other's email addresses.",
                         "category": "conf",
                         "why": "Confidentiality. Nothing was changed or lost, but personal contact details were exposed to people who should never have seen them. Like Optus, the failure is exposure, and it can be reportable."},
                        {"text": "A landlord's payout account in the rent ledger is quietly changed after Priya's login is phished, so next month's $2,180 rent is set to pay an unknown account.",
                         "category": "integ",
                         "why": "Integrity. The record still opens and the system still works, but the payment details were altered without permission, which is exactly how payment-redirection fraud drains money."},
                        {"text": "8:30am Saturday, mid open-inspection season. The property-management system is down for four hours, so no one can open lease documents, entry codes or the inspection schedule.",
                         "category": "avail",
                         "why": "Availability. Nothing was stolen or changed, but a system the office depends on is not reachable when it is needed most."},
                        {"text": "A tenant application PDF with a driver licence and two payslips, 'Application_Reddy_Nikhil.pdf', is left face-up in the reception printer tray where walk-in clients can read it.",
                         "category": "conf",
                         "why": "Confidentiality. Sensitive identity documents were exposed to strangers. Exposure is the failure, even when nothing is taken."},
                        {"text": "Someone edits a signed lease in the shared drive, changing the rent from $520 to $560 a week, and no one notices for a fortnight.",
                         "category": "integ",
                         "why": "Integrity. A trusted record was altered without approval, so it can no longer be relied on, which in a contract is a real problem, not just a data one."},
                        {"text": "Monday morning, a ransom note appears on the front-desk PC and every file in the Inspections folder is renamed to end .locked.",
                         "category": "avail",
                         "why": "Availability. The files are not read or changed, but the office cannot reach them, which stops the day's work."},
                    ],
                },
            },
            {
                "key": "cafe-wifi",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: sending a lease from a cafe",
                "body": "<p>It is 1:10pm. Priya is at the Cornershop Cafe in Seddon "
                "between inspections, and she needs to email a signed lease, "
                "<strong>Lease_14Bishop_St.pdf</strong> (it has the tenant's licence "
                "and bank details in it), back to the office before a 2pm deadline. "
                "She has just joined the cafe's open <strong>Cornershop Free "
                "WiFi</strong>, which needs no password. Your call decides how safe "
                "this is. Work it through.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> an open "
                "network is shared ground. Use a connection you control, and let "
                "https protect the data the rest of the way.</div>",
                "payload": {
                    "prompt": "Priya is on an open cafe Wi-Fi with a sensitive file to send. Make each call and see the consequence.",
                    "start": "join",
                    "nodes": {
                        "join": {
                            "text": "She is connected to the open Cornershop Free WiFi and the lease is ready to send. What is her first move?",
                            "choices": [
                                {"label": "Switch to her phone's own 4G hotspot instead of the open cafe Wi-Fi, then send", "outcome": "good",
                                 "feedback": "Right. The cafe Wi-Fi is open, so anyone else on it could try to watch unencrypted traffic. Her phone's mobile data is her own connection, not shared ground.", "to": "sent"},
                                {"label": "Send it now on the cafe Wi-Fi, it is faster than mobile data", "outcome": "bad",
                                 "feedback": "Open Wi-Fi is shared ground: anyone on it can attempt to read traffic that is not encrypted. Do not send sensitive files over a network you do not control.", "to": "open_bad"},
                                {"label": "Ask the cafe staff for a Wi-Fi password so the connection is 'secure'", "outcome": "bad",
                                 "feedback": "A cafe password does not make it your network. Everyone in the cafe has the same password and shares the same Wi-Fi, so it is still not a connection you control.", "to": "open_bad"},
                            ],
                        },
                        "open_bad": {
                            "text": "On a network full of strangers, anything not encrypted end to end can be read in transit. A lease full of identity and bank details is exactly what you never send that way. Use your own connection instead.",
                            "choices": [],
                        },
                        "sent": {
                            "text": "She is on her own 4G hotspot now, away from the cafe crowd. Before she hits send on the webmail, what does she check?",
                            "choices": [
                                {"label": "That the webmail address bar shows https and the padlock, so the message is encrypted the whole way to the server", "outcome": "good",
                                 "feedback": "Exactly. Even on a trusted connection, https is what scrambles the data across the public internet all the way to the server. Own connection plus https is the safe combination.", "to": "win"},
                                {"label": "Nothing, being on her own hotspot is enough on its own", "outcome": "bad",
                                 "feedback": "The hotspot stops the cafe crowd watching, but the data still crosses the public internet to reach the server. https is what protects it the rest of the way. Check for the padlock.", "to": "hotspot_bad"},
                            ],
                        },
                        "hotspot_bad": {
                            "text": "The hotspot was the right move, but it only covers the first hop. Across the public internet, https is what keeps the lease unreadable. Always check for the padlock before sending anything sensitive.",
                            "choices": [],
                        },
                        "win": {
                            "text": "Own connection, https confirmed, lease sent and safe with minutes to spare. That is the whole habit: on shared or open Wi-Fi, get onto a connection you control, and let the padlock protect the data the rest of the way.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "harden-the-office",
                "kind": "harden",
                "points": 2,
                "title": "Harden the office before it opens",
                "hero": "data-journey",
                "body": "<p>First, the why. The animation above is the exact risk "
                "Lesson 1 described: on an open connection your data travels in the "
                "clear and a listener reads it, while encryption turns it into "
                "gibberish. Now the how.</p>"
                "<p>It is Monday, 8am, and Yarraville Real Estate opens in fifteen "
                "minutes. Dean has asked you to walk the office setup before the day "
                "starts. Four things are not set up safely yet. For each one, choose "
                "the fix that genuinely closes the gap, using the Essential Eight "
                "habits from Lesson 1, and watch it flip to Secured.</p>"
                "<div class=\"cy-callout\">For each item, pick the option that truly "
                "closes the door. Lock down all four to finish.</div>",
                "payload": {
                    "prompt": "Secure each part of the office setup. Lock down all four to finish.",
                    "steps": [
                        {
                            "label": "The whole office shares one login, office@yarravillere.com.au, for the property-management system",
                            "risk": "A shared login hides who did what, and one leaked password hands over everything.",
                            "options": [
                                {"text": "Give each person their own named account and remove the shared one", "correct": True,
                                 "why": "Right. Individual accounts make every action traceable to a person, and one leaked password no longer unlocks the whole system. Shared logins are a known Essential Eight weak point."},
                                {"text": "Write the shared password on a card by the front desk so nobody forgets it", "correct": False,
                                 "why": "That makes the shared login even more exposed. The fix is individual accounts, not an easier-to-find shared password."},
                                {"text": "Keep the shared login but change its password every month", "correct": False,
                                 "why": "It is still one shared login that hides who did what, and monthly changes just get written on notes. Give each person their own account."},
                            ],
                        },
                        {
                            "label": "The mailbox that receives landlord bank-detail changes has a password only, no second step",
                            "risk": "If that password is phished or guessed, an attacker walks straight into the inbox that authorises money movements.",
                            "options": [
                                {"text": "Turn on multi-factor authentication (MFA) for that mailbox", "correct": True,
                                 "why": "Right. MFA adds a second factor, like a code on your phone, so a stolen password alone cannot open the mailbox. The Medibank attackers got in through remote access that lacked MFA."},
                                {"text": "Make the password twenty characters long instead", "correct": False,
                                 "why": "A long password still travels and can still be phished. A second factor is what stops a stolen password being reused. Turn on MFA."},
                                {"text": "Only open that mailbox on the office computer", "correct": False,
                                 "why": "That does not stop a stolen password being used from anywhere else. Add MFA so the password alone is not enough."},
                            ],
                        },
                        {
                            "label": "The only backup of the trust-account ledger sits in a folder on the same front-desk PC as the live file",
                            "risk": "If ransomware or theft hits that PC, the backup goes with it, and there is no path back.",
                            "options": [
                                {"text": "Add a second backup kept offline or off-site, separate from that PC", "correct": True,
                                 "why": "Right. A copy on the same machine is lost with it. Keeping at least one backup offline or off-site means ransomware or a stolen PC cannot take your only path back."},
                                {"text": "Copy the backup into a second folder on the same PC", "correct": False,
                                 "why": "Both copies are lost together if that PC is locked or stolen. Keep one copy off the machine entirely."},
                                {"text": "Trust the system's own cloud and keep no separate backup", "correct": False,
                                 "why": "One copy anywhere is a single point of failure. Keep an independent, separate backup as well."},
                            ],
                        },
                        {
                            "label": "The office router still uses the internet provider's default admin password, printed on a sticker",
                            "risk": "Default passwords are published online, so anyone who reaches the settings page can look yours up and take over.",
                            "options": [
                                {"text": "Change the router admin password to a long, unique one only staff know", "correct": True,
                                 "why": "Right. Default router passwords are printed and published, so the factory value is public knowledge. Changing it is the single most important router fix."},
                                {"text": "Hide the sticker so nobody can read the default password", "correct": False,
                                 "why": "Attackers reach the router over the network and look defaults up online, not by reading the sticker. Hiding it changes nothing. Change the password."},
                                {"text": "Make the Wi-Fi network name (SSID) hidden so nobody finds the router", "correct": False,
                                 "why": "Hiding the network name does not stop anyone determined and does not fix the default admin password. Change the password."},
                            ],
                        },
                    ],
                },
            },
            {
                "key": "read-the-wifi",
                "kind": "check",
                "points": 2,
                "title": "Read the Wi-Fi settings screen",
                "diagram": "router-wifi",
                "body": "<p>This is Yarraville Real Estate's router wireless settings "
                "page, open in a browser on the office network. The admin password "
                "has already been changed and the firmware is up to date. But one "
                "row on this page leaves the office wide open. Read it the way you "
                "now know how, then answer.</p>"
                "<div class=\"cy-callout\">Remember the Essential Eight habit for "
                "Wi-Fi: it should be encrypted, with a long passphrase, not open for "
                "anyone in range to join.</div>",
                "question": "What is the security problem on this Wi-Fi page, and the fix?",
                "hint": "Look at the Security row. One value means there is no encryption at all.",
                "options": [
                    ("Wi-Fi security is set to Open, so anyone nearby can join and read the traffic. Set it to WPA2 or WPA3 with a long passphrase", True,
                     "Right. An open network has no encryption, so anyone in range can join and read wireless traffic, and no password is needed to get on. WPA2 or WPA3 with a strong passphrase is the Essential Eight habit that closes it. The admin password and firmware here are already fine."),
                    ("The firmware being up to date is the risk on this page", False,
                     "No. Up-to-date firmware is a good thing; it means known security holes are already patched. The real problem is that the Wi-Fi is open, with no encryption."),
                    ("The network name, YarravilleRE-Office, gives away that it is a real-estate office", False,
                     "A recognisable network name is not the security problem here. The open, unencrypted Wi-Fi is what anyone in range can join and read."),
                    ("The page offers a guest network, which should not exist", False,
                     "A guest network is a good thing to add, not a risk. The problem on this page is that the main Wi-Fi is Open, with no encryption."),
                ],
            },
            {
                "key": "first-move",
                "kind": "respond",
                "points": 2,
                "title": "Three things go wrong",
                "body": "<p>One last drill, and the most important, because this is "
                "where it counts. Three moments at Yarraville Real Estate when "
                "something goes wrong. Knowing what a network is was the start. The "
                "real skill is your first move, because it decides how far a problem "
                "spreads. For each one, choose the soundest first move and see how it "
                "plays out.</p>"
                "<div class=\"cy-callout\"><strong>The habit to build:</strong> fast "
                "and calm beats clever. Deny, disconnect or hand it in first, then "
                "report it.</div>",
                "payload": {
                    "prompt": "Choose the soundest first move for each. Handle all three to finish.",
                    "situations": [
                        {
                            "id": "mfa-bomb",
                            "text": "Tuesday, 9:10pm. Dean's phone keeps buzzing with Microsoft 365 approval requests to sign in to his work account, one after another, that he did not start himself. What should he do?",
                            "options": [
                                {"text": "Deny every prompt, change his 365 password now, and report it to the office IT support", "outcome": "good",
                                 "feedback": "Right. Repeated prompts you did not start mean someone already has your password and is hoping you will tap Approve by mistake. Deny them all, change the password so the stolen one stops working, and report it. The MFA prompt is doing its job."},
                                {"text": "Approve one so the buzzing stops for the night", "outcome": "bad",
                                 "feedback": "That is exactly what the attacker wants. One approval lets them straight in. Never approve a prompt you did not start. Deny them all and change the password."},
                                {"text": "Put the phone on silent and deal with it in the morning", "outcome": "risky",
                                 "feedback": "The attacker keeps trying overnight, and one accidental tap lets them in. Do not just mute it. Change the password now so the stolen one is useless."},
                            ],
                        },
                        {
                            "id": "stolen-laptop",
                            "text": "Friday, 5:40pm. Cody's work laptop, with saved logins and tenant files on it, is taken from his car outside Highpoint shopping centre. What is the first move?",
                            "options": [
                                {"text": "Tell Dean and IT straight away so they can change his passwords, sign the laptop out of its accounts remotely, and assess whether it is a notifiable breach", "outcome": "good",
                                 "feedback": "Right. Fast reporting lets IT lock the accounts and remote-wipe the device before anything is opened, and because tenant personal data is on it, Dean has to assess it under the Privacy Act, not sit on it."},
                                {"text": "Wait a day or two to see if it turns up before telling anyone", "outcome": "bad",
                                 "feedback": "Every hour the saved logins and tenant files sit unprotected. Report it now so passwords are changed and the device is wiped remotely."},
                                {"text": "Just buy a replacement laptop and carry on", "outcome": "bad",
                                 "feedback": "A new laptop does nothing about the data on the stolen one. Change the passwords, remote-wipe it, and assess the breach."},
                            ],
                        },
                        {
                            "id": "rogue-usb",
                            "text": "Monday, 8:20am. A USB stick labelled 'Rentals Q2 backup' is found on the front step. Cody is about to plug it into the reception PC to see whose it is. What should he do?",
                            "options": [
                                {"text": "Not plug it in, and hand it to Dean or IT, who can check it safely", "outcome": "good",
                                 "feedback": "Right. A 'lost' USB left where staff will find it is a known trick to get malware onto a machine. Plugging it in can run code the moment it is opened. Never plug unknown media into a work PC."},
                                {"text": "Plug it in quickly, just to read the folder names and find the owner", "outcome": "bad",
                                 "feedback": "Opening it is the risk. Some drives run code automatically as soon as they connect. Do not plug an unknown stick into a work PC. Hand it in."},
                                {"text": "Plug it into the spare laptop instead, to be safe", "outcome": "risky",
                                 "feedback": "Any work machine is at risk, and it may be on the same network as everything else. Do not plug an unknown USB into any office device. Give it to IT."},
                            ],
                        },
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
