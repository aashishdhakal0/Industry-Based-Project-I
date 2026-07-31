"""Module 3, Phishing & Social Engineering: the con behind the click, the email
family (phishing, spear phishing, whaling), the attacks that leave the inbox
(smishing, vishing, pretexting, baiting), and the investigator's habits.

Same shape and standard as Modules 1 and 2 (see modules/content/module_one.py and
docs/module-authoring.md): a lesson is a scrollable room of collapsible task
PANELS. Each panel is a full, deep task: several teaching paragraphs (what it is,
a concrete Australian example, why it matters, what to do), a diagram where it
helps, a callout box with a specific scenario, sometimes a mid-panel check, then
the end interactive. Points sum to 10 per lesson and bank at lesson end.

Voice: warm, confident, human. Plain Australian English. No em-dashes, no filler,
no repetition, and nothing recycled from earlier modules.

Panel fields: key, kind, points, title, optional `diagram`, `body` (rich HTML,
may include a `<div class="cy-callout">`), optional `inline_check`
{question, hint, options}, optional `body2`, then either a check
(question/hint/options) or an activity (`payload`). Check option tuples are
(text, is_correct, explanation).
"""

LESSONS = [
    {
        "title": "The con behind the click",
        "reading_time_minutes": 10,
        "intro": "Phishing is not really a computer attack, it is a confidence "
        "trick. Meet social engineering, the levers it pulls on human nature, and "
        "why careful, clever people fall for it every day.",
        "tasks": [
            {
                "key": "what-se",
                "kind": "check",
                "points": 2,
                "title": "Hacking the human, not the machine",
                "diagram": "se-levers",
                "body": "<p>Most of this course has been about protecting machines: "
                "the network, the router, the files. This module is about something "
                "the attacker finds far easier to break into than any of those, which "
                "is you. The polite name for it is social engineering, and it simply "
                "means manipulating a person into doing something that helps the "
                "attacker, rather than hacking a computer to do it.</p>"
                "<p>Think about why a criminal would bother cracking a strong password "
                "when they could just talk someone into handing it over. Guessing a "
                "long, unique password could take a computer millions of years. "
                "Sending a convincing email that asks for it takes about five minutes. "
                "The technology you have learned to secure is genuinely hard to break, "
                "so the modern attacker aims at the one part of the system that can be "
                "reasoned with, rushed and charmed.</p>"
                "<p>Phishing, the fake message you have met a few times already, is the "
                "most common form of social engineering, but it is not the only one. "
                "The same trick works by text, by phone call, and in person. What ties "
                "them together is not the channel, it is the goal: to get a human being "
                "to trust, to hurry, and to act.</p>"
                "<div class=\"cy-callout\"><strong>Why this matters to you:</strong> "
                "you are not the weakest link, you are the thing the attacker is "
                "actually targeting, which makes you the most important defence there "
                "is. Every other control can be perfect, and a single convincing "
                "request can still walk straight past it if the person on the end "
                "says yes. That is daunting, but it is also empowering: your judgement "
                "is the control that catches what the machines cannot.</div>",
                "question": "What is social engineering?",
                "hint": "Look for the option about manipulating a person rather than attacking a machine.",
                "options": [
                    ("Manipulating a person into doing something that helps the attacker", True,
                     "Yes. Social engineering targets human trust and judgement, which is often far easier than breaking the technology."),
                    ("A way of designing social media websites", False,
                     "No. Despite the name, it has nothing to do with building websites. It is a con aimed at people."),
                    ("A tool that makes passwords stronger", False,
                     "The opposite. Social engineering is a technique attackers use, not a protection."),
                    ("A type of firewall", False,
                     "No. A firewall is a technical defence. Social engineering is about tricking people, not machines."),
                ],
            },
            {
                "key": "levers",
                "kind": "check",
                "points": 2,
                "title": "The levers they pull",
                "body": "<p>Social engineering works because it pulls on a handful of "
                "very normal human instincts. None of these are flaws in you; they are "
                "the ordinary reflexes that make daily life work. Attackers have simply "
                "learned to press them on purpose.</p>"
                "<p>The big ones are worth naming. <strong>Authority</strong>: we tend "
                "to do what a boss, a bank or the tax office appears to ask. <strong>"
                "Urgency</strong>: a deadline or a threat makes us act before we think. "
                "<strong>Fear</strong>: the worry that an account will be closed or a "
                "fine will grow pushes us to comply. <strong>Curiosity</strong>: an "
                "intriguing subject line or an unexpected file is hard to leave alone. "
                "And <strong>trust</strong>: a familiar name, logo or friendly tone "
                "lowers our guard.</p>"
                "<p>Once you can name the lever, the spell weakens. A message that "
                "combines authority and urgency, say an email that looks like it is "
                "from your manager and demands something in the next ten minutes, is "
                "not a coincidence. That combination is engineered, and recognising "
                "the engineering is the first step to not being moved by it.</p>"
                "<div class=\"cy-callout\"><strong>The tax-time double whammy.</strong> "
                "A message claiming to be from the ATO, warning of an overdue debt and "
                "a fine that grows each day, pulls authority and fear and urgency all "
                "at once. It is designed to make your stomach drop so you pay first and "
                "think later. Noticing all three levers pressing at the same moment is "
                "itself the warning sign.</div>",
                "inline_check": {
                    "question": "An email that looks like it is from your CEO and says 'do this in the next 10 minutes' is mainly pulling which two levers?",
                    "hint": "Think about who it claims to be from, and the time pressure it applies.",
                    "options": [
                        ("Authority and urgency", True,
                         "Yes. The apparent seniority is authority, and the tight deadline is urgency. Together they are engineered to stop you checking."),
                        ("Curiosity and trust", False,
                         "Those can feature elsewhere, but the standout here is a senior figure (authority) plus a hard deadline (urgency)."),
                        ("Neither, it is a genuine request", False,
                         "The combination of apparent authority and a sudden deadline is a classic pressure tactic worth pausing on."),
                        ("Fear and curiosity", False,
                         "There may be a little fear, but the clearest pair is authority (the CEO) and urgency (ten minutes)."),
                    ],
                },
                "body2": "<p>Here is the practical move. When a message makes you feel "
                "something strongly, pressured, frightened, flattered or intensely "
                "curious, treat that feeling as a prompt to slow down rather than speed "
                "up. The emotion is often the attack working. Naming the lever out loud, "
                "even just to yourself, breaks its grip long enough for your judgement "
                "to catch up.</p>",
                "question": "Why is it useful to recognise the lever a message is pulling?",
                "hint": "What happens to the trick once you can name what it is doing to you?",
                "options": [
                    ("Naming the lever weakens its grip, giving your judgement time to catch up", True,
                     "Exactly. The manipulation works best unnoticed. Spotting it turns a strong feeling into a signal to slow down."),
                    ("It makes the message load faster", False,
                     "This is about your judgement, not technical speed. Recognising the lever helps you resist the pressure."),
                    ("It means the message is definitely safe", False,
                     "No. Recognising a lever is a warning sign, not an all-clear. It prompts you to check, not to trust."),
                    ("It automatically reports the sender", False,
                     "Recognising a lever is a mental habit, not an automatic action. It helps you pause and then decide."),
                ],
            },
            {
                "key": "baiting",
                "kind": "check",
                "points": 2,
                "title": "Baiting: the tempting offer",
                "body": "<p>Not every con relies on fear and pressure. Baiting works "
                "the opposite way, by offering something you want. The lever it pulls "
                "is curiosity or a little greed, and it dangles a reward to get you to "
                "take an action you otherwise would not.</p>"
                "<p>The classic physical version is a USB stick left where a staff "
                "member will find it, in a car park or a foyer, labelled something "
                "irresistible like 'Staff salaries 2025' or 'Confidential'. Whoever "
                "plugs it in to see what is on it has just invited malware onto the "
                "network, which is exactly what the label was for. The digital versions "
                "are everywhere too: a free copy of expensive software, a prize you did "
                "not enter to win, a leaked celebrity photo, a too-good voucher.</p>"
                "<p>The defence is a healthy suspicion of the unearned. If something "
                "arrives free, unexpected and enticing, that is precisely when to be "
                "most careful, because the enticement is doing a job. A found USB "
                "stick goes to your IT team, not into your computer, and an offer that "
                "seems too good to be true almost always is.</p>"
                "<div class=\"cy-callout\"><strong>The car park drop in "
                "Cairns.</strong> A tourism operator's staff found three USB sticks "
                "scattered near the staff entrance one morning, each neatly labelled "
                "'Rosters and pay'. One curious employee plugged one in to return it to "
                "its owner, and quietly installed malware that had been waiting on it. "
                "The label was the whole attack. Curiosity, not carelessness, was the "
                "lever.</div>",
                "question": "What is baiting?",
                "hint": "Unlike a threat, this technique offers you something. What is it exploiting?",
                "options": [
                    ("Luring you with something tempting, like a found USB stick or a free prize, to make you act", True,
                     "Yes. Baiting exploits curiosity or greed by dangling a reward, such as a labelled USB or a too-good offer."),
                    ("Threatening to close your account unless you pay", False,
                     "That is a fear and urgency tactic. Baiting tempts you with a reward rather than a threat."),
                    ("Flooding a website with traffic", False,
                     "That is a DDoS from Module 2. Baiting is a social trick that offers you something enticing."),
                    ("Encrypting your files for a ransom", False,
                     "That is ransomware. Baiting is the lure that might deliver such malware, by tempting you to take an action."),
                ],
            },
            {
                "key": "why-smart-people",
                "kind": "check",
                "points": 2,
                "title": "Why careful people still fall",
                "body": "<p>It is tempting to think phishing only catches the careless "
                "or the not-very-tech-savvy. That comfort is exactly what makes the "
                "rest of us vulnerable. Some of the most damaging incidents in "
                "Australia have caught experienced, intelligent professionals, and it "
                "is worth being honest about why.</p>"
                "<p>Falling for a con is not a failure of intelligence, it is a "
                "consequence of being human and busy. You process a great many "
                "messages a day, mostly on autopilot, often on a phone between other "
                "tasks. A good social engineering attack is designed to fit that flow: "
                "it looks routine, it arrives at a plausible moment, and it asks for "
                "something that feels normal. You are not being stupid when you nearly "
                "act on it, you are being efficient, and the attacker is exploiting "
                "your efficiency.</p>"
                "<p>This matters because the belief 'I would never fall for that' is "
                "itself a risk. The people who stay safest are not the ones who think "
                "they are too smart to be tricked, they are the ones who accept that "
                "anyone can be caught on the wrong day and therefore build in a habit "
                "of checking. Humility is a security control.</p>"
                "<div class=\"cy-callout\"><strong>Watch for this:</strong> the danger "
                "moment is not when a message looks obviously dodgy, it is when it "
                "looks completely normal and lands while you are rushed. That is when a "
                "careful person acts on autopilot. The fix is not to be cleverer, it is "
                "to slow down for the requests that actually matter, like a payment or "
                "a password.</div>",
                "question": "Why do intelligent, careful people still fall for phishing?",
                "hint": "Think about how you process most messages during a busy day.",
                "options": [
                    ("Attacks are designed to look routine and arrive when you are busy and on autopilot", True,
                     "Yes. It is not about intelligence. A good con fits the flow of a busy day, which is exactly when we act without checking."),
                    ("Only people who ignore training ever fall for it", False,
                     "Not so. Experienced, trained professionals are caught too, because the best attacks look completely normal."),
                    ("It only happens to people who are bad with computers", False,
                     "Being technical is little protection against a convincing human con. Anyone rushed can be caught."),
                    ("Because they never receive any emails", False,
                     "That makes no sense. The risk comes precisely from handling many messages quickly."),
                ],
            },
            {
                "key": "lever-sort",
                "kind": "sort",
                "points": 2,
                "title": "Match the message to the lever",
                "body": "<p>The quickest way to make the levers stick is to spot them "
                "in the wild. Remember the main ones: <strong>authority</strong> "
                "(a boss, a bank, the tax office), <strong>urgency</strong> (act now or "
                "else), <strong>fear</strong> (something bad will happen), and <strong>"
                "curiosity</strong> (you will want to look).</p>"
                "<p>Below are eight lines lifted from real-style scam messages. Tap "
                "each one, then tap the main lever it is pulling. Get all eight to "
                "finish.</p>",
                "payload": {
                    "prompt": "Tap a scam line, then tap the lever it pulls. All eight to finish.",
                    "buckets": [
                        {"id": "authority", "label": "Authority"},
                        {"id": "urgency", "label": "Urgency"},
                        {"id": "fear", "label": "Fear"},
                        {"id": "curiosity", "label": "Curiosity"},
                    ],
                    "items": [
                        {"id": "ceo", "text": "This is the CEO. I need you to handle a payment for me.",
                         "bucket": "authority", "why": "Leaning on a senior figure's position is the authority lever."},
                        {"id": "ato", "text": "Official notice from the Tax Office regarding your account.",
                         "bucket": "authority", "why": "Posing as a government body borrows authority to make you comply."},
                        {"id": "10min", "text": "You have 10 minutes before this link expires.",
                         "bucket": "urgency", "why": "A ticking deadline is pure urgency, designed to stop you checking."},
                        {"id": "today", "text": "Pay today or the service will be cut off.",
                         "bucket": "urgency", "why": "Act now or lose something is the urgency lever."},
                        {"id": "arrest", "text": "A warrant will be issued for your arrest unless you respond.",
                         "bucket": "fear", "why": "A frightening threat is the fear lever, meant to override calm judgement."},
                        {"id": "suspend", "text": "Your account has been compromised and will be suspended.",
                         "bucket": "fear", "why": "The dread of losing access is fear, pushing you to react."},
                        {"id": "photos", "text": "You will not believe these leaked photos, click to see.",
                         "bucket": "curiosity", "why": "An irresistible tease is the curiosity lever."},
                        {"id": "salary", "text": "Attached: the new staff salary spreadsheet.",
                         "bucket": "curiosity", "why": "A file you are dying to open plays on curiosity."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Phishing and its sharper cousins",
        "reading_time_minutes": 10,
        "intro": "From the wide net of ordinary phishing to the tailored strike of "
        "spear phishing and whaling. Then triage a real morning's inbox and tell the "
        "genuine mail from the fakes.",
        "tasks": [
            {
                "key": "phishing",
                "kind": "check",
                "points": 2,
                "title": "Phishing: one net, thrown wide",
                "diagram": "phishing-email",
                "body": "<p>Ordinary phishing is the mass-market version of the con: "
                "the same fake message sent to enormous numbers of people at once, in "
                "the hope that a small fraction will bite. The attacker does not know "
                "or care who you are. You are one address in a list of a hundred "
                "thousand, and the message is written to be vaguely plausible to "
                "anyone.</p>"
                "<p>Because it is generic, ordinary phishing carries the tells you "
                "already know from Module 1. A greeting like 'Dear Customer' because it "
                "cannot use your name. A sender address that is a lookalike rather than "
                "the real thing. A manufactured deadline. And a link that leads "
                "somewhere other than where it claims. The diagram above is a textbook "
                "example, with each tell marked.</p>"
                "<p>The economics explain the sloppiness. When you send to a hundred "
                "thousand people, you do not need each message to be a masterpiece, you "
                "just need a few percent to click. That is also the good news: mass "
                "phishing is the easiest kind to catch, because the same lack of "
                "personal detail that makes it cheap to send is what gives it "
                "away.</p>"
                "<div class=\"cy-callout\"><strong>A whole street gets the same "
                "email.</strong> On the same morning, a hairdresser, a plumber and a "
                "cafe on one Adelaide high street each receive an identical email "
                "claiming their email account is 'over quota' and must be verified "
                "within 24 hours. It is addressed to none of them by name. That is "
                "mass phishing: no aim, just volume, hoping one of the three is busy "
                "enough to click.</div>",
                "inline_check": {
                    "question": "What is the giveaway that most reveals ordinary mass phishing?",
                    "hint": "Think about what a message sent to a hundred thousand strangers cannot know about you.",
                    "options": [
                        ("It is generic, with no personal detail, because it was sent to a huge list", True,
                         "Yes. Mass phishing cannot personalise, so a generic greeting and no specific detail are the classic tells."),
                        ("It always addresses you by your full name", False,
                         "The opposite. Mass phishing usually cannot use your name, which is why it says things like 'Dear Customer'."),
                        ("It comes from your real bank's genuine address", False,
                         "It comes from a lookalike, not the genuine address. A real address is not a phishing tell."),
                        ("It is written in perfect, personalised detail about your job", False,
                         "That would point to spear phishing, which is targeted. Mass phishing is generic."),
                    ],
                },
                "body2": "<p>Hold on to that idea of the generic net, because the next "
                "two panels are about what happens when an attacker stops fishing with "
                "a net and starts fishing with a spear. The moment a message knows "
                "something real about you, the tells you rely on start to "
                "disappear.</p>",
                "question": "How does ordinary phishing differ from a targeted attack?",
                "hint": "Think about how many people receive it and how personalised it is.",
                "options": [
                    ("It is sent generically to huge numbers of people, not tailored to one person", True,
                     "Yes. Mass phishing throws one wide net at everyone, which is why it is generic and easier to spot."),
                    ("It is always sent to just one carefully chosen person", False,
                     "That describes spear phishing. Ordinary phishing is mass and generic."),
                    ("It can only be sent by post", False,
                     "Phishing arrives by email and other digital channels, not by post."),
                    ("It is completely harmless", False,
                     "Mass phishing catches a great many people every year. It is far from harmless."),
                ],
            },
            {
                "key": "spear",
                "kind": "check",
                "points": 2,
                "title": "Spear phishing: aimed at you by name",
                "body": "<p>Ordinary phishing is a net thrown wide: the same message "
                "blasted to a hundred thousand inboxes, hoping a few people bite. Spear "
                "phishing is the opposite, and it is far more dangerous. It is a single "
                "message crafted for a single target, and it uses real details about "
                "you to slip under your guard.</p>"
                "<p>The difference you feel is that a spear phish does not read like "
                "spam. It knows your name, your role, the name of your manager or your "
                "supplier, a project you are actually working on. Instead of 'Dear "
                "Valued Customer' it says 'Hi Marnie, can you sort the invoice for the "
                "Thompson job before Friday?' Everything about it fits, because the "
                "attacker did their homework before sending a word.</p>"
                "<p>That homework is easier than most people realise, which is the "
                "subject of the next panel. Your name and role might be on the company "
                "website, your manager's name in a social media post, your supplier's "
                "name on the side of a work van in a photo. None of that is secret, and "
                "stitched together it lets a stranger write a message that sounds "
                "exactly like someone you know.</p>"
                "<div class=\"cy-callout\"><strong>A Newcastle building firm, one "
                "convincing email.</strong> The office manager receives a message that "
                "appears to be from a subcontractor she deals with every week, "
                "referring to the actual site they are working on and asking her to "
                "update the bank details for this month's payment. It is polite, "
                "specific and perfectly timed. Because it fits what she was expecting, "
                "she nearly changes the details without a second thought. What saves "
                "her is not spotting a spelling mistake, because there are none; it is "
                "the simple habit of ringing the subbie on his known number to "
                "check.</div>",
                "question": "What makes spear phishing more dangerous than ordinary mass phishing?",
                "hint": "Think about how it is written and who it is aimed at.",
                "options": [
                    ("It is personalised with real details about you, so it slips past your guard", True,
                     "Yes. Because it uses genuine, specific detail, the usual tells vanish and it reads like a real message."),
                    ("It is sent to far more people at once", False,
                     "The opposite. Spear phishing is aimed at one person or a small group, which is what makes it convincing."),
                    ("It always contains obvious spelling mistakes", False,
                     "No. A good spear phish is carefully written. Waiting for a spelling mistake will not save you."),
                    ("It can only be sent to email addresses, never phones", False,
                     "The targeting, not the channel, is the point. The danger is the personal detail, not where it lands."),
                ],
            },
            {
                "key": "how-they-research-you",
                "kind": "check",
                "points": 1,
                "title": "Where they get the details",
                "body": "<p>If spear phishing needs real details, it is fair to ask "
                "where an attacker finds them. The uncomfortable answer is that most of "
                "it is sitting in plain sight, put there by us for perfectly good "
                "reasons. Gathering it does not take a hacker, just a patient reader "
                "with a search engine.</p>"
                "<p>Your organisation's website lists staff names, roles and often "
                "email formats. Social media reveals who reports to whom, who is on "
                "leave, and what projects are underway. An out-of-office reply hands a "
                "stranger your manager's name and a colleague to contact 'in your "
                "absence'. A photo from a work event shows the supplier logos on the "
                "wall. None of it is secret, and that is the point: an attacker "
                "assembles a dozen harmless public facts into one very convincing "
                "message.</p>"
                "<div class=\"cy-callout\"><strong>The out-of-office goldmine.</strong> "
                "An automatic reply that says 'I am at a conference until Monday, for "
                "urgent accounts matters contact Dev on dev@firm.com.au' has just "
                "handed an attacker a script: pose as you, contact Dev, invent an "
                "urgent accounts matter. Consider keeping auto-replies brief and "
                "avoiding who-to-contact-for-payments detail.</div>",
                "question": "Where do attackers usually get the personal details for a spear phish?",
                "hint": "Does it take secret hacking, or just reading what is already public?",
                "options": [
                    ("From public sources: your website, social media, and auto-replies", True,
                     "Yes. Most of the detail is already public. Attackers simply assemble harmless facts into a convincing message."),
                    ("Only by breaking into your computer first", False,
                     "They rarely need to. The details for a spear phish are usually gathered from public information."),
                    ("They cannot get any real details, so they guess", False,
                     "Guessing is mass phishing. Spear phishing works precisely because the details are real and easy to find."),
                    ("From a secret government database", False,
                     "No need for anything so exotic. Public websites and social media supply most of what they use."),
                ],
            },
            {
                "key": "whaling",
                "kind": "check",
                "points": 2,
                "title": "Whaling: harpooning the big fish",
                "body": "<p>Whaling is spear phishing aimed at the biggest fish in the "
                "pond: senior executives, business owners, the people who can authorise "
                "money or access. The name is grimly literal. A single successful "
                "whaling attack on a person with signing authority can be worth far "
                "more than a thousand ordinary phishing hits.</p>"
                "<p>The most common and costly form is often called CEO fraud, or "
                "business email compromise. The attacker poses as a senior leader and "
                "sends an urgent, confidential request to someone in finance: 'I am in "
                "a meeting and cannot talk, please transfer this payment to close a "
                "deal, keep it between us for now.' It stacks authority, urgency and "
                "secrecy so the junior staff member feels unable to question it. "
                "Australian businesses lose serious money to this every year.</p>"
                "<p>The defence is a rule that protects everyone, especially the person "
                "being impersonated: any unusual or urgent payment request is verified "
                "on a separate, known channel before it is actioned, no matter who it "
                "appears to come from. A genuine leader will thank you for checking. An "
                "attacker is defeated by it. Making that verification a normal, "
                "expected step removes the pressure to just comply.</p>"
                "<div class=\"cy-callout\"><strong>The 'CEO' who could not "
                "talk.</strong> A Perth firm's accounts officer got an email from the "
                "managing director, travelling overseas, asking her to urgently pay a "
                "new supplier and to reply by email only because he was in back-to-back "
                "meetings. The 'reply by email only' was the tell: it existed to stop "
                "her doing the one thing that would have exposed it, picking up the "
                "phone. She rang his real number anyway. He had sent nothing.</div>",
                "question": "What is the safest defence against CEO fraud and whaling?",
                "hint": "The attack relies on you not checking with the real person. What removes that weakness?",
                "options": [
                    ("Verify any unusual or urgent payment request on a separate known channel, whoever it seems to be from", True,
                     "Yes. A quick check on a trusted, separate channel defeats the impersonation, and a genuine leader will welcome it."),
                    ("Always do what a senior person asks without question", False,
                     "That is exactly what the attack counts on. Seniority in an email is not proof, and urgency is a red flag."),
                    ("Reply to the email to ask if it is really them", False,
                     "Risky. If the account or address is controlled by the attacker, you are just asking the attacker."),
                    ("Only worry about emails from people you do not know", False,
                     "Whaling impersonates people you do know, like your own CEO. The safeguard is verifying the request, not the name."),
                ],
            },
            {
                "key": "mixed-inbox",
                "kind": "mailsort",
                "points": 3,
                "title": "Triage the morning inbox",
                "body": "<p>Real life does not label the emails for you. A normal "
                "morning is a mix of genuine mail and the occasional fake, and the "
                "skill is telling them apart at a glance without either clicking a "
                "scam or ignoring a real message.</p>"
                "<p>Below is a shared inbox as it might look first thing. Some of these "
                "are perfectly genuine and some are phishing, ordinary or targeted. For "
                "each one, decide: Genuine or Phishing. Lean on everything so far, the "
                "sender address, the levers, the specific detail or lack of it. Sort "
                "them all correctly to finish.</p>",
                "payload": {
                    "prompt": "Mark each email Genuine or Phishing. Sort all six correctly to finish.",
                    "emails": [
                        {"id": "colleague", "from": "Priya Sharma <priya.sharma@ourcouncil.gov.au>",
                         "subject": "Re: March minutes", "preview": "Thanks, I have attached the "
                         "final version we agreed on. See you Tuesday.",
                         "phish": False,
                         "why": "A colleague on your own domain, continuing a real thread, with no link, no pressure and no request for anything sensitive."},
                        {"id": "m365", "from": "Microsoft 365 <security@m365-account-verify.com>",
                         "subject": "Your password expires in 2 hours", "preview": "Verify your "
                         "account now to avoid being locked out permanently.",
                         "phish": True,
                         "why": "A lookalike domain (not microsoft.com), a manufactured two-hour deadline, and a verify-your-password link. Three tells at once."},
                        {"id": "invoice", "from": "Accounts <accounts@boltonsupplies.com.au>",
                         "subject": "Invoice 20418 for July delivery", "preview": "Please find "
                         "this month's invoice attached, same details as always. Thanks.",
                         "phish": False,
                         "why": "An expected invoice from a known supplier's real domain, same bank details as always, and no urgency or change of account."},
                        {"id": "ceo", "from": "Dan Reid <dan.reid.md@outlook-corp-mail.com>",
                         "subject": "Quick favour, are you at your desk?", "preview": "In meetings "
                         "all day. Need you to action a supplier payment urgently and keep it between us.",
                         "phish": True,
                         "why": "Whaling. The managing director's name on a public webmail lookalike, urgency, secrecy and a payment request. Verify on a known number."},
                        {"id": "newsletter", "from": "AusCyber Weekly <news@auscyberweekly.com.au>",
                         "subject": "This week in security", "preview": "Your Tuesday roundup of "
                         "cyber news. Manage your subscription any time at the link below.",
                         "phish": False,
                         "why": "A newsletter you subscribed to, from its consistent domain, with an ordinary manage-subscription link and nothing urgent or sensitive."},
                        {"id": "parcel", "from": "Australia Post <delivery@auspost-parcels-au.info>",
                         "subject": "Parcel held: small fee required", "preview": "Your parcel is "
                         "on hold. Pay a $3.20 redelivery fee within 24 hours or it will be returned.",
                         "phish": True,
                         "why": "A lookalike domain (not auspost.com.au), a small fee, and a 24-hour deadline. The real Australia Post does not collect fees this way."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Beyond the inbox",
        "reading_time_minutes": 10,
        "intro": "The same con by other channels: scam texts, scam phone calls, and "
        "the invented backstories that make them work. Then take a live pretext call "
        "and make the calls yourself.",
        "tasks": [
            {
                "key": "smishing",
                "kind": "check",
                "points": 2,
                "title": "Smishing: the con by text",
                "body": "<p>Phishing does not live only in email. Smishing is phishing "
                "by SMS, the scam text message, and it is thriving because a text feels "
                "more personal and immediate than an email, and there is less room on "
                "the screen for the details that would give it away.</p>"
                "<p>The themes are predictable because they work on almost everyone: a "
                "parcel held for a small fee, a myGov or Medicare message about a "
                "payment, a bank alert about a suspicious transaction, a toll or fine "
                "notice. Each pulls a familiar lever, and each carries a link to a "
                "lookalike site built to catch your details. The link is the hook, "
                "just as it is in email.</p>"
                "<p>The safe habit is the same one, adapted to the phone: never tap the "
                "link in an unexpected text. If you think it might be real, open the "
                "organisation's proper app or type its known website yourself, or ring "
                "the number on the back of your card. Your bank, myGov and Australia "
                "Post will never mind you reaching them the front way instead of "
                "through their supposed text.</p>"
                "<div class=\"cy-callout\"><strong>The link that looks almost "
                "right.</strong> A text says a myGov payment is waiting and links to "
                "my-gov-au-secure.com. The real service is my.gov.au. That extra "
                "wording, tacked around the familiar name, is the entire trick. When a "
                "text pushes you toward a link, the address bar is where the truth is, "
                "so go the front way and never tap through.</div>",
                "question": "You get an unexpected text about a held parcel with a link to pay a small fee. Best move?",
                "hint": "The link is the hook. How can you check without using it?",
                "options": [
                    ("Do not tap the link; check via the carrier's real app or website yourself", True,
                     "Yes. Go the front way. Open the official app or type the known address rather than trusting the link in the text."),
                    ("Tap the link quickly before the parcel is returned", False,
                     "That is exactly the pressure the scam relies on. The deadline and small fee are there to rush you."),
                    ("Reply to the text asking if it is genuine", False,
                     "Replying just reaches the scammer, who will say yes. Check through the carrier's real channel instead."),
                    ("Forward it to all your contacts to warn them", False,
                     "Well meant, but that spreads the scam link. Report it and check through the official channel instead."),
                ],
            },
            {
                "key": "vishing",
                "kind": "check",
                "points": 2,
                "title": "Vishing: the con by phone",
                "body": "<p>Vishing is phishing by voice, the scam phone call. Hearing "
                "a real human voice makes a con feel far more legitimate than an email "
                "ever could, and a skilled caller can steer a conversation, apply "
                "pressure and improvise in a way that a static message cannot. That is "
                "what makes it so effective.</p>"
                "<p>The familiar Australian versions pose as trusted institutions. A "
                "caller claims to be from the ATO, warning of a tax debt and threatening "
                "arrest unless you pay immediately, often by unusual means like gift "
                "cards. Another claims to be your bank's fraud team, saying your account "
                "is compromised and they need to 'verify' your details or move your "
                "money to a 'safe account'. Another poses as tech support, insisting "
                "your computer is infected and they need remote access to fix it.</p>"
                "<p>The rule that defeats all of them is beautifully simple: hang up and "
                "call back on a number you already trust. No genuine bank, tax office or "
                "company will object to you hanging up and ringing the number on your "
                "card, your statement or the official website. A scammer, on the other "
                "hand, will do everything to keep you on the line, because the moment "
                "you call back independently, the con is over.</p>"
                "<div class=\"cy-callout\"><strong>The gift-card giveaway.</strong> A "
                "Hobart retiree was told by a caller 'from the ATO' that she owed a debt "
                "and had to settle it that afternoon in gift cards from the "
                "supermarket, or police would attend. No real government body is ever "
                "paid in gift cards. That single detail marks the call as a scam before "
                "anything else, and hanging up to ring the ATO's real number would have "
                "confirmed it in a minute.</div>",
                "inline_check": {
                    "question": "A caller says they are from your bank's fraud team and need you to confirm your login to secure your account. What should you do?",
                    "hint": "Who can prove who they are over an incoming call, and how could you check independently?",
                    "options": [
                        ("Hang up and call the bank back on the number from your card or statement", True,
                         "Yes. You cannot verify an incoming caller, so end the call and ring the bank on a number you already trust."),
                        ("Read out your login details so they can secure the account", False,
                         "Never. A genuine bank will not ask you to confirm a password or code over the phone. This is the scam."),
                        ("Stay on the line and do whatever they ask to be safe", False,
                         "Staying on the line is what the scammer wants. Hang up and verify independently."),
                        ("Give them remote access to your computer to check", False,
                         "No. Handing remote access to an unverified caller is how a con becomes a compromise. Hang up and call back."),
                    ],
                },
                "body2": "<p>Notice the thread running through email, text and phone: "
                "the attacker always supplies the way to respond, the link or the "
                "number to call, because that path leads back to them. Your defence is "
                "to refuse the path they offer and reach the organisation the way you "
                "already know. On the phone that means hang up and call back, every "
                "time.</p>",
                "question": "What single habit defeats almost every scam phone call?",
                "hint": "The caller wants to keep you on the line. What breaks that?",
                "options": [
                    ("Hang up and call back on a number you already trust", True,
                     "Yes. You cannot verify an incoming caller, so ending the call and dialling a known number ends the con."),
                    ("Ask the caller to prove who they are", False,
                     "A practised scammer will happily reel off convincing details. You cannot verify them over their call, so call back instead."),
                    ("Stay polite and do as they ask", False,
                     "Complying is exactly the goal of the call. Politely hang up and verify independently."),
                    ("Give them a little information to see if they are genuine", False,
                     "Any information helps them. Do not test them by sharing; hang up and call the organisation yourself."),
                ],
            },
            {
                "key": "caller-id-spoofing",
                "kind": "check",
                "points": 1,
                "title": "The number can lie",
                "body": "<p>Here is the detail that makes vishing so convincing, and "
                "that many people do not know: the number showing on your phone can be "
                "faked. It is called caller ID spoofing, and it lets a scammer make "
                "their call appear to come from your bank's real number, a government "
                "line, or even a number in your own contacts.</p>"
                "<p>This matters because a lot of people treat the displayed number as "
                "proof. It is not. If a call shows your bank's name and number, that "
                "tells you almost nothing about who is really on the line. The same "
                "goes for the reverse trick, where a scammer tells you to 'check the "
                "number, it is really us', relying on the spoof to build trust.</p>"
                "<div class=\"cy-callout\"><strong>Trust the call back, not the caller "
                "ID.</strong> Because the incoming number can be faked but a number you "
                "dial yourself cannot be redirected, the safe move never changes: end "
                "the call and ring back on a number you sourced independently. The "
                "display lied on the way in; it cannot lie about where your own call "
                "goes out.</div>",
                "question": "A call shows your bank's real name and phone number on the screen. What does that prove?",
                "hint": "Can the number that appears on an incoming call be faked?",
                "options": [
                    ("Very little, because caller ID can be spoofed to show any number", True,
                     "Yes. The displayed number can be faked, so it is no proof. Hang up and call back on a number you trust."),
                    ("That the call is definitely genuine", False,
                     "No. Caller ID spoofing lets scammers display any number they like, including your bank's real one."),
                    ("That the caller has hacked your phone", False,
                     "Spoofing does not require hacking your phone. It simply fakes the number that is displayed."),
                    ("That you must be talking to your bank", False,
                     "A matching number is not proof. It can be spoofed, so verify by calling back independently."),
                ],
            },
            {
                "key": "pretexting",
                "kind": "check",
                "points": 2,
                "title": "Pretexting: the invented backstory",
                "body": "<p>Underneath many of these calls and emails is a technique "
                "called pretexting: the attacker invents a believable scenario and "
                "identity, a pretext, that gives them a reason to ask for what they "
                "want. It is the difference between a clumsy 'give me your password' "
                "and a smooth 'hi, it is Sam from IT, I am fixing that email issue "
                "you reported and I just need to confirm your login to test it'.</p>"
                "<p>The pretext works by supplying a story that makes the request feel "
                "normal. A fake IT technician helping with a problem. A fake auditor who "
                "needs access for a review. A fake delivery driver who needs a code. A "
                "fake new starter who cannot get into a system. Each has a reason to be "
                "asking, and each leans on your natural willingness to be helpful. "
                "Helpfulness is a lovely human trait and a favourite tool of the "
                "social engineer.</p>"
                "<p>The defence is to separate the request from the story. However "
                "plausible the backstory, some things are never appropriate to give "
                "out: your password, a one-time code, remote access to your machine. "
                "When anyone asks for those, the right response is not to judge how "
                "convincing they are, it is to stop and verify who they are through an "
                "official channel, regardless of how reasonable their reason "
                "sounds.</p>"
                "<div class=\"cy-callout\"><strong>'It is Sam from IT.'</strong> A "
                "Toowoomba real estate office got a call from a friendly 'IT "
                "contractor' following up a genuine-sounding support ticket, asking a "
                "staff member to read out the code that had just been texted to her so "
                "he could 'complete the sync'. That code was her two-factor login. The "
                "story was smooth, the manner was warm, and the request was one no real "
                "technician would ever make. She said she would call IT back, and the "
                "line went dead.</div>",
                "question": "What is pretexting?",
                "hint": "Think about the made-up story an attacker uses to justify their request.",
                "options": [
                    ("Inventing a believable identity and scenario that makes a request feel normal", True,
                     "Yes. The pretext is the cover story, like posing as IT support, that gives the attacker a reason to ask for what they want."),
                    ("Flooding a phone line with automated calls", False,
                     "That is a different attack. Pretexting is about a convincing invented story, not volume."),
                    ("Sending the same scam text to thousands of numbers", False,
                     "That is smishing at scale. Pretexting is a tailored backstory used to build trust."),
                    ("Encrypting files and demanding a ransom", False,
                     "That is ransomware. Pretexting is a social trick that uses a fabricated identity and reason."),
                ],
            },
            {
                "key": "phone-branch",
                "kind": "branch",
                "points": 3,
                "title": "A call from 'IT support'",
                "body": "<p>Time to handle one yourself. You are at the front desk when "
                "the phone rings, and the caller has a friendly manner and a plausible "
                "story. Make the calls you would really make. There are no trick "
                "questions, and if a choice goes wrong you will see why and get another "
                "go.</p>"
                "<p>The thread to hold onto: a smooth backstory is not proof, real "
                "support never needs your password or code, and verifying through a "
                "channel you already trust is always a reasonable thing to do.</p>",
                "payload": {
                    "prompt": "Choose what you would really do. You can always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "The phone rings. 'Hi, it is Sam from the IT support company your office "
                            "uses. We have had an alert on your account and I need to fix it before it locks you "
                            "out. Can you confirm the login you use?'",
                            "choices": [
                                {"label": "Read out your username and password so Sam can fix it", "to": "n1bad",
                                 "outcome": "bad",
                                 "feedback": "Real IT never needs your password to fix your account, and a friendly manner is not proof. That login is now the attacker's."},
                                {"label": "Say you will call the IT company back on their known number", "to": "n2",
                                 "outcome": "good",
                                 "feedback": "Exactly right. You cannot verify an incoming caller, so offer to call back through a channel you already trust."},
                            ],
                        },
                        "n1bad": {
                            "text": "Sam thanks you warmly and hangs up. Within the hour, your account is sending "
                            "phishing emails to the whole client list.",
                            "choices": [{"label": "See what would have worked", "to": "n2"}],
                        },
                        "n2": {
                            "text": "Sam gets a little pushy: 'There really is not time to call back, the account "
                            "will lock in five minutes. Just read me the code we have texted you and I will sort it.'",
                            "choices": [
                                {"label": "Read out the code, since there is a deadline", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "The five-minute deadline is manufactured urgency, and that code is your two-factor login. Never read it to anyone."},
                                {"label": "Decline, and hang up to call IT on their real number", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Well held. A sudden deadline plus a request for a code is the con showing itself. Hanging up ends it."},
                            ],
                        },
                        "n2bad": {
                            "text": "The code was your two-factor login. With it, the attacker walks straight into "
                            "your account, deadline and all.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "You have hung up. What is the most useful next step?",
                            "choices": [
                                {"label": "Report the call to your manager or IT so others are warned", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes. Reporting it means colleagues can be warned and the account watched, turning a dodgy call into a non-event."},
                                {"label": "Say nothing, since you did not fall for it", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "Not quite. If you were called, others are being called too. A quick heads-up protects the colleague who is busier than you today."},
                            ],
                        },
                        "n3bad": {
                            "text": "You keep it to yourself. An hour later a busier colleague, given no warning, "
                            "reads out their code to the same friendly voice.",
                            "choices": [{"label": "See the better path", "to": "end"}],
                        },
                        "end": {
                            "text": "That is a pretext call handled: a smooth story is not proof, no real support "
                            "needs your password or code, verify through a channel you trust, and warn others. You "
                            "just protected the whole office by not being rushed.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
    {
        "title": "Reading an email like an investigator",
        "reading_time_minutes": 9,
        "intro": "Turn everything into a routine: inspect a message for its tells, "
        "verify before you trust, report the right way, and name the technique when "
        "you see it.",
        "tasks": [
            {
                "key": "inspect",
                "kind": "inbox",
                "points": 3,
                "title": "Inspect the message",
                "diagram": "phishing-email",
                "body": "<p>You now know the tricks. The last skill is a calm routine "
                "for checking any message before you act on it, the same few places an "
                "investigator always looks. It takes seconds and it does not require "
                "any technical knowledge at all.</p>"
                "<p>Look first at the sender's real address, not the display name, "
                "because the friendly name is trivial to fake while the domain after "
                "the @ is much harder to. Look at any link by hovering your mouse over "
                "it, without clicking, to see where it truly leads, or on a phone by "
                "pressing and holding. Look for manufactured urgency and for a request "
                "that does not fit, like a change of bank details or a demand for a "
                "password. And notice a greeting that is oddly generic for someone who "
                "should know you.</p>"
                "<p>Any one of these can be innocent on its own. It is the pattern that "
                "matters. A lookalike sender plus a deadline plus a credential request "
                "is not three coincidences, it is a phish. Below is a message that has "
                "landed in the shared inbox. Read it the investigator's way and tap "
                "every part that should give you pause.</p>",
                "inline_check": {
                    "question": "What is the most reliable single thing to check on any suspicious email?",
                    "hint": "The friendly display name is easy to fake. What is much harder to fake?",
                    "options": [
                        ("The sender's real address, the domain after the @", True,
                         "Yes. The display name is trivial to fake, but the real domain is far harder, so it is the most reliable tell to check."),
                        ("Whether the email has a company logo", False,
                         "A logo is trivial to copy, so a perfect one proves nothing. Check the real sending domain instead."),
                        ("Whether it was sent in the morning", False,
                         "Timing tells you nothing about whether a message is genuine. The sending domain is what to check."),
                        ("How polite the wording is", False,
                         "Scammers can be perfectly polite. Politeness is not a safety signal; the real domain is what to inspect."),
                    ],
                },
                "body2": "<p>Keep that habit of checking the real address in mind as "
                "you work through the message below, and let the other tells, the "
                "deadline, the link, the odd greeting, confirm what the domain already "
                "hints at.</p>",
                "payload": {
                    "prompt": "This landed in the shared inbox. Tap every part that should give you pause. Find them all to finish.",
                    "avatar": "IT",
                    "parts": [
                        {"id": "from", "zone": "From",
                         "text": "IT Helpdesk <helpdesk@company-it-support.net>",
                         "bad": True,
                         "why": "A lookalike domain. Your real helpdesk would be on your own company domain, not company-it-support.net."},
                        {"id": "subject", "zone": "Subject",
                         "text": "Action required: mailbox will be deactivated in 24 hours",
                         "bad": True,
                         "why": "Manufactured urgency and a threat of losing your mailbox, designed to make you act before checking."},
                        {"id": "greeting", "zone": "Body",
                         "text": "Dear User,",
                         "bad": True,
                         "why": "A generic greeting from your own IT team, who would normally know your name, is a quiet tell."},
                        {"id": "reason", "zone": "Body",
                         "text": "We are upgrading the mail server this week.",
                         "bad": False,
                         "why": "On its own this is ordinary filler. The real tells are the sender, the deadline, the greeting and the link."},
                        {"id": "link", "zone": "Body",
                         "text": "Confirm your password here to keep your mailbox active: verify-mail-login.net",
                         "bad": True,
                         "why": "A request to confirm your password through an outside lookalike link. No genuine IT team ever asks for this."},
                    ],
                },
            },
            {
                "key": "verify",
                "kind": "check",
                "points": 2,
                "title": "Verify before you trust",
                "body": "<p>Inspecting a message tells you when to be suspicious. "
                "Verifying is what you do next, and it is the single most valuable habit "
                "in this whole module. The principle is one line: when a message asks "
                "you to do something that matters, confirm it through a separate channel "
                "you already trust, not through anything the message itself "
                "provides.</p>"
                "<p>The reason that phrasing is so careful is that a scammer always "
                "supplies their own path back to them: the link to click, the number to "
                "ring, the address to reply to. Every one of those leads to the "
                "attacker. So you deliberately ignore all of them. To check an invoice, "
                "you ring the supplier on the number from a past statement. To check a "
                "message from your bank, you use the number on your card. To check a "
                "request from a colleague, you walk over or call their known "
                "extension.</p>"
                "<p>This costs a minute and it feels almost rude the first few times, "
                "as though you are being distrustful. Reframe it: verifying important "
                "requests is simply what professionals do, and the people you contact "
                "will understand. A minute of checking is nothing against the cost of a "
                "redirected payment or a stolen login, and no genuine sender was ever "
                "harmed by being confirmed.</p>"
                "<div class=\"cy-callout\"><strong>The golden rule, in one line.</strong> "
                "Hover before you click, and verify on a channel you already trust "
                "before you act on anything that involves money, passwords or a change "
                "of details. If you remember nothing else from this module, remember "
                "that.</div>",
                "question": "The safest way to verify an unexpected request is to:",
                "hint": "Should you use the contact details the message gives you, or ones you already have?",
                "options": [
                    ("Confirm it through a separate channel you already trust, not the one the message provides", True,
                     "Yes. The message's own link or number leads back to the attacker, so verify using contact details you already hold."),
                    ("Reply to the message and ask if it is genuine", False,
                     "If it is a scam, that just asks the scammer, who will confirm it. Use an independent, trusted channel."),
                    ("Click the link to see where it goes", False,
                     "Clicking is the risk you are trying to avoid. Hover to inspect, and verify through a trusted channel instead."),
                    ("Trust it if it looks professional enough", False,
                     "A polished look is easy to fake and proves nothing. Verify the request through a channel you already trust."),
                ],
            },
            {
                "key": "report",
                "kind": "check",
                "points": 2,
                "title": "Report, do not just delete",
                "body": "<p>When you spot a phish, the instinct is to delete it and move "
                "on. Deleting protects only you, and only for a moment. Reporting "
                "protects everyone, because it lets the people who look after your "
                "systems warn colleagues, block the sender, and watch for anyone who "
                "did click.</p>"
                "<p>Reporting is easy and there is never any blame in it. Most workplaces "
                "want you to use the report button in your email program, or to forward "
                "the message to an internal address like your IT or security team, or "
                "simply to tell your manager. If you think you might have already clicked "
                "or replied, that is even more important to report quickly, not less. "
                "The staff who own up fast turn a near miss into a non-event, and good "
                "workplaces treat them as heroes, not culprits.</p>"
                "<p>Beyond your workplace, Australia has official places to report. "
                "Scams can be reported to Scamwatch, and cybercrime affecting you or "
                "your business can be reported through ReportCyber. You do not need to "
                "become an expert in either; the main habit is simply to tell someone "
                "rather than to quietly delete and hope.</p>"
                "<div class=\"cy-callout\"><strong>Why silence is the expensive "
                "option.</strong> If you delete a phish and say nothing, the colleague "
                "at the next desk, who is busier than you today, gets the same message "
                "with no warning. Thirty seconds of reporting is what stops one blocked "
                "attempt from becoming ten successful ones across the office.</div>",
                "question": "You spot and correctly identify a phishing email. What is the best thing to do with it?",
                "hint": "What action protects your colleagues, not just you?",
                "options": [
                    ("Report it, using the report button or by telling IT, so others can be protected", True,
                     "Yes. Reporting lets your team warn colleagues and block the sender. Deleting quietly protects only you, only for a moment."),
                    ("Just delete it and move on", False,
                     "Deleting protects only you, and the same message still reaches your colleagues with no warning. Report it."),
                    ("Reply to tell the scammer you are onto them", False,
                     "Replying confirms your address is live and invites more. Do not engage; report it instead."),
                    ("Forward it to all your colleagues as a warning", False,
                     "Well meant, but that spreads the live scam and any dangerous links. Report it through the proper channel instead."),
                ],
            },
            {
                "key": "technique-classify",
                "kind": "classify",
                "points": 3,
                "title": "Name the technique",
                "body": "<p>The final skill is recognition at a glance. When you can "
                "name what you are looking at, phishing, spear phishing, smishing or "
                "vishing, you respond faster and more calmly, and you describe it "
                "clearly when you report it.</p>"
                "<p>Below are several real-style approaches. For each one, name the "
                "technique. Remember the shorthand: a generic email to everyone is "
                "phishing, a tailored email using your real details is spear phishing, "
                "a scam text is smishing, and a scam phone call is vishing.</p>",
                "payload": {
                    "prompt": "Read each approach and name the technique. Get all six to finish.",
                    "categories": [
                        {"id": "phishing", "label": "Phishing"},
                        {"id": "spear", "label": "Spear phishing"},
                        {"id": "smishing", "label": "Smishing"},
                        {"id": "vishing", "label": "Vishing"},
                    ],
                    "events": [
                        {"id": "generic", "category": "phishing",
                         "text": "An email to 'Dear Customer' warning your mailbox is over quota, sent to thousands of addresses at once.",
                         "why": "Generic, mass, and impersonal. That is ordinary phishing."},
                        {"id": "targeted", "category": "spear",
                         "text": "An email using your name, your manager's name and the real project you are on, asking you to update a supplier's bank details.",
                         "why": "Personalised with real details about you and your work. That is spear phishing."},
                        {"id": "parcel", "category": "smishing",
                         "text": "A text message about a held parcel, asking you to pay a small fee at a lookalike link.",
                         "why": "A scam delivered by SMS is smishing."},
                        {"id": "atocall", "category": "vishing",
                         "text": "A phone call claiming to be the ATO, demanding immediate payment of a debt in gift cards.",
                         "why": "A scam delivered by voice call is vishing."},
                        {"id": "bankcall", "category": "vishing",
                         "text": "A caller says they are your bank's fraud team and asks you to confirm your login to secure the account.",
                         "why": "A scam phone call, even one that spoofs the bank's number, is vishing."},
                        {"id": "mygovtext", "category": "smishing",
                         "text": "A text says a myGov payment is waiting and links to my-gov-au-secure.com.",
                         "why": "A scam text with a lookalike link is smishing."},
                    ],
                },
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
        # ---- Lesson 1: social engineering foundations ----
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is social engineering?",
            "options": [
                ("Manipulating a person into doing something that helps the attacker", True,
                 "Yes. It targets human trust and judgement, which is often far easier than breaking the technology."),
                ("A method for building social media apps", False,
                 "No. Despite the name it has nothing to do with building software. It is a con aimed at people."),
                ("A type of antivirus", False,
                 "No. It is an attack technique, not a defence."),
                ("A way to make Wi-Fi faster", False,
                 "No. It is about tricking people, not networks or speed."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Why do attackers target people rather than only computers?",
            "options": [
                ("A person can be rushed and charmed, which is often far easier than breaking strong technology", True,
                 "Yes. Cracking a strong password can take ages; talking someone into giving it takes minutes."),
                ("Computers cannot be attacked at all", False,
                 "They can, but strong controls make it hard, so attackers aim at the person instead."),
                ("People have no part in security", False,
                 "The opposite. People are central, which is exactly why attackers target them."),
                ("It is illegal to attack computers but not people", False,
                 "Both are illegal. Attackers target people because it is often easier, not for legal reasons."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "A message that appears to come from your CEO and demands action in ten minutes is pulling which levers?",
            "options": [
                ("Authority and urgency", True,
                 "Yes. The apparent seniority is authority and the tight deadline is urgency, a combination engineered to stop you checking."),
                ("Curiosity and generosity", False,
                 "Not here. The standout levers are a senior figure (authority) and a hard deadline (urgency)."),
                ("Only fear", False,
                 "There may be a little fear, but the clearest pair is authority and urgency."),
                ("None, it is a normal request", False,
                 "A senior figure plus a sudden deadline is a classic pressure combination worth pausing on."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "When a message makes you feel a strong emotion like fear or urgency, that feeling is best treated as:",
            "options": [
                ("A prompt to slow down and check, because the emotion may be the attack working", True,
                 "Yes. Strong feeling is often the manipulation. Naming it and slowing down breaks its grip."),
                ("A sign the message must be genuine and urgent", False,
                 "No. Manufactured emotion is a red flag, not proof. Slow down rather than speed up."),
                ("A reason to act immediately", False,
                 "Acting fast is exactly what the attacker wants. The feeling is a cue to pause."),
                ("Something to ignore completely", False,
                 "Do not ignore it; use it. The emotion is a useful signal to check before acting."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "What is baiting?",
            "options": [
                ("Luring you with something tempting, like a found USB or a free prize, to make you act", True,
                 "Yes. Baiting exploits curiosity or greed by dangling a reward."),
                ("Threatening to close your account", False,
                 "That is fear and urgency. Baiting offers a reward rather than a threat."),
                ("Flooding a website with traffic", False,
                 "That is a DDoS. Baiting is a social trick that tempts you."),
                ("Guessing your password", False,
                 "No. Baiting lures you into an action, it does not guess credentials."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "You find a USB stick labelled 'Staff salaries' in the car park. What should you do?",
            "options": [
                ("Do not plug it in; hand it to your IT team", True,
                 "Yes. A tempting labelled USB is classic baiting. Plugging it in could install malware, so give it to IT."),
                ("Plug it in to find the owner", False,
                 "That is exactly the trap. The enticing label exists to make you plug it in and infect the machine."),
                ("Take it home and use it for your own files", False,
                 "Never use an unknown USB. It could carry malware. Hand it to IT instead."),
                ("Throw it in the bin so no one else finds it", False,
                 "Better to give it to IT, who can handle it safely and know an attempt was made."),
            ],
        },
        {
            "lesson": 1, "difficulty": "HARD",
            "text": "Why do intelligent, careful professionals still fall for social engineering?",
            "options": [
                ("Good attacks look routine and arrive when people are busy and acting on autopilot", True,
                 "Yes. It is not about intelligence. A con that fits the flow of a busy day is the one that catches careful people."),
                ("Only untrained people ever fall for it", False,
                 "Trained, experienced people are caught too, because the best attacks look completely normal."),
                ("It only affects people who are bad with technology", False,
                 "Being technical is little defence against a convincing human con."),
                ("Because they do not use email", False,
                 "The risk comes from handling many messages quickly, not from avoiding them."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "Which mindset keeps a person safest from social engineering?",
            "options": [
                ("Accepting anyone can be caught on a bad day, and building in a habit of checking", True,
                 "Yes. Humility plus a checking habit beats overconfidence. 'I would never fall for that' is itself a risk."),
                ("Being certain you are too smart to be tricked", False,
                 "That confidence is exactly what leaves people exposed. Anyone can be caught when rushed."),
                ("Assuming every message is genuine to save time", False,
                 "That is the opposite of safe. A habit of checking important requests is what protects you."),
                ("Never reading any messages", False,
                 "Not practical. The safe approach is to read but verify what matters."),
            ],
        },
        {
            "lesson": 1, "difficulty": "EASY",
            "text": "The lever an attacker pulls by posing as the tax office or a bank is:",
            "options": [
                ("Authority", True,
                 "Yes. Impersonating a powerful body leans on our tendency to comply with authority."),
                ("Curiosity", False,
                 "Curiosity is about tempting you to look. Posing as an official body is authority."),
                ("Generosity", False,
                 "Posing as an authority is not about generosity. It is the authority lever."),
                ("Boredom", False,
                 "That is not one of the levers. Impersonating an official body is authority."),
            ],
        },
        {
            "lesson": 1, "difficulty": "MEDIUM",
            "text": "An email subject reads 'You will not believe these leaked photos'. Which lever is this?",
            "options": [
                ("Curiosity", True,
                 "Yes. An irresistible tease that makes you want to look is the curiosity lever."),
                ("Authority", False,
                 "There is no figure of power here. The pull is your curiosity."),
                ("Fear", False,
                 "It is not threatening you. It is tempting you to look, which is curiosity."),
                ("Trust", False,
                 "It does not rely on a familiar name. It baits your curiosity."),
            ],
        },
        # ---- Lesson 2: phishing, spear, whaling ----
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "Ordinary mass phishing is best described as:",
            "options": [
                ("The same generic fake message sent to huge numbers of people at once", True,
                 "Yes. It is a wide net, generic and impersonal, hoping a small fraction bite."),
                ("A single message tailored to one specific person", False,
                 "That is spear phishing. Mass phishing is generic and sent widely."),
                ("A phone call from a scammer", False,
                 "That is vishing. Mass phishing arrives as a generic message to many people."),
                ("A genuine marketing email", False,
                 "No. Phishing is a fraudulent message designed to trick you, not legitimate marketing."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What most reliably reveals ordinary mass phishing?",
            "options": [
                ("It is generic, with no personal detail, because it went to a huge list", True,
                 "Yes. Mass phishing cannot personalise, so a generic greeting and lack of specific detail are the tells."),
                ("It addresses you by your full name and job title", False,
                 "That points to spear phishing. Mass phishing usually cannot use your name."),
                ("It comes from your bank's genuine address", False,
                 "It comes from a lookalike, not the genuine address."),
                ("It contains detailed, accurate information about your projects", False,
                 "That is spear phishing. Mass phishing is generic."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What makes spear phishing more dangerous than mass phishing?",
            "options": [
                ("It is personalised with real details, so the usual tells vanish and it reads as genuine", True,
                 "Yes. Real, specific detail makes it convincing and hard to spot."),
                ("It is sent to many more people", False,
                 "The opposite. Spear phishing targets one person or a small group."),
                ("It always has obvious spelling errors", False,
                 "No. A good spear phish is carefully written. Do not rely on spotting mistakes."),
                ("It can only be sent by post", False,
                 "It arrives digitally. The danger is the personalisation, not the channel."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "Where do attackers usually get the personal details for a spear phish?",
            "options": [
                ("From public sources like your website, social media and auto-replies", True,
                 "Yes. Most detail is already public. Attackers assemble harmless facts into a convincing message."),
                ("By first breaking into your computer", False,
                 "They rarely need to. Public information usually supplies enough."),
                ("They cannot get real details, so they guess", False,
                 "Guessing is mass phishing. Spear phishing uses genuine, easily found details."),
                ("From a secret database only criminals can access", False,
                 "No need for anything exotic. Public websites and social media supply most of it."),
            ],
        },
        {
            "lesson": 2, "difficulty": "EASY",
            "text": "An out-of-office reply can help an attacker because it may reveal:",
            "options": [
                ("Who to contact in your absence and details they can use to pose as you", True,
                 "Yes. It can hand over a colleague's name and a plausible reason to make contact."),
                ("Your exact password", False,
                 "An auto-reply does not contain your password, but it can reveal names and contacts useful for a con."),
                ("Nothing of any use to anyone", False,
                 "It can be a goldmine of names and context for a spear phish. Keep auto-replies brief."),
                ("The attacker's own identity", False,
                 "No. It reveals your details, not theirs."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "What is whaling?",
            "options": [
                ("Spear phishing aimed at senior people who can authorise money or access", True,
                 "Yes. Whaling targets the big fish, whose access or signing authority makes a single hit very valuable."),
                ("Phishing sent to as many people as possible", False,
                 "That is mass phishing. Whaling is targeted at high-value individuals."),
                ("A scam carried out only by text message", False,
                 "That is smishing. Whaling targets senior figures, usually by email."),
                ("A harmless internal newsletter", False,
                 "No. Whaling is a targeted attack on senior staff."),
            ],
        },
        {
            "lesson": 2, "difficulty": "HARD",
            "text": "An email from your 'managing director', who is travelling, urgently asks you to pay a new supplier and reply by email only. The safest response is to:",
            "options": [
                ("Verify on a separate known channel, such as ringing their real number, before doing anything", True,
                 "Yes. 'Reply by email only' exists to stop you checking. Verify independently, and a genuine leader will thank you."),
                ("Pay it immediately because the director asked", False,
                 "Seniority in an email is not proof, and urgency plus secrecy is a classic CEO-fraud pattern. Verify first."),
                ("Reply to the email to confirm it is really them", False,
                 "If the address is the attacker's, you are just asking the attacker. Use a separate trusted channel."),
                ("Ignore it entirely without checking", False,
                 "It might be genuine. The right move is to verify on a known channel, not to guess."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "'CEO fraud' or business email compromise typically stacks which pressures?",
            "options": [
                ("Authority, urgency and secrecy, so a junior person feels unable to question it", True,
                 "Yes. Posing as a leader, demanding speed, and asking to keep it quiet all work together to prevent checking."),
                ("Generosity and patience", False,
                 "The opposite. It relies on pressure and secrecy, not patience."),
                ("Curiosity about a prize", False,
                 "That is baiting. CEO fraud leans on authority and urgency around a payment."),
                ("A friendly, no-rush tone", False,
                 "It is usually urgent by design, to stop you verifying."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "A genuine invoice from a supplier you deal with monthly would usually:",
            "options": [
                ("Come from their known address, with the usual details and no sudden urgency", True,
                 "Yes. Consistency with past dealings and no pressure to change details is what a genuine invoice looks like."),
                ("Demand payment within the hour to a brand new account", False,
                 "A sudden deadline and a changed account are classic invoice-scam signs, not normal business."),
                ("Come from a free webmail lookalike address", False,
                 "A lookalike or webmail sender is a red flag, not a sign of a genuine supplier."),
                ("Insist you keep the payment secret", False,
                 "Secrecy around a payment is a warning sign, not normal for a routine invoice."),
            ],
        },
        {
            "lesson": 2, "difficulty": "MEDIUM",
            "text": "When triaging a mixed inbox, an email is most likely genuine when it:",
            "options": [
                ("Continues a real thread from a known contact, with no pressure or credential request", True,
                 "Yes. A familiar sender, an expected context, and no urgency or request for secrets all point to genuine."),
                ("Uses a lookalike domain and a two-hour deadline", False,
                 "Those are phishing tells, not signs of a genuine message."),
                ("Asks you to confirm your password via a link", False,
                 "No legitimate sender asks that. It is a phishing hallmark."),
                ("Comes from a senior name on a public webmail address, demanding secrecy", False,
                 "That is a whaling pattern, not a sign of a genuine email."),
            ],
        },
        # ---- Lesson 3: smishing, vishing, spoofing, pretexting ----
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What is smishing?",
            "options": [
                ("Phishing carried out by SMS text message", True,
                 "Yes. Smishing is a scam delivered by text, often about parcels, myGov or your bank."),
                ("Phishing carried out by phone call", False,
                 "That is vishing. Smishing is by text message."),
                ("A way of encrypting text messages", False,
                 "No. Smishing is an attack, not a protection."),
                ("A harmless promotional text", False,
                 "No. Smishing is a fraudulent text designed to trick you."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "You get an unexpected text about a held parcel with a link to pay a fee. Best move?",
            "options": [
                ("Do not tap the link; check via the carrier's official app or website", True,
                 "Yes. Go the front way. The link is the hook, so use the official channel instead."),
                ("Tap the link quickly before the parcel is returned", False,
                 "That deadline is the pressure the scam relies on. Do not tap the link."),
                ("Reply asking if it is genuine", False,
                 "Replying reaches the scammer. Check through the carrier's real channel."),
                ("Pay the fee to be safe", False,
                 "Never pay via a link in an unexpected text. Verify through the official channel first."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What is vishing?",
            "options": [
                ("Phishing carried out by voice, over a phone call", True,
                 "Yes. Vishing is a scam phone call, such as a fake ATO, bank or tech-support call."),
                ("Phishing carried out by email", False,
                 "That is ordinary phishing. Vishing is by phone call."),
                ("A voice-recognition login", False,
                 "No. Vishing is an attack, not a login method."),
                ("A type of voicemail greeting", False,
                 "No. Vishing is a fraudulent phone call designed to trick you."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "What single habit defeats almost every scam phone call?",
            "options": [
                ("Hang up and call back on a number you already trust", True,
                 "Yes. You cannot verify an incoming caller, so dialling a known number yourself ends the con."),
                ("Ask the caller to prove who they are", False,
                 "A practised scammer will rattle off convincing details. Call back on a known number instead."),
                ("Stay on the line and comply to be safe", False,
                 "Staying on the line is what they want. Hang up and verify independently."),
                ("Give a little information to test them", False,
                 "Any information helps them. Do not test them; hang up and call the organisation yourself."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "A caller claims to be from the ATO and demands payment of a debt in gift cards. This is:",
            "options": [
                ("A scam, because no genuine government body is ever paid in gift cards", True,
                 "Yes. The gift-card demand alone marks it as a scam. Hang up and verify with the ATO's real number."),
                ("Probably genuine, since it is the ATO", False,
                 "The ATO does not demand gift cards or threaten immediate arrest. This is a classic vishing scam."),
                ("Fine to pay if you are worried about arrest", False,
                 "The arrest threat is a scare tactic. No real body collects debts in gift cards. Do not pay."),
                ("Only a scam if the caller is rude", False,
                 "Politeness is irrelevant. The gift-card demand is the giveaway."),
            ],
        },
        {
            "lesson": 3, "difficulty": "HARD",
            "text": "A call displays your bank's real name and number on the screen. What does that prove?",
            "options": [
                ("Very little, because caller ID can be spoofed to show any number", True,
                 "Yes. The displayed number can be faked, so it is no proof. Hang up and call back on a trusted number."),
                ("That the call is definitely from your bank", False,
                 "No. Spoofing lets scammers display any number, including your bank's real one."),
                ("That your phone has been hacked", False,
                 "Spoofing does not require hacking your phone. It simply fakes the displayed number."),
                ("That you must comply with the caller", False,
                 "A matching number is not proof. Verify by calling back independently."),
            ],
        },
        {
            "lesson": 3, "difficulty": "EASY",
            "text": "What is pretexting?",
            "options": [
                ("Inventing a believable identity and scenario that makes a request feel normal", True,
                 "Yes. The pretext is the cover story, like posing as IT, that justifies the attacker's request."),
                ("Sending thousands of identical scam texts", False,
                 "That is smishing at scale. Pretexting is a tailored backstory to build trust."),
                ("Flooding a phone line with calls", False,
                 "That is a different attack. Pretexting is about a convincing invented story."),
                ("Encrypting files for ransom", False,
                 "That is ransomware. Pretexting is a social trick using a fabricated identity."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Someone calls posing as IT support and asks you to read out the code just texted to you. You should:",
            "options": [
                ("Refuse, and call IT back on a known number, because that code is your login", True,
                 "Yes. A one-time code is a key to your account. No genuine technician needs it, so verify independently."),
                ("Read it out, since IT is helping you", False,
                 "Never share a one-time code. A real technician would never ask, so this is the con."),
                ("Read it out only if they sound friendly", False,
                 "A warm manner is part of the act. Never share a code, however friendly the caller."),
                ("Text the code to the number they give you", False,
                 "That hands your login straight to the attacker. Do not share codes with anyone."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "Pretexting often succeeds by exploiting which everyday human trait?",
            "options": [
                ("Our willingness to be helpful", True,
                 "Yes. A plausible story plus our natural helpfulness makes an unreasonable request feel reasonable."),
                ("Our dislike of all strangers", False,
                 "If anything, suspicion would help. Pretexting exploits helpfulness and trust, not hostility."),
                ("Our ability to read minds", False,
                 "That is not a real trait. Pretexting works on ordinary helpfulness."),
                ("Our love of paperwork", False,
                 "No. It exploits the wish to be helpful and to solve the caller's apparent problem."),
            ],
        },
        {
            "lesson": 3, "difficulty": "MEDIUM",
            "text": "The common thread across scam emails, texts and calls is that the attacker:",
            "options": [
                ("Supplies the path to respond, the link or number, because it leads back to them", True,
                 "Yes. So the defence is to ignore their path and reach the organisation the way you already know."),
                ("Always reveals their real identity", False,
                 "They hide it. The tell is that the response path they give you leads back to them."),
                ("Never uses any urgency", False,
                 "Urgency is one of their favourite tools. The common thread is the response path they supply."),
                ("Only ever uses email", False,
                 "They use email, text and phone. The shared trait is the attacker-controlled path back."),
            ],
        },
        # ---- Lesson 4: inspect, verify, report, recognise ----
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "What is the most reliable single thing to check on a suspicious email?",
            "options": [
                ("The sender's real address, the domain after the @", True,
                 "Yes. The display name is trivial to fake, but the real domain is much harder, so it is the best tell."),
                ("Whether it has a company logo", False,
                 "A logo is easy to copy. A perfect one proves nothing; check the sending domain."),
                ("The time it was sent", False,
                 "Timing tells you nothing about legitimacy. The sending domain is what to check."),
                ("How polite the wording is", False,
                 "Scammers can be polite. Politeness is not a safety signal; inspect the real domain."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "How can you safely see where a link really leads before clicking?",
            "options": [
                ("Hover your mouse over it, or press and hold on a phone, to reveal the true address", True,
                 "Yes. Hovering shows the real destination without clicking, so you can check it against what is claimed."),
                ("Click it and see what happens", False,
                 "Clicking is the risk you are trying to avoid. Hover to inspect first."),
                ("Trust the text of the link exactly as shown", False,
                 "The visible text can differ from the real destination. Hover to see where it truly goes."),
                ("Forward it to a friend to click for you", False,
                 "That just puts someone else at risk. Hover to inspect it safely yourself."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "The safest way to verify an unexpected request is to:",
            "options": [
                ("Confirm it through a separate channel you already trust, not one the message provides", True,
                 "Yes. The message's own link or number leads back to the attacker. Use contact details you already hold."),
                ("Reply and ask whether it is genuine", False,
                 "If it is a scam, you are just asking the scammer. Use an independent trusted channel."),
                ("Click the link to check where it goes", False,
                 "Clicking is the risk. Verify through a separate trusted channel instead."),
                ("Trust it if it looks professional", False,
                 "Polish is easy to fake. Verify important requests through a channel you already trust."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "You spot and identify a phishing email at work. The best thing to do is:",
            "options": [
                ("Report it, via the report button or by telling IT, so colleagues can be protected", True,
                 "Yes. Reporting lets your team warn others and block the sender. Deleting quietly protects only you."),
                ("Just delete it and move on", False,
                 "Deleting protects only you, and the same message still reaches colleagues with no warning."),
                ("Reply to tell the scammer you spotted them", False,
                 "Replying confirms your address is live and invites more. Report it instead."),
                ("Forward it to the whole office as a warning", False,
                 "That spreads the live scam and its links. Report it through the proper channel."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "Why is reporting a phish better than just deleting it?",
            "options": [
                ("It lets your team warn colleagues and block the sender, protecting everyone", True,
                 "Yes. Deleting helps only you for a moment; reporting protects the whole office."),
                ("It makes your own inbox faster", False,
                 "Speed is not the point. Reporting protects colleagues who may get the same message."),
                ("It automatically arrests the scammer", False,
                 "It does not do that, but it does let your team warn others and block the sender."),
                ("There is no benefit; deleting is just as good", False,
                 "Deleting protects only you. Reporting stops the same attack reaching your colleagues."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "If you think you may have already clicked a phishing link or entered your password, you should:",
            "options": [
                ("Report it straight away so the account can be secured quickly", True,
                 "Yes. Fast reporting turns a near miss into a non-event. There is never blame for owning up early."),
                ("Say nothing and hope nothing happens", False,
                 "Silence lets a small problem grow. Report it fast so the account can be secured."),
                ("Delete the email so there is no record", False,
                 "Deleting the message does not undo a clicked link or entered password. Report it."),
                ("Wait a week to see if anything breaks", False,
                 "Waiting hands the attacker time. Report it immediately."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "A generic email to 'Dear Customer' sent to thousands of people at once is an example of:",
            "options": [
                ("Phishing", True,
                 "Yes. Generic, mass and impersonal is ordinary phishing."),
                ("Spear phishing", False,
                 "Spear phishing is personalised to a specific target. This is generic mass phishing."),
                ("Vishing", False,
                 "Vishing is a phone call. This is a mass email, so it is phishing."),
                ("Smishing", False,
                 "Smishing is a text message. This generic email is phishing."),
            ],
        },
        {
            "lesson": 4, "difficulty": "MEDIUM",
            "text": "An email using your name, your manager's name and your real project, asking you to change a supplier's bank details, is:",
            "options": [
                ("Spear phishing", True,
                 "Yes. Personalised with genuine details about you and your work, it is spear phishing."),
                ("Ordinary mass phishing", False,
                 "Mass phishing is generic. The real personal detail here makes it spear phishing."),
                ("Smishing", False,
                 "Smishing arrives by text. This is a targeted email, so it is spear phishing."),
                ("A harmless internal email", False,
                 "A request to change bank details, however personalised, should be verified. This pattern is spear phishing."),
            ],
        },
        {
            "lesson": 4, "difficulty": "EASY",
            "text": "A scam phone call claiming to be your bank's fraud team is an example of:",
            "options": [
                ("Vishing", True,
                 "Yes. A scam delivered by voice call is vishing, even if it spoofs the bank's number."),
                ("Phishing by email", False,
                 "This is a phone call, so it is vishing rather than email phishing."),
                ("Smishing", False,
                 "Smishing is by text. A phone call is vishing."),
                ("Baiting", False,
                 "Baiting lures with a reward. A scam call posing as your bank is vishing."),
            ],
        },
        {
            "lesson": 4, "difficulty": "HARD",
            "text": "Which single rule best protects you against the whole social engineering family?",
            "options": [
                ("For anything involving money, passwords or changed details, verify on a channel you already trust", True,
                 "Yes. Whatever the channel or technique, verifying important requests independently defeats the con."),
                ("Only open emails from people you know", False,
                 "Attackers impersonate people you know. Verifying the request, not just the name, is what protects you."),
                ("Trust any message that looks professional", False,
                 "Polish is easy to fake. Verification, not appearance, is the reliable defence."),
                ("Never use email, text or the phone", False,
                 "Not practical. The workable rule is to verify important requests through a trusted channel."),
            ],
        },
    ],
}
