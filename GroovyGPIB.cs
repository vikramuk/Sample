SCPI and Excel demo
SCPI and Excel demo - For FLUKE multimeter
import java.lang.System;
import com.gehc.gep.core.data.api.Data
import com.gehc.gep.core.data.api.DataSubType
import com.gehc.gep.controller.mcb.api.Mcb
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    def run() {
        Data mcbData = dataModel.get(Mcb.CURRENTS_ON_DATA_ID, DataSubType.INPUT)
         
        multimeter = networkModel.get("multimeter")         // Creation of an element in the NetworkModel, which id is "multimeter"
        multimeter.setIp("172.16.0.50").setPort(3490)       // The ip and port number of the element are set
        multimeter.connect()                                // Finally, the element is connected to the application
        excelFile = excel.get("test multi")                 // Creation of an ExcelFile element from the ExcelModel, which id is "demo"
        excelSheet = excelFile.get("First test")            // Creation of a sheet in the previouly created ExcelFile
        Thread.sleep(100)
         
        multimeter.scpi("SYST:REM")                         // The .spci() method allows to send SCPI command to the remote device, here it set the device to remote mode
        multimeter.scpi("SYST:BEEP")
        multimeter.scpi("CONF:CURR:DC")
        multimeter.scpi("CURR:RANG MAX")
        multimeter.scpi("INIT")
        multimeter.scpi("SYST:BEEP")
         
        Thread.sleep(100)
         
        excelSheet.get(1, 1).writeCell("T0 + n ms")
        excelSheet.get(2, 1).writeCell("Current")
        long t0 = System.currentTimeMillis();
        for (int i = 0; i < 20; i ++) {
            if ( (i & 1) == 0 ) {
                // even
                mcbData.addRecord("Groovy", Boolean.TRUE)
            } else {
                // odd
                mcbData.addRecord("Groovy", Boolean.FALSE)
            }
             
            eventModel.get(Mcb.SEND_CONTROL_TOPIC_EVENT_ID).addOccurence("Groovy", "Groovy", null);
            result = multimeter.scpi("MEAS:CURR:DC?")
            excelSheet.get(2, i+2).writeCell(result)
            long duration = System.currentTimeMillis() - t0;
            excelSheet.get(1, i+2).writeCell(duration)
            println "Measure n°" + i + " after " + duration + "ms = " + result
            Thread.sleep(500)
        }
         
        excelFile.saveAs("{user}/testMultiResult.xlsx")
        multimeter.disconnect()
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)kjmhgk
    }
}

LeCroy scope demo
LeCroy scope Demo
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    def run() {
         
        leCroy = leCroyScopeModel.get("firstScope")                                                // Creation of the LecroyElement which id is firstScope
         
        leCroy.connect("169.254.89.238")                                                     // Connection to the leCroy scope
        //leCroy.setConfiguration("C:/Users/212578019/Documents/ScopeConfig.txt")            // Command to set or save the configuration of the leCroy scope
        //leCroy.saveConfigurationTo("C:/Users/212578019/Documents/ScopeConfig.txt")
        leCroy.screenShotScope("D:/HardCopy/", "{user}/Avant.png", "Avant.png")              // Command used to screenshot the leCroyScope
        leCroy.setConfiguration("C:/Users/212578019/Documents/ScopeConfig.txt")
        leCroy.sendCommand("C1:VDIV 80")                                                     // sendCommand is used to send a command to the leCroy scope
        leCroy.sendCommand("C2:VDIV 80")   
        println leCroy.getPiMeasure(6)                                                       
        leCroy.sendCommand("C1:OFST -10 MV")
        leCroy.sendCommand("C2:OFST -10 MV")
         
        leCroy.waitForScope()
         
        leCroy.screenShotScope("D:/HardCopy/", "{user}/Apres.png", "Apres.png")
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)kjmhgk
    }
}
 
