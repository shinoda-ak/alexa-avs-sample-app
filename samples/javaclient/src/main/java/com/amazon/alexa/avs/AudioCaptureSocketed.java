/** 
 * Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Amazon Software License (the "License"). You may not use this file 
 * except in compliance with the License. A copy of the License is located at
 *
 *   http://aws.amazon.com/asl/
 *
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the 
 * specific language governing permissions and limitations under the License.
 */
package com.amazon.alexa.avs;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PipedInputStream;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.TargetDataLine;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.conexant.alexa.avs.CircularBuffer;

public class AudioCaptureSocketed {
    private static AudioCaptureSocketed sAudioCapture;
    //private final TargetDataLine microphoneLine;
    private AudioFormat audioFormat;
    private AudioBufferThread thread;

    private static final int BUFFER_SIZE_IN_SECONDS = 9;
    private static final int CBUFFER_SIZE_IN_SECONDS = 1;
    private static final int PORT = 5451;

    private final int BUFFER_SIZE_IN_BYTES;
    private final int SOCKET_BUFFER_SIZE = 2048;

    private static final Logger log = LoggerFactory.getLogger(AudioCaptureSocketed.class);
    
    public static AudioCaptureSocketed getAudioHardware(final AudioFormat audioFormat,
            MicrophoneLineFactory microphoneLineFactory) throws LineUnavailableException {
        if (sAudioCapture == null) {
            sAudioCapture = new AudioCaptureSocketed(audioFormat, microphoneLineFactory);
        }
        return sAudioCapture;
    }

    private AudioCaptureSocketed(final AudioFormat audioFormat, MicrophoneLineFactory microphoneLineFactory)
            throws LineUnavailableException {
        super();
        this.audioFormat = audioFormat;
        //microphoneLine = microphoneLineFactory.getMicrophone();
        //if (microphoneLine == null) {
        //    throw new LineUnavailableException();
        //}
        BUFFER_SIZE_IN_BYTES = (int) ((audioFormat.getSampleSizeInBits() * audioFormat.getSampleRate()) / 8
                * BUFFER_SIZE_IN_SECONDS);
        for (int i = 0; i<10; i++){
	        try{
	        	startContinuousRecording();
	        	break;
	        }
	        catch (LineUnavailableException | IOException e){
	        	log.error("Error starting Continuous recording");
	        }
        }
    }
    
    private void startContinuousRecording() throws LineUnavailableException, IOException {
        //try{
	    	//startCapture();
	        thread = new AudioBufferThread();
	        thread.start();
        //} catch (LineUnavailableException e) {
        //    stopCaptureReal();
        //    throw e;
        //}
    }

    public InputStream getAudioInputStream(final RecordingStateListener stateListener,
            final RecordingRMSListener rmsListener) throws LineUnavailableException, IOException {
        try {
            //startCapture();
            PipedInputStream inputStream = new PipedInputStream(BUFFER_SIZE_IN_BYTES);
            thread.setAudioStateOutputStream(inputStream, stateListener, rmsListener);
            //thread = new AudioBufferThread(inputStream, stateListener, rmsListener);
            //thread.start();
            return inputStream;
        } catch (IOException e) {
            stopCapture();
            throw e;
        }
    }

    public void stopCapture() {
    	thread.closePipedOutputStream();
    }
    public void stopCaptureReal() {
        //microphoneLine.stop();
        //microphoneLine.close();
    }
    

    private void startCapture() throws LineUnavailableException {
        //microphoneLine.open(audioFormat);
        //microphoneLine.start();
    }

    public int getAudioBufferSizeInBytes() {
        return BUFFER_SIZE_IN_BYTES;
    }

    private class AudioBufferThread extends Thread {

        private AudioStateOutputStream audioStateOutputStream;
        private CircularBuffer cBuffer;
        private Boolean firstRun = true;
        private Socket socket = null;
        private DataInputStream input = null;
        private ServerSocket serverSocket = null;

        public AudioBufferThread(PipedInputStream inputStream,
                RecordingStateListener recordingStateListener, RecordingRMSListener rmsListener)
                        throws IOException {
            audioStateOutputStream =
                    new AudioStateOutputStream(inputStream, recordingStateListener, rmsListener);
        }
        
        public AudioBufferThread() throws IOException
        {
            cBuffer = new CircularBuffer((int)(audioFormat.getSampleSizeInBits() * audioFormat.getSampleRate() / 8 * CBUFFER_SIZE_IN_SECONDS));
            serverSocket = new ServerSocket(PORT, 0, InetAddress.getByName(null));
        }
        
        public void setAudioStateOutputStream(PipedInputStream inputStream,
                RecordingStateListener recordingStateListener, RecordingRMSListener rmsListener)
                        throws IOException {
        	audioStateOutputStream =
            new AudioStateOutputStream(inputStream, recordingStateListener, rmsListener);
        	firstRun = true;
        }
        

        @Override
        public void run() {
        	while (true) {
        		try{
	        		while(socket == null) {
	        			socket = serverSocket.accept();
	        			input = new DataInputStream(socket.getInputStream());
	        		}
	        		
		            while (socket != null && input != null && !socket.isClosed()) {
		            	copyAudioBytesFromInputToOutput();
		            }
		            
		            closePipedOutputStream();
		            closeSocket();
        		}
        		catch(Exception ex) {
        			closeSocket();
        		}
        	}
        }
        
        private void closeSocket(){
        	try {
    			if (input != null) {
    				input.close();
    				input = null;
    			}
    			if (socket != null) {
    				socket.close();
    				socket = null;        			
    			}
			}
			catch (IOException e)
			{
				log.error("Error closing socket/input");
			}
        }

        private void copyAudioBytesFromInputToOutput() {
            byte[] data = new byte[SOCKET_BUFFER_SIZE]; 
            		//new byte[microphoneLine.getBufferSize() / 5];
            //int numBytesRead = microphoneLine.read(data, 0, data.length);
            try {
                int numBytesRead = input.read(data, 0, SOCKET_BUFFER_SIZE);
                if (numBytesRead == -1)
                	throw new IOException();
            	if(audioStateOutputStream != null){
            		if (firstRun)
            		{
            			audioStateOutputStream.write(cBuffer.getEntireBuffer(), 0, cBuffer.size);
            			firstRun = false;
            		}
            		audioStateOutputStream.write(data, 0, numBytesRead);
            		
            	}
            	cBuffer.insertArray(data);
            } catch (IOException e) {
                //stopCaptureReal();
            	closeSocket();
            }
        }

        public void closePipedOutputStream() {
            try {
                audioStateOutputStream.close();
                audioStateOutputStream = null;
            } catch (IOException e) {
                log.error("Failed to close audio stream ", e);
            }
        }
    }

}
