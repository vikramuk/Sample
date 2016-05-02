/**
 * @license

Copyright 2014 Günter Fuchs

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
* 
* @version 0.3
 */
package com.gpib;


import com.sun.jna.Memory;
import com.sun.jna.NativeLong;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.ByteByReference;
import com.sun.jna.ptr.IntByReference;
import com.sun.jna.ptr.LongByReference;
import com.sun.jna.ptr.NativeLongByReference;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;

import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.nio.file.Files;

import visa.VisaLibrary;
import visatype.VisatypeLibrary;


/**
 * This class provides Java wrapper functions around the native Windows VISA API.
 * @author Günter Fuchs (gfuchs@acousticmicroscopy.com)
 * todo Test instantiating more than one instrument.
 */
public class JVisa {
  /** version of this library */
  public static final String JVISA_VERSION = "JVisa Version 0.3";

  /** What is called viSession in Visa DLL becomes Handle in JVisa
    so that viSession is not mistaken for a Java object.
    The handle gets initialized only once when this class is loaded (first 
    time only initialization).
  */
  protected static long visaResourceManagerHandle = 0;
  
  /**
   * number of bytes read
   */
  long readCount;
  
  /** 
   * This method gets the resource manager handle.
   * @return handle
   */
  public long getResourceManagerHandle() {
    return visaResourceManagerHandle;
  }
  /** 
   * handle for one instrument
   * This class handles only one instrument. To control more instruments
   * instantiate one class per instrument. The resource manager is common (static)
   * to all instances.
   */
  protected NativeLong visaInstrumentHandle;
  /**
   * This method returns the handle for the instrument.
   * @return instrument handle
   */
  public long getInstrumentHandle() {
    return visaInstrumentHandle.longValue();
  }
  /** default size for input buffer */
  protected int bufferSizeDefault = 1024;
  /** encoding of response when it is a string */
  protected String responseEncoding = "UTF8";
  /** the name of this class used by its logger */
  protected static final String className = JVisa.class.getName();
  /** logger of this class */
  public static final Logger LOGGER = Logger.getLogger(className);
  /** logger file handler */
  public static FileHandler logFileHandler;
  /** logger formatter */
  public static SimpleFormatter logFormatter;
  /** Log folder is added to the current path. */ 
  public final String LOG_FOLDER = "log/";
  /** constant when VISA return status is not success */
  public long VISA_JAVA_ERROR = 0x7FFFFFFF;
  /** JNA VISA functions return this status object */
  public JVisaStatus statusObject;

  /**
   * constructor
   */
  public JVisa() {
    try {
      statusObject = new JVisaStatus(bufferSizeDefault, responseEncoding);
//            LOGGER.setLevel(Level.INFO);
      LOGGER.setLevel(Level.SEVERE);
      LOGGER.info(String.format("user.dir is %s", System.getProperty("user.dir")));
      // todo Create log folder if it does not exist.
      Path logPath = Paths.get(LOG_FOLDER);
      if (Files.notExists(logPath)) {
        Files.createDirectory(logPath);
      }
      logFileHandler = new FileHandler(String.format("%s%sLog.txt", LOG_FOLDER, JVisa.class.getSimpleName()));
      logFormatter = new SimpleFormatter();
      logFileHandler.setFormatter(logFormatter);
      LOGGER.addHandler(logFileHandler);
    }
    catch(SecurityException | IOException e) {
        LOGGER.log(Level.SEVERE, e.getMessage(), e);
    }
  }
    
    
  /**
   * This method returns the version of this library.
   * @return version string
   */
//  public static String getVersion() {
//    return JVISA_VERSION;
//  }

  /**
   * This method sets the path and file name for a log file.
   * @param logPath path and full name of log file
   */
  public void setLogFile(String logPath) {
    try {
      // Is closing necessary, or does removal close the file?
      logFileHandler.close();
      LOGGER.removeHandler(logFileHandler);
      logFileHandler = new FileHandler(logPath);
      LOGGER.addHandler(logFileHandler);
    }
    catch(SecurityException | IOException e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
    }
  }


  /**
   * This method gets the resource manager handle. 
   * @return the visaResourceManagerHandle
   */
  public long getVisaResourceManagerHandle() {
    return visaResourceManagerHandle;
  }


