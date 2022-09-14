09/10/22

Today I will be working on the achievement collection page.

Doing
 - Add and implement back button for achievement collection page

Done
 - Put all achievement collections in a scroll area. 
 - Connect achievement collection page to its button.

Keep in mind to always type out the entire unfamiliar code for practicing instead 
of simply copying or auto complete the code.
I am contemplating whether to put every page in the main windows as a stack
or to put each subpage under their parent pages. The advantage of the first
is it is easier to see all the pages at once, but then it is hard to see the
hierarchy of the pages.

09/08/22

Doing Today:
 - Put classes and functions in separate files and make it work.

09/07/22

The program is becoming increasingly hard to manage, maybe I should separate 
classes and functions to different files.

09/05/22

Although I heard some people said the best practice is to commit one thing
at a time, I found it hard to follow because almost every part of this program 
are interconnected, and it is difficult to only do one part at the time. 
I suppose it is better to just keep the standard in mind and do it in my own way.

To Do: 
    - Make sub window replace old window with animation stretch from top right,
and hide the old window.

09/01/22

Objective: Completion of Achievement pages implementation.
Task:
   - Windows behavior: 
     - close when tap outside.
     - toggle window with button.
   - Improve create new achievement page appearance.
   - Create achievement button class to show title, summary, and progress.
   - Create achievement info page when current achievement button clicked.
     - edit button
     - delete button
     - modify progress function
     - complete button
   - Create all achievement page
   
Just an idea for other part of the program, I can let the user turn on
or off the utilities they don't want and change the theme to light, system, and dark.

Question:
   - Do I need setting buttons for achievement page?

08/31/22

I probably should start to think about how to package the code to be the real app.

Stuff Done Today:
- Add setting and user button at the end of menus to have better measure of the
size of the menus.
- Rework achievement menu: add scroll area for achievement buttons
- Add achievement page skeleton

I think it is good timing to set a road mark for this project.
I would say completion of achievement pages and functions would be a good one.
I will rule out exactly what to do to achieve it tomorrow.

08/30/22

It is important to plan what to do and record how much I have done
and the problems I encountered and solved for future reference so I will 
start doing it from now on.
Stuff To Do Today:
   - Draw Icons
   - Add create new achievement page
Stuff Done Today:
   - Draw trophy icon for achievement, might change to star o6r star medal.
   - Have a slide in page for creating new achievement interface
Problems solved today:
   - I had trouble setting layout that contains buttons onto the panel
widget because the background buttons disappears, but it appears to be
because of panel's stylesheet is inline which makes it later than the
button's style sheet being set from stylesheet file. So I changed panel's
stylesheet to read from the file and it worked.

I probably should stop when I feel bad to continue doing something, especially
those things that I actually like myself to do because I don't want to feel 
stressed doing them.

I also need to commit more frequently.

08/28/22

Two days ago I fixed the display of the app window, and added some buttons for the utilities along with
some temporary image to represent each utilities which will be replaced by the proper one I will need to 
draw later. The next thing to that is to change the font, and it spent me two days to figure out how to
do it. The first thing I tried is to use stylesheet, which I beilieve is CSS, so I tried it, after fixing
some error I still could not see the font change. I then do research again to find out I need to add
the file to QFontDatabase, so I did that, no luck again. It ended up I was on the right track, and I just
needed to use absolute path instead of the relative one (which seems to be macOS specific problem and I 
still don't know why). I will need to develop in different platform (Windows, Linux) as well to avoid these
sorts of problems. Now I changed the font and next thing I want to do is to draw the icons and make the menu
looks better. As a leader I have to know more than my team members do (although I don't have one yet), and 
work way harder.
Fixed some layout and added a toggle for Experience, took quit a long time on that but it looks pretty good.
Gotta draw the icons tomorrow.

08/24/22

After working on experience bar and objective display (or quest helper), and I also want to work on other 
utilities such as skill tree and achievements and quest log, I thought why not combine them into one app, 
RPGOverlay, not sure if 'RPG' make sense because there isn't role-play element in there, but I just think 
it is cooler. 
Just to re-cap the purpose of these utilities, experience bar is to provide a sense of progression 
and make tasks less boring. Objective display is for reminding myself to focus on one thing and have clear
direction to prevent myself get lost and keep myself motivated. Skill tree is also similar to game skills,
for me to record the skill level I obtained and the skills I want to gain. Achievements is customize trophy
system, both reward myself for achieve something significant and serve as the 'cookie jar' to build my self
confidence and encourage myself to strike for higher achievement. 
So here is a rough plan to build it: 
 - Basic UI design (document it)
   - I want it to be accessable on the toolbar for mac, not sure how I want
it to go with windows, but I am using mac so mac first. 
 - Figure out how to make Python app on mac toolbar
   - System tray & Mac menu bar applications | pythonguis.com/tutorials/system-tray-mac-menu-bar-applications-pyqt/
 - Build app according to the design
Finished the design for main menu and achievement, I started to learn how to make toolbar icon app in pyqt.
The tutorial only shows how to make the icon pop up a menu but I want to have a window stick right under it,
and since there doesn't seems to be a function for QSystemTray to show a window instead of menu (but there
is a geometry() function and actived() signal) so I figure I could show such window indirectly. 
There were some confusion for the timing of tray updating its position, it gave me weird position at first
but it comes out that the correct position updates after it emits the activated signal, so the problem is 
solved since the reason was found. I still need to make some adjustments to the window and then I can start
working on the interface, but this is it for today.
