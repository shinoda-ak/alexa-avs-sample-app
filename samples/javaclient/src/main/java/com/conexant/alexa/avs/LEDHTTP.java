/*© 2017 Conexant Systems, LLC
 
 
Permission is hereby granted by Conexant, free of charge, to any developer obtaining a copy
of this software and associated documentation files (the "Software"), 
to download, use, copy, modify, merge and distribute the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.  CONEXANT RESERVES THE RIGHT TO MAKE CHANGES TO THE SOFTWARE 
WITHOUT NOTIFICATION.
*/

package com.conexant.alexa.avs;

import java.net.HttpURLConnection;
import java.net.URL;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LEDHTTP {
    private static final Logger log = LoggerFactory.getLogger(LEDHTTP.class);
    
    public static String s_ready = "/Ready";
    public static String s_volume = "/Volume?volume=";
    public static String s_recording = "/RecordingStarted";
    public static String s_cloud = "/CloudActivityStarted";
    public static String s_cloudstop = "/CloudActivityStopped";
    public static String s_speaking = "/SpeakingStarted";
    public static String s_music = "/MusicPlay";
    public static String s_finished = "/Finished";
    public static String s_error = "/Error";
    public static String s_alarmstart = "/AlarmStart";
    public static String s_alarmstop = "/AlarmStop";

    public static void makeHTTPRequest(String urlToUse)
    {
        try
        {
            URL url = new URL("http", "localhost", 4000, urlToUse);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.getResponseCode();
        }
        catch(Exception e)
        {
            log.info(e.getMessage());
        }

    }
    
}
