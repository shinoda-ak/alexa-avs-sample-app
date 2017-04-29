cd samples/
cd tLED/
lxterminal -e "sudo python tLEDServer.py" &
cd ../companionService
lxterminal -e "npm start" &
cd ../javaclient
lxterminal -e "mvn exec:exec" &
#sleep 32
#Uncomment if run automatically at startup
cp ~/leftarc ~/.asoundrc
sleep 1
cd ../wakeWordAgent/src
lxterminal -e "./wakeWordAgent -e sensory" &
cd ../../recordingAgent
lxterminal -e "./run.sh" &
cd ~
