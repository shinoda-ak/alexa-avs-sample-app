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

#include <sys/types.h>
#include <sys/socket.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h> 

namespace ConexantAgent {

	class SocketConnection {
	public:
		SocketConnection();
		virtual ~SocketConnection();
		int sendAll(char *buf, int *len);
		bool initializeSocket();
		bool makeConnection();

	private:
		void clearSocketMembers();
		void init();

		// Socket variables
		int m_socketHandle = -1;
		bool m_socketConnected = false;
		struct sockaddr_in m_socketAddr;
		const u_short PORT_NUMBER = 5451;
	};

}