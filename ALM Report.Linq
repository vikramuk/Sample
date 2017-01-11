
Document Number	<<[CommonFields.First().DocumentId]>>
Title	<<[CommonFields.First().Title]>>
Path	<<[CommonFields.First().Path]>>
Type	<<[CommonFields.First().ReportType]>>

<<foreach [testSet in TestSets]>><<[Name]>>
Signer	Meaning	Date/Time
<<foreach [signature in ds.TestSetSignatures.Where(s => s.Name == testSet.Name)]>><<[signature.Signer]>>	<<[signature.Meaning]>>	<<[signature.DateTime]>><</foreach>>

<</foreach>>

 
Table of Contentsa
No table of contents entries found.
1	Document Information
<<[CommonFields.First().Description] -html>>
<<foreach [attachmentItem in TestSetFolderAttachments]>>
Test Set Folder Attachment: <<[attachmentItem.Name]>> 
<</foreach>>
2	Test Information
2.1	<<foreach [testSet in TestSets]>>Test Set - <<[Name]>> (ID:<<[TestSetID]>>)
<<[Description] -html>>
2.1.1	 <<foreach [testInstance in ds.TestInstances.Where(i => i.TC_CYCLE_ID == testSet.TestSetID)]>>Test Instance - <<[Name]>>
Status: <<[ExecutionStatus]>>
Trace ID: <<[Test]>>
Description:
<<[ds.Tests.First(t => t.TestID == Test).Description] -html>>
<<if [Justification != “”]>>Justification: <<[Justification]>><</if>>
<<if [ds.Runs.Count(r => r.TestInstance == TC_CYCLE_ID) == 0]>>No Run -- Test Info
<<if [!ds.DesignSteps.Any()]>>No Steps
<<else>>Steps:
Step Name	Description	Expected	Actual
<<foreach [step in ds.DesignSteps.Where(s => s.TestInstanceID == TestInstanceUniqueID)]>><<[StepName]>>	<<[Description] -html>>
	<<[Expected] -html>>
	<<[Actual] -html>><</foreach>>
<<foreach [attachment in ds.DesignStepAttachments.Where(s => s.TestInstanceID == TestInstanceUniqueID)]>>
<<[Name]>>
 
<</foreach>><</if>><<else>>Exec Date: <<[ds.Runs.Last(r => r.TestInstance == TC_CYCLE_ID).ExecDate]>>
Run Name: <<[ds.Runs.Last(r => r.TestInstance == TC_CYCLE_ID).RunName]>>
Tester: <<[ds.Runs.Last(r => r.TestInstance == TC_CYCLE_ID).Tester]>>
Step Name	Description	Expected	Actual
<<foreach [step in ds.RunSteps.Where(s => s.RunID == ds.Runs.Last(r => r.TestInstance == TC_CYCLE_ID).RunID)]>><<[StepName]>>	<<[Description] -html>>
	<<[Expected] -html>>
	<<[Actual] -html>><</foreach>>
<<foreach [attachment in ds.RunStepAttachments.Where(s => s.RunID == ds.Runs.Last(r => r.TestInstance == TC_CYCLE_ID).RunID)]>>
<<[Name]>>
 
<</foreach>><</if>><</foreach>><</foreach>>



