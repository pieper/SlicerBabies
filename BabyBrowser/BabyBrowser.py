import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

#
# BabyBrowser
#

class BabyBrowser(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "BabyBrowser" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Pediatric Neuroradiology"]
    self.parent.dependencies = []
    self.parent.contributors = ["Steve Pieper (Isomics, Inc.)"]
    self.parent.helpText = """
    A browser for the MGH ADC Atlas v1.0.0
    """
    self.parent.acknowledgementText = """
    This work is supported by 1R01EB014947-01 MI2B2 ENABLED PEDIATRIC RADIOLOGICAL DECISION SUPPORT

    See: https://www.nmr.mgh.harvard.edu/lab/mi2b2

    Y Ou, N Reynolds, R Gollub,, R Pienaar, Y Wang, T Wang, D Sack, K Andriole, S Pieper, C Herrick, S Murphy, P Grant, L Zollei, "Developmental Brain ADC Atlas Creation From Clinical Images". Organization for Human Brain Mapping (OHBM). (2014)  [PDF: http://www.nmr.mgh.harvard.edu/~you2/publications/BabyAtlasing_OHBM14.pdf]

    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# BabyBrowserWidget
#

class BabyBrowserWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # scale factor for screen shots
    #
    self.screenshotScaleFactorSliderWidget = ctk.ctkSliderWidget()
    self.screenshotScaleFactorSliderWidget.singleStep = 1.0
    self.screenshotScaleFactorSliderWidget.minimum = 1.0
    self.screenshotScaleFactorSliderWidget.maximum = 50.0
    self.screenshotScaleFactorSliderWidget.value = 1.0
    self.screenshotScaleFactorSliderWidget.setToolTip("Set scale factor for the screen shots.")
    parametersFormLayout.addRow("Screenshot scale factor", self.screenshotScaleFactorSliderWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = BabyBrowserLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    screenshotScaleFactor = int(self.screenshotScaleFactorSliderWidget.value)
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), enableScreenshotsFlag,screenshotScaleFactor)


#
# BabyBrowserLogic
#

class BabyBrowserLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, atlasPath=None):
    self.atlasPath = atlasPath
    if not self.atlasPath:
      atlasBasePath = '/Users/pieper/data/babybrain/MGH_ADC_Atlases_v1.0.0'
    self.atlasPath = '/Users/pieper/data/babybrain'
    developmentalDirPath = os.path.join(self.atlasPath, 'babyBrain/MGH_ADC_Atlases_registered_4Ddramms')
    self.developmentalPath = os.path.join(developmentalDirPath, 'reg_allatlases_dramms4D.nii')
    self.volumeTypes = [ "", "_stdev" ]
    self.timePoints = [ "week0-1",
                        "quarter0_excludingweek0",
                        "quarter1",
                        "quarter2",
                        "quarter3",
                        "year1-2",
                        "year2-3",
                        "year3-4",
                        "year4-5",
                        "year5-6",
                        ]
    self.volumesByTypeAndAge = {}


  def loadAtlas(self):
    registeredAtlasPath = os.path.join(self.atlasPath, "atlases_rigidregistered")
    for volumeType in self.volumeTypes:
      for timePoint in self.timePoints:
        fileName = "atlas_%s%s_rigidtoyear1-2.nii.gz" % (timePoint, volumeType)
        volumePath = os.path.join(registeredAtlasPath, fileName)
        self.delayDisplay('loading: %s' % fileName, 50)
        success,node = slicer.util.loadVolume(volumePath, returnNode=True)
        if not success:
          raise Exception('could not load', volumePath)
        self.volumesByTypeAndAge[volumeType,timePoint] = node


  def loadDevelopmentalAtlas(self):
    import numpy

    # get the header - this reader doesn't support 4D
    # but can query the header.
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(self.developmentalPath)
    reader.Update()
    niftiHeader = reader.GetNIFTIHeader()

    print(self.developmentalPath)
    if niftiHeader.GetDataType() != 16:
      print (niftiHeader.GetDataType())
      raise Exception('Can only load float data')

    # create the correct size and shape vtkImageData
    columns = niftiHeader.GetDim(1)
    rows = niftiHeader.GetDim(2)
    slices = niftiHeader.GetDim(3)
    frames = niftiHeader.GetDim(4)

    fp = open(self.developmentalPath, 'rb')
    headerThrowaway = fp.read(niftiHeader.GetVoxOffset())
    niiArray = numpy.fromfile(fp, numpy.dtype('float32'))

    niiShape = (frames, slices, rows, columns)
    niiArray = niiArray.reshape(niiShape)

    image = vtk.vtkImageData()
    image.SetDimensions(columns, rows, slices)
    image.AllocateScalars(vtk.VTK_FLOAT, frames)
    from vtk.util.numpy_support import vtk_to_numpy
    imageShape = (slices, rows, columns, frames)
    imageArray = vtk_to_numpy(image.GetPointData().GetScalars()).reshape(imageShape)

    # copy the data from numpy to vtk (need to shuffle frames to components)
    for frame in range(frames):
      imageArray[:,:,:,frame] = niiArray[frame]

    # create the multivolume node and display it
    multiVolumeNode = slicer.vtkMRMLMultiVolumeNode()

    multiVolumeNode.SetScene(slicer.mrmlScene)

    multiVolumeDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
    multiVolumeDisplayNode.SetReferenceCount(multiVolumeDisplayNode.GetReferenceCount()-1)
    multiVolumeDisplayNode.SetScene(slicer.mrmlScene)
    multiVolumeDisplayNode.SetDefaultColorMap()
    slicer.mrmlScene.AddNode(multiVolumeDisplayNode)

    multiVolumeNode.SetAndObserveDisplayNodeID(multiVolumeDisplayNode.GetID())
    multiVolumeNode.SetAndObserveImageData(image)
    multiVolumeNode.SetNumberOfFrames(frames)
    multiVolumeNode.SetName("DevelopmentalAtlas")
    multiVolumeNode.SetAttribute("MultiVolume.FrameLabels", str(self.timePoints)[1:-1])
    slicer.mrmlScene.AddNode(multiVolumeNode)

    return multiVolumeNode


class BabyBrowserTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_BabyBrowser1()

  def test_BabyBrowser1(self):
    """Load the data"""

    self.delayDisplay("Starting the test",100)

    logic = BabyBrowserLogic()

    self.delayDisplay("Loading registered atlas",100)
    logic.loadDevelopmentalAtlas()

    self.delayDisplay("Loading native space atlas",100)
    logic.loadAtlas()

    #
    # automatically select the volume to display
    #
    appLogic = slicer.app.applicationLogic()
    selNode = appLogic.GetSelectionNode()
    selNode.SetReferenceActiveVolumeID(multiVolumeNode.GetID())
    appLogic.PropagateVolumeSelection()





    self.delayDisplay('Test passed!')
