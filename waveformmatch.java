package com.ge.lotus.automation.util;
 

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.awt.image.DataBuffer;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.TimerTask;

import javax.imageio.ImageIO;

 

public class WaveformVerify {
	TimerTask t;
	 

	public boolean verifyFhrListVSC(List<Integer> inputfhrList,String parameterBlocck) {
		boolean isfhrListplotted = false;
		try {
	 	  
			// Step2: Capture the screen shot ADB Bridge
			Thread.currentThread().sleep(30000);
			 captureTheScreenShot();    
			Thread.currentThread().sleep(10000);
			// Step3: Crop the Image only for VSC Chart
			cropImage(); 

			// Step4 Verify the Plotted values Against to the input values
	 
			isfhrListplotted = verifyFHRValues(inputfhrList,parameterBlocck);
		} catch (Exception e) {
			isfhrListplotted = false;
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return isfhrListplotted;
	}

	public static void captureTheScreenShot() throws IOException {

		try {
			Process p = Runtime.getRuntime()
					.exec("cmd /c adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png");
			 
		} catch (IOException e1) {
			System.out.println("Exception Occured while capturing the screenshot");
			e1.printStackTrace();
		}
		System.out.println("ScreenshotCaptured");

	}

	public static void cropImage() throws IOException {
		try{
		System.out.println("Cropping ScreenShot");
		BufferedImage image = ImageIO.read(new File("screencap.png"));
		// create a cropped image from the original image
		BufferedImage croppedImage = image.getSubimage(30, 70, 870, 368);
		File outputfile = new File("CroppedImage.png");
		ImageIO.write(croppedImage, "png", outputfile);
		System.out.println("Screenshot cropped with vercites 30, 70, 894, 368");
		}catch(IOException ie){
			System.out.println("Unable to Crop the image");
			ie.printStackTrace();
			throw ie;
		}
	}

	public static boolean compareImage(File fileA, File fileB) {
		try {
			// take buffer data from botm image files //
			BufferedImage biA = ImageIO.read(fileA);
			DataBuffer dbA = biA.getData().getDataBuffer();
			int sizeA = dbA.getSize();
			BufferedImage biB = ImageIO.read(fileB);
			DataBuffer dbB = biB.getData().getDataBuffer();
			int sizeB = dbB.getSize();
			// compare data-buffer objects //
			int i = 0;
			if (sizeA == sizeB) {
				for (; i < sizeA; i++) {
					if (dbA.getElem(i) != dbB.getElem(i)) {
						return false;
					}
				}

				System.out.println("" + ((i / sizeA) * 100));
				return true;
			} else {
				return false;
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Failed to compare image files ...");
			return false;
		}
	}

	public static boolean verifyFHRValues(List<Integer> inputfhrList,String parameterBlocck) throws Exception {
		boolean isfhrListplotted = false; 
		List<Integer> plottedFHRList = null;
		BufferedImage image;
		int width;
		int height;
		try {
			File input = new File("CroppedImage.png");
			image = ImageIO.read(input);
			width = image.getWidth();
			height = image.getHeight();
			System.out.println("RED " + new Color(image.getRGB(798, 54)).getRed());

			int inputListIndex = 0;
			int stabiliseTime = 60;
			Color c = null;
			boolean isFirstInputFound = false;
			DecimalFormat df = new DecimalFormat("#.00"); 
			double pixelsPerFhr = (double)height/210;
			
			for (int i = 0; i < width; i++) {
				plottedFHRList = new ArrayList<Integer>();

				for (int j = 0; j < height; j++) {
					c = new Color(image.getRGB(i, j));

					// System.out.println(c.getRGB())
					if(c.getRed() == 0 && c.getBlue() == 0 && c.getGreen() == 0){
						 
					}

					//US1 Parameter Block
					if(parameterBlocck.equals("US1")){
					if (Arrays.asList(-16221837, -15959179, -15959435, -15959692, -15959435, -15762057, -15696521,
							-15762571, -15565961, -15499912).contains(c.getRGB()) || (c.getRed() <= 50)) {

						// System.out.println("RED"+c.getRed()+" Blue
						// :"+c.getBlue());
						 
						int fhr = (int) ((height - j) / (Double)df.parse( df.format(pixelsPerFhr))) + 30;
						plottedFHRList.add(fhr);

					}
					}else if (parameterBlocck.equals("US2")){
						if (c.getBlue() <=20) {

							// System.out.println("RED"+c.getRed()+" Blue
							// :"+c.getBlue());
							 
							 Double pixelPerFHRinDouble = (Double)df.parse( df.format(pixelsPerFhr));
							int fhr = (int) ((height - j) /  pixelPerFHRinDouble)  + 30;
							plottedFHRList.add(fhr);

						}
					}

				}
				
				int firstFHR =0;
				int lastFhr =0;
				if (!plottedFHRList.isEmpty()) {
					  firstFHR = plottedFHRList.get(0);
					  lastFhr = plottedFHRList.get(plottedFHRList.size() - 1);
					if (firstFHR <= (inputfhrList.get(inputListIndex) + 5) && firstFHR >= (inputfhrList.get(inputListIndex) - 5)) {
						System.out.println("INPUT VALUE : " + inputfhrList.get(inputListIndex) + " MY TESTCASE PASSED (" + firstFHR + ", " + lastFhr + ")");
						stabiliseTime = 0;
						if(inputListIndex == 0){
							isFirstInputFound = true;
						}
						
						if (lastFhr != inputfhrList.get(inputListIndex)) {
							if(inputListIndex!= (inputfhrList.size()-1)){
								inputListIndex++;
							}

						}

					} else if (lastFhr <= (inputfhrList.get(inputListIndex) + 5)
							&& lastFhr >= (inputfhrList.get(inputListIndex) - 5)) {
						System.out.println("INPUT VALUE : " + inputfhrList.get(inputListIndex) + " MY TESTCASE PASSED ("
								+ firstFHR + ", " + lastFhr + ")");
						stabiliseTime = 0;
						if(inputListIndex == 0){
							isFirstInputFound = true;
						}
						if(inputListIndex!= (inputfhrList.size()-1)){
							inputListIndex++;
						}

					}else {
						if(isFirstInputFound == false)
						continue;
						
						if (firstFHR <= (inputfhrList.get(inputListIndex-1) + 5)
								&& firstFHR >= (inputfhrList.get(inputListIndex) - 5)) {
							stabiliseTime = 0;
							continue;
						} else if (lastFhr <= (inputfhrList.get(inputListIndex-1) + 5)
								&& lastFhr >= (inputfhrList.get(inputListIndex) - 5)) {
							stabiliseTime = 0;
							continue;
						} else 	if(stabiliseTime <= 52){
							 
							stabiliseTime++;
							continue;
						}else if (stabiliseTime > 52) {
							
							System.out.println("TestCase Failed due to stabilizing time more than 20 Seconds ");
							System.out.println("---------------------------------------------------------------");
							System.out.println("Input FHR VALUE is : "+inputfhrList.get(inputListIndex));
							System.out.println("First FHR VALUE is : "+ firstFHR);
							System.out.println("Last FHR VALUE is  : "+lastFhr);
							System.out.println("---------------------------------------------------------------");
							
							isfhrListplotted =false;
							break;
						}
					}

					stabiliseTime++;
					isfhrListplotted = true;
				}  else { 
					if(isFirstInputFound == false)
						continue;
					isfhrListplotted = false;
					System.out.println("TestCase Failed Because Pen Lift");
				} 
			}
		} catch (Exception e) {
			e.printStackTrace();
			throw e;
		}
		return isfhrListplotted;
	}

	public void moveFilesToBackup(boolean testCaseResult,List<String> screenShotNames ){
		InputStream inStream = null;
		OutputStream outStream = null;
		 Date dNow = new Date( );
	      SimpleDateFormat ft = 
	      new SimpleDateFormat ("yyyyMMddhhmm");
	      String time = ft.format(dNow);

	      final String curDir = System.getProperty("user.dir");
	    	try{
	    		File dir = new File(curDir+"/"+time);
	    		dir.mkdir();
	    		System.out.println(dir);
	    	 
	    	
	    		System.out.println("FolderName : "+dir.getName());
	    		for(String inputFile:screenShotNames){
	    	    File afile =new File(inputFile);
	    	    File bfile =new File(dir.getName()+"/"+time+""+inputFile);
	    		
	    	    inStream = new FileInputStream(afile);
	    	    outStream = new FileOutputStream(bfile);
	        	
	    	    byte[] buffer = new byte[1024];
	    		
	    	    int length;
	    	    //copy the file content in bytes 
	    	    while ((length = inStream.read(buffer)) > 0){
	    	  
	    	    	outStream.write(buffer, 0, length);
	    	 
	    	    }
	    	 
	    	    inStream.close();
	    	    outStream.close();
	    	    
	    	    //delete the original file
	    	    afile.delete();
	    	    
	    	    System.out.println("File is copied successful!");
	    		}
	    	}catch(IOException e){
	    	    e.printStackTrace();
	    	}
	}
	
	
	public void writePlottedFHRValuestoFile(String path,String content){

		 
		content = content.concat("List of plotted FHR Values : ");
	 
			content  = content.concat(content.toString()+"\r");
			
	 
		try {
		File file = new File(path);

		// if file doesnt exists, then create it
		if (!file.exists()) {
			file.createNewFile();
		}

		FileWriter fw;
		
			fw = new FileWriter(file.getAbsoluteFile());
		
		BufferedWriter bw = new BufferedWriter(fw);
		bw.write(content);
		bw.close();

		System.out.println("Done");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
		
	}
	
	public static void main(String[] args) throws Exception {
		cropImage();
		
	}
}
