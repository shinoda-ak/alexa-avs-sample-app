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

public class CircularBuffer {
	public int size = 0;
	private int posp = 0;
	private byte[] buf;
	
	public CircularBuffer(int s) {
		size = s;
		buf = new byte[s];
	}
	
	public void insert(byte c) {
		buf[posp] = c;
		posp = (posp+1)%size;
	}
	
	
	//Returns how many bytes were copied
	public int insertArray(byte[] arr)
	{		
		if (arr.length >= size)
		{
			//Fill the buffer with the newest bytes
			System.arraycopy(arr, arr.length-size, buf, 0, size);
			posp = 0;
			return size;
		}
		//Length from oldest byte to end
		int lenToEnd = size - posp;
		//Copy to the buffer's end or just copy the entire array
		System.arraycopy(arr, 0, buf, posp, Math.min(lenToEnd, arr.length));
		
		if(arr.length > lenToEnd)
		{
			//Copy the rest of the array
			System.arraycopy(arr, lenToEnd, buf, 0, arr.length-lenToEnd);
		}
		//Move pointer to oldest byte
		posp = (posp + arr.length)%size;
		return arr.length;
	}
	
	public byte[] getEntireBuffer() {
		byte[] ret = new byte[size];
		//Length from oldest byte to end
		int lenToEnd = size - posp;
		
		//Copy from oldest byte to end
		System.arraycopy(buf, posp, ret, 0, lenToEnd);
		//Copy from 0 to newest byte
		if (lenToEnd != size)
		{
			System.arraycopy(buf, 0, ret, lenToEnd, size - lenToEnd);		
		}
		return ret;
	}
	public byte[] getPartialBuffer(int count) {		
		//Return entire buffer if asked for it all or more
		if (count >= size){
			return getEntireBuffer();
		}		
		
		byte[] ret = new byte[count];		
		//Length from oldest byte to end
		int lenToEnd = size - posp;
		
		System.arraycopy(buf, posp, ret, 0, Math.min(lenToEnd, count));
		
		if (lenToEnd < count)
			System.arraycopy(buf, 0, ret, lenToEnd, count - lenToEnd);
		
		return ret;
	}
}
