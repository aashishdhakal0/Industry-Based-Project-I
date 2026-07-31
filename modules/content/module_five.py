"""Module 5, Firewall & Network Defence: the defences that sit around the whole
business (firewalls), dividing the network so trouble cannot spread
(segmentation), locking down remote access (VPNs), and the discipline of patches
and alerts, ending with a hunt for the weaknesses in a fictional network.

Same shape and standard as Modules 1 to 4 (see docs/module-authoring.md): a
lesson is a scrollable room of collapsible task PANELS. Each panel is a full,
deep task: several teaching paragraphs (what it is, a concrete Australian
example, why it matters, what to do), a diagram where it helps, a callout box
with a specific scenario, sometimes a mid-panel check, then the end interactive.
Points sum to 10 per lesson and bank at lesson end.

Voice: warm, confident, human. Plain Australian English. No em-dashes, no filler,
no repetition. Where a topic brushed an earlier module the angle is new: the VPN
here is remote access into the business network, not a tool for cafe Wi-Fi; and
patching goes from "install updates" to a defence discipline.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "The firewall: your network's gatekeeper",
        "reading_time_minutes": 10,
        "intro": "Meet the guard on the door of your network. Learn what a firewall "
        "actually does, the difference between the hardware and software kinds, and "
        "the honest limits of what any firewall can protect you from.",
        "tasks": [
            {
                "key": "what-firewall",
                "kind": "check",
                "points": 2,
                "title": "What a firewall actually does",
                "diagram": "firewall",
                "body": "<p>The word firewall sounds dramatic, but the idea is calm "
                "and simple. A firewall is a guard that sits between your network and "
                "the wider internet, checking the traffic trying to pass in either "
                "direction and deciding what is allowed through and what is turned "
                "away. Nothing more mysterious than a security guard on the door of a "
                "building, waving some people in and stopping others.</p>"
                "<p>Every device that reaches the internet is constantly sending and "
                "receiving little packets of data. Some of that traffic is you loading "
                "a website or sending an email, all perfectly wanted. Some of it is "
                "the internet's background noise of automated tools probing every "
                "address they can find, looking for a way in. The firewall's job is to "
                "let the wanted traffic through and quietly refuse the rest, so those "
                "probes never even reach your computers.</p>"
                "<p>This matters because your network is being knocked on far more "
                "often than you would ever notice. A business connected to the "
                "internet receives automated connection attempts constantly, day and "
                "night, from all over the world. Without a firewall, each of those "
                "knocks reaches your devices directly. With one, the overwhelming "
                "majority are stopped at the door before they are ever a "
                "problem.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "you will probably never configure a firewall yourself, and that is "
                "fine. What matters is knowing it is there, that it is doing quiet, "
                "constant work, and that it is one of the first things worth asking "
                "your IT support about: is our firewall on, and is it set up "
                "properly? A network without one is a building with no guard and the "
                "front door propped open.</div>",
                "question": "What is the main job of a firewall?",
                "hint": "Think of a guard on a door. What is it deciding about the traffic?",
                "options": [
                    ("It checks traffic between your network and the internet and decides what is allowed through", True,
                     "Yes. A firewall is the gatekeeper, letting wanted traffic pass and turning away the rest."),
                    ("It scrambles your files so only you can read them", False,
                     "That is encryption. A firewall controls network traffic, it does not encrypt your files."),
                    ("It backs up your data automatically", False,
                     "That is a backup. A firewall guards the flow of network traffic, it does not copy your data."),
                    ("It makes your internet connection faster", False,
                     "Speed is not its purpose. A firewall filters traffic for safety, not speed."),
                ],
            },
            {
                "key": "how-firewall-works",
                "kind": "check",
                "points": 2,
                "title": "Allow, deny, and the safest default",
                "body": "<p>A firewall makes its decisions using rules, and "
                "understanding the shape of those rules tells you a lot about good "
                "security in general. Each rule says something like 'allow this kind "
                "of traffic' or 'deny that kind', based on where it is coming from, "
                "where it is going, and what sort of connection it is.</p>"
                "<p>The important part is the starting point. A well set up firewall "
                "uses what is called default-deny: it blocks everything by default, "
                "and then you open up only the specific things you actually need. This "
                "is the opposite of default-allow, where everything is let through "
                "except the handful of things you remember to block. Default-deny is "
                "far safer, because the things you forgot about stay closed rather "
                "than open. You cannot possibly list every bad thing in advance, but "
                "you can list the few good things you need.</p>"
                "<div class=\"cy-callout\"><strong>The guest list, not the "
                "banned list.</strong> Picture two ways to run the door of an event. "
                "One is a banned list: let everyone in except the specific people you "
                "have named to keep out. The other is a guest list: keep everyone out "
                "except the specific people you have named to let in. The guest list "
                "is default-deny, and it is obviously safer, because a troublemaker "
                "you never thought of still does not get in.</div>",
                "inline_check": {
                    "question": "Which firewall approach is safer, and why?",
                    "hint": "One blocks everything except what you allow. The other allows everything except what you block.",
                    "options": [
                        ("Default-deny, because anything you did not explicitly allow stays blocked", True,
                         "Yes. Blocking by default means the threats you never thought of are closed off automatically. It is the guest list, not the banned list."),
                        ("Default-allow, because it is more convenient", False,
                         "Convenient, but risky. Allowing everything by default leaves open every threat you forgot to block."),
                        ("Neither, the starting point makes no difference", False,
                         "It makes a big difference. Default-deny closes the gaps you did not anticipate; default-allow leaves them open."),
                        ("Default-allow, because it blocks more things", False,
                         "It is the other way around. Default-allow blocks only what you list; default-deny blocks everything but what you allow."),
                    ],
                },
                "body2": "<p>You will meet this same idea again and again in security, "
                "and now you have a name for it. Least access, allow only what is "
                "needed, deny the rest, is the safe default not just for firewalls but "
                "for who can open a file, who can reach a server, and what a new "
                "account can do. When in doubt, start closed and open only what you "
                "must.</p>",
                "question": "What does a 'default-deny' firewall do?",
                "hint": "Think about what happens to traffic you have not written a rule about.",
                "options": [
                    ("Blocks all traffic except the specific things you have chosen to allow", True,
                     "Yes. Default-deny starts closed and opens only what is needed, so forgotten gaps stay shut."),
                    ("Allows all traffic except the specific things you block", False,
                     "That is default-allow, the riskier approach. Default-deny starts closed, not open."),
                    ("Denies you access to your own network", False,
                     "No. It denies unwanted traffic, not your legitimate use. You allow what you need."),
                    ("Turns the firewall off by default", False,
                     "No. Default-deny is the firewall working at its safest, blocking all but the allowed traffic."),
                ],
            },
            {
                "key": "hardware-vs-software",
                "kind": "check",
                "points": 2,
                "title": "Two firewalls are better than one",
                "body": "<p>When people say firewall they can mean one of two things, "
                "and the healthiest setup uses both together. Knowing the difference "
                "helps you understand what protects what.</p>"
                "<p>A hardware firewall is a physical device at the edge of your "
                "network, very often built into the same router that connects your "
                "office to the internet. It guards the whole network at once, "
                "everything behind it, which makes it your first line of defence. A "
                "software firewall is a program running on an individual device, like "
                "the one built into Windows or macOS. It guards just that one machine, "
                "wherever it goes.</p>"
                "<p>You want both, and the reason is a familiar one: layers. The "
                "hardware firewall stops most trouble at the network's front door. But "
                "a laptop leaves the office and connects to cafe and home networks "
                "with no such guard, and there its own software firewall is what "
                "protects it. And if something nasty does get onto the network, a "
                "device's software firewall is a second wall between it and that "
                "machine. Neither replaces the other.</p>"
                "<div class=\"cy-callout\"><strong>The laptop that left the "
                "building.</strong> A consultant's laptop is well protected in the "
                "office, sitting snugly behind the company's hardware firewall. On "
                "Friday she takes it home and joins her flatmate's network, and the "
                "office firewall now protects it not at all. What stands guard is the "
                "software firewall built into the laptop itself, which is exactly why "
                "leaving it switched on matters.</div>",
                "question": "Why is it best to have both a hardware and a software firewall?",
                "hint": "Think about a device that leaves the protected office network.",
                "options": [
                    ("The hardware one guards the whole network, and the software one guards a device even when it leaves", True,
                     "Yes. They cover different situations. Together they protect the network and each device, in the office and away from it."),
                    ("Two firewalls make the internet twice as fast", False,
                     "Speed is not the point. Two firewalls provide layered protection in different situations."),
                    ("You only ever need one, so the second is pointless", False,
                     "They do different jobs. The hardware one protects the network, the software one protects a device anywhere."),
                    ("Software firewalls protect the building and hardware ones protect laptops", False,
                     "It is the other way around. Hardware guards the network edge; software guards the individual device."),
                ],
            },
            {
                "key": "firewall-limits",
                "kind": "check",
                "points": 2,
                "title": "What a firewall cannot do",
                "body": "<p>A firewall is essential, but like every control in this "
                "course it has limits, and a false sense of safety is its own risk. "
                "Knowing what a firewall does not protect you from tells you why the "
                "rest of your habits still matter.</p>"
                "<p>The key limit is this: a firewall controls traffic, but it usually "
                "cannot tell a good decision from a bad one within the traffic you "
                "have allowed. Your firewall permits web browsing and email, because "
                "you need them. So when a staff member clicks a phishing link in an "
                "email you were allowed to receive, and types their password into a "
                "convincing fake site over a connection the firewall happily permits, "
                "the firewall sees nothing wrong. The traffic looked exactly like "
                "normal web browsing, because that is what it was.</p>"
                "<p>The same goes for a threat carried in on a USB stick, or a "
                "vulnerability in software that has not been patched. A firewall "
                "guards the network's doors; it does not read your mind about which "
                "email is a trap, and it does not fix holes inside the building. This "
                "is not a weakness of firewalls, it is simply their scope. They are "
                "one strong layer, and the human habits and the patching from the rest "
                "of this course are the others.</p>"
                "<div class=\"cy-callout\"><strong>Invited straight through the "
                "gate.</strong> A council worker receives a phishing email, clicks the "
                "link, and enters her login on a fake page. The firewall never "
                "objected, because to it the traffic was ordinary web browsing, which "
                "she had every right to do. The firewall guarded the door; it could "
                "not stop her opening it from the inside. That is what the phishing "
                "training was for.</div>",
                "question": "Which of these can a firewall NOT protect you from?",
                "hint": "Think about traffic the firewall already allows, like web browsing and email.",
                "options": [
                    ("A staff member clicking a phishing link and entering their password on a fake site", True,
                     "Right. The firewall allows web browsing, so it cannot tell that a permitted connection is going to a scam. Human habits cover this gap."),
                    ("An automated probe trying to connect to your network from the internet", False,
                     "That is exactly what a firewall is good at stopping. It turns away unwanted incoming connections."),
                    ("Unwanted incoming traffic from unknown addresses", False,
                     "A firewall handles this well, blocking unwanted incoming connections at the network's edge."),
                    ("Random connection attempts from the internet's background noise", False,
                     "Blocking those constant probes is a firewall's core strength."),
                ],
            },
            {
                "key": "firewall-sort",
                "kind": "sort",
                "points": 2,
                "title": "Firewall's job, or someone else's?",
                "body": "<p>The clearest way to understand a firewall is to be clear "
                "about where it helps and where a different defence has to step in. A "
                "firewall is superb at controlling network traffic at the door. It is "
                "no help at all against a bad decision made in traffic it already "
                "allows, or a threat that never touches the network's edge.</p>"
                "<p>Sort each situation into 'A firewall helps here' or 'Needs a "
                "different defence'. Get all six right to finish.</p>",
                "payload": {
                    "prompt": "Sort each one: does a firewall help, or does it need a different defence? All six to finish.",
                    "buckets": [
                        {"id": "firewall", "label": "A firewall helps"},
                        {"id": "other", "label": "Needs a different defence"},
                    ],
                    "items": [
                        {"id": "probe", "text": "Automated tools probing your network from the internet",
                         "bucket": "firewall", "why": "Turning away unwanted incoming connections is exactly a firewall's strength."},
                        {"id": "phish", "text": "A staff member entering their password on a phishing site",
                         "bucket": "other", "why": "The firewall allows web browsing, so training and habits cover this, not the firewall."},
                        {"id": "incoming", "text": "Blocking connection attempts to a service you never use",
                         "bucket": "firewall", "why": "A default-deny firewall closes off services you have not chosen to expose."},
                        {"id": "usb", "text": "Malware carried in on a USB stick someone plugs in",
                         "bucket": "other", "why": "That never touches the network's edge, so a firewall cannot see it. Device controls and care do."},
                        {"id": "unpatched", "text": "A known hole in software that has not been updated",
                         "bucket": "other", "why": "A firewall does not fix vulnerabilities inside your systems. Patching does."},
                        {"id": "exposed", "text": "Stopping the internet from reaching your internal file server directly",
                         "bucket": "firewall", "why": "Keeping internal systems from being directly reachable is a firewall's job."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Segmentation: contain the trouble",
        "reading_time_minutes": 10,
        "intro": "One big flat network means one infection can reach everything. "
        "Learn how dividing a network into zones keeps a problem in one place, and "
        "why a separate guest network is the easiest win of all.",
        "tasks": [
            {
                "key": "flat-network",
                "kind": "check",
                "points": 2,
                "title": "The trouble with one big network",
                "body": "<p>Most small workplaces start with the simplest possible "
                "setup: one network, with everything on it. The computers, the "
                "printer, the server, the visitors' phones, the smart TV in the "
                "waiting room, all connected together and all able to talk to one "
                "another. It is called a flat network, and it works perfectly well "
                "right up until something goes wrong.</p>"
                "<p>The problem is what happens when a single device is compromised. On "
                "a flat network, that one infected machine can reach every other "
                "device, because they are all connected as equals with nothing between "
                "them. The worm you met in Module 2 lives for exactly this: it lands "
                "on one computer and copies itself across the flat network to all the "
                "others, unopposed. One careless click can become an every-machine "
                "problem in minutes.</p>"
                "<p>Think of it as an open-plan building with no internal doors. A fire "
                "starting anywhere can spread everywhere, because there is nothing to "
                "stop it. That openness is convenient for the people inside, and it is "
                "just as convenient for anything that gets in. The fix is not to "
                "abandon the network, it is to add some internal doors, which is "
                "exactly what the next panel is about.</p>"
                "<div class=\"cy-callout\"><strong>Watch for this:</strong> the "
                "riskiest thing on a flat network is often the thing nobody thinks "
                "about, like a cheap smart device or a visitor's laptop. On a flat "
                "network, that forgotten device sits as an equal beside your most "
                "important server, one hop away from it.</div>",
                "question": "What is the main danger of a flat network, where everything is connected together?",
                "hint": "Think about what a single infected device can reach.",
                "options": [
                    ("One infected device can potentially reach every other device on the network", True,
                     "Yes. With nothing separating them, a compromise anywhere can spread everywhere, which is how a worm sweeps a whole office."),
                    ("The internet becomes slower for everyone", False,
                     "Speed is not the core issue. The danger is that a single compromise can spread to everything."),
                    ("Devices cannot communicate with each other at all", False,
                     "The opposite is true. On a flat network they can all communicate, which is exactly the risk."),
                    ("Only the newest device is ever at risk", False,
                     "Any device can be the entry point, and from there the whole flat network is reachable."),
                ],
            },
            {
                "key": "segmentation",
                "kind": "check",
                "points": 2,
                "title": "Segmentation: dividing the network so trouble can't spread",
                "diagram": "segmentation",
                "body": "<p>In Module 2 you met the worm, the malware that copies "
                "itself from machine to machine across a network on its own. The reason "
                "a worm can be so devastating is usually a flat network: one big "
                "network where every device can talk to every other one, so the moment "
                "malware lands anywhere, the whole place is within reach.</p>"
                "<p>Segmentation is the fix, and the idea is beautifully simple. You "
                "divide the one big network into smaller, separate zones, so that a "
                "problem in one zone is contained there instead of spreading "
                "everywhere. It is the digital version of the watertight compartments "
                "in a ship's hull. A leak floods one compartment, the doors seal, and "
                "the ship stays afloat. Without the compartments, a single leak sinks "
                "the whole vessel.</p>"
                "<p>In a real workplace the zones follow how much you trust something "
                "and how sensitive it is. Visitors' devices go on a guest network that "
                "cannot reach anything internal. Everyday staff computers sit on their "
                "own network. And the crown jewels, the server holding patient records "
                "or the machines running the payments, sit in a tightly restricted "
                "zone that almost nothing else can touch. If a staff laptop is "
                "infected, the malware goes looking for the records server and finds "
                "the door locked, because that server lives behind its own wall.</p>"
                "<div class=\"cy-callout\"><strong>A worm meets a wall.</strong> A "
                "physiotherapy clinic's reception PC catches a worm from a dodgy "
                "download. On a flat network it would have reached the records server "
                "within minutes. But the clinic had placed that server in its own "
                "segment, so the worm spread across the reception zone and stopped "
                "dead at the boundary. What could have been a catastrophe was a bad "
                "afternoon instead.</div>",
                "inline_check": {
                    "question": "What does network segmentation mainly achieve?",
                    "hint": "Think about the watertight compartments in a ship. What do they do to a leak?",
                    "options": [
                        ("It contains a compromise to one zone instead of letting it spread across everything", True,
                         "Yes. Like watertight compartments, segmentation seals a problem into one area so it cannot reach the rest."),
                        ("It makes the internet faster for everyone", False,
                         "Speed is not the point. Segmentation is about containing a compromise, not performance."),
                        ("It removes the need for a firewall", False,
                         "No. Segmentation works alongside a firewall as another layer, it does not replace it."),
                        ("It encrypts all your files", False,
                         "That is encryption, a different control. Segmentation divides the network into contained zones."),
                    ],
                },
                "body2": "<p>You do not set this up yourself, but you benefit from it "
                "and you can ask for it. The two segmentation wins any small business "
                "can request from its IT support are a genuinely separate guest Wi-Fi, "
                "and keeping the most sensitive systems off the same network as "
                "everyday browsing and email. Both shrink how far any single infection "
                "can travel.</p>",
                "question": "On a flat network with no segmentation, what happens when one device is infected?",
                "hint": "With no internal walls, what can the malware reach?",
                "options": [
                    ("The malware can potentially reach every other device, because they are all connected together", True,
                     "Yes. With no boundaries between devices, a compromise anywhere can spread to everything on the network."),
                    ("Nothing, because devices cannot affect each other", False,
                     "On a flat network they very much can. That connectedness is exactly what lets malware spread."),
                    ("Only that one device is ever at risk", False,
                     "Not on a flat network. From that one device, everything else is reachable."),
                    ("The firewall automatically deletes the malware", False,
                     "A firewall guards the network edge, not movement between devices inside a flat network. Segmentation is what limits that."),
                ],
            },
            {
                "key": "guest-iot",
                "kind": "check",
                "points": 2,
                "title": "Guests and gadgets belong on their own network",
                "body": "<p>Segmentation can sound like a big enterprise project, but "
                "two pieces of it are simple, cheap and available to the smallest "
                "business, and together they remove a surprising amount of risk. Both "
                "are about keeping the least trustworthy things away from the most "
                "important ones.</p>"
                "<p>The first is a separate guest Wi-Fi. Visitors, customers and "
                "contractors get their own network that reaches the internet but "
                "cannot see your internal systems at all. If a visitor's phone happens "
                "to be infected, it stays walled off in the guest zone, nowhere near "
                "your files or your server. Most business routers can create a guest "
                "network in a few clicks, and there is rarely a good reason not to.</p>"
                "<p>The second is keeping smart devices, the internet-connected TVs, "
                "cameras, speakers and sensors often lumped together as the Internet "
                "of Things, off your main network. These gadgets are notorious for "
                "weak security and passwords that never get changed, which makes them "
                "an easy way in. Put them on the guest or a separate network, and a "
                "compromised smart TV cannot become a doorway to your records.</p>"
                "<div class=\"cy-callout\"><strong>The waiting-room TV.</strong> A "
                "medical practice's smart TV, sitting on the main network with the "
                "default password it shipped with, was the weakest device in the "
                "building and one hop from the patient records. Moving it onto the "
                "guest network took two minutes and turned the practice's softest "
                "target into a dead end.</div>",
                "question": "Where should visitors' devices and smart gadgets like a TV or camera be connected?",
                "hint": "Should the least trustworthy devices sit beside your most important systems, or apart from them?",
                "options": [
                    ("On a separate guest or isolated network, away from your internal systems", True,
                     "Yes. Keeping low-trust devices on their own network means a compromised one cannot reach your important systems."),
                    ("On the main network, so everything is together and simple", False,
                     "That is the flat-network risk. A weak guest device or smart gadget then sits right beside your server."),
                    ("They do not need to connect to anything", False,
                     "They usually do need the internet. The point is which network they use, keeping them separate from internal systems."),
                    ("Directly on the records server for convenience", False,
                     "That would put your most sensitive system next to your least trustworthy devices, the worst possible place."),
                ],
            },
            {
                "key": "least-access",
                "kind": "check",
                "points": 1,
                "title": "Least access, for the network",
                "body": "<p>Segmentation is really one idea you have already met, "
                "applied to the network itself: least access. In Module 4 it meant "
                "giving each person only the file access they need. Here it means "
                "letting each part of the network reach only the other parts it "
                "genuinely needs to, and nothing more.</p>"
                "<p>The reception computer needs to reach the booking system, so it "
                "may. It has no reason to reach the payroll server, so it cannot. A "
                "guest phone needs the internet, so it gets that and only that. When "
                "you set the network up this way, you are not being unfriendly, you "
                "are shrinking the map an attacker can travel. Every connection you do "
                "not need is one you can safely close, and every closed connection is "
                "a path a compromise cannot take.</p>",
                "question": "Applying 'least access' to a network means:",
                "hint": "Should each part reach everything, or only what it genuinely needs?",
                "options": [
                    ("Letting each part reach only the other parts it genuinely needs, and nothing more", True,
                     "Yes. Closing every connection you do not need shrinks the paths a compromise could travel."),
                    ("Giving every device access to everything for convenience", False,
                     "That is the flat-network problem. Least access deliberately limits what each part can reach."),
                    ("Removing everyone's access to the network", False,
                     "No. It is about matching access to genuine need, not cutting off legitimate use."),
                    ("Only the manager's computer may connect to anything", False,
                     "Not quite. It is about need, not seniority. Each device reaches what its role requires."),
                ],
            },
            {
                "key": "segment-classify",
                "kind": "classify",
                "points": 3,
                "title": "Which network does it belong on?",
                "body": "<p>Time to think like the person planning the network. Below "
                "are devices you might find in a small clinic. For each one, decide "
                "which zone it belongs in: the Guest network for low-trust visitor and "
                "smart devices, the Staff network for everyday work computers, or the "
                "Sensitive zone for the systems holding the most valuable data.</p>"
                "<p>Lean on the whole lesson: keep the least trustworthy things away "
                "from the most important ones, and give each device only the reach its "
                "job needs.</p>",
                "payload": {
                    "prompt": "Tap a device, then tap the network it belongs on. Get all six to finish.",
                    "categories": [
                        {"id": "guest", "label": "Guest"},
                        {"id": "staff", "label": "Staff"},
                        {"id": "sensitive", "label": "Sensitive"},
                    ],
                    "events": [
                        {"id": "visitor", "category": "guest",
                         "text": "A patient's phone connecting to the waiting-room Wi-Fi.",
                         "why": "A visitor device is low trust. It belongs on the guest network, away from internal systems."},
                        {"id": "reception", "category": "staff",
                         "text": "The reception computer used for bookings and email.",
                         "why": "An everyday work machine belongs on the staff network."},
                        {"id": "records", "category": "sensitive",
                         "text": "The server holding patient medical records.",
                         "why": "The most valuable data belongs in the tightly restricted sensitive zone."},
                        {"id": "tv", "category": "guest",
                         "text": "The smart TV in the waiting room.",
                         "why": "A smart gadget with weak security belongs on the guest or isolated network, not beside your systems."},
                        {"id": "nurse", "category": "staff",
                         "text": "A nurse's laptop used for daily work and notes.",
                         "why": "A staff work device belongs on the staff network."},
                        {"id": "payments", "category": "sensitive",
                         "text": "The machine that processes card payments.",
                         "why": "A payment system handles sensitive financial data, so it belongs in the sensitive zone."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Remote access and the VPN",
        "reading_time_minutes": 10,
        "intro": "The office network now reaches beyond the office. Learn how a VPN "
        "lets people work remotely through an encrypted tunnel, and why that same "
        "tunnel is a door you must lock with real care.",
        "tasks": [
            {
                "key": "remote-work",
                "kind": "check",
                "points": 2,
                "title": "The office network, from anywhere",
                "body": "<p>Work no longer stays in the building. People need to reach "
                "the office file server from home, a manager checks the internal "
                "systems from a hotel, a visiting specialist connects to the practice "
                "software between sites. All of that means letting someone outside the "
                "building reach systems that live inside it, which is genuinely useful "
                "and genuinely risky.</p>"
                "<p>The tension is easy to see. Everything in this module so far has "
                "been about keeping the outside from reaching your internal systems: "
                "the firewall turns away outsiders, segmentation walls off the "
                "sensitive zone. Remote access deliberately pokes a hole through all "
                "of that, a way for the right people to get in from the outside. Do it "
                "carelessly and you have handed attackers the same door.</p>"
                "<p>The wrong way is depressingly common: exposing an internal system "
                "straight to the internet with just a password on it, so anyone who "
                "finds it can hammer away at that password day and night. The right "
                "way is a controlled, encrypted, locked-down tunnel that only your "
                "people can use, which is exactly what a VPN provides, and what the "
                "next panel is about.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "if you or a colleague need to work remotely, how that access is set "
                "up is one of the most important security decisions the business "
                "makes. It is worth asking: how do we connect in from outside, and is "
                "it protected by more than just a password? A convenient shortcut here "
                "is a favourite way in for attackers.</div>",
                "question": "Why does remote access to the office network need special care?",
                "hint": "Think about what remote access deliberately does to the walls the firewall and segmentation built.",
                "options": [
                    ("It deliberately opens a way for outsiders to reach internal systems, which attackers can target too", True,
                     "Yes. Remote access pokes a hole through your defences for the right people, and that same door must be locked hard against everyone else."),
                    ("It makes the office internet faster", False,
                     "Speed is not the issue. The care is needed because remote access is a way into your internal systems."),
                    ("It is only ever used by attackers, never staff", False,
                     "Staff use it legitimately all the time. The point is to make sure only they can, not attackers."),
                    ("It has no real risks worth worrying about", False,
                     "It has serious risks. A poorly secured remote-access door is a favourite target for attackers."),
                ],
            },
            {
                "key": "vpn-remote",
                "kind": "check",
                "points": 2,
                "title": "The VPN as a tunnel into the network",
                "diagram": "vpn-tunnel",
                "body": "<p>A VPN, a virtual private network, is the proper way to let "
                "someone work remotely. You met the idea in Module 4 as a way to "
                "protect yourself on public Wi-Fi. Here it does a related but distinct "
                "job: it creates a secure, encrypted tunnel from a remote person's "
                "device all the way into the business network, so that working from "
                "home feels, to the systems, as though you were plugged in at the "
                "office.</p>"
                "<p>Two things make the tunnel valuable. It is encrypted, so everything "
                "travelling between the remote worker and the office is scrambled and "
                "unreadable to anyone in between, even across a dodgy home or hotel "
                "connection. And it is a single, controlled entry point, so instead of "
                "exposing lots of internal systems to the internet, you expose one "
                "well-guarded doorway and require people to come through it. That is a "
                "far smaller and far more defensible target.</p>"
                "<div class=\"cy-callout\"><strong>One guarded door, not many "
                "windows.</strong> Without a VPN, letting five staff work from home "
                "might mean exposing five different systems to the internet, five "
                "windows an attacker can try. With a VPN, all five come through one "
                "encrypted, monitored front door, which you can lock properly and "
                "watch. Fewer openings, better guarded, is the whole idea.</div>",
                "inline_check": {
                    "question": "What does a remote-access VPN create?",
                    "hint": "Think about a secure, private path from a remote device to the office systems.",
                    "options": [
                        ("An encrypted tunnel from a remote device into the business network", True,
                         "Yes. The VPN scrambles the connection and funnels remote workers through one controlled, guarded entry point."),
                        ("A faster internet connection for the office", False,
                         "Speed is not its purpose. A VPN provides a secure, encrypted path into the network."),
                        ("A backup of the office server", False,
                         "That is a backup, a different thing. A VPN is a secure tunnel for remote access."),
                        ("A public website anyone can visit", False,
                         "The opposite. A VPN is a private, controlled entry point, not something open to the public."),
                    ],
                },
                "body2": "<p>So a VPN turns many exposed openings into one guarded one, "
                "and scrambles the traffic on the way. That is a big improvement, but "
                "notice what it also means: that one door now leads all the way inside. "
                "If it is not locked properly, it is not a smaller risk, it is a single "
                "very valuable target. Which is exactly why the next panel is about "
                "keeping it locked.</p>",
                "question": "What is the security advantage of routing remote workers through a VPN?",
                "hint": "Compare exposing many systems to the internet with exposing one guarded entry point.",
                "options": [
                    ("It replaces many exposed openings with one encrypted, controlled entry point", True,
                     "Yes. Instead of exposing several internal systems, everyone comes through a single guarded, encrypted door."),
                    ("It means you no longer need passwords", False,
                     "You still need strong authentication. A VPN secures the path; it does not remove the need to prove who you are."),
                    ("It makes the internal systems public", False,
                     "The opposite. It keeps them private, reachable only through the controlled tunnel."),
                    ("It removes the need for a firewall", False,
                     "No. A VPN works alongside the firewall and segmentation as another layer, not a replacement."),
                ],
            },
            {
                "key": "vpn-risks",
                "kind": "check",
                "points": 2,
                "title": "A tunnel is a door: lock it hard",
                "body": "<p>Here is the sharp edge of the VPN, and it is important. "
                "Because a VPN leads all the way into your network, it is one of the "
                "most valuable doors an attacker can find, and remote-access systems "
                "are among the most heavily targeted things on the internet. A VPN set "
                "up carelessly does not reduce your risk, it concentrates it into one "
                "high-value target.</p>"
                "<p>Locking it hard comes down to three things. First, multi-factor "
                "authentication on the VPN, always, so that a stolen password alone "
                "cannot open the tunnel. A password-only VPN is a disaster waiting to "
                "happen, because attackers try leaked passwords against remote access "
                "constantly. Second, keeping the VPN software itself patched and up to "
                "date, because flaws in remote-access systems are found regularly and "
                "attacked within days. Third, least access again: someone coming "
                "through the VPN should reach only what their role needs, not the "
                "entire network, so a compromised account is still contained.</p>"
                "<div class=\"cy-callout\"><strong>The unpatched door.</strong> A "
                "regional firm ran a remote-access system it had not updated in "
                "months. A known flaw in that exact system was being actively "
                "exploited across the country, and one night an attacker walked through "
                "the unpatched, password-only tunnel and straight into the network. "
                "MFA and a timely patch would each, on their own, have kept the door "
                "shut.</div>",
                "question": "What is the most important protection to put on a remote-access VPN?",
                "hint": "The attack usually starts with a stolen or guessed password. What stops that alone from working?",
                "options": [
                    ("Multi-factor authentication, so a stolen password by itself cannot open the tunnel", True,
                     "Yes. MFA is essential on a VPN, because attackers relentlessly try leaked passwords against remote access. Keep it patched too."),
                    ("A faster internet plan for the office", False,
                     "Speed does nothing for security. A VPN's first protection is strong authentication like MFA."),
                    ("Making the VPN reachable by anyone to be helpful", False,
                     "That is the danger, not the fix. A VPN should be locked down with MFA and patching, not opened up."),
                    ("Turning off the firewall once the VPN is on", False,
                     "Never. The firewall and the VPN are layers that work together. You keep both."),
                ],
            },
            {
                "key": "remote-hygiene",
                "kind": "check",
                "points": 1,
                "title": "The device at the other end matters",
                "body": "<p>One more piece completes the remote-access picture, and it "
                "is easy to overlook. A VPN secures the tunnel, but it does nothing "
                "about the state of the device at the far end of it. If a staff "
                "member's home laptop is riddled with malware, connecting it to the "
                "office over a perfectly secure VPN simply gives that malware a clean, "
                "encrypted road into your network.</p>"
                "<p>This is why remote work is a shared responsibility. The business "
                "provides the secure tunnel and the rules; the remote worker keeps "
                "their end trustworthy, with an up-to-date, protected device, ideally "
                "one provided or approved for work rather than a shared family "
                "computer. The tunnel is only as safe as the two ends it connects.</p>",
                "question": "A staff member connects to the office VPN from a home laptop that is full of malware. What is the risk?",
                "hint": "The tunnel is secure, but what is it now connecting to your network?",
                "options": [
                    ("The malware gets a secure road into the office network, because the VPN protects the tunnel, not the device", True,
                     "Yes. A VPN secures the connection, but a compromised device at the far end can carry its infection straight in."),
                    ("None, because the VPN cleans the laptop automatically", False,
                     "A VPN does not scan or clean devices. It secures the connection, so the device's own health still matters."),
                    ("The VPN will run more slowly, but that is all", False,
                     "The real risk is not speed. An infected device can bring its malware into the network through the tunnel."),
                    ("The office firewall will delete the malware on the laptop", False,
                     "The firewall does not reach out and clean a remote personal device. The device's own security is what counts."),
                ],
            },
            {
                "key": "remote-branch",
                "kind": "branch",
                "points": 3,
                "title": "Setting up remote access",
                "body": "<p>Put it into practice. A staff member needs to work from "
                "home, and it falls to you to help decide how they will connect. Make "
                "the calls you would really make. There are no trick questions, and if "
                "a choice goes wrong you will see why and get another go.</p>"
                "<p>The thread to hold onto: a controlled encrypted tunnel beats an "
                "exposed system, a password alone is never enough on a door into your "
                "network, and the device at the far end has to be trustworthy "
                "too.</p>",
                "payload": {
                    "prompt": "Choose what you would really do. You can always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "Priya needs to reach the office file server from home. The quickest option is to "
                            "expose the server straight to the internet with her password on it. What do you do?",
                            "choices": [
                                {"label": "Expose the server to the internet, it is just one password", "to": "n1bad",
                                 "outcome": "bad",
                                 "feedback": "An internet-exposed server with only a password is hammered by automated attacks constantly. This is the classic way in."},
                                {"label": "Set up a VPN so she comes through one encrypted, controlled door", "to": "n2",
                                 "outcome": "good",
                                 "feedback": "Right. A VPN gives one guarded, encrypted entry point instead of exposing the server itself."},
                            ],
                        },
                        "n1bad": {
                            "text": "Within a day, automated tools are trying thousands of passwords against the exposed server.",
                            "choices": [{"label": "See the better path", "to": "n2"}],
                        },
                        "n2": {
                            "text": "The VPN is ready. How should Priya prove who she is when she connects?",
                            "choices": [
                                {"label": "A password alone, to keep it simple", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "A password-only VPN is a disaster waiting to happen, because attackers try leaked passwords against remote access relentlessly."},
                                {"label": "Her password plus multi-factor authentication", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Yes. MFA on the VPN means a stolen password by itself cannot open the tunnel."},
                            ],
                        },
                        "n2bad": {
                            "text": "A month later, Priya's password leaks from another site, and it opens the VPN too.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "Priya asks to connect from the shared family computer, which is old and rarely updated. What do you say?",
                            "choices": [
                                {"label": "Fine, the VPN keeps it safe anyway", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "The VPN secures the tunnel, not the device. An old, unprotected computer can carry malware straight in through it."},
                                {"label": "Use a work-approved, up-to-date device for the connection", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Right. The tunnel is only as safe as the device at each end, so the remote machine needs to be trustworthy too."},
                            ],
                        },
                        "n3bad": {
                            "text": "The family computer had malware, which used the secure tunnel as a clean road into the office network.",
                            "choices": [{"label": "See the better path", "to": "end"}],
                        },
                        "end": {
                            "text": "That is remote access set up well: a VPN instead of an exposed system, MFA on the tunnel, and a "
                            "trustworthy device at the far end. You gave people the access they needed without handing attackers a door.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
    {
        "title": "Alerts, patches, and finding the gaps",
        "reading_time_minutes": 9,
        "intro": "Two everyday defences that quietly matter most: keeping software "
        "patched, and taking security alerts seriously. Then put the whole module "
        "together by finding the weaknesses in a real-looking network.",
        "tasks": [
            {
                "key": "patch-management",
                "kind": "check",
                "points": 2,
                "title": "Patching: closing the holes before they are used",
                "body": "<p>Module 1 told you to install updates. This lesson is about "
                "why that simple habit is one of the most powerful network defences "
                "there is, and what goes wrong when it slips. A patch is an update "
                "that fixes a security hole in software, and applying patches promptly "
                "is called patch management.</p>"
                "<p>The reason timing matters so much is the risk window. When a "
                "security flaw is discovered, it usually becomes public knowledge, and "
                "the fix is released at the same time. From that moment, two races "
                "begin: you racing to install the patch, and attackers racing to "
                "exploit the flaw on everyone who has not. Automated tools scan the "
                "whole internet for unpatched systems within days, sometimes hours, of "
                "a flaw becoming known. Every day a patch is not applied is a day your "
                "system carries a hole that attackers already have a map to.</p>"
                "<p>The practical answer is to make patching automatic wherever you "
                "can, so devices and software update themselves without waiting for "
                "someone to remember, and to pay special attention to the systems that "
                "face the internet, like the firewall, the router and any remote-access "
                "system, because those are what the automated scans find first. The "
                "unpatched, internet-facing system is one of the most common ways "
                "Australian organisations are breached.</p>"
                "<div class=\"cy-callout\"><strong>The known hole nobody "
                "closed.</strong> A business kept meaning to update its remote-access "
                "system, but it was never quite the right week. The flaw was public, "
                "the patch was available, and automated tools were already scanning "
                "for exactly that unpatched system. The break-in did not need a genius, "
                "only a door that had been left unlocked after everyone was told which "
                "door it was.</div>",
                "question": "Why does applying security patches promptly matter so much?",
                "hint": "Think about the gap between a flaw becoming known and you fixing it.",
                "options": [
                    ("Once a flaw is public, attackers race to exploit unpatched systems, often within days", True,
                     "Yes. The patch and the flaw usually go public together, so every day unpatched is a day attackers have a map to your hole."),
                    ("Patches always make software run faster", False,
                     "Speed is not the point. Patches close known security holes before attackers can use them."),
                    ("Patches change the colour of the screen", False,
                     "Appearance is incidental. The security value is in closing known vulnerabilities."),
                    ("There is no rush, because attackers cannot find unpatched systems", False,
                     "They very much can. Automated tools scan the whole internet for unpatched systems within days of a flaw becoming known."),
                ],
            },
            {
                "key": "reading-alerts",
                "kind": "check",
                "points": 2,
                "title": "Taking security alerts seriously",
                "body": "<p>Your defences talk to you. Antivirus quarantines "
                "something, the browser warns that a connection is not private, an app "
                "asks you to approve a login. These are security alerts, and how you "
                "respond to them is a real part of your network's defence. The two "
                "failures are opposite: panicking at every one, and ignoring the ones "
                "that matter.</p>"
                "<p>A particular alert is worth singling out, because attackers abuse "
                "it: the unexpected multi-factor prompt. If your phone buzzes asking "
                "you to approve a login that you did not just start, that is not a "
                "glitch to dismiss, it is a signal that someone has your password and "
                "is trying to get in right now. The correct response is to deny it and "
                "report it, never to approve it. Attackers even send a flood of these "
                "prompts hoping you will approve one just to stop the buzzing, a trick "
                "that only works if you do not know what the prompt means.</p>"
                "<p>The general rule is calm and simple. A security alert you did not "
                "expect deserves a moment of attention, not a reflexive click to make "
                "it go away. When in doubt, do not approve, do not dismiss, and ask. A "
                "genuine alert reported early is a problem caught small; a genuine "
                "alert clicked away is an open door.</p>"
                "<div class=\"cy-callout\"><strong>Never approve a prompt you did not "
                "start.</strong> The single most useful habit with alerts is this one. "
                "An approval request for a login you did not begin means someone else "
                "is holding your password. Denying it stops them cold, and reporting "
                "it gets your password changed before they try again.</div>",
                "inline_check": {
                    "question": "Your phone keeps buzzing with login-approval requests you did not start. What should you do?",
                    "hint": "Who is triggering those prompts, and what would approving one do?",
                    "options": [
                        ("Deny them and report it, because someone likely has your password and is trying to log in", True,
                         "Yes. An approval request you did not start means someone else has your password. Deny it and get the password changed."),
                        ("Approve one so the buzzing stops", False,
                         "Never. That is exactly the trick. Approving one lets the attacker in. Deny, and report it."),
                        ("Ignore it, it is probably just a glitch", False,
                         "It is not a glitch. Repeated prompts you did not start are a live attempt to get into your account."),
                        ("Turn your phone off and carry on", False,
                         "That leaves the attempt unreported and your password still compromised. Deny the prompts and report it."),
                    ],
                },
                "body2": "<p>The same balance from Module 2, notice but do not panic, "
                "applies here. Not every warning is a crisis, and a workplace drowning "
                "in false alarms will start ignoring them, which is its own danger. "
                "The aim is a calm habit: take unexpected security alerts seriously "
                "enough to check, report the genuine ones, and let your IT support "
                "help tune out the noise over time.</p>",
                "question": "What is the safest response to an unexpected security alert or prompt?",
                "hint": "Should you click it away to stop the nagging, or pause on it?",
                "options": [
                    ("Give it a moment of attention: do not approve, do not dismiss, and ask if unsure", True,
                     "Yes. An unexpected alert deserves a pause, not a reflexive click. Report the genuine ones early."),
                    ("Always approve it so it stops appearing", False,
                     "Approving a prompt you did not start can let an attacker in. Never click one away just to be rid of it."),
                    ("Always ignore it, since alerts are just noise", False,
                     "Some alerts are genuine and important. Ignoring them all is how a real problem is missed."),
                    ("Immediately shut down the whole network", False,
                     "Over-reacting to every alert causes its own harm. Pause, check, and report the genuine ones."),
                ],
            },
            {
                "key": "netmap",
                "kind": "netmap",
                "points": 4,
                "title": "Find the weaknesses",
                "body": "<p>Everything in this module comes together in one job: "
                "looking at a network and spotting where it is exposed. Below is the "
                "setup at the fictional Riverside Clinic, drawn as a simple map of its "
                "devices. Some are configured well and some carry a weakness you now "
                "know how to recognise.</p>"
                "<p>Tap every weakness you can find. Think about everything from this "
                "module: default passwords on the gatekeeper, unpatched systems, "
                "low-trust devices sitting beside sensitive ones, and remote access "
                "left open. Find them all to finish.</p>",
                "payload": {
                    "prompt": "Tap every weakness in the Riverside Clinic network. Find all of them to finish.",
                    "nodes": [
                        {"id": "firewall", "label": "Router / Firewall", "detail": "Admin password still the factory default",
                         "weak": True,
                         "why": "A default admin password lets anyone who reaches the gatekeeper take it over. Change it to something strong and unique."},
                        {"id": "server", "label": "Records server", "detail": "Not updated in 14 months",
                         "weak": True,
                         "why": "An unpatched server is full of known holes that automated tools actively scan for. It needs patching, urgently."},
                        {"id": "guest", "label": "Guest Wi-Fi", "detail": "On the same network as the clinical systems",
                         "weak": True,
                         "why": "A guest device could reach sensitive systems. Guests belong on a separate, isolated segment."},
                        {"id": "tv", "label": "Waiting-room smart TV", "detail": "On the main network with its default password",
                         "weak": True,
                         "why": "A weak smart device beside your systems is an easy way in. Move it to the guest network and change its password."},
                        {"id": "remote", "label": "Remote access", "detail": "Open to the internet, password only, no MFA",
                         "weak": True,
                         "why": "Password-only remote access is relentlessly attacked. It needs multi-factor authentication and to be kept patched."},
                        {"id": "reception", "label": "Reception PC", "detail": "Updates on automatically, screen auto-locks",
                         "weak": False,
                         "why": "Patched and locked. This one is set up well, nothing to fix here."},
                        {"id": "backup", "label": "Nightly backup", "detail": "Kept offsite and tested last month",
                         "weak": False,
                         "why": "A tested, offsite backup is exactly right. This is a strength, not a weakness."},
                    ],
                },
            },
            {
                "key": "defence-recap",
                "kind": "check",
                "points": 2,
                "title": "Your network defence habits",
                "body": "<p>That is the whole module, and it comes down to a handful of "
                "layered defences you can now recognise and ask about. A firewall "
                "guards the network's doors, ideally default-deny, with both a hardware "
                "and a software one. Segmentation divides the network so trouble in one "
                "zone cannot spread, starting with a separate guest and smart-device "
                "network. Remote access comes through a locked-down VPN with MFA, not "
                "an exposed system. And underneath it all, everything is kept patched "
                "and security alerts are taken seriously.</p>"
                "<p>You will not configure most of this yourself, and you do not need "
                "to. What you can do is recognise a weakness when you see one, ask your "
                "IT support the right questions, and never be the person who props a "
                "door open for convenience. Network defence is layers, and an informed "
                "person is one of the strongest layers of all.</p>",
                "question": "What is the single idea that ties all of these network defences together?",
                "hint": "No single control is perfect. What do you do instead of relying on one?",
                "options": [
                    ("Layer several defences, so a gap in one is covered by the others", True,
                     "Yes. Firewall, segmentation, locked-down remote access and patching are layers. Together they mean one weakness is not a disaster."),
                    ("Pick the single best defence and rely only on that", False,
                     "No single control is enough. The strength is in layering them, so a gap in one is covered by another."),
                    ("Leave it all to the firewall", False,
                     "A firewall is one layer. It cannot stop a phishing click, an unpatched hole, or spread across a flat network."),
                    ("Assume you are too small to be a target", False,
                     "Automated attacks do not care how small you are. Layered defences protect businesses of every size."),
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
        # ---- Lesson 1: firewalls ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is the main job of a firewall?",
            "options": [
                ("To check traffic between your network and the internet and decide what is allowed through", True,
                 "Yes. A firewall is the gatekeeper, letting wanted traffic pass and turning away the rest."),
                ("To scramble your files so only you can read them", False,
                 "That is encryption. A firewall controls network traffic, not file contents."),
                ("To back up your data automatically", False,
                 "That is a backup. A firewall filters traffic, it does not copy data."),
                ("To make your internet faster", False,
                 "Speed is not its job. A firewall filters traffic for safety."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A firewall set to 'default-deny' will:",
            "options": [
                ("Block all traffic except the specific things you have chosen to allow", True,
                 "Yes. It starts closed and opens only what is needed, so forgotten gaps stay shut."),
                ("Allow all traffic except what you specifically block", False,
                 "That is default-allow, the riskier approach. Default-deny starts closed."),
                ("Block you from using your own network", False,
                 "No. It blocks unwanted traffic, not your legitimate use."),
                ("Switch the firewall off", False,
                 "No. Default-deny is the firewall working at its safest."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why is default-deny safer than default-allow?",
            "options": [
                ("Anything you did not explicitly allow stays blocked, including threats you never thought of", True,
                 "Yes. It is the guest list, not the banned list, so unanticipated threats are closed off automatically."),
                ("It lets more traffic through", False,
                 "It lets less through, only what you allow. That is what makes it safer."),
                ("It is simply more convenient", False,
                 "Convenience favours default-allow. Default-deny trades a little convenience for much better safety."),
                ("It makes no real difference", False,
                 "It makes a big difference by closing the gaps you did not anticipate."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is the difference between a hardware and a software firewall?",
            "options": [
                ("A hardware firewall guards the whole network at its edge; a software one guards a single device", True,
                 "Yes. They cover different situations, which is why using both gives the best protection."),
                ("A hardware firewall guards one laptop; a software one guards the whole building", False,
                 "It is the other way around. Hardware guards the network edge; software guards the individual device."),
                ("They are two names for exactly the same thing", False,
                 "They are different. One protects the network edge, the other protects a device wherever it goes."),
                ("Only hardware firewalls actually work", False,
                 "Both work and do different jobs. The software one protects a device even when it leaves the network."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why should a laptop have its own software firewall on, even if the office has a hardware one?",
            "options": [
                ("Because when the laptop leaves the office, the hardware firewall no longer protects it", True,
                 "Yes. Away from the office network, the device's own software firewall is what stands guard."),
                ("Because software firewalls make laptops faster", False,
                 "Speed is not the point. It is about protection when the device is off the office network."),
                ("Because the hardware firewall stops working at night", False,
                 "The hardware firewall keeps running. The issue is that it only protects devices on its network."),
                ("Because laptops cannot use hardware firewalls at all", False,
                 "A laptop is protected by the hardware firewall while on that network. Off it, the software firewall matters."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "Which of these can a firewall NOT protect you from?",
            "options": [
                ("A staff member clicking a phishing link and entering their password on a fake site", True,
                 "Right. The firewall allows web browsing, so it cannot tell a permitted connection is going to a scam. Human habits cover this."),
                ("Automated probes trying to connect from the internet", False,
                 "Blocking those is a firewall's core strength."),
                ("Unwanted incoming traffic from unknown addresses", False,
                 "A firewall handles this well at the network's edge."),
                ("The internet reaching your internal server directly", False,
                 "Keeping internal systems from being directly reachable is exactly a firewall's job."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "A firewall mainly protects your network by:",
            "options": [
                ("Turning away unwanted traffic at the boundary between your network and the internet", True,
                 "Yes. It filters what may pass in and out, stopping most unwanted traffic at the door."),
                ("Deleting viruses already on your computer", False,
                 "That is antivirus. A firewall controls traffic at the network boundary."),
                ("Encrypting your web browsing", False,
                 "That is what HTTPS does. A firewall filters traffic, it does not encrypt it."),
                ("Storing your passwords safely", False,
                 "That is a password manager. A firewall guards network traffic."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Malware carried into the office on a USB stick is a gap a firewall cannot cover because:",
            "options": [
                ("It never crosses the network boundary the firewall guards", True,
                 "Yes. A firewall watches traffic at the network's edge. A USB threat bypasses that entirely, so other controls are needed."),
                ("Firewalls only work on weekends", False,
                 "Firewalls run constantly. The issue is that a USB threat does not pass through the network boundary."),
                ("USB sticks are always safe", False,
                 "They are not. An unknown USB can carry malware, which is why this gap needs care and device controls."),
                ("The firewall would make the USB faster", False,
                 "Speed is irrelevant. The point is that a USB threat bypasses the firewall's view."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "The best firewall setup for most workplaces is:",
            "options": [
                ("Both a hardware firewall at the network edge and a software one on each device", True,
                 "Yes. Layers. The hardware one guards the network, the software one guards each device anywhere."),
                ("Neither, they are unnecessary", False,
                 "A firewall is a core defence. A network without one is a building with no guard on the door."),
                ("Only a software firewall, never hardware", False,
                 "The hardware firewall guards the whole network at once. You want both, not one."),
                ("As many firewalls as possible, turned off", False,
                 "A firewall only helps when it is on. Two working firewalls, hardware and software, is the goal."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "'Least access', applied to a firewall, means:",
            "options": [
                ("Allow only the traffic that is genuinely needed, and deny the rest", True,
                 "Yes. Start closed and open only what you must, so unanticipated threats stay blocked."),
                ("Allow everything so nobody is inconvenienced", False,
                 "That is the risky default-allow. Least access deliberately permits only what is needed."),
                ("Block all traffic including your own legitimate use", False,
                 "No. It blocks unwanted traffic while allowing the specific things you need."),
                ("Give the newest device the most access", False,
                 "Access follows genuine need, not how new a device is."),
            ],
        },
        # ---- Lesson 2: segmentation ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What is the main danger of a flat network?",
            "options": [
                ("One infected device can potentially reach every other device", True,
                 "Yes. With nothing separating them, a compromise anywhere can spread everywhere."),
                ("The internet becomes slower", False,
                 "Speed is not the core danger. The risk is uncontained spread of a compromise."),
                ("Devices cannot talk to each other", False,
                 "On a flat network they all can, which is exactly the risk."),
                ("Only the newest device is at risk", False,
                 "Any device can be the entry point, and from there everything is reachable."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What does network segmentation achieve?",
            "options": [
                ("It contains a compromise to one zone instead of letting it spread across everything", True,
                 "Yes. Like watertight compartments, it seals a problem into one area."),
                ("It makes the internet faster", False,
                 "Speed is not the point. Segmentation is about containment."),
                ("It removes the need for a firewall", False,
                 "No. It works alongside a firewall as another layer."),
                ("It encrypts all your files", False,
                 "That is encryption, a different control."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A helpful way to picture segmentation is:",
            "options": [
                ("Watertight compartments in a ship, so one leak floods only one section", True,
                 "Yes. The compartments contain the leak, just as segments contain a compromise."),
                ("A single open-plan room with no doors", False,
                 "That is a flat network, the opposite of segmentation."),
                ("A faster internet cable", False,
                 "Segmentation is about containment, not speed."),
                ("A backup kept in the cloud", False,
                 "That is a backup. Segmentation divides the network into contained zones."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Where should visitors' devices connect?",
            "options": [
                ("On a separate guest network that cannot reach internal systems", True,
                 "Yes. A guest network gives them the internet while keeping them away from your systems."),
                ("On the main network with everything else", False,
                 "That is the flat-network risk. A visitor device then sits beside your server."),
                ("Directly on the records server", False,
                 "The worst place. Low-trust devices should be kept away from sensitive systems."),
                ("They should never have any internet access", False,
                 "They usually need the internet. The point is to keep them on a separate network."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Why keep smart devices, like an internet-connected TV, off the main network?",
            "options": [
                ("They often have weak security and unchanged passwords, making them an easy way in", True,
                 "Yes. A compromised smart device on the main network is one hop from your important systems."),
                ("They use too much electricity", False,
                 "Power use is not the security concern. Their weak security is."),
                ("They cannot connect to Wi-Fi anyway", False,
                 "They connect readily, which is why keeping them on a separate network matters."),
                ("They make the TV picture blurry", False,
                 "Picture quality is irrelevant. The issue is their weak security beside your systems."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "A reception PC has no need to reach the payroll server. Applying 'least access' to the network means:",
            "options": [
                ("The reception PC should not be able to reach the payroll server", True,
                 "Yes. Closing connections that are not needed shrinks the paths a compromise could travel."),
                ("Every device should reach every other for convenience", False,
                 "That is the flat-network problem. Least access limits reach to genuine need."),
                ("Only the manager's PC may connect to anything", False,
                 "It is about need, not seniority. Each device reaches what its role requires."),
                ("Nobody should be able to use the network", False,
                 "No. Legitimate use continues; only unneeded connections are closed."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A worm infects a reception PC. On a well-segmented network, what happens?",
            "options": [
                ("It spreads within that zone but is stopped at the boundary of the sensitive zone", True,
                 "Yes. Segmentation contains the worm, so the crown-jewel systems behind their own wall stay safe."),
                ("It instantly reaches the records server", False,
                 "That is what happens on a flat network. Segmentation is designed to stop exactly this."),
                ("It is automatically deleted by the router", False,
                 "A router does not clean infections. Segmentation limits how far the worm can travel."),
                ("Nothing at all happens", False,
                 "The infected zone is still affected. The benefit is that it cannot spread to the sensitive systems."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "The easiest segmentation win for a small business is:",
            "options": [
                ("Turning on a separate guest Wi-Fi network", True,
                 "Yes. Most business routers can do it in a few clicks, and it keeps low-trust devices off your systems."),
                ("Unplugging the internet entirely", False,
                 "That is not practical. A separate guest network is the simple, sensible win."),
                ("Giving every device access to everything", False,
                 "That is the opposite of segmentation. Keep low-trust devices separate."),
                ("Buying a faster router", False,
                 "Speed does not segment a network. A separate guest network does."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Where does a server holding sensitive customer records belong?",
            "options": [
                ("In a tightly restricted sensitive zone that almost nothing else can reach", True,
                 "Yes. The most valuable data belongs behind its own wall, reachable only by what genuinely needs it."),
                ("On the guest network for convenience", False,
                 "Never. That would place your crown jewels beside the least trustworthy devices."),
                ("On the same flat network as everything else", False,
                 "That leaves it one hop from any infected device. It belongs in its own segment."),
                ("On the waiting-room TV", False,
                 "That makes no sense and would be extremely exposed. Sensitive data belongs in a restricted zone."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Segmentation is essentially which idea, applied to the network?",
            "options": [
                ("Least access: each part reaches only what it genuinely needs", True,
                 "Yes. It is the same least-access principle from file sharing, applied to how parts of the network connect."),
                ("Making everything reachable for speed", False,
                 "The opposite. Segmentation deliberately limits what each part can reach."),
                ("Encrypting every file twice", False,
                 "That is not what segmentation is. It divides the network into contained zones."),
                ("Backing up the whole network nightly", False,
                 "That is a backup. Segmentation is about containing a compromise."),
            ],
        },
        # ---- Lesson 3: remote access and VPN ----
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why does remote access to the office network need special care?",
            "options": [
                ("It deliberately opens a way for outsiders to reach internal systems, which attackers can target too", True,
                 "Yes. It pokes a hole through your defences for the right people, so that door must be locked hard against everyone else."),
                ("It makes the office internet faster", False,
                 "Speed is not the issue. The care is needed because it is a way into your systems."),
                ("It is only ever used by attackers", False,
                 "Staff use it legitimately. The goal is to ensure only they can, not attackers."),
                ("It has no real risks", False,
                 "A poorly secured remote-access door is a favourite target for attackers."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What does a remote-access VPN create?",
            "options": [
                ("An encrypted tunnel from a remote device into the business network", True,
                 "Yes. It scrambles the connection and funnels remote workers through one controlled entry point."),
                ("A faster internet connection", False,
                 "Speed is not its purpose. It provides a secure, encrypted path into the network."),
                ("A backup of the office server", False,
                 "That is a backup. A VPN is a secure tunnel for remote access."),
                ("A public website anyone can visit", False,
                 "The opposite. A VPN is a private, controlled entry point."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "The security advantage of routing remote workers through a VPN is that it:",
            "options": [
                ("Replaces many exposed openings with one encrypted, controlled entry point", True,
                 "Yes. Instead of exposing several systems, everyone comes through a single guarded, encrypted door."),
                ("Removes the need for passwords", False,
                 "You still need strong authentication. A VPN secures the path, it does not replace proving who you are."),
                ("Makes internal systems public", False,
                 "The opposite. It keeps them private, reachable only through the tunnel."),
                ("Removes the need for a firewall", False,
                 "No. It works alongside the firewall as another layer."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "What is the most important protection to put on a remote-access VPN?",
            "options": [
                ("Multi-factor authentication, so a stolen password alone cannot open the tunnel", True,
                 "Yes. Attackers relentlessly try leaked passwords against remote access, so MFA is essential. Keep it patched too."),
                ("A faster internet plan", False,
                 "Speed does nothing for security. Strong authentication like MFA is the first protection."),
                ("Making it reachable by anyone", False,
                 "That is the danger, not the fix. A VPN must be locked down, not opened up."),
                ("Turning off the firewall once it is on", False,
                 "Never. The VPN and firewall are layers that work together."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why is keeping a VPN's software patched so important?",
            "options": [
                ("Flaws in remote-access systems are found regularly and attacked within days", True,
                 "Yes. Because a VPN leads into your network, an unpatched one is a high-value, actively targeted door."),
                ("Patches make the VPN faster", False,
                 "Speed is not the point. Patches close known holes attackers are already exploiting."),
                ("A patched VPN needs no password", False,
                 "You still need MFA and a password. Patching closes vulnerabilities, it does not replace authentication."),
                ("VPNs never have security flaws", False,
                 "They do, and remote-access flaws are among the most exploited. Prompt patching is essential."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "A staff member connects to the office VPN from a home laptop riddled with malware. The risk is that:",
            "options": [
                ("The malware gets a secure road into the network, because the VPN protects the tunnel, not the device", True,
                 "Yes. A VPN secures the connection, but a compromised device at the far end can carry its infection straight in."),
                ("Nothing, the VPN cleans the laptop", False,
                 "A VPN does not scan or clean devices. The device's own health still matters."),
                ("The VPN just runs slower", False,
                 "The real risk is the malware reaching the network through the tunnel, not speed."),
                ("The office firewall deletes the malware remotely", False,
                 "The firewall does not clean a remote personal device. That device's security is what counts."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "The riskiest way to let a staff member work from home is to:",
            "options": [
                ("Expose the internal server straight to the internet with only a password", True,
                 "Yes. An internet-exposed, password-only system is hammered by automated attacks constantly. Use a VPN with MFA instead."),
                ("Set up a VPN with multi-factor authentication", False,
                 "That is the safe way, not the risky one. It gives one guarded, encrypted door."),
                ("Use a work-approved, up-to-date device", False,
                 "That is good practice. The risk is exposing a system directly with just a password."),
                ("Keep the remote-access software patched", False,
                 "That is exactly what you should do. The risk is an exposed, password-only system."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "How is a VPN for remote access different from using a VPN on public Wi-Fi?",
            "options": [
                ("Remote access connects you into the business network; on public Wi-Fi it mainly shields your own traffic", True,
                 "Yes. Same encryption idea, different job: one is a doorway into the office, the other protects you on an untrusted network."),
                ("They are completely unrelated and share nothing", False,
                 "They share the encrypted-tunnel idea. The difference is what the tunnel connects you to."),
                ("A remote-access VPN needs no security", False,
                 "It needs strong security precisely because it leads into your network."),
                ("Public Wi-Fi VPNs are the only real kind", False,
                 "Both are real and useful. Remote-access VPNs connect people into the business network."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "Remote work is a shared responsibility because:",
            "options": [
                ("The business provides a secure tunnel and rules, and the worker keeps their device trustworthy", True,
                 "Yes. The tunnel is only as safe as the two ends it connects, so both sides have a part to play."),
                ("Only the business ever needs to do anything", False,
                 "The remote device matters too. A compromised laptop can carry malware in through a secure tunnel."),
                ("Only the worker ever needs to do anything", False,
                 "The business must provide and lock down the access. Both sides share the responsibility."),
                ("Nobody is responsible for remote security", False,
                 "Both sides are. Secure remote work depends on the tunnel and the device being trustworthy."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "'Least access' applied to a VPN connection means someone coming through it should:",
            "options": [
                ("Reach only the systems their role needs, not the whole network", True,
                 "Yes. Limiting reach means a compromised remote account is still contained, not a free run of everything."),
                ("Automatically become a network administrator", False,
                 "That is the opposite of least access, and dangerous. Remote users should reach only what they need."),
                ("Be able to reach every system for convenience", False,
                 "Broad reach spreads risk. Least access keeps a remote connection to what its role requires."),
                ("Lose all access to their own files", False,
                 "No. They keep the access they need; they simply do not get more than that."),
            ],
        },
        # ---- Lesson 4: patching, alerts, finding gaps ----
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Why does applying security patches promptly matter so much?",
            "options": [
                ("Once a flaw is public, attackers race to exploit unpatched systems, often within days", True,
                 "Yes. The patch and the flaw usually go public together, so every unpatched day is a day attackers have a map to your hole."),
                ("Patches make software run faster", False,
                 "Speed is not the point. Patches close known security holes."),
                ("Patches change how the screen looks", False,
                 "Appearance is incidental. The value is closing vulnerabilities."),
                ("There is no rush, attackers cannot find unpatched systems", False,
                 "They can, within days, using automated scans of the whole internet."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "What is a 'patch'?",
            "options": [
                ("An update that fixes a security hole in software", True,
                 "Yes, and applying patches promptly is one of the most powerful defences there is."),
                ("A type of firewall", False,
                 "No. A patch is a software update that fixes a vulnerability."),
                ("A backup copy of your files", False,
                 "That is a backup. A patch fixes a flaw in software."),
                ("A password for your router", False,
                 "No. A patch is an update that closes a security hole."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Which systems most deserve prompt patching?",
            "options": [
                ("Internet-facing systems like the firewall, router and remote-access system", True,
                 "Yes. Those are what automated scans find first, so their unpatched flaws are exploited fastest."),
                ("Only devices that are switched off", False,
                 "A switched-off device is not the concern. Internet-facing systems are the priority."),
                ("Only brand-new devices", False,
                 "Age is not the deciding factor. Internet-facing systems are the ones attackers reach first."),
                ("None, patching is optional", False,
                 "Patching is a core defence. Internet-facing systems especially must be kept current."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "The best way to keep most systems patched is to:",
            "options": [
                ("Turn on automatic updates wherever you can", True,
                 "Yes. Automation means devices update themselves without waiting for someone to remember."),
                ("Wait until something breaks before updating", False,
                 "By then a known flaw may already be exploited. Patch promptly, ideally automatically."),
                ("Never update, to avoid changes", False,
                 "That leaves known holes open. Prompt patching closes them."),
                ("Only update once a year", False,
                 "Far too slow. Flaws are exploited within days, so patch promptly and automatically."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Your phone keeps buzzing with login-approval requests you did not start. You should:",
            "options": [
                ("Deny them and report it, because someone likely has your password", True,
                 "Yes. Approval requests you did not start mean someone else holds your password. Deny, and get it changed."),
                ("Approve one so the buzzing stops", False,
                 "Never. That is the trick. Approving one lets the attacker in."),
                ("Ignore it as a glitch", False,
                 "It is not a glitch. Repeated prompts you did not start are a live attempt to get in."),
                ("Turn the phone off and carry on", False,
                 "That leaves it unreported and your password still compromised. Deny and report."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "The safest response to an unexpected security alert or prompt is to:",
            "options": [
                ("Pause: do not approve, do not dismiss, and ask if unsure", True,
                 "Yes. An unexpected alert deserves a moment of attention, not a reflexive click. Report the genuine ones."),
                ("Always approve it to make it go away", False,
                 "Approving a prompt you did not start can let an attacker in."),
                ("Always ignore it as noise", False,
                 "Some alerts are genuine and important. Ignoring them all is how a real problem is missed."),
                ("Shut down the whole network immediately", False,
                 "Over-reacting to every alert causes its own harm. Pause, check, report the genuine ones."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Attackers sometimes flood you with MFA approval prompts hoping that you will:",
            "options": [
                ("Approve one just to stop the buzzing, which lets them in", True,
                 "Yes. It only works if you do not know what the prompt means. Never approve a login you did not start."),
                ("Change your password to a stronger one", False,
                 "That is not their goal. They want you to approve a prompt so they can get in."),
                ("Turn on a firewall", False,
                 "Not their aim. They are trying to get you to approve their login attempt."),
                ("Report them to the police", False,
                 "They are hoping you approve, not report. Deny every prompt you did not start."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "On a network map, a router or firewall still set to its factory admin password is:",
            "options": [
                ("A weakness, because default passwords are published and let anyone take over the gatekeeper", True,
                 "Yes. Change it to something strong and unique. A default on the gatekeeper is a serious hole."),
                ("Fine, because the default is secret", False,
                 "Factory defaults are published online for anyone to find. That is exactly why it is a weakness."),
                ("A strength, because it is simple", False,
                 "Simplicity here is danger. A default admin password is one of the first things attackers try."),
                ("Only a problem for large companies", False,
                 "It is a problem for any network. Automated attacks target defaults everywhere."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Which of these on a network map is a strength, not a weakness?",
            "options": [
                ("A nightly backup kept offsite and tested last month", True,
                 "Yes. A tested, offsite backup is exactly right. It is a strength worth keeping."),
                ("A records server not updated in over a year", False,
                 "That is a weakness. An unpatched server is full of known holes."),
                ("Guest Wi-Fi on the same network as clinical systems", False,
                 "That is a weakness. Guests belong on a separate, isolated segment."),
                ("Remote access open to the internet with no MFA", False,
                 "That is a serious weakness. Remote access needs MFA and patching."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "What single idea ties firewalls, segmentation, VPNs and patching together?",
            "options": [
                ("Layer several defences, so a gap in one is covered by the others", True,
                 "Yes. No single control is perfect, so overlapping layers mean one weakness is not a disaster."),
                ("Rely only on the single best defence", False,
                 "No single control is enough. The strength is in layering them."),
                ("Leave everything to the firewall", False,
                 "A firewall is one layer. It cannot stop a phishing click, an unpatched hole, or spread on a flat network."),
                ("Assume you are too small to be targeted", False,
                 "Automated attacks do not care about size. Layered defences protect businesses of every size."),
            ],
        },
    ],
}
