# ballroompro
A Ballroom Competition Platform for all the parties involved in the organization and the running of the event.

**Projet component outline:**
Competitor side:
-	Account registration that will be remembered (username & password that can be used across competitions)
-	Signing up for competitions (choosing a competition from the list of available, choosing the desired level (bronze, silver etc.) and styles to compete in (jive, cha cha etc.)
o	Selecting a partner and sending an invite to them that they can confirm for the registration of a couple to be confirmed

Organizer side:
-	Creating new competitions, selecting which levels and styles are available
-	Approving that a heat has finished and progressing onto the next one
-	After the competition has been finished, getting back a list of results

Judge side:
-	A mobile platform to get insight into the ongoing heat, see all the competitors participating and selecting ones to be promoted

Server side:
-	Confirming registration of couples, adding them to the list of competitors for select level/style combinations
-	Sorting competitors into heats (if a level/style has e.g. 24 participants and only 8 can dance at one time, they should be sorted into heats of 8 or whatever number that works best so that every heat has an approximately equal number of competitors)
-	Starting a heat, collecting the information from the judges
o	Once the rankings from the judges have been collected, first summarizing all the results to determine which dancers have moved to the following heat
o	Then, giving the organizer a green light to approve the heat and move onto the next one
-	After all the heats have been finished, summarizing the results in a spreadsheet format or some other

Observer side:
-	A screen showing the current and upcoming heats and the competitors in each of them, so that the competitors know if they have moved onto the next round.

**Initially chosen computational tasks:**
1.	Creating a system for the organizer to create competitions (through a server database of competitions and some system of classes that can be instantiated as competitions)
2.	Creating a system for a competitor to register through
a.	Some system of account registration (to be researched? Not expecting any breakthroughs in the encryption of user details, just a simple system)
b.	Registering through competitions and being added to the database of competitors as a subclass of the class of the competition
3.	Creating a system of automatically sorting into heats once the organizer grants approval (based on the registration closing)


