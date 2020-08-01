# Automated chest x-ray interpretation:Project review
* Created a CNN model for detecting 5 diseases which are Cardiomegaly,Edema,Consolidation,Atelectasis,Pleural Effusion
* Removed the redundant parts from the image like shoulder or text using a library that can detect lungs on chest x-rays
* Mapped the uncertain values in the csv using LSR(Label smoothning regression).
* Trained a number of CNN models on all the images like XceptionNet, EfficientNet, InceptionResNetV2, DenseNet etc. to identify multiple labels for each class.
* Three models with best AUC were chosen for ensembelling by concatinating the last layers of each model.
## Code and Resources Used
* **Python version**: 3.6.9
* **Packages**: Pandas,matplotlib,numpy,cv2,tensorflow,keras,sklearn,tqdm
* **Requrements for using lung finder**: pip install lungs-finder
* **Requirements for using EfficientNet**: pip install keras_efficientnets
* **Dataset Download**: wget http://download.cs.stanford.edu/deep/CheXpert-v1.0-small.zip
## EDA 
* Structure of Dataset directory
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/structureofdirectory.png "Structure of dataset directory")
* Sample of images
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/original%20images(1).png "Sample of images")
