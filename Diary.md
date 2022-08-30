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