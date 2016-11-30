package Steps;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.testng.AssertJUnit.assertEquals;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

import javax.imageio.ImageIO;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import cucumber.api.java.After;
import cucumber.api.java.Before;
import cucumber.api.Scenario;
import com.jacob.com.Variant;
import com.smartbear.cucumber.TestComplete;
import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;

public class TestEtymoALM {

	@Given("^i Run StepD$")
	public void TestEtymoALM_1() throws Throwable {
		// Write code here that turns the phrase above into concrete actions
		System.out.println("Step:i Run StepD");
	}

	@When("^i run StepD$")
	public void TestEtymoALM_2() throws Throwable {
		// Write code here that turns the phrase above into concrete actions
		System.out.println("Step:i Run StepD");
	}

	@Then("^i should expect StepD$")
	public void TestEtymoALM_3() throws Throwable {
		// // Write code here that turns the phrase above into concrete actions
		System.out.println("Step:i should expect StepD");
		assertEquals(true, true);
	}
	
	
	@Given("^i Run StepE$")
	public void TestEtymoALM_4() throws Throwable {
		// Write code here that turns the phrase above into concrete actions
		System.out.println("Step:i Run StepE");
	}

	@When("^i run StepE$")
	public void TestEtymoALM_5() throws Throwable {
		// Write code here that turns the phrase above into concrete actions
		System.out.println("Step:i Run StepE");
	}

	@Then("^i should expect StepE$")
	public void TestEtymoALM_6() throws Throwable {
		// // Write code here that turns the phrase above into concrete actions
		System.out.println("Step:i should expect StepE");
		assertEquals(true, false);
	}


	@After
	public void tearDown(Scenario scenario) throws IOException {
		if (takeScreenshot() == true) {
			final byte[] screenshot = getImageAsByteArray();
			scenario.embed(screenshot, "image/png");
		} else {
			System.out.println("Error in capturing the screenshot");
		}
	}

	public byte[] getImageAsByteArray() throws IOException {
		
		System.out.println(System.getProperty("user.dir"));
		ByteArrayOutputStream baos = new ByteArrayOutputStream(1000);
		BufferedImage img = ImageIO.read(new File(System.getProperty("user.dir"), "screencap.png"));
		ImageIO.write(img, "png", baos);
		baos.flush();

		String base64String = Base64.encode(baos.toByteArray());
		baos.close();

		byte[] bytearray = Base64.decode(base64String);
		return bytearray;
	}

	public boolean takeScreenshot() {
		boolean isSuccess = false;

		try {
			Process p = Runtime.getRuntime()
					.exec("cmd /c adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png");
			isSuccess = true;
			System.out.println(System.getProperty("user.dir"));
		} catch (IOException e1) {
			System.out.println("Exception Occured while capturing the screenshot");
			e1.printStackTrace();
			isSuccess = false;
		}
		System.out.println("ScreenshotCaptured");
		return isSuccess;
	}

}
