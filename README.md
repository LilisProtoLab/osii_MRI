# OSII Mini 

![Zach_magnet](./Docs/Images/Magnet_Zach.jpg)

Documentation for building the open source ultra low-field MRI for education

Magnetic Resonance Imaging (MRI) is one of the most powerful and versatile non-invasive medical imaging devices. 
Ultra low-field MRI scanners such as __OSII One__ have recently reached the maturity level of [attempting eligibility for standardization and medical certification](https://www.opensourceimaging.org/). 
These open source projects has pooled the knowledge and experience of many experts and can be built and maintained for a fraction of the price of current instruments. 

This educational project is a collaboration initiated by the [Lili's Proto Lab](https://www.uu.nl/lpl) with the aim of preparing a hands-on workshop for student teams to replicated an OSII-inspired functioning MRI.
Student teams can be a great force in progressing this field. 
Collectively, they can enhance the accuracy and utility of open-source MRI devices through rigorous calibration procedures, iterative testing, and collaboration with experts in both engineering and medical fields.  

## Getting started

These are the essential elements for creating a magnetic resonance image:
+ A uniform magenetic field B0
+ Coils for creating field gradients in x, y, and z -directions
+ Coils for sending and recieving pulses
+ Electronics for creating the imaging pulse sequences
+ Software to control the sequences and reconstructing the images

In this repository, we have split the steps into independent experiments so that one can start building each of the elements and persome some benchmark measurements.

## Building the main magnet
To create a uniform base field, we use the [Halbach Array](https://en.wikipedia.org/wiki/Halbach_array) construction. Check these [build instructions](./Docs/FrameAssembly) and [design files](./Build/HalbachFrame).

The current design is adopted from the OSII mini magnet designed by Dr. Joshua Harper from [Sustainable MRI Lab](smrilab.com) and Thomas O'Reilly and [Andrew Webb at Leiden University](https://www.universiteitleiden.nl/en/staffmembers/andrew-webb#tab-2). The main change in our design is using lids for keeping small magnets in place instead glueing them.  

__The Halbach Frame:__
	+ 120 mm inner diameter 
	+ DSV 100 x100 x100 mm
	+ 396 magnets 12x12x12 mm
	+ 50 mT
	+ around 1200 Euros for a completed magnet
	
### Verifying the field uniformity
To achieve MR imaging, the base magnetic field must be uniform. Based on experience, the maximum allowed field inhomgeneity is 3000 ppm. The field uniformity can be checked with a 3D scanner. [See instructions](./Docs/Fieldscanner) forconverting a 3D printer into such a scanner.

### Shimming the main magnet
The uncorrected fluctuations in Halbach with only big 6x6x6 mm magnets can be as high as 15000 ppm. This uniformity must be improved by adding extra magnets in a process called [shimming](./Docs/Shimming). 
Because of this process, each Halbach assembly is unique.

### Gradient coils
To create a three dimensional MRI, the spatial information must be [encoded in time, frequency and phase response](https://mriquestions.com/how-to-locate-signals.html#/) along these orthogonal axes. This encodig requires controlling applying various field gradients, dynamically. This encoding is done with 3 gradient coils. Check these [build instructions](./Build/GradientCoils).

### Send and recieve circuitry
MRI is based on measuring quantum effect called the spin echo. In short, the water molecules can be excited in a way that they emit a a measurable radio frequency signal at a specific delay after their excitation. The excitation pulse can be much stronger than the echo pulse, and therfore delicate circuitry is necessary to separate the spin echo from other possible spurious signals. Check these [design consideration](./Docs/RFCoils)

### The MRI console
In MRI literature, all the electronic boards that are used for generating and analyzing the required RF sequences are collectively called the MRI console. Once a uniform B0 is constructed and proper RF coils are embedded in the assembly frame, in principle the setup can be combined with suitable commercial or open source consoles. Here is a list of consoles that have been tested with various low-field MRI devices.

+ [Kea2](https://magritek.com/products/kea/) provided by magritek
+ [OCRA](https://openmri.github.io/ocra/) built on top of [STEMlab/Red Pitaya](https://www.redpitaya.com/f130/STEMlab-board)

## Latest news

The build instructions for the gluefree Halbach magnet are posted in the [Build](./Build/HalbachFrame) folder.

## Outcomes

Our main goal to support the student teams who collaborate in replicating this low field MRI. 
In parallel, all outputs of this collaboration will be shared with the sister MRI project such as the OSII ONE. 

## Team

+ Utrecht University, Lilis Proto Lab:
	+ Project lead: Sanli Faez
	+ Contributors: Zachary Meredith, Low Field Legends (Experiment Design class of 2024)

+ Universidad Paraguayo Alemana: 
	+ Project lead: Joshua Harper
	+ Contributors: Rodney Rojas

+ NIST Boulder: 
	+ Project lead: Stephen Ogier
	+ Contributors: Katy Keenan

+ New York University, Interactive Telecommunications Program:
	+ Greg Shakar
	
## MRI Resources
More information about MRIs and their operations can be found below:
+ [MRI Questions website maintained by Allen D. Elster](https://mriquestions.com/index.html)
+ [OSI<sup>2</sup> Repository:](https://gitlab.com/osii) Here you can find additional information about the original OSI<sup>2</sup> ONE

### Related projects
Several groups worldwide have succeeded in replicating this device or have created similar designs. 

+ [OSI2 ONE MR Scanner](https://www.opensourceimaging.org/project/osii-one/)
+ [OCRA Console](https://openmri.github.io/ocra/)
+ [Earth-field NMR](https://phas.ubc.ca/~michal/Earthsfield/) 
+ [Hallbach Magnet designer](https://github.com/menkueclab/HalbachMRIDesigner)
+ [Table top MRI scanner](https://tabletop.martinos.org/index.php/Main_Page)
+ [Open Source relaxometry](https://github.com/mtwieg/NMR)

We would like to keep a curated list of open source low-field MRI projects. If you know of a project that has to be added to this list, send us a message or create a pull request.

For a long list of somewhat related open source hardware and software projects check [Open Source Imaging Initiative, OSI²](https://www.opensourceimaging.org/)


## Get involved

We don't accept pull request at this moment. Our goal is to open up for external contributions after November 2024 

This is a bottom-up initiative and participation in the project is on a voluntary basis. If you share the vision and goals of this initiative, we welcome all your compassionate support. 

You can support this initiative by any or all these options:
-	Recommending this workshop to enthusiastic students* in your institute.
-	Providing support, mentorship and expert advice to students who participate.
-	Hosting student teams in your lab/institute after the workshop for enhancing their builds.
-	Contributing to the preparation of the workshop with time, funding, or student assistants.
-	Financial support for purchasing the build materials.

Please contatct Sanli, @sanlifaez, for any inquiries.

## License

This project is licensed under [CERN Open Hardware Licence Version 2 - Weakly Reciprocal](./LICENSE).
Licenses of the individual modules of OSI² ONE that are used without alteration apply accordingly.

## (Funding)

This project has recieved an Open Science Hacker grant from the Lili's Proto Lab

![LPL sharing image](./Docs/Images/lpl_sharing.jpg)
