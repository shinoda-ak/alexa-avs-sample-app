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

#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>
#include "SocketConnection.h"

using namespace ConexantAgent;

int main(int argc, char *argv[])
{
	int i, sockfd = 0, n = 0, buffer_frames = 1024, channels = 1;
	int BUFSIZE = (int)(buffer_frames * snd_pcm_format_width(SND_PCM_FORMAT_S16_LE) / 8 * channels);
	int b = BUFSIZE;
	char *buffer;
	buffer = (char*)malloc(BUFSIZE);
	snd_pcm_t *capture_handle;
	struct sockaddr_in serv_addr;
	unsigned int rate = 16000;
	snd_pcm_hw_params_t *hw_params;
	snd_pcm_format_t format = SND_PCM_FORMAT_S16_LE;
	int err;
	SocketConnection *conn = new SocketConnection();

	if ((err = snd_pcm_open(&capture_handle, "default", SND_PCM_STREAM_CAPTURE, 0)) < 0) {
		fprintf(stderr, "cannot open audio device %s (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	if ((err = snd_pcm_hw_params_malloc(&hw_params)) < 0) {
		fprintf(stderr, "cannot allocate hardware parameter structure (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	if ((err = snd_pcm_hw_params_any(capture_handle, hw_params)) < 0) {
		fprintf(stderr, "cannot initialize hardware parameter structure (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	if ((err = snd_pcm_hw_params_set_access(capture_handle, hw_params, SND_PCM_ACCESS_RW_INTERLEAVED)) < 0) {
		fprintf(stderr, "cannot set access type (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	if ((err = snd_pcm_hw_params_set_format(capture_handle, hw_params, format)) < 0) {
		fprintf(stderr, "cannot set sample format (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	fprintf(stdout, "hw_params format set\n");

	if ((err = snd_pcm_hw_params_set_rate_near(capture_handle, hw_params, &rate, 0)) < 0) {
		fprintf(stderr, "cannot set sample rate (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	if ((err = snd_pcm_hw_params_set_channels(capture_handle, hw_params, channels)) < 0) {
		fprintf(stderr, "cannot set channel count (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	if ((err = snd_pcm_hw_params(capture_handle, hw_params)) < 0) {
		fprintf(stderr, "cannot set parameters (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	snd_pcm_hw_params_free(hw_params);

	if ((err = snd_pcm_prepare(capture_handle)) < 0) {
		fprintf(stderr, "cannot prepare audio interface for use (%s)\n",
			snd_strerror(err));
		exit(1);
	}

	fprintf(stdout, "audio interface prepared\n");

	while (true)
	{
		while (!conn->initializeSocket())
		{
			sleep(2);
		}

		while (!conn->makeConnection())
		{
			sleep(2);
			fprintf(stderr, "Failed to connect to AVS\n");
		}
		try{
			while (snd_pcm_readi(capture_handle, buffer, buffer_frames) >= 0 && !conn->sendAll(buffer, &b))
			{			
				b = BUFSIZE;
			}
		}
		catch(...)
		{
			printf("Exception occurred while reading or sending");
		}
	}
}
