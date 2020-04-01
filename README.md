# HomeAutomation

The code in this project is a framework for handling intents. It does a number of things:

- It sets up an HTTP server which receives Intents from Rhasspy
- It adds an abstraction between Rhasspy and the code that handles the intents. Because of that, it should be possible to use the IntentHandlers which are created based on this project with other software like Rhasspy.
- I want to actively develop my IntentHandlers, and I don't want to have to manually update the Sentences & Slots in Rhasspy all the time when I make a code change. Therefore I added some functionality that takes all the IntentDefinitions, as I've named them and uploads them to Rhasspy when the server is started. For now only quite basic Sentences can be created. In the future I want to be able to support quite complicated sentences like the ones used in https://community.rhasspy.org/t/rhasspy-can-tell-you-the-weather-at-least-if-you-speak-german/671
- I want to be able to use multiple speakers, so I can choose on which device my voice assistant answers me. One of those is a Sonos speaker, so I've added functionality to play voice responses on a Sonos speaker.
