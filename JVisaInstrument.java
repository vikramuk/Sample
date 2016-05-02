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
 */
package com.gpib;

import java.util.logging.Level;
import visatype.VisatypeLibrary;


/**
 * This class provides basic Visa instrument handling.
 * @author Günter Fuchs (gfuchs@acousticmicroscopy.com)
*/
public class JVisaInstrument extends JVisa {
  /** return status of VISA functions */
  private long visaStatus = VisatypeLibrary.VI_SUCCESS;
  
  protected byte[] binaryResponse;
  
  /** 
   * This method gets the visa status 
   * @see JVisaStatus#visaStatus
   * @return status
  */
  public long getVisaStatus() {
    return visaStatus;
  }
  /** response string to a "*IDN?" command */ 
  private String instrumentId = "";
  /**
   * This method returns the instrument ID string 
   * @see instrumentId
   * @return instrument ID
   */
  public String getId() {
    return instrumentId;
  }
  /** logger of this class */
//  private static final Logger LOGGER_INSTRUMENT = Logger.getLogger(JVisaInstrument.className);


  /**
   * constructor
   */
  public JVisaInstrument() {
    try {
      statusObject = new JVisaStatus(bufferSizeDefault, responseEncoding);
    }
    catch(Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
    }
  }


  /**
   * Sends a command and receives its response string.
   * Since the caller cannot know the response length in advance,
   * the size of the response buffer is hard-coded.
   * @param command string to send
   * @param response string received
   * @param bufferSize size of string (C string) buffer
   * @return status of the operation
   */
  public long sendAndReceive(String command, JVisaReturnString response, int bufferSize) {
    visaStatus = VISA_JAVA_ERROR;
    try {
      visaStatus = write(command);
      if (visaStatus != VisatypeLibrary.VI_SUCCESS) {
        return visaStatus;
      }
      return read(response, bufferSize);
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * Sends a command and receives its response string.
   * Since the caller cannot know the response length in advance,
   * the size of the response buffer is hard-coded.
   * @param command string to send
   * @param response string received
   * @return status of the operation
   */
  public long sendAndReceive(String command, JVisaReturnString response) {
    return sendAndReceive(command, response, bufferSizeDefault);
  }


  /**
   * Sends a command and receives its response.
   * @param command string to send
   * @param response bytes received
   * @param bufferSize size of buffer to allocate. The buffer in response might be smaller
   *                   since it gets allocated with readCount
   * @return status of the operation
   */
  public long sendAndReceive(String command, JVisaReturnBytes response, int bufferSize) {
    visaStatus = VISA_JAVA_ERROR;
    try {
      visaStatus = write(command);
      if (visaStatus != VisatypeLibrary.VI_SUCCESS) {
          return visaStatus;
      }
      return read(response, bufferSize);
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }


  /**
   * Reads the instrument id by sending a "*IDN?" command.
   * @param id response string
   * @return status of the operation
   */
  public long readId(JVisaReturnString id) {
    try {
      visaStatus = sendAndReceive("*IDN?", id);
      if (visaStatus == VisatypeLibrary.VI_SUCCESS) {
        instrumentId = id.returnString;
        LOGGER.info(instrumentId);
      }
      return visaStatus;
    }
    catch (Exception e) {
      LOGGER.log(Level.SEVERE, e.getMessage(), e);
      return VISA_JAVA_ERROR;
    }
  }
}
