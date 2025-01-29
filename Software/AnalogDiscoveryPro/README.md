# WaveformWizards (Utrecht Experiment Design 2024-2025)
## Team
Martijn Teunissen, Tom de Wit & Stephen Yang

## Project
Pulse Design: creating the Python code for radiofrequency pulses using the Digilent Analog Discovery Pro 2230. This was part of the Experiment Design course at Utrecht University 2024-2025.

## Description
We have focussed on building up the code for the Digilent Analog Discovery 2 from scratch using Labphew. However, halfway through the project, we received the ADPro 2230 and continued our work with this device. 
Our code should provide the basis for being able to produce customizable waveform signals that will be sent through the RF coils. Then, it collects received data and does some analysis, like FFT or comparing decay times.
We have used the open source code from Redpitaya, MaRCoS, as well as other online sources as an example for 
what our signals should 
be able to do, and to see what kind of infrastructure the code itself should have. The main goal was to make 
spin echoes in hydrogen nuclei possible. However, we have also spent 
time on attempting free spin decay (FSD), also called free induction decay. 

## Potential users
Our Waveform Wizards code should allow later students to create customizable waveforms in an accessible way by adjusting parameters, which can then be used by the RF coils for MRI within low field. Then, it should be able to process the detected data using, for example Fourier transforms. This is essential for localizing the signals and creating distinguishable images. Later, other people may build upon our code to optimize its usage for detecting spin echoes in MRI. For example, frequency- and phase-encoding, and decoding the received signal are essential for being able to create a 2D MR image.

## Contributing
We are open to contributions to this project. For specific questions about our work, you may contact us. Also consider the contacts in the contacts.md file under the docs folder.

### Get Started: 1. Waveforms
- Download and install the WaveForms App from the [Digilent website](https://digilent.com/reference/software/waveforms/waveforms-3/getting-started-guide?srsltid=AfmBOooaJ09qz_NDtRdJEY9DOgeqVafgLIt8qAkdc28EIDsZJksaF6ml). This app will help you test and visualize waveforms with the Digilent device and the framework is needed in order to later connect to the device using Python.

### Get Started: 2. Conda environment
- Follow the [Conda tutorial](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) to create the environment necessary for connecting to the Digilent device using Python.
- Use the `environment.yml` file to create the environment with all required packages for data acquisition.


## Data Structure
The data folder contains example data that can be used with the provided scripts. This data is organized to align with the workflow of the project and facilitate easy access for measurement, processing, and analysis tasks. A Google Drive link with example data is available for users to download and set up their data structure.

- **`data/`**: Root folder for all experiment-related data.
  - **`free_spin_decay/`**: Contains data specific to the free induction decay experiments.
    - **`null/`**: Contains data where there is no sample in the setup.
    - **`sample/`**: Data from experiment with water sample in setup.
  - **`paramagnetic/`**: Contains data specific to experiments with a file in setup.
    - **`file_sample/`**: Data from experiment with file in setup.
    - **`null/`**: Contains data where there is no sample in the setup.
  - **`spin_echo/`**: Contains data specific to spin echo experiments.
    - **`fake/`**: Contains data from theoretical spin echo.
    

**Example Data Link**:  The example data provided via the Google Drive link demonstrates this structure and serves as a reference for setting up your experiments. Ensure that you download and place the files in the respective folders before running the scripts. https://drive.google.com/drive/folders/1Gm8FnW9RD147fiaXP4M2Zela7Wfxy8P3?usp=share_link


## License
This project is released under the MIT license. The license is listed under [LICENSE.md](./LICENSE.md) and available at https://choosealicense.com/licenses/mit/.
MIT License
Copyright (c) 2024 Martijn Teunissen, Tom de Wit & Stephen Yang

## Project status
Our work on this part of the project will finish at the end of January 2025, as the UED course comes to an end.