"""Module 5, Firewall & Network Defence: two deep, hands-on lessons.

The flagship "defence" module, rebuilt to the five-task room shape but pushed
harder than Modules 1 to 4: it opens each lesson with a CSS "watch it unfold"
animated sequence, and it carries two signature interactions built for this
module. Lesson 1 turns the learner into someone who can actually read a firewall
rule set (the new FIREWALL activity: an ordered, first-match rule table with real
traffic to judge). Lesson 2 is defence in depth: sort devices into network zones,
set up remote access safely, find the weaknesses on a business network, and keep
the whole thing patched and watched.

  Lesson 1  The firewall: reading the rules that guard your network
  Lesson 2  Defence in depth: segment, connect safely, and watch for trouble

Voice: warm, plain Australian English, no em-dashes, no emoji. Each lesson is
four interactive activities plus one picture-question CHECK (task 3), points sum
to 10 per lesson and bank at lesson end. The quiz is exactly ten, split five and
five across the two lessons, every question tracing to the lesson that teaches it.
"""

LESSONS = [
    {
        "title": "The firewall: reading the rules that guard your network",
        "reading_time_minutes": 9,
        "intro": "A firewall is the guard on the door between your business and "
        "the internet. This lesson does more than explain it: you will watch one "
        "work, then read a real rule set and decide, traffic by traffic, what gets "
        "in and what gets turned away.",
        "tasks": [
            {
                "key": "read-the-rules",
                "kind": "firewall",
                "points": 2,
                "title": "Read the firewall's rules",
                "hero": "firewall-flow",
                "body": "<p>A firewall is not magic. It is a short list of "
                "<strong>rules</strong>, checked from the top down, and the "
                "<strong>first rule that matches decides</strong> what happens to "
                "that traffic. Watch the sequence above: a connection arrives, it "
                "is checked against the rules, and it is either allowed through or "
                "blocked at the gate. Most business firewalls end with one quiet, "
                "powerful rule: deny everything not already allowed.</p>"
                "<div class=\"cy-callout\">Read each rule from the top. Stop at the "
                "first one that matches the traffic. That rule wins.</div>",
                "payload": {
                    "prompt": "Here is a small firm's firewall. Read the rules, then decide for each connection below whether it is Allowed or Blocked.",
                    "rules": [
                        {"n": 1, "action": "ALLOW", "desc": "Staff browsing and email, going out to the internet"},
                        {"n": 2, "action": "ALLOW", "desc": "Anyone on the internet reaching your public website"},
                        {"n": 3, "action": "DENY", "desc": "Remote Desktop from the internet to any office computer"},
                        {"n": 4, "action": "DENY", "desc": "Everything else coming in from the internet (default deny)"},
                    ],
                    "traffic": [
                        {"text": "A staff member opens their webmail in a browser.", "verdict": "ALLOW", "rule": 1,
                         "why": "Allowed by rule 1. Staff browsing and email going out is exactly what the first rule permits."},
                        {"text": "A customer loads your public website.", "verdict": "ALLOW", "rule": 2,
                         "why": "Allowed by rule 2. Your website is meant to be reached from the internet, so this is wanted traffic."},
                        {"text": "An unknown address on the internet tries to open Remote Desktop on the reception PC.", "verdict": "BLOCK", "rule": 3,
                         "why": "Blocked by rule 3. Remote Desktop exposed to the internet is a classic way in, so it is denied outright."},
                        {"text": "An automated scanner probes a random office computer's file sharing.", "verdict": "BLOCK", "rule": 4,
                         "why": "Blocked by rule 4. Nothing above matched, so the default-deny rule turns it away. This is most of what a firewall does all day."},
                        {"text": "A stranger on the internet tries to connect straight to your accounts computer.", "verdict": "BLOCK", "rule": 4,
                         "why": "Blocked by rule 4. There is no rule inviting that connection in, so the default deny stops it at the door."},
                    ],
                },
            },
            {
                "key": "firewall-scope",
                "kind": "classify",
                "points": 2,
                "title": "What a firewall can, and cannot, stop",
                "body": "<p>A firewall is powerful at one job: controlling which "
                "connections are allowed between your network and the outside. It is "
                "not the whole of security. Anything that arrives looking like "
                "normal, invited traffic, a staff member clicking a link, a correct "
                "password typed in, walks straight past it. Knowing the edge of what "
                "a firewall covers is what tells you where your other defences have "
                "to do the work.</p>"
                "<div class=\"cy-callout\">Ask: is this an uninvited connection from "
                "outside (a firewall's job), or something that looks legitimate (a "
                "job for another layer)?</div>",
                "inline_check": {
                    "question": "Your firewall is doing its job well. Why do you still need antivirus, staff training and strong passwords?",
                    "hint": "Think about what a firewall never sees.",
                    "options": [
                        ("Because a firewall only controls connections; it cannot stop a staff member being tricked or a weak password being guessed", True,
                         "Right. A firewall guards the door. It does nothing about a person inviting trouble in, or a legitimate-looking login. Those need other layers."),
                        ("Because a firewall stops working after a few months", False,
                         "No. A firewall keeps working. The point is that it only ever controls connections, so other risks need other defences."),
                        ("Because antivirus makes the firewall faster", False,
                         "No. They do different jobs. The reason you need both is that a firewall cannot cover what it never sees."),
                        ("You do not; a good firewall is enough on its own", False,
                         "No. A firewall is one layer. Phishing, weak passwords and malware on a device all get past it and need their own defences."),
                    ],
                },
                "payload": {
                    "prompt": "Read each situation and tap whether the firewall can stop it, or whether it needs another defence. Sort all six to finish.",
                    "categories": [
                        {"id": "fw", "label": "A firewall can stop this"},
                        {"id": "other", "label": "Needs another defence"},
                    ],
                    "events": [
                        {"text": "An automated probe from the internet trying to reach an internal server.",
                         "category": "fw",
                         "why": "A firewall's core job. It is an uninvited inbound connection, and the default-deny rule turns it away."},
                        {"text": "A staff member clicking a link in a convincing phishing email.",
                         "category": "other",
                         "why": "Needs another defence. The person invited it, so the firewall sees ordinary outbound browsing. Training and email filtering cover this."},
                        {"text": "A stranger on the internet trying to connect straight to your database.",
                         "category": "fw",
                         "why": "A firewall's core job. There is no rule inviting that connection, so it is blocked at the door."},
                        {"text": "A weak, reused password being guessed on your webmail login.",
                         "category": "other",
                         "why": "Needs another defence. The login looks legitimate to the firewall. Strong passwords and multi-factor sign-in stop this."},
                        {"text": "Constant automated connection attempts to computers you never exposed.",
                         "category": "fw",
                         "why": "A firewall's core job. Uninvited inbound traffic is exactly what default-deny is for."},
                        {"text": "A dodgy attachment a staff member opens on their laptop.",
                         "category": "other",
                         "why": "Needs another defence. The file is already inside on a device. Antivirus, updates and caution cover this, not the firewall."},
                    ],
                },
            },
            {
                "key": "firewall-config",
                "kind": "check",
                "points": 2,
                "title": "Read the firewall on the wall",
                "diagram": "firewall",
                "body": "<p>Here is the picture to keep in your head: the firewall "
                "sits between the internet and your network, and its job is to let "
                "the wanted traffic through while turning away everything else. Read "
                "the diagram above, then answer the question. This is the mental "
                "model that makes every rule you read make sense.</p>"
                "<div class=\"cy-callout\">The safest firewall starts closed and "
                "opens only what the business genuinely needs.</div>",
                "question": "Looking at the firewall above, what is the safest way to decide what it allows?",
                "hint": "Think about whether you start open and close things, or start closed and open things.",
                "options": [
                    ("Start closed: deny everything, then allow only the specific traffic the business needs", True,
                     "Right. This is default-deny. You open the few doors you need and leave everything else shut, so anything you did not think of is blocked by default."),
                    ("Start open: allow everything, then block the bad things as you notice them", False,
                     "No. That is default-allow, and it means anything you have not thought to block gets in. Start closed and open only what you need."),
                    ("Allow anything from Australian addresses and block the rest", False,
                     "No. Location is easy to fake and says nothing about intent. Decide by what traffic the business actually needs, starting from closed."),
                    ("Allow anything that uses the padlock (https)", False,
                     "No. Plenty of unwanted traffic is encrypted too. The padlock is not a safety rating. Start closed and allow only what is needed."),
                ],
            },
            {
                "key": "probe-at-the-door",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: a request to open a door",
                "body": "<p>Firewalls get loosened one convenient exception at a "
                "time, and that is how gaps appear. This drill puts a realistic "
                "request in front of you: a supplier wants remote access to a "
                "machine, today. How you handle it decides whether you have solved a "
                "problem or opened a hole. Work it through.</p>"
                "<div class=\"cy-callout\"><strong>The habit:</strong> open the "
                "narrowest door that does the job, for the shortest time, and never "
                "expose a whole computer to the open internet.</div>",
                "payload": {
                    "prompt": "A supplier needs to reach one machine to fix something. Make each call and see the consequence.",
                    "start": "ask",
                    "nodes": {
                        "ask": {
                            "text": "A software supplier emails: 'Please open Remote Desktop from the internet to the back-office PC so we can log in and fix the till system.' What do you do?",
                            "choices": [
                                {"label": "Give them access through a controlled path, such as a VPN, limited to that one machine and switched off afterwards", "outcome": "good",
                                 "feedback": "Right. A controlled, temporary path into one machine does the job without exposing anything to the open internet.", "to": "narrow"},
                                {"label": "Open Remote Desktop from the internet to that PC, and leave it on in case they need it again", "outcome": "bad",
                                 "feedback": "That is exactly the exposure attackers scan for around the clock. An always-on Remote Desktop door is one of the most common ways in.", "to": "rdp_bad"},
                                {"label": "Turn the firewall off for an hour so they can definitely connect", "outcome": "bad",
                                 "feedback": "Turning the guard off entirely exposes every machine, not just theirs. Never drop the whole firewall for one task.", "to": "off_bad"},
                            ],
                        },
                        "rdp_bad": {
                            "text": "Within days, automated scanners find the open Remote Desktop and start trying passwords against it non-stop. An exposed remote-login door is a standing invitation. A controlled, temporary path would have avoided it.",
                            "choices": [],
                        },
                        "off_bad": {
                            "text": "With the firewall down, every machine is briefly reachable from the internet, not just the one that needed fixing. The guard protects everything or nothing. Never switch it all off for one job.",
                            "choices": [],
                        },
                        "narrow": {
                            "text": "Access is set up through a controlled path to that one machine. Before you send it, how long should the door stay open?",
                            "choices": [
                                {"label": "Only while the work is happening, then close it again", "outcome": "good",
                                 "feedback": "Exactly. A door that is open only while it is needed cannot be found and used later. Open narrow, close fast.", "to": "win"},
                                {"label": "Leave it open permanently, so you never have to set it up again", "outcome": "bad",
                                 "feedback": "A permanent door is a permanent risk, whether or not anyone is using it. Close it when the work is done.", "to": "perm_bad"},
                            ],
                        },
                        "perm_bad": {
                            "text": "The access lingers for months, forgotten, a quiet way in if that supplier's account is ever compromised. Convenience left the door open. Close access the moment the work is finished.",
                            "choices": [],
                        },
                        "win": {
                            "text": "One machine, one controlled path, open only while the work happened, then shut. That is how you say yes to a real need without turning it into a standing hole. Narrow, temporary, and never the whole computer exposed.",
                            "choices": [],
                        },
                    },
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
                        {"text": "Staff web browsing out to the internet", "bucket": "allow",
                         "why": "Allow. Everyday browsing is normal outbound traffic the office needs to work."},
                        {"text": "Remote Desktop reachable from the internet", "bucket": "deny",
                         "why": "Deny by default. An exposed remote-login door is one of the most scanned and attacked services there is."},
                        {"text": "Reaching your public website from outside", "bucket": "allow",
                         "why": "Allow. The website is meant to be public, so this is wanted traffic."},
                        {"text": "Direct connections from the internet to the accounts PC", "bucket": "deny",
                         "why": "Deny by default. Internal computers should never be directly reachable from the internet."},
                        {"text": "Sending and receiving normal work email", "bucket": "allow",
                         "why": "Allow. Email is core to the business, so this traffic is expected."},
                        {"text": "File sharing exposed to the whole internet", "bucket": "deny",
                         "why": "Deny by default. Internal file sharing belongs inside the network, never open to the world."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Defence in depth: segment, connect safely, and watch for trouble",
        "reading_time_minutes": 9,
        "intro": "One wall is never the whole plan. This lesson is about depth: "
        "divide the network so trouble cannot roam, let people in from outside "
        "without opening the front door, find the weak spots yourself, and keep the "
        "whole thing patched and watched.",
        "tasks": [
            {
                "key": "zone-it",
                "kind": "classify",
                "points": 2,
                "title": "Put each thing on the right network",
                "hero": "segment-flow",
                "body": "<p><strong>Segmentation</strong> means dividing one big "
                "network into separate zones, so a problem in one cannot spread to "
                "the rest. Watch the comparison above: on a flat network an "
                "infection reaches everything; on a segmented one, a barrier seals "
                "it into a single zone. The everyday version is deciding which "
                "network each device belongs on. A trusted zone for staff work, a "
                "guest zone for visitors and the public Wi-Fi, and a restricted zone "
                "for the sensitive systems.</p>"
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
                        {"text": "A staff laptop used for everyday work.",
                         "category": "trusted",
                         "why": "Trusted zone. Everyday staff devices belong on the internal work network, not mixed in with visitors or the crown jewels."},
                        {"text": "The free Wi-Fi in the waiting room, for customers' phones.",
                         "category": "guest",
                         "why": "Guest zone. Visitor devices you do not control must be kept off the staff network entirely, on their own segment."},
                        {"text": "The server holding customer records and accounts.",
                         "category": "restricted",
                         "why": "Restricted zone. The most sensitive systems get their own tightly controlled segment, reachable only by who genuinely needs them."},
                        {"text": "A visiting contractor's personal tablet.",
                         "category": "guest",
                         "why": "Guest zone. An outside device you do not manage should never touch the staff or sensitive networks."},
                        {"text": "The reception computer staff use for bookings.",
                         "category": "trusted",
                         "why": "Trusted zone. A managed staff machine belongs on the internal work network."},
                        {"text": "The payment and card system.",
                         "category": "restricted",
                         "why": "Restricted zone. Payment systems carry the highest risk and the strictest rules, so they are isolated on their own segment."},
                    ],
                },
            },
            {
                "key": "remote-access",
                "kind": "branch",
                "points": 2,
                "title": "Decision drill: working from home, safely",
                "diagram": "vpn-tunnel",
                "body": "<p>People need to reach the office network from outside: "
                "from home, on the road, between jobs. The wrong way is to expose "
                "office systems straight to the internet. The right way is a "
                "<strong>VPN</strong>, an encrypted tunnel that lets a remote device "
                "join the network through one guarded, locked door, as the picture "
                "above shows. Work through setting it up.</p>"
                "<div class=\"cy-callout\"><strong>The rule:</strong> one guarded, "
                "encrypted door with strong sign-in beats many systems exposed "
                "directly to the internet.</div>",
                "inline_check": {
                    "question": "Looking at the tunnel above, what does a VPN actually give a remote worker?",
                    "hint": "Think about who can read the traffic, and how many doors are exposed.",
                    "options": [
                        ("One encrypted, guarded way into the network, so office systems are not exposed directly to the internet", True,
                         "Right. The VPN is a single locked, encrypted door. The remote device joins through it, and nothing else has to be left open to the world."),
                        ("Faster internet for the person working from home", False,
                         "No. A VPN is about a secure, private connection into the network, not speed."),
                        ("A way to avoid needing any password at all", False,
                         "No. A VPN still needs strong sign-in. It gives an encrypted tunnel, not a way around logging in."),
                        ("Free antivirus for the remote laptop", False,
                         "No. A VPN does not scan for malware. It is an encrypted, controlled door into the network."),
                    ],
                },
                "payload": {
                    "prompt": "Staff need to work from home. Make each call and see the consequence.",
                    "start": "how",
                    "nodes": {
                        "how": {
                            "text": "Your team needs to reach the office file server from home. How do you set that up?",
                            "choices": [
                                {"label": "Put it behind a VPN: staff connect through one encrypted, guarded tunnel", "outcome": "good",
                                 "feedback": "Right. A VPN gives one controlled, encrypted door. The server itself stays off the open internet.", "to": "auth"},
                                {"label": "Expose the file server directly to the internet with a password", "outcome": "bad",
                                 "feedback": "A server open to the whole internet gets probed constantly, and one weak password is all it takes. Put it behind a VPN.", "to": "expose_bad"},
                                {"label": "Email copies of the files to everyone's personal address instead", "outcome": "bad",
                                 "feedback": "Now sensitive files are scattered across personal inboxes, out of your control. Give controlled access through a VPN, do not spray copies around.", "to": "email_bad"},
                            ],
                        },
                        "expose_bad": {
                            "text": "The exposed server is found by automated scanners within hours, and the password guessing begins and never stops. Anything reachable from the whole internet is under constant attack. A VPN would have kept it hidden.",
                            "choices": [],
                        },
                        "email_bad": {
                            "text": "Copies of work files now sit in personal inboxes you cannot manage or recall. Scattering data is not remote access. Give people a controlled way in instead.",
                            "choices": [],
                        },
                        "auth": {
                            "text": "The VPN is set up. How do people sign in to it?",
                            "choices": [
                                {"label": "A strong password plus a second factor, such as a code on their phone", "outcome": "good",
                                 "feedback": "Exactly. The VPN is a door into everything, so it deserves the strongest sign-in: a good password and a second factor.", "to": "win"},
                                {"label": "One shared password the whole team uses", "outcome": "bad",
                                 "feedback": "A shared password cannot be traced, is never changed when someone leaves, and leaks easily. Give each person their own strong sign-in with a second factor.", "to": "shared_bad"},
                            ],
                        },
                        "shared_bad": {
                            "text": "The shared VPN password spreads beyond the team and is never changed. One leak and a stranger has the same door into the network that staff use. Individual logins with a second factor are the fix.",
                            "choices": [],
                        },
                        "win": {
                            "text": "One encrypted tunnel, individual strong logins, a second factor on the door into everything. Staff can work from anywhere, and the office systems were never exposed to the open internet. That is remote access done safely.",
                            "choices": [],
                        },
                    },
                },
            },
            {
                "key": "segmented-map",
                "kind": "check",
                "points": 2,
                "title": "Read the segmented network",
                "diagram": "segmentation",
                "body": "<p>Here is segmentation as a picture: the same business, but "
                "divided into separate guest, staff and sensitive zones, like "
                "watertight compartments in a ship. Read the diagram above, then "
                "answer. The whole value is in what happens when something goes "
                "wrong in one compartment.</p>"
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
                "small business set-up with several weak spots hiding in plain "
                "sight: things exposed that should not be, defaults left in place, "
                "zones that were never separated. Tap each weakness you can find. "
                "This is exactly the walk-through a security review does.</p>"
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
                        {"label": "Customer Wi-Fi sharing the same network as the accounts computer", "weak": True,
                         "why": "No segmentation. A problem on a visitor's device can reach the sensitive accounts machine. These belong on separate zones."},
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
                "key": "patch-and-watch",
                "kind": "sort",
                "points": 2,
                "title": "Patch it, and watch it",
                "body": "<p>Walls and zones are the structure. The upkeep is two "
                "habits: <strong>patching</strong>, which closes known holes before "
                "they are used, and <strong>watching</strong>, which means noticing "
                "the alerts that say something is wrong. Most breaches use a hole "
                "that a patch had already fixed, or an alert that nobody read. Sort "
                "these habits into the ones that close a gap and the ones that leave "
                "it open.</p>"
                "<div class=\"cy-callout\">Tap a habit, then tap whether it closes "
                "the gap or leaves it open. Sort all six to finish.</div>",
                "payload": {
                    "prompt": "Sort each habit into Closes the gap or Leaves it open.",
                    "buckets": [
                        {"id": "closes", "label": "Closes the gap"},
                        {"id": "opens", "label": "Leaves it open"},
                    ],
                    "items": [
                        {"text": "Turning on automatic updates for computers and key software", "bucket": "closes",
                         "why": "Closes the gap. Automatic updates apply patches promptly, closing known holes before attackers reach them."},
                        {"text": "Ignoring an alert that a system is signing in from overseas at 3am", "bucket": "opens",
                         "why": "Leaves it open. An unread alert is a missed early warning. Watching means acting on the signals, not just collecting them."},
                        {"text": "Updating the router's firmware when the maker releases a fix", "bucket": "closes",
                         "why": "Closes the gap. The router is your front door; keeping its software current closes holes attackers actively look for."},
                        {"text": "Running software the vendor stopped supporting years ago", "bucket": "opens",
                         "why": "Leaves it open. Unsupported software never gets patched, so its known holes stay open forever. Replace it."},
                        {"text": "Reviewing security alerts regularly and following up the odd ones", "bucket": "closes",
                         "why": "Closes the gap. Alerts only help if someone reads them. Regular review turns them into early warnings you can act on."},
                        {"text": "Clicking 'remind me later' on updates for months", "bucket": "opens",
                         "why": "Leaves it open. Every delayed update is a known hole left open longer. Patch promptly, ideally automatically."},
                    ],
                },
            },
        ],
    },
]

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: The firewall: reading the rules ----
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
            "text": "Why is leaving Remote Desktop open to the internet so risky?",
            "options": [
                ("It is a remote-login door that automated scanners find and attack constantly", True,
                 "Yes. Exposed remote-login services are among the most scanned and attacked things online. They belong behind a VPN, not open to the world."),
                ("It makes the internet slower for staff", False,
                 "No. The risk is not speed. An exposed remote-login door is a constant target for attackers."),
                ("It uses up too much electricity", False,
                 "No. The problem is security, not power. It gives attackers a login to hammer at around the clock."),
                ("It stops the website from loading", False,
                 "No. It does not affect the website. The danger is that it is an exposed door attackers relentlessly probe."),
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
        # ---- Lesson 2: Defence in depth ----
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
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Most breaches that use a software hole use one that could have been prevented. How?",
            "options": [
                ("The hole had a patch available that was never applied", True,
                 "Yes. A great many breaches use a known hole that an update had already fixed. Prompt patching closes it before attackers arrive."),
                ("The building had no alarm system", False,
                 "No. This is about software, not physical alarms. The fix is applying the patches that close known holes."),
                ("The staff were not wearing ID badges", False,
                 "No. Badges are unrelated. The prevention is keeping software patched so known holes are closed."),
                ("The office Wi-Fi password was too long", False,
                 "No. A long password is good. The point is that unpatched software leaves known holes open."),
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