SCPI demo
SCPI Demo - For FLUKE multimeter
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    def run() {
        multimeter = networkModel.get("multimeter")         // Creation of an element in the NetworkModel, which id is "multimeter"
        multimeter.setIp("172.16.0.50").setPort(3490)       // The ip and port number of the element are set
        multimeter.connect()                                // Finally, the element is connected to the application
        Thread.sleep(100)
         
        multimeter.scpi("SYST:REM")                         // The .spci() method allows to send SCPI command to the remote device, here it set the device to remote mode
        multimeter.scpi("SYST:BEEP")
        multimeter.scpi("CONF:CURR:DC")
        multimeter.scpi("CURR:RANG MAX")
        multimeter.scpi("INIT")
        multimeter.scpi("SYST:BEEP")
         
        Thread.sleep(100)
        multimeter.disconnect()
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)kjmhgk
    }
}
 
FTP demo
FTP demo
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    def run() {
       ftp = networkModel.get("ftpServer")                                // Create a new NetworkElement which id is ftpServer
       ftp.setIp("172.16.0.33").setPort(21)                               // set the IP address and the port number of the NetworkElement to 172.16.0.33 and 21
       ftp.connectFtp()                                                   // Conect the host to the remote FTP server using the NetworkElement
       ftp.uploadFtp("usr/test.txt", "{user}/testUpload.txt")             // Upload the file testUpload.txt located on the user folder on the host to the FTP server on usr/test.txt
       ftp.downloadFtp("usr/test.txt", "{user}/testDownload.txt")         // Download the file test.txt located on the FTP server on usr/test.txt to the user folder on the host with testDowload.txt as name
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)kjmhgk
    }
}
 
Excel demo
Excel demo
import com.gehc.gep.controller.mcb.api.Mcb
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    def run() {
        excelFile = excel.get("test multi")                 // Creation of an ExcelFile element from the ExcelModel, which id is "demo"
        excelSheet = excelFile.get("First test")            // Creation of a sheet in the previouly created ExcelFile
        excelSheet.get(1, 1).writeCell("T0 + n ms")
        excelSheet.get(2, 1).writeCell("Current")
        result = "test"
        duration = 1
        excelSheet.get(2, i+2).writeCell(result)
        excelSheet.get(1, i+2).writeCell(duration)
        excelFile.saveAs("{user}/testMultiResult.xlsx")
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)
    }
}

Swing demo
Swing demo
import groovy.swing.SwingBuilder
import java.awt.BorderLayout
new SwingBuilder().edt {
  frame(title: 'Frame', size: [100, 100], show: true) {
    borderLayout()
    textlabel = label(text: 'Display McbControlTopic.currents_on.feedback', constraints: BorderLayout.NORTH)
    button(text:'Display',
         actionPerformed: {return 2})
  }
}

Telnet demo
Telnet demo
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    def run() {
       test = networkModel.get("test")
       test.setIp("172.16.0.33").setPort(52024)
       test.connect()
       test.telnet('')
       test.telnet("test z")
       Thread.sleep(2000)
       test.printBuffer()
       test.telnet("test z")
       Thread.sleep(2000)
       test.printBuffer()      
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)
    }
}
write and read demo
write and read demo
import com.gehc.gep.controller.mcb.api.Mcb
import org.codehaus.groovy.runtime.InvokerHelper
 
class Main extends Script {
    def run() {
       File file = resources.getFile("{user}/testUpload.txt")
        
       // Write in a file
       PrintWriter out = new PrintWriter(file)
       out.print("testScriptGroovy")
       out.close()
           
       // Read all File at once
       FileInputStream fileReader = new FileInputStream(file)
       int content;
       while ((content = fileReader.read()) != -1) {
            System.out.print((char) content);
        }
       // Read line by line
       BufferedReader bufFileReader = new BufferedReader(new InputStreamReader(new FileInputStream(file)))
       bufFileReader.readLine()
       bufFileReader.close()
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)kjmhgk
    }
}
