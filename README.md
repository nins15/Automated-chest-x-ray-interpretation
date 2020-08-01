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
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/structureofdirectory.png "Structure of dataset directory")
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/original%20images(1).png "Sample of images")
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Distribution%20of%20size.png "Size distribution of images")
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Distribution%20according%20to%20diseases.png "Distribution according to diseases")
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Percentageofnullvalues.png "Percentage of null values")

## Data Cleaning and Image Preprocessing
The training labels in the dataset for each observation are either 0 (negative), 1 (positive), or u (uncertain). The author of the dataset has suggested few ways to deal with the uncertain data these are 
* **U-Zeroes**: We map all instances of the uncertain label to 0.
* **U-Ones**: We map all instances of the uncertain label to 1.

We have used U-ones+LSR this means instad of mapping the uncertain labels to one we will map them to a value close to one we will select a value randomly between 0.55-0.85 . Similarly we have used U-zeros+LSR where we will map the uncertain valoes to a number randomly between 0-0.3.

The learning performance of deep neural networks on raw CXRs may be affected by the irrelevant noisy areas such as texts or the existence of irregular borders. Moreover, we observe a high ratio of CXRs that have poor alignment. we need to select only the useful part i.e. the part containing lungs. For that we will use lung finder which is a library for detecting lungs on chest x-ray images for further processing.
Sample of new images is
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/lungfinder.png "Lung finder")

## Model Building

We have used three models XceptionNet, InceptionRenetV2, EfficientNet and joined the last fully-connected layer which is a 5-dimensional dense layer, followed by sigmoid activations that were applied to each of the outputs to obtain the predicted probabilities of the presence of the 5 pathology classes.to obtain indicvidual probablities of each of the five classes. After training we have tested the data on testing dataset present in valid folder of the dataset.


![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Xception.png "Xception")
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/EfficientnetAUCcurve.png "Efficientnet")
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Inceptionbestauccurve.png "Inception")


## Ensembling
We used last layers of all the models and concatenated them
![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Ensembleimage.png "Ensemble")

## Model performance

![alt text](https://github.com/nins15/Automated-chest-x-ray-interpretation/blob/master/Ensemble_Xcep_Incep_Eff.png "EnsembleAUC")

