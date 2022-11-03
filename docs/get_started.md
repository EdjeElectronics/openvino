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
 
   <h4><a name="openvino-basics">OpenVINO Basics</a></h4>
   <p>Learn the basics of working with models and inference in OpenVINO. Begin with “Hello World” Interactive Tutorials that show how to prepare models, run inference, and retrieve results using the OpenVINO API. Then, explore other examples from the Open Model Zoo and OpenVINO Code Samples that can be adapted for your own application.</p>
   
   <div id="GSG_nextstepchoice">
      
   <h4><a href="tutorials.html">Interactive Tutorials - Jupyter Notebooks</a></h4>
      <p>Start with interactive Python tutorials that show the basics of model inferencing, the OpenVINO API, how to convert models to OpenVINO format, and more.</p>
      <ul>
         <li><a href="001-hello-world-with-output.html">Hello Image Classification</a> - Load an image classification model in OpenVINO and use it to apply a label to an image</li>
         <li><a href="002-openvino-api-with-output.html">OpenVINO Runtime API Tutorial</a> - Learn the basic Python API for working with models in OpenVINO</li>
         <li><a href="101-tensorflow-to-openvino-with-output.html">Convert TensorFlow Models to OpenVINO</a></li>
         <li><a href="102-pytorch-onnx-to-openvino-with-output.html">Convert PyTorch Models to OpenVINO</a></li>
      </ul>

   <h4><a href="openvino_docs_OV_UG_Samples_Overview.html">OpenVINO Code Samples</a></h4>
      <p>View sample code for various C++ and Python applications that can be used as a starting point for your own application. For C++ developers, step through the <a href="openvino_docs_get_started_get_started_demos.html">Basic OpenVINO Workflow</a> to learn how to build and run an image classification program that uses OpenVINO’s C++ API.</p>
      
   <h4><a href="openvino_docs_OV_UG_Integrate_OV_with_your_application.html">Integrate OpenVINO With Your Application</a></h4>
      <p>Learn how to use the OpenVINO API to implement an inference pipeline in your application.</p>
      
   </div>
   
    

   <div style="clear:both;"> </div>

@endsphinxdirective
