"""Module 1 — Network Security Fundamentals: the real lesson content and quiz.

Content, not schema: kept as plain data so it reads like the teaching material it
is, and so the seed command stays re-runnable. Written in plain Australian
English for non-technical readers — small businesses, councils, schools.

LESSONS is four lesson bodies (HTML, sanitised on save). QUIZ is a 15-question
bank; ten are drawn per attempt. Every option carries an explanation_text — that
is what the Adaptive Feedback Engine reads back to the learner, so the wrong
options explain the misconception, not just "incorrect".
"""

# --------------------------------------------------------------------------
# Lessons
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network actually is",
        "reading_time_minutes": 4,
        "body": """
<p>Before we can protect a network, it helps to know what one actually is — in
everyday terms, with no jargon. A <strong>network</strong> is simply two or more
devices connected so they can share information. The laptop that talks to the
office printer, the phone that picks up email over Wi-Fi, the eftpos terminal
that reaches the bank — each of those is a small conversation between devices,
and the network is what carries it.</p>

<p>Your workplace network usually has a few familiar parts. There are the
<em>devices</em> people use: computers, phones, tablets, printers. There is a
<em>router</em> or modem, which is the box that connects your workplace to the
internet and passes messages between your devices. And there is the
<em>internet</em> itself — a vast, shared network of other networks that your
information travels across to reach a website, a supplier or a customer.</p>

<h2>Information is always in one of three states</h2>
<p>When we talk about keeping a network secure, it helps to picture where your
information is at any moment. It is either <strong>at rest</strong> (saved on a
device or a server), <strong>in transit</strong> (moving across the network to
somewhere else), or <strong>in use</strong> (open on a screen in front of
someone). Each state needs looking after. A customer list is exposed just as
easily by an email sent to the wrong person as by a stolen laptop.</p>

<h2>The three questions security is really asking</h2>
<p>Security people use a simple model called the <strong>CIA triad</strong>.
It has nothing to do with spies — the letters stand for
<strong>Confidentiality</strong>, <strong>Integrity</strong> and
<strong>Availability</strong>, and they are the three things we are trying to
protect. Almost every security decision comes back to one of them.</p>

<ul>
  <li><strong>Confidentiality</strong> — keeping information away from people who
  shouldn't see it. When you lock a filing cabinet or put a password on a
  spreadsheet of customer details, you are protecting confidentiality.</li>
  <li><strong>Integrity</strong> — making sure information is accurate and hasn't
  been changed without permission. If someone alters an invoice's bank details,
  the file still opens, but its integrity is gone — and that is how a lot of
  money goes missing.</li>
  <li><strong>Availability</strong> — making sure the information and systems are
  there when you need them. A backup you can actually restore protects
  availability; so does keeping your systems running rather than knocked offline
  by an attack.</li>
</ul>

<blockquote>A quick way to remember it: confidentiality is "only the right people
can see it", integrity is "it hasn't been tampered with", and availability is
"it works when I need it".</blockquote>

<h3>A everyday example</h3>
<p>Picture a small accounting practice. A spreadsheet of clients' tax file
numbers sits on the office computer. If a staff member emails that spreadsheet to
the wrong client, that's a <strong>confidentiality</strong> breach — the right
information reached the wrong person. If a scammer quietly edits a client's refund
account number, that's an <strong>integrity</strong> breach — the file looks fine
but now sends money astray. And if ransomware locks the computer the morning tax
returns are due, that's an <strong>availability</strong> breach — the information
still exists, but no one can reach it. Same office, same spreadsheet, three very
different failures. Naming which one you're worried about tells you what to do.</p>

<h3>Where your information lives</h3>
<table>
  <thead><tr><th>State</th><th>Everyday example</th></tr></thead>
  <tbody>
    <tr><td>At rest</td><td>A customer list saved on a laptop or server.</td></tr>
    <tr><td>In transit</td><td>That list attached to an email crossing the internet.</td></tr>
    <tr><td>In use</td><td>The list open on screen at a shared front desk.</td></tr>
  </tbody>
</table>
<p>Good security looks after all three. A locked laptop protects data at rest, but
it does nothing for a copy already emailed away — so we think about each state
rather than trusting a single lock.</p>

<h2>Why this matters for you</h2>
<p>You don't need to run the network to help keep it safe. Most real incidents
turn on an everyday choice — a link clicked, a password reused, a file shared a
little too widely. When you can name what you're protecting, the everyday choices
get easier. If an email would expose customer details, that's a confidentiality
question. If a request would change where money is sent, that's an integrity
question. If losing a file would stop work for a day, that's an availability
question.</p>

<p>None of this requires technical training. It's a way of thinking: whenever
you're unsure about a request or a task, ask which of the three it touches, and
the sensible response usually becomes obvious. A shop assistant who wouldn't leave
the till drawer open on the counter already understands confidentiality and
availability in the physical world — the same instincts carry straight across to
information, once you know what to look for.</p>

<p>In the next lesson we'll look at where networks are most often exposed — the
weak points attackers actually use — and why the biggest one isn't a machine at
all.</p>
""",
    },
    {
        "title": "Where the weak points are",
        "reading_time_minutes": 4,
        "body": """
<p>Attackers are not magicians. They rarely "break in" through some clever
technical feat. Far more often they walk in through a door someone left open —
a weak password, an out-of-date program, or a person having a busy day. The ways
in are called <strong>attack vectors</strong>, and the good news is that the
common ones are few, well understood, and mostly preventable.</p>

<h2>The common ways in</h2>
<ul>
  <li><strong>Phishing</strong> — a message that pretends to be from someone you
  trust (a bank, a supplier, your own IT team) to trick you into clicking a link,
  opening a file, or handing over a password. This is the single most common way
  organisations are attacked.</li>
  <li><strong>Weak or reused passwords</strong> — if the same password protects
  your email and a dozen other sites, then one leaked site hands an attacker the
  lot. Attackers routinely try passwords stolen from one place against every
  other place they can find.</li>
  <li><strong>Out-of-date software</strong> — programs get security fixes for a
  reason: someone found a hole. Until you install the update, that hole is open,
  and attackers actively scan for machines that haven't patched.</li>
  <li><strong>Malware</strong> — harmful software that sneaks onto a device,
  usually through a dodgy attachment, download or link. <em>Ransomware</em>, which
  locks up your files and demands payment, is a kind of malware.</li>
  <li><strong>Unsafe networks</strong> — free public Wi-Fi at a café or airport
  is convenient, but you can't be sure who else is on it or what they can see.</li>
</ul>

<h2>The biggest weak point isn't a machine</h2>
<p>If you remember one thing from this module, make it this:
<strong>human error is the biggest risk of all</strong>. Study after study — in
Australia and worldwide — finds that the large majority of security incidents
involve a person doing something entirely ordinary: clicking a link that looked
genuine, reusing a password, sending a file to the wrong address, or approving a
payment because the email seemed urgent.</p>

<p>This is not a reason to feel guilty, and it is certainly not a reason to
distrust your team. It is simply where the leverage is. A firewall can't stop you
from typing your password into a convincing fake page. Antivirus can't un-send an
email. But <em>you</em> can pause when something feels rushed, and that single
habit prevents more harm than any product.</p>

<blockquote>Attackers rely on urgency. "Act now or your account is closed."
"Pay this invoice today." The pressure is deliberate — it exists to stop you
thinking. Slowing down is a security control.</blockquote>

<h3>A closer look at ransomware</h3>
<p>Ransomware deserves a special mention because it's behind many of the worst
days Australian organisations have. It usually arrives the same ordinary way — a
booby-trapped attachment or link — and once it runs it encrypts your files and
demands payment for the key. Paying is no guarantee of getting anything back, and
it marks you as willing to pay again. The genuine defence isn't heroics on the
day; it's the boring habits set up beforehand: current backups you've tested,
prompt updates, and staff who pause before opening the unexpected. An organisation
with a good backup can often restore and carry on rather than negotiate.</p>

<h3>Why updates close the door</h3>
<p>It's worth understanding <em>why</em> updates matter so much. When a company
releases a security update, it is effectively announcing "here is a hole we've
just fixed". Attackers read those announcements too, and immediately go looking
for machines that haven't applied the fix yet. So the gap between an update being
available and you installing it is exactly the window attackers aim for. Turning
on automatic updates shrinks that window to almost nothing, which is why it's one
of the highest-value habits in this whole course.</p>

<h2>Why attackers target smaller organisations</h2>
<p>Small businesses, local councils and schools sometimes assume they're too
small to be a target. The opposite is true. Attackers use automated tools that
knock on thousands of doors at once; they aren't choosing you personally, they're
finding whichever door is unlocked. Smaller organisations are attractive precisely
because they often have valuable information and fewer defences than a large
corporation.</p>

<p>Notice, too, that these weak points stack up. An attacker who sends a phishing
email is hoping you also reused a password, or haven't updated, or won't check
before you click. That's why good security is layered: no single habit has to be
perfect, because the next one catches what the last one missed. If a phishing
email slips past you but two-factor authentication stops the stolen password from
working, the attack still fails. You don't need a wall without a single crack —
you need enough overlapping habits that one lapse isn't a disaster.</p>

<p>The pattern across all of these is the same: a small, sensible habit closes the
gap. Strong, unique passwords. Prompt updates. A moment's pause before acting on an
unexpected message. In the next lesson we'll look at the piece of equipment that
sits between your workplace and the whole internet — the router — and how to shut
its most common weak points.</p>
""",
    },
    {
        "title": "Wi-Fi, routers and the front door",
        "reading_time_minutes": 4,
        "body": """
<p>If your network were a building, the <strong>router</strong> would be the front
door. It's the box (sometimes called a modem or gateway) that connects everything
in your workplace to the internet. Almost all of your information passes through
it, which makes it one of the most important things to set up properly — and one
of the most commonly neglected.</p>

<h2>Change the default passwords — both of them</h2>
<p>A new router usually arrives with two passwords, and people often confuse them:</p>
<ul>
  <li>The <strong>Wi-Fi password</strong>, which people type to join the wireless
  network.</li>
  <li>The <strong>admin password</strong>, which is used to log in and change the
  router's own settings.</li>
</ul>
<p>Both matter. The admin password is the one people forget exists, and it's the
dangerous one to leave on the factory default — the defaults for most models are
published online, so anyone who reaches the router can take it over. Change both
to strong, unique passwords when the device is first set up.</p>

<h2>Use modern Wi-Fi encryption</h2>
<p>Encryption scrambles the information travelling over your Wi-Fi so that someone
nearby can't simply read it out of the air. On the router's settings you'll see
options like WPA3 or WPA2 — choose the most recent one your equipment supports.
Avoid the old "WEP" setting if you ever see it; it's long broken and can be
cracked in minutes with freely available tools. This is a one-time setting that
quietly protects every device on the network, so it's well worth getting right
when the router is first switched on.</p>

<h2>Offer a guest network</h2>
<p>Most routers can run a separate <strong>guest network</strong>. It's exactly
what it sounds like: a second Wi-Fi name for visitors, contractors and personal
phones, kept apart from the network your work devices use. If a visitor's phone is
infected, a guest network keeps that problem away from your business systems. It
also means you're not handing out the password to your main network to everyone
who drops by.</p>

<blockquote>A useful rule: the devices that hold your work belong on one network,
and everything else — guests, personal phones, smart gadgets — belongs on the
guest network.</blockquote>

<h2>Keep the router itself updated</h2>
<p>A router is a small computer, and like any computer it receives security
updates (its "firmware"). Many modern routers update themselves automatically; it
is worth confirming that yours does, because an unpatched router is a weak point
that sits in front of everything else. If your router is very old and no longer
receives updates from the manufacturer, replacing it is one of the most
worthwhile security purchases a small organisation can make.</p>

<h2>Mind the smart gadgets</h2>
<p>Modern workplaces quietly fill up with internet-connected devices beyond the
obvious computers and phones — smart TVs in the meeting room, a wireless security
camera, a printer that emails scans, even a smart kettle in the kitchen. Each of
these is a small computer on your network, and each is a potential weak point,
especially the cheaper ones that rarely receive updates. The guest network earns
its keep here too: putting these gadgets on the guest network, away from the
machines that hold your work, limits the harm if one of them is compromised. You
don't need to fear them — just don't let an unattended smart device share a
network with your customer records.</p>

<h2>A word on public Wi-Fi</h2>
<p>The front-door idea works away from the office too. On public Wi-Fi at a café,
hotel or airport, you don't control the network and can't be sure who else is on
it. Avoid doing sensitive work — banking, logging into work systems — over it. If
you must, use your phone's mobile connection or a trusted VPN instead. A VPN
creates a private, encrypted tunnel through the untrusted network, so even if
someone is listening, all they see is scrambled traffic. Treat any network you
don't control as a public space: fine for reading the news, not for your payroll.</p>

<h2>Know what's connected, and where the box sits</h2>
<p>Two small habits round out the router. First, every so often, take a look at
what's connected to your network — most routers list the current devices in their
settings. If you spot something you don't recognise, that's worth asking about.
You can't protect what you don't know is there, and a quick glance now and then
keeps surprises to a minimum. Second, give a thought to where the router
physically lives. In a shared or public-facing space — a café counter, a
reception desk — a router within arm's reach can be reset or tampered with by
anyone. Tucking it somewhere staff-only removes an easy opportunity, the same way
you'd keep the till or the keys out of a customer's reach.</p>

<p>Set the router up well and you've closed a whole category of risk before it
starts. In the last lesson we'll pull everything together into a short checklist
you can actually use.</p>
""",
    },
    {
        "title": "A simple security checklist",
        "reading_time_minutes": 3,
        "body": """
<p>You've now met the big ideas: what a network is, the three things we protect
(confidentiality, integrity and availability), where the common weak points are,
and why a calm human is the best defence of all. This last lesson turns that into
a short, practical checklist — the handful of habits that prevent the great
majority of problems.</p>

<h2>The everyday habits</h2>
<ul>
  <li><strong>Pause before you act on an unexpected message.</strong> Urgency is
  the attacker's favourite tool. If a message pushes you to hurry, that's your cue
  to slow down and check.</li>
  <li><strong>Verify money and detail changes another way.</strong> If an email
  asks you to change bank details or pay an unexpected invoice, confirm by phoning
  a number you already have — not one from the message.</li>
  <li><strong>Use strong, unique passwords, helped by a password manager.</strong>
  You don't have to remember them all; that's the tool's job. The point is that no
  two accounts share a password.</li>
  <li><strong>Turn on two-factor authentication</strong> wherever it's offered,
  especially on email. It means a stolen password alone isn't enough to get in.</li>
  <li><strong>Install updates promptly</strong> on your devices, apps and router.
  Most can be set to update automatically — let them.</li>
  <li><strong>Keep good backups</strong> of anything you couldn't bear to lose, and
  check now and then that you can actually restore them. That's your safety net
  against ransomware and simple mistakes alike.</li>
</ul>

<h2>Map it back to what you're protecting</h2>
<p>Each habit protects one of the three things from the first lesson. Strong
passwords and two-factor protect <strong>confidentiality</strong>. Verifying a
change of bank details protects <strong>integrity</strong>. Backups protect
<strong>availability</strong>. When you can see <em>why</em> a habit matters, it's
far easier to keep.</p>

<blockquote>Security isn't a product you buy once. It's a set of small, repeatable
habits — and none of them require you to be technical.</blockquote>

<h3>Make the habits easy to keep</h3>
<p>A habit only helps if it survives a busy week, so lean on tools that do the
remembering for you. A password manager generates and stores a different strong
password for every account, so the only thing you memorise is the one password
that opens the manager. Automatic updates mean you never have to decide to patch —
it simply happens. Automatic cloud or external-drive backups run without anyone
choosing to start them. The theme is the same throughout: set it up once so that
staying safe becomes the default rather than a daily decision. Security that
depends on everyone being perfect every day will fail; security built into the
routine holds up.</p>

<h3>Share it with your team</h3>
<p>These habits work best when everyone shares them, because an attacker only
needs one unlocked door. It's worth a short conversation with colleagues: agree
that nobody will be blamed for reporting a mistake, that unexpected payment
requests are always verified by phone, and that it's normal — expected, even — to
pause and check. A workplace where people feel safe to say "I think I clicked
something" is far more secure than one where fear keeps problems hidden until
they're expensive.</p>

<h2>If something does go wrong</h2>
<p>Even careful people have off days. If you think you've clicked something you
shouldn't have, or entered a password into a suspicious page, the most important
thing is to <strong>say so quickly</strong>. Tell whoever looks after your IT, or
your manager, straight away. Fast reporting is what turns a near-miss into a
non-event; staying quiet out of embarrassment is what lets a small problem grow.
There is never trouble for reporting — only for hiding it.</p>

<h2>Start with one thing</h2>
<p>If a six-point list feels like a lot at once, don't try to do everything today.
Pick the single habit that would help you most and start there. For many people
that's turning on two-factor authentication for their email, because email is the
account attackers most want — it's the key that resets all the others. For others
it's finally setting up a password manager, or switching on automatic updates and
never thinking about patching again. Momentum matters more than perfection: one
habit firmly in place beats six half-remembered ones. Once the first is second
nature, add the next.</p>

<p>It also helps to know you're not alone in this. In Australia, free guidance for
small organisations is available from the Australian Cyber Security Centre, and
genuine scams can be reported through Scamwatch. Knowing where to turn takes some
of the worry out of it — you don't have to have every answer yourself, you just
have to know that help exists and be willing to ask.</p>

<p>That's the foundation. You now know what a network is, what you're protecting,
where the risks are, and the habits that keep them at bay. When you're ready, take
the module quiz to lock it in — and remember, there's no timer and you can retake
it if you need to.</p>
""",
    },
]


