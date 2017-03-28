function Blood()
{
  //Runs the "app_debug" tested application.
  //TestedApps.app_debug.Run();
  //Specifies the mobile device as current for the test commands working with mobile devices.
  Mobile.SetCurrent("LOTUS");
  var visible = true;
  
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer, "Visible", cmpEqual, true);
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_label object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_label, "Visible", cmpEqual, true);
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_unit object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_unit, "Visible", cmpEqual, true);
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_alarmhighlimit object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_alarmhighlimit, "Visible", cmpEqual, true);
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_alarmlowlimit object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_alarmlowlimit, "Visible", cmpEqual, true);
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_value object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_value, "Visible", cmpEqual, true);
  //Checks whether the 'Visible' property of the Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_rightcontainer.ImageView_volumecontroller object equals True.
  aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_rightcontainer.ImageView_volumecontroller, "Visible", cmpEqual, true);
  
  return visible;
}

function Oxygen(spo2Value){
  
  var actualspo2Value = aqObject.CheckProperty(Aliases.Device.Process_mic_monitoring.RootLayout.Layout_normal_vitalblocks_container.Layout_mspo2_normal_vitalblock.Layout_mspo2_vital_block_normal.Layout_rl_mspo2_leftcontainer.TextView_tv_value, "mText", cmpEqual,spo2Value ) 
  Log.Message("actualspo2Value"+actualspo2Value);
  
  return actualspo2Value;
}
