using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.IO.Ports;
using System.Threading;

namespace Serialport_PS320
{
    class Serial1
    {
        static void Main(string[] args)
        {
            string COMPort = "";
            int baudrate = 0;
            string l_command = "";
            if (args == null)
            {
                COMPort = "COM2";
                baudrate = 9600;
                l_command = "030";
            }
            else
            {               
               COMPort = args[0];
               baudrate = Int32.Parse(args[1]);
                l_command = args[2];
            }                       
            SerialPort mySerialPort = new SerialPort(COMPort, baudrate, Parity.None, 8);
            try
                {
                if (mySerialPort.IsOpen)
                    mySerialPort.Close();
                    mySerialPort.Open();
                //Write(mySerialPort, l_command, true);
                /*
                    byte[] bytes = Encoding.ASCII.GetBytes(l_command);
                    mySerialPort.Write(bytes, 0, 10);
                    //Thread.Sleep(50); // small delay
                    mySerialPort.Write(bytes, 10, 9); 
                */
                foreach (char c in l_command)
                {
                    mySerialPort.Write(new string(c, 1));                    
                    Thread.Sleep(50);
                }
                mySerialPort.Write("\r");
                mySerialPort.Close();
                }
            catch (IOException ex)
                {
                    Console.WriteLine(ex);
                }



        }
        static void Write(SerialPort port, string data, bool sleep)
        {
            foreach (char c in data)
            {
                port.Write(new string(c, 1));
                if (sleep)
                    Thread.Sleep(50);
            }
            port.Write("\r");
        }
    }
}