# --------------------------------------------------------------------------
# Quiz — a 15-question bank; ten drawn per attempt.
# Each question names the lesson it comes from (1-based, into LESSONS above) so
# the Adaptive Feedback Engine can trace a mistake back to the right lesson.
# Options: exactly one correct; every option carries an explanation.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "In plain terms, what is a computer network?",
            "options": [
                ("Two or more devices connected so they can share information", True,
                 "Correct — a network is just devices connected to share information, from two machines to the whole internet."),
                ("A single computer with a fast processor", False,
                 "No — one computer on its own isn't a network; a network is about devices being connected to each other."),
                ("A type of antivirus program", False,
                 "No — antivirus is software that protects a device; it isn't what a network is."),
                ("The password you use to log in", False,
                 "No — a password protects access, but it isn't the network itself."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "What do the letters in the 'CIA triad' stand for?",
            "options": [
                ("Confidentiality, Integrity and Availability", True,
                 "Correct — these are the three things security protects, and most decisions come back to one of them."),
                ("Computers, Internet and Applications", False,
                 "No — the triad is about what we protect, not a list of equipment."),
                ("Control, Inspection and Access", False,
                 "No — these sound plausible but aren't the triad; it's Confidentiality, Integrity and Availability."),
                ("Confidential Intelligence Agency", False,
                 "No — despite the initials, the CIA triad has nothing to do with spy agencies."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "An invoice's bank details are secretly changed so payment goes to a stranger. Which part of the CIA triad has failed?",
            "options": [
                ("Integrity — the information was altered without permission", True,
                 "Correct — the file still opens, but its accuracy is gone; that's an integrity failure, and a common way money is stolen."),
                ("Availability — the file can't be opened", False,
                 "No — availability is about whether you can access something; here the file opens fine, it's just been tampered with."),
                ("Confidentiality — someone saw information they shouldn't", False,
                 "Not quite — the problem isn't who saw it, it's that the details were changed. That's integrity."),
                ("None of them — this isn't a security issue", False,
                 "No — altering financial details without permission is very much a security issue: a failure of integrity."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "Keeping a restorable backup of your files mainly protects which part of the CIA triad?",
            "options": [
                ("Availability — you can still get your information when you need it", True,
                 "Correct — backups mean an attack or mistake doesn't cost you access to your information; that's availability."),
                ("Confidentiality — it hides the files from others", False,
                 "No — a backup doesn't hide anything; it ensures you can still get your data back. That's availability."),
                ("Integrity — it proves the files weren't changed", False,
                 "Not the main point — backups are chiefly about being able to restore access, which is availability."),
                ("Backups aren't related to security at all", False,
                 "No — backups are a core security control; they protect availability against ransomware and mistakes."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "EASY",
            "text": "What is 'phishing'?",
            "options": [
                ("A message pretending to be from someone you trust, to trick you into clicking or sharing details", True,
                 "Correct — phishing impersonates a trusted sender and is the most common way organisations are attacked."),
                ("A way of speeding up your internet connection", False,
                 "No — phishing has nothing to do with connection speed; it's a form of deception."),
                ("A tool that backs up your files", False,
                 "No — that's a backup; phishing is a scam message designed to trick you."),
                ("A setting on your router", False,
                 "No — phishing is a type of attack delivered by message, not a router setting."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "According to this module, what is the single biggest security risk?",
            "options": [
                ("Human error — everyday mistakes like clicking a link or reusing a password", True,
                 "Correct — most incidents involve an ordinary human action, which is why calm habits matter more than any product."),
                ("Old printers", False,
                 "No — while any device can be a weak point, the biggest risk overall is human error."),
                ("Having too many backups", False,
                 "No — backups are a good thing; they're never the risk."),
                ("Using a router at all", False,
                 "No — routers are essential; the biggest risk is everyday human error, not the equipment."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "Why is reusing the same password across many sites dangerous?",
            "options": [
                ("If one site is breached, attackers try that password everywhere else", True,
                 "Correct — a single leak then unlocks all your accounts; unique passwords contain the damage."),
                ("It makes websites load more slowly", False,
                 "No — password reuse has no effect on speed; the danger is that one leak unlocks everything."),
                ("It uses up storage on your device", False,
                 "No — passwords don't take meaningful storage; the risk is that a single breach spreads."),
                ("There's no real danger if the password is long", False,
                 "No — even a long password is dangerous if reused, because one breached site exposes it everywhere."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "HARD",
            "text": "An email says 'Pay this overdue invoice in the next hour or the account will be closed.' What's the safest first step?",
            "options": [
                ("Pause, and verify the request using contact details you already have", True,
                 "Correct — urgency is a pressure tactic. Slowing down and confirming another way is the safest move."),
                ("Pay immediately so the account isn't closed", False,
                 "No — acting fast is exactly what the attacker wants; the deadline exists to stop you thinking."),
                ("Reply to the email asking if it's genuine", False,
                 "Risky — if it's a scam, you're just asking the attacker, who will say yes. Verify through a channel you trust."),
                ("Click the link to see the invoice details", False,
                 "No — clicking an unexpected link is how many attacks begin; verify before you click anything."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "Why do attackers often target small businesses, councils and schools?",
            "options": [
                ("Automated tools look for any unlocked door, and smaller organisations often have fewer defences", True,
                 "Correct — attacks are largely automated and opportunistic; being small doesn't mean being safe."),
                ("They are too small to be worth attacking", False,
                 "No — this is the dangerous myth; smaller organisations are targeted precisely because defences are often lighter."),
                ("They never hold any valuable information", False,
                 "No — they hold plenty of valuable data, from customer details to payment information."),
                ("Attackers personally choose each victim by name", False,
                 "No — most attacks are automated and untargeted, knocking on thousands of doors at once."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "On a new router, which password is the dangerous one to leave on the factory default?",
            "options": [
                ("The admin password used to change the router's settings", True,
                 "Correct — default admin passwords are published online, so leaving it unchanged lets anyone take the router over."),
                ("The Wi-Fi password guests use to connect", False,
                 "Partly — you should change this too, but the admin password is the critical one people forget exists."),
                ("Your email password", False,
                 "No — your email password isn't set on the router; the risky default here is the router's admin password."),
                ("Neither needs changing if the box is new", False,
                 "No — both should be changed, and the admin password especially, because its defaults are publicly known."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "EASY",
            "text": "What is the main benefit of a separate 'guest' Wi-Fi network?",
            "options": [
                ("It keeps visitors' and personal devices apart from your work devices", True,
                 "Correct — if a guest device is infected, a guest network keeps that problem away from your business systems."),
                ("It makes your internet twice as fast", False,
                 "No — a guest network is about separation and safety, not speed."),
                ("It removes the need for any passwords", False,
                 "No — a guest network still uses a password; it simply separates guests from your main network."),
                ("It automatically backs up guest files", False,
                 "No — a guest network doesn't back anything up; its purpose is to keep guest devices separate."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "When setting Wi-Fi encryption, which should you choose?",
            "options": [
                ("The most recent option your equipment supports, such as WPA3 or WPA2", True,
                 "Correct — modern encryption protects everything on the network; pick the newest your gear supports."),
                ("The oldest option, WEP, for compatibility", False,
                 "No — WEP is long broken and should be avoided; choose WPA2 or WPA3 instead."),
                ("No encryption, to keep things simple", False,
                 "No — an open network lets anyone nearby read your traffic; always use modern encryption."),
                ("It doesn't matter which you choose", False,
                 "No — it matters a great deal; older schemes like WEP are insecure, so pick the newest available."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "HARD",
            "text": "You need to log in to a work system while on free café Wi-Fi. What's the safest choice?",
            "options": [
                ("Use your phone's mobile connection or a trusted VPN instead", True,
                 "Correct — on a network you don't control, use mobile data or a trusted VPN for anything sensitive."),
                ("Go ahead — café Wi-Fi is always safe", False,
                 "No — you can't be sure who else is on public Wi-Fi or what they can see; treat it as a public space."),
                ("Just make sure the café is busy", False,
                 "No — how many customers there are tells you nothing about whether the network is safe."),
                ("Turn off your screen brightness so no one can see", False,
                 "No — the risk is the network carrying your data, not someone reading your screen."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "EASY",
            "text": "What does turning on two-factor authentication achieve?",
            "options": [
                ("A stolen password alone is no longer enough to get into the account", True,
                 "Correct — two-factor adds a second check, so a leaked password by itself won't let an attacker in."),
                ("It makes your password impossible to steal", False,
                 "No — it doesn't stop a password being stolen; it makes a stolen password insufficient on its own."),
                ("It removes the need for a password entirely", False,
                 "No — two-factor works alongside your password, adding a second step rather than replacing it."),
                ("It backs up your account", False,
                 "No — two-factor is about verifying it's really you; it isn't a backup."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "MEDIUM",
            "text": "You realise you may have entered your password into a suspicious page. What's the best thing to do?",
            "options": [
                ("Report it straight away to whoever looks after your IT or your manager", True,
                 "Correct — fast reporting turns a near-miss into a non-event; there's never trouble for reporting, only for hiding it."),
                ("Say nothing and hope nothing happens", False,
                 "No — staying quiet lets a small problem grow; quick reporting is what limits the damage."),
                ("Delete the email and carry on as normal", False,
                 "No — deleting the message doesn't undo an entered password; you need to report it so the account can be secured."),
                ("Wait a week to see if anything goes wrong", False,
                 "No — waiting gives an attacker time; report it immediately so action can be taken."),
            ],
        },
    ],
}
