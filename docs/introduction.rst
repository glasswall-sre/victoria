Introduction
============
Victoria is a generic command-line interface (CLI) written in Python.
On its own it doesn't come with very much, but its power mainly comes from
the ability to write plugins for it.

You can write a plugin CLI to do any number of tasks and put it in a Python
package, then a user can install the package and Victoria will dynamically
load the plugin and execute it when the user calls it via the CLI.

For example, say you find youself having to manually download data from blob
storage somewhere and run a script on it to look at the data, perhaps extracting
some important features from it. Your process for this before was to manually
browse to the blob storage and download the data in an archive, then extract
the archive and run a bespoke script to analyse the data.

This bespoke script requires a bunch of configuration values that tend to change
a lot as the data grows more complex, and lots of members of your team need to
use it, so you have to share the config around and make sure everyone is
synced up with all the changes.

Not only this, but sometimes the data needs to be analysed very quickly, in
time-sensitive situations. It's a situation that is rife with the risk for
human error.

If this situation is in any way familiar to you, then Victoria may be useful
for you.

With Victoria, you could write a plugin that wraps up the script functionality
as well as grabbing the data from blob storage. You could version the script
with the config, allowing your team to install/update your tools
quickly and deterministically. You could even store different configs in
cloud storage (including with encrypted secret values), and Victoria will
use the remote configs transparently to the user.

Backstory
---------
Victoria was developed by Glasswall_'s SRE_ team. We're responsible for
running a SaaS email platform for our customers that has very specific 
reliability requirements. We're on-call 24/7 in case something goes wrong with 
the system, and when something does go wrong we have to figure out what's gone 
wrong and solve it as fast as we can with minimal customer impact.

As a team, we're fairly young. We were formed in August 2019, and a lot of our
work to support the system then was exploratory and highly manual. In Google's
SRE book, this work is called toil_.

We had a 
process in place to identify manual work that was taking us too much time and
had a high risk of human error, and when we identified this work we wrote
various bespoke scripts that we could run to do certain things. Examples
included rebuilding corrupted email data, replaying dead letters, analysing
customer usage for capacity planning, redeploying masses of microservices at
once, and many many more.

Eventually, we had too many of these scripts and it was starting to get
unwieldy sharing them around and ensuring the config was correct. Work started
to find a solution to this problem, and Victoria was born.

We're now looking to put Victoria in the cloud in a serverless environment so
we can use it as a chat bot. Watch this space!

Why is it called Victoria?
--------------------------
It's an acronym! It stands for:

- Very
- Important
- Commands for
- Toil
- Optimisation:
- Reducing
- Inessential
- Activities

We do not wish to comment on how much work went into coming up with the name.

.. _Glasswall: https://glasswallsolutions.com/
.. _SRE: https://sre.glasswallsolutions.com/
.. _toil: https://landing.google.com/sre/sre-book/chapters/eliminating-toil/