cd samples/tLED/
sudo python tLEDServer.py &
sleep 10
cd ../companionService
sleep 1
npm start &
cd ../javaclient
sleep 10
mvn exec:exec -Dalpn-boot.version=8.1.6.v20151105 &
sleep 32
cp ~/leftarc ~/.asoundrc
cd ../wakeWordAgent/src
sleep 5
./wakeWordAgent -e gpio &
cd ../../recordingAgent
sleep 5
./run.sh &
cd ~
