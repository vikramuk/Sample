package com.ge.lotus.automation.acs;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Properties;

public class ACSUtility {
	private final String REFERER = "http://localhost:8270";
	static Properties prop = new Properties();
	static InputStream input = null;
	
	public static void addNellcoreDevice(String ParameterName,String device,String parameterValue) throws Exception {
		
		startDeviceinACS(ParameterName,device);
		Thread.currentThread().sleep(5000);
		new ACSUtility().sendPost(getFinalACSXMLString(ParameterName,parameterValue));
		Thread.currentThread().sleep(5000);
		removeDeviceinACS(ParameterName);
		
	}
	
	public static void startDeviceinACS(String parameter, String deviceName) throws Exception{
		removeDeviceinACS(parameter);
		ACSUtility acsUtility =  new ACSUtility();
		acsUtility.sendPost(getFinalStringForAddingDevice(parameter,deviceName));
		acsUtility.sendPost(getFinalStringForStartSimulator(parameter));
	}
	
	
	public static void removeDeviceinACS(String parameter) throws Exception{
		ACSUtility acsUtility =  new ACSUtility();
		acsUtility.sendPost(getFinalStringForRemovingDevice(parameter));
		System.out.println("Device Romoved for "+parameter);
	}
	
	public static String getFinalACSXMLString( String parameterName,String parameterValue) throws IOException{
		String comPort = null;
		 
		comPort = getValue(parameterName.replaceAll("\\s+","")+"ComPort");
		
		
		String finalXMLString = getValue("parameter_1");
		
		finalXMLString += comPort+getValue("parameter_2");
		
		finalXMLString += parameterName+getValue("parameter_3"); 
		
		finalXMLString += parameterValue+getValue("parameter_4");
		
		return finalXMLString;
	}
	
	public static String getFinalStringForStartSimulator( String parameterName) throws IOException{
		String comPort = null;
		 
		comPort = getValue(parameterName.replaceAll("\\s+","")+"ComPort");
				
		String finalXMLString = getValue("starting_simulator1");
		
		finalXMLString += comPort+getValue("starting_simulator2");
		
						
		return finalXMLString;
	}
	
	public static String getFinalStringForAddingDevice( String parameterName,String deviceName) throws IOException{
		String comPort = null;
		 
		comPort = getValue(parameterName.replaceAll("\\s+","")+"ComPort");
				
		String finalXMLString = getValue("Adding_Device1");
		
		finalXMLString += comPort+getValue("Adding_Device2");
		
		finalXMLString += deviceName+getValue("Adding_Device3"); 
				
		return finalXMLString;
	}
	
	
	public static String getFinalStringForRemovingDevice( String parameterName) throws IOException{
		String comPort = null;
		 
		comPort = getValue(parameterName.replaceAll("\\s+","")+"ComPort");
				
		String finalXMLString = getValue("Remove_device1");
		
		finalXMLString += comPort+getValue("Remove_device2");
		
		
				
		return finalXMLString;
	}
	
	public static String getValue(String key) throws IOException{
		input = new FileInputStream("SimulationUrl.properties");

		// load a properties file
		prop.load(input);
 		
		String value = prop.getProperty(key);
		 
		return value;
	}
	
	
	// HTTP GET request
		private String sendGet() throws Exception {
			String url = REFERER;
			URL obj = new URL(url);
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();

			// optional default is GET
			con.setRequestMethod("GET");
			//add request header
			con.setRequestProperty("Referer", "http://localhost:8270/gui/");
			con.setRequestProperty("Accept-Language", "en-US,en");
			con.setRequestProperty("Connection", "keep-alive");
			con.setRequestProperty("Accept", "*/*");
			con.setRequestProperty("Content-Type", "text/plain");
			con.setRequestProperty("charset", "UTF-8");

			int responseCode = con.getResponseCode();
			System.out.println("\nSending 'GET' request to URL : " + url);
			System.out.println("Response Code : " + responseCode);
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer response = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			in.close();

			//print result
			System.out.println(response.toString());
			return response.toString();

		}

		// HTTP POST request
		public String sendPost(String Command) throws Exception {

			String url = REFERER;
			String urlParameters = Command;		
			//http://stackoverflow.com/questions/23517139/java-lang-classcastexception-com-sun-net-ssl-internal-www-protocol-https-httpsu
			URL obj = new URL(null, url, new sun.net.www.protocol.http.Handler());
			HttpURLConnection  con = (HttpURLConnection) obj.openConnection();
			con.setDoOutput(true);
			con.setUseCaches( false );
			con.setInstanceFollowRedirects(true);
			//add reqest header
			con.setRequestMethod("POST");
			con.setRequestProperty("Referer", "http://localhost:8270");
			con.setRequestProperty("Accept-Language", "en-US,en");
			con.setRequestProperty("Connection", "keep-alive");
			con.setRequestProperty("Accept", "*/*");
			con.setRequestProperty("Content-Type", "text/plain");
			con.setRequestProperty("charset", "UTF-8");

			// Send post request 
			DataOutputStream wr = new DataOutputStream(con.getOutputStream());
			wr.writeBytes(urlParameters);		
			wr.flush();
			wr.close();
			int responseCode = con.getResponseCode();
			System.out.println("\nSending 'POST' request to URL : " + url);
			//System.out.println("Post parameters : " + urlParameters);
			System.out.println("Response Code : " + responseCode);
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer response = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			in.close();
			//print result
			System.out.println(response.toString());
			return response.toString();
		}

}
