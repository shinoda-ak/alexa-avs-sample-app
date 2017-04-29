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

#include "SocketConnection.h"
#include <exception>


namespace ConexantAgent {

SocketConnection::SocketConnection() {
	clearSocketMembers();
}


SocketConnection::~SocketConnection() {
	if (m_socketHandle >= 0) {
		close(m_socketHandle);
	}
}

int SocketConnection::sendAll(char *buf, int *len) {
	int total = 0;        // how many bytes we've sent
	int bytesleft = *len; // how many we have left to send
	int n;

	while (total < *len) {
		n = send(m_socketHandle, buf + total, bytesleft, 0);
		if (n == -1) { break; }
		total += n;
		bytesleft -= n;
	}

	*len = total; // return number actually sent here

	return n == -1 ? -1 : 0; // return -1 on failure, 0 on success
}

void SocketConnection::clearSocketMembers() {
	// This is called either on initialization (to set initial values of these
	// related data members), or to reset so we can try creating a new
	// connection.

	if (m_socketHandle >= 0) {
		close(m_socketHandle);
	}
	m_socketHandle = -1;      // 0 can be a valid socket
	m_socketConnected = false;
	memset(&m_socketAddr, 0, sizeof(sockaddr_in));
}

void SocketConnection::init() {
	clearSocketMembers();

	m_socketHandle = socket(AF_INET, SOCK_STREAM, IPPROTO_IP);
	if (m_socketHandle < 0) {
		throw std::exception();
	}

	struct ifaddrs* ifAddrStruct = nullptr;
	getifaddrs(&ifAddrStruct);
	for (struct ifaddrs* ifAddr = ifAddrStruct; ifAddr; ifAddr = ifAddr->ifa_next) {

		if (ifAddr->ifa_addr &&
			(ifAddr->ifa_addr->sa_family == AF_INET) &&
			(ifAddr->ifa_flags & (IFF_LOOPBACK | IFF_UP | IFF_RUNNING))) {

			memcpy(&m_socketAddr, ifAddr->ifa_addr, sizeof(sockaddr_in));
			m_socketAddr.sin_family = AF_INET;
			m_socketAddr.sin_port = htons(PORT_NUMBER);

			break;
		}
	}
	if (ifAddrStruct) {
		freeifaddrs(ifAddrStruct);
	}
}

bool SocketConnection::initializeSocket() {
	try {
		init();
	}
	catch (std::exception) {
		fprintf(stderr, "Failed to initialize socket\n");
		return false;
	}
	return true;
}

bool SocketConnection::makeConnection() {

	if (connect(m_socketHandle,
		(struct sockaddr*)&m_socketAddr,
		sizeof(m_socketAddr)) < 0) {
		return false;
	}

	m_socketConnected = true;
	fprintf(stdout, "Connected\n");
	return true;
}

}