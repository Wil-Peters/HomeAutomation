# HomeAutomation

Rhasspy is a very cool open source project for setting up your own, private (so it does not communicate to any cloud) smart speaker. If you're interested, you can find its documentation here: https://rhasspy.readthedocs.io/en/latest/

What Rhasspy does is recognize what a user wants when they give a command to their smart speaker. It does by comparing the command the user gives to sentences that were stored in Rhasspy. When Rhasspy recognizes a sentence, it sends an Intent to anyone who is listening for it. The code in this project:

- Sets up an HTTP server which receives Intents from Rhasspy
- Adds an abstraction between Rhasspy and the code that handles the intents. Because of that, it should be possible to use the IntentHandlers which are created based on this project with other software like Rhasspy.
- Automatically updates Rhasspy with the latest Sentences & Slots when the server is started. This is for people (like me) who want to actively develop their IntentHandlers, and don't want to have to manually update the Sentences & Slots in Rhasspy all the time when they make a code change. 

  To be able to do this, this project uses IntentDefinitions. IntentDefinitions are created in code, and are broken down into Sentences & Slots. For now only quite basic IntentDefinitions can be created. In the future I want to be able to support quite complicated sentences like the ones used in https://community.rhasspy.org/t/rhasspy-can-tell-you-the-weather-at-least-if-you-speak-german/671
  
    
  Example:
  
  ```
        dim_room = IntentDefinition("DimRoom")

        room_names = [room.name for room in self._hue_manager.groups]
        room_parameter = SentenceParameter(self.ROOM, True, possible_values=room_names)
        up_down_parameter = SentenceParameter(self.UP_DOWN, True, possible_values=[self.UP, self.DOWN])
        in_decrease_parameter = SentenceParameter(self.IN_DECREASE, True, possible_values=[
            self.INCREASE, self.DECREASE])

        sentence_builder = SentenceBuilder()
        sentence_builder.add_string("Dim the lights in the")\
            .add_parameter(room_parameter)\
            .add_parameter(up_down_parameter)
        sentence = sentence_builder.build()

        sentence_builder2 = SentenceBuilder()
        sentence_builder2.add_parameter(in_decrease_parameter)\
            .add_string("the brightness in the")\
            .add_parameter(room_parameter)

        sentence2 = sentence_builder2.build()
        dim_room.add_sentence(sentence)
        dim_room.add_sentence(sentence2)
  ```
  
  Will translate into the following Rhasspy sentences & slots:
  
  ```
  Sentences
  
  [DimRoom]
  Dim the lights in the $Room{Room} (Up | Down){UpDown}
  (Increase | Decrease){InDecrease} the brightness in the $Room{Room}
  
  
  Slots
  
  "Room": [
        "living room",
        "backyard",
        "dining",
        "attic",
        "kitchen",
        "study"
    ]
   ```
  
- Enables the use of multiple speakers, so you can choose on which device your voice assistant answers you. For me personally, I want my voice assistant to be able to answer me on my Sonos speaker, so I built support for that.

Design:

![alternative text](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/Wil-Peters/HomeAutomation/development/plantuml.txt)
