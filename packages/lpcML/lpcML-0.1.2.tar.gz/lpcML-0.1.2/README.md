# LPC ML

LPC ML is a tool developed in the CiTIUS, USC by the MODEV group for training a multi-layer perceptron (MLP) neural network to optimize and analyze the impact of different design parameters on laser power converters (LPCs) solar cells.

<img src="images/lpc.png" width="500">

**Fig.1:** GaAs-based horizontal laser power converter

Data used to feed the neural networks is shared in [data/hLPC_GaAS_5W_ml.csv](data/hLPC_GaAS_5W_ml.csv).

## Installation
First you need to have installed **pip3** on your system. For Ubuntu, open up a terminal and type:

    sudo apt update
    sudo apt install python3-pip

**Installation of lpcML via pip3**

Install the tool using pip3:

    pip3 install lpcML

and check the library is installed by importing it from a **python3 terminal**:

    import lpcML

Unless an error comes up, LPC ML is now installed on your environment.

> ⚠️ **WARNING** 
> If the module is already installed, make sure to upgrade it to the latest version before using it. 

    pip3 install lpcML --upgrade

> ❗ **CAUTION**  
> To ensure the versions compatibility and avoiding the *urllib3 (2.2.1) or chardet (4.0.0) doesn't match a supported version!* error use the following command:

    pip3 install --upgrade requests



## First Steps

To store the simulation data from optimizations or an iterative simulation process into a json file, you can use the [simulations_to_json.ipynb](simulations_to_json.ipynb) file.

An step by step example to train an MLP neural network model with the simplest output (one FoM) is reported in the jupyter notebook: [lpc_ml_calibration.ipynb](lpc_ml_calibration.ipynb).

You can find another example of a dynamic-ouptut (multiple FoMs) MLP neural network in [lpc_ml_calibration_multiplefoms.ipynb](lpc_ml_calibration_multiplefoms.ipynb)

The I-V curves can also be predicted by training an MLP model as shown in [lpc_ml_calibration_iv.ipynb](lpc_ml_calibration_.ipynb)