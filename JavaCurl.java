package com.httpclient;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class JavaURL_ACSim {

	static String PORT = "COM8";
	private final String REFERER = "http://localhost:8270";
	private final String get_supported_devices = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>get_supported_devices</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value></data></array></value></param></params></methodCall>";
	private final String add_device = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>add_device</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value><value><string>U-TT</string></value></data></array></value></param></params></methodCall>";
	private final String get_devices = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>get_devices</string></value></param><param><value><array><data></data></array></value></param></params></methodCall>";
	private final String get_device_info = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>get_device_info</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value></data></array></value></param></params></methodCall>";
	private final String get_parameters = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>get_parameters</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value></data></array></value></param></params></methodCall>";
	private final String starting_simulator = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>start_simulator</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value></data></array></value></param></params></methodCall>";
	private final static String simulate_parameter_T2 = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>simulate_parameter</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value><value><string>T2</string></value><value><string>37.5</string></value></data></array></value></param><param><value><struct><member><name>Send</name><value><boolean>1</boolean></value></member></struct></value></param></params></methodCall>";
	private final static String simulate_parameter_T1 = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>simulate_parameter</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value><value><string>T1</string></value><value><string>36.5</string></value></data></array></value></param><param><value><struct><member><name>Send</name><value><boolean>1</boolean></value></member></struct></value></param></params></methodCall>";
	private final String stopping_simulator = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>stop_simulator</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value></data></array></value></param></params></methodCall>";
	private final String removed_device = "<?xml version='1.0'?><methodCall><methodName>run_keyword</methodName><params><param><value><string>remove_device</string></value></param><param><value><array><data><value><string>"+PORT+"</string></value></data></array><value></param></params></methodCall>";
	
	
	public static void main(String[] args) throws Exception {
		JavaURL_ACSim http = new JavaURL_ACSim();

//		System.out.println("Testing 1 - Send Http GET request");
//		http.sendGet();

		System.out.println("\nTesting 2 - Send Http POST request");
		http.sendPost(simulate_parameter_T1);
		System.out.println("\nTesting 2 - Send Http POST request");
		http.sendPost(simulate_parameter_T2);
	}

	// HTTP GET request
	private void sendGet() throws Exception {
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

	}

	// HTTP POST request
	private void sendPost(String Command) throws Exception {

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

	}

}
