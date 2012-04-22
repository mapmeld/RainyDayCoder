<h3>Summary</h3>
<b>Rainy Day Coder</b> is an app that encourages you to complete your next lesson on Codecademy on rainy nights and weekends.

When you graduate, you can join Code for America's Brigade of volunteer coders and designers.

<h3>Technology</h3>
Coded in Python, runs on Google App Engine

This project is enthusiastically <strong>open source</strong> and welcomes your spinoff, whether it's <i>Sunny Sunday Mapper</i>, <i>Snowbound Musician</i>, or something else entirely.

<h3>Install Directions</h3>
<ol>
<li>Set up a Google App Engine instance</li>
<li>Create an app on Twitter with read/write access and an OAuth token</li>
<li>Create a botconfig.py file with info about your Twitter API account. This file is not shared with GitHub because it is in the .gitignore file</li>
<li>Register a number on Twilio to send SMS messages.</li>
<li>Put your Twilio number, account, and token into phoneconfig.py This file is in .gitignore and not shared with GitHub</li>
<li>Upload the app to Google App Engine</li>
</ol>

TODO:
<ul>
<li>Add zipcode to state to region support via <a href="http://daspecster.github.com/ziptastic/index.html">Ziptastic</a></li>
<li>Check each region daily, but don't contact weekenders or recently-contacted people</li>
<li>Logging in and changing user settings</li>
<li>Better answers on why to code</li>
<li>Watch Codecademy progress on Twitter</li>
<li>Connect to Khan Academy's CS videos</li>
<li>Connect to the Stanford AI course videos</li>
</ul>
