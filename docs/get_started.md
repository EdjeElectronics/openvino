# Get Started {#get_started}

@sphinxdirective

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Install & Config
   
   Installing OpenVINO <openvino_docs_install_guides_overview>
   Additional Configurations <openvino_docs_install_guides_configurations_header>
   Uninstalling <openvino_docs_install_guides_uninstalling_openvino>
   Troubleshooting <openvino_docs_get_started_guide_troubleshooting>
   
.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Get Started Guides
   
   Interactive Tutorials (Python) <tutorials>
   Samples <openvino_docs_OV_UG_Samples_Overview>


@endsphinxdirective
 
@sphinxdirective
.. raw:: html

   <link rel="stylesheet" type="text/css" href="_static/css/getstarted_style.css">
   
   <p id="GSG_introtext">Welcome to OpenVINO! This guide introduces installation and learning materials for Intel® Distribution of OpenVINO™ toolkit. The guide walks through the following steps:<br />
     <a href="https://mybinder.org/v2/gh/openvinotoolkit/openvino_notebooks/HEAD?filepath=notebooks%2F201-vision-monodepth%2F201-vision-monodepth.ipynb" >Quick Start Example</a>
     <a href="openvino_docs_install_guides_overview.html" >Install OpenVINO</a>
     <a href="#learn-openvino" >Learn OpenVINO</a>
   </p>
   <div style="clear:both;"> </div> 
   
   <h3><a name="quick-start-example">1. Quick Start Example (No Installation Required)</a></h3>
   
   <img src="https://user-images.githubusercontent.com/15709723/127752390-f6aa371f-31b5-4846-84b9-18dd4f662406.gif">
   <p>Try out OpenVINO's capabilities with this quick start example that estimates depth in a scene using an OpenVINO monodepth model. <a href="https://mybinder.org/v2/gh/openvinotoolkit/openvino_notebooks/HEAD?filepath=notebooks%2F201-vision-monodepth%2F201-vision-monodepth.ipynb" >Run the example in a Jupyter Notebook inside your web browser</a> to quickly see how to load a model, prepare an image, inference the image, and display the result.</p>
   
   <h3><a name="install-openvino">2. Install OpenVINO</a></h3>
   
   <p>Visit the <a href="openvino_docs_install_guides_overview.html" >Install OpenVINO Overview page</a> to view options for installing OpenVINO and setting up a development environment on your device.</p>
   
      
   <h3><a name="get-started-tutorials">3. Learn OpenVINO</a></h3>
   
   <p>OpenVINO provides a wide array of examples and documentation showing how to work with models, run inference, and deploy applications. Step through the sections below to learn the basics of OpenVINO and explore its advanced optimization features. Visit <a href="documentation.html">OpenVINO’s documentation</a> for further details on how to use its features and tools.</p>
   
   <p>OpenVINO users of all experience levels can try <a href="https://www.intel.com/content/www/us/en/developer/tools/devcloud/edge/overview.html">Intel Dev Cloud</a>, a free web-based service for developing, testing, and running OpenVINO applications for free on an online cluster of the latest Intel hardware.</p>
 
   <h4>(a name="openvino-basics">OpenVINO Basics</a></h3>
   <p>Learn the basics of working with models and inference in OpenVINO. Begin with “Hello World” Interactive Tutorials that show how to prepare models, run inference, and retrieve results using the OpenVINO API. Then, explore other examples from the Open Model Zoo and OpenVINO Code Samples that can be adapted for your own application.</p>
   
   <div id="GSG_nextstepchoice">
      
      <h4><a href="tutorials.html"><h4>Interactive Tutorials - Jupyter Notebooks</h4>
         <p>Start with interactive Python tutorials that show the basics of model inferencing, the OpenVINO API, how to convert models to OpenVINO format, and more.</p>
         <ul>
            <li><a href="001-hello-world-with-output.html">Hello Image Classification</a> - Load an image classification model in OpenVINO and use it to apply a label to an image</li>
            <li><a href="002-openvino-api-with-output.html">OpenVINO Runtime API Tutorial</a> - Learn the basic Python API for working with models in OpenVINO</li>
            <li><a href="101-tensorflow-to-openvino-with-output.html">Convert TensorFlow Models to OpenVINO</a></li>
            <li><a href="102-pytorch-onnx-to-openvino-with-output.html">Convert PyTorch Models to OpenVINO</a></li>
         </ul>
         
         
         
     
     <a href="tutorials.html" >
        <h4>Interactive Tutorials - Jupyter Notebooks (Python) </h4>
        <p>Learn from a choice of interactive Python tutorials targeting typical OpenVINO use cases.</p>
     </a> 		
     <a href="openvino_docs_OV_UG_Samples_Overview.html" >
        <h4>OpenVINO Samples	</h4>
        <p>See ready-made applications explaining OpenVINO features and various use-cases.		</p>
     </a> 
     <a href="openvino_inference_engine_ie_bridges_python_sample_speech_sample_README.html" >
        <h4>Reference Implementation For Speech Recognition Apps (Python)</h4>
        <p>Use a speech recognition demo and Kaldi model conversion tool as reference. </p>
     </a>
     <a href="openvino_inference_engine_samples_speech_sample_README.html" >
        <h4>Reference Implementation For Speech Recognition Apps (C++)</h4>
        <p>Use a speech recognition demo and Kaldi model conversion tool as reference. </p>
     </a>
     <a href="omz_demos.html" >
        <h4>Open Model Zoo Demo Applications</h4>
        <p>See Open Model Zoo demo applications to use robust application templates for implementing specific deep learning scenarios. </p>
     </a>
     <a href="http://devcloud.intel.com/edge/" >
        <h4>Intel® DevCloud 	</h4>
        <p>Develop, test, and run your OpenVINO solution for free on a cluster of the latest Intel® hardware. </p>
     </a> 
   </div>
   <div style="clear:both;"> </div>

@endsphinxdirective
