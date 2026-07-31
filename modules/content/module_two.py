"""Module 2, Recognising Cyber Threats: the malware family, attacks on the whole
business, the real Australian breaches, and how to recognise and react.

Same shape and standard as Module 1 (see modules/content/module_one.py and
docs/module-authoring.md): a lesson is a scrollable room of collapsible task
PANELS. Each panel is a full, deep task: several teaching paragraphs (what it is,
a concrete Australian example, why it matters, what to do), a diagram where it
helps, a callout box with a specific scenario, sometimes a mid-panel check, then
the end interactive. Points sum to 10 per lesson and bank at lesson end.

Voice: warm, confident, human. Plain Australian English. No em-dashes, no filler,
no repetition, and nothing recycled from Module 1. The real cases (Optus and
Medibank, both 2022) are presented as widely-reported factual scenarios for
teaching, framed evenly and without blame.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "The malware family",
        "reading_time_minutes": 10,
        "intro": "Malware is not one thing, it is a family, and the members behave "
        "very differently. Meet the viruses, worms, trojans and spyware so you can "
        "tell them apart by how they move.",
        "tasks": [
            {
                "key": "what-malware",
                "kind": "check",
                "points": 2,
                "title": "What malware actually is",
                "diagram": "malware-family",
                "body": "<p>The word you will hear most often is virus, but it is "
                "usually the wrong word. The correct umbrella term is <strong>"
                "malware</strong>, short for malicious software, and it covers every "
                "kind of program written to do harm: viruses, worms, trojans, "
                "spyware and ransomware among them. A virus is just one member of "
                "that family, in the same way a labrador is one kind of dog.</p>"
                "<p>Getting the word right is more than pedantry. Each member of the "
                "family gets in differently, spreads differently and is stopped "
                "differently, so lumping them all together as viruses hides the very "
                "thing that helps you defend against them. The diagram above lays out "
                "the family you will meet in this lesson.</p>"
                "<p>Nearly all of it arrives the same handful of ways: an attachment "
                "you open, a program you download and run, a dodgy link, or an "
                "infected USB stick someone plugs in. Notice how many of those "
                "involve a person doing something. That is the good news you saw in "
                "Module 1 from another angle: a moment of care at the point of entry "
                "stops a great deal of malware before it ever runs.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "you do not need to recognise malware by name to stay safe, but "
                "knowing the family helps you understand a warning from your IT "
                "support, describe what you are seeing, and grasp why a particular "
                "precaution exists. A worm and a trojan are not stopped by the same "
                "habit.</div>",
                "question": "What does the word 'malware' mean?",
                "hint": "Look for the broad term. One option is an umbrella that covers the others.",
                "options": [
                    ("Malicious software: the umbrella term for viruses, worms, trojans, spyware and more", True,
                     "Exactly. Malware is the whole family of harmful software. A virus is just one member of it."),
                    ("Another word for a computer virus, and nothing else", False,
                     "Not quite. A virus is one kind of malware. Malware is the broader term that includes worms, trojans and others."),
                    ("Hardware that has broken down", False,
                     "No. Malware is software written to do harm, not faulty equipment."),
                    ("A setting you switch on to protect your computer", False,
                     "The opposite. Malware is the threat, not the protection."),
                ],
            },
            {
                "key": "virus-worm",
                "kind": "check",
                "points": 2,
                "title": "Viruses and worms: two ways to spread",
                "body": "<p>The two oldest kinds of malware are the virus and the "
                "worm, and most people use the words as if they mean the same thing. "
                "They do not, and the difference is genuinely useful, because it "
                "tells you how each one gets around, and therefore how you slow it "
                "down.</p>"
                "<p>A computer virus is a lot like its biological namesake: it cannot "
                "spread on its own. It needs a host and it needs you. A virus hides "
                "inside a file or a program and only wakes up when someone opens that "
                "file or runs that program. Share the infected file by email, a USB "
                "stick or a download, and the virus travels with it, but only as far "
                "as the next person who chooses to open it. That human action is the "
                "step it depends on.</p>"
                "<p>A worm is the one that keeps security teams up at night, because "
                "it needs no host and no help. A worm is a self-contained program "
                "that copies itself from one computer to the next across a network, "
                "by itself, as fast as the connection allows. One worm loose on an "
                "office network at nine in the morning can be on every machine by "
                "morning tea without a single person clicking anything.</p>"
                "<div class=\"cy-callout\"><strong>Two very different mornings in "
                "Ballarat.</strong> A small manufacturer emails a quote spreadsheet "
                "around the office; it carries a virus, and it only infects the "
                "people who actually open the attachment. A month later a worm slips "
                "onto the same network through an unpatched machine, and by lunchtime "
                "it has copied itself to every computer on the floor on its own. Same "
                "office, two speeds, and they call for two different defences.</div>",
                "inline_check": {
                    "question": "Which one can spread from computer to computer with nobody opening a file?",
                    "hint": "One needs a person to run it. The other moves by itself across the network.",
                    "options": [
                        ("The worm", True,
                         "Yes. A worm copies itself across the network on its own, which is exactly what makes it spread so fast."),
                        ("The virus", False,
                         "Not the virus. A virus only spreads when someone opens the infected file it is hiding in."),
                        ("The trojan", False,
                         "A trojan waits to be run too. The self-spreading one is the worm."),
                        ("None of them can spread by themselves", False,
                         "A worm can and does. Spreading by itself is its defining trait."),
                    ],
                },
                "body2": "<p>The difference is not trivia, it changes what protects "
                "you. A virus is held back by the plain habit of not opening files "
                "you were not expecting, because it cannot move until someone opens "
                "it. A worm laughs at that habit, because it never waited for anyone; "
                "what slows a worm is keeping software updated so it has no open door "
                "to crawl through, and separating the network so it cannot reach "
                "every machine at once. You will meet both of those defences properly "
                "in Module 5.</p>",
                "question": "A staff member opens an email attachment and their PC is infected, but nothing else on the network is touched until they forward the file to a colleague. Virus or worm?",
                "hint": "Did it spread on its own, or only when a person passed the file along?",
                "options": [
                    ("A virus", True,
                     "Right. It only moved when a person opened and then forwarded the file. That dependence on human action is the mark of a virus."),
                    ("A worm", False,
                     "A worm would have spread across the network by itself, with no forwarding needed. This one waited for a person, so it is a virus."),
                    ("A DDoS attack", False,
                     "A DDoS is a flood of traffic against a service, not an infected file. This is a virus."),
                    ("Spyware", False,
                     "Spyware secretly watches and steals. This one spread through an opened attachment, which points to a virus."),
                ],
            },
            {
                "key": "trojans",
                "kind": "check",
                "points": 2,
                "title": "Trojans: hidden in something you trust",
                "body": "<p>A trojan takes its name from the wooden horse of the old "
                "story: a gift wheeled through the gates that turned out to be full "
                "of soldiers. A trojan is malware wearing a disguise. It looks like "
                "something you actually want, a free program, a document, an update, "
                "a game, and you install or open it yourself. The disguise is the "
                "whole trick, because you invited it in.</p>"
                "<p>Unlike a virus or a worm, a trojan does not try to spread. Its job "
                "is to get onto one machine and open a door. Once it runs it might "
                "quietly install other malware, create a hidden way in for the "
                "attacker to come back later, steal your files, or sit and wait. The "
                "damage happens after you have already trusted it, which is what makes "
                "trojans so effective.</p>"
                "<p>The common giveaways are worth knowing. Software from an unofficial "
                "site or a search-engine advert rather than the maker's own page. A "
                "file that is not the type it claims, like an invoice that is actually "
                "a program. And the classic: a cracked or free copy of software that "
                "normally costs money, which is one of the most reliable ways to end "
                "up with a trojan.</p>"
                "<div class=\"cy-callout\"><strong>A Gold Coast cafe's new roster "
                "app.</strong> A manager searches for a free staff-rostering tool and "
                "downloads the first result, a program from a site they had never "
                "heard of. It even opens a little rostering window, so it seems "
                "genuine. In the background it has installed a trojan that quietly "
                "hands an attacker access to the till computer. The app worked, which "
                "is precisely why nobody suspected a thing.</div>",
                "question": "What is the defining feature of a trojan?",
                "hint": "Think about how it gets onto the machine. What does the victim believe they are doing?",
                "options": [
                    ("It disguises itself as something you want, so you install or open it yourself", True,
                     "Yes. The disguise is the trick. You let it in because it looks legitimate, then it does its real work."),
                    ("It spreads across the network on its own", False,
                     "That is a worm. A trojan does not spread itself, it waits to be run by someone who trusts it."),
                    ("It floods a website with traffic", False,
                     "That is a denial-of-service attack, not a trojan. A trojan is disguised software you run yourself."),
                    ("It can only infect phones, never computers", False,
                     "Trojans target computers and phones alike. The defining trait is the disguise, not the device."),
                ],
            },
            {
                "key": "spyware",
                "kind": "check",
                "points": 2,
                "title": "Spyware: quietly watching",
                "body": "<p>Not all malware announces itself. Ransomware wants you to "
                "know it is there, because it is demanding money. Spyware wants the "
                "exact opposite: it works best when you never notice it at all. "
                "Spyware is software that secretly watches what you do and reports it "
                "back to whoever planted it.</p>"
                "<p>The most common and dangerous kind is a keylogger, which records "
                "every key you press. Think about what that captures over a single "
                "day: the password to your email, the login for your banking, the "
                "code for the safe, a private message. Other spyware takes "
                "screenshots, switches on a webcam, or copies your files. All of it "
                "flows quietly to a stranger while everything on your screen looks "
                "perfectly normal.</p>"
                "<p>Because there is no dramatic lockout or ransom note, spyware can "
                "sit for weeks. The signs are subtle: a device that runs hotter or "
                "slower than usual, a battery that drains faster, or the strange "
                "experience of an account being accessed by someone who somehow knew "
                "the password. That last one is often the first real clue.</p>"
                "<div class=\"cy-callout\"><strong>A shared reception desk in "
                "Adelaide.</strong> A physiotherapy clinic uses one front-desk "
                "computer that every staff member logs into. A keylogger, carried in "
                "on a trojan months earlier, has been recording the booking-system "
                "password each time it is typed. Nobody noticed anything wrong, until "
                "patient records started being viewed from an account and at hours "
                "that made no sense.</div>",
                "question": "What does spyware such as a keylogger mainly do?",
                "hint": "The name is a clue. What is it trying to achieve, and how loudly?",
                "options": [
                    ("Secretly record what you do, such as the passwords you type, and send it to an attacker", True,
                     "Exactly. Spyware works by staying hidden and quietly stealing information like logins and messages."),
                    ("Lock your files and demand a payment to unlock them", False,
                     "That is ransomware, which wants to be noticed. Spyware does the opposite and stays hidden."),
                    ("Flood your internet connection so nothing loads", False,
                     "That describes a denial-of-service attack. Spyware is about quietly watching and stealing."),
                    ("Make your computer run faster", False,
                     "No. If anything spyware slows a device down as it works away in the background."),
                ],
            },
            {
                "key": "malware-sort",
                "kind": "sort",
                "points": 2,
                "title": "Match the behaviour to the malware",
                "body": "<p>You now know the four you will meet most often, and the "
                "quickest way to lock them in is to sort them by behaviour rather "
                "than by name. Remember the core of each one. A <strong>virus</strong> "
                "hides in a file and needs a person to open it. A <strong>worm</strong> "
                "copies itself across the network on its own. A <strong>trojan</strong> "
                "is a disguise you install yourself. <strong>Spyware</strong> hides "
                "and quietly steals what you do.</p>"
                "<p>Below are eight behaviours. Tap each one, then tap the member of "
                "the family it belongs to. Get all eight and you have the map.</p>",
                "payload": {
                    "prompt": "Tap a behaviour, then tap the malware it describes. All eight to finish.",
                    "buckets": [
                        {"id": "virus", "label": "Virus"},
                        {"id": "worm", "label": "Worm"},
                        {"id": "trojan", "label": "Trojan"},
                        {"id": "spyware", "label": "Spyware"},
                    ],
                    "items": [
                        {"id": "hides", "text": "Hides in a file and only runs when someone opens it",
                         "bucket": "virus", "why": "That dependence on a person opening the file is the mark of a virus."},
                        {"id": "usb", "text": "Rides along on a USB stick and infects whoever opens the file",
                         "bucket": "virus", "why": "It still needs a person to open the file, so it is a virus."},
                        {"id": "self", "text": "Copies itself from machine to machine across the network, unaided",
                         "bucket": "worm", "why": "Self-spreading with no human action is exactly what a worm does."},
                        {"id": "unpatched", "text": "Jumps to the next computer through an unpatched hole, on its own",
                         "bucket": "worm", "why": "Spreading itself through an open door in the software is a worm."},
                        {"id": "disguise", "text": "Arrives disguised as a free program you chose to install",
                         "bucket": "trojan", "why": "A disguise you install yourself is the defining trick of a trojan."},
                        {"id": "backdoor", "text": "Looks like a video player but opens a hidden door for an attacker",
                         "bucket": "trojan", "why": "Pretending to be something useful while doing harm is a trojan."},
                        {"id": "keys", "text": "Quietly records the passwords you type and sends them away",
                         "bucket": "spyware", "why": "Secretly capturing what you type is spyware, usually a keylogger."},
                        {"id": "watch", "text": "Watches your screen for weeks without ever showing itself",
                         "bucket": "spyware", "why": "Hidden, patient watching and stealing is spyware."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Ransomware, and attacks on the whole business",
        "reading_time_minutes": 10,
        "intro": "Some attacks target a single laptop. Others aim at the whole "
        "organisation. Meet ransomware and the traffic flood called a DDoS, and "
        "learn to tell which kind of trouble you are looking at.",
        "tasks": [
            {
                "key": "ransomware",
                "kind": "check",
                "points": 2,
                "title": "Ransomware: holding your files hostage",
                "body": "<p>Ransomware is the member of the malware family that has "
                "done the most damage to Australian organisations, and it works in a "
                "brutally simple way. Once it runs, it scrambles your files using "
                "encryption, turning documents, spreadsheets and photos into "
                "unreadable gibberish, then it puts a note on the screen demanding a "
                "payment, almost always in cryptocurrency, in exchange for the key to "
                "unscramble them.</p>"
                "<p>What makes it so effective is that it attacks availability, the "
                "third pillar from Module 1. Your files have not been taken anywhere. "
                "They are right there, on your own computer, and you simply cannot "
                "read them. For a business that runs on its bookings, records or "
                "accounts, an hour of that is painful and a week of it can be "
                "fatal.</p>"
                "<p>Ransomware usually arrives the ways you now recognise: a trojan in "
                "a download, an attachment opened in a hurry, or a worm-like spread "
                "through an unpatched network. That is worth holding onto, because it "
                "means the same everyday care that stops the rest of the family stops "
                "ransomware getting its first foothold.</p>"
                "<div class=\"cy-callout\"><strong>A regional real estate office, "
                "Monday morning.</strong> Every agent arrives to the same screen: a "
                "message saying their files are encrypted and a countdown demanding "
                "payment. The property photos, the contracts, the trust records, all "
                "there and all unreadable. The agency that recovers by Tuesday is the "
                "one with a tested backup. The one that does not is looking at weeks "
                "of rebuilding, if it can rebuild at all.</div>",
                "inline_check": {
                    "question": "Ransomware mainly attacks which of the three security pillars from Module 1?",
                    "hint": "Your files are not stolen or altered. What can you no longer do with them?",
                    "options": [
                        ("Availability, because you cannot get to your own files", True,
                         "Yes. The files are still there and unchanged, you just cannot reach them, which is an availability failure."),
                        ("Confidentiality, because the files are shown to strangers", False,
                         "Not the main point. Classic ransomware locks your files rather than publishing them. The core hit is to availability."),
                        ("Integrity, because the files are secretly altered", False,
                         "The files are scrambled wholesale, not quietly edited to mislead you. The pillar lost is availability."),
                        ("None, ransomware is not really a security problem", False,
                         "It is one of the most serious. Being locked out of everything you need to work is an availability failure."),
                    ],
                },
                "body2": "<p>This is why backups keep coming up. A recent backup that "
                "you have actually tested and can restore takes away the attacker's "
                "entire advantage. You wipe the infected machines, restore your files, "
                "and carry on, without sending a cent to a criminal. A backup nobody "
                "has ever tested, though, is only a hope, and the worst morning to "
                "discover it stopped running months ago is this one.</p>",
                "question": "Why is a tested backup the single best defence against ransomware?",
                "hint": "Ransomware's power is that it holds your only copy. What removes that power?",
                "options": [
                    ("You can restore your files and keep working, instead of paying the attacker", True,
                     "Exactly. If you have a clean copy to restore, the threat to lock you out loses its force."),
                    ("It stops the ransomware from ever arriving", False,
                     "A backup does not block the infection, but it means the infection cannot hold your only copy hostage."),
                    ("It makes the encrypted files readable again automatically", False,
                     "It does not unscramble the locked files. It lets you restore clean copies from before the attack."),
                    ("It hides your files so ransomware cannot find them", False,
                     "It does not hide anything. Its value is giving you a clean copy to come back to."),
                ],
            },
            {
                "key": "should-you-pay",
                "kind": "check",
                "points": 2,
                "title": "Should you ever pay?",
                "body": "<p>When ransomware hits and there is no good backup, the "
                "demand is designed to feel like the only way out. It usually is not, "
                "and paying carries risks that are easy to miss in a panic.</p>"
                "<p>First, paying is no guarantee. You are dealing with criminals, and "
                "plenty of victims who paid received a key that only half worked, or "
                "nothing at all. Second, the money funds the next attack and marks "
                "you as a business that pays, which quietly moves you up the list for "
                "a second visit. Third, in some cases paying can carry legal "
                "complications of its own. Australian authorities, including the "
                "Australian Cyber Security Centre, advise against paying for exactly "
                "these reasons.</p>"
                "<p>The right move is to treat the decision as one you make with help, "
                "not alone at the keyboard at 8am. Disconnect the affected machines "
                "from the network to stop the spread, report it, and get proper "
                "advice. The businesses that come through ransomware best are almost "
                "always the ones that prepared before it happened, with backups and a "
                "plan, which is the whole subject of Module 6.</p>"
                "<div class=\"cy-callout\"><strong>The quiet second visit.</strong> A "
                "logistics firm paid a ransom to get its files back and breathed a "
                "sigh of relief. Four months later it was hit again by the same group, "
                "who already knew the firm would pay. Paying had not closed the door "
                "the attackers came through; it had simply told them the door was "
                "worth using twice.</div>",
                "question": "Why do authorities generally advise against paying a ransom?",
                "hint": "Think beyond getting your files back. What does paying encourage, and does it even guarantee recovery?",
                "options": [
                    ("It does not guarantee recovery, it funds more crime, and it marks you as a business that pays", True,
                     "Right. Payment is unreliable, it bankrolls the next attack, and it can invite a second hit on you specifically."),
                    ("Paying is illegal in every case in Australia", False,
                     "It is not a blanket crime, though it can carry legal complications. The main reasons are that it is unreliable and it funds more attacks."),
                    ("Paying always makes the attackers delete their copy of your data", False,
                     "There is no such guarantee. You are trusting criminals to keep their word, which they often do not."),
                    ("It is cheaper to pay than to keep backups", False,
                     "Backups are far cheaper than a ransom and, unlike a payment, they actually work. Preparing beats paying."),
                ],
            },
            {
                "key": "ddos",
                "kind": "check",
                "points": 3,
                "title": "DDoS: drowning a service in traffic",
                "diagram": "ddos",
                "body": "<p>Not every attack tries to get inside your computer. Some "
                "aim to knock a service offline from the outside, and the most common "
                "of these is the DDoS, which stands for Distributed Denial of "
                "Service. The idea is as simple as its name is clunky: overwhelm a "
                "website or online service with so much traffic that it can no longer "
                "answer the real customers trying to reach it.</p>"
                "<p>The 'distributed' part is what makes it hard to stop. The flood "
                "does not come from one place you could simply block. It comes from "
                "thousands or even millions of computers at once, often ordinary "
                "devices around the world that have themselves been infected and "
                "quietly conscripted into what is called a botnet. To your server it "
                "looks like an impossible crowd all knocking at the door in the same "
                "second.</p>"
                "<p>Crucially, a DDoS does not steal or change anything. Nothing gets "
                "into your files. It is a pure attack on availability: your website is "
                "up, your data is safe, and yet no customer can get through. For a "
                "business that sells or books online, being unreachable during your "
                "busiest hour is the entire harm, and it is real.</p>"
                "<div class=\"cy-callout\"><strong>A ticketing site on release "
                "day.</strong> A Melbourne venue puts a popular show on sale at 9am. "
                "At 8:59 a DDoS begins, and the flood of junk traffic buries the site "
                "so genuine fans see nothing but timeouts and spinning wheels. No "
                "records are stolen and no files are touched, but the on-sale is "
                "ruined and the refunds and reputation damage are very real. "
                "Defending against this usually means a specialist service that "
                "filters the flood upstream, which is a conversation to have before "
                "the day, not during it.</div>",
                "question": "What does a DDoS attack actually do?",
                "hint": "Nothing is stolen or changed. What happens to the real customers?",
                "options": [
                    ("Floods a service with so much traffic that real users can no longer reach it", True,
                     "Yes. It is an attack on availability. The site stays intact but is buried under junk traffic so genuine users cannot get through."),
                    ("Steals the customer database from the website", False,
                     "That would be a data breach. A DDoS does not take anything, it just overwhelms the service so nobody can use it."),
                    ("Encrypts the files on the server and demands a ransom", False,
                     "That is ransomware. A DDoS does not touch your files, it drowns the service in traffic from the outside."),
                    ("Secretly records what visitors type on the site", False,
                     "That would be spyware or a compromised page. A DDoS is purely about flooding the service to knock it offline."),
                ],
            },
            {
                "key": "device-vs-service",
                "kind": "check",
                "points": 1,
                "title": "A device problem, or a business problem?",
                "body": "<p>Here is a simple way to hold the whole lesson together. "
                "Some attacks land on a single device: a virus on one laptop, spyware "
                "on the reception PC, a trojan someone installed. Others go after the "
                "whole organisation at once: ransomware sweeping every shared file, or "
                "a DDoS knocking your public service offline.</p>"
                "<p>The reason it helps to notice the scale is that it points to who "
                "needs to act. A single infected laptop can often be taken off the "
                "network and cleaned. An attack on the whole business, where shared "
                "drives are locked or the website is down for everyone, is an "
                "all-hands situation that needs reporting and coordination straight "
                "away. Recognising the difference is the first move toward the right "
                "response.</p>",
                "question": "Which of these is an attack on the whole business rather than one device?",
                "hint": "Which one affects everyone at once, not just a single machine?",
                "options": [
                    ("Ransomware locking every file on the shared drive", True,
                     "Yes. When shared files are locked for everyone, the whole business is hit and it needs an immediate, coordinated response."),
                    ("A keylogger on one reception computer", False,
                     "That is serious, but it sits on a single device that can be taken off the network and cleaned."),
                    ("A virus in an attachment one person opened", False,
                     "That starts on one machine. It can spread if forwarded, but on its own it is a single-device problem."),
                    ("A trojan someone installed on their own laptop", False,
                     "That affects the one laptop it was installed on, not the whole organisation at once."),
                ],
            },
            {
                "key": "biz-classify",
                "kind": "classify",
                "points": 2,
                "title": "Which kind of trouble is this?",
                "body": "<p>Time to put names to real situations. Below are a handful "
                "of things that might land on your desk on any given day. Some are "
                "attacks and some are perfectly normal, because a big part of "
                "recognising threats is not crying wolf at every hiccup.</p>"
                "<p>Read each one and choose what it is. You are looking for the "
                "signature: locked files and a demand mean ransomware, a flood of "
                "traffic burying a service means a DDoS, an unfamiliar harmful program "
                "means malware, and a calm expected event is simply legitimate.</p>",
                "payload": {
                    "prompt": "Read each alert and choose what it is. Get them all to finish.",
                    "categories": [
                        {"id": "legit", "label": "Legitimate"},
                        {"id": "ransomware", "label": "Ransomware"},
                        {"id": "ddos", "label": "DDoS"},
                        {"id": "malware", "label": "Malware"},
                    ],
                    "events": [
                        {"id": "locked", "category": "ransomware",
                         "text": "Every file on the shared drive now ends in .locked, and a note on the screen demands payment in cryptocurrency within 48 hours.",
                         "why": "Files encrypted plus a payment demand is the unmistakable signature of ransomware."},
                        {"id": "flood", "category": "ddos",
                         "text": "The online booking site is timing out for everyone, and the traffic logs show a sudden flood from thousands of addresses at once.",
                         "why": "A sudden flood of traffic burying a service so nobody can reach it is a DDoS attack."},
                        {"id": "newsletter", "category": "legit",
                         "text": "The monthly newsletter went out on schedule at 10am and a few customers have replied to say thanks.",
                         "why": "Expected, routine, and harmless. Calling this an attack would be a false alarm."},
                        {"id": "antivirus", "category": "malware",
                         "text": "The antivirus has quarantined a program that arrived in a downloaded 'invoice', flagging it as a trojan.",
                         "why": "A harmful program caught in a download is malware, in this case a trojan the antivirus stopped."},
                        {"id": "update", "category": "legit",
                         "text": "IT emailed last week that Saturday's system update might make things briefly unavailable, and on Saturday it is.",
                         "why": "This was announced in advance and is planned maintenance. It is legitimate, not an attack."},
                        {"id": "keys", "category": "malware",
                         "text": "A staff member's saved passwords are being used from a strange location, and their laptop has been running hot for weeks.",
                         "why": "Quietly stolen credentials plus a hot, slow machine points to spyware, which is a type of malware."},
                    ],
                },
            },
        ],
    },
    {
        "title": "The big breaches: Optus and Medibank",
        "reading_time_minutes": 10,
        "intro": "In 2022 two of the largest data breaches in Australian history put "
        "the personal details of millions of people at risk. Understand what a "
        "breach really is, what happened, and why it matters to you.",
        "tasks": [
            {
                "key": "what-breach",
                "kind": "check",
                "points": 2,
                "title": "What a data breach actually is",
                "diagram": "data-breach",
                "body": "<p>A data breach is different from everything else in this "
                "module so far. Malware attacks your device and a DDoS attacks your "
                "service, but a breach is about your information ending up in the "
                "wrong hands: personal details, customer records, logins, taken from "
                "where they were stored or exposed to people who should never have "
                "seen them.</p>"
                "<p>Notice that a breach is chiefly a failure of confidentiality, the "
                "first pillar from Module 1. The information itself may be perfectly "
                "intact and the systems may keep running normally. The harm is simply "
                "that private data is now somewhere it should not be, and once it is "
                "out, it cannot be called back.</p>"
                "<p>Breaches happen in a few common ways. An attacker steals a login "
                "and walks in as if they were staff. A system is left exposed to the "
                "internet without a password. A laptop or a database is lost or "
                "misconfigured. Or, as you saw in Module 1, someone simply emails a "
                "file to the wrong person. The two cases you are about to look at were "
                "not small mistakes; they were among the largest breaches this country "
                "has seen.</p>"
                "<div class=\"cy-callout\"><strong>Why it lands on you.</strong> When "
                "a company you have never worked for is breached, your details can "
                "still be in it, because you were a customer. That is what makes "
                "breaches feel so unfair: the mistake is made by an organisation, and "
                "the risk is carried by the ordinary people whose information they "
                "held.</div>",
                "question": "A data breach is mainly a failure of which security pillar?",
                "hint": "Nothing is necessarily locked or altered. What has gone wrong is about who can see the information.",
                "options": [
                    ("Confidentiality, because private information reaches people who should not have it", True,
                     "Yes. A breach is information ending up in the wrong hands, which is a confidentiality failure."),
                    ("Availability, because you cannot reach your files", False,
                     "That describes ransomware or a DDoS. In a breach the systems often keep working; the problem is who can see the data."),
                    ("Integrity, because the data is secretly changed", False,
                     "A breach is usually about data being taken or exposed, not quietly altered. The pillar lost is confidentiality."),
                    ("None, a breach is not a security issue", False,
                     "A breach is one of the most serious security failures, precisely because exposed data cannot be recalled."),
                ],
            },
            {
                "key": "optus",
                "kind": "check",
                "points": 3,
                "title": "Optus, 2022: millions of records exposed",
                "body": "<p>In September 2022, the telecommunications company Optus "
                "disclosed a data breach that affected a very large number of current "
                "and former customers, reported to be in the order of 9.8 million "
                "people. For a country of about 26 million, that is a striking share "
                "of the population caught in a single incident.</p>"
                "<p>The information exposed was the kind that matters. It included "
                "names, dates of birth, phone numbers and email addresses, and for a "
                "portion of those affected it reached further, into identity document "
                "numbers such as passport, driver licence and Medicare numbers. That "
                "combination is exactly what someone needs to attempt identity theft "
                "in another person's name.</p>"
                "<p>What made the breach so widely discussed was how it reportedly "
                "happened. According to public reporting, an access point to customer "
                "data was reachable over the internet without requiring a login. There "
                "was, in effect, a door that should have been locked and was not. No "
                "clever malware, no elaborate trick, just a way in that was left open, "
                "which is a sobering reminder that a great deal of security is simply "
                "not leaving doors unlocked.</p>"
                "<div class=\"cy-callout\"><strong>The follow-on wave.</strong> Within "
                "days, Australians whose details were exposed began receiving scam "
                "texts and emails that used their real names and referenced the "
                "breach, trying to trick them into handing over even more. A breach is "
                "rarely the end of the story; it is often the raw material for the "
                "phishing that comes next, which is the very last panel of this "
                "lesson.</div>",
                "inline_check": {
                    "question": "Why was the type of data in the Optus breach especially serious?",
                    "hint": "Think about what you can do with someone's name, birth date and identity document numbers together.",
                    "options": [
                        ("It included identity details like document numbers, which can be used to attempt identity theft", True,
                         "Yes. Names, dates of birth and identity document numbers together are the ingredients for impersonating someone."),
                        ("It was only email addresses, which are harmless", False,
                         "It went well beyond email addresses, reaching identity document numbers for some, which is far more serious."),
                        ("The files were encrypted so no one could read them", False,
                         "This was a breach, not ransomware. The data was exposed and readable, which is the whole problem."),
                        ("Nothing serious was exposed", False,
                         "A great deal was exposed, including identity document numbers for a portion of those affected."),
                    ],
                },
                "body2": "<p>There is a lesson here that applies to every organisation, "
                "not just a telco. Optus was not undone by a genius hacker; it was "
                "undone, on the public account, by a gap in the basics. The same "
                "principle scales all the way down to a small business: keep the doors "
                "that face the internet locked, collect only the personal data you "
                "genuinely need, and do not keep it a day longer than you must. Data "
                "you never collected cannot be breached.</p>",
                "question": "What was the widely reported cause of the Optus breach?",
                "hint": "It was not sophisticated malware. It was closer to a door being left unlocked.",
                "options": [
                    ("An access point to customer data was reachable over the internet without a login", True,
                     "Yes. On public reporting, a way in that should have required a login did not, which is why the basics matter so much."),
                    ("Every employee's password was guessed one by one", False,
                     "That is not what was reported. The issue was an exposed access point that needed no login at all."),
                    ("A staff member paid a ransom to attackers", False,
                     "That confuses it with ransomware. The Optus incident was a data breach through an exposed access point."),
                    ("Customers gave their details to a phishing email", False,
                     "The breach was on the company's side, an exposed system, not customers being individually phished."),
                ],
            },
            {
                "key": "medibank",
                "kind": "check",
                "points": 2,
                "title": "Medibank, 2022: when health data leaks",
                "body": "<p>Weeks after Optus, in October 2022, the health insurer "
                "Medibank disclosed a breach of its own, affecting around 9.7 million "
                "current and former customers. If Optus showed how exposed identity "
                "data can be, Medibank showed something even more sensitive: health "
                "information.</p>"
                "<p>The data taken included names, dates of birth, Medicare numbers "
                "and, most sensitively, health claims details, the record of medical "
                "services people had received. This is about as private as personal "
                "information gets, and its exposure can cause real distress quite apart "
                "from any financial fraud. On public reporting, the attackers got in "
                "using a stolen login credential, a legitimate username and password "
                "that had fallen into the wrong hands, which let them walk in looking "
                "like a genuine user.</p>"
                "<p>Medibank decided not to pay the ransom the attackers demanded. In "
                "response, the attackers published the stolen data. It was a stark, "
                "public illustration of the point from the last lesson: paying is a "
                "gamble that funds crime and guarantees nothing, and even not paying "
                "carries a terrible cost when the data is this sensitive. There are no "
                "good options once the data is already out, which is exactly why "
                "prevention matters so much more than response.</p>"
                "<div class=\"cy-callout\"><strong>The credential is the key.</strong> "
                "The Medibank attackers did not smash a window; they used a key. A "
                "single stolen login opened the door, which is the strongest possible "
                "argument for the habits in Module 4: unique passwords so one leak "
                "does not travel, and two-factor authentication so a stolen password "
                "on its own is not enough to get in.</div>",
                "question": "On public reporting, how did the attackers get into Medibank's systems?",
                "hint": "They did not break in by force. They used something that let them look like a real user.",
                "options": [
                    ("With a stolen login credential, which let them appear to be a genuine user", True,
                     "Yes. A stolen username and password opened the door, which is why unique passwords and two-factor matter so much."),
                    ("By flooding the website with traffic until it broke", False,
                     "That describes a DDoS. Medibank was a data breach, reportedly through a stolen login."),
                    ("By leaving a database exposed to the internet with no password", False,
                     "That was closer to the Optus account. Medibank was reported to involve a stolen credential."),
                    ("By posting a USB stick to the office", False,
                     "That is not what was reported. The reported entry point was a stolen login credential."),
                ],
            },
            {
                "key": "what-it-means-for-you",
                "kind": "check",
                "points": 1,
                "title": "What a leaked record means for you",
                "body": "<p>It is easy to read a breach as a story about big companies "
                "and shrug. The reason to care is that the fallout lands on ordinary "
                "people. When your details are exposed, the practical risk is that "
                "someone tries to use them: to open an account in your name, to pass a "
                "security check by knowing your date of birth, or to make a scam "
                "message far more convincing because it quotes real information about "
                "you.</p>"
                "<p>The sensible response is calm and specific. If you are told your "
                "data was in a breach, change the password on that account and anywhere "
                "you reused it, turn on two-factor authentication, and be extra wary of "
                "messages that arrive knowing your details, because those are the "
                "follow-on scams. If identity documents were exposed, the organisation "
                "and government services can advise on replacing them. You are not "
                "powerless; you just need to act on the right things.</p>",
                "question": "You are told your details were exposed in a company's data breach. What is a sensible first step?",
                "hint": "You cannot un-leak the data. What can you still control about the accounts involved?",
                "options": [
                    ("Change the password on that account and anywhere you reused it, and turn on two-factor", True,
                     "Yes. You cannot recall leaked data, but you can lock down the accounts so the exposed details are harder to misuse."),
                    ("Nothing can be done, so there is no point acting", False,
                     "There is plenty you can do. Changing passwords and enabling two-factor genuinely reduces the risk."),
                    ("Immediately pay any fee a follow-up message asks for", False,
                     "The opposite. Messages that arrive after a breach quoting your details are usually the follow-on scam."),
                    ("Delete your email account entirely", False,
                     "That is drastic and unnecessary, and it can lock you out of other services. Securing the accounts is the measured step."),
                ],
            },
            {
                "key": "post-breach-inbox",
                "kind": "inbox",
                "points": 2,
                "title": "The scams that follow a breach",
                "body": "<p>A breach is rarely the end. The stolen details become fuel "
                "for a second round of attacks, because a scammer who knows your real "
                "name, your provider and a snippet of true information can craft a "
                "message that is far harder to doubt. After both 2022 breaches, exactly "
                "this happened at scale.</p>"
                "<p>The reassuring part is that these follow-on messages still give "
                "themselves away in the same places you learned to check in Module 1. "
                "Real details in the greeting do not make the sender, the link or the "
                "urgency any more genuine. Here is one of these post-breach emails. "
                "Tap every part that should make you pause.</p>",
                "payload": {
                    "prompt": "This landed days after a breach was in the news. Tap every part that looks off. Find them all to finish.",
                    "avatar": "MB",
                    "parts": [
                        {"id": "from", "zone": "From",
                         "text": "Medibank Security <alerts@medibank-secure-verify.com>",
                         "bad": True,
                         "why": "A lookalike domain. The real insurer would not use medibank-secure-verify.com, a name built to borrow trust."},
                        {"id": "greeting", "zone": "Body",
                         "text": "Dear Sarah Nguyen, we hold your policy 4471 on record.",
                         "bad": False,
                         "why": "Unsettling, but a real name or number from a breach does not make the sender genuine. It is bait, not proof."},
                        {"id": "subject", "zone": "Subject",
                         "text": "Your account is at risk, verify within 2 hours to avoid suspension",
                         "bad": True,
                         "why": "Manufactured urgency and a threat of suspension, designed to rush you past your own judgement."},
                        {"id": "link", "zone": "Body",
                         "text": "Confirm your identity now at medibank-secure-verify.com/confirm",
                         "bad": True,
                         "why": "An unexpected link to the lookalike site, ready to capture whatever you type. Never click it; go to the real site yourself."},
                        {"id": "ask", "zone": "Body",
                         "text": "Re-enter your Medicare number and banking details to confirm it is you.",
                         "bad": True,
                         "why": "A genuine organisation does not ask you to re-enter identity and banking details through an emailed link."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Recognising and reacting",
        "reading_time_minutes": 9,
        "intro": "Pull it all together: the warning signs anyone can spot, how to "
        "tell a real attack from an ordinary glitch, and the calm first moves when "
        "you realise something is wrong.",
        "tasks": [
            {
                "key": "warning-signs",
                "kind": "check",
                "points": 2,
                "title": "The warning signs anyone can spot",
                "body": "<p>You do not need to be technical to be the person who "
                "notices something is wrong, and often the non-technical person at the "
                "front desk spots it first. Most threats leave the same everyday "
                "traces, and knowing them turns a vague unease into a clear signal "
                "worth reporting.</p>"
                "<p>Watch for a device that suddenly runs hot, slow or noisy for no "
                "reason, which can mean something is working away in the background. "
                "Watch for pop-ups, new toolbars or programs you did not install. "
                "Watch for files that will not open or have odd new names, the "
                "hallmark of ransomware. And watch for the social signs: colleagues "
                "saying they got a strange email 'from you', or a login alert for an "
                "account you did not sign into. That last pair often reveals a "
                "compromise before anything on your own screen looks wrong.</p>"
                "<p>None of these on its own is proof, and that is fine. The skill is "
                "not certainty, it is noticing the change and saying something. A "
                "threat spotted early, while it is still one hot laptop or one strange "
                "email, is a threat handled cheaply.</p>"
                "<div class=\"cy-callout\"><strong>The tell that came from outside.</strong> "
                "An accountant in Wagga first learned her email was compromised not "
                "from her own computer, which seemed perfectly normal, but from three "
                "clients in one afternoon asking why she had sent them a link to a "
                "strange login page. The people around you are part of your alarm "
                "system.</div>",
                "question": "Which of these is a classic warning sign worth reporting?",
                "hint": "Look for the change that suggests something is happening you did not start.",
                "options": [
                    ("Colleagues say they received a strange email from your address that you never sent", True,
                     "Yes. That strongly suggests your account or device is compromised, and it is worth reporting straight away."),
                    ("Your computer works exactly as it always has", False,
                     "That is reassuring, not a warning sign. The signs to watch are unexpected changes."),
                    ("You received an email you were expecting from a known colleague", False,
                     "That is normal, expected activity, not a warning sign."),
                    ("A website loaded a little slowly once, then was fine", False,
                     "A single slow load is usually nothing. The real signals are persistent or unexplained changes, like spam sent in your name."),
                ],
            },
            {
                "key": "attack-or-glitch",
                "kind": "check",
                "points": 2,
                "title": "Is it an attack, or just a glitch?",
                "body": "<p>Recognising threats has a flip side that matters just as "
                "much: not everything that goes wrong is an attack. Computers are "
                "imperfect. Programs crash, updates cause hiccups, hard drives fill "
                "up, and the internet has slow days. If you treat every glitch as a "
                "breach you will exhaust yourself and, worse, you will cry wolf so "
                "often that nobody listens when it is real.</p>"
                "<p>A rough guide helps. Ordinary glitches tend to be isolated, "
                "explainable and one-off: one program crashes and reopens fine, the "
                "wifi is slow during a storm, a document will not print. Attacks tend "
                "to be patterned, unexplained and spreading: many files renamed at "
                "once, a demand for money, several colleagues affected, an account "
                "logged into from another country. When in doubt the answer is not to "
                "panic and not to ignore it, but to ask, because a two-minute check "
                "with your IT support settles it.</p>"
                "<div class=\"cy-callout\"><strong>A slow laptop with a simple "
                "cause.</strong> A council worker was convinced her sluggish laptop "
                "had a virus. It turned out the hard drive was 99 percent full, a "
                "completely ordinary problem with a completely ordinary fix. Staying "
                "calm and asking, rather than assuming the worst, saved a lot of "
                "worry. The habit is the same either way: notice, then check.</div>",
                "inline_check": {
                    "question": "Which pattern points to an attack rather than an ordinary glitch?",
                    "hint": "Attacks tend to be patterned and spreading. Glitches tend to be isolated and explainable.",
                    "options": [
                        ("Many files renamed at once with a demand for payment on the screen", True,
                         "Yes. A coordinated change across many files plus a ransom demand is a clear attack, not a random hiccup."),
                        ("One program crashed once and reopened normally", False,
                         "That is a classic ordinary glitch. A single crash that recovers is rarely an attack."),
                        ("The wifi was slow during a thunderstorm", False,
                         "That has a plain, everyday explanation. It is a glitch, not a sign of an attack."),
                        ("A document would not print until you restarted the printer", False,
                         "That is routine equipment trouble, not a security incident."),
                    ],
                },
                "body2": "<p>The point is not to become an expert diagnostician. It is "
                "to hold two ideas at once: take genuine warning signs seriously, and "
                "do not spiral over every ordinary fault. That balance, calm attention "
                "rather than alarm or denial, is exactly what a good first responder "
                "brings, and it is a skill anyone can practise.</p>",
                "question": "Your one program crashes, then reopens and works fine for the rest of the day. Most likely?",
                "hint": "Is this isolated and recovered, or patterned and spreading?",
                "options": [
                    ("An ordinary glitch, not an attack", True,
                     "Right. A single crash that recovers cleanly is everyday computer behaviour, not a sign of an attack."),
                    ("Definitely ransomware", False,
                     "Ransomware locks your files and demands payment. One program crashing and recovering does not fit that at all."),
                    ("Definitely a DDoS attack", False,
                     "A DDoS floods an online service with traffic. A single local program crash is unrelated."),
                    ("Definitely spyware", False,
                     "Possible in theory, but a lone crash that recovers is far more likely an ordinary glitch. Watch for a pattern before assuming the worst."),
                ],
            },
            {
                "key": "triage-classify",
                "kind": "classify",
                "points": 3,
                "title": "Classify the alert",
                "body": "<p>This is the recognising-threats skill in its purest form. "
                "A real morning brings a mix of the alarming and the harmless, and "
                "your job is to sort them calmly and correctly, so the genuine threats "
                "get raised and the false alarms do not drown them out.</p>"
                "<p>Below are six situations. For each one, decide whether it is "
                "legitimate or which kind of attack it is. Lean on the signatures you "
                "have built up across this module: locked files and a demand mean "
                "ransomware, a traffic flood means a DDoS, exposed personal records "
                "mean a data breach, and a calm expected event is simply legitimate.</p>",
                "payload": {
                    "prompt": "Read each alert and choose what it is. Get all six to finish.",
                    "categories": [
                        {"id": "legit", "label": "Legitimate"},
                        {"id": "ransomware", "label": "Ransomware"},
                        {"id": "ddos", "label": "DDoS"},
                        {"id": "breach", "label": "Data breach"},
                    ],
                    "events": [
                        {"id": "notice", "category": "breach",
                         "text": "A company you have an account with writes to say your name, email and date of birth were exposed in a security incident.",
                         "why": "Personal records exposed to the wrong hands is a data breach."},
                        {"id": "locked", "category": "ransomware",
                         "text": "Staff arrive to find the shared drive full of files ending in .crypt and a note demanding payment for the key.",
                         "why": "Encrypted files plus a payment demand is ransomware."},
                        {"id": "flood", "category": "ddos",
                         "text": "Your public website is unreachable for everyone, and your host reports an enormous surge of traffic from all over the world.",
                         "why": "A worldwide traffic surge burying your site so nobody can reach it is a DDoS."},
                        {"id": "backup", "category": "legit",
                         "text": "At 2am the scheduled backup ran, emailed a success report, and finished on time as it does every night.",
                         "why": "A routine, successful, scheduled backup is entirely legitimate."},
                        {"id": "darkweb", "category": "breach",
                         "text": "A journalist contacts you: a file of your customers' names and addresses is being offered for sale on a criminal forum.",
                         "why": "Customer records taken and offered for sale is a data breach."},
                        {"id": "maintenance", "category": "legit",
                         "text": "The booking system is briefly down during the Sunday maintenance window your provider told you about last week.",
                         "why": "Announced, scheduled maintenance is legitimate, not an attack."},
                    ],
                },
            },
            {
                "key": "react-branch",
                "kind": "branch",
                "points": 3,
                "title": "You spot something. Now what?",
                "body": "<p>Recognising a threat is only worth something if you know "
                "the first few calm moves that follow. You do not need the full "
                "incident plan yet, that is all of Module 6, but you do need the "
                "instinct that turns a bad moment into a contained one.</p>"
                "<p>Walk through a real situation below. There are no trick questions, "
                "and if a choice goes wrong you will see why and get another go. The "
                "thread running through it is simple: stop the spread, do not hide it, "
                "and get the right people involved quickly.</p>",
                "payload": {
                    "prompt": "Choose what you would really do. You can always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "You open an attachment and a window flashes up, then vanishes. Moments later "
                            "a few files on your screen start renaming themselves to end in .locked. What do you do first?",
                            "choices": [
                                {"label": "Disconnect the computer from the network, by wifi or cable", "to": "n2",
                                 "outcome": "good",
                                 "feedback": "Exactly. Taking it off the network first is the single best way to stop ransomware spreading to shared drives and other machines."},
                                {"label": "Keep working and hope it stops on its own", "to": "n1bad",
                                 "outcome": "bad",
                                 "feedback": "Carrying on gives it time to encrypt more, and to reach the shared drive and your colleagues. Disconnecting first would have contained it."},
                            ],
                        },
                        "n1bad": {
                            "text": "Minutes later the shared drive is affected too, and a colleague's files begin locking.",
                            "choices": [{"label": "See the better first move", "to": "n2"}],
                        },
                        "n2": {
                            "text": "The machine is now off the network. What next?",
                            "choices": [
                                {"label": "Report it to whoever looks after IT straight away", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Right. Fast reporting gets the right people acting while the damage is still small, and there is never trouble for raising it early."},
                                {"label": "Try to delete the ransom note and clean it up quietly yourself", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "Cleaning up alone can destroy evidence and miss machines that are also affected. This needs to be reported, not hidden."},
                            ],
                        },
                        "n2bad": {
                            "text": "Working alone, you miss that a second computer was also reached, and it keeps spreading quietly.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "IT asks whether the business has recent backups. You know the nightly backup ran and was tested last month. "
                            "The attacker's note demands payment. What do you advise?",
                            "choices": [
                                {"label": "Restore from the tested backup rather than pay", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes. With a clean, tested backup you can recover without funding criminals or gambling on a key that may not work."},
                                {"label": "Pay the ransom quickly to be safe", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "Paying is unreliable, funds more crime and marks you as a payer. With a good backup there is no need to even consider it."},
                            ],
                        },
                        "n3bad": {
                            "text": "You reconsider: there is a tested backup sitting right there, and paying would risk everything for nothing.",
                            "choices": [{"label": "Take the better path", "to": "end"}],
                        },
                        "end": {
                            "text": "That is a threat recognised and contained: disconnect to stop the spread, report it fast, and "
                            "recover from a tested backup instead of paying. You handled the first hour well. Module 6 turns these "
                            "instincts into a full plan.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz. A bank of 40 (draw 10 at random), ten per lesson. Four options each,
# exactly one correct, and every option carries an explanation that teaches. This
# is the fuel for the Adaptive Feedback Engine. Same house voice: warm, plain, no
# em-dashes.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        # ---- Lesson 1: the malware family ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does the term 'malware' mean?",
            "options": [
                ("Malicious software: the umbrella term for viruses, worms, trojans, spyware and more", True,
                 "Yes. Malware is the whole family of harmful software, and a virus is only one member of it."),
                ("A specific brand of antivirus", False,
                 "No. Malware is the threat, not the protection against it."),
                ("Faulty hardware", False,
                 "No. Malware is harmful software, not broken equipment."),
                ("A strong password", False,
                 "No. That is a defence. Malware is the harmful software it helps protect against."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "What is the key difference between a virus and a worm?",
            "options": [
                ("A virus needs a person to open the infected file; a worm spreads across the network by itself", True,
                 "Exactly. That is why a worm can move so fast, and why the two are stopped by different defences."),
                ("A virus spreads by itself; a worm needs a person to run it", False,
                 "That is backwards. The worm is the self-spreading one; the virus needs a person to open the file."),
                ("They are two words for exactly the same thing", False,
                 "No. The difference in how they spread is real and useful for defending against each."),
                ("A virus only affects phones and a worm only affects computers", False,
                 "No. Both can affect computers. The real difference is whether it spreads on its own."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A worm is especially dangerous on a network because it:",
            "options": [
                ("Copies itself from machine to machine on its own, with no human action", True,
                 "Yes. Needing no help means it can reach every machine on a network very quickly."),
                ("Can only spread if each person opens an attachment", False,
                 "That describes a virus. A worm does not wait for anyone."),
                ("Encrypts files and demands a ransom", False,
                 "That is ransomware. A worm's defining trait is self-spreading."),
                ("Disguises itself as a program you want", False,
                 "That is a trojan. A worm spreads itself rather than relying on a disguise."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is the defining feature of a trojan?",
            "options": [
                ("It disguises itself as something you want, so you install or run it yourself", True,
                 "Yes. You let it in because it looks legitimate, and then it does its real work."),
                ("It spreads across the network without any help", False,
                 "That is a worm. A trojan relies on you choosing to run it."),
                ("It floods a website with traffic", False,
                 "That is a DDoS. A trojan is disguised software you run yourself."),
                ("It is completely harmless", False,
                 "No. A trojan is harmful; the disguise is exactly what makes it dangerous."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Downloading cracked or free copies of paid software is risky mainly because:",
            "options": [
                ("It is one of the most common ways to end up with a trojan", True,
                 "Yes. Those downloads are a favourite hiding place for disguised malware."),
                ("It uses too much internet data", False,
                 "Data use is not the real risk. The danger is the malware often hidden inside."),
                ("It makes your screen brighter", False,
                 "That is unrelated. The real risk is a hidden trojan."),
                ("It is always completely safe", False,
                 "The opposite. Unofficial software downloads are a classic source of trojans."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What does spyware such as a keylogger do?",
            "options": [
                ("Secretly records what you do, like the passwords you type, and sends it to an attacker", True,
                 "Yes. Spyware works by staying hidden and quietly stealing information."),
                ("Locks your files and demands payment", False,
                 "That is ransomware, which wants to be noticed. Spyware stays hidden."),
                ("Makes your computer run faster", False,
                 "No. If anything it slows a device as it works in the background."),
                ("Backs up your files safely", False,
                 "No. Spyware steals your information; it does not protect it."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why does spyware often go unnoticed for a long time?",
            "options": [
                ("It is designed to stay hidden and make no obvious changes while it steals", True,
                 "Yes. Unlike ransomware it does not announce itself, so it can watch quietly for weeks."),
                ("It immediately locks you out of your computer", False,
                 "That is ransomware. Spyware does the opposite and hides."),
                ("It always shows a large warning on the screen", False,
                 "No. Announcing itself would defeat its purpose. Spyware stays quiet."),
                ("It only runs for one second and then deletes itself", False,
                 "No. It tends to sit and watch for as long as it can."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "An infected USB stick spreads malware only to people who open the file on it. This behaviour describes a:",
            "options": [
                ("Virus", True,
                 "Yes. It still needs a person to open the file, which is the mark of a virus rather than a self-spreading worm."),
                ("Worm", False,
                 "A worm would spread by itself without anyone opening anything. This one waits for a person."),
                ("DDoS attack", False,
                 "A DDoS is a flood of traffic against a service, not an infected file on a USB stick."),
                ("Data breach", False,
                 "A breach is information being exposed. This is malware spreading through an opened file, a virus."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Most malware gets its first foothold by:",
            "options": [
                ("Someone opening an attachment, running a download, or clicking a bad link", True,
                 "Yes. Many entry points involve a person acting, which is why care at that moment stops so much malware."),
                ("Appearing on a computer with no cause at all", False,
                 "Malware needs a way in. It does not simply materialise from nothing."),
                ("The computer being too new", False,
                 "Age is not how malware arrives. It comes through downloads, attachments and links."),
                ("Having antivirus installed", False,
                 "Antivirus helps stop malware; it does not invite it in."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Which statement is true about the malware family?",
            "options": [
                ("A virus is one type of malware, alongside worms, trojans and spyware", True,
                 "Yes. Malware is the family; virus is a single member people often use as a catch-all by mistake."),
                ("Virus and malware mean exactly the same thing", False,
                 "No. A virus is one kind of malware, not the whole category."),
                ("Trojans spread by themselves like worms", False,
                 "No. Trojans wait to be run; worms self-spread."),
                ("Spyware always announces itself loudly", False,
                 "No. Spyware's whole point is to stay hidden."),
            ],
        },
        # ---- Lesson 2: ransomware, paying, DDoS, scale ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What does ransomware do?",
            "options": [
                ("Encrypts your files and demands a payment to unlock them", True,
                 "Yes, and a tested backup is what lets you recover without paying."),
                ("Floods a website with traffic", False,
                 "That is a DDoS. Ransomware locks your files and demands money."),
                ("Quietly records your passwords", False,
                 "That is spyware. Ransomware makes itself very much known."),
                ("Speeds up your computer", False,
                 "No. Ransomware locks you out of your own files."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "Ransomware mainly attacks which security pillar?",
            "options": [
                ("Availability, because you cannot reach your own files", True,
                 "Yes. The files are still there and unchanged, you just cannot get to them."),
                ("Confidentiality, because the files are shown to the public", False,
                 "Classic ransomware locks files rather than publishing them. The core hit is to availability."),
                ("Integrity, because it edits your files to mislead you", False,
                 "It scrambles files wholesale rather than quietly editing them. The pillar lost is availability."),
                ("None, ransomware is harmless", False,
                 "It is among the most damaging attacks a business can face."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Why do authorities generally advise against paying a ransom?",
            "options": [
                ("It does not guarantee recovery, funds more crime, and marks you as a business that pays", True,
                 "Right. Payment is unreliable and it bankrolls the next attack, sometimes on you again."),
                ("Paying instantly removes the malware for good", False,
                 "It does not. Paying deals with the demand, not the infection or the open door."),
                ("The files unlock themselves after a week anyway", False,
                 "There is no such guarantee. Without a backup or a working key, encrypted files stay locked."),
                ("Backups are more expensive than a ransom", False,
                 "Backups are far cheaper and, unlike a payment, they actually work."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is the best defence that lets a business recover from ransomware without paying?",
            "options": [
                ("Recent backups that have been tested and can actually be restored", True,
                 "Yes. A clean copy to restore takes away the attacker's leverage entirely."),
                ("A faster internet connection", False,
                 "Speed does nothing against ransomware."),
                ("Paying quickly for a discount", False,
                 "Paying is unreliable and funds crime. A tested backup is the real answer."),
                ("Turning the computer off and on again", False,
                 "That will not undo the encryption ransomware applies."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "What does 'DDoS' stand for and do?",
            "options": [
                ("Distributed Denial of Service: it floods a service with traffic so real users cannot reach it", True,
                 "Yes. It is an attack on availability, burying a service under junk traffic."),
                ("Data Deletion of Storage: it erases your hard drive", False,
                 "No. A DDoS does not delete files; it overwhelms a service with traffic."),
                ("Direct Download of Software: it installs programs", False,
                 "No. A DDoS is a traffic flood, not a download."),
                ("Double Data of Security: it backs up your data twice", False,
                 "No. A DDoS is a denial-of-service attack, not a backup."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What makes a DDoS hard to simply block?",
            "options": [
                ("The flood comes from thousands of computers at once, not one place", True,
                 "Yes. Because it is distributed across many infected devices, there is no single source to shut off."),
                ("It comes from a single, easily blocked address", False,
                 "That would be easy to block. The difficulty is that it is distributed across many sources."),
                ("It only happens once and never repeats", False,
                 "DDoS attacks can be sustained and repeated. Their spread across many sources is what makes them hard to block."),
                ("It politely asks the server to slow down", False,
                 "There is nothing polite about it. It overwhelms the service with sheer volume."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "During a DDoS attack, what happens to your data?",
            "options": [
                ("Nothing is stolen or changed; the service is just made unreachable", True,
                 "Yes. A DDoS attacks availability only. Your files are intact but customers cannot get through."),
                ("Every file is encrypted and held for ransom", False,
                 "That is ransomware. A DDoS does not touch your files."),
                ("The customer database is copied and sold", False,
                 "That is a data breach. A DDoS floods the service rather than stealing data."),
                ("Your passwords are recorded as you type", False,
                 "That is spyware. A DDoS is a traffic flood from the outside."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A network of infected computers used to send the traffic in a DDoS is called a:",
            "options": [
                ("Botnet", True,
                 "Yes. A botnet is a collection of hijacked devices an attacker directs, often to flood a target."),
                ("Backup", False,
                 "No. A backup is a safe copy of your data, nothing to do with an attack."),
                ("Firewall", False,
                 "No. A firewall is a defence. The attacking network of infected devices is a botnet."),
                ("Trojan", False,
                 "A trojan might be used to infect a device, but the network of infected devices itself is a botnet."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Which of these is an attack on the whole business at once, rather than a single device?",
            "options": [
                ("Ransomware locking every file on the shared drive", True,
                 "Yes. When the shared drive is locked for everyone, the whole business is affected and it needs a coordinated response."),
                ("A keylogger on one reception computer", False,
                 "Serious, but it sits on one device that can be isolated and cleaned."),
                ("A virus in an attachment one person opened", False,
                 "That starts on a single machine, even if it can spread when forwarded."),
                ("A trojan on one staff member's laptop", False,
                 "That affects the one laptop, not the whole organisation at once."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "You realise ransomware is encrypting files on your PC. Sensible first move?",
            "options": [
                ("Disconnect the computer from the network to stop it spreading", True,
                 "Yes. Getting it off the network first limits the spread to shared drives and other machines."),
                ("Keep working and hope it stops", False,
                 "Carrying on just gives it time to encrypt more and reach others. Disconnect first."),
                ("Pay the ransom immediately", False,
                 "Not the first move, and often not needed at all. Contain it, then report and get advice."),
                ("Email the ransom note to all staff to warn them", False,
                 "Warning people matters, but the urgent first action is to disconnect and contain the spread."),
            ],
        },
        # ---- Lesson 3: breaches, Optus, Medibank ----
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What is a data breach?",
            "options": [
                ("Personal information being taken or exposed to people who should not have it", True,
                 "Yes. A breach is a failure of confidentiality: private data ends up in the wrong hands."),
                ("Your files being encrypted for ransom", False,
                 "That is ransomware. A breach is about data being exposed, not locked."),
                ("A website being flooded with traffic", False,
                 "That is a DDoS. A breach is about information leaking, not availability."),
                ("A computer running slowly", False,
                 "That is a performance issue, not a data breach."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "A data breach is mainly a failure of which pillar?",
            "options": [
                ("Confidentiality, because private data reaches the wrong people", True,
                 "Yes. The systems may keep running; the harm is who can now see the information."),
                ("Availability, because you cannot reach your files", False,
                 "That is ransomware or a DDoS. In a breach the data is often still accessible to you; it has just also leaked."),
                ("Integrity, because the data is secretly altered", False,
                 "A breach is usually about exposure, not quiet alteration. The pillar lost is confidentiality."),
                ("Speed, because the network slows down", False,
                 "Speed is not one of the three pillars. A breach is a confidentiality failure."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Roughly how many people were affected by the 2022 Optus breach?",
            "options": [
                ("In the order of 9.8 million current and former customers", True,
                 "Yes, a striking share of the Australian population caught in one incident."),
                ("About 500 people", False,
                 "It was vastly larger, reported to be around 9.8 million people."),
                ("Nobody was actually affected", False,
                 "A very large number were affected, reported to be around 9.8 million."),
                ("Exactly 100", False,
                 "The reported figure was far higher, in the order of 9.8 million."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "What was the widely reported cause of the Optus breach?",
            "options": [
                ("An access point to customer data was reachable over the internet without a login", True,
                 "Yes. On public reporting, a door that should have required a login did not, a failure of the basics."),
                ("A worm spread through the whole network", False,
                 "That is not what was reported. The issue was an exposed access point needing no login."),
                ("Every customer was individually phished", False,
                 "The breach was on the company's side, an exposed system, not customers being phished one by one."),
                ("The building's power was cut", False,
                 "A power cut is not a data breach. The reported cause was an exposed access point."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why was the data exposed in the Optus breach especially serious?",
            "options": [
                ("It included identity document numbers, which can be used to attempt identity theft", True,
                 "Yes. Names, birth dates and document numbers together are the ingredients for impersonating someone."),
                ("It was only marketing preferences", False,
                 "It went far beyond that, reaching identity document numbers for some of those affected."),
                ("The data was encrypted and unreadable", False,
                 "This was a breach, not ransomware. The exposed data was readable, which is the problem."),
                ("Nothing sensitive was involved", False,
                 "A great deal was, including identity document numbers for a portion of people affected."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "What made the Medibank breach particularly sensitive?",
            "options": [
                ("It exposed health claims information, some of the most private data there is", True,
                 "Yes. Health records can cause real distress if exposed, quite apart from any financial fraud."),
                ("It only exposed public phone book listings", False,
                 "It went well beyond public information, into private health claims data."),
                ("No personal information was involved", False,
                 "A great deal of personal and health information was involved."),
                ("It was a DDoS that stole nothing", False,
                 "It was a data breach, and sensitive health data was taken."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "On public reporting, how did attackers get into Medibank's systems?",
            "options": [
                ("Using a stolen login credential, appearing to be a genuine user", True,
                 "Yes. A stolen username and password opened the door, which is why unique passwords and two-factor matter so much."),
                ("By flooding the site with traffic", False,
                 "That is a DDoS. Medibank was a data breach via a stolen login."),
                ("By leaving a database open with no password", False,
                 "That was closer to the Optus account. Medibank reportedly involved a stolen credential."),
                ("By infecting customers with a virus", False,
                 "The reported entry point was a stolen login, not a virus spread among customers."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Medibank chose not to pay the ransom. What did the attackers then do?",
            "options": [
                ("Published the stolen data, showing that not paying carries a heavy cost too", True,
                 "Yes. It was a stark example that once sensitive data is taken, there are no good options left."),
                ("Quietly deleted all the stolen data", False,
                 "They did the opposite and published it. Attackers cannot be trusted to delete anything."),
                ("Returned the data and apologised", False,
                 "Criminals do not do that. They published the data when the ransom was refused."),
                ("Restored the company's files for free", False,
                 "This was a breach, not ransomware on Medibank's files. The attackers published the stolen data."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "You are told your details were in a company's data breach. A sensible first step is to:",
            "options": [
                ("Change that account's password and anywhere you reused it, and turn on two-factor", True,
                 "Yes. You cannot recall leaked data, but you can lock down the accounts so it is harder to misuse."),
                ("Do nothing, since the data is already out", False,
                 "There is plenty you can still do to reduce the risk to your accounts."),
                ("Pay any fee the follow-up message asks for", False,
                 "The opposite. Messages quoting your breached details are usually the follow-on scam."),
                ("Post your new password publicly so it is on record", False,
                 "Never share a password. Keep it private and unique."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Why do phishing scams often spike right after a big breach?",
            "options": [
                ("Scammers use the leaked real details to make their messages far more convincing", True,
                 "Yes. A message that quotes your real name or provider is much harder to doubt, so breaches fuel the next round of phishing."),
                ("Breaches make everyone's spam filter stop working", False,
                 "Filters keep working. The spike comes from scammers exploiting the leaked details."),
                ("Companies send more genuine emails after a breach", False,
                 "The surge is scam messages exploiting the breach, not a rise in genuine mail."),
                ("Phishing has nothing to do with breaches", False,
                 "They are closely linked. Breached data is raw material for more convincing phishing."),
            ],
        },
        # ---- Lesson 4: recognising and reacting ----
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "Which of these is a classic warning sign worth reporting?",
            "options": [
                ("Colleagues receiving strange emails 'from you' that you never sent", True,
                 "Yes. That strongly suggests your account or device is compromised, and it is worth reporting straight away."),
                ("Your computer working exactly as normal", False,
                 "That is reassuring, not a warning sign."),
                ("An expected email from a known colleague", False,
                 "That is normal activity, not a warning sign."),
                ("A website loading slowly once, then fine", False,
                 "A single slow load is usually nothing. Watch for persistent or unexplained changes instead."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Files on a machine suddenly being renamed with odd new extensions is a hallmark of:",
            "options": [
                ("Ransomware", True,
                 "Yes. Mass renaming as files are encrypted, often with a new extension, is a classic ransomware sign."),
                ("A DDoS attack", False,
                 "A DDoS floods a service with traffic; it does not rename your local files."),
                ("A slow internet connection", False,
                 "That would not rename files. Mass renaming points to ransomware."),
                ("A normal software update", False,
                 "Updates do not scramble your files and rename them. That pattern is ransomware."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Which pattern points to a real attack rather than an ordinary glitch?",
            "options": [
                ("Many files renamed at once with a demand for payment on screen", True,
                 "Yes. A coordinated change across many files plus a ransom demand is clearly an attack."),
                ("One program crashing once and reopening fine", False,
                 "That is a classic ordinary glitch, not an attack."),
                ("Slow wifi during a thunderstorm", False,
                 "That has an everyday explanation. It is a glitch, not an attack."),
                ("A printer needing a restart", False,
                 "That is routine equipment trouble, not a security incident."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Your laptop is slow, and it turns out the hard drive is almost completely full. This is most likely:",
            "options": [
                ("An ordinary glitch with an ordinary fix, not an attack", True,
                 "Yes. A full drive is a common, harmless cause of slowness. Notice, then check, rather than assuming the worst."),
                ("Definitely ransomware", False,
                 "Ransomware locks files and demands payment. A full drive causing slowness does not fit that."),
                ("Definitely a DDoS", False,
                 "A DDoS floods an online service. A full local drive is unrelated."),
                ("Definitely a data breach", False,
                 "A breach is about exposed data, not a slow laptop with a full drive."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Why is it a problem to treat every minor glitch as a serious attack?",
            "options": [
                ("Crying wolf too often means real warnings get ignored", True,
                 "Yes. Constant false alarms exhaust everyone and drown out the genuine signals when they come."),
                ("Glitches are always attacks, so it is never a problem", False,
                 "Many glitches are harmless and everyday. Treating all of them as attacks is counterproductive."),
                ("It makes your computer faster", False,
                 "It has no such effect. The real cost is that genuine alerts stop being taken seriously."),
                ("Reporting anything is against the rules", False,
                 "Reporting genuine concerns is encouraged. The point is to distinguish real signals from noise."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "You spot ransomware encrypting files on your PC. What is the best first action?",
            "options": [
                ("Disconnect the computer from the network to stop the spread", True,
                 "Yes. Isolating it first is the single best way to stop it reaching shared drives and other machines."),
                ("Delete the ransom note and try to clean it up quietly yourself", False,
                 "Cleaning up alone can destroy evidence and miss other affected machines. Report it instead."),
                ("Pay the ransom straight away", False,
                 "Not the first move, and often unnecessary. Contain it first, then report and get advice."),
                ("Keep working so you do not lose time", False,
                 "Carrying on gives it time to spread. Disconnecting first contains the damage."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "After disconnecting an infected machine, the next best step is to:",
            "options": [
                ("Report it to whoever looks after IT straight away", True,
                 "Yes. Fast reporting gets the right people acting while the damage is small, and there is no trouble for raising it early."),
                ("Say nothing in case you get blamed", False,
                 "Staying quiet lets the problem grow. Early, blame-free reporting is what limits the damage."),
                ("Reconnect it to see if the problem fixed itself", False,
                 "Reconnecting risks spreading the infection again. Keep it isolated and report it."),
                ("Wait a week to see what happens", False,
                 "Waiting only gives an attacker time. Report it now."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "The people around you noticing strange emails 'from you' shows that:",
            "options": [
                ("Colleagues and contacts are part of your early-warning system", True,
                 "Yes. Others often spot a compromise before anything on your own screen looks wrong."),
                ("You should ignore what other people report", False,
                 "The opposite. Their reports can be your first and best clue that something is wrong."),
                ("Nothing is wrong as long as your screen looks normal", False,
                 "A compromise can be invisible on your own screen while it is obvious to the people receiving messages from you."),
                ("Email is always safe", False,
                 "Email is a common route for attacks. Reports of strange messages from you are a real warning."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "The calm approach to a possible threat is best summed up as:",
            "options": [
                ("Notice the change, then check, rather than panicking or ignoring it", True,
                 "Yes. Calm attention beats both alarm and denial, and a quick check with IT usually settles it."),
                ("Assume the worst and shut everything down immediately", False,
                 "Over-reacting to every hiccup causes its own harm and burns out your alertness."),
                ("Ignore everything unless the whole office stops working", False,
                 "By then a threat has had free rein. Early noticing and checking is far better."),
                ("Only worry if a message tells you to worry", False,
                 "Scam messages often tell you to act. Your own calm judgement matters more than their prompts."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Recognising a threat early matters most because:",
            "options": [
                ("A threat caught while it is small is far cheaper and easier to contain", True,
                 "Yes. One hot laptop or one strange email is a manageable problem; a spread across the business is not."),
                ("Early threats are always harmless", False,
                 "They are not harmless, but they are far easier to contain before they spread."),
                ("It lets you ignore the problem for longer", False,
                 "Recognising early is about acting sooner, not delaying."),
                ("It guarantees nothing bad will ever happen", False,
                 "Nothing guarantees that, but early recognition dramatically limits the damage."),
            ],
        },
    ],
}