  /**
   * This method creates a session for a default resource manager.
   * @return status of the operation
   * todo VisaLibrary.ViStatus is the interface for a callback function. Implement it. 
   */
  public long openDefaultResourceManager() {
    try {
      LOGGER.info("Open resource manager.");
      NativeLongByReference pViSession = new NativeLongByReference();
      VisaLibrary.ViStatus visaStatus = VisaLibrary.INSTANCE.viOpenDefaultRM(pViSession);
      statusObject.setStatus(visaStatus);
      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
        return statusObject.visaStatusLong;
      }
      LOGGER.info(String.format("visaStatus = 0x%08X", statusObject.visaStatusLong));
      visaResourceManagerHandle = pViSession.getValue().longValue();
      if (visaResourceManagerHandle != 0) {
        statusObject.printStatusDescription(visaResourceManagerHandle);
        statusObject.resourceManagerHandle = visaResourceManagerHandle;
      }
        // Install event handler.
  //      JVisaEvent eventObject = new JVisaEvent(userHandle);
  //      JVisaCallback callback = new JVisaCallback(eventObject);
  //      Pointer pUserHandle = new LongByReference(userHandle).getPointer();
  //      visaStatus = TkVISA64Library.INSTANCE.viInstallHandler(
  //              new NativeLong(visaResourceManagerHandle), 
  //              new NativeLong(TkVISA64Library.VI_EVENT_EXCEPTION), 
  //              eventObject.getHandlerType(), 
  //              pUserHandle);
  //      statusObject.setStatus(visaStatus);
  //      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
  //          return statusObject.visaStatusLong;
  //      }
    }
    catch (Error | Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      statusObject.resourceManagerHandle = 0;
      return VISA_JAVA_ERROR;
    }
    return statusObject.visaStatusLong;
  }

  /**
   * This method closes the resource manager.
   * @return status of the operation
   */
  public long closeResourceManager() {
      try {
        LOGGER.info("Close resource manager.");
        VisaLibrary.ViStatus visaStatus = VisaLibrary.INSTANCE.viClose(new NativeLong(visaResourceManagerHandle));
        statusObject.setStatus(visaStatus);
        statusObject.resourceManagerHandle = visaResourceManagerHandle = 0;
      }
      catch (Exception e) {
        LOGGER.log(Level.SEVERE, e.getMessage(), e);
        return VISA_JAVA_ERROR;
      }
      return statusObject.visaStatusLong;
  }


  /**
   * This method gets an attribute of type byte (native ViUInt8).
   * @param attribute which attribute to get
   * @param value contains an attribute of type short
   * @param sessionHandle handle of resource manager or instrument
   * @return status of the operation
   */
  public long getAttribute(int attribute, JVisaReturnNumber value, long sessionHandle) {
    try {
      VisaLibrary.ViStatus visaStatus;
      String formatString = "Attribute value = 0x";
      LOGGER.info(String.format("Get attribute %08X.", attribute));
      if (value.returnNumber instanceof Short) {
        ByteByReference pByte = new ByteByReference();
        visaStatus = VisaLibrary.INSTANCE.viGetAttribute(
                new NativeLong(visaResourceManagerHandle), 
                new NativeLong(attribute), pByte.getPointer());
        value.returnNumber = pByte.getValue();
        formatString += "%02X";
      }
      else if (value.returnNumber instanceof Integer) {
        IntByReference pInt = new IntByReference();
        visaStatus = VisaLibrary.INSTANCE.viGetAttribute(
                new NativeLong(visaResourceManagerHandle), 
                new NativeLong(attribute), pInt.getPointer());
        value.returnNumber = pInt.getValue();
        formatString += "%04X";
      }
      else if (value.returnNumber instanceof Long) {
        LongByReference pLong = new LongByReference();
        visaStatus = VisaLibrary.INSTANCE.viGetAttribute(
                new NativeLong(visaResourceManagerHandle), 
                new NativeLong(attribute), pLong.getPointer());
        value.returnNumber = pLong.getValue();
        formatString += "%08X";
      }
      else {
        return VISA_JAVA_ERROR;
      }
      statusObject.setStatus(visaStatus);
      LOGGER.info(String.format(formatString, value.returnNumber));
    }
    catch (Exception e) {
        LOGGER.log(Level.SEVERE, e.getMessage(), e);
        return VISA_JAVA_ERROR;
    }
    return statusObject.visaStatusLong;
  }


  /**
   * This method gets an attribute of type String (native ViPChar).
   * @param attribute which attribute to get
   * @param value contains an attribute of type String
   * @param sessionHandle handle of resource manager or instrument
   * @return status of the operation
   */
  public long getAttribute(int attribute, JVisaReturnString value, long sessionHandle) {
    try {
      LOGGER.info(String.format("Get attribute %08X.", attribute));
      Memory responseBuffer = new Memory(bufferSizeDefault);
      VisaLibrary.ViStatus visaStatus = VisaLibrary.INSTANCE.viGetAttribute(
              new NativeLong(visaResourceManagerHandle), 
              new NativeLong(attribute), 
              (Pointer) responseBuffer);
      statusObject.setStatus(visaStatus);
      value.returnString = responseBuffer.getString(0, responseEncoding).trim();
      LOGGER.info(String.format("Attribute value = %s", value.returnString));
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
    return statusObject.visaStatusLong;
  }


  /**
   * This method sets an attribute.
   * @param attribute which attribute to get
   * @param value contains an attribute
   * @param sessionHandle handle of resource manager or instrument
   * @return status of the operation
   * todo Investigate whether the Java signed int variable value gets converted
   *      correctly to unsigned int in NativeLong(value). Sometimes, msb is
   *      set in an attribute, e.g. VI_ATTR_RECV_TCPIP_ADDR is 0xBFFF4198UL.
   */
  public long setAttribute(int attribute, int value, long sessionHandle) {
    try {
      LOGGER.info(String.format("Set attribute %08X to %08X.", attribute, value));
      VisaLibrary.ViStatus visaStatus = VisaLibrary.INSTANCE.viSetAttribute(
              new NativeLong(sessionHandle), 
              new NativeLong(attribute), 
              new NativeLong(value)); 
      statusObject.setStatus(visaStatus);
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
    return statusObject.visaStatusLong;
  }


  /**
   * This method sets an attribute for a resource manager.
   * @param attribute which attribute to get
   * @param value contains an attribute
   * @return status of the operation
   */
  public long setAttribute(int attribute, int value) {
    return setAttribute(attribute, value, visaResourceManagerHandle);
  }


  /**
   * This method sets the communication timeout.
   * @param timeout in ms
   * @return status of the operation
   */
  public long setTimeout(int timeout) {
    try {
      LOGGER.info("Set timeout.");
      long visaStatus = setAttribute(VisaLibrary.VI_ATTR_TMO_VALUE, timeout, getInstrumentHandle());
      if (visaStatus != VisatypeLibrary.VI_SUCCESS) {
          return visaStatus;
      }
      return visaStatus;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * This method gets the version of the resource (TekVisa.dll).
   * @param version   resource version number
   * @return status of the operation
   */
  public long getResourceVersion(JVisaReturnNumber version) {
    try {
      LOGGER.info("Get resource version.");
      long visaStatus = getAttribute(VisaLibrary.VI_ATTR_RSRC_SPEC_VERSION, version, visaResourceManagerHandle);
      if (visaStatus != VisatypeLibrary.VI_SUCCESS) {
        return visaStatus;
      }
      LOGGER.info(String.format("Resource version = 0x%08X", version.returnNumber));
      return visaStatus;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }

  
  /**
   * This method converts a Java String to a ByteBuffer / C-type string.
   * @param source string to convert
   * @return Java string converted to C-type string (0 terminated) 
   */
  public ByteBuffer stringToByteBuffer(String source) {
    try {
      ByteBuffer dest = ByteBuffer.allocate(source.length() + 1);
      dest.put(source.getBytes(responseEncoding));
      dest.position(0);
      return dest;
    }
    catch (UnsupportedEncodingException e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return null;
    }
  }

  /**
   * Opens an instrument session.
   * @param instrument string that contains the instrument address and bus interface
   * @return status of the operation
   */
  public long openInstrument(String instrument) {
    VisaLibrary.ViStatus visaStatus;
    NativeLongByReference pViInstrument = new NativeLongByReference();
    try {
      LOGGER.info(String.format("Open instrument %s.", instrument));
      ByteBuffer pViString = stringToByteBuffer(instrument);
      if (pViString == null) {
        return VISA_JAVA_ERROR;
      }
      visaStatus = VisaLibrary.INSTANCE.viOpen(
              new NativeLong(visaResourceManagerHandle), 
              pViString,         // byte buffer for instrument string
              new NativeLong(0), // access mode (locking or not). 0:Use Visa default
              new NativeLong(0), // timeout, only when access mode equals locking,
              pViInstrument      // pointer to instrument object
              );
      statusObject.setStatus(visaStatus);
      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
        LOGGER.log(Level.SEVERE, String.format("Could not open session for %s.", instrument), (Throwable) null);
        return statusObject.visaStatusLong;
      }
      else {
        if (statusObject.visaStatusLong == VisatypeLibrary.VI_SUCCESS) {
          visaInstrumentHandle = pViInstrument.getValue();
          LOGGER.info(String.format("viInstrument = 0x%08X.", visaInstrumentHandle.longValue()));
        }
        else {
          visaInstrumentHandle = new NativeLong(0);
        }
      }
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
    return VisatypeLibrary.VI_SUCCESS;
  }


  /**
   * This method closes an instrument session.
   * @return status of the operation
   */
  public long closeInstrument() {
    VisaLibrary.ViStatus visaStatus;
    try {
      LOGGER.info("Close instrument.");
      visaStatus = VisaLibrary.INSTANCE.viClose(visaInstrumentHandle);
      statusObject.setStatus(visaStatus);
      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
        LOGGER.severe("Could not close session.");
        return VISA_JAVA_ERROR;
      }
      return VisatypeLibrary.VI_SUCCESS;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * @return the visaInstrumentHandle as long
   */
  public long getVisaInstrumentHandle() {
    return visaInstrumentHandle.longValue();
  }


  /**
   * This method sends buffer content (usually a command) to the instrument.
   * @param command command or other ASCII data
   * @return status of the operation
   */
  public long write(String command) {
    VisaLibrary.ViStatus visaStatus;
    try {
      LOGGER.info(String.format("Write command \"%s\".", command));
      ByteBuffer pBuffer = stringToByteBuffer(command);
      if (pBuffer == null) {
        return VISA_JAVA_ERROR;
      }
      long commandLength = command.length();
      NativeLongByReference returnCount = new NativeLongByReference();
      visaStatus = VisaLibrary.INSTANCE.viWrite(
              visaInstrumentHandle, pBuffer, new NativeLong(commandLength), returnCount);
      statusObject.setStatus(visaStatus);
      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
        LOGGER.severe(String.format("Could not write %s.", command));
      }
      else {
        long count = returnCount.getValue().longValue();
        if (count != commandLength) {
          LOGGER.severe(String.format("Could only write %d instead of %d bytes.", count, commandLength));
          return VISA_JAVA_ERROR;
        }
      }
      return VisatypeLibrary.VI_SUCCESS;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * This method reads data from the instrument, e.g. a command response or data.
   * @param response response buffer
   * @param bufferSize size of response buffer in bytes
   * @return status of the operation
   */
  protected long read(ByteBuffer response, int bufferSize) {
    VisaLibrary.ViStatus visaStatus;
    try {
      LOGGER.info("Read response.");
      NativeLongByReference returnCount = new NativeLongByReference();
      visaStatus = VisaLibrary.INSTANCE.viRead(
              visaInstrumentHandle, response, new NativeLong(bufferSize), returnCount);
      statusObject.setStatus(visaStatus);
      readCount = returnCount.getValue().longValue();
      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
        if (readCount == 0) {
          LOGGER.severe("Reading count is 0.");
          return VISA_JAVA_ERROR;
        }
      }
      return VisatypeLibrary.VI_SUCCESS;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * This method reads a string from the instrument, e.g. a command response.
   * @param response response string
   * @param bufferSize size of response buffer in bytes
   * @return status of the operation
   */
  public long read(JVisaReturnString response, int bufferSize) {
    long visaStatus;
    try {
      ByteBuffer buffer = ByteBuffer.allocate(bufferSize);
      visaStatus = read(buffer, bufferSize);
      if (visaStatus == VISA_JAVA_ERROR) {
        return visaStatus;
      }
      response.returnString = new String(buffer.array(), 0, (int) readCount, responseEncoding).trim();
      LOGGER.info(response.returnString);
      return VisatypeLibrary.VI_SUCCESS;
    }
    catch (UnsupportedEncodingException e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * This method reads a string from the instrument, usually a command response.
   * @param response response string
   * @return status of the operation
   */
  public long read(JVisaReturnString response) {
    return read(response, bufferSizeDefault);
  }


  /**
   * This method reads a byte array from the instrument, usually a command response.
   * @param response response byte array
   * @param bufferSize size of response buffer in bytes
   * @return status of the operation
   */
  public long read(JVisaReturnBytes response, int bufferSize) {
    long visaStatus;
    try {
      readCount = 0;
      ByteBuffer buffer = ByteBuffer.allocate(bufferSize);
      visaStatus = read(buffer, bufferSize);
      if (visaStatus == VISA_JAVA_ERROR) {
        return visaStatus;
      }
      response.returnBytes = new byte[(int) readCount];
      System.arraycopy(buffer.array(), 0, response.returnBytes, 0, (int) readCount);
      return VisatypeLibrary.VI_SUCCESS;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * This method clears the instrument.
   * @return status of the operation
   */
  public long clear() {
    VisaLibrary.ViStatus visaStatus;
    try {
      LOGGER.info("Send viClear.");
      visaStatus = VisaLibrary.INSTANCE.viClear(visaInstrumentHandle);
      statusObject.setStatus(visaStatus);
      if (statusObject.visaStatusLong != VisatypeLibrary.VI_SUCCESS) {
        LOGGER.severe("Could not send viClear.");
      }
      return VisatypeLibrary.VI_SUCCESS;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }
}
