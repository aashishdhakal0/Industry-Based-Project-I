"""Module 5, Firewall & Network Defence: understand it, then apply it.

The flagship "defence" module. Lesson 1 TEACHES the ideas, opening on a CSS
"watch it unfold" firewall animation, then building the mental model: what a
firewall is (a guard checking rules top-down, first match wins, default deny),
why one wall is never enough (defence in depth), segmentation as watertight
compartments, and safe remote access through a VPN. Lesson 2 APPLIES it with the
signature FIREWALL rule-reading activity, sorting devices into zones, reading a
segmented network, finding weaknesses on a business map, and default-deny sorting.

  Lesson 1  UNDERSTAND IT  — four teaching panels, each with a real visual, plus
            one comprehension check on default-deny.
  Lesson 2  APPLY IT       — the FIREWALL rule table, CLASSIFY zones, a picture
            CHECK, NETMAP weaknesses, and a default-deny SORT.

Voice: warm, plain Australian English, no em-dashes, no emoji. Grounded in ACSC
(cyber.gov.au) guidance on firewalls, network segmentation, remote access, and
patching (the Essential Eight). Points sum to 10 per lesson and bank at lesson end.
"""

LESSONS = [
    {
        "title": "The firewall, and the idea of defence in depth",
        "reading_time_minutes": 9,
        "intro": "A firewall is the guard on the door between your business and the "
        "internet. This lesson builds the whole mental model: how a firewall "
        "decides, why one wall is never the whole plan, how dividing a network "
        "contains trouble, and how people get in from outside safely.",
        "tasks": [
            {
                "key": "the-firewall",
                "kind": "concept",
                "points": 2,
                "title": "The firewall: a guard reading a list of rules",
                "diagram": "firewall",
                "body": "<p>A firewall is not magic. It is the guard on the "
                "connection between your network and the internet, and it works from "
                "a short list of <strong>rules</strong>. Every "
                "connection that arrives is checked against those rules, and is "
                "either allowed through or blocked at the gate.</p>"
                "<p>Two ideas make sense of every firewall you will ever meet:</p>"
                "<ul>"
                "<li><strong>First match wins.</strong> The rules are checked from "
                "the top down, and the first rule that matches the traffic decides "
                "what happens to it. The rest are not checked. This is why the order "
                "of the rules matters so much.</li>"
                "<li><strong>Default deny.</strong> The safest firewall ends with one "
                "quiet, powerful rule: block everything not already allowed. You open "
                "only the few doors the business needs, and anything you never "
                "thought of is shut by default. This starting-from-closed stance is "
                "what the Australian Signals Directorate recommends.</li>"
                "</ul>"
                "<p>Most firewalls today are also <strong>stateful</strong>: once you "
                "start a conversation with a website, the firewall remembers it and "
                "lets the replies back in, while still blocking anything that tries to "
                "start a conversation with you from the outside. You do not manage "
                "that; it just means the firewall can tell your traffic apart from a "
                "stranger's, and a home or small-business router has one built in "
                "already.</p>"
                "<div class=\"cy-callout\">Read the rules from the top, stop at the "
                "first that matches, and remember what the bottom rule is doing: "
                "turning away the constant, automated probes you never invited in.</div>",
            },
            {
                "key": "defence-in-depth",
                "kind": "concept",
                "points": 2,
                "title": "One wall is never the whole plan",
                "diagram": "defence-in-depth",
                "body": "<p>A firewall is powerful at exactly one job: controlling "
                "which connections are allowed between your network and the outside. "
                "It is not the whole of security, and knowing its edge is what tells "
                "you where the other defences have to do the work.</p>"
                "<p>Anything that arrives looking like normal, invited traffic walks "
                "straight past it: a staff member clicking a link in a phishing "
                "email, a correct-looking password typed into a login, a dodgy file "
                "opened on a laptop that is already inside. The firewall never sees a "
                "problem, because from its point of view nothing broke the rules.</p>"
                "<p>That is why real security is built in <strong>layers</strong>, "
                "called defence in depth: a firewall at the edge, antivirus and "
                "updates on the devices, strong passwords and multi-factor sign-in on "
                "the accounts, staff who can spot a scam, and backups for when "
                "something still gets through. Each layer covers what the others "
                "cannot. This is exactly the thinking behind the ASD "
                "<strong>Essential Eight</strong>, which bundles several of these "
                "layers (patching, multi-factor authentication, restricting admin "
                "rights, controlling macros, and backups) into one baseline, because "
                "no single one is enough on its own.</p>"
                "<div class=\"cy-callout\">If one control fails, the next should "
                "still catch the problem. No single wall, however good, is a whole "
                "defence.</div>",
            },
            {
                "key": "segmentation",
                "kind": "concept",
                "points": 2,
                "title": "Segmentation: watertight compartments",
                "diagram": "segmentation",
                "body": "<p><strong>Segmentation</strong> means dividing one big "
                "network into separate zones, so a problem in one cannot spread to "
                "the rest. On a flat network where everything shares one space, an "
                "infection reaches every machine; on a segmented one, shown in the "
                "diagram, a barrier seals it into a single zone.</p>"
                "<p>The everyday version is deciding which network each thing belongs "
                "on. A small business usually wants three zones:</p>"
                "<ul>"
                "<li><strong>Trusted</strong>: managed staff devices doing everyday "
                "work.</li>"
                "<li><strong>Guest</strong>: visitors, and the public Wi-Fi, kept "
                "well away from staff systems.</li>"
                "<li><strong>Restricted</strong>: the sensitive systems (customer "
                "records, accounts, payment terminals), isolated and reachable only "
                "by who genuinely needs them.</li>"
                "</ul>"
                "<p>Think of watertight compartments in a ship. Segmentation does not "
                "stop trouble starting, but it stops one flooded compartment from "
                "sinking the whole vessel.</p>"
                "<div class=\"cy-callout\">A guest's infected phone should never be "
                "able to reach the accounts machine. Separate zones are what make "
                "that true.</div>",
            },
            {
                "key": "remote-access",
                "kind": "concept",
                "points": 2,
                "title": "Letting people in from outside, safely",
                "diagram": "vpn-tunnel",
                "body": "<p>People need to reach the office network from outside: "
                "from home, on the road, between jobs. The wrong way is to expose "
                "office systems straight to the internet, where automated scanners "
                "find them within hours and hammer at the login around the clock. An "
                "exposed <strong>Remote Desktop</strong> door is one of the most "
                "common ways attackers get in.</p>"
                "<p>Exposed remote-login is one of the most common ways ransomware "
                "gets into a business, precisely because it offers attackers a "
                "direct door with a password to guess.</p>"
                "<p>The right way is a <strong>VPN</strong>, a virtual private "
                "network. It builds an encrypted tunnel from a "
                "remote device back into the office network through one guarded, "
                "locked door. The office systems themselves stay hidden from the open "
                "internet; only the VPN door is exposed, and it gets the strongest "
                "sign-in you have: an individual password for each person plus a "
                "second factor. Recall that the Medibank attackers got in through "
                "remote access that had no second factor; a VPN with multi-factor "
                "sign-in is exactly the control that closes that door.</p>"
                "<p>And whatever you build, keep it maintained. <strong>Patching</strong> "
                "closes known holes before they are used, and <strong>watching</strong> "
                "the alerts means noticing when something is wrong. A great many "
                "breaches use a hole a patch had already fixed, or an alert nobody "
                "read, which is why prompt updates and someone actually reading the "
                "logs matter so much.</p>"
                "<div class=\"cy-callout\">One guarded, encrypted door with strong "
                "sign-in beats many systems exposed directly to the internet. Then "
                "keep it patched and watched.</div>",
            },
            {
                "key": "read-the-default",
                "kind": "check",
                "points": 2,
                "title": "Quick check: read the firewall's last rule",
                "diagram": "fw-default",
                "body": "<p>One quick check to finish. The firewall rules screen above "
                "lists the allow rules at the top, and then a final rule that decides "
                "what happens to everything the rules above did not mention. You just "
                "learned which final rule is the safe one. Read the bottom rule, then "
                "answer.</p>"
                "<div class=\"cy-callout\">The safest firewall starts closed: the "
                "last rule should deny anything not explicitly allowed above.</div>",
                "question": "For the last rule, the catch-all that decides everything not listed above, which setting is safe?",
                "hint": "Should the leftover, un-named traffic be allowed in, or denied?",
                "options": [
                    ("DENY everything else. Start closed and allow only the specific traffic listed above", True,
                     "Right. This is default-deny. The few doors you need are opened by the rules above, and the final rule shuts everything else, so anything you did not think of is blocked by default."),
                    ("ALLOW everything else, then block bad traffic as you notice it", False,
                     "No. That is default-allow, and it means anything you have not thought to block gets in. The catch-all should deny, not allow."),
                    ("ALLOW everything else, but only from Australian addresses", False,
                     "No. Location is easy to fake and says nothing about intent. The safe catch-all denies anything not explicitly allowed."),
                    ("ALLOW everything else that uses the padlock (https)", False,
                     "No. Plenty of unwanted traffic is encrypted too. The padlock is not a safety rating. The catch-all should deny."),
                ],
            },
        ],
    },
    {
        "title": "Put the defences to work: rules, zones, and weak spots",
        "reading_time_minutes": 9,
        "intro": "Now use it at Portsea Bay Motel, a 30-room motel where manager "
        "Glenys Park runs the front desk, guests bring their own devices, and the "
        "booking system, card terminal and CCTV all share the one network. Read the "
        "firewall rule set and judge live traffic, sort devices into the right "
        "zones, read a segmented network, hunt the weak spots on the site map, and "
        "think default-deny.",
        "tasks": [
            {
                "key": "read-the-rules",
                "kind": "firewall",
                "points": 2,
                "title": "Read the firewall's rules",
                "hero": "firewall-flow",
                "body": "<p>First, watch a firewall work: the animation above shows a "
                "connection arriving, being checked against the rules, and being "
                "allowed or blocked at the gate. Now you read the rules yourself.</p>"
                "<p>Here is a small firm's firewall. Lesson 1 gave you the "
                "two ideas that decode it: read the rules top-down, and the first one "
                "that matches wins, with a default-deny at the bottom. Read the rule "
                "set, then decide for each connection whether it is Allowed or "
                "Blocked, and watch which rule decides.</p>"
                "<div class=\"cy-callout\">Read each rule from the top. Stop at the "
                "first one that matches the traffic. That rule wins.</div>",
                "payload": {
                    "prompt": "Here is a small firm's firewall. Read the rules, then decide for each connection below whether it is Allowed or Blocked.",
                    "rules": [
                        {"n": 1, "action": "ALLOW", "desc": "Front desk staff browsing and email, going out to the internet"},
                        {"n": 2, "action": "ALLOW", "desc": "Guests on the guest Wi-Fi reaching the internet"},
                        {"n": 3, "action": "ALLOW", "desc": "Anyone on the internet reaching the motel's booking website"},
                        {"n": 4, "action": "DENY", "desc": "Remote Desktop from the internet to any office computer"},
                        {"n": 5, "action": "DENY", "desc": "Everything else coming in from the internet (default deny)"},
                    ],
                    "traffic": [
                        {"text": "A guest streams a movie on the guest Wi-Fi.", "verdict": "ALLOW", "rule": 2,
                         "why": "Allowed by rule 2. Guests reaching the internet from the guest Wi-Fi is exactly what that rule permits."},
                        {"text": "A traveller loads the motel's booking website to reserve a room.", "verdict": "ALLOW", "rule": 3,
                         "why": "Allowed by rule 3. The booking website is meant to be reached from the internet, so this is wanted traffic."},
                        {"text": "An unknown internet address tries to open Remote Desktop on the reception PC.", "verdict": "BLOCK", "rule": 4,
                         "why": "Blocked by rule 4. Remote Desktop exposed to the internet is a classic way in, so it is denied outright."},
                        {"text": "An automated scanner probes the CCTV recorder from the internet.", "verdict": "BLOCK", "rule": 5,
                         "why": "Blocked by rule 5. Nothing above matched, so the default-deny rule turns it away. This is most of what a firewall does all day."},
                        {"text": "A stranger on the internet tries to connect straight to the card payment terminal.", "verdict": "BLOCK", "rule": 5,
                         "why": "Blocked by rule 5. There is no rule inviting that connection in, so the default deny stops it at the door."},
                    ],
                },
            },
            {
                "key": "zone-it",
                "kind": "classify",
                "points": 2,
                "title": "Put each thing on the right network",
                "hero": "segment-flow",
                "body": "<p>First, watch why zones matter: the animation above shows an "
                "infection racing across a flat network, then being sealed into a "
                "single zone once the network is segmented. Now you place each "
                "device.</p>"
                "<p>Segmentation in practice is deciding which network each "
                "device belongs on. A trusted zone for staff work, a guest zone for "
                "visitors and the public Wi-Fi, and a restricted zone for the "
                "sensitive systems. Place each device where it belongs.</p>"
                "<div class=\"cy-callout\">Read each device and tap the zone it "
                "belongs on. Every zone is used. Sort all six to finish.</div>",
                "payload": {
                    "prompt": "Place each device on the right network: Trusted (staff), Guest (visitors and public), or Restricted (sensitive systems).",
                    "categories": [
                        {"id": "trusted", "label": "Trusted (staff)"},
                        {"id": "guest", "label": "Guest (visitors, public)"},
                        {"id": "restricted", "label": "Restricted (sensitive)"},
                    ],
                    "events": [
                        {"text": "The reception PC Glenys uses for check-ins and email.",
                         "category": "trusted",
                         "why": "Trusted zone. Everyday managed staff devices belong on the internal work network, not mixed in with guests or the crown jewels."},
                        {"text": "The Wi-Fi in the rooms and lobby for guests' phones and laptops.",
                         "category": "guest",
                         "why": "Guest zone. Devices you do not control must be kept off the staff network entirely, on their own segment."},
                        {"text": "The card payment terminal at the front desk.",
                         "category": "restricted",
                         "why": "Restricted zone. Payment systems carry the highest risk and the strictest rules, so they are isolated on their own segment."},
                        {"text": "A guest's own laptop, joined to the room Wi-Fi.",
                         "category": "guest",
                         "why": "Guest zone. An outside device you do not manage should never touch the staff or sensitive networks."},
                        {"text": "The night manager's work laptop for the booking system.",
                         "category": "trusted",
                         "why": "Trusted zone. A managed staff machine belongs on the internal work network."},
                        {"text": "The CCTV recorder holding the camera footage.",
                         "category": "restricted",
                         "why": "Restricted zone. Sensitive systems like the camera recorder get their own tightly controlled segment, reachable only by who genuinely needs them."},
                    ],
                },
            },
            {
                "key": "segmented-map",
                "kind": "check",
                "points": 2,
                "title": "Read the segmented network",
                "diagram": "segmentation",
                "body": "<p>A picture-question, straight from Lesson 1. Here is "
                "segmentation as a picture: the same business, divided into separate "
                "guest, staff and sensitive zones, like watertight compartments in a "
                "ship. Read the diagram, then answer. The whole value is in what "
                "happens when something goes wrong in one compartment.</p>"
                "<div class=\"cy-callout\">Segmentation does not stop trouble "
                "starting. It stops trouble spreading.</div>",
                "question": "Looking at the segmented network above, what is the main benefit if one device is infected?",
                "hint": "Think about where the trouble can and cannot travel.",
                "options": [
                    ("The infection is contained to that zone, instead of spreading across the whole business", True,
                     "Right. Zones act like watertight compartments. A problem in the guest network cannot reach the sensitive systems, so one infected device does not become an infected business."),
                    ("The infected device fixes itself automatically", False,
                     "No. Segmentation does not repair anything. It limits how far a problem can spread, which is a different and very useful thing."),
                    ("Infections cannot happen on a segmented network", False,
                     "No. Segmentation does not prevent an infection starting. It contains it once it has, keeping it out of the other zones."),
                    ("The internet gets faster for everyone", False,
                     "No. Segmentation is about containment and control, not speed. Its benefit is stopping trouble spreading between zones."),
                ],
            },
            {
                "key": "find-weaknesses",
                "kind": "netmap",
                "points": 2,
                "title": "Find the weaknesses",
                "body": "<p>Now put it together on a real-looking network. Below is a "
                "small business set-up with several weak spots hiding in plain sight: "
                "things exposed that should not be, defaults left in place, zones that "
                "were never separated. Tap each weakness you can find. This is exactly "
                "the walk-through a security review does.</p>"
                "<div class=\"cy-callout\">Look for anything reachable from outside "
                "that should not be, and anything sensitive sharing a network with "
                "everyday devices.</div>",
                "payload": {
                    "prompt": "Tap every weakness on this business network. Find all of them to finish.",
                    "nodes": [
                        {"label": "Router still using its default admin password", "weak": True,
                         "why": "A default password is public knowledge. This is often the very first thing an attacker tries."},
                        {"label": "Remote Desktop open to the internet on the office PC", "weak": True,
                         "why": "An exposed remote-login door is scanned and attacked constantly. It should be behind a VPN, not open to the world."},
                        {"label": "Guest lobby Wi-Fi sharing the same network as the card payment terminal", "weak": True,
                         "why": "No segmentation. A problem on a guest's device can reach the payment terminal. These belong on separate zones."},
                        {"label": "Server software two years without an update", "weak": True,
                         "why": "Unpatched software has known holes that are freely documented. It needs regular updates to stay safe."},
                        {"label": "Staff laptops on the trusted work network", "weak": False,
                         "why": "This is fine. Managed staff devices belong on the internal work network."},
                        {"label": "The public website reachable from the internet", "weak": False,
                         "why": "This is fine. A public website is meant to be reached from outside. That is wanted traffic."},
                    ],
                },
            },
            {
                "key": "allow-or-deny",
                "kind": "sort",
                "points": 2,
                "title": "Default-deny thinking",
                "body": "<p>The instinct a good firewall trains in you is simple: "
                "open only what the business genuinely uses, and deny the rest by "
                "default. That way, the things you never thought about are already "
                "blocked. Sort these common services into the ones a small office "
                "usually needs open, and the ones that should stay shut unless there "
                "is a clear reason.</p>"
                "<div class=\"cy-callout\">Tap an item, then tap whether it should "
                "usually be Allowed or Denied by default. Sort all six to finish.</div>",
                "payload": {
                    "prompt": "Sort each service into Allow (the office needs it) or Deny by default (shut unless there is a clear reason).",
                    "buckets": [
                        {"id": "allow", "label": "Usually allow"},
                        {"id": "deny", "label": "Deny by default"},
                    ],
                    "items": [
                        {"text": "Guests on the guest Wi-Fi reaching the internet", "bucket": "allow",
                         "why": "Allow. Guest devices going out to the internet is expected traffic the motel offers on purpose."},
                        {"text": "Remote Desktop reachable from the internet", "bucket": "deny",
                         "why": "Deny by default. An exposed remote-login door is one of the most scanned and attacked services there is."},
                        {"text": "Reaching the motel's booking website from outside", "bucket": "allow",
                         "why": "Allow. The booking site is meant to be public, so this is wanted traffic."},
                        {"text": "Direct internet connections to the card payment terminal", "bucket": "deny",
                         "why": "Deny by default. Payment and internal systems should never be directly reachable from the internet."},
                        {"text": "The front desk sending and receiving normal work email", "bucket": "allow",
                         "why": "Allow. Email is core to running the motel, so this traffic is expected."},
                        {"text": "The CCTV recorder exposed to the whole internet", "bucket": "deny",
                         "why": "Deny by default. The camera recorder belongs inside the network, never open to the world."},
                    ],
                },
            },
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: understand it (firewall + defence in depth) ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is a firewall, in plain terms?",
            "options": [
                ("A guard on the connection between your network and the internet, that allows some traffic and blocks the rest", True,
                 "Yes. A firewall checks traffic against its rules and decides what is allowed between your network and the outside world."),
                ("A program that removes viruses from a computer", False,
                 "No. That is antivirus. A firewall controls which connections are allowed in and out of the network."),
                ("A backup of your important files", False,
                 "No. That is a backup. A firewall controls network traffic, it does not store copies of files."),
                ("A stronger password for your router", False,
                 "No. A firewall is not a password. It is the guard that decides which connections are allowed through."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A firewall checks its rules from the top down. What happens when a connection matches a rule?",
            "options": [
                ("The first rule that matches decides, and the rest are not checked for that connection", True,
                 "Yes. Order matters. The firewall stops at the first matching rule and applies it, which is why rule order is so important."),
                ("Every rule is applied, and they are added together", False,
                 "No. The firewall stops at the first match. It does not combine rules."),
                ("The last rule in the list always wins", False,
                 "No. It is the first matching rule that decides, read from the top down."),
                ("It picks whichever rule is least strict", False,
                 "No. It is not about strictness. The first rule that matches the traffic is the one applied."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What does a 'default deny' rule at the bottom of a firewall do?",
            "options": [
                ("Blocks anything that was not specifically allowed by an earlier rule", True,
                 "Yes. Default deny means you open only the doors you need, and everything else is blocked, including things you never thought of."),
                ("Allows anything that was not specifically blocked", False,
                 "No. That is the opposite, default allow, which is far riskier. Default deny blocks anything not explicitly allowed."),
                ("Deletes traffic logs at the end of the day", False,
                 "No. It has nothing to do with logs. It blocks any traffic not already permitted."),
                ("Turns the firewall off overnight", False,
                 "No. It does not switch anything off. It is the catch-all rule that blocks whatever was not allowed above it."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A firewall is doing its job well. Why do you still need training, antivirus and strong passwords?",
            "options": [
                ("Because a firewall only controls connections; it cannot stop a person being tricked or a valid-looking login", True,
                 "Yes. A firewall guards the door. Phishing, malware on a device, and guessed passwords all get past it and need their own layers."),
                ("Because a firewall only works during business hours", False,
                 "No. A firewall runs constantly. The point is that it only ever controls connections, so other risks need other defences."),
                ("Because antivirus makes the firewall run faster", False,
                 "No. They do separate jobs. You need both because a firewall cannot cover what it never sees."),
                ("You do not; a firewall alone is enough", False,
                 "No. A firewall is one layer. Real security is several layers, because each covers what the others cannot."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is the safe way to let staff reach the office network from home?",
            "options": [
                ("Through a VPN: one encrypted, guarded tunnel with strong individual sign-in", True,
                 "Yes. A VPN gives a single controlled, encrypted door into the network, so office systems are never exposed directly to the internet."),
                ("Expose each office system directly to the internet with a password", False,
                 "No. Anything open to the whole internet is attacked constantly. A VPN keeps systems hidden behind one guarded door."),
                ("Email copies of the files to everyone's personal address", False,
                 "No. That scatters sensitive data out of your control. Give controlled access through a VPN instead."),
                ("Share one team password so everyone can log in easily", False,
                 "No. Shared passwords cannot be traced and leak easily. Each person needs their own strong sign-in with a second factor."),
            ],
        },
        # ---- Lesson 2: apply it (rules, zones, weak spots) ----
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "In a firewall rule set, an inbound connection matches no allow rule above the final 'deny everything else'. What happens?",
            "options": [
                ("It is blocked by the default-deny rule at the bottom", True,
                 "Yes. Anything not specifically allowed above falls through to the default deny and is turned away. That is most of what a firewall does all day."),
                ("It is allowed, because nothing blocked it earlier", False,
                 "No. That would be default-allow. With a default-deny at the bottom, unmatched traffic is blocked."),
                ("It is held until an administrator approves it", False,
                 "No. A firewall does not queue traffic for approval. Unmatched inbound traffic hits the default deny and is blocked."),
                ("It is allowed only if it uses https", False,
                 "No. The padlock is irrelevant to the rule. Unmatched inbound traffic is blocked by default deny."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is network segmentation?",
            "options": [
                ("Dividing one network into separate zones so a problem in one cannot spread to the rest", True,
                 "Yes. Like watertight compartments, segmentation keeps trouble in one zone from reaching the others."),
                ("Making the network faster by adding more cables", False,
                 "No. Segmentation is about containment, not speed. It divides the network into isolated zones."),
                ("Backing the network up to the cloud", False,
                 "No. That is a backup. Segmentation is dividing the network into separate, contained zones."),
                ("Sharing one network between every device for simplicity", False,
                 "No. That is the opposite, a flat network. Segmentation separates devices into zones so trouble cannot roam."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why should guest and customer Wi-Fi be on a separate network from the accounts computer?",
            "options": [
                ("So a problem on a visitor's device cannot reach the sensitive systems", True,
                 "Yes. Keeping visitor devices on their own zone means an infected phone in the waiting room cannot touch the accounts machine."),
                ("So visitors get a faster connection than staff", False,
                 "No. It is not about speed for visitors. It is about keeping devices you do not control away from sensitive systems."),
                ("So you can charge guests for the Wi-Fi", False,
                 "No. The reason is containment, not billing. Separate zones stop trouble spreading from an untrusted device."),
                ("Because guests are not allowed to use the internet", False,
                 "No. Guests can have Wi-Fi. It just belongs on its own zone, away from the sensitive systems."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "On a network map, which of these is a genuine weakness to fix?",
            "options": [
                ("A router still using its default admin password", True,
                 "Yes. Default passwords are public knowledge and among the first things an attacker tries. Change it to something strong and unique."),
                ("The public website being reachable from the internet", False,
                 "No. A public website is meant to be reached from outside. That is wanted traffic, not a weakness."),
                ("Staff laptops sitting on the trusted work network", False,
                 "No. That is correct placement. Managed staff devices belong on the internal work network."),
                ("Automatic updates being switched on", False,
                 "No. Automatic updates are a strength, not a weakness. They close known holes promptly."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A security alert shows a staff account signing in from overseas at 3am. What does 'watching' your network mean here?",
            "options": [
                ("Actually reading the alert and following it up, not just collecting it", True,
                 "Yes. Alerts only help if someone acts on them. An odd sign-in like this is an early warning worth investigating straight away."),
                ("Deleting the alert so the list stays tidy", False,
                 "No. Deleting it throws away an early warning. Watching means reading and following up the odd ones."),
                ("Waiting to see if it happens a few more times first", False,
                 "No. A suspicious overseas sign-in is worth acting on now, not after it has happened repeatedly."),
                ("Turning off alerts so they stop interrupting work", False,
                 "No. That blinds you to real warnings. The point of watching is to notice and act on signals like this."),
            ],
        },
    ],
}
